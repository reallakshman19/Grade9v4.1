"""Reconcile the immutable Chemistry R00 audit with a later author-correction delta.

These tests validate statuses and reference discipline, NOT scientific validity or a
cold independent QRT judgment. The referenced B02 branch is not in this PR tree.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs" / "audits" / "chemistry-c01-c14"

def test_post_r00_delta_preserves_snapshot_and_no_automatic_pass():
    m = json.loads((ROOT / "CHEMISTRY_C01_C14_EVIDENCE_MATRIX_R1.json").read_text())
    d = json.loads((ROOT / "CHEMISTRY_C01_C14_POST_R00_CORRECTION_DELTA_R2.json").read_text())
    original = {r["subtopic_id"] for r in m["rows"] if r["qualification_disposition"] == "FAIL"}
    expected = {"CHEM-C11.05", "CHEM-C14.01", "CHEM-C14.05"}
    assert original == expected
    assert {r["subtopic_id"] for r in d["corrections"]} == expected
    assert d["baseline"]["original_r00_status"] == {"PASS":0,"FAIL":3,"HOLD":81}
    assert d["post_correction"]["independently_qualified_subtopics"] == 0
    assert d["post_correction"]["qualification_status"] == "HOLD"
    assert all(r["candidate_status"] == "AUTHOR_CANDIDATE_REMEDIATED" and r["academic_status"] == "R01_R02_HOLD" for r in d["corrections"])
    assert all(r["files"] and all(len(f["blob_sha"]) == 40 for f in r["files"]) for r in d["corrections"])
    assert d["correction_source"]["verified_head"] != d["baseline"]["audit_head"]

def test_old_gap_register_remains_custodial():
    g = json.loads((ROOT / "CHEMISTRY_MISSING_CONTENT_AND_GATES_R1.json").read_text())
    old = {x["id"]:x for x in g["issues"]}
    assert len(old) == 14
    for item in ("CHEM-FC-001","CHEM-FC-002","CHEM-FC-013"):
        assert old[item]["status"] == "FAIL"

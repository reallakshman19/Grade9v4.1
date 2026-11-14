"""Post-PH02 132-row matrix reconciliation preserves historical audit and source identities."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R0=ROOT/"review/physics/ph01-ph12-full-coverage-r00/PHYSICS_PH01_PH12_EVIDENCE_R00.v1.json"
R1=ROOT/"review/physics/ph01-ph12-full-coverage-r1/PHYSICS_PH01_PH12_EVIDENCE_R1.v1.json"
G1=ROOT/"review/physics/ph01-ph12-full-coverage-r1/PHYSICS_PH01_PH12_GAPS_R1.v1.json"


def test_ph02_r1_reconciles_eight_pairs_preserving_132_denominator():
    old=json.loads(R0.read_text(encoding="utf-8"))
    new=json.loads(R1.read_text(encoding="utf-8"))
    gaps=json.loads(G1.read_text(encoding="utf-8"))
    assert len(old["rows"])==len(new["rows"])==len(gaps["row_gaps"])==132
    assert old["summary"]["dedicated_core1a"]==62
    assert new["summary"]["dedicated_core1a"]==70
    assert new["summary"]["dedicated_core1b"]==70
    assert new["summary"]["remaining_missing_dedicated"]==62
    assert new["summary"]["source_admitted"]==0
    assert new["based_on"]["independent_review"] is False
    ph02=[r for r in new["rows"] if r["topic_id"]=="PH02"]
    assert len(ph02)==8
    for r in ph02:
        assert all(r["presence"][k] for k in ("chapter_draft","dedicated_core1a","dedicated_core1b"))
        assert r["audit_result"]=="OWNER_DIRECTED_AUTHORED_STUDY_READY"
        assert r["source"]["exact_original_exam_admission"]=="NOT_CLAIMED"
        assert r["qrt"]["independent_qrt"].startswith("NOT_CLAIMED")
        assert r["qrt"]["authored_cycles"]==3
        for kind in ("core1a","core1b"):
            f=r["evidence"][kind]
            assert (ROOT/f["path"]).is_file()
            assert r["subtopic_id"][-3:] in f["path"]
        assert any(x["subtopic_id"]==r["subtopic_id"] and not x["missing"]
                   for x in gaps["row_gaps"])

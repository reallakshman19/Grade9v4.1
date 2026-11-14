"""Reviewer-only ledger: complete scope inventory, immutable pins and no source admission."""
import hashlib,json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
PH="nsejs/physics/curriculum/agent1/PH01/"
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def test_coverage_ledger_inventory_and_pins():
    a=read(PH+"ph01-coverage-review.r4_6.json")
    for pin in a["pins"].values():assert blob(pin["path"])==pin["blob"]
    q={x["question_uid"]:x for x in read(a["pins"]["registry"]["path"])["questions"] if x["subject"]=="PHYSICS"}
    rows=a["registry_dispositions"]
    assert len(rows)==len(q)==95 and set(x["question_uid"] for x in rows)==set(q)
    assert all(q[x["question_uid"]]["content_revision_sha256"]==x["content_revision_sha256"] and x["authentication"]=="HOLD" for x in rows)
    assert Counter(x["disposition"] for x in rows)==a["statistics"]["registry_dispositions"]
    ext=a["external_2025_dispositions"]
    assert len(ext)==20 and len({x["locator"] for x in ext})==20
    assert all(x["canonical_uid"] is None and x["bank_id"] is None and x["authentication"]=="HOLD" for x in ext)
    assert Counter(x["disposition"] for x in ext)==a["statistics"]["external_2025_dispositions"]
    assert sum(x["transfer_cycle_id"] is not None for x in ext)==4
def test_coverage_association_and_role_reconciliation():
    a=read(PH+"ph01-coverage-review.r4_6.json")
    m=read(a["pins"]["map"]["path"]);p=read(a["pins"]["package"]["path"])
    cycles={x["id"]:x for x in p["core1b"]}
    expected={(x["id"],z["cycle_id"]):z for x in m["records"] for z in x["preparation"]}
    observed={(x["source_locator"],x["cycle_id"]):x for x in a["association_review"]}
    assert len(expected)==len(observed)==87 and set(expected)==set(observed)
    assert Counter(x["author_disposition"] for x in observed.values())==a["statistics"]["association_dispositions"]
    for k,z in observed.items():
        assert z["qrt_target_id"]==expected[k]["qrt_target_id"]==cycles[z["cycle_id"]]["qrt_target_id"]
        assert z["task_w"]==cycles[z["cycle_id"]]["protected_work"] and z["exact_fit"]=="HOLD"
    for rec in a["linked_source_review"]:
        source=next(x for x in m["records"] if x["id"]==rec["source_locator"])
        assert rec["canonical_records"]==source["canonical_records"] and rec["bank_record"]==source["bank_record"]
        if rec["role"]=="DROPPED_NOT_COVERAGE_CREDIT":
            assert not rec["focused_cycle_ids"]
            assert all(x["author_disposition"]=="STUDY_ONLY_DROPPED" for x in observed.values() if x["source_locator"]==rec["source_locator"])
    assert a["statistics"]["authenticated_core2"]==a["statistics"]["independently_qualified_qrts"]==0 and a["release"]=="HOLD"

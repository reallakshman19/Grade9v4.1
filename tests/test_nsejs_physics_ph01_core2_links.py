"""Candidate exact identity links, never academic admission."""
import hashlib,json
from pathlib import Path
from tools.ph01_source_pin_custody import pinned_blob_sha, pinned_json
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def test_ph01_core2_existing_records():
    m=read("nsejs/physics/curriculum/agent1/PH01/ph01-core2-construction-map.r4_1.json")
    assert m["counts"]=={"locators":11,"canonical_records":12,"bank_records":4,"primary":6,"cross_topic":4,"dropped":1,"qualified":0}
    for k in ("canonical","candidate_bank","integrity"):
        x=m["source_inventory"][k]
        assert pinned_blob_sha(ROOT,x)==x["git_blob_sha"]
    c={q["question_uid"]:q for q in read("nsejs/core2/question-map.v1.json")["questions"]}
    b={q["question_uid"]:q for q in pinned_json(ROOT,m["source_inventory"]["integrity"])["items"]}
    for r in m["records"]:
        assert r["source_status"]==r["exact_fit"]=="HOLD"
        for q in r["canonical_records"]:assert c[q["question_uid"]]["content_revision_sha256"]==q["content_revision_sha256"]
        if r["bank_record"]:
            q=r["bank_record"];assert b[q["question_uid"]]["observed_question_revision_sha256"]==q["observed_question_revision_sha256"]
        for q in r["preparation"]:
            assert (ROOT/q["core1a"]).is_file() and (ROOT/q["core1b"]).is_file()
    assert len(next(r for r in m["records"] if r["id"]=="PH01-LINK-2024-51-Q46")["canonical_records"])==2
    assert next(r for r in m["records"] if r["id"]=="PH01-LINK-2022-51-Q45")["role"]=="DROPPED_NOT_COVERAGE_CREDIT"

"""Mechanical source-pointer test for Chemistry C08-C14 R00 B4 screen.
Does NOT determine learning sufficiency or certify D3/D4.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs/audits/chemistry-c08-c14/CHEMISTRY_C08_C14_B4_REVIEW_REGISTER_R1.json"
BASE=ROOT/"curriculum/chemistry/agent-b"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_c08_c14_b4_screen_is_bounded_and_source_anchored():
    audit=load(AUDIT)
    assert audit["base_main_sha"]=="7a5c425f02d8a365a738bb11df1982cbe38e9f82"
    assert audit["academic_disposition"]=="HOLD"
    assert audit["inventory"]=={"units":7,"subtopics":40,"core1b_cycles":120,
        "qrt_bands_independently_qualified":0,"findings":17}
    books={}
    cycles={}
    for i in range(8,15):
        u=f"C{i:02d}"
        b=load(BASE/"learner"/f"{u}.reader.v0.1.0.json")
        c=load(BASE/"core1b"/f"{u}.core1b.v0.1.0.json")
        assert b["academic_status"]=="DRAFT_ACADEMIC_HOLD"
        assert c["release"]["qrt_adjudication"]=="HOLD"
        books[u]={s["id"]:s for s in b["sections"]}
        cycles[u]={x["cycle_id"]:x for x in c["cycles"]}
        assert len(cycles[u])==3*len(books[u])
    assert sum(map(len,books.values()))==40
    assert sum(map(len,cycles.values()))==120
    assert len(audit["findings"])==17
    assert len({f["cycle_id"] for f in audit["findings"]})==17
    for f in audit["findings"]:
        u=f["unit_id"]
        book=books[u][f["subtopic_id"]]
        task=cycles[u][f["cycle_id"]]
        assert task["subtopic_ref"]==f["subtopic_id"]
        assert f["worked_anchor"] in book["worked"]
        assert f["prompt_anchor"] not in task["attempt"]["prompt"]\n        assert len(task["attempt"]["post_commit_closure"]["model_response"])>120\n        assert task["attempt"]["protected_W"] != "The learner independently completes the causal bridge, not exposed before first attempt."
        assert task["source_role"]=="AUTHORED_PRACTICE"
        assert task["academic_status"]!="APPROVED"
        assert f["status"]=="B4_REVIEW_REQUIRED"
        assert f["academic_disposition"]=="HOLD"

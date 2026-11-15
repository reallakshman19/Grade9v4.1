"""WPE-parity Chemistry R3 source-to-task before/after regression, not academic certification."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/"curriculum"/"chemistry"/"agent-b"
A=ROOT/"curriculum"/"chemistry"/"adapters"
AUD=ROOT/"docs"/"audits"/"chemistry-c08-c14"

def get(path): return json.loads(path.read_text(encoding="utf-8"))

def test_seventeen_exact_fixed_id_changed_condition_candidates_and_original_baseline():
    old=get(AUD/"CHEMISTRY_C08_C14_B4_REVIEW_REGISTER_R1.json")
    delta=get(AUD/"CHEMISTRY_C08_C14_REMEDIATION_DELTA_R3.json")
    assert len(old["findings"])==len(delta["changes"])==17
    assert delta["counts"]["generic_protected_W_before"]==79
    assert delta["counts"]["generic_protected_W_after"]==0
    assert {x["cycle_id"] for x in old["findings"]}=={x["cycle_id"] for x in delta["changes"]}
    for x in delta["changes"]:
        cycles=get(B/"core1b"/f"{x['unit_id']}.core1b.v0.1.0.json")["cycles"]
        task=next(t for t in cycles if t["cycle_id"]==x["cycle_id"])
        assert task["attempt"]["prompt"]==x["current_authored_attempt"]
        assert task["attempt"]["protected_W"]==x["current_protected_W"]
        assert task["attempt"]["post_commit_closure"]["model_response"]==x["current_model_response"]
        assert task["boundary_test"]["prompt"]==x["current_boundary"]
        assert x["prior_core1b_anchor"] not in task["attempt"]["prompt"]
        assert len(task["attempt"]["post_commit_closure"]["model_response"])>=130
        assert len({h["text"] for h in task["attempt"]["hints"]})==3
        assert [h["id"] for h in task["attempt"]["hints"]]==["H1","H2","H3"]
        assert all(s in task for s in ("predict","attempt","reconstruct","diagnose","repair","boundary_test"))
        assert task["academic_status"]=="AUTHOR_CANDIDATE_REQUIRES_INDEPENDENT_REVIEW"
        assert all(v=="UNREVIEWED" for v in task["reviews"].values())
        assert x["independent_science"]==x["independent_QRT"]=="NOT_RUN"

def test_reader_and_manuscript_scientific_bridges_were_added():
    expected={"C08":4,"C09":2,"C12":4,"C13":1,"C14":3}
    count=0
    for u,n in expected.items():
        book=get(B/"learner"/f"{u}.reader.v0.1.0.json")
        new=[s for s in book["sections"] if any("different" in x.lower() or "ledger" in x.lower() or "measur" in x.lower() for x in s["teaching"])]
        assert len(new)>=n
        manuscript=(B/"textbook"/f"{u}.core1a.md").read_text(encoding="utf-8")
        assert manuscript.count("Model-selection bridge (authored teaching)")>=n
        count+=n
    assert count==14

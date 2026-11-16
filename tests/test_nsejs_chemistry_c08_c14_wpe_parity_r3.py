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

def test_revised_y_warrants_are_taught_and_x_z_w_are_exact():
    delta=get(AUD/"CHEMISTRY_C08_C14_REMEDIATION_DELTA_R3.json")
    for item in delta["changes"]:
        unit=item["unit_id"]
        pack=get(B/"core1b"/f"{unit}.core1b.v0.1.0.json")
        book=get(B/"learner"/f"{unit}.reader.v0.1.0.json")
        adapter=get(A/f"{unit}.v1.json")
        task=next(x for x in pack["cycles"] if x["cycle_id"]==item["cycle_id"])
        q=next(x for s in adapter["subtopics"] for x in s["qrt_instances"] if x["instance_id"]==task["qrt_instance_ref"])
        section=next(x for x in book["sections"] if x["id"]==item["subtopic_id"])
        assert q["slots"]["Y"] in section["teaching"]
        assert q["slots"]["X"]==task["attempt"]["prompt"]
        assert q["slots"]["Z"]==task["attempt"]["post_commit_closure"]["model_response"]
        assert q["slots"]["W"]==task["attempt"]["protected_W"]
        assert q["status"]=="ACADEMIC_HOLD"
        assert task["source_exam_question_id"] is None

def test_selected_scientific_numeric_checkpoints_are_independent():
    # Checks task arithmetic, not scientific/QRT acceptance.
    assert 2*0.010==0.020  # Zn -> Ag ideal electron stoichiometry
    assert round(0.010-0.006,3)==0.004  # Ca2+ after carbonate precipitation
    assert round(2.50*90/(159.6+5*18),3)==0.901  # copper sulfate hydrate water
    oxygen_consumed=2*8  # 8 mL CH4, 24 mL O2, 4 mL inert N2
    oxygen_left=24-oxygen_consumed
    dry_total=8+oxygen_left+4
    post_absorber=oxygen_left+4
    assert (dry_total,post_absorber,oxygen_left)==(20,12,8)

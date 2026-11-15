"""PH01/02/07/08 R2 author-candidate science, custody and source-asset regression.

Pure structural/scientific fixtures do NOT establish independent B1–B7 or R3.
"""
import hashlib
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"nsejs/physics/quality-r1"
FOCUS={"PH01-M05","PH02-F04","PH07-02","PH08-08"}


def load(name):
    return json.loads((PATH/name).read_text(encoding="utf-8"))


def gitsha(name):
    raw=(PATH/name).read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()


def test_v2_fresh_source_content_is_correctly_scoped():
    j=load("cases.v2.json")
    assert j["schema"]=="g9v41-four-physics-deep-reconstruction/v2"
    assert j["status"]=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"
    assert {x["unit"] for x in j["units"]}==FOCUS
    assert len({x["challenge"]["uid"] for x in j["units"]})==4
    for x in j["units"]:
        assert x["source"]["original_exam_admission"]=="HOLD"
        assert x["source"]["role"]=="AUTHORED_TRANSFER"
        assert x["adapter"]["author_qrt_hypothesis"]["independent_score"] is None
        assert x["adapter"]["selected_as_canonical"] is False
        assert len(x["study"]["examples"])==3
        assert x["study"]["model_limits"] if "model_limits" in x["study"] else x["study"]["assumptions"]
        assert x["challenge"]["prompt"] not in [e["prompt"] for e in x["study"]["examples"]]


def test_v2_exact_public_asset_pins_and_no_review_status_fetch():
    pins=load("asset-pins.v2.json")
    assert pins["status"]=="AUTHOR_ONLY__NOT_INDEPENDENTLY_SIGNED__ACADEMIC_HOLD"
    assert pins["source_v2_git_blob"]==gitsha("cases.v2.json")
    assert len(pins["items"])==7
    for entry in pins["items"]:
        assert entry["git_blob_sha"]==gitsha(entry["path"])
        if entry["path"]!="cases.v2.json" and entry["path"]!="public-source-status.v2.json":
            assert load(entry["path"])["source_v2_git_blob"]==pins["source_v2_git_blob"]
    pinned=(PATH/"pinned-assets.js").read_text(encoding="utf-8")
    assert gitsha("asset-pins.v2.json") in pinned
    assert "await gitBlobSha(raw)!==expected" in pinned
    assert "Candidate pin manifest does not match audited bytes" in pinned
    ledger=load("public-source-status.v2.json")
    assert ledger["schema"]=="g9v41-physics-source-status-public/v2"
    assert ledger["count"]==41 and len(ledger["rows"])==41
    assert all(x["source_exam_admission"]=="HOLD" for x in ledger["rows"])
    js=(PATH/"runtime.js").read_text(encoding="utf-8")
    assert 'pinnedJson("public-source-status.v2.json"' in js
    assert "review/physics/" not in js
    assert "case_v1" not in js


def test_precommit_payload_has_no_author_rubric_boundary_or_answer():
    a=load("cases.v2.json")
    p=load("prediction-prompts.v2.json")
    t=load("attempt-prompts.v2.json")
    g=load("postattempt-guidance.v2.json")
    b=load("boundary-models.v2.json")
    assert {x["unit"] for x in p["units"]}==FOCUS
    assert {x["unit"] for x in t["units"]}==FOCUS
    assert {x["unit"] for x in g["units"]}==FOCUS
    assert {x["unit"] for x in b["units"]}==FOCUS
    assert all(set(x)=={"unit","chapter","revision","uid","prediction"} for x in p["units"])
    assert all(set(x)=={"unit","chapter","revision","uid","prompt","fields"} for x in t["units"])
    pre=(PATH/"prediction-prompts.v2.json").read_text(encoding="utf-8")+(PATH/"attempt-prompts.v2.json").read_text(encoding="utf-8")
    for x in a["units"]:
        assert x["challenge"]["reconstruct"] not in pre
        assert x["challenge"]["boundaryPrompt"] not in pre
        assert x["challenge"]["boundaryModel"] not in pre
        assert x["challenge"]["transfer_difference"] not in pre
        assert x["adapter"]["reason"] not in pre
        for hint in x["challenge"]["hints"]:assert hint not in pre
        assert "author_qrt_hypothesis" not in pre
    assert "−0.10 K/s" not in pre and "12 N" not in pre
    for x in g["units"]:
        assert len(x["rubric"])>=4
        assert len(x["boundaryFields"])==2
        assert "boundaryModel" not in x
    for x in b["units"]:
        assert len(x["boundaryRubric"])==2


def test_newton_compliant_transient_vs_maintained_rigid_equations():
    x=next(x for x in load("cases.v2.json")["units"] if x["unit"]=="PH02-F04")
    assert "compressed spring bumper" in x["challenge"]["prompt"]
    assert "rigid" in x["study"]["model"].lower()
    assert "compliant" in x["study"]["model"].lower()
    motor,brake,ma,mb,aa,ab=18,4,3,2,2,4
    c_from_a=motor-ma*aa
    c_from_b=mb*ab+brake
    assert c_from_a==c_from_b==12
    assert ab-aa==2
    a_rigid=(motor-brake)/(ma+mb)
    c_rigid=motor-ma*a_rigid
    assert math.isclose(a_rigid,2.8) and math.isclose(c_rigid,9.6)
    assert aa!=ab and aa!=a_rigid


def test_heat_phase_inverse_and_boundary_witness():
    assert (90-30)*120==7200
    assert math.isclose(7200/(180*1000),0.04)
    assert 7200/600==12
    assert (90-90)*120==0
    # Worked P and Q are different figures from fresh A/B task
    assert 24/160==0.15 and 40/400==0.10
    assert (75-15)*100/(200000)==0.03


def test_echo_inverse_sum_difference_and_mirror_ambiguity():
    v=325;b=12;t_direct_ms=40;t_ref_ms=46.154
    direct=v*t_direct_ms/1000
    reflected=v*t_ref_ms/1000
    difference=math.sqrt(direct**2-b**2)
    summation=math.sqrt(reflected**2-b**2)
    source=(summation+difference)/2
    receiver=(summation-difference)/2
    assert abs(source-7)<0.01 and abs(receiver-2)<0.01
    assert math.isclose(math.sqrt(12**2+(7-2)**2),13)
    assert math.isclose(math.sqrt(12**2+(7+2)**2),15)
    assert t_ref_ms-t_direct_ms<7


def test_motion_inverse_anchor_and_corner():
    x5=14-10
    x0=x5-(3*3-2*2)
    x7=x5+2*1
    assert x0==-1 and x7==6
    assert 9-4+2==7 and 9+4+2==15
    assert (-3,+2,-1)==(-3,2,-1)
    assert 3!=-2
    assert x5-2*2==0 and 9+4+4==17


def test_r2_code_uses_locks_and_early_first_divergence():
    core=(PATH/"protected-attempt-store.js").read_text(encoding="utf-8")
    runtime=(PATH/"assessment-r2.js").read_text(encoding="utf-8")
    assert "navigator.locks.request(key" in core
    assert "const old=read()" in core
    assert 'kind==="prediction"' in core and 'kind==="first"' in core
    assert "First commitment mutation rejected" in core
    assert "Prediction mutation rejected" in core
    assert "Non-monotonic transition rejected" in core
    assert "window.addEventListener(\"storage\"" in core
    assert "UNKNOWN_NO_LOCAL_GUIDE_EVIDENCE" in core
    assert "const wrong=checked.find" in runtime
    assert "All checked model/value fields match" in runtime
    assert '"postattempt-guidance.v2.json"' in runtime
    assert '"boundary-models.v2.json"' in runtime
    assert "function evaluate" in runtime
    assert "Commit prediction" in runtime and "Commit immutable first attempt" in runtime
    assert "boundaryModels" not in (PATH/"attempt-prompts.v2.json").read_text(encoding="utf-8")


def test_four_new_candidate_topic_adapters_map_exact_r2_task_without_academic_promotion():
    paths={
      "PH01-M05":"nsejs/physics/curriculum/agent1/PH01/topic-adapter.PH01.quality-r2.json",
      "PH02-F04":"nsejs/physics/curriculum/agent1/PH02/topic-adapter.PH02.quality-r2.json",
      "PH07-02":"nsejs/physics/curriculum/topics/PH07/topic-adapter.PH07.quality-r2.json",
      "PH08-08":"nsejs/physics/curriculum/topics/PH08/topic-adapter.PH08.quality-r2.json",
    }
    expected_counts={"PH01-M05":54,"PH02-F04":25,"PH07-02":44,"PH08-08":47}
    units={x["unit"]:x for x in load("cases.v2.json")["units"]}
    for unit,path in paths.items():
        a=json.loads((ROOT/path).read_text(encoding="utf-8"))
        c=units[unit]
        entries=[x for group in a["cells"] for x in group["instance_ids"]]
        assert len(entries)==expected_counts[unit] and len(set(entries))==len(entries)
        assert a["status"]=="CANDIDATE_ONLY"
        assert a["canonical_selection"]=="NOT_SELECTED"
        assert a["independent_qrt"]=="NOT_RUN"
        assert a["quality_r2_extension"]["task_id"]==c["challenge"]["uid"]
        assert a["quality_r2_extension"]["source_case_git_blob"]==gitsha("cases.v2.json")
        assert a["quality_r2_extension"]["accepted_d3"] is False
        assert a["quality_r2_extension"]["accepted_d4"] is False
        assert a["quality_r2_extension"]["independent_qrt_scores"] is None
        assert c["challenge"]["uid"] in entries
        assert any(group["cell_id"]==c["adapter"]["cell"] and
                   c["challenge"]["uid"] in group["instance_ids"] for group in a["cells"])

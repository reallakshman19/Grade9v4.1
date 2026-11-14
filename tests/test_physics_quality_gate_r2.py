"""Synthetic adversarial cases for evidence gate. No academic approval claimed."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"docs/agent-entry/quality-gate-r2/verify_evidence_packet.py"
spec=importlib.util.spec_from_file_location("physics_evidence_gate_r2",SCRIPT)
assert spec and spec.loader
Q=importlib.util.module_from_spec(spec)
spec.loader.exec_module(Q)
T="This is a distinct, complete synthetic claim witnessing a specific reasoning step."
C="This independent paragraph demonstrates the mechanism rather than reporting a numeric answer."
WHY="This is a mechanically anchored exact excerpt, requiring a human to assess its scientific truth."


def case(tmp_path, golden=False):
    role_ref={}
    candidates=[]
    for (group,field),role in Q.REF_ROLES.items():
        tag=f"EV-{group}-{field}"
        role_ref[(group,field)]=tag
        candidates.append((tag,role))
    negative_refs={}
    for kind in sorted(Q.GOLDEN_NEGATIVE):
        tag="LOG-"+kind
        negative_refs[kind]=tag
        candidates.append((tag,"QA_NEGATIVE_LOG"))

    all_lines={}
    for index,(tag,role) in enumerate(candidates):
        if role.startswith("SCIENCE_"): path="evidence/science.txt"
        elif role.startswith("CORE1A_"): path="evidence/lesson.html"
        elif role.startswith("CORE1B_"): path="evidence/transfer.html"
        elif role.startswith("CORE2_"): path="evidence/core2.txt"
        elif role=="QA_NEGATIVE_LOG":path="evidence/negative.txt"
        else:path="evidence/chromium.txt"
        if role=="QA_NEGATIVE_LOG":
            kind=tag.removeprefix("LOG-")
            snippet=f"{kind} REJECTED {WHY} {tag}"
        elif tag.endswith("portrait_receipt_ref"):
            snippet=f"1000x1600 HTTP Chromium PASS {WHY} {tag}"
        elif tag.endswith("landscape_receipt_ref"):
            snippet=f"1600x1000 HTTP Chromium PASS {WHY} {tag}"
        else:
            snippet=f"{tag} {T} {C} {WHY}"
        all_lines.setdefault(path,[]).append((tag,snippet,role))
    for path,lines in all_lines.items():
        p=tmp_path/path
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text("\n".join(x[1] for x in lines)+"\n",encoding="utf-8")

    evidence=[]
    for path,lines in all_lines.items():
        digest=hashlib.sha256((tmp_path/path).read_bytes()).hexdigest()
        for n,(tag,snippet,role) in enumerate(lines,1):
            evidence.append({"id":tag,"role":role,"path":path,"sha256":digest,
              "start_line":n,"end_line":n,"excerpt":snippet,
              "claim":f"{tag} test evidence is present at exact declared bytes and line range.",
              "why_this_proves_claim":WHY+" A subject reviewer still must check scientific merit."})
    refs=lambda group,field:role_ref[(group,field)]
    p={
      "schema_version":"g9v41-physics-evidence-packet/v2",
      "task":{"task_id":"G9-A01-PH01-EXAMPLE","owner_workpack":"A01","topic_id":"PH01",
        "subtopic_id":"PH01-M03","base_sha":"1"*40,"head_sha":"2"*40,
        "contract_version":"1.1.0","blueprint_version":"0.2.0",
        "golden_sample_sha":"2"*40,"delivery_kind":"GOLDEN_SAMPLE" if golden else "BATCH_ITEM"},
      "declarations":{"source_status":"AUTHOR_CREATED_NO_EXAM_SOURCE",
        "science_status":"AUTHOR_UNVERIFIED","qrt_status":"AUTHOR_PROPOSED","academic_status":"HOLD",
        "owner_release_status":"NOT_REQUESTED","reviewer_independent":False},
      "evidence":evidence,
      "science":{"primary_derivation_ref":refs("science","primary_derivation_ref"),
        "independent_check_ref":refs("science","independent_check_ref"),
        "units_signs_ref":refs("science","units_signs_ref"),
        "assumptions_limit_ref":refs("science","assumptions_limit_ref"),
        "counterexample_ref":refs("science","counterexample_ref"),"model_version":"synthetic-only"},
      "core1a":{"student_ready_path":"evidence/lesson.html",
        **{k:refs("core1a",k) for k in [
          "phenomenon_ref","prerequisite_ref","causal_explanation_ref",
          "diagram_ref","foundation_ref","connected_ref","advanced_ref",
          "misconception_ref","synthesis_ref"]},
        "self_teaching_test":{
          "learner_can_explain":"A student must explain the positive direction before selecting velocity models; no mere recall.",
          "novice_dependency_check":"A cold reader without learned sign conventions must be able to reconstruct the necessary prerequisite coordinate choices before graph work.",
          "unassisted_question":"How would a different origin change an interval's signed displacement, and why?",
          "expected_reasoning":"Subtract endpoint positions and preserve a fixed sign convention; changing origin shifts positions but not their differences or velocities.",
          "counterfactual_reasoning":"If the positive axis is reversed, both position differences and signed velocities change sign, while distance and speed do not."}},
      "core1b":{"student_ready_path":"evidence/transfer.html",
        "anchor_problem":"A trolley moving east reverses after five seconds. Find average speed from a simple table, including rest.",
        "new_problem":"Two moving observers reconstruct an unknown reversal interval from a graph, then test feasibility against a second observer.",
        "anchor_crux":"Choose average speed by summing nonnegative travel distances over the complete duration, including stationary intervals.",
        "new_crux":"Choose signed graph areas and solve an inverse observer constraint with time-domain validation.",
        "novelty_mechanism":"INVERSE_CONSTRAINT",
        "numeric_swap_rejected":"Reversing the velocity frame changes the unknown, representation and feasibility check; merely replacing the numbers cannot solve the task.",
        **{k:refs("core1b",k) for k in [
          "fresh_task_ref","model_route_ref","boundary_ref",
          "hint_nonleak_ref","first_save_ref","revision_return_ref"]},
        "stages":{name:"The student must construct and justify a relevant physical model without receiving the protected answer. "+name for name in
          ["predict","attempt","reconstruct","diagnose","repair","boundary_test"]},
        "hints":{"H1":"Identify the measured quantities and positive direction without naming the answer.",
          "H2":"Consider which graph slope or signed area is relevant, but do not solve it for the learner.",
          "H3":"Compare time domains and model assumptions, not the final numeric solution.",
          "blocked_until_first_save":True},
        "multiple_subtopic_main":{"contract_applies":True,
          "instance_ids":["PH01-M03-D3","PH01-M05-D3"],
          "subtopic_ids":["PH01-M03","PH01-M05"],
          "integrated_reasoning":"The integrated MAIN combines two distinct types of motion information to reconstruct an observer constraint and reject an out-of-interval solution."}},
      "core2":{"identity":"AUTHORED-PH01-TASK",
        "source_role":"AUTHORED_TRANSFER",
        "stem_figure_ref":refs("core2","stem_figure_ref"),
        "derivation_key_ref":refs("core2","derivation_key_ref"),
        "figure_need":"NOT_REQUIRED","figure_status":"NO_FIGURE_NEEDED",
        "original_source_fidelity":"NOT_SELF_APPROVED","exam_question_count_claim":0},
      "negative_tests":[{"case":k,"mutation":f"Inject {k} into a deliberately broken, synthetic fixture.",
        "expected_failure":f"{k} should be blocked as a deliberate invalid witness.",
        "observed_failure":f"{k} REJECTED","reproduction_command":f"pytest -k negative_{k.lower()}",
        "log_ref":negative_refs[k]} for k in sorted(Q.GOLDEN_NEGATIVE if golden else Q.BATCH_NEGATIVE)],
      "browser":{"head_sha":"2"*40,
        "portrait_receipt_ref":refs("browser","portrait_receipt_ref"),
        "landscape_receipt_ref":refs("browser","landscape_receipt_ref"),
        **{k:"PASS" for k in ["keyboard_and_touch","storage_failure","stale_revision","pre_first_help","figure_render"]},
        "outcome":"MECHANICAL_ONLY_NOT_ACADEMIC_APPROVAL"},
      "self_audit":{"red_team_hypotheses":[
        "The target might be answerable by copying a previously worked example with only new numbers.",
        "A missing or mislabeled diagram could remove the information needed to select a valid model.",
        "The learner might see protected hints before any saved first attempt, invalidating mastery evidence."],
        "known_defects":[],"rejected_alternatives":[
          "A short formula-only Core1A section cannot establish the reason the model works.",
          "A changed number alone cannot establish transfer or a separate QRT operation."],
        "evidence_completeness":"AUTHOR_ASSERTED_COMPLETE",
        "self_disposition":"CANDIDATE_REVIEW_REQUESTED","review_requested":True}
    }
    return p


def assert_blocked(packet, root, code):
    result=Q.validate(packet,root)
    assert result["mechanical_status"]=="BLOCKED"
    assert any(code in problem for problem in result["findings"]),result


def test_synthetic_full_golden_packet_is_structurally_grounded(tmp_path):
    p=case(tmp_path,golden=True)
    r=Q.validate(p,tmp_path)
    assert r["findings"]==[],r
    assert r["mechanical_status"]=="EVIDENCE_STRUCTURALLY_GROUNDED"
    assert r["academic_status"]=="HOLD"
    assert r["review_required"] is True
    assert r["owner_per_question_approval_required"] is False


def test_batch_item_remains_academic_hold_even_if_structurally_grounded(tmp_path):
    r=Q.validate(case(tmp_path),tmp_path)
    assert r["mechanical_status"]=="EVIDENCE_STRUCTURALLY_GROUNDED",r
    assert r["academic_status"]=="HOLD"


def test_reject_changed_source_bytes_even_if_excerpt_still_matches(tmp_path):
    p=case(tmp_path)
    path=tmp_path/p["evidence"][0]["path"]
    path.write_text(path.read_text()+"tamper\n",encoding="utf-8")
    assert_blocked(p,tmp_path,"BYTE_HASH_MISMATCH")


def test_reject_fake_quote_and_wrong_line(tmp_path):
    p=case(tmp_path)
    p["evidence"][0]["start_line"]=p["evidence"][0]["end_line"]=999
    assert_blocked(p,tmp_path,"BAD_LINE_RANGE")
    p=case(tmp_path)
    p["evidence"][0]["excerpt"]="An invented source quotation not present in the declared range."
    assert_blocked(p,tmp_path,"EXCERPT_NOT_AT_GIVEN_LINES")


def test_reject_numeric_swap_even_when_author_says_it_is_fresh(tmp_path):
    p=case(tmp_path)
    p["core1b"]["anchor_problem"]="Find speed of object after 4 m in 2 s."
    p["core1b"]["new_problem"]="Find speed of object after 9 m in 6 s."
    assert_blocked(p,tmp_path,"NUMERIC_REPARAMETERIZATION_DETECTED")


def test_reject_bad_evidence_role_and_deleted_negative(tmp_path):
    p=case(tmp_path)
    p["science"]["primary_derivation_ref"]=p["science"]["independent_check_ref"]
    assert_blocked(p,tmp_path,"EVIDENCE_ROLE_MISMATCH")
    p=case(tmp_path)
    p["negative_tests"]=[x for x in p["negative_tests"] if x["case"]!="HINT_LEAK"]
    assert_blocked(p,tmp_path,"MISSING_ADVERSARIAL_TEST")


def test_reject_unresolved_figure_and_fake_academic_promotion(tmp_path):
    p=case(tmp_path)
    p["core2"]["figure_need"]="REQUIRED"
    p["core2"]["figure_status"]="MISSING_HOLD"
    assert_blocked(p,tmp_path,"REQUIRED_FIGURE_MISSING")
    p=case(tmp_path)
    p["declarations"]["academic_status"]="APPROVED"
    assert_blocked(p,tmp_path,"SCHEMA:declarations/academic_status:")


def test_reject_badge_promotion_even_when_source_hash_evidence_is_updated(tmp_path):
    p=case(tmp_path)
    path=tmp_path/p["core1a"]["student_ready_path"]
    path.write_text(path.read_text()+"\n{Reviewed} · Peer-Audited Module\n",encoding="utf-8")
    assert_blocked(p,tmp_path,"UNSUPPORTED_REVIEW_BADGE")


def test_reject_wrong_browser_receipt_and_mismatched_sha(tmp_path):
    p=case(tmp_path)
    p["browser"]["head_sha"]="f"*40
    assert_blocked(p,tmp_path,"BROWSER_HEAD_NOT_BOUND_TO_SOURCE_HEAD")
    p=case(tmp_path)
    e=next(x for x in p["evidence"] if x["id"]==p["browser"]["landscape_receipt_ref"])
    e["excerpt"]=e["excerpt"].replace("1600x1000","390x844")
    assert_blocked(p,tmp_path,"WRONG_BROWSER_VIEWPORT")


def test_reject_missing_multisubtopic_main_on_c06_v11(tmp_path):
    p=case(tmp_path)
    p["core1b"]["multiple_subtopic_main"]["subtopic_ids"]=["PH01-M03"]
    assert_blocked(p,tmp_path,"MAIN_NOT_MULTI_INSTANCE_MULTI_SUBTOPIC")


def test_reject_open_author_defects_or_holds(tmp_path):
    p=case(tmp_path)
    p["self_audit"]["known_defects"]=["The science figure is currently wrong."]
    assert_blocked(p,tmp_path,"OPEN_DEFECTS_NOT_CLOSED")

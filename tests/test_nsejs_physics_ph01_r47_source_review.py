"""R00 PH01 R4.7 reconciliation handoff invariants.

Static confidentiality/identity checks here, not independent R01 acceptance.
The two-tree byte comparison runs separately in the pinned-source workflow.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics/curriculum/agent1/PH01"

def data(name):
    return json.loads((PH/name).read_text(encoding="utf-8"))

def test_r47_reconciliation_pinned_source_held():
    report=data("PH01_R47_SOURCE_REVISION_R00.v1.json")
    assert report["canonical"]["byte_exact_blob_equal"]
    assert report["canonical"]["physics_rows"]==95
    assert report["corpus"]["size"]==50
    assert report["corpus"]["actual_stems_options_answers_steps_unchanged"]
    assert (report["provenance"]["ledger_before"],report["provenance"]["ledger_main"])==(11,36)
    assert report["provenance"]["new_locator_records"]==25
    assert report["integrity"]["declared_matches_observed_main"]==50
    assert report["integrity"]["academic_admission"]=="HOLD"
    assert report["release"]["approved_to_merge"] is False
    assert report["release"]["academic_B1_B7"]=="HOLD"
    assert all(t["admission"]=="HOLD" for t in report["targets"])
    assert all(t["independent_QRT"]=="NOT_RUN" for t in report["targets"])
    uids={t["uid"] for t in report["targets"]}
    assert uids=={"g9:pcb:physics:nsejs-2022-physics-r1:003",
                  "g9:pcb:physics:nsejs-2024-physics-r1:001",
                  "g9:pcb:physics:nsejs-2024-physics-r1:020"}

def test_r47_blind_intake_has_no_solution_or_author_qrt_label():
    blind=data("PH01_R47_R01_BLIND_INTAKE.v1.json")
    assert blind["candidate_count"]==3
    assert len(blind["blind_cases"])==3
    assert blind["mode"]=="R01_BLIND_QRT_FIRST__NO_AUTHOR_RATINGS_OR_SOLUTIONS"
    assert [len(x["input_graphs"]) for x in blind["blind_cases"]]==[1,0,3]
    for case in blind["blind_cases"]:
        assert case["prompt"] and len(case["prompt"])>200
        assert case["source_locator_only"]["source_admission"]=="HOLD"
        assert case["question_type"]=="ORIGINAL_AUTHORED_TRANSFER_NOT_EXACT_EXAM_STEM"
        for forbidden in ("solution","answer","protected_work","qrt_target_id","primary_operation",
                          "band","difficulty_score","decisive_route","source_w","hints","model_response"):
            assert forbidden not in case, forbidden
        assert "D3" not in case["blind_id"] and "D4" not in case["blind_id"]

def test_r47_historical_learning_package_is_unchanged_historical_hold():
    pkg=data("physics-topic-package.v1_1.r4_7.json")
    assert pkg["version"]=="0.11.0"
    assert len(pkg["core1b"])==63
    assert pkg["acceptance"]["release"]=="HOLD"
    assert pkg["core2_sources"]==[]
    assert all(c["runtime_verification"]=="NOT_RUN" for c in pkg["core1b"])

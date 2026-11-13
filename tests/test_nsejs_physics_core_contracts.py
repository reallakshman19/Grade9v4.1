"""C01-C08 contract tests: synthetic mechanics only, never academic approval."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "nsejs/physics/curriculum/contracts"
SCRIPT = CONTRACTS / "tools/validate_physics_contracts.py"
FIXTURE = CONTRACTS / "fixtures/physics-topic.synthetic.valid.json"

spec = importlib.util.spec_from_file_location("physics_core_contract_validation", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def payload():
    return mod.read_json(FIXTURE)


def validate(p):
    return mod.validate_topic(p, mod.read_json(mod.CONTRACT_FILE),
                              mod.read_json(mod.SCHEMA_FILE))


def test_manifest_has_eight_contracts_and_exact_two_agent_partition():
    c = mod.read_json(mod.CONTRACT_FILE)
    assert mod.validate_manifest(c) == []
    assert len(c["contracts"]) == 8
    assert c["topic_ownership"]["AGENT_1"] == [f"PH{i:02d}" for i in range(1, 7)]
    assert c["topic_ownership"]["AGENT_2"] == [f"PH{i:02d}" for i in range(7, 13)]
    assert c["dependencies"]["physics_blueprint"]["status"] == "DRAFT_OWNER_REVIEW"
    assert c["dependencies"]["d1_d2_blueprint"]["status"] == "SPEC_PENDING"


def test_valid_synthetic_pack_is_mechanical_pass_but_academic_hold():
    receipt = mod.inspect_package(FIXTURE)
    assert receipt["issues"] == []
    assert receipt["mechanical_status"] == "PASS"
    assert receipt["academic_status"] == "HOLD"
    assert receipt["release_status"] == "HOLD"


def test_wrong_topic_owner_fails_closed():
    p = payload()
    p["owner_agent"] = "AGENT_2"
    assert "WRONG_OWNER:PH01:AGENT_2" in validate(p)


def test_cross_subject_pack_is_schema_invalid():
    p = payload()
    p["subject_id"] = "CHEMISTRY"
    assert any(x.startswith("SCHEMA:subject_id:") for x in validate(p))


def test_only_two_distinct_qrt_operations_rejected():
    p = payload()
    p["subtopics"][0]["qrt_targets"][2]["primary_operation"] = "MODEL"
    issues = validate(p)
    assert any(x.startswith("INSUFFICIENT_DISTINCT_QRT_OPERATIONS") for x in issues)


def test_wrong_blueprint_cell_fails():
    p = payload()
    p["subtopics"][0]["qrt_targets"][1]["blueprint_cell"] = "D3.2"
    assert any(x.startswith("WRONG_QRT_CELL:PH01-KIN-SYN-2") for x in validate(p))


def test_insufficient_five_factor_band_score_fails():
    p = payload()
    p["subtopics"][0]["qrt_targets"][1]["factor_evidence"]["reasoning_chain_length"]["score"] = 0
    assert any(x.startswith("BAND_FACTOR_TOTAL_MISMATCH:PH01-KIN-SYN-2") for x in validate(p))


def test_wrong_blueprint_pin_fails():
    p = payload()
    p["pins"]["blueprint"]["git_blob_sha"] = "f" * 40
    assert "DEPENDENCY_PIN_MISMATCH:blueprint" in validate(p)


def test_unverified_direct_exam_link_fails():
    p = payload()
    p["subtopics"][0]["qrt_targets"][0]["source_role"] = "DIRECT_EXAM_EVIDENCE"
    assert any(x.startswith("EXAM_SOURCE_RECORD_MISSING:PH01-KIN-SYN-1") for x in validate(p))


def test_duplicate_subtopic_and_missing_main_cycle_fail():
    p = payload()
    p["subtopics"].append(copy.deepcopy(p["subtopics"][0]))
    p["core1b"] = [x for x in p["core1b"]
                    if not (x["kind"] == "MAIN" and x["qrt_target_id"] == "PH01-KIN-SYN-1")]
    issues = validate(p)
    assert any(x.startswith("DUPLICATE_SUBTOPIC_ID") for x in issues)
    assert any(x.startswith("CORE1B_MAIN_MISSING:D3.2") for x in issues)


def test_first_attempt_storage_policy_cannot_be_disabled():
    p = payload()
    p["core1b"][0]["attempt_policy"]["save_first_answer_before_hint"] = False
    assert any(x.startswith("SCHEMA:core1b/0/attempt_policy/") for x in validate(p))


def test_legacy_or_unknown_qrt_operation_fails():
    p = payload()
    p["subtopics"][0]["qrt_targets"][0]["primary_operation"] = "CALCULATE"
    assert any(x.startswith("SCHEMA:subtopics/0/qrt_targets/0/primary_operation") for x in validate(p))


def test_no_author_can_promote_release():
    p = payload()
    p["acceptance"]["release"] = "APPROVED"
    assert any(x.startswith("SCHEMA:acceptance/release:") for x in validate(p))
    p = payload()
    p["acceptance"]["gates"]["release_authority"] = "PASS"
    assert any(x.startswith("SCHEMA:acceptance/gates/release_authority:") for x in validate(p))


def test_missing_science_reference_fails():
    p = payload()
    p["subtopics"][0]["science_ref_ids"] = ["MISSING-SCIENCE"]
    assert any(x.startswith("UNKNOWN_SCIENCE_REF:") for x in validate(p))


def test_identical_worked_anchor_and_fresh_task_fails():
    p = payload()
    p["core1b"][0]["fresh_task"] = p["core1a"][0]["progressive_examples"][0]["problem"]
    assert any(x.startswith("CORE1B_REUSES_WORKED_ANCHOR") for x in validate(p))


def test_local_blueprint_blob_change_is_detected():
    c = mod.read_json(mod.CONTRACT_FILE)
    c["dependencies"]["physics_blueprint"]["git_blob_sha"] = "0" * 40
    assert any(x.startswith("PIN_BLOB_MISMATCH:physics_blueprint:") for x in mod.validate_manifest(c))

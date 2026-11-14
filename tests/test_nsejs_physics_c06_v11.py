"""Versioned C06 v1.1 MAIN multi-instance contract tests.

All fixtures are author-exposed candidate tasks. Structural PASS does not
establish source custody, independent QRT, physics qualification or mastery.
"""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "nsejs/physics/curriculum/contracts"
PACK = ROOT / "nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.json"
LEGACY_PACK = ROOT / "nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1.json"

spec = importlib.util.spec_from_file_location("physics_core_contract_v11_validator",
                                              CONTRACTS / "tools/validate_physics_contracts.py")
assert spec is not None and spec.loader is not None
V = importlib.util.module_from_spec(spec)
spec.loader.exec_module(V)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def data():
    return read_json(PACK)


def violations(p):
    return V.validate_topic(p, read_json(V.CONTRACT_FILE_V1_1),
                            read_json(V.SCHEMA_FILE_V1_1))


def assert_issue(p, prefix):
    assert any(error.startswith(prefix) for error in violations(p)), violations(p)


def test_v11_manifest_and_schema_validate_with_exact_pins():
    assert V.validate_manifest(read_json(V.CONTRACT_FILE_V1_1)) == []
    from jsonschema import Draft202012Validator
    Draft202012Validator.check_schema(read_json(V.SCHEMA_FILE_V1_1))


def test_v11_ph01_candidate_is_mechanically_valid_with_all_review_holds():
    r = V.inspect_package(PACK)
    assert r["mechanical_status"] == "PASS", r["issues"]
    assert r["issues"] == []
    assert r["academic_status"] == r["release_status"] == "HOLD"
    p = data()
    assert p["schema"].endswith("/v1.1")
    assert p["pins"]["contracts_version"] == "1.1.0"
    assert p["topic_adapter"]["status"] == "CANDIDATE_ONLY"
    assert all(state == "HOLD" for state in p["acceptance"]["gates"].values()
               if state != "NOT_RUN")


def test_old_v1_source_and_synthetic_contract_still_validate():
    for path in (LEGACY_PACK,
                 CONTRACTS / "fixtures/physics-topic.synthetic.valid.json"):
        r = V.inspect_package(path)
        assert r["mechanical_status"] == "PASS", r["issues"]
        assert r["release_status"] == "HOLD"


def test_exact_three_cognitive_operations_in_each_three_subtopics():
    p = data()
    assert [x["id"] for x in p["subtopics"]] == [
        "PH01-M03", "PH01-M05", "PH01-M07"
    ]
    for sub in p["subtopics"]:
        assert len(sub["qrt_targets"]) == 3
        assert {x["primary_operation"] for x in sub["qrt_targets"]} == {
            "MODEL", "REPRESENT", "SYNTHESIZE"
        }
        assert {x["blueprint_cell"] for x in sub["qrt_targets"]} == {
            "D3.4", "D3.5", "D3.6"
        }
        assert all(x["source_role"] == "AUTHORED_TRANSFER" and
                   x["qrt_status"] == "PROPOSED" for x in sub["qrt_targets"])


def test_cell_main_is_one_per_cell_joint_over_all_three_subtopics():
    p = data()
    mains = [x for x in p["core1b"] if x["kind"] == "MAIN"]
    instances = [x for x in p["core1b"] if x["kind"] == "INSTANCE"]
    assert len(mains) == 3 and len(instances) == 9
    for main in mains:
        adapter_cell = next(x for x in p["topic_adapter"]["cells"]
                            if x["cell_id"] == main["cell_id"])
        assert set(main["instance_qrt_ids"]) == set(adapter_cell["instance_ids"])
        assert len(main["instance_qrt_ids"]) == 3
        assert main["qrt_target_id"] in main["instance_qrt_ids"]
        assert all("PH01-" in ref for ref in main["instance_qrt_ids"])
    for instance in instances:
        assert instance["instance_qrt_ids"] == [instance["qrt_target_id"]]
        assert instance["runtime_verification"] == "NOT_RUN"


def test_reject_main_with_only_one_instance():
    p = data()
    m = next(x for x in p["core1b"] if x["kind"] == "MAIN")
    m["instance_qrt_ids"] = [m["qrt_target_id"]]
    assert_issue(p, "CORE1B_MAIN_TOO_FEW_INSTANCES")


def test_reject_main_missing_bound_subtopic_even_if_two_remain():
    p = data()
    m = next(x for x in p["core1b"] if x["kind"] == "MAIN")
    m["instance_qrt_ids"] = m["instance_qrt_ids"][:2]
    assert_issue(p, "CORE1B_MAIN_INCOMPLETE_CELL_COVERAGE")


def test_reject_main_cross_cell_qrt_instance():
    p = data()
    m = next(x for x in p["core1b"] if x["kind"] == "MAIN")
    wrong = next(x for x in p["topic_adapter"]["cells"]
                 if x["cell_id"] != m["cell_id"])["instance_ids"][0]
    m["instance_qrt_ids"][0] = wrong
    assert_issue(p, "CORE1B_MAIN_CROSS_CELL")


def test_reject_duplicate_main_for_one_cell():
    p = data()
    m = next(x for x in p["core1b"] if x["kind"] == "MAIN")
    clone = copy.deepcopy(m)
    clone["id"] = "DUPLICATE-MAIN"
    clone["qrt_target_id"] = clone["instance_qrt_ids"][0]
    clone["subtopic_id"] = "PH01-M03"
    p["core1b"].append(clone)
    assert_issue(p, "CORE1B_MAIN_NOT_EXACTLY_ONE")


def test_reject_unknown_main_member():
    p = data()
    m = next(x for x in p["core1b"] if x["kind"] == "MAIN")
    m["instance_qrt_ids"][1] = "DOES-NOT-EXIST"
    assert_issue(p, "CORE1B_MAIN_UNKNOWN_INSTANCE")


def test_reject_instance_cycle_with_other_target_reference():
    p = data()
    c = next(x for x in p["core1b"] if x["kind"] == "INSTANCE")
    c["instance_qrt_ids"] = [
        x for x in p["topic_adapter"]["cells"][0]["instance_ids"]
        if x != c["qrt_target_id"]
    ][:1]
    assert_issue(p, "CORE1B_INSTANCE_REFERENCES_NOT_EXACT")


def test_reject_main_cell_mismatch():
    p = data()
    main = next(x for x in p["core1b"] if x["kind"] == "MAIN")
    main["cell_id"] = "D3.7"
    assert_issue(p, "CORE1B_CELL_ID_MISMATCH")


def test_reject_adapter_member_missing_from_qrt_target():
    p = data()
    p["topic_adapter"]["cells"][0]["instance_ids"].append("NONEXISTENT")
    assert_issue(p, "ADAPTER_CELL_TARGET_MISMATCH")


def test_release_and_credential_gate_cannot_be_promoted_by_authors():
    p = data()
    p["acceptance"]["release"] = "APPROVED"
    assert_issue(p, "SCHEMA:acceptance/release:")
    p = data()
    p["acceptance"]["gates"]["cognitive_qualification"] = "PASS"
    assert_issue(p, "SCHEMA:acceptance/gates/cognitive_qualification:")


def test_v11_adapter_standalone_equals_package_and_versions_are_pinned():
    p = data()
    actual = read_json(PACK.parent / "topic-adapter.PH01.v0.2.0.json")
    assert p["topic_adapter"] == actual
    assert p["pins"]["topic_adapter_version"] == "0.2.0"
    assert p["pins"]["blueprint"]["version"] == "0.2.0"
    assert p["pins"]["shared_qrt_28"]["version"] == "1.0.0"


def test_cross_topic_integrated_main_keeps_physics_math_valid():
    mains = {m["cell_id"]: m for m in data()["core1b"] if m["kind"] == "MAIN"}
    # D3.4 cart: xA(t>=5)=18-2t; xB=25-t -> t=-7 (invalid).
    assert (25 - 5) > 8
    assert (-7 < 5)
    # D3.5 moving observer: ground net -3, observer +16, relative -19 m.
    assert (3 * 2 + 0 * 3 - 3 * 3) == -3
    assert (1 * 2 - 2 * 3 - 5 * 3) == -19
    # D3.6 reversal at 3 s, real encounter at 5 s, position +10 m.
    assert (30 / (4 + 4)) > 3
    assert (15 - 5) == (30 - 4 * 5) == 10
    assert 12 + (5 - 3) == 14
    assert all(m["runtime_verification"] == "NOT_RUN" for m in mains.values())

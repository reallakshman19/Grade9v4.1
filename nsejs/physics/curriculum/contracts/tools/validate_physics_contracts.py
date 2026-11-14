#!/usr/bin/env python3
"""Fail-closed C01-C08 Physics topic-package validation (mechanical checks only).

The public GitHub candidate is not a scientific, QRT, source, B1-B7, or release
approval. Native Shared/QRT checkers and independent reviews remain authoritative.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent.parent
REPO_ROOT = HERE.parents[3]
CONTRACT_FILE = HERE / "core-contracts.v1.json"
SCHEMA_FILE = HERE / "physics-topic-package.v1.schema.json"

GATES = (
    "source_authenticity", "content_correctness", "cognitive_qualification",
    "teaching_sufficiency", "assessment_validity", "implementation",
    "release_authority",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _duplicates(items: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicate: set[str] = set()
    for item in items:
        if item in seen:
            duplicate.add(item)
        seen.add(item)
    return sorted(duplicate)


def verify_contract_source_pins(
    contract: dict[str, Any], repo_root: Path = REPO_ROOT
) -> list[str]:
    problems: list[str] = []
    deps = contract.get("dependencies", {})
    for key in ("physics_blueprint", "physics_resolved", "d3_subtiles"):
        pin = deps.get(key, {})
        rel = pin.get("path")
        digest = pin.get("git_blob_sha")
        if not isinstance(rel, str) or not isinstance(digest, str):
            problems.append(f"PIN_FIELDS_MISSING:{key}")
            continue
        file_path = repo_root / rel
        if not file_path.is_file():
            problems.append(f"PIN_FILE_MISSING:{key}:{rel}")
            continue
        if git_blob_sha(file_path) != digest:
            problems.append(f"PIN_BLOB_MISMATCH:{key}:{rel}")
    # The 28-template dependency is in a *different repository*.
    # Its declared SHA cannot be authenticated from this checkout alone.
    return problems


def validate_manifest(
    contract: dict[str, Any], repo_root: Path = REPO_ROOT
) -> list[str]:
    issues: list[str] = []
    if contract.get("schema") != "g9v41-nsejs-physics-core-contracts/v1":
        issues.append("MANIFEST_SCHEMA_MISMATCH")
    if contract.get("state") != "ENGINEERING_CANDIDATE__ACADEMIC_HOLD":
        issues.append("MANIFEST_AUTHORITY_ESCALATION")
    if contract.get("subject_id") != "PHYSICS" or contract.get("academic_track") != "NSEJS":
        issues.append("MANIFEST_SUBJECT_MISMATCH")
    expected = [f"PH{i:02d}" for i in range(1, 13)]
    topics = contract.get("topics", [])
    ids = [t.get("topic_id") for t in topics]
    if sorted(ids) != expected or _duplicates(ids):
        issues.append("TOPIC_PARTITION_INCOMPLETE_OR_DUPLICATED")
    ownership = contract.get("topic_ownership", {})
    for owner, expected_ids in (
        ("AGENT_1", expected[:6]), ("AGENT_2", expected[6:])
    ):
        actual = ownership.get(owner, [])
        if actual != expected_ids:
            issues.append(f"OWNER_PARTITION_MISMATCH:{owner}")
        if [t["topic_id"] for t in topics if t.get("owner") == owner] != expected_ids:
            issues.append(f"TOPIC_OWNER_MISMATCH:{owner}")
    if sorted(c.get("id") for c in contract.get("contracts", [])) != [
        f"C{i:02d}" for i in range(1, 9)
    ]:
        issues.append("EIGHT_CONTRACTS_MISSING")
    cognitive = contract.get("cognitive_contract", {})
    operations = cognitive.get("operations", [])
    if operations != ["RETRIEVE", "EXPLAIN", "APPLY", "MODEL",
                      "REPRESENT", "SYNTHESIZE", "JUSTIFY"]:
        issues.append("QRT_OPERATION_ORDER_CHANGED")
    if len(operations) * 4 != 28:
        issues.append("QRT_TEMPLATE_COUNT_MISMATCH")
    if cognitive.get("minimum_distinct_operations_per_subtopic") != 3:
        issues.append("SUBTOPIC_MINIMUM_CHANGED")
    if cognitive.get("bands") != {"D3": {"min": 6, "max": 7},
                                  "D4": {"min": 8, "max": 10}}:
        issues.append("ADVANCED_BAND_RANGES_CHANGED")
    if contract.get("gates") != list(GATES):
        issues.append("NONCOMPENSATORY_GATES_CHANGED")
    bp = contract.get("dependencies", {}).get("physics_blueprint", {})
    if (bp.get("version"), bp.get("status"), bp.get("cell_count")) != (
        "0.2.0", "DRAFT_OWNER_REVIEW", 14
    ):
        issues.append("PHYSICS_BLUEPRINT_DRAFT_AUTHORITY_CHANGED")
    shared = contract.get("dependencies", {}).get("shared_qrt_28", {})
    if shared.get("count") != 28 or shared.get("status") != "EXTERNAL_PIN_UNQUALIFIED":
        issues.append("SHARED_QRT_EXTERNAL_AUTHORITY_CHANGED")
    if contract.get("dependencies", {}).get("d1_d2_blueprint", {}).get("status") != "SPEC_PENDING":
        issues.append("D1_D2_UNAUTHORIZED_PROMOTION")
    if contract.get("dependencies", {}).get("wpe_topic_adapter", {}).get("status") != "UNSELECTED__ROOT_WORKSPACE_NOT_IN_PUBLIC_TREE":
        issues.append("WPE_ADAPTER_UNAUTHORIZED_SELECTION")
    issues.extend(verify_contract_source_pins(contract, repo_root))
    return issues


def validate_topic(
    package: dict[str, Any], contract: dict[str, Any],
    schema: dict[str, Any],
) -> list[str]:
    problems: list[str] = []
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(package), key=lambda e: str(e.path)):
        loc = "/".join(str(p) for p in error.path) or "ROOT"
        problems.append(f"SCHEMA:{loc}:{error.message}")
    if problems:
        return problems

    topic_id = package["topic_id"]
    topics = {t["topic_id"]: t for t in contract["topics"]}
    if topic_id not in topics:
        return [f"UNKNOWN_TOPIC:{topic_id}"]
    if topics[topic_id]["owner"] != package["owner_agent"]:
        problems.append(f"WRONG_OWNER:{topic_id}:{package['owner_agent']}")

    pins = package["pins"]
    deps = contract["dependencies"]
    if pins["contracts_version"] != contract["version"]:
        problems.append("CONTRACT_VERSION_MISMATCH")
    for pkg_key, dep_key, expected_version in (
        ("blueprint", "physics_blueprint", "0.2.0"),
        ("shared_qrt_28", "shared_qrt_28", "1.0.0"),
    ):
        declared = pins[pkg_key]
        authoritative = deps[dep_key]
        if declared["version"] != expected_version or (
            declared["git_blob_sha"] != authoritative["git_blob_sha"]
        ):
            problems.append(f"DEPENDENCY_PIN_MISMATCH:{pkg_key}")
    adapter = package["topic_adapter"]
    if (adapter["topic_id"] != topic_id
            or adapter["version"] != pins["topic_adapter_version"]
            or adapter["adapter_id"] != f"PHYS-TOPIC-{topic_id}"):
        problems.append("ADAPTER_ID_VERSION_TOPIC_MISMATCH")

    subtopics = package["subtopics"]
    sub_ids = [row["id"] for row in subtopics]
    science_ids = [row["id"] for row in package["science_records"]]
    science = set(science_ids)
    source_ref_ids = [row["reference_id"] for row in package["syllabus_references"]]
    for label, ids in (
        ("SUBTOPIC", sub_ids), ("SCIENCE", science_ids),
        ("SYLLABUS_REFERENCE", source_ref_ids),
        ("CORE1A", [x["id"] for x in package["core1a"]]),
        ("CORE1B", [x["id"] for x in package["core1b"]]),
        ("CORE2", [x["item_id"] for x in package["core2_sources"]]),
    ):
        for duplicate in _duplicates(ids):
            problems.append(f"DUPLICATE_{label}_ID:{duplicate}")

    target_by_id: dict[str, tuple[str, dict[str, Any]]] = {}
    op_order = contract["cognitive_contract"]["operations"]
    for sub in subtopics:
        if not sub["id"].startswith(topic_id + "-"):
            problems.append(f"CROSS_TOPIC_SUBTOPIC_ID:{sub['id']}")
        for ref in sub["syllabus_reference_ids"]:
            if ref not in source_ref_ids:
                problems.append(f"UNKNOWN_SYLLABUS_REF:{sub['id']}:{ref}")
        for ref in sub["science_ref_ids"]:
            if ref not in science:
                problems.append(f"UNKNOWN_SCIENCE_REF:{sub['id']}:{ref}")
        op_set = {t["primary_operation"] for t in sub["qrt_targets"]}
        if len(op_set) < 3:
            problems.append(f"INSUFFICIENT_DISTINCT_QRT_OPERATIONS:{sub['id']}")
        for target in sub["qrt_targets"]:
            qid = target["id"]
            if qid in target_by_id:
                problems.append(f"DUPLICATE_QRT_TARGET:{qid}")
            target_by_id[qid] = (sub["id"], target)
            try:
                ordinal = op_order.index(target["primary_operation"]) + 1
            except ValueError:
                problems.append(f"UNKNOWN_PRIMARY_OPERATION:{qid}")
                continue
            expected_cell = f"{target['band']}.{ordinal}"
            if target["blueprint_cell"] != expected_cell:
                problems.append(f"WRONG_QRT_CELL:{qid}:{expected_cell}")
            total = sum(value["score"] for value in target["factor_evidence"].values())
            band_range = contract["cognitive_contract"]["bands"][target["band"]]
            if not band_range["min"] <= total <= band_range["max"]:
                problems.append(f"BAND_FACTOR_TOTAL_MISMATCH:{qid}:{total}")
            if target["source_role"] == "DIRECT_EXAM_EVIDENCE":
                matches = [x for x in package["core2_sources"]
                           if x["item_id"] == target["task_identity"]
                           and x["source_role"] == "DIRECT_EXAM_EVIDENCE"]
                if not matches:
                    problems.append(f"EXAM_SOURCE_RECORD_MISSING:{qid}")

    adapter_cells: dict[str, set[str]] = {}
    for cell in adapter["cells"]:
        cell_id = cell["cell_id"]
        if cell_id in adapter_cells:
            problems.append(f"DUPLICATE_ADAPTER_CELL:{cell_id}")
        adapter_cells[cell_id] = set(cell["instance_ids"])
        if _duplicates(cell["instance_ids"]):
            problems.append(f"DUPLICATE_ADAPTER_INSTANCE:{cell_id}")
        for target_id in cell["instance_ids"]:
            target = target_by_id.get(target_id)
            if target is None or target[1]["blueprint_cell"] != cell_id:
                problems.append(f"ADAPTER_CELL_TARGET_MISMATCH:{cell_id}:{target_id}")
    for qid, (_, qrt) in target_by_id.items():
        if qid not in adapter_cells.get(qrt["blueprint_cell"], set()):
            problems.append(f"QRT_TARGET_MISSING_FROM_ADAPTER:{qid}")

    core1a_coverage: dict[str, int] = {}
    for lesson in package["core1a"]:
        if lesson["subtopic_id"] not in sub_ids:
            problems.append(f"CORE1A_UNKNOWN_SUBTOPIC:{lesson['id']}")
        tiers = {x["tier"] for x in lesson["progressive_examples"]}
        if tiers != {"FOUNDATION", "CONNECTED", "ADVANCED"}:
            problems.append(f"CORE1A_INCOMPLETE_PROGRESSIVE_EXAMPLES:{lesson['id']}")
        for step in lesson["derivation_steps"]:
            if step["science_ref_id"] not in science:
                problems.append(f"CORE1A_UNKNOWN_SCIENCE:{lesson['id']}")
        for target in lesson["covered_qrt_ids"]:
            if target not in target_by_id or target_by_id[target][0] != lesson["subtopic_id"]:
                problems.append(f"CORE1A_INVALID_QRT_LINK:{lesson['id']}:{target}")
            core1a_coverage[target] = core1a_coverage.get(target, 0) + 1
    for target in target_by_id:
        if core1a_coverage.get(target, 0) != 1:
            problems.append(f"CORE1A_COVERAGE_NOT_UNIQUE:{target}")

    cycle_coverage: set[tuple[str, str]] = set()
    main_by_cell: dict[str, int] = {}
    for cycle in package["core1b"]:
        qid = cycle["qrt_target_id"]
        target = target_by_id.get(qid)
        if target is None or target[0] != cycle["subtopic_id"]:
            problems.append(f"CORE1B_INVALID_TARGET:{cycle['id']}:{qid}")
            continue
        key = (qid, cycle["kind"])
        if key in cycle_coverage:
            problems.append(f"CORE1B_DUPLICATE_CYCLE:{qid}:{cycle['kind']}")
        cycle_coverage.add(key)
        if cycle["kind"] == "MAIN":
            cell = target[1]["blueprint_cell"]
            main_by_cell[cell] = main_by_cell.get(cell, 0) + 1
        # A string/bool claim cannot prove genuine novelty. It must be reviewed.
        anchor_texts = [ex["problem"].strip().casefold()
                        for lesson in package["core1a"]
                        for ex in lesson["progressive_examples"]]
        if cycle["fresh_task"].strip().casefold() in anchor_texts:
            problems.append(f"CORE1B_REUSES_WORKED_ANCHOR:{cycle['id']}")
    for qid in target_by_id:
        if (qid, "INSTANCE") not in cycle_coverage:
            problems.append(f"CORE1B_INSTANCE_MISSING:{qid}")
    for cell in adapter_cells:
        if main_by_cell.get(cell, 0) < 1:
            problems.append(f"CORE1B_MAIN_MISSING:{cell}")

    if package["acceptance"]["release"] != "HOLD":
        problems.append("RELEASE_UNAUTHORIZED")
    if any(status not in ("HOLD", "NOT_RUN")
           for status in package["acceptance"]["gates"].values()):
        problems.append("INDEPENDENT_GATE_SELF_APPROVAL")
    return problems


def inspect_package(
    path: Path, repo_root: Path = REPO_ROOT
) -> dict[str, Any]:
    contract = read_json(CONTRACT_FILE)
    schema = read_json(SCHEMA_FILE)
    Draft202012Validator.check_schema(schema)
    issues = validate_manifest(contract, repo_root)
    package = read_json(path)
    issues.extend(validate_topic(package, contract, schema))
    return {
        "file": str(path),
        "mechanical_status": "PASS" if not issues else "FAIL",
        "academic_status": "HOLD",
        "release_status": "HOLD",
        "warnings": [
            "Shared 28 QRT templates are pinned to an external repository; checkout-only validation cannot authenticate those bytes.",
            "Structural PASS never proves correctness, textbook sufficiency, blind QRT, B1-B7 admission, real first-attempt protection, or release.",
            "WPE adapter remains unselected; Physics Blueprint v0.2.0 remains DRAFT_OWNER_REVIEW; D3.1 remains PAUSED.",
        ],
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="Candidate Physics topic package JSON")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = parser.parse_args()
    result = inspect_package(args.package, args.repo_root)
    print(json.dumps(result, indent=2))
    return 0 if result["mechanical_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())

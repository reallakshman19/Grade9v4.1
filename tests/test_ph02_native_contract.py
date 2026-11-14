"""PH02 native C01–C08 v1.1 structural integrity. Does not assert academic approval."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "nsejs/physics/curriculum/agent1/PH02"
PACKAGE = BASE / "physics-topic-package.v1_1.json"
ADAPTER = BASE / "topic-adapter.PH02.v0.1.0.json"
QRT = ROOT / "nsejs/physics/ph02/qrt-candidates.v1.json"
OPS = {"EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"}


def test_ph02_native_validator_exact_candidate_no_release():
    validator_path = ROOT / "nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py"
    spec = importlib.util.spec_from_file_location("ph02_native_validator", validator_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.inspect_package(PACKAGE, ROOT)
    assert result["mechanical_status"] == "PASS", result["issues"]
    assert result["academic_status"] == "HOLD"
    assert result["release_status"] == "HOLD"


def test_ph02_native_24_distinct_targets_and_six_integrated_main():
    data = json.loads(PACKAGE.read_text(encoding="utf-8"))
    adapter = json.loads(ADAPTER.read_text(encoding="utf-8"))
    candidate = json.loads(QRT.read_text(encoding="utf-8"))
    assert data["topic_id"] == "PH02"
    assert data["status"] == "DRAFT_AUTHOR_EXPOSED"
    assert data["topic_adapter"] == adapter
    assert len(data["subtopics"]) == 8
    assert len(data["core1a"]) == 8
    assert len(candidate["tasks"]) == 16
    assert len(candidate["main_cycles"]) == 6
    assert len(data["core1b"]) == 30
    assert not data["core2_sources"]
    assert data["acceptance"]["release"] == "HOLD"
    by_id = {target["id"]: sub["id"] for sub in data["subtopics"] for target in sub["qrt_targets"]}
    assert len(by_id) == 24
    for sub in data["subtopics"]:
        assert len(sub["qrt_targets"]) == 3
        assert len({t["primary_operation"] for t in sub["qrt_targets"]}) == 3
        assert all(t["source_role"] == "AUTHORED_TRANSFER" for t in sub["qrt_targets"])
        assert all(t["qrt_status"] == "HOLD" for t in sub["qrt_targets"])
    mains = [x for x in data["core1b"] if x["kind"] == "MAIN"]
    inst = [x for x in data["core1b"] if x["kind"] == "INSTANCE"]
    assert len(mains) == 6 and len(inst) == 24
    assert {x["cell_id"] for x in mains} == {"D3.2","D3.3","D3.4","D3.5","D3.6","D3.7"}
    for main in mains:
        refs = main["instance_qrt_ids"]
        assert len(refs) >= 2
        assert len({by_id[x] for x in refs}) >= 2
        assert all(any(t["id"] == x and t["blueprint_cell"] == main["cell_id"]
                       for sub in data["subtopics"] for t in sub["qrt_targets"]) for x in refs)
        assert len(set(refs)) == len(refs)
    for cycle in data["core1b"]:
        assert cycle["runtime_verification"] == "NOT_RUN"
        assert cycle["attempt_policy"]["fail_closed_on_storage_error"]
    assert (ROOT / "nsejs/physics/core1/PH02/main/index.html").is_file()
    assert (ROOT / "nsejs/physics/textbook/PH02/index.html").is_file()


def test_ph02_candidate_boundaries_no_exam_authentication():
    data = json.loads(PACKAGE.read_text(encoding="utf-8"))
    assert not data["core2_sources"]
    assert all(x["qualification_status"] == "HOLD" for x in data["science_records"])
    assert all(x["status"] == "HOLD" for x in data["acceptance"]["b1_b7"].values())
    assert all(x in {"HOLD","NOT_RUN"} for x in data["acceptance"]["gates"].values())

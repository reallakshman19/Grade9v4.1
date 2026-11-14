"""PH02 negative mutations demonstrate native mechanical rejection, not scientific approval."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/"nsejs/physics/curriculum/contracts"
P=ROOT/"nsejs/physics/curriculum/agent1/PH02/physics-topic-package.v1_1.json"


def engine():
    path=C/"tools/validate_physics_contracts.py"
    spec=importlib.util.spec_from_file_location("ph02_adversarial_engine",path)
    module=importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def prepare():
    return (json.loads(P.read_text(encoding="utf-8")),
            json.loads((C/"core-contracts.v1_1.json").read_text(encoding="utf-8")),
            json.loads((C/"physics-topic-package.v1_1.schema.json").read_text(encoding="utf-8")))


def test_ph02_negative_exact_anchor_reuse_rejected():
    pkg,contract,schema=prepare()
    cycle=next(x for x in pkg["core1b"] if x["kind"]=="INSTANCE")
    cycle["fresh_task"]=pkg["core1a"][0]["progressive_examples"][0]["problem"]
    violations=engine().validate_topic(pkg,contract,schema)
    assert any("CORE1B_REUSES_WORKED_ANCHOR" in x for x in violations)


def test_ph02_negative_false_review_or_release_badge_rejected():
    pkg,contract,schema=prepare()
    pkg["acceptance"]["release"]="ACADEMIC_APPROVED"
    violations=engine().validate_topic(pkg,contract,schema)
    assert any("SCHEMA:acceptance/release" in x for x in violations)


def test_ph02_negative_main_incomplete_member_rejected():
    pkg,contract,schema=prepare()
    cycle=next(x for x in pkg["core1b"] if x["kind"]=="MAIN")
    cycle["instance_qrt_ids"]=cycle["instance_qrt_ids"][:-1]
    violations=engine().validate_topic(pkg,contract,schema)
    assert any("CORE1B_MAIN_INCOMPLETE_CELL_COVERAGE" in x for x in violations)


def test_ph02_negative_fake_original_exam_source_rejected():
    pkg,contract,schema=prepare()
    pkg["subtopics"][0]["qrt_targets"][0]["source_role"]="DIRECT_EXAM_EVIDENCE"
    violations=engine().validate_topic(pkg,contract,schema)
    assert any("EXAM_SOURCE_RECORD_MISSING" in x for x in violations)

"""B01 R01 cold intake integrity; NOT an independent scientific review."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
B01=ROOT/"nsejs/physics/curriculum/topics/PH07/b01"
Q=B01/"r01-cold"
SCRIPT=ROOT/"tools/physics_b01_r01_cold_intake.py"

def builder():
    spec=importlib.util.spec_from_file_location("b01_r01_cold_intake_builder",SCRIPT)
    assert spec and spec.loader
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_r01_89_blind_prompts_reproduce_exact_source_pinned_records():
    module=builder()
    actual,expected_map=module.collect()
    blind=json.loads((Q/"B01_R01_STAGE_A_PROMPTS.v1.json").read_text())
    cross=json.loads((Q/"B01_R01_STAGE_B_CROSSWALK.v1.json").read_text())
    assert actual==blind
    assert expected_map==cross
    assert blind["intake_count"]==89
    assert len(blind["items"])==89
    assert len(cross["rows"])==89
    assert len(set(x["blind_id"] for x in blind["items"]))==89
    assert len(set(x["blind_id"] for x in cross["rows"]))==89

def test_r01_stage_a_does_not_expose_author_key_qrt_metadata_or_solution():
    doc=json.loads((Q/"B01_R01_STAGE_A_PROMPTS.v1.json").read_text())
    forbidden={"target_id","subtopic_id","instance_cycle","package_path","source_role",
               "author_claimed_cell","primary_operation","band","factor_evidence",
               "decisive_route","protected_work","reconstruct","answer_key","solution"}
    assert all(not forbidden.intersection(row) for row in doc["items"])
    for row in doc["items"]:
        assert set(row)=={"blind_id","prompt","figure_intake","stage_a_submission","qualification"}
        assert re.fullmatch(r"B01-COLD-\d{3}",row["blind_id"])
        assert len(row["prompt"])>20
        assert "Shortest valid route:" not in row["prompt"]
        assert row["stage_a_submission"]=="FROZEN_INDEPENDENT_REVIEW_REQUIRED"
        assert row["qualification"]=="HOLD"
    assert doc["academic_status"]=="HOLD"

def test_r01_stage_b_89_exact_crosswalk_and_review_separation():
    blind=json.loads((Q/"B01_R01_STAGE_A_PROMPTS.v1.json").read_text())
    x=json.loads((Q/"B01_R01_STAGE_B_CROSSWALK.v1.json").read_text())
    ids={z["blind_id"] for z in blind["items"]}
    assert ids=={z["blind_id"] for z in x["rows"]}
    assert x["access_gate"]=="ONLY_AFTER_SIGNED_STAGE_A_INDEPENDENT_REASONING"
    assert x["academic_status"]=="HOLD"
    assert x["independent_reviewer"]=="NOT_ASSIGNED"
    assert x["admitted_count"]==x["selected_canonical_mains"]==0
    assert sum(z["source_kind"]=="PRIMARY" for z in x["rows"])==75
    assert sum(z["source_kind"]=="SUPPLEMENTAL" for z in x["rows"])==14
    for z in x["rows"]:
        assert z["author_solution_access"]=="OPEN_ONLY_AFTER_STAGE_A_FROZEN"
        assert z["independent_admission"]=="HOLD"
        path=ROOT/z["package_path"]
        assert path.is_file()
        assert builder().git_blob(path)==z["package_git_blob"]

def test_source_identity_conflicts_and_exam_admission_stay_hold():
    p=json.loads((B01/"B01_SOURCE_REVIEW_OVERLAY.v1.json").read_text())
    assert len(p["identity_review_queue"])==2
    assert {z["locator"] for z in p["identity_review_queue"]}=={
        "NSEJS-2018-JS511-Q9","NSEJS-2017-JS534-Q1"}
    source=json.loads((B01/"B01_CUMULATIVE_SOURCE_TO_LEARNING.v2.json").read_text())
    assert source["counts"]["direct_exam_admissions"]==0
    register=json.loads((B01/"B01_R01_REVIEW_QUEUE.v1.json").read_text())
    assert len(register["targets"])==89
    assert len(register["mixed_mains"])==16
    assert register["all_gates"]=="HOLD"

def test_no_false_independent_r01_receipt_exists():
    content=(Q/"README.md").read_text(encoding="utf-8")
    assert "author-exposed" in content.lower()
    assert "89" in content
    assert "16" in content
    assert "Stage A" in content and "Stage B" in content
    assert "independent" in content.lower()
    assert "NOT_ASSIGNED" in content

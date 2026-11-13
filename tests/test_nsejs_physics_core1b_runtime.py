"""Candidate PH01 Core1B support integrity tests; does not grant academic review."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PH01 = ROOT / "nsejs/physics/curriculum/agent1/PH01"
PACK = PH01 / "physics-topic-package.v1_1.json"
SUPPORT = PH01 / "ph01-core1b-support.v1.json"
RUNTIME = ROOT / "nsejs/physics/core1/ph01-qrt-r2/index.html"
COVERAGE = PH01 / "ph01-subtopic-qrt-coverage.v1.json"


def obj(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_twelve_cycles_have_exactly_one_support_record_each():
    p = obj(PACK)
    s = obj(SUPPORT)
    assert s["status"] == "AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"
    assert len(p["core1b"]) == len(s["cycles"]) == 12
    assert {x["cycle_id"] for x in s["cycles"]} == {x["id"] for x in p["core1b"]}


def test_hints_are_three_distinct_nonempty_stepped_texts():
    for row in obj(SUPPORT)["cycles"]:
        assert list(row["hints"]) == ["H1", "H2", "H3"]
        hints = list(row["hints"].values())
        assert all(len(h) > 50 for h in hints)
        assert len(set(hints)) == 3


def test_all_boundary_questions_have_model_closure():
    p = obj(PACK)
    support = {x["cycle_id"]: x for x in obj(SUPPORT)["cycles"]}
    for item in p["core1b"]:
        assert len(item["stages"]["boundary_test"]) > 35
        assert len(support[item["id"]]["boundary_solution"]) > 75
        assert item["stages"]["boundary_test"] != support[item["id"]]["boundary_solution"]


def test_client_attempt_protection_and_revision_code_exist():
    html = RUNTIME.read_text(encoding="utf-8")
    for phrase in (
        'crypto.subtle.digest("SHA-256", bytes)',
        'first_answer: {prediction, answer, saved_at: now()}',
        'help_exposure: record ? record.help_exposure : []',
        'revisions.push({text: note, saved_at: now()',
        'boundary_attempts.push({text: answer,saved_at: now()',
        'mastery_status: "UNASSESSED"',
        'if (!current || (record && record.first_answer)) return;',
        'window', 'localStorage.setItem',
    ):
        assert phrase in html
    assert "<iframe" not in html
    assert 'g9v41-nsejs-physics-topic-package/v1.1' in html
    assert 'TEXTBOOK_BEFORE_FIRST' in html
    assert 'TEXTBOOK_AFTER_FIRST' in html


def test_ph01_coverage_ledger_is_precise_and_unadmitted():
    p = obj(PACK)
    ledger = obj(COVERAGE)
    assert ledger["summary"]["total_subtopics"] == 8
    assert ledger["summary"]["subtopics_with_3_distinct_proposed_qrt_operations"] == len(p["subtopics"]) == 3
    assert ledger["summary"]["proposed_d3_qrt_targets"] == sum(len(s["qrt_targets"]) for s in p["subtopics"]) == 9
    assert ledger["summary"]["main_cycles_with_three_distinct_subtopics"] == len([x for x in p["core1b"] if x["kind"] == "MAIN"]) == 3
    assert ledger["summary"]["instance_cycles"] == len([x for x in p["core1b"] if x["kind"] == "INSTANCE"]) == 9
    assert ledger["summary"]["subtopics_still_missing_qrt_constructions"] == 5
    assert ledger["summary"]["qualified_qrt_targets"] == 0
    assert p["acceptance"]["release"] == "HOLD"

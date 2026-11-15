"""PH01, PH02, PH07, PH08: source-safe 41-route R00 gate.

Static engineering guard only: not a Core1A sufficiency judgment, blind QRT
review, HTTP browser run, or original examination authentication.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PH = ROOT / "nsejs/physics"
R00 = ROOT / "review/physics/ph01-ph02-ph07-ph08-r00"
FOCUS = {"PH01": 8, "PH02": 8, "PH07": 12, "PH08": 13}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_41_catalogued_routes_are_present_and_are_not_admissions():
    catalog = load(PH / "learn/catalog.json")
    manifest = load(R00 / "PHYSICS_41_ROUTE_AND_QUALITY_GATE_R00.v1.json")
    assert catalog["candidate_only"] is True
    assert manifest["mode"] == "AUTHOR_EXPOSED_STATIC_ROUTE_AUDIT__FAIL_CLOSED"
    assert manifest["counts"]["subtopic_rows"] == 41
    assert manifest["counts"]["authenticated_exam_admissions"] == 0
    assert manifest["counts"]["independent_academic_qualifications"] == 0
    assert manifest["counts"]["exact_head_browser_scenarios_executed_in_this_review"] == 0
    assert all(v == "HOLD" for k, v in manifest["qualification_status"].items()
               if k != "tablet_exact_head")
    assert manifest["qualification_status"]["tablet_exact_head"] == "NOT_RUN"
    scoped = [c for c in catalog["chapters"] if c["id"] in FOCUS]
    assert {c["id"]: len(c["units"]) for c in scoped} == FOCUS
    rows = manifest["rows"]
    assert len(rows) == 41
    assert Counter(r["chapter"] for r in rows) == Counter(FOCUS)
    assert len({r["subtopic_id"] for r in rows}) == 41
    unit_lookup = {
        (c["id"], ("PH01-" + u["id"] if c["id"] == "PH01"
                     else "PH02-" + u["id"] if c["id"] == "PH02"
                     else u["id"])): u
        for c in scoped for u in c["units"]
    }
    for r in rows:
        u = unit_lookup[(r["chapter"], r["subtopic_id"])]
        assert r["title"] == u["title"]
        assert r["core1a_path"] == "nsejs/physics/" + u["learn"]
        assert r["core1b_path"] == "nsejs/physics/" + u["practice"]
        for k in ("core1a_path", "core1b_path"):
            assert (ROOT / r[k]).is_file(), r[k]
        assert r["route_status"] == "CATALOGUED_CANDIDATE_STATIC_PATH"
        assert r["source_exam_admission"] == r["b1_b7"] == r["release"] == "HOLD"
        assert r["science_independent"] == r["qrt_independent"] == "NOT_RUN_IN_THIS_REVIEW"


def test_existing_author_evidence_does_not_promote_source_or_qrt():
    ph01 = load(PH / "curriculum/agent1/PH01/ph01-subtopic-routes.r4_7.json")
    ph02 = load(PH / "ph02/units.v1.json")
    b01 = load(PH / "curriculum/topics/PH07/b01/B01_CORE2_COVERAGE.v1.json")
    matrix = load(R00 / "PHYSICS_41_ROUTE_AND_QUALITY_GATE_R00.v1.json")
    assert ph01["status"] == "AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"
    assert len(ph01["units"]) == 8
    assert all(u["qualified"] == 0 for u in ph01["units"])
    assert ph02["academic_status"] == ph02["release_status"] == "HOLD"
    assert ph02["independent_qrt"] == "NOT_RUN"
    assert len(ph02["units"]) == 8
    assert ph02["no_original_exam_claim"] is True
    assert len(b01["rows"]) == 25
    assert b01["audit"]["qualified_direct_exam_items"] == 0
    assert b01["audit"]["qualified_d3_d4_exam_items"] == 0
    relations = {r["subtopic_id"]: r["relation"] for r in b01["rows"]}
    for r in matrix["rows"]:
        if r["chapter"] in ("PH07", "PH08"):
            assert r["source_relation"] == relations[r["subtopic_id"]]
    assert matrix["counts"]["ph07_ph08_b01_source_relations"] == dict(
        Counter(relations.values())
    )


def test_heat_and_sound_never_substitute_legacy_buoyancy_routes():
    catalog = load(PH / "learn/catalog.json")
    for c in catalog["chapters"]:
        if c["id"] in ("PH07", "PH08"):
            assert c["questionTopic"] is None
            assert c["help"] is None
            assert all(not u["title"].startswith("Continue: ") for u in c["units"])
    chapter = (PH / "learn/chapter.js").read_text(encoding="utf-8")
    nav = (PH / "learn/learner-nav.js").read_text(encoding="utf-8")
    assert "legacy fluids bank is not evidence of Heat or Sound coverage" in chapter
    assert "Read the complete chapter" not in chapter
    assert "Source-matched exam questions pending review" in chapter
    assert "Chapter complete · Return" not in nav

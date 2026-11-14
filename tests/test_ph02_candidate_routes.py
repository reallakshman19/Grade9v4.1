"""PH02 author-candidate checks: mechanical coverage only, not academic or source approval."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "nsejs/physics/ph02/units.v1.json"
EXPECTED = {f"PH02-F{i:02d}" for i in range(1, 9)}


def _data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_ph02_eight_distinct_author_units_with_hold():
    data = _data()
    assert data["schema"] == "g9v41-ph02-author-candidate-content/v1"
    assert data["academic_status"] == "HOLD"
    assert data["release_status"] == "HOLD"
    assert data["original_exam_identity"] is None
    assert data["independent_qrt"] == "NOT_RUN"
    ids = [u["id"] for u in data["units"]]
    assert len(ids) == 8 and len(set(ids)) == 8
    assert set(ids) == EXPECTED


def test_ph02_nine_witnesses_three_anchors_and_distinct_transfer():
    for u in _data()["units"]:
        for key in (
            "title", "competency", "phenomenon", "mechanism",
            "warrant", "figure", "anchor", "misconception",
            "boundary", "synthesis", "practice"
        ):
            assert u[key], (u["id"], key)
        assert len(u["progression"]) == 3
        assert [row[0] for row in u["progression"]] == [
            "FOUNDATION", "CONNECTED", "ADVANCED"
        ]
        assert u["anchor"]["problem"] != u["practice"]["prompt"]
        assert u["practice"]["uid"].startswith("AUTHORED-")
        assert u["practice"]["revision"]
        for key in (
            "prediction", "prompt", "w", "hints", "reconstruction",
            "alternative", "diagnosis", "repair",
            "boundaryPrompt", "boundaryModel"
        ):
            assert u["practice"][key], (u["id"], key)
        assert len(u["practice"]["hints"]) == 3
        assert "EXAM" not in u["practice"]["uid"]


def test_ph02_standalone_routes_have_exact_unit_identity():
    for i in range(1, 9):
        unit = f"PH02-F{i:02d}"
        sub = f"F{i:02d}"
        for kind, script, marker in (
            ("textbook", "lesson.js", "data-ph02-lesson"),
            ("core1", "practice.js", "data-ph02-practice"),
        ):
            path = ROOT / f"nsejs/physics/{kind}/PH02/{sub}/index.html"
            html = path.read_text(encoding="utf-8")
            assert f'data-unit="{unit}"' in html
            assert marker in html
            assert f'../../../ph02/{script}' in html
            assert "iframe" not in html.lower()
            assert "ACADEMIC" in html or "academic" in html


def test_ph02_fail_closed_runtime_guard_strings_present():
    script = (ROOT / "nsejs/physics/ph02/practice.js").read_text(encoding="utf-8")
    for token in (
        "first_answer", "first_prediction", "first_at", "revision",
        "localStorage.setItem", "localStorage.getItem", "round-trip mismatch",
        "invalid or stale stored revision", "reconstruct_seen",
        "hints_seen", "diagnosis_text", "repair_text",
        "boundary_attempt", "boundary_revealed", "exposure",
        "helpLink", "prehelp", "assisted_before_first"
    ):
        assert token in script
    assert script.index("ensureStored(next)") < script.index("if(ensureStored(next))refresh()")+1


def test_ph02_core1a_uses_science_figures_and_not_authentic_badge():
    script = (ROOT / "nsejs/physics/ph02/lesson.js").read_text(encoding="utf-8")
    for token in ("A1 · Observe", "A2 · What", "A3 · Construct",
                  "A4 · Derive", "A5 · Read", "A6 · Three",
                  "A7 · Worked", "A8 · Diagnose", "A9 · Counterexample",
                  'role="img"', "<svg", "Core1B transfer"):
        assert token in script
    assert "OWNER-AUTHORIZED AUTHORED LESSON" in script

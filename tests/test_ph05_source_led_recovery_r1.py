"""Candidate integrity only: no academic or source admission."""
import json
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "nsejs/physics/curriculum/agent1/PH05/source-led-r1"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_ph05_preserves_inventory_and_holds():
    data = load(DIR / "source-to-learning.v1.json")
    inv = load(ROOT / "nsejs/physics/curriculum/agent1/ph01-ph06-syllabus-inventory.v1.json")
    original = next(c["subtopics"] for c in inv["chapters"] if c["topic_id"] == "PH05")
    for key in ("subtopic_id", "title", "scope_role"):
        assert [r[key] for r in data["stable_subtopics"]] == [r[key] for r in original]
    assert data["release"] == "HOLD"
    assert data["counts"]["qualified_direct_exam_items"] == data["counts"]["qualified_d3_d4"] == 0
    assert data["counts"]["original_exam_items_published"] == 0

def test_source_leads_are_revision_bound_and_census_is_explicit():
    data = load(DIR / "source-to-learning.v1.json")
    canonical = {q["question_uid"]: q for q in load(ROOT / "nsejs/core2/question-map.v1.json")["questions"] if q["subject"] == "PHYSICS"}
    ledger = {q["question_uid"]: q for q in load(ROOT / "nsejs/data/physics-core2-integrity.v1.json")["items"]}
    seen = set()
    for row in data["source_records"]:
        assert row["source_authenticity"] == row["academic_admission"] == "HOLD"
        assert row["accepted_source_band"] is None
        if row["canonical_binding"]:
            b = row["canonical_binding"]
            assert canonical[b["question_uid"]]["content_revision_sha256"] == b["revision_sha256"]
            seen.add(b["question_uid"])
        if row["bank_binding"]:
            b = row["bank_binding"]
            assert ledger[b["question_uid"]]["observed_question_revision_sha256"] == b["revision_sha256"]
    assert seen.isdisjoint(data["source_inventory"]["unscreened_canonical_uids"])
    assert seen | set(data["source_inventory"]["unscreened_canonical_uids"]) == set(canonical)
    assert data["source_inventory"]["scope"] == "TARGETED_LEADS_ONLY__NOT_COMPLETE_CENSUS"

def test_q36_transfer_roles_and_math():
    data = load(DIR / "core1b-candidates.v1.json")
    assert data["source_band"] is None and data["source_role"] == "AUTHORED_TRANSFER"
    assert data["release"] == "HOLD" and len(data["tasks"]) == 2
    for t in data["tasks"]:
        assert t["nomination_status"] == "AUTHOR_ONLY_NOT_QUALIFIED"
        assert len(t["hints"]) == 3 and t["factors"] is None
        assert all(t[k] for k in ("prediction","prompt","w","reconstruction","alternative","diagnosis","repair","boundaryPrompt","boundaryModel"))
    # Q36 normalized G=M=d=1: both equal masses share potential release.
    assert 2 * Fraction(1,2) == Fraction(1,1)
    # PR38 contact limit: each speed squared = GM/(2R).
    assert 2 * Fraction(1,2) * Fraction(1,2) == Fraction(1,2)
    # Fresh D3: normalize G=m=s=1; total KE=4/3, initial separation=1.
    r = Fraction(9,13)
    assert 3 * (1/r - 1) == Fraction(4,3)
    # Fresh D4: r=s/2, G=m=s=1, heavy speed squared=2/3.
    assert 3 * Fraction(2,3) == 2 * (1/Fraction(1,2) - 1)
    assert "r=9s/13" in data["tasks"][0]["reconstruction"]
    assert "V²=u²" in data["tasks"][1]["reconstruction"]

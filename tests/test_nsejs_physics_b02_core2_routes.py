"""B02 scoped structural regression; not academic or Chromium acceptance."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "nsejs/physics/curriculum/topics"
PH09 = TOPICS / "PH09/subtopics"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_all_subtopics_have_separate_units_and_advanced_candidate():
    cov = load(PH09 / "B02_ADVANCED_COVERAGE.v1.json")
    ids = {f"{topic}-{i:02}" for topic, n in (("PH09",12),("PH10",17)) for i in range(1,n+1)}
    assert {x["subtopic_id"] for x in cov["subtopics"]} == ids
    for row in cov["subtopics"]:
        d = TOPICS / row["subtopic_id"][:4] / "subtopics" / row["subtopic_id"]
        for f in ("core1a.html","core1b.html","reasoning.svg","core1b-candidate.v1.json"):
            assert (d / f).is_file()
        assert row["D3"] + row["D4"] >= 1
        assert row["qualified"] == 0

def test_existing_question_links_and_fresh_pairs():
    m = load(PH09 / "core2-optics-routes.v1.json")
    integrity = load(ROOT / "nsejs/data/physics-core2-integrity.v1.json")
    revisions = {i["question_uid"]:i["observed_question_revision_sha256"] for i in integrity["items"]}
    assert len(m["routes"]) == len({r["question_uid"] for r in m["routes"]}) == 11
    for r in m["routes"]:
        assert r["academic_admission"] == r["exact_source"] == "HOLD"
        assert (ROOT / urlsplit(r["source_return"]).path).is_file()
        if r["source_collection"].endswith("physics-core2-candidates.v1.json"):
            assert revisions[r["question_uid"]] in {x["revision"] for x in r["observed_revisions"]}
        if r["route_role"] == "BLOCKED_EXAM_LOCATOR":
            assert not r["targeted_task_data"]
            continue
        for key in ("targeted_core1a","targeted_core1b","targeted_task_data"):
            assert (ROOT / r[key]).is_file()
        data = load(ROOT / r["targeted_task_data"])
        assert data["source_question_uid"] == r["question_uid"]
        assert data["source_revision_sha256"] == r["observed_question_revision_sha256"]
        assert data["acceptance"]["release"] == "HOLD"
        main, instance = data["core1b"]
        assert (main["kind"], instance["kind"]) == ("MAIN","INSTANCE")
        assert {main["id"],instance["id"]} == set(r["task_ids"])
        assert main["fresh_task"] != instance["fresh_task"]
        assert all(t["source_role"] == "AUTHORED_TRANSFER" for t in (main,instance))

def test_five_factor_arithmetic_and_no_automatic_admission():
    cov = load(PH09 / "B02_ADVANCED_COVERAGE.v1.json")
    assert len(cov["supplemental_assessments"]) == 12
    for row in cov["supplemental_assessments"]:
        factors = row["factor_evidence"]
        assert len(factors) == 5
        assert all(0 <= v["score"] <= 2 and v["evidence"] for v in factors.values())
        assert sum(v["score"] for v in factors.values()) == row["total"]
        assert row["band_candidate"] == ("D4" if row["total"] >= 8 else "D3")
        assert row["instance_band"] == "NOT_SCORED"
        assert row["disposition"] == "AUTHOR_PROPOSED__INDEPENDENT_HOLD"

def test_card_route_guard_and_no_answer_detail_on_card():
    script = (PH09 / "core2-card-links.js").read_text(encoding="utf-8")
    assert "card.dataset.questionUid" in script
    assert "card.dataset.contentRevision" in script
    assert "if (!exact) return" in script
    assert "existing.remove()" in script
    assert "route.science_or_source_hold" not in script
    assert "OFFICIAL_ID_CONTRADICTED" in script

"""Read-only Agent 2 coverage/source/reader reconciliation.

This checks contract lineage and draft structure, not science or learner mastery.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CURR = ROOT / "nsejs" / "physics" / "curriculum"
TOPICS = [f"PH{i:02d}" for i in range(7, 13)]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_eighty_three_planning_subtopics_and_exactly_twelve_native_candidates():
    record = load(CURR / "agent2/PH07_PH12_CHAPTER_COVERAGE.v1.json")
    rows = record["subtopics"]
    assert len(rows) == 83
    ids = [x["subtopic_id"] for x in rows]
    assert len(ids) == len(set(ids))
    statuses = [x["native_C01_C08_status"] for x in rows]
    assert statuses.count("LEAD_NATIVE_CANDIDATE") == 6
    assert statuses.count("SECOND_NATIVE_CANDIDATE") == 6
    assert statuses.count("NATIVE_SUBTOPIC_NOT_AUTHORED") == 71
    assert record["tally"]["independently_qualified"] == 0
    assert all(x["source_authenticity"] == "HOLD" and x["science_qualification"] == "HOLD" for x in rows)


@pytest.mark.parametrize("topic", TOPICS)
def test_chapter_anchors_match_all_planning_subtopics(topic: str):
    record = load(CURR / "agent2/PH07_PH12_CHAPTER_COVERAGE.v1.json")
    page = (CURR / f"topics/{topic}/index.html").read_text(encoding="utf-8")
    sub = [x for x in record["subtopics"] if x["topic_id"] == topic]
    assert sub
    assert "ACADEMIC_HOLD" in page
    assert "Not an approved textbook." in page
    assert 'href="core1b-preview.html"' in page
    for row in sub:
        anchor = row["chapter_section_anchor"].split("#")[-1]
        assert f'id="{anchor}"' in page, row["subtopic_id"]
        assert len(row["planned_primary_operations"]) == 3


@pytest.mark.parametrize("topic", TOPICS)
def test_two_native_subtopics_per_topic_keep_d3_only_and_all_review_gates_held(topic: str):
    pkg = load(CURR / f"topics/{topic}/physics-topic-package.v1.json")
    assert pkg["topic_id"] == topic
    assert pkg["owner_agent"] == "AGENT_2"
    assert pkg["version"] == "0.2.0"
    assert pkg["topic_adapter"]["version"] == "0.2.0"
    assert len(pkg["subtopics"]) == 2
    assert len(pkg["core1a"]) == 2
    assert len(pkg["core1b"]) == 12
    assert len({s["id"] for s in pkg["subtopics"]}) == 2
    assert pkg["core2_sources"] == []
    assert all(s["qualification_status"] == "HOLD" for s in pkg["science_records"])
    assert all(t["source_role"] == "AUTHORED_TRANSFER" and
               t["band"] == "D3" and t["qrt_status"] == "PROPOSED"
               for s in pkg["subtopics"] for t in s["qrt_targets"])
    assert pkg["acceptance"]["release"] == "HOLD"
    assert all(x == "HOLD" for x in pkg["acceptance"]["gates"].values()
               if x != "NOT_RUN")


def test_core2_corpus_and_source_holds_have_not_been_promoted():
    audit = load(CURR / "agent2/PH07_PH12_CORE2_CUSTODY_HOLD.v1.json")
    summary = audit["counts"]
    assert summary["map_physics_rows"] == 95
    assert summary["candidate_corpus_rows"] == 50
    assert summary["canonical_proven_exact"] == 0
    assert len(audit["candidates"]) == 50
    assert len(audit["known_false_exam_locators"]) == 2
    assert all(x["admission"] == "HOLD" for x in audit["candidates"])
    assert all("stem" not in x and "solution" not in x for x in audit["candidates"])


def test_reader_is_internally_linked_and_draft_only():
    index = (CURR / "agent2/index.html").read_text(encoding="utf-8")
    for topic in TOPICS:
        assert f"topics/{topic}/index.html" in index
        chapter = (CURR / f"topics/{topic}/index.html").read_text(encoding="utf-8")
        assert re.search(r"<h3 id=\"s\\d+\"", chapter)
        assert 'href="../../agent2/index.html"' in chapter
        assert 'href="core1b-preview.html"' in chapter

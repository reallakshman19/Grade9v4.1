"""Agent 2 PH07–PH12 lead authoring: exact contract and coverage smoke tests.

These prove syntax, declared lineage and mechanical consistency only.
No academic approval inferred from software validation.
"""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "nsejs" / "physics" / "curriculum"
TOPICS = tuple(f"PH{i:02d}" for i in range(7, 13))
VALIDATOR = runpy.run_path(
    str(CURRICULUM / "contracts" / "tools" / "validate_physics_contracts.py")
)["inspect_package"]


def pkg_path(topic: str) -> Path:
    return CURRICULUM / "topics" / topic / "physics-topic-package.v1.json"


@pytest.mark.parametrize("topic", TOPICS)
def test_topic_package_has_no_structural_contract_findings(topic: str) -> None:
    result = VALIDATOR(pkg_path(topic), ROOT)
    assert result["mechanical_status"] == "PASS", result["issues"]
    assert result["academic_status"] == "HOLD"
    assert result["release_status"] == "HOLD"


@pytest.mark.parametrize("topic", TOPICS)
def test_lead_coverage_is_specific_and_source_neutral(topic: str) -> None:
    data = json.loads(pkg_path(topic).read_text(encoding="utf-8"))
    assert data["owner_agent"] == "AGENT_2"
    assert data["topic_adapter"]["adapter_id"] == "PHYS-TOPIC-" + topic
    assert data["core2_sources"] == []
    assert all(t["source_role"] == "AUTHORED_TRANSFER" for s in data["subtopics"] for t in s["qrt_targets"])
    assert all(t["qrt_status"] == "PROPOSED" for s in data["subtopics"] for t in s["qrt_targets"])
    assert data["acceptance"]["release"] == "HOLD"
    assert len(data["core1a"]) == 1, "Only one lead section is authored per topic in this slice"
    assert len(data["core1b"]) == 6
    assert all(c["runtime_verification"] == "NOT_RUN" for c in data["core1b"])
    assert all("APPROVED" not in str(v) for v in data["acceptance"]["gates"].values())


@pytest.mark.parametrize("topic", TOPICS)
def test_manuscript_has_non_duplicate_example_tiers(topic: str) -> None:
    data = json.loads(pkg_path(topic).read_text(encoding="utf-8"))
    lesson = data["core1a"][0]
    examples = lesson["progressive_examples"]
    assert [x["tier"] for x in examples] == ["FOUNDATION", "CONNECTED", "ADVANCED"]
    assert len({x["problem"].strip().lower() for x in examples}) == 3
    assert len(lesson["scientific_narrative"].split()) >= 95
    assert all(step["why_valid"] for step in lesson["derivation_steps"])
    chapter = (CURRICULUM / "topics" / topic / "CHAPTER_LEAD_DRAFT.md").read_text(encoding="utf-8")
    assert len(chapter.split()) >= 370
    assert "NOT COMPLETE CHAPTER" in chapter
    assert chapter.count("**Independent check:**") == 3


def test_inventory_matches_phase_zero_partition_without_false_completion() -> None:
    record = json.loads(
        (CURRICULUM / "agent2" / "PH07_PH12_SUBTOPIC_REGISTER.v1.json").read_text(encoding="utf-8")
    )
    assert record["source_count"] == 83
    assert record["counts"] == {
        "PH07": 12, "PH08": 13, "PH09": 12,
        "PH10": 17, "PH11": 14, "PH12": 15,
    }
    ids = [s["id"] for s in record["subtopics"]]
    assert len(ids) == len(set(ids)) == 83
    assert all(len(set(s["qrt_operations"])) == 3 for s in record["subtopics"])
    assert set(record["authored_leads"]) == set(TOPICS)
    for topic in TOPICS:
        assert record["authored_leads"][topic] in ids


def test_no_proposed_d4_is_masquerading_as_admitted() -> None:
    for topic in TOPICS:
        p = json.loads(pkg_path(topic).read_text(encoding="utf-8"))
        for s in p["subtopics"]:
            for task in s["qrt_targets"]:
                assert task["band"] == "D3"  # D4 gaps deliberately unfilled until warranted
                assert task["source_role"] == "AUTHORED_TRANSFER"
        assert all(v["status"] == "HOLD" for v in p["acceptance"]["b1_b7"].values())


def test_worked_physics_anchor_arithmetic() -> None:
    # Independent elementary sanity checks for the authored anchor examples.
    # Mirror image: f=12 cm, object x=24 cm -> virtual v=8 cm.
    assert 12 * 24 / (12 + 24) == 8
    # Lens displacement: D=90 cm, f=20 cm, x=(30,60).
    assert 30 * 60 == 90 * 20
    assert 90 * 90 - 4 * 90 * 20 == 30 * 30
    # Parallel resistors: 6 and 3 ohms -> 2 ohms.
    assert (6 * 3) / (6 + 3) == 2
    # A co-located 0.60-s echo at 340 m/s gives a wall 102 m away.
    assert 340 * 0.60 / 2 == 102

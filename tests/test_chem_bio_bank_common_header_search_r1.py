"""Chemistry/Biology bank discoverability, shared published header, safe search index contract.

These tests verify routes and status, not exam-source authentication.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_both_candidate_banks_are_present_and_academically_disclaimed():
    cases = (
        ("chemistry", "atomic_structure", 6),
        ("biology", "living_world", 5),
    )
    for subject, topic, topics in cases:
        page = read(f"nsejs/{subject}/index.html")
        data = json.loads(read(f"nsejs/data/{subject}-core2-candidates.v1.json"))
        reader = read(f"nsejs/js/core2-{subject}-reader.js")
        assert len(data["questions"]) == data["total_questions"] == 119
        assert len({q["topic"] for q in data["questions"]}) == topics
        assert all(q.get("stem") for q in data["questions"])
        assert f'href="index.html?topic={topic}#topicWorkspace"' in page
        assert "119 candidates" in page
        assert 'id="qbSearch"' in page and 'id="topicWorkspace"' in page
        assert f'fetch("../data/{subject}-core2-candidates.v1.json")' in reader
        assert "Peer-Audited Curriculum" not in page
        assert "official verified key" not in reader.lower()
        assert "not independently authenticated" in reader.lower()
        assert "HOLD" in page and "HOLD" in reader


def test_chemistry_has_single_canonical_chapter_route_and_visible_bank():
    hub = read("nsejs/chemistry/index.html")
    registry = json.loads(read("nsejs/chemistry/learner-navigation.v1.json"))
    assert len(registry["units"]) == 14
    assert sum(len(u["subtopics"]) for u in registry["units"]) == 84
    assert not registry["rules"]["legacy_bank_collapsed_by_default"]
    assert 'id="chem-bank-archive" class="chem-bank-archive" open' in hub
    assert 'href="#chem-chapters"' in hub
    assert hub.count('class="chem-chapter-card"') == 14


def test_biology_topic_deep_links_are_real_links_and_not_javascript_void():
    page = read("nsejs/biology/index.html")
    assert "javascript:void(0)" not in page
    for topic in ("living_world", "life_processes", "coordination", "genetics", "environment"):
        assert f'index.html?topic={topic}#topicWorkspace' in page


def test_same_header_contract_is_installed_on_all_published_html():
    nav = read("site-nav.js")
    workflow = read(".github/workflows/owner-technical-preview-pages.yml")
    assert 'function normalizeMast(' in nav
    assert 'normalizeMast(mast,link,routes,current,scope)' in nav
    assert 'Grade9 common navigation: subjects, NSEJS and search' in nav
    for destination in ("index.html", "nsejs/index.html", "nsejs/physics/index.html",
                        "nsejs/chemistry/index.html", "nsejs/biology/index.html",
                        "mathematics/index.html", "architecture/index.html"):
        assert destination in nav
    assert 'nsejs/chemistry/question-bank.html' not in nav
    assert 'nsejs/biology/question-bank.html' not in nav
    assert 'data-grade9-nav="common-r1"' in workflow
    assert 'for item in folder.rglob("*"):' in workflow
    assert 'target.suffix.lower() in {".html", ".htm"}' in workflow
    assert 're.search(r"</body\\s*>"' in workflow
    assert 'PREVIEW_COMMON_NAV_NOT_INSTALLED' in workflow
    # The staged-pages scan must interpret regex whitespace, not a literal
    # backslash followed by "s" (which previously counted zero HTML pages).
    assert 're.search(r"</body\\\\s*>", page' not in workflow
    assert 're.search(r"</body\\s*>", page' in workflow


def test_published_search_rebuild_is_safe_and_contains_bank_routes():
    workflow = read(".github/workflows/owner-technical-preview-pages.yml")
    builder = read("tools/build_search_index.py")
    assert 'python3 tools/build_search_index.py' in workflow
    assert 'QUESTION_BANK_NOT_INDEXED' in workflow
    assert 'ANSWER_BEARING_SEARCH_INDEX' in workflow
    assert 'PAGE-{key}-QUESTION-BANK' in builder
    assert 'topic={topic}#topicWorkspace' in builder
    assert 'CANDIDATE QUESTION BANK · ACADEMIC HOLD' in builder
    assert 'options = []' in builder and 'hints = []' in builder
    assert 'python trusted/docs/agent-entry/production-control-r3/release.py' in read(".github/workflows/deploy.yaml")

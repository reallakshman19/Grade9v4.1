"""Test verification of Search 2 (Question Bank Inline Reader Search & Filter Bar)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_qb_filter_panel_present_in_all_subject_readers():
    pages = [
        ROOT / "nsejs" / "physics" / "index.html",
        ROOT / "nsejs" / "chemistry" / "index.html",
        ROOT / "nsejs" / "biology" / "index.html",
    ]
    for page in pages:
        content = page.read_text(encoding="utf-8")
        assert 'id="qbFilters"' in content, f"qbFilters missing in {page}"
        assert 'id="qbSearch"' in content, f"qbSearch input missing in {page}"
        assert 'id="qbTopicSelect"' in content, f"qbTopicSelect missing in {page}"
        assert 'id="qbDifficulty"' in content, f"qbDifficulty missing in {page}"
        assert 'id="qbExam"' in content, f"qbExam missing in {page}"
        assert 'id="qbSort"' in content, f"qbSort missing in {page}"
        assert 'id="qbClear"' in content, f"qbClear missing in {page}"
        assert 'id="qbResultCount"' in content, f"qbResultCount missing in {page}"

def test_qb_filter_css_styles_present():
    css_file = ROOT / "css" / "site-search.css"
    content = css_file.read_text(encoding="utf-8")
    assert ".qb-filter-panel" in content
    assert ".qb-search-field" in content
    assert ".qb-filter-controls" in content
    assert ".qb-result-count" in content
    assert ".card-highlight" in content

def test_qb_filter_js_logic_present():
    scripts = [
        ROOT / "nsejs" / "js" / "core2-physics-reader.js",
        ROOT / "nsejs" / "js" / "core2-chemistry-reader.js",
        ROOT / "nsejs" / "js" / "core2-biology-reader.js",
    ]
    for script in scripts:
        content = script.read_text(encoding="utf-8")
        assert "filterState" in content, f"filterState missing in {script}"
        assert "applyFilters" in content, f"applyFilters missing in {script}"
        assert "initFilterBar" in content, f"initFilterBar missing in {script}"
        assert "resetFilters" in content, f"resetFilters missing in {script}"
        assert "qb-card-anchor" in content or "data-qid" in content, f"anchor linking missing in {script}"

def test_attempt_evaluation_and_key_highlighting():
    # 1. Verify CSS styles for attempt evaluation and correct-key highlights
    css_content = (ROOT / "css" / "tablet-12-7.css").read_text(encoding="utf-8")
    assert ".opt-user-correct" in css_content
    assert ".opt-user-wrong" in css_content
    assert ".opt-correct-key" in css_content
    assert ".attempt-feedback-banner" in css_content
    assert ".feedback-correct" in css_content
    assert ".feedback-wrong" in css_content

    # 2. Verify reader scripts evaluate attempts and highlight correct keys
    readers = [
        ROOT / "nsejs" / "js" / "core2-physics-reader.js",
        ROOT / "nsejs" / "js" / "core2-chemistry-reader.js",
        ROOT / "nsejs" / "js" / "core2-biology-reader.js",
    ]
    for reader in readers:
        code = reader.read_text(encoding="utf-8")
        assert "renderAttemptFeedback" in code, f"renderAttemptFeedback missing in {reader}"
        assert "opt-correct-key" in code, f"opt-correct-key highlighting missing in {reader}"
        assert "opt-user-wrong" in code, f"opt-user-wrong highlighting missing in {reader}"
        assert "attempt-feedback-banner" in code, f"attempt-feedback-banner missing in {reader}"
        assert "retryBtn" in code, f"retryBtn missing in {reader}"

"""Unit tests for Grade9 v4.0 Unified & Customizable Site Search Engine.

Validates:
1. Search index generation, document count, and manifest integrity.
2. Search document schema and category taxonomy.
3. Scoping customizability (all, nsejs-only, per-subject).
4. Relevance matching, query resolution, and synonym expansion.
5. Search assets (JSON, JS, CSS) availability across portal and nsejs directories.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def search_index():
    index_path = REPO_ROOT / "data" / "learner-search-index.v1.json"
    assert index_path.exists(), "Search index file data/learner-search-index.v1.json must exist."
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def search_manifest():
    manifest_path = REPO_ROOT / "data" / "learner-search-manifest.v1.json"
    assert manifest_path.exists(), "Manifest file data/learner-search-manifest.v1.json must exist."
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def keyword_synonyms():
    syn_path = REPO_ROOT / "data" / "keyword-synonyms.v1.json"
    assert syn_path.exists(), "Thesaurus file data/keyword-synonyms.v1.json must exist."
    with open(syn_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_search_index_manifest_integrity(search_index, search_manifest):
    """Manifest matches index length and SHA-256 fingerprint."""
    assert len(search_index) == search_manifest["total_documents"]
    assert search_manifest["total_documents"] >= 300, "Should index at least 300 learning documents."

    raw_bytes = (REPO_ROOT / "data" / "learner-search-index.v1.json").read_bytes()
    computed_sha = hashlib.sha256(raw_bytes).hexdigest()
    assert computed_sha == search_manifest["sha256"]

    # Verify mirrored copy in nsejs/data/
    nsejs_path = REPO_ROOT / "nsejs" / "data" / "learner-search-index.v1.json"
    assert nsejs_path.exists()
    assert hashlib.sha256(nsejs_path.read_bytes()).hexdigest() == computed_sha


def test_search_document_taxonomy_and_fields(search_index):
    """Every search document conforms to required metadata contract."""
    allowed_categories = {"question", "tablet", "curriculum", "page"}
    allowed_subjects = {"Physics", "Chemistry", "Biology", "Mathematics", "Common", "Cross-Subject"}

    assert len(search_index) > 0
    for doc in search_index:
        assert "id" in doc and doc["id"], "Document must have an ID"
        assert "title" in doc and doc["title"], f"Document {doc['id']} must have a title"
        assert "type" in doc and doc["type"], f"Document {doc['id']} must have a type"
        assert doc["category"] in allowed_categories, f"Invalid category {doc['category']} in {doc['id']}"
        assert doc["subject"] in allowed_subjects, f"Invalid subject {doc['subject']} in {doc['id']}"
        assert "url" in doc and doc["url"], f"Document {doc['id']} must have a target URL"
        assert "search_text" in doc and doc["search_text"], f"Document {doc['id']} must have a search vector"
        assert "badge" in doc and doc["badge"], f"Document {doc['id']} must have a display badge"
        assert "is_nsejs" in doc, f"Document {doc['id']} must declare is_nsejs boolean"


def test_customizable_nsejs_scoping(search_index):
    """Scoping to 'is_nsejs' isolates only Junior Science items."""
    nsejs_docs = [d for d in search_index if d.get("is_nsejs")]
    non_nsejs_docs = [d for d in search_index if not d.get("is_nsejs")]

    assert len(nsejs_docs) >= 280, "NSEJS scope should cover questions, tablets, and topic hubs."
    assert len(non_nsejs_docs) >= 3, "Non-NSEJS scope covers portal hubs and WPE pilot."

    # Verify all 3 subjects exist in NSEJS scope
    nsejs_subjects = {d["subject"] for d in nsejs_docs}
    assert "Physics" in nsejs_subjects
    assert "Chemistry" in nsejs_subjects
    assert "Biology" in nsejs_subjects

    # Check question distribution
    questions = [d for d in nsejs_docs if d["category"] == "question"]
    assert len(questions) >= 270, "Should include at least 270 candidate & authored questions."


def test_subject_scoping_isolation(search_index):
    """Filter by subject produces isolated, non-empty candidate subsets."""
    for subj in ["Physics", "Chemistry", "Biology"]:
        subj_docs = [d for d in search_index if d["subject"] == subj]
        assert len(subj_docs) >= 40, f"Subject {subj} must have at least 40 indexed items."
        # Verify no document in this slice has wrong subject
        assert all(d["subject"] == subj for d in subj_docs)


def test_question_locator_and_stem_retrieval(search_index):
    """Key candidate questions can be retrieved by ID, locator, and stem keyword."""
    # 1. Physics Ant convex mirror question
    ant_matches = [d for d in search_index if "ant" in d["search_text"] and "convex" in d["search_text"]]
    assert len(ant_matches) >= 1
    assert any(d["original_id"] == "NSEJS-2023-P-Q01" or "NSEJS-23-OPT-01" in d["title"] for d in ant_matches)

    # 2. Chemistry Bohr model electron transition
    bohr_matches = [d for d in search_index if "bohr" in d["search_text"] and "electron" in d["search_text"]]
    assert len(bohr_matches) >= 1
    assert any("CHEM-NSEJS-ATOM" in d["id"] or "ATOM" in d["title"] for d in bohr_matches)

    # 3. Biology Sweet pea purple flower genetics
    pea_matches = [d for d in search_index if "sweet pea" in d["search_text"] or "lathyrus" in d["search_text"]]
    assert len(pea_matches) >= 1
    assert any("BIO-NSEJS-GEN" in d["id"] for d in pea_matches)

    # 4. Authored Practice question
    auth_matches = [d for d in search_index if "G9-AUTH-MECH" in d["id"] or "G9-AUTH-MECH" in d["search_text"]]
    assert len(auth_matches) >= 1


def test_synonym_thesaurus_coverage(keyword_synonyms):
    """Synonyms thesaurus defines active aliases for core STEM domains."""
    syns = keyword_synonyms.get("synonyms", [])
    assert len(syns) >= 10, "Must have comprehensive synonyms entries."
    slugs = {s["slug"] for s in syns}
    for expected in ["optics", "fluids", "circuits", "atomic-structure", "chemical-bonding", "mole-concept", "redox", "genetics", "immunology", "virology", "nsejs"]:
        assert expected in slugs, f"Missing expected synonym slug: {expected}"


def test_search_runtime_and_stylesheet_assets():
    """Client-side search runtime script and CSS stylesheet exist and are non-empty."""
    js_path = REPO_ROOT / "js" / "site-search.js"
    css_path = REPO_ROOT / "css" / "site-search.css"

    assert js_path.exists(), "js/site-search.js must exist."
    assert css_path.exists(), "css/site-search.css must exist."

    js_code = js_path.read_text(encoding="utf-8")
    assert "Grade9Search" in js_code
    assert "openSearch" in js_code
    assert "setScope" in js_code
    assert "scoreItem" in js_code
    assert "Ctrl" in js_code

    css_code = css_path.read_text(encoding="utf-8")
    assert ".g9-search-dialog" in css_code
    assert ".g9-search-scope-bar" in css_code
    assert ".g9-search-tab" in css_code
    assert ".g9-search-qb-bridge" in css_code

"""Complete search inventory and deliberately wrong negative-control fixtures."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from audit_search_full import REQUIRED_ENTRYPOINTS, audit
from search_learner_pages import public_pages, is_public_html


def put(root, path, data):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(data, encoding="utf-8")


def public_fixture(tmp_path):
    docs = []
    for i, path in enumerate(REQUIRED_ENTRYPOINTS):
        put(tmp_path, path, "<html><head><title>Learn</title></head><body>"
            '<script src="site-nav.js" data-grade9-nav="common-r1"></script></body></html>')
        if path.startswith("nsejs/"):
            subj = path.split("/")[1].title() if path.count("/") >= 2 else "Common"
        elif path.startswith(("physics/", "chemistry/", "mathematics/")):
            subj = path.split("/")[0].title()
        else:
            subj = "Common"
        docs.append({
            "id": "TEST-" + str(i), "url": path, "title": "Learner " + str(i),
            "search_text": "learner " + str(i), "subject": subj, "category": "page",
            "is_nsejs": path.startswith("nsejs/"),
            "badge": "LEARNING CANDIDATE · HOLD" if path.startswith("nsejs/")
                     else "TECHNICAL PREVIEW · REVIEW PENDING",
        })
    put(tmp_path, "js/site-search.js",
        "let currentScope = isNSEJSPage ? 'nsejs' : 'all';")
    put(tmp_path, "site-nav.js", "// nav")
    index = json.dumps(docs, ensure_ascii=False, indent=2).encode("utf-8")
    meta = {
        "sha256": hashlib.sha256(index).hexdigest(),
        "total_documents": len(docs),
        "public_html_pages": len(public_pages(tmp_path)),
        "by_subject": dict(Counter(d["subject"] for d in docs)),
        "by_category": dict(Counter(d["category"] for d in docs)),
    }
    for p in ("data/learner-search-index.v1.json",
              "nsejs/data/learner-search-index.v1.json"):
        (tmp_path / p).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / p).write_bytes(index)
    for p in ("data/learner-search-manifest.v1.json",
              "nsejs/data/learner-search-manifest.v1.json"):
        put(tmp_path, p, json.dumps(meta))
    for p in ("data/keyword-synonyms.v1.json",
              "nsejs/data/keyword-synonyms.v1.json"):
        put(tmp_path, p, '{"synonyms":[]}')
    return docs


def test_all_published_subject_families_are_in_discovery():
    pages = set(public_pages(ROOT))
    for path in REQUIRED_ENTRYPOINTS:
        assert path in pages, path
    for path in ("preview/index.html", "preview/batches/index.html",
                 "architecture/guidebook.html", "docs/agent-entry/index.html",
                 "nsejs/biology/question-bank.html", "nsejs/chemistry/question-bank.html"):
        assert path in pages, path
    for forbidden in ("preview/404.html", "preview/alpha-board.html",
                      "preview/question-status-archive.html",
                      "nsejs/physics/curriculum/topics/PH07/b01/source-to-learning-review.html",
                      "workspace/legacy/g9v3.5/some.html",
                      "review/physics/test.html"):
        assert not is_public_html(forbidden), forbidden


def test_audit_accepts_proper_full_public_fixture(tmp_path):
    public_fixture(tmp_path)
    report = audit(tmp_path, tmp_path)
    assert report["status"] == "PASS", report["errors"]
    assert report["stats"]["eligible_html"] == len(REQUIRED_ENTRYPOINTS)
    assert report["stats"]["indexed_documents"] == len(REQUIRED_ENTRYPOINTS)


def test_negative_duplicate_and_dead_link_are_rejected(tmp_path):
    docs = public_fixture(tmp_path)
    docs[1]["id"] = docs[0]["id"]
    docs[2]["url"] = "not-found.html"
    for p in ("data/learner-search-index.v1.json",
              "nsejs/data/learner-search-index.v1.json"):
        put(tmp_path, p, json.dumps(docs))
    result = audit(tmp_path, tmp_path)
    assert result["status"] == "FAIL"
    assert any("DUPLICATE_SEARCH_ID" in x for x in result["errors"])
    assert any("DEAD_OR_UNSAFE_RESULT" in x for x in result["errors"])


def test_negative_answer_leak_mirrors_and_hash_are_rejected(tmp_path):
    docs = public_fixture(tmp_path)
    docs[0]["answer"] = "deliberately unsafe fixture"
    put(tmp_path, "data/learner-search-index.v1.json", json.dumps(docs))
    result = audit(tmp_path, tmp_path)
    assert result["status"] == "FAIL"
    assert any("ANSWER_OR_REVIEW_PAYLOAD_IN_INDEX" in x for x in result["errors"])
    assert "SEARCH_INDEX_MIRRORS_DIFFER" in result["errors"]
    assert "INDEX_SHA256_MANIFEST_MISMATCH" in result["errors"]


def test_negative_unindexed_learner_page_and_search_loader_are_rejected(tmp_path):
    public_fixture(tmp_path)
    put(tmp_path, "physics/missing-coverage.html", "<body></body>")
    result = audit(tmp_path, tmp_path)
    assert result["status"] == "FAIL"
    assert "UNINDEXED_PUBLIC_HTML:physics/missing-coverage.html" in result["errors"]
    assert "PUBLISHED_HTML_WITHOUT_SEARCH:physics/missing-coverage.html" in result["errors"]

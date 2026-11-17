#!/usr/bin/env python3
"""Independent full public search audit, run AFTER building and staging Pages.

This checks the actual deployable files, not only the author's recent edits.
Historical/evidence pages may be staged but must not be promoted as learner
search records. The audit writes reports OUTSIDE public/, never review payloads.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from search_learner_pages import public_pages  # noqa: E402

FORBIDDEN_KEYS = {
    "answer", "answers", "answer_key", "correct_option", "official_option",
    "solution", "solutions", "worked_solution", "final_answer", "steps",
    "reconstruction", "boundaryModel", "diagnosis", "repair", "key",
}
REQUIRED_ENTRYPOINTS = (
    "index.html", "physics/index.html", "chemistry/index.html",
    "mathematics/index.html", "architecture/index.html",
    "nsejs/index.html", "nsejs/physics/index.html",
    "nsejs/chemistry/index.html", "nsejs/biology/index.html",
    "physics/wpe/index.html",
)
# A shell with a required query parameter should not get an empty reader hit.
# Selected question/lesson routes to these shells are indexed separately.
DYNAMIC_SHELLS = {
    "nsejs/physics/learn/chapter.html",
    "nsejs/physics/ph05/source-led-r2/index.html",
    "nsejs/physics/ph05/source-checkpoint.html",
    "nsejs/chemistry/textbook/index.html",
    "nsejs/physics/quality-r1/study.html",
    "nsejs/physics/quality-r1/challenge.html",
    "nsejs/physics/quality-r1/source.html",
}


def audit(repo: Path, staged: Path) -> dict:
    errors = []
    warnings = []
    stats = {}
    primary = staged / "data/learner-search-index.v1.json"
    mirror = staged / "nsejs/data/learner-search-index.v1.json"
    manifest = staged / "data/learner-search-manifest.v1.json"
    other_manifest = staged / "nsejs/data/learner-search-manifest.v1.json"
    synonyms = staged / "data/keyword-synonyms.v1.json"
    other_synonyms = staged / "nsejs/data/keyword-synonyms.v1.json"

    for required in (primary, mirror, manifest, other_manifest, synonyms, other_synonyms,
                     staged / "js/site-search.js", staged / "site-nav.js"):
        if not required.is_file():
            errors.append("MISSING_PUBLICATION_ASSET:" + required.relative_to(staged).as_posix())
    if errors:
        return {"status": "FAIL", "errors": errors, "warnings": warnings, "stats": stats}

    idx_raw = primary.read_bytes()
    manifest_raw = manifest.read_bytes()
    if idx_raw != mirror.read_bytes():
        errors.append("SEARCH_INDEX_MIRRORS_DIFFER")
    if manifest_raw != other_manifest.read_bytes():
        errors.append("SEARCH_MANIFEST_MIRRORS_DIFFER")
    if synonyms.read_bytes() != other_synonyms.read_bytes():
        errors.append("SYNONYM_MIRRORS_DIFFER")

    try:
        docs = json.loads(idx_raw)
        meta = json.loads(manifest_raw)
    except (ValueError, UnicodeDecodeError) as exc:
        return {"status": "FAIL", "errors": ["INVALID_SEARCH_JSON:" + str(exc)],
                "warnings": warnings, "stats": stats}
    if not isinstance(docs, list) or not docs:
        return {"status": "FAIL", "errors": ["EMPTY_OR_NONLIST_INDEX"],
                "warnings": warnings, "stats": stats}

    sha = hashlib.sha256(idx_raw).hexdigest()
    if meta.get("sha256") != sha:
        errors.append("INDEX_SHA256_MANIFEST_MISMATCH")
    if meta.get("total_documents") != len(docs):
        errors.append("INDEX_DOCUMENT_COUNT_MISMATCH")

    categories = Counter()
    subjects = Counter()
    seen_ids = set()
    seen_urls = set()
    covered_paths = set()
    bad_urls = []
    for i, item in enumerate(docs):
        if not isinstance(item, dict):
            errors.append("NONOBJECT_SEARCH_RECORD:" + str(i))
            continue
        identity, url = item.get("id"), item.get("url")
        if not isinstance(identity, str) or not identity:
            errors.append("MISSING_SEARCH_ID:" + str(i))
        elif identity in seen_ids:
            errors.append("DUPLICATE_SEARCH_ID:" + identity)
        seen_ids.add(identity)
        if not isinstance(url, str) or not url:
            errors.append("MISSING_SEARCH_URL:" + str(i))
            continue
        if url in seen_urls:
            errors.append("DUPLICATE_SEARCH_URL:" + url)
        seen_urls.add(url)
        parsed = urlsplit(url)
        path = unquote(parsed.path)
        parts = PurePosixPath(path).parts
        if (parsed.scheme or parsed.netloc or path.startswith("/") or not path
                or ".." in parts or any(part.startswith(".") for part in parts)):
            bad_urls.append(url)
            continue
        if not (staged / path).is_file():
            bad_urls.append(url)
        covered_paths.add(path)
        subject = item.get("subject")
        category = item.get("category")
        subjects[str(subject)] += 1
        categories[str(category)] += 1
        if category not in {"question", "tablet", "curriculum", "page"}:
            errors.append("INVALID_SEARCH_CATEGORY:" + str(identity))
        if not isinstance(item.get("title"), str) or not item.get("title"):
            errors.append("EMPTY_SEARCH_TITLE:" + str(identity))
        if not isinstance(item.get("search_text"), str) or not item.get("search_text"):
            errors.append("EMPTY_SEARCH_VECTOR:" + str(identity))
        if FORBIDDEN_KEYS.intersection(item):
            errors.append("ANSWER_OR_REVIEW_PAYLOAD_IN_INDEX:" + str(identity))
        if category == "question" and (item.get("options", []) != [] or item.get("hints", []) != []):
            errors.append("QUESTION_ANSWER_BEARING_FIELDS:" + str(identity))
        if item.get("is_nsejs") and "HOLD" not in str(item.get("badge", "")):
            errors.append("NSEJS_CONTENT_MISSING_HOLD_LABEL:" + str(identity))

    if bad_urls:
        errors.extend("DEAD_OR_UNSAFE_RESULT:" + x for x in bad_urls[:30])
    for kind, cnt in categories.items():
        if meta.get("by_category", {}).get(kind) != cnt:
            errors.append("CATEGORY_COUNT_MISMATCH:" + kind)
    for subject, cnt in subjects.items():
        if meta.get("by_subject", {}).get(subject) != cnt:
            errors.append("SUBJECT_COUNT_MISMATCH:" + subject)

    indexable = set(public_pages(repo))
    unindexed = sorted(indexable.difference(covered_paths).difference(DYNAMIC_SHELLS))
    if unindexed:
        errors.extend("UNINDEXED_PUBLIC_HTML:" + path for path in unindexed[:40])
    for path in REQUIRED_ENTRYPOINTS:
        if path not in covered_paths:
            errors.append("MISSING_SITE_ENTRYPOINT:" + path)

    published_html = sorted(p.relative_to(staged).as_posix()
                            for p in staged.rglob("*.html") if p.is_file())
    staged_navigation = 0
    missing_navigation = []
    for path in published_html:
        raw = (staged / path).read_text(encoding="utf-8", errors="replace")
        if re.search(r"</body\s*>", raw, flags=re.I):
            staged_navigation += 1
            if 'data-grade9-nav' not in raw and "js/site-search.js" not in raw:
                missing_navigation.append(path)
    if missing_navigation:
        errors.extend("PUBLISHED_HTML_WITHOUT_SEARCH:" + x for x in missing_navigation[:40])
    if meta.get("public_html_pages") != len(indexable):
        errors.append("PUBLIC_HTML_COUNT_MISMATCH")
    if len(published_html) < len(indexable):
        errors.append("PUBLISHED_HTML_BELOW_INDEXABLE_COUNT")
    if not {"Physics", "Chemistry", "Biology", "Mathematics", "Common"} <= set(subjects):
        errors.append("MISSING_SUBJECT_IN_SEARCH")
    runtime = (staged / "js/site-search.js").read_text(encoding="utf-8")
    if "let currentScope = isNSEJSPage ? 'nsejs' : 'all'" not in runtime:
        errors.append("HOME_SEARCH_NOT_ALL_PORTALS")
    skipped = sorted(set(published_html).difference(indexable))
    # These may be technical, historical or evidence pages. Report rather
    # than silently counting them as verified discoverable learner content.
    if skipped:
        warnings.append("PUBLISHED_BUT_EXCLUDED_FROM_LEARNER_SEARCH:" + str(len(skipped)))

    stats.update({
        "published_html": len(published_html),
        "published_with_search_loader": staged_navigation,
        "eligible_html": len(indexable),
        "indexed_documents": len(docs),
        "by_category": dict(categories),
        "by_subject": dict(subjects),
        "nonindexed_published_html": skipped,
        "eligible_html_without_results": unindexed,
        "index_sha256": sha,
    })
    return {"schema": "g9-search-publication-audit/v1",
            "status": "PASS" if not errors else "FAIL",
            "errors": errors, "warnings": warnings, "stats": stats}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--staged", type=Path, default=ROOT / "public")
    parser.add_argument("--json-output", type=Path, default=ROOT / "artifacts/search-full-audit.json")
    parser.add_argument("--summary-output", type=Path, default=ROOT / "artifacts/search-full-audit.md")
    args = parser.parse_args()
    report = audit(args.repo, args.staged)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    stats = report.get("stats", {})
    lines = [
        "# Grade9 full-site search publication audit",
        "",
        "**Status: " + report["status"] + "**",
        "",
        "| Check | Count |",
        "|---|---:|",
    ]
    lines.extend("| " + key.replace("_", " ") + " | " + str(stats.get(key, "?")) + " |"
                 for key in ("published_html", "published_with_search_loader",
                             "eligible_html", "indexed_documents"))
    lines.extend(["", "## By subject", ""])
    lines.extend("- " + subject + ": " + str(count)
                 for subject, count in sorted(stats.get("by_subject", {}).items()))
    lines.extend(["", "## Errors", ""])
    lines.extend("- " + x for x in report["errors"] or ["None"])
    lines.extend(["", "## Non-indexed published pages (by policy)", ""])
    lines.extend("- " + x for x in stats.get("nonindexed_published_html", []))
    args.summary_output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("status", "errors", "warnings")}))
    print("Search audit: published=", stats.get("published_html"),
          "eligible=", stats.get("eligible_html"),
          "records=", stats.get("indexed_documents"),
          "subject_counts=", stats.get("by_subject"))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

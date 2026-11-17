#!/usr/bin/env python3
"""Stage the exact owner preview files for CI and GitHub Pages."""
import json
import os
import shutil
import re
import posixpath
from pathlib import Path

out = Path("public")
out.mkdir(exist_ok=True)
web_roots = (
    "architecture", "chemistry", "css", "curriculum", "data",
    "docs", "examples", "js", "mathematics", "nsejs", "physics",
    "preview", "reference", "templates",
)
web_suffixes = {
    ".html", ".htm", ".css", ".js", ".mjs", ".json", ".svg",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".txt", ".webmanifest",
}
blocked = {
    ".git", ".github", "review", "tests", "tools", "src",
    "workspace", "schemas", "__pycache__", "node_modules",
    ".venv", "private", "secrets",
}

def stage(path):
    if path.is_symlink() or not path.is_file():
        return
    if any(part in blocked or part.startswith(".") for part in path.parts):
        return
    if path.suffix.lower() not in web_suffixes:
        return
    target = out / path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
    if target.suffix.lower() in {".html", ".htm"}:
        raw = target.read_text(encoding="utf-8")
        if re.search(r"</body\s*>", raw, flags=re.I):
            # A single common header, including existing mastheads and
            # legacy pages, without modifying the source HTML checkout.
            if "data-grade9-nav" not in raw:
                rel = posixpath.relpath("public/site-nav.js", target.parent.as_posix())
                tag = '<script defer src="' + rel + '" data-grade9-nav="common-r1"></script>'
                raw = re.sub(r"</body\s*>", lambda m: tag + "\n" + m.group(0),
                             raw, count=1, flags=re.I)
            target.write_text(raw, encoding="utf-8")

for name in ("index.html", "site.css", "site-nav.js"):
    source = Path(name)
    if source.is_file():
        stage(source)
for name in web_roots:
    folder = Path(name)
    if folder.is_dir():
        for item in folder.rglob("*"):
            stage(item)
if not (out / "index.html").is_file():
    raise SystemExit("PREVIEW_MISSING_ROOT_INDEX")
if not (out / "site-nav.js").is_file():
    raise SystemExit("PREVIEW_COMMON_HEADER_MISSING")
for p in ("data/learner-search-index.v1.json", "nsejs/data/learner-search-index.v1.json"):
    if not (out / p).is_file() or (out / p).stat().st_size < 100:
        raise SystemExit("PREVIEW_SEARCH_INDEX_MISSING:" + p)
for p in ("nsejs/chemistry/index.html", "nsejs/biology/index.html"):
    page = (out / p).read_text(encoding="utf-8")
    if 'data-grade9-nav="common-r1"' not in page:
        raise SystemExit("PREVIEW_COMMON_NAV_NOT_INSTALLED:" + p)
html_pages = 0
for page_file in out.rglob("*.html"):
    page = page_file.read_text(encoding="utf-8")
    if re.search(r"</body\s*>", page, flags=re.I):
        html_pages += 1
        if "data-grade9-nav" not in page:
            raise SystemExit("PREVIEW_COMMON_NAV_MISSING:" + str(page_file))
if html_pages == 0:
    raise SystemExit("PREVIEW_NO_HTML_PAGES")
print("All published HTML pages with a body have the common header loader:", html_pages)
(out / ".nojekyll").touch()
(out / "preview-release-status.json").write_text(
    json.dumps({
        "kind": "OWNER_DIRECTED_UNREVIEWED_TECHNICAL_PREVIEW",
        "academic_status": "HOLD",
        "r3_signed_production_release": False,
        "source_sha": os.environ["RELEASE_SHA"],
        "warning": "Source pages are technical candidates, not independently accepted academic material.",
    }, indent=2) + "\n", encoding="utf-8",
)
print("Staged static preview; review, tests, workspace and source code excluded.")

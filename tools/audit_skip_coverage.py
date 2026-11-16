#!/usr/bin/env python3
"""Audit Skip control integration across public subject learner routes.

Only learner pages, not private workspace/review archival pages.
Checks actual HTML entrypoints and their direct script dependencies; it never
mistakes a hidden DOM node for an available learner Skip control.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SUBJECTS = [
    ROOT / "nsejs",
    ROOT / "physics" / "wpe",
    ROOT / "curriculum" / "chemistry" / "preview",
]
DYNAMIC_ENTRYPOINTS = [
    "nsejs/physics/index.html",
    "nsejs/chemistry/index.html",
    "nsejs/biology/index.html",
    "nsejs/core1-recovery.html",
    "nsejs/chemistry/textbook/index.html",
    "nsejs/physics/learn-mechanics.html",
    "physics/wpe/learn-challenge.html",
]
TEXTAREA = re.compile(r"<textarea\b", re.I)
INPUT = re.compile(r"<input\b[^>]*\btype\s*=\s*['\"]?(?:text|number)\b[^>]*>", re.I | re.S)
SCRIPT = re.compile(r"<script\b[^>]*\bsrc\s*=\s*['\"]([^'\"]+)['\"]", re.I)
SKIP_FILE = ROOT / "nsejs" / "js" / "skip-mandatory-response.js"


def requires_skip(html: str) -> bool:
    if TEXTAREA.search(html):
        return True
    return any(
        re.search(r"\brequired\b", tag, flags=re.I)
        or re.search(r"(?:answer|attempt|predict|reason|diagnos|repair|transfer|boundary|response)", tag, re.I)
        for tag in INPUT.findall(html)
    )


def sources_with_skip(path: Path, text: str) -> bool:
    if "skip-mandatory-response.js" in text:
        # A real external script tag, not a statement in plain page prose.
        if any("skip-mandatory-response.js" in ref for ref in SCRIPT.findall(text)):
            return True
    for source in SCRIPT.findall(text):
        if source.startswith(("https:", "http:", "//")):
            continue
        script = (path.parent / urlsplit(source).path).resolve()
        if not script.is_relative_to(ROOT) or not script.is_file():
            continue
        code = script.read_text(encoding="utf-8")
        if "data-g9-skip-loader" in code or "skip-mandatory-response.js" in code:
            return True
    return False


def audit() -> dict:
    pages = sorted(
        {p for folder in SUBJECTS if folder.is_dir() for p in folder.rglob("*.html")}
    )
    form_pages = []
    covered = []
    uncovered = []
    for path in pages:
        source = path.read_text(encoding="utf-8", errors="replace")
        if not requires_skip(source):
            continue
        name = path.relative_to(ROOT).as_posix()
        form_pages.append(name)
        (covered if sources_with_skip(path, source) else uncovered).append(name)
    hubs = [
        path for path in DYNAMIC_ENTRYPOINTS
        if not sources_with_skip(ROOT / path, (ROOT / path).read_text(encoding="utf-8"))
    ]
    return {
        "scope": ["nsejs/**/*", "physics/wpe/**/*",
                  "curriculum/chemistry/preview/**/*"],
        "html_pages": len(pages),
        "response_pages": len(form_pages),
        "covered_response_pages": len(covered),
        "uncovered_response_pages": uncovered,
        "missing_dynamic_entrypoints": hubs,
        "audit_is_academic_acceptance": False,
    }


if __name__ == "__main__":
    report = audit()
    print(json.dumps(report, indent=2))
    if report["uncovered_response_pages"] or report["missing_dynamic_entrypoints"]:
        sys.exit(1)

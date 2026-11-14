#!/usr/bin/env python3
"""Architecture documentation: real HTTP Chromium tablet and legacy-route QA.

This validates documentation navigation, layout and redirects, not independent
science, learner mastery, academic admission or Golden Sample activation.
"""
from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review-artifacts/architecture-docs"
DOCUMENTS = [
    ("/architecture/review-guide.html", "Independent Audit Field Guide"),
    ("/architecture/core2-source-to-learning-pipeline.html",
     "Core2-Led Source-to-Learning Pipeline"),
]


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
         "--directory", str(ROOT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    receipt: dict = {
        "task": "G9V41_ARCHITECTURE_AUDITOR_R3_HTTP_CHROMIUM",
        "academic_status": "HOLD",
        "r2_policy": "PILOT_AWAITING_OWNER_GOLDEN",
        "kind": "HTTP_CHROMIUM_DOCUMENTATION_NAVIGATION_ONLY",
        "cases": [],
    }
    try:
        for _ in range(80):
            if server.poll() is not None:
                raise RuntimeError("Local HTTP server exited unexpectedly")
            try:
                urllib.request.urlopen(base + "/architecture/review-guide.html", timeout=1).close()
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise RuntimeError("Local HTTP server failed readiness check")

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for label, width, height in (
                    ("portrait", 1000, 1600),
                    ("landscape", 1600, 1000),
                ):
                    ctx = browser.new_context(
                        viewport={"width":width, "height":height},
                        has_touch=True, device_scale_factor=1,
                    )
                    page = ctx.new_page()
                    failures: list[str] = []
                    page.on("pageerror", lambda e: failures.append(str(e)))
                    for path, expected in DOCUMENTS:
                        page.goto(base + path, wait_until="load")
                        assert expected in page.title(), (path, page.title())
                        assert expected in page.locator("h1").first.inner_text()
                        assert page.locator("main").count() == 1
                        overflow = page.evaluate(
                            "() => Math.max(0, document.documentElement.scrollWidth - window.innerWidth)"
                        )
                        assert overflow <= 1, (path, "horizontal overflow", overflow)
                        if path.endswith("review-guide.html"):
                            for anchor in (
                                "scope","roles","intake","science","core1a","core1b",
                                "core2","qrt","runtime","coverage","findings",
                                "receipt","golden","references",
                            ):
                                assert page.locator("#"+anchor).count() == 1, anchor
                                assert page.locator(f'a[href="#{anchor}"]').count() >= 1, anchor
                            page.locator('aside.auditor-toc a[href="#core1b"]').focus()
                            page.keyboard.press("Enter")
                            assert page.evaluate("location.hash") == "#core1b"
                        else:
                            for n in range(1,9):
                                assert page.locator(f"#stage-{n}").count() == 1
                        dest = OUT / f"{path.rsplit('/',1)[-1][:-5]}-{label}-{width}x{height}.png"
                        page.screenshot(path=str(dest), full_page=True)
                        receipt["cases"].append({
                            "page":path,"orientation":label,
                            "viewport":f"{width}x{height}",
                            "horizontal_overflow_px":overflow,
                            "keyboard_anchor":"PASS" if path.endswith("review-guide.html") else "NOT_APPLICABLE",
                            "page_errors":list(failures),
                            "status":"PASS",
                            "screenshot":dest.name,
                        })
                    assert failures == [], failures
                    ctx.close()
                legacy = browser.new_context(viewport={"width":1000,"height":1600})
                lp = legacy.new_page()
                lp.goto(base + "/architecture/pipeline-flowchart.html?from=legacy#stage-5")
                lp.wait_for_url(
                    "**/architecture/core2-source-to-learning-pipeline.html?from=legacy#stage-5",
                    timeout=15000,
                )
                assert lp.locator("#stage-5").count() == 1
                assert "Core2-Led Source-to-Learning" in lp.title()
                legacy.close()
                receipt["cases"].append({
                    "page":"/architecture/pipeline-flowchart.html",
                    "case":"LEGACY_URL_WITH_QUERY_AND_STAGE_ANCHOR",
                    "status":"PASS",
                    "anchor":"#stage-5",
                })
            finally:
                browser.close()
    finally:
        server.terminate()
        try:server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=3)
    (OUT / "receipt.json").write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

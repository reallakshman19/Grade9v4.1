#!/usr/bin/env python3
"""Real HTTP Chromium QA for the PH09-PH12 author preview, not academic review.

Run from repository checkout:
  python tools/physics_ph09_ph12_wpe_parity_browser_qa.py
Requires playwright and installed Chromium. Produces a local JSON receipt.
No code path in this tool promotes source, QRT or B1-B7 status.
"""
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PATH = "/review/physics/ph09-ph12-wpe-parity-r1/preview.html"
OUT = ROOT / "review-artifacts" / "physics-ph09-ph12-parity-r1"
TOPICS = ["PH09-04", "PH10-09", "PH11-07", "PH12-09"]
VIEWPORTS = [(1280, 800), (1024, 768), (900, 1280), (800, 1280)]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *_args):
        pass


def assert_no_leak(page):
    assert page.locator("#post-attempt").is_hidden()
    assert page.locator("#reveal").is_disabled()
    assert page.locator("#reconstruct-list li").count() == 0
    assert page.locator("iframe").count() == 0
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}{PATH}"
    receipt = {
        "mode": "AUTHOR_EXPOSED_BROWSER_TECHNICAL_QA",
        "original_exam_admissions": 0,
        "science": "HOLD", "qrt": "NOT_RUN",
        "b1_b7": "HOLD", "release": "HOLD",
        "cases": [],
    }
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for width, height in VIEWPORTS:
                    context = browser.new_context(viewport={"width": width, "height": height}, has_touch=True)
                    page = context.new_page()
                    errors = []
                    page.on("pageerror", lambda exc: errors.append(str(exc)))
                    try:
                        page.goto(url, wait_until="domcontentloaded")
                        page.wait_for_function(
                            "() => document.querySelector('#load-status').textContent.includes('Four original cases loaded')",
                            timeout=30000,
                        )
                        for subtopic in TOPICS:
                            page.locator("#chapter-choice").select_option(subtopic)
                            assert_no_leak(page)
                            assert page.locator("#fresh-task").inner_text()
                            assert page.locator("#worked-solution li").count() >= 3
                            # Orientation help is stored but does not unlock the solution.
                            page.locator("#help-button").click()
                            assert page.locator("#orientation-help").is_visible()
                            assert_no_leak(page)
                            original = f"Original independent route for {subtopic} at {width}x{height}"
                            page.locator("#first-predict").fill("My prediction before feedback")
                            page.locator("#first-attempt").fill(original)
                            page.locator("#save-first").click()
                            assert page.locator("#reveal").is_enabled()
                            assert page.locator("#first-attempt").is_disabled()
                            page.reload(wait_until="domcontentloaded")
                            page.wait_for_function(
                                "() => document.querySelector('#load-status').textContent.includes('Four original cases loaded')",
                                timeout=30000,
                            )
                            page.locator("#chapter-choice").select_option(subtopic)
                            assert page.locator("#first-attempt").input_value() == original
                            assert page.locator("#first-attempt").is_disabled()
                            assert page.locator("#post-attempt").is_hidden()
                            page.locator("#reveal").click()
                            assert page.locator("#post-attempt").is_visible()
                            assert page.locator("#reconstruct-list li").count() >= 3
                            page.locator("#revision").fill("Repaired and independently reconsidered the boundary.")
                            page.locator("#save-revision").click()
                            assert "Revision saved" in page.locator("#revision-status").inner_text()
                            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
                            receipt["cases"].append({
                                "viewport": [width, height], "subtopic_id": subtopic,
                                "result": "PASS",
                                "checks": [
                                    "no feedback before commit", "help exposure", "first attempt persisted",
                                    "refresh", "separate revision", "no iframe", "no horizontal overflow"
                                ],
                            })
                        assert not errors, errors
                    finally:
                        context.close()
                # Denied storage must never permit first-attempt commit or revelation.
                context = browser.new_context()
                context.add_init_script(
                    "Object.defineProperty(window,'localStorage',{get(){throw Error('Storage denied')}})"
                )
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => document.querySelector('#load-status').textContent.includes('Four original cases loaded')",
                    timeout=30000,
                )
                assert page.locator("#save-first").is_disabled()
                assert_no_leak(page)
                assert "locked" in page.locator("#attempt-status").inner_text().lower()
                receipt["storage_denial"] = "PASS_FAIL_CLOSED"
                context.close()

                # Corrupted local record must also fail closed.
                context = browser.new_context()
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => document.querySelector('#load-status').textContent.includes('Four original cases loaded')",
                    timeout=30000,
                )
                page.evaluate(
                    "() => localStorage.setItem('g9-physics-ph09-ph12-author-preview-r1-20261115:PH09-04','{bad')"
                )
                page.reload(wait_until="domcontentloaded")
                page.wait_for_function(
                    "() => document.querySelector('#load-status').textContent.includes('Four original cases loaded')",
                    timeout=30000,
                )
                assert page.locator("#save-first").is_disabled()
                assert_no_leak(page)
                receipt["corrupt_storage"] = "PASS_FAIL_CLOSED"
                context.close()
            finally:
                browser.close()
        assert len(receipt["cases"]) == 4 * len(TOPICS)
        receipt["status"] = "PASS"
    except Exception as exc:
        receipt["status"] = "FAIL"
        receipt["error"] = repr(exc)
        raise
    finally:
        (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        server.shutdown()
        thread.join(timeout=5)


if __name__ == "__main__":
    run()

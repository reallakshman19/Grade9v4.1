#!/usr/bin/env python3
"""HTTP Chromium adversarial checks for PH09–PH12 SOURCE→Core1A→Core1B→SOURCE R2.

Technical candidate preview only. Browser localStorage isn't authenticated examination
custody. The tests never establish source, QRT, science, B1–B7, or Owner admission.
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


def loaded(page):
    page.wait_for_function(
        "() => document.querySelector('#load-status').textContent.includes('Four source')",
        timeout=30000,
    )


def assert_no_leak(page, source_phase=False):
    assert page.locator("#post-attempt").is_hidden()
    assert page.locator("#reveal").is_disabled()
    assert page.locator("#reconstruct-list li").count() == 0
    assert page.locator("#diagnose").text_content() == ""
    assert page.locator("#repair").text_content() == ""
    assert page.locator("#boundary").text_content() == ""
    assert page.locator("iframe").count() == 0
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
    if source_phase:
        assert page.locator("#journey").is_hidden()
        assert page.locator("#source-learn").is_disabled()
        # Hiding an already-populated worked answer in DOM is not sufficient:
        # the source-first gate must not mount teaching or transfer content.
        assert page.locator("#worked-solution li").count() == 0
        assert page.locator("#teaching-model").text_content() == ""
        assert page.locator("#fresh-task").text_content() == ""


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}{PATH}"
    receipt = {
        "mode": "AUTHOR_EXPOSED_BROWSER_TECHNICAL_QA_R2",
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
                    context = browser.new_context(
                        viewport={"width": width, "height": height}, has_touch=True
                    )
                    page = context.new_page()
                    errors = []
                    page.on("pageerror", lambda exc: errors.append(str(exc)))
                    try:
                        page.goto(url, wait_until="domcontentloaded")
                        loaded(page)
                        for subtopic in TOPICS:
                            page.locator("#chapter-choice").select_option(subtopic)
                            assert_no_leak(page, source_phase=True)
                            assert page.locator("#source-question").inner_text()
                            adapter_revision = "r3" if subtopic == "PH11-07" else "r2"
                            assert page.locator("#source-adapter-link").get_attribute("href").endswith(
                                f"topic-adapter.{subtopic[:4]}.wpe-parity-{adapter_revision}.v1.json"
                            )
                            assert page.locator("#reviewer-adapter-evidence").is_hidden()
                            assert page.locator("#connected-bridge").is_hidden()
                            assert page.locator("#bridge-steps li").count() == 0
                            # The protected move stays out of the visible prompt.
                            assert "new learner-owned decision" not in page.locator(
                                "#protected-work"
                            ).inner_text().lower()
                            source_answer = (
                                f"Initial source reasoning for {subtopic} at {width}x{height}"
                            )
                            page.locator("#source-attempt").fill(source_answer)
                            page.locator("#source-save").click()
                            assert page.locator("#source-learn").is_enabled()
                            page.locator("#source-learn").click()
                            assert page.locator("#journey").is_visible()
                            assert page.locator("#fresh-task").inner_text()
                            assert page.locator("#worked-solution li").count() >= 3
                            if subtopic == "PH11-07":
                                assert page.locator("#connected-bridge").is_visible()
                                assert page.locator("#bridge-steps li").count() == 4
                                assert "10 V" in page.locator("#bridge-question").inner_text()
                                assert "18 V" in page.locator("#fresh-task").inner_text()
                            else:
                                assert page.locator("#connected-bridge").is_hidden()

                            # Nondecisive help must not unlock reconstruction.
                            page.locator("#help-button").click()
                            assert page.locator("#orientation-help").is_visible()
                            assert_no_leak(page)
                            original = f"Independent transfer for {subtopic} at {width}x{height}"
                            page.locator("#first-predict").fill("My prediction before feedback")
                            page.locator("#first-attempt").fill(original)
                            page.locator("#save-first").click()
                            assert page.locator("#reveal").is_enabled()
                            assert page.locator("#first-attempt").is_disabled()

                            # On refresh, the SOURCE and TRANSFER originals must survive,
                            # but reconstruction remains hidden until deliberately revealed.
                            page.reload(wait_until="domcontentloaded")
                            loaded(page)
                            page.locator("#chapter-choice").select_option(subtopic)
                            assert page.locator("#source-attempt").input_value() == source_answer
                            page.locator("#source-attempt").is_disabled()
                            page.locator("#source-learn").click()
                            assert page.locator("#first-attempt").input_value() == original
                            assert page.locator("#first-attempt").is_disabled()
                            assert page.locator("#post-attempt").is_hidden()
                            page.locator("#reveal").click()
                            assert page.locator("#reconstruct-list li").count() >= 3
                            assert page.locator("#diagnose-stage").is_hidden()
                            assert page.locator("#repair-stage").is_hidden()
                            assert page.locator("#boundary-stage").is_hidden()
                            assert page.locator("#diagnose").text_content() == ""
                            assert page.locator("#repair").text_content() == ""
                            assert page.locator("#boundary").text_content() == ""

                            page.locator("#reconstruct-response").fill(
                                "I compare my first attempt to the displayed model and check assumptions."
                            )
                            page.locator("#save-reconstruct").click()
                            assert page.locator("#diagnose-stage").is_visible()
                            assert page.locator("#repair-stage").is_hidden()
                            page.locator("#diagnosis-response").fill(
                                "The original attempt states my actual evidence; I do not infer a misconception without it."
                            )
                            page.locator("#save-diagnosis").click()
                            assert page.locator("#repair-stage").is_visible()
                            assert page.locator("#boundary-stage").is_hidden()
                            page.locator("#revision").fill(
                                "Repaired reasoning, with a separate physical consistency check."
                            )
                            page.locator("#save-revision").click()
                            assert "Revision saved" in page.locator("#revision-status").inner_text()
                            assert page.locator("#boundary-stage").is_visible()
                            assert page.locator("#source-return-stage").is_hidden()
                            page.locator("#boundary-response").fill(
                                "An independent boundary falsifier using a changed assumption."
                            )
                            page.locator("#save-boundary").click()
                            assert page.locator("#source-return-stage").is_visible()
                            page.locator("#source-return-response").fill(
                                "I revisit the original author checkpoint with revised reasoning."
                            )
                            page.locator("#save-source-return").click()
                            assert "Source return saved" in page.locator(
                                "#source-return-status"
                            ).inner_text()
                            assert page.locator("#reviewer-adapter-evidence").is_visible()
                            assert page.locator("#source-attempt").input_value() == source_answer
                            assert page.locator("#first-attempt").input_value() == original
                            assert page.evaluate(
                                "document.documentElement.scrollWidth <= innerWidth + 1"
                            )
                            receipt["cases"].append({
                                "viewport": [width, height],
                                "subtopic_id": subtopic,
                                "result": "PASS",
                                "checks": [
                                    "original author source first", "source→teach gate",
                                    "no decisive preattempt hint", "first transfer preserved on reload",
                                    "reconstruction only after first commit",
                                    "separate diagnosis and repair commits",
                                    "boundary attempt before source return",
                                    "original and revised source answers separate",
                                    "no iframe", "no horizontal overflow",
                                ],
                            })
                        assert not errors, errors
                    finally:
                        context.close()

                # No browser storage -> no source first, no teaching/feedback.
                context = browser.new_context()
                context.add_init_script(
                    "Object.defineProperty(window,'localStorage',{get(){throw Error('Storage denied')}})"
                )
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded")
                loaded(page)
                assert page.locator("#source-save").is_disabled()
                assert_no_leak(page, source_phase=True)
                assert "locked" in page.locator("#source-status").inner_text().lower()
                receipt["storage_denial"] = "PASS_FAIL_CLOSED"
                context.close()

                # Corrupt the content-hash-keyed SOURCE attempt record.
                context = browser.new_context()
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded")
                loaded(page)
                page.locator("#source-attempt").fill(
                    "Initial candidate source explanation to record a content-bound key."
                )
                page.locator("#source-save").click()
                page.evaluate(
                    """() => {
                      const key=Object.keys(localStorage).find(
                        k=>k.startsWith('g9-physics-ph09-ph12-author-preview-r1-20261115:PH09-04:')
                      );
                      if (!key) throw Error('Missing content-bound source key');
                      localStorage.setItem(key,'{bad');
                    }"""
                )
                page.reload(wait_until="domcontentloaded")
                loaded(page)
                assert page.locator("#source-save").is_disabled()
                assert_no_leak(page, source_phase=True)
                receipt["corrupt_storage"] = "PASS_FAIL_CLOSED"
                context.close()

                # Inject a write denial between source commitment and new transfer.
                context = browser.new_context()
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded")
                loaded(page)
                page.locator("#source-attempt").fill(
                    "Source answer before injected storage write failure."
                )
                page.locator("#source-save").click()
                page.locator("#source-learn").click()
                page.locator("#first-predict").fill("Prediction")
                page.locator("#first-attempt").fill("Independent answer")
                page.evaluate(
                    "() => { Storage.prototype.setItem = function(){throw Error('Injected denial')}; }"
                )
                page.locator("#save-first").click()
                assert page.locator("#reveal").is_disabled()
                assert page.locator("#post-attempt").is_hidden()
                receipt["mid_attempt_write_denial"] = "PASS_FAIL_CLOSED"
                context.close()

                # Exercise ?case= deep-link without unlocking the source-first gate.
                context = browser.new_context()
                page = context.new_page()
                page.goto(url + "?case=PH12-09", wait_until="domcontentloaded")
                loaded(page)
                assert page.locator("#chapter-choice").input_value() == "PH12-09"
                assert_no_leak(page, source_phase=True)
                receipt["deep_link"] = "PASS_SOURCE_FIRST"
                context.close()
            finally:
                browser.close()

        assert len(receipt["cases"]) == len(VIEWPORTS) * len(TOPICS)
        receipt["status"] = "PASS"
    except Exception as exc:
        receipt["status"] = "FAIL"
        receipt["error"] = repr(exc)
        raise
    finally:
        (OUT / "receipt.json").write_text(
            json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
        )
        server.shutdown()
        thread.join(timeout=5)


if __name__ == "__main__":
    run()

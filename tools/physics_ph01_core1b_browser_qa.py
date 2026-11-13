#!/usr/bin/env python3
"""PH01 Core1B candidate runtime — HTTP Chromium evidence, never academic admission.

Tests full first-response persistence, sequential H1–H3, help/repair separation,
boundary answer gating, content-revision binding and blocked-storage behavior.
No claim that tasks meet native B1–B7 or independent D3 review.
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
OUT = ROOT / "review-artifacts/physics-core1b"
URL_PATH = "/nsejs/physics/core1/ph01-qrt-r2/index.html"
PREFIX = "G9V41:PH01:R2:"


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def storage_snapshot(page):
    return page.evaluate("""() => {
      const keys = Object.keys(localStorage).filter(k => k.startsWith('G9V41:PH01:R2:') && !k.endsWith(':probe'));
      const usable = keys.filter(k => k.split(':').length >= 5 && localStorage.getItem(k).includes('"first_answer"'));
      const k = usable[0];
      return {keys: usable, record: k ? JSON.parse(localStorage.getItem(k)) : null};
    }""")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    port = free_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
         "--directory", str(ROOT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    url = f"http://127.0.0.1:{port}{URL_PATH}"
    receipt = {"task": "PH01_CORE1B_HTTP_CHROMIUM_R2", "candidate": True,
               "academic_status": "HOLD", "tests": []}
    try:
        for _ in range(50):
            if server.poll() is not None:
                raise RuntimeError("HTTP server exited")
            try:
                urllib.request.urlopen(url, timeout=1).close()
                break
            except Exception:
                time.sleep(.1)
        else:
            raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for orientation, width, height in (
                    ("portrait", 1000, 1600),
                    ("landscape", 1600, 1000)
                ):
                    ctx = browser.new_context(viewport={"width":width,"height":height},
                                              has_touch=True,device_scale_factor=1)
                    page = ctx.new_page()
                    errors = []
                    page.on("pageerror", lambda err: errors.append(str(err)))
                    page.on("console", lambda msg: errors.append(msg.text)
                            if msg.type == "error" else None)
                    page.goto(url, wait_until="load")
                    page.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Candidate task loaded')")
                    assert page.locator("#cycleSelect option").count() == 12
                    assert page.locator("#postAttempt").is_hidden()
                    assert page.locator("#showReconstruct").is_hidden()
                    assert page.locator("#attemptInput").is_enabled()
                    assert not page.locator("#metaRevision").inner_text().endswith("Revision")
                    page.locator("#predictInput").fill("I will check the post-change motion model.")
                    page.locator("#attemptInput").fill("Model choice before algebra. My preliminary prediction is no meeting.")
                    page.locator("#saveFirst").click()
                    assert page.locator("#postAttempt").is_visible()
                    assert page.locator("#saveFirst").is_disabled()
                    assert "My preliminary prediction is no meeting" in page.locator("#savedFirst").inner_text()
                    first = storage_snapshot(page)["record"]
                    assert first["first_answer"]["answer"].endswith("no meeting.")
                    assert first["help_exposure"] == []
                    assert first["revisions"] == []
                    # H2 cannot be opened before H1; subsequent help is recorded.
                    assert page.get_by_role("button", name="Open H2").is_disabled()
                    page.get_by_role("button", name="Open H1").click()
                    assert page.get_by_role("button", name="Open H2").is_enabled()
                    page.get_by_role("button", name="Open H2").click()
                    page.get_by_role("button", name="Open H3").click()
                    page.locator("#showReconstruct").click()
                    assert page.locator("#reconstructAnswer").is_visible()
                    page.locator("#diagnoseInput").fill("I had assumed the overall average speed was the post-change velocity.")
                    page.locator("#saveDiagnose").click()
                    page.locator("#repairInput").fill("Use the piecewise position law, check the interval and closing direction.")
                    page.locator("#saveRepair").click()
                    page.locator("#boundaryInput").fill("If the direction reverses again, a meeting becomes possible.")
                    page.locator("#saveBoundary").click()
                    assert page.locator("#showBoundary").is_enabled()
                    page.locator("#showBoundary").click()
                    assert "t=8 s" in page.locator("#boundaryAnswer").inner_text()
                    revised = storage_snapshot(page)["record"]
                    assert revised["first_answer"] == first["first_answer"]
                    assert {x["kind"] for x in revised["help_exposure"]} == {
                        "H1","H2","H3","RECONSTRUCT","BOUNDARY_MODEL"
                    }
                    assert len(revised["diagnosis_notes"]) == 1
                    assert revised["diagnosis_notes"][0]["kind"] == "LEARNER_SELF_REPORT_NOT_DIAGNOSIS"
                    assert len(revised["revisions"]) == 1
                    assert revised["revisions"][0]["helped"] is True
                    assert len(revised["boundary_attempts"]) == 1
                    assert revised["mastery_status"] == "UNASSESSED"
                    # Refresh must restore the same SHA-bound first answer and exposure.
                    page.reload(wait_until="load")
                    page.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Candidate task loaded')")
                    assert page.locator("#saveFirst").is_disabled()
                    assert page.locator("#reconstructAnswer").is_visible()
                    assert page.locator("#boundaryAnswer").is_visible()
                    same = storage_snapshot(page)["record"]
                    assert same["first_answer"] == first["first_answer"]
                    overflow = page.evaluate(
                        "() => document.documentElement.scrollWidth - window.innerWidth")
                    assert overflow <= 1, f"horizontal overflow {overflow}"
                    page.screenshot(path=str(OUT / f"PH01-core1b-{orientation}-{width}x{height}.png"),
                                    full_page=True)
                    assert errors == [], errors
                    ctx.close()
                    receipt["tests"].append({
                        "orientation": orientation, "viewport": f"{width}x{height}",
                        "cycles":12, "first_attempt_immutable":"PASS",
                        "sequential_hints":"PASS", "help_exposure":"PASS",
                        "revision_separate":"PASS", "boundary_gating":"PASS",
                        "refresh":"PASS","overflow_px":max(0,overflow),
                        "page_errors":errors,"status":"PASS"
                    })
                blocked = browser.new_context(viewport={"width":1000,"height":1600})
                blocked.add_init_script("""Object.defineProperty(window, 'localStorage', {
                    configurable: true,
                    get() { throw new DOMException('Blocked for regression', 'SecurityError'); }
                });""")
                bp = blocked.new_page()
                bp.goto(url, wait_until="load")
                bp.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Storage unavailable')")
                assert bp.locator("#attemptInput").is_enabled(), "Learner should still be able to copy work"
                assert bp.locator("#saveFirst").is_disabled()
                assert bp.locator("#postAttempt").is_hidden()
                assert "Storage unavailable" in bp.locator("#runtimeStatus").inner_text()
                blocked.close()
                receipt["tests"].append({
                    "case":"disabled_storage", "first_answer_fake_success":False,
                    "answers_remain_locked":True,"copy_input_enabled":True,
                    "status":"PASS"
                })
            finally:
                browser.close()
    finally:
        server.terminate()
        try: server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill();server.wait(timeout=3)
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n",
                                      encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

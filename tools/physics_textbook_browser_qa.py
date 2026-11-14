#!/usr/bin/env python3
"""HTTP Chromium checks for PH01's candidate reading-first textbook.

Checks rendered page ergonomics and teaching-demo interactions only; not QRT,
science approval, native Core1B protected-attempt runtime, or learner mastery.
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
OUT = ROOT / "review-artifacts/physics-textbook"
PATH = "/nsejs/physics/textbook/PH01/index.html"


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    port = _free_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port),
         "--bind", "127.0.0.1", "--directory", str(ROOT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    url = f"http://127.0.0.1:{port}{PATH}"
    receipt = {"task": "PH01_CHROMIUM_TABLET_CANDIDATE",
               "academic_status": "HOLD", "tests": []}
    try:
        for attempt in range(40):
            if server.poll() is not None:
                raise RuntimeError("HTTP server exited before browser test")
            try:
                urllib.request.urlopen(url, timeout=1).close()
                break
            except Exception:
                time.sleep(.1)
        else:
            raise RuntimeError("HTTP server failed to accept connections")

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for orientation, width, height in [
                    ("portrait", 1000, 1600),
                    ("landscape", 1600, 1000)
                ]:
                    context = browser.new_context(
                        viewport={"width": width, "height": height},
                        device_scale_factor=1, has_touch=True
                    )
                    page = context.new_page()
                    issues: list[str] = []
                    page.on("pageerror", lambda err: issues.append(str(err)))
                    page.on("console", lambda msg: issues.append(msg.text) if msg.type == "error" else None)
                    page.goto(url, wait_until="load")
                    assert "Motion and Kinematics" in page.locator("h1").inner_text()
                    assert page.locator("svg[role='img']").count() >= 2
                    assert page.locator("details").count() >= 5
                    overflow = page.evaluate(
                        "() => ({scroll: document.documentElement.scrollWidth, "
                        "viewport: window.innerWidth})"
                    )
                    assert overflow["scroll"] <= overflow["viewport"] + 1, overflow

                    slider = page.locator("#observer")
                    slider.focus()
                    assert page.locator("#a-output").inner_text().strip() == "+1 m/s"
                    assert page.locator("#rel-output").inner_text().strip() == "+2 m/s"
                    page.keyboard.press("ArrowRight")
                    assert page.locator("#a-output").inner_text().strip() == "+2 m/s"
                    assert page.locator("#rel-output").inner_text().strip() == "+1 m/s"

                    first = page.locator("details").first
                    assert not first.evaluate("(node) => node.open")
                    first.locator("summary").focus()
                    page.keyboard.press("Enter")
                    assert first.evaluate("(node) => node.open")

                    page.screenshot(path=str(OUT / f"PH01-{orientation}-{width}x{height}.png"))
                    assert not issues, issues
                    receipt["tests"].append({
                        "orientation": orientation, "viewport": f"{width}x{height}",
                        "chapter_rendered": True, "graph_figures": 2,
                        "interactive_slider_keyboard": "PASS",
                        "details_keyboard": "PASS",
                        "overflow_px": max(0, overflow["scroll"] - overflow["viewport"]),
                        "page_errors": issues, "status": "PASS"
                    })
                    context.close()
            finally:
                browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=3)

    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

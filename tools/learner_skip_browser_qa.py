#!/usr/bin/env python3
"""Real HTTP Chromium smoke/regression for optional learner response Skip.

Technical UI behavior only: does not certify Physics/Chemistry/Biology science.
"""
from __future__ import annotations

import json
import os
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    "biology": [
        "/nsejs/biology/index.html",
        "/nsejs/biology/core1/bio-genetics-coordination-r1/index.html",
        "/nsejs/biology/core1/bio-immunology-defense-d3-r1/index.html",
        "/nsejs/biology/core1/bio-viral-genetics-d3-r1/index.html",
    ],
    "chemistry": [
        "/nsejs/chemistry/index.html",
        "/nsejs/chemistry/core1/chem-electronic-structure-d3-r1/index.html",
        "/nsejs/chemistry/core1/chem-phosphorus-oxyacids-d3-r1/index.html",
        "/nsejs/chemistry/textbook/index.html?unit=C08&mode=practice",
        "/curriculum/chemistry/preview/C01.html?mode=practice",
    ],
    "physics": [
        "/nsejs/physics/index.html",
        "/nsejs/physics/core1/ph01-m01-r47/index.html",
        "/nsejs/physics/core1/nsejs-optics-displacement-d3-r1/index.html",
        "/nsejs/physics/curriculum/topics/PH07/b01/PH07-01/core1b.html",
        "/physics/wpe/learn-challenge.html",
    ],
}


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        return


def inspect(page, base: str, route: str, subject: str):
    page.goto(base + route, wait_until="domcontentloaded", timeout=25000)
    page.wait_for_function("window.Grade9Skip?.version === 'r1'", timeout=12000)
    info = page.evaluate("""() => {
      const fields = [...document.querySelectorAll('main textarea,main input[type="text"],main input[type="number"]')];
      return {fields:fields.length, skipControls:document.querySelectorAll('.g9-skip-control').length,
        visible: [...document.querySelectorAll('.g9-skip-button')].filter(x=>x.getClientRects().length).length};
    }""")
    # All actual eligible response fields are instrumented, excluding deliberate
    # header/search/read-only fields. A hidden future stage is still represented.
    if info["fields"] and not info["skipControls"]:
        raise AssertionError(f"Mandatory fields without Skip: {route} / {info}")
    visible = page.locator(".g9-skip-button:visible")
    if visible.count():
        skip = visible.first
        box = skip.locator("xpath=..")
        field = box.locator("xpath=preceding-sibling::*[1]")
        before = field.input_value()
        skip.click()
        assert box.get_attribute("data-skipped") == "true", route
        assert field.input_value() == before, f"Skip forged an answer: {route}"
        link = box.locator("a.g9-skip-continue")
        assert link.count() == 1 and link.get_attribute("href"), route
        assert "No answer submitted or scored" in box.locator(".g9-skip-status").inner_text() or (
            "not submitted or scored" in box.locator(".g9-skip-status").inner_text()
        ), route
        assert "SKIPPED" not in field.input_value(), route
        assert skip.evaluate("(b)=>getComputedStyle(b).minHeight") != "0px", route
        field.fill("Student is now trying the problem independently.")
        assert box.get_attribute("data-skipped") == "false", route
        if subject in ("biology", "chemistry") and "/core1/" in route:
            model = page.locator('[data-role="model-host"]')
            if model.count():
                assert model.first.is_hidden(), "Skip leaked a model before answer commit"
    return dict(subject=subject, route=route, **info)


def main():
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(Quiet, directory=str(ROOT))
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    results = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for width, height in ((1000, 1600), (1600, 1000)):
                ctx = browser.new_context(viewport={"width": width, "height": height},
                                          device_scale_factor=1, is_mobile=False)
                for subject, routes in ROUTES.items():
                    for route in routes:
                        page = ctx.new_page()
                        try:
                            results.append(dict(orientation=f"{width}x{height}",
                                                **inspect(page, base, route, subject)))
                        finally:
                            page.close()
                ctx.close()
            browser.close()
    finally:
        server.shutdown()
    assert len(results) == 28, results
    print("SKIP_REAL_CHROMIUM_PASS: 28 subject-route/orientation visits")
    print(json.dumps({"checked":len(results),"routes":results}, indent=2))


if __name__ == "__main__":
    main()

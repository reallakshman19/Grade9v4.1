"""HTTP Chromium smoke tests for Chemistry candidate Core1A/Core1B textbook.

Runs only against committed candidate files, at 12.7-inch-style landscape
and portrait CSS viewports. Does not assert academic qualification.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
PORT = 8788
BASE = f"http://127.0.0.1:{PORT}/curriculum/chemistry/preview"
OUT = ROOT / "chemistry-tablet-artifacts"
OUT.mkdir(exist_ok=True)
UNITS = {"C01": 6, "C02": 7, "C03": 6, "C04": 6, "C05": 6, "C06": 6, "C07": 7}
VIEWPORTS = {"portrait": (1000, 1600), "landscape": (1600, 1000)}


def check(condition, label):
    if not condition:
        raise AssertionError(label)


def check_chapter(page, unit, n, scene):
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    response = page.goto(f"{BASE}/{unit}.html", wait_until="domcontentloaded", timeout=30000)
    check(response is not None and response.status == 200, f"{unit} HTTP status")
    page.locator("article.lesson").first.wait_for(timeout=20000)
    check(page.locator("article.lesson").count() == n, f"{unit} section count")
    check(page.locator("section.demand").count() == 3 * n, f"{unit} three operations/subtopic")
    check(page.locator("section.demand .attempt").count() == 3 * n, f"{unit} Core1B cycles")
    check(page.locator(".note").inner_text().lower().find("academic") >= 0,
          f"{unit} academic HOLD notice")
    check(not errors, f"{unit} JS exceptions: {errors}")
    dims = page.evaluate("() => ({width:document.documentElement.scrollWidth, viewport:window.innerWidth})")
    check(dims["width"] <= dims["viewport"] + 3, f"{unit} overflow {dims}")
    minheight = page.locator(".attempt button").first.evaluate(
        "e => parseFloat(getComputedStyle(e).minHeight)")
    check(minheight >= 54, f"{unit} touch button height {minheight}")
    if unit == "C07":
        images = page.locator("figure.chem-figure img")
        check(images.count() == 4, "Four C07 diagrams")
        images.first.scroll_into_view_if_needed()
        page.wait_for_function("() => [...document.images].every(x => x.complete)", timeout=12000)
        check(all(images.nth(i).evaluate("(e) => e.naturalWidth > 0") for i in range(4)),
              "All four C07 figures load")
        page.screenshot(path=str(OUT / f"C07-{scene}.png"), full_page=False)


def check_first_attempt_protection(page):
    page.goto(f"{BASE}/C07.html", wait_until="domcontentloaded")
    post = page.locator(".attempt .post").first
    field = page.locator(".attempt textarea").first
    button = page.locator(".attempt button").first
    check(post.is_hidden(), "Model answer hidden before attempt")
    button.click()
    check(post.is_hidden(), "Empty answer does not reveal solution")
    field.fill("My initial reasoning: compare electron transfer and total charge.")
    button.click()
    check(post.is_visible(), "Model answer revealed after first commit")
    check(field.is_disabled(), "First attempt locked after commit")
    saved = field.input_value()
    page.reload(wait_until="domcontentloaded")
    page.locator(".attempt textarea").first.wait_for(timeout=20000)
    check(page.locator(".attempt textarea").first.input_value() == saved, "Exact revision first attempt persists")
    check(page.locator(".attempt textarea").first.is_disabled(), "First attempt remains protected on refresh")
    check(page.locator(".attempt .post").first.is_visible(), "Post-attempt feedback persists")
    check(page.locator(".attempt .post").first.inner_text().find("Model response") >= 0,
          "Full reconstruction closure accessible")


def check_storage_disabled(browser):
    ctx = browser.new_context(viewport={"width": 1000, "height": 1600})
    ctx.add_init_script("""Object.defineProperty(window, 'localStorage', {
        configurable: true, get() { throw Error('localStorage disabled'); }
    });""")
    page = ctx.new_page()
    page.goto(f"{BASE}/C07.html", wait_until="domcontentloaded")
    page.locator(".attempt textarea").first.wait_for(timeout=20000)
    page.locator(".attempt textarea").first.fill("A model choice before feedback")
    page.locator(".attempt button").first.click()
    check(page.locator(".attempt .post").first.is_visible(), "Disabled storage fallback preserves the live session")
    status = page.locator(".attempt .mini").first.inner_text().lower()
    check("storage unavailable" in status, f"Storage limitation must be explicit: {status}")
    ctx.close()


def main():
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    try:
        for _ in range(70):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}", timeout=1).read(1)
                break
            except Exception:
                time.sleep(0.25)
        else:
            raise RuntimeError("HTTP server did not start")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            try:
                for name, (width, height) in VIEWPORTS.items():
                    ctx = browser.new_context(viewport={"width": width, "height": height},
                                              is_mobile=False, has_touch=True)
                    page = ctx.new_page()
                    for unit, n in UNITS.items():
                        check_chapter(page, unit, n, name)
                    if name == "landscape":
                        check_first_attempt_protection(page)
                    ctx.close()
                check_storage_disabled(browser)
            finally:
                browser.close()
        print("PASS: 14 HTTP tablet views (7 units x 2 orientations), 44 subtopics, "
              "132 three-demand Core1B cycles, C07 diagrams, protected first attempt, "
              "refresh readback, disabled-storage disclosure and no overflow. "
              "No academic approval inferred from software validation.")
    finally:
        server.terminate()
        server.wait(timeout=8)


if __name__ == "__main__":
    main()

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
    check(page.locator(".chapter-spine").count() == 1, f"{unit} connected chapter spine")
    check(page.locator(".big-idea").count() == n, f"{unit} original big idea per subtopic")
    check(page.locator(".reasoning-path").count() == n, f"{unit} causal chains")
    check(page.locator(".investigation").count() == n, f"{unit} investigations")
    check(page.locator(".chapter-closure").count() == 1, f"{unit} chapter synthesis")
    details = page.locator(".investigation .investigation-answer").first
    check(not details.evaluate("(e) => e.open"), f"{unit} inquiry analysis initially hidden")
    details.locator("summary").click()
    check(details.evaluate("(e) => e.open"), f"{unit} inquiry can be explored by learner")
    check(page.locator("section.demand .attempt").count() == 3 * n, f"{unit} Core1B cycles")
    check(page.locator(".note").inner_text().lower().find("academic") >= 0,
          f"{unit} academic HOLD notice")
    check(not errors, f"{unit} JS exceptions: {errors}")
    dims = page.evaluate("() => ({width:document.documentElement.scrollWidth, viewport:window.innerWidth})")
    check(dims["width"] <= dims["viewport"] + 3, f"{unit} overflow {dims}")
    minheight = page.locator(".attempt button").first.evaluate(
        "e => parseFloat(getComputedStyle(e).minHeight)")
    check(minheight >= 54, f"{unit} touch button height {minheight}")
    images = page.locator("figure.chem-figure img")
    expected_figures = 4 if unit == "C07" else 2
    check(images.count() == expected_figures, f"{unit}: expected {expected_figures} explanatory diagrams")
    # R2 presents one subtopic at a time. Navigate to each figure's owner instead
    # of trying to scroll into a hidden lesson; still verify ALL original figures.
    for i in range(expected_figures):
        owner_id = images.nth(i).locator("xpath=ancestor::article[contains(@class,'lesson')]").get_attribute("id")
        check(bool(owner_id), f"{unit} image {i} has no owning subtopic")
        page.locator(f'.toc a[href="#{owner_id}"]').click()
        check(page.locator(f"#{owner_id}").is_visible(), f"{unit} selected image subtopic invisible")
        check(page.locator("article.lesson:visible").count() == 1, f"{unit} duplicate subtopic pages")
        images.nth(i).scroll_into_view_if_needed()
        page.wait_for_function("""i => { const e = document.querySelectorAll("figure.chem-figure img")[i]; return !!e && e.complete && e.naturalWidth > 0; }""", arg=i, timeout=12000)
    check(all(images.nth(i).evaluate("(e) => e.naturalWidth > 0") for i in range(expected_figures)),
          f"{unit} all figures load")
    if unit == "C07":
        page.screenshot(path=str(OUT / f"C07-{scene}.png"), full_page=False)


def check_first_attempt_protection(page):
    page.goto(f"{BASE}/C07.html", wait_until="domcontentloaded")
    post = page.locator(".attempt .post").first
    prediction = page.locator(".attempt .prediction-stage").first
    pred_input = prediction.locator("textarea.prediction-input")
    first = page.locator(".attempt .first-attempt").first
    field = first.locator("textarea")
    check(post.is_hidden(), "Model answer hidden before prediction")
    check(first.is_hidden(), "First attempt blocked until prediction")
    prediction.locator("button.predict-submit").click()
    check(first.is_hidden(), "Blank prediction cannot open attempt")
    pred_input.fill("First predict the likely ion-charge relation, state the assumptions.")
    prediction.locator("button.predict-submit").click()
    check(prediction.is_hidden(), "Prediction locked after durable commit")
    check(first.is_visible(), "First attempt opens only after prediction")
    check(page.locator(".attempt .hint-ladder").first.is_visible(), "Hints available in attempt stage")
    check(not page.locator(".attempt .hint-contents").first.inner_text().strip(),
          "No hints revealed without recording exposure")
    page.locator(".attempt button.hint-submit").first.click()
    check("H1:" in page.locator(".attempt .hint-contents").first.inner_text(), "First hint recorded before reveal")
    check(post.is_hidden(), "Hint must not show model")
    first.locator("button").click()
    check(post.is_hidden(), "Blank first attempt does not reveal solution")
    field.fill("My independent first reasoning: compare electron transfer and total charge.")
    first.locator("button").click()
    check(post.is_visible(), "Reconstruction stage displayed after first commit")
    check("Model response" not in post.inner_text(), "Model answer leaked after first attempt")
    check(field.is_disabled(), "First attempt locked after commit")
    saved = field.input_value()
    first_stage = post.locator("textarea.stage-input")
    check(first_stage.count() == 1, "One independent post-attempt stage active")
    check("Reconstruct" in post.locator(".core1b-stage h4").last.inner_text(), "Reconstruct first")
    first_stage.fill("I reconstruct the particle and charge ledger under the stated assumptions.")
    post.locator("button.stage-submit").click()
    check("Diagnose" in post.locator(".core1b-stage h4").last.inner_text(), "Diagnose follows reconstruct")
    page.reload(wait_until="domcontentloaded")
    field = page.locator(".attempt .first-attempt textarea").first
    field.wait_for(timeout=20000)
    post = page.locator(".attempt .post").first
    check(field.input_value() == saved and field.is_disabled(), "First attempt unchanged after refresh")
    check(page.locator(".attempt .prediction-stage").first.is_hidden(), "Prediction commit survives refresh")
    check("H1:" in page.locator(".attempt .hint-contents").first.inner_text(), "Hint exposure survives refresh")
    for title in ("Diagnose", "Repair", "Boundary test"):
        check(title in post.locator(".core1b-stage h4").last.inner_text(), f"Expected {title}")
        check("Model response" not in post.inner_text(), f"Model leaked before {title}")
        post.locator("textarea.stage-input").fill(
            "My independent reasoning at the "+title+" stage: test the model and its conditions.")
        post.locator("button.stage-submit").click()
    check("Model response" in post.inner_text(), "Model appears after saved boundary test only")
    page.reload(wait_until="domcontentloaded")
    page.locator(".attempt .post .model-closure").first.wait_for(timeout=20000)
    check("Model response" in page.locator(".attempt .post").first.inner_text(),
          "Completion survives refresh")


def check_storage_disabled(browser):
    ctx = browser.new_context(viewport={"width": 1000, "height": 1600})
    ctx.add_init_script("""Object.defineProperty(window, 'localStorage', {
        configurable: true, get() { throw Error('localStorage disabled'); }
    });""")
    page = ctx.new_page()
    page.goto(f"{BASE}/C07.html", wait_until="domcontentloaded")
    page.locator(".attempt textarea").first.wait_for(timeout=20000)
    page.locator(".attempt .prediction-input").first.fill("A model choice before feedback")
    page.locator(".attempt button.predict-submit").first.click()
    check(page.locator(".attempt .post").first.is_hidden(), "Disabled storage must NOT reveal the worked response")
    check(page.locator(".attempt .first-attempt").first.is_hidden(), "Attempt gated when prediction save fails")
    check(page.locator(".attempt .prediction-input").first.is_enabled(), "Prediction editable when storage fails")
    check(page.locator(".attempt details").count() == 0, "Disabled storage must NOT insert hints")
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
        print("PASS: 14 HTTP tablet views (7 units x 2 orientations), 44 complete inquiries, "
              "132 three-demand Core1B cycles, 16 science figures across seven chapters, "
              "protected first attempt, refresh readback, disabled-storage disclosure "
              "and no overflow. No academic approval inferred from software validation.")
    finally:
        server.terminate()
        server.wait(timeout=8)


if __name__ == "__main__":
    main()

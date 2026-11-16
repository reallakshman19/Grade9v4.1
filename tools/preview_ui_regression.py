"""Preview UI regression: original WPE practice + tablet navigation, not academic QA."""
from __future__ import annotations
import pathlib, subprocess, sys, time, urllib.request
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
PORT = 8765
BASE = f"http://127.0.0.1:{PORT}"
OUT = ROOT / "preview-ui-artifacts"
OUT.mkdir(exist_ok=True)
URLS = ["preview/index.html", "preview/physics-wpe.html", "preview/practice.html", "preview/progress.html", "preview/alpha-board.html", "preview/batches/index.html", "preview/batches/reader.html"]
SIZES = [(1280,800), (1024,768), (900,1280), (800,1280), (390,844)]
failures = []

def assert_that(condition, message):
    if not condition: raise AssertionError(message)

def open_url(page, path):
    response = page.goto(f"{BASE}/{path}", wait_until="load", timeout=30000)
    assert_that(response is not None and response.status == 200, f"{path}: HTTP 200")
    page.locator("#grade9-universal-nav").wait_for(state="attached", timeout=9000)

def tests(browser):
    for width,height in SIZES:
        ctx=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1, color_scheme="dark")
        page=ctx.new_page()
        for path in URLS:
            errors=[]
            page.on("pageerror",lambda e,errs=errors: errs.append(str(e)))
            open_url(page,path)
            result=page.evaluate("""() => {
              const host=document.querySelector('#grade9-universal-nav');
              const root=host?.shadowRoot;
              const main=document.querySelector('main');
              const allWidth=document.documentElement.scrollWidth;
              return {site:!!root, subjects:root?.querySelectorAll('nav.subjects a').length||0,
                      local:document.querySelectorAll('nav.top-nav').length,
                      bodyWidth:allWidth, viewport:innerWidth,
                      header:!!document.querySelector('header'), main:!!main,
                      cardTop:main?.querySelector('.card')?.getBoundingClientRect().top,
                      mainTop:main?.getBoundingClientRect().top,
                      globalHeight:host?.getBoundingClientRect().height,
                      primaryHeight:root?.querySelector('.primary')?.getBoundingClientRect().height,
                      contextHeight:root?.querySelector('.context')?.getBoundingClientRect().height,
                      navHeight:root?.querySelector('.subjects')?.getBoundingClientRect().height,
                      shortcutsHeight:root?.querySelector('.shortcuts')?.getBoundingClientRect().height};
            }""")
            assert_that(result["site"] and result["subjects"] == 7, f"{path} {width}: seven-link common nav absent {result}")
            assert_that(result["local"]==0, f"{path} {width}: duplicate menu {result}")
            assert_that(result["bodyWidth"]<=result["viewport"]+2, f"{path} {width}: horizontal overflow {result}")
            assert_that(not errors, f"{path} {width}: JS exception {errors}")
            if path=="preview/practice.html":
                assert_that(page.locator(".banner-disclosure").is_visible(), "review status missing")
                assert_that(page.locator("math").count()>10, "MathML absent")
                if width==1024:
                    assert_that(result["cardTop"] is not None and result["cardTop"] < 475,
                                f"Practice question too low on tablet: {result}")
                    # Common subject header stays visible; WPE-specific shortcuts
                    # can be deliberately expanded without covering the question.
                    shortcuts=page.locator("#grade9-universal-nav .nav-shortcuts-btn")
                    assert_that(shortcuts.count()==1,"WPE shortcut toggle missing")
                    shortcuts.click()
                    expanded=page.evaluate("""() => {
                      const s=document.querySelector('#grade9-universal-nav')?.shadowRoot;
                      return s?.querySelector('.context')?.classList.contains('expanded');
                    }""")
                    assert_that(expanded,"WPE shortcuts cannot be expanded")
                    shortcuts.click()
                    page.screenshot(path=str(OUT/"practice-1024x768.png"))
                if width==800:
                    page.screenshot(path=str(OUT/"practice-800x1280.png"))
            if path=="preview/physics-wpe.html" and width==1024:
                page.screenshot(path=str(OUT/"learn-1024x768.png"))
        # Cross-page state and no-answer-leak interaction
        open_url(page,"preview/practice.html")
        assert_that(page.locator("#btn-reveal-solution").is_hidden(),"Solution should be hidden pre-attempt")
        page.locator('input[name="practice-answer"]').first.check()
        page.locator("#learner-reasoning").fill("I would use energy conservation.")
        page.locator("#btn-submit-answer").click()
        assert_that(page.locator("#btn-reveal-solution").is_visible(),"Reveal button should appear after attempt")
        assert_that(page.locator("#panel-solution").is_hidden(),"Solution must remain hidden after attempt")
        page.locator("#btn-reveal-solution").click()
        assert_that(page.locator("#panel-solution").is_visible(),"Worked solution should appear after deliberate reveal")
        saved_before=page.evaluate("() => sessionStorage.getItem('grade9_alpha_progress')")
        open_url(page,"preview/progress.html")
        saved_after=page.evaluate("() => sessionStorage.getItem('grade9_alpha_progress')")
        status_text=page.locator("#status-wpe-practice").inner_text()
        assert_that("attempt recorded" in status_text.casefold(),
                   f"Session progress not preserved: before={saved_before!r}, after={saved_after!r}, status={status_text!r}")
        if width==1024:
            page.locator("#btn-reset-progress").click()
            page.wait_for_function("""() => document.getElementById('status-wpe-practice')?.textContent?.toLowerCase().includes('not started') && sessionStorage.getItem('grade9_alpha_progress') === null""", timeout=8000)
        ctx.close()

def main():
    server = subprocess.Popen([sys.executable,"-m","http.server",str(PORT),"--bind","127.0.0.1"],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(70):
            try:
                urllib.request.urlopen(BASE, timeout=1).read(1)
                break
            except Exception: time.sleep(0.2)
        else: raise RuntimeError("Local HTTP server was not reachable")
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
            try: tests(browser)
            finally:browser.close()
        print("PASS: 7 pages x 5 viewports, no duplicate site menus, no overflow, practice attempt/reveal/progress session; dark-preference regression.")
    finally:server.terminate();server.wait(timeout=8)

if __name__=="__main__":main()

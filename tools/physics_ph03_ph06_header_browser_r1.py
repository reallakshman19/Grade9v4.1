"""HTTP Chromium witness: recovered Momentum routes, Fluids primer, shared header.
Technical candidate only. This does NOT authenticate examination sources or assess free text.
"""
from __future__ import annotations
import functools
import http.server
import threading
from pathlib import Path

from playwright.sync_api import expect,sync_playwright

ROOT=Path(__file__).resolve().parents[1]


def check(browser,base,width,height):
    context=browser.new_context(viewport={"width":width,"height":height},has_touch=True)
    page=context.new_page()
    try:
        physics=base+"/nsejs/physics/"
        def inject_header():
            page.evaluate("""() => {
                if(document.querySelector('script[data-grade9-nav]'))return;
                const el=document.createElement('script');
                el.src='/site-nav.js';
                el.dataset.grade9Nav='common-r1';
                document.head.appendChild(el);
            }""")
            page.locator("#grade9-universal-nav").wait_for(timeout=15000)
            assert page.evaluate("""() => {
              const host=document.querySelector('#grade9-universal-nav');
              const s=host?.shadowRoot;
              return s?.querySelectorAll('nav.subjects a').length===7
                && s?.querySelectorAll('.shortcuts a').length===4
                && !s?.querySelector('.subjects a[href*="/nsejs/physics/index.html"]')?.hasAttribute('disabled');
            }"""),"common header does not have seven subject routes and four focused Physics shortcuts"
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"),"header has horizontal document overflow"

        page.goto(physics+"learn/chapter.html?ph=PH03",wait_until="domcontentloaded")
        expect(page.locator(".g9-lesson-card")).to_have_count(7,timeout=20000)
        expect(page.locator(".g9-hold-note").first).to_contain_text("0/7 accepted")
        inject_header()
        expect(page.locator("#grade9-universal-nav")).to_be_attached()
        for id in ("P01","P02","P03","P04","P05","P06","P07"):
            expect(page.locator("#"+id+" .g9-lesson-actions a")).to_have_count(2)
        page.goto(physics+"textbook/PH03/P01/index.html",wait_until="domcontentloaded")
        expect(page.locator("h1")).to_contain_text("Momentum as mass times signed velocity",timeout=18000)
        expect(page.locator("#model-slider")).to_be_visible(timeout=18000)
        assert "Learning path on HOLD" not in page.locator("main").inner_text()
        page.goto(physics+"core1/PH03/P02/index.html",wait_until="domcontentloaded")
        expect(page.locator("#save-first")).to_be_visible(timeout=18000)
        expect(page.locator("#ph03-status")).not_to_contain_text("Unexpected PH03 content")
        page.goto(physics+"textbook/PH06/index.html",wait_until="domcontentloaded")
        expect(page.locator("h1")).to_have_text("Fluids")
        expect(page.locator("li[data-unit]")).to_have_count(10)
        expect(page.locator('li[data-available-native="true"]')).to_have_count(1)
        expect(page.locator("#fluids-p")).to_have_text("20,000")
        expect(page.locator("#fluids-f")).to_have_text("400")
        page.locator("#fluids-depth").evaluate("(el)=>{el.value='3';el.dispatchEvent(new Event('input',{bubbles:true}))}")
        page.locator("#fluids-area").evaluate("(el)=>{el.value='0.015';el.dispatchEvent(new Event('input',{bubbles:true}))}")
        expect(page.locator("#fluids-p")).to_have_text("30,000")
        expect(page.locator("#fluids-f")).to_have_text("450")
        page.locator("#fluids-check-answer").click()
        expect(page.locator("#fluids-feedback")).to_contain_text("Enter a finite numerical answer")
        assert page.locator("#fluids-worked").is_hidden()
        page.locator("#fluids-skip-answer").click()
        expect(page.locator("#fluids-feedback")).to_contain_text("no correct-answer or mastery credit")
        assert page.locator("#fluids-worked").is_visible()
        page.locator("#fluids-undo-skip").click()
        assert page.locator("#fluids-worked").is_hidden()
        page.locator("#fluids-answer").fill("450")
        page.locator("#fluids-check-answer").click()
        expect(page.locator("#fluids-feedback")).to_contain_text("ungraded")
        expect(page.locator("#fluids-worked")).to_be_visible()
        inject_header()
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"),"Fluids page overflow"
        page.screenshot(path=str(ROOT/"artifacts/ph03-ph06-recovery"/("fluids-"+str(width)+"x"+str(height)+".png")),full_page=True)
        return {"viewport":[width,height],"momentumPairs":7,"fluidNativePairs":1,"fluidRoadmap":10,"headerLinks":7,"academic":"HOLD"}
    finally:
        context.close()


def check_masthead(browser,base):
    ctx=browser.new_context(viewport={"width":1024,"height":768})
    page=ctx.new_page()
    try:
        page.goto(base+"/architecture/guidebook.html",wait_until="domcontentloaded")
        page.evaluate("""() => {
          const el=document.createElement('script');el.src='/site-nav.js';
          el.dataset.grade9Nav='common-r1';document.head.appendChild(el);
        }""")
        expect(page.locator('header.mast nav.tabs[aria-label="Grade9 common navigation: subjects, NSEJS and search"]')).to_be_attached(timeout=15000)
        expect(page.locator("header.mast nav.tabs a")).to_have_count(7)
        assert page.locator("#grade9-universal-nav").count()==0,"duplicate global header added over masthead"
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2")
    finally:ctx.close()


def main():
    artifacts=ROOT/"artifacts/ph03-ph06-recovery"
    artifacts.mkdir(parents=True,exist_ok=True)
    srv=http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    try:
        base="http://127.0.0.1:"+str(srv.server_port)
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
            try:
                results=[check(browser,base,*size) for size in ((1600,1000),(1000,1600))]
                check_masthead(browser,base)
            finally:browser.close()
        import json
        (artifacts/"receipt.json").write_text(json.dumps({
            "disposition":"AUTHOR_EXPOSED_TECHNICAL_PASS_ACADEMIC_HOLD",
            "results":results
        },indent=2)+"\n")
        print("PASS: Momentum 7/7 candidate routes, Fluids transparent 1/10 and interaction, shared header both orientations")
    finally:srv.shutdown()


if __name__=="__main__":main()

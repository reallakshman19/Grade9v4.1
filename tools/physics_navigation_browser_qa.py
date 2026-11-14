#!/usr/bin/env python3
"""HTTP Chromium QA of real NSEJS Physics learner navigation at 12.7-inch viewports."""
from __future__ import annotations
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]

def check_size(page, label):
    dims=page.evaluate("({width:innerWidth,scroll:document.documentElement.scrollWidth})")
    assert dims["scroll"]-dims["width"]<=3,(label,dims)

def run(origin, browser, size):
    ctx=browser.new_context(viewport={"width":size[0],"height":size[1]},
                            has_touch=True,device_scale_factor=1)
    page=ctx.new_page()
    errors=[]
    page.on("pageerror",lambda error:errors.append(str(error)))
    page.route("https://cdn.jsdelivr.net/**",lambda route:route.abort())
    try:
        home=origin+"/nsejs/physics/index.html"
        page.goto(home,wait_until="domcontentloaded")
        page.locator("#chapter-PH01 .g9-chapter-open").wait_for()
        assert page.locator("#chapter-PH03 a").count()==0
        assert not page.locator("#g9-explore-bank").evaluate("(e)=>e.open")
        check_size(page,"home")
        page.locator("#chapter-PH01 .g9-chapter-open").click()
        page.locator("#M01 .g9-lesson-actions a").first.wait_for()
        assert page.locator(".g9-lesson-card").count()==8
        check_size(page,"PH01 chapter")
        page.locator("#M01 .g9-lesson-actions a").first.click()
        page.locator("#g9-learner-nav .g9-study-actions a.g9-next").wait_for()
        assert "PH01" in page.locator("#g9-learner-nav").inner_text()
        page.locator("#g9-learner-nav .g9-study-actions a.g9-next").click()
        page.locator("#g9-learner-nav").wait_for()
        assert "Try it" in page.locator("#g9-learner-nav").inner_text()
        page.locator('#g9-learner-nav a').filter(has_text="Chapter").first.click()
        page.locator("#M01").wait_for()
        # B02 subtopic topology uses the same controls, despite different file tree.
        page.goto(home,wait_until="domcontentloaded")
        page.locator("#chapter-PH09 .g9-chapter-open").click()
        page.locator("#PH09-01 .g9-lesson-actions a").first.wait_for()
        assert page.locator(".g9-lesson-card").count()==12
        page.locator("#PH09-01 .g9-lesson-actions a").first.click()
        page.locator("#g9-learner-nav").wait_for()
        page.locator('#g9-learner-nav .g9-study-actions a').filter(has_text="2 · Try it").click()
        page.locator("#g9-learner-nav").wait_for()
        assert "PH09-01" in page.locator("#g9-learner-nav").inner_text()
        # Original candidate-bank deep-links remain available and offer return.
        page.goto(home+"?topic=optics&from=PH09&unit=PH09-01#topicWorkspace",
                  wait_until="domcontentloaded")
        page.wait_for_function("document.querySelector('#g9-explore-bank').open")
        assert page.locator(".g9-bank-return").count()==1
        # Preview chapters never assert complete subtopic practice.
        page.goto(origin+"/nsejs/physics/learn/chapter.html?ph=PH11",wait_until="domcontentloaded")
        page.locator(".g9-chapter-resources a").first.wait_for()
        assert page.locator(".g9-lesson-card").count()==0
        check_size(page,"PH11 preview")
        assert not errors,errors
        return {"viewport":str(size[0])+"x"+str(size[1]),"status":"PASS"}
    finally:ctx.close()

def main():
    handler=partial(SimpleHTTPRequestHandler,directory=str(ROOT))
    server=ThreadingHTTPServer(("127.0.0.1",0),handler)
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        origin="http://127.0.0.1:"+str(server.server_port)
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for dims in [(1000,1600),(1600,1000)]:
                    print(run(origin,browser,dims),flush=True)
            finally:browser.close()
    finally:server.shutdown();server.server_close();thread.join(timeout=4)

if __name__=="__main__":main()

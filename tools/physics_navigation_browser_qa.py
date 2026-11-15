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
        assert page.locator("#chapter-PH03 a").count()==1
        page.locator("#chapter-PH03 a").click()
        page.locator("#P03 .g9-lesson-actions a").first.wait_for()
        assert page.locator(".g9-lesson-card").count()==1
        assert "Golden Sample only: 1 of 7" in page.locator("#g9-chapter-content").inner_text()
        page.locator("#P03 .g9-lesson-actions a").first.click()
        page.locator("#g9-learner-nav").wait_for()
        assert "Momentum and Collisions" in page.locator("#g9-learner-nav").inner_text()
        assert "Golden Sample" in page.locator("#g9-learner-nav").inner_text()
        check_size(page,"PH03 Golden chapter")
        page.goto(home,wait_until="domcontentloaded")
        assert "Current Electricity" in page.locator("#learn-physics").inner_text()
        assert "PH11" not in page.locator("#learn-physics").inner_text()
        assert "PH05" not in page.locator("#learn-physics").inner_text()
        assert not page.locator("#g9-explore-bank").evaluate("(e)=>e.open")
        check_size(page,"home")
        page.locator("#chapter-PH01 .g9-chapter-open").click()
        page.locator("#M01 .g9-lesson-actions a").first.wait_for()
        assert page.locator(".g9-lesson-card").count()==8
        check_size(page,"PH01 chapter")
        page.locator("#M01 .g9-lesson-actions a").first.click()
        page.locator("#g9-learner-nav .g9-study-actions a.g9-next").wait_for()
        assert "Motion and Kinematics" in page.locator("#g9-learner-nav").inner_text()
        page.locator("#g9-learner-nav .g9-study-actions a.g9-next").click()
        page.locator("#g9-learner-nav").wait_for()
        assert "Try it" in page.locator("#g9-learner-nav").inner_text()
        page.locator('#g9-learner-nav .g9-study-actions a').filter(has_text="Motion and Kinematics").first.click()
        page.locator("#M01").wait_for()
        # B01 primary Core1B redirects to a six-stage shared reader. It must
        # preserve the originating PH07 subtopic and chapter return context.
        page.goto(origin+"/nsejs/physics/curriculum/topics/PH07/b01/PH07-01/core1b.html",
                  wait_until="domcontentloaded")
        page.wait_for_url("**/learner-preview/index.html?subtopic=PH07-01")
        page.locator("#g9-learner-nav .g9-study-actions a").filter(has_text="Heat and Thermal Physics").wait_for()
        assert "Temperature, thermometers and calibration" in page.locator("#g9-learner-nav").inner_text()
        page.locator("#g9-learner-nav .g9-study-actions a").filter(has_text="Heat and Thermal Physics").click()
        page.locator("#PH07-01 .g9-lesson-actions a").first.wait_for()
        assert "ph=PH07" in page.url

        # B02 subtopic topology uses the same controls, despite different file tree.
        page.goto(home,wait_until="domcontentloaded")
        page.locator("#chapter-PH09 .g9-chapter-open").click()
        page.locator("#PH09-01 .g9-lesson-actions a").first.wait_for()
        assert page.locator(".g9-lesson-card").count()==12
        page.locator("#PH09-01 .g9-lesson-actions a").first.click()
        page.locator("#g9-learner-nav").wait_for()
        page.locator('#g9-learner-nav .g9-study-actions a').filter(has_text="2 · Try it").click()
        page.locator("#g9-learner-nav").wait_for()
        assert "Ray model, rectilinear light and ordinary reflection" in page.locator("#g9-learner-nav").inner_text()
        # Original candidate-bank deep-links remain available and offer return.
        page.goto(home+"?topic=optics&from=PH09&unit=PH09-01#topicWorkspace",
                  wait_until="domcontentloaded")
        page.wait_for_function("document.querySelector('#g9-explore-bank').open")
        assert page.locator(".g9-bank-return").count()==1
        # Preview chapters never assert complete subtopic practice.
        page.goto(origin+"/nsejs/physics/learn/chapter.html?ph=PH11",wait_until="domcontentloaded")
        page.locator(".g9-chapter-resources a").first.wait_for()
        assert page.locator(".g9-lesson-card").count()==0
        check_size(page,"Current Electricity preview")
        assert page.locator("#g9-chapter-crumb").inner_text()=="Current Electricity"
        assert page.locator(".g9-chapter-resources a").filter(has_text="foundation worksheet").count()==1
        assert page.locator(".g9-chapter-resources a").filter(has_text="advanced worksheet").count()==1
        # Direct worksheet link must survive a roundtrip to topic-related teaching.
        qid="NSEJS-CIRC-L2-Q14"
        question=home+"?topic=circuits&q="+qid+"#question-"+qid
        page.goto(question,wait_until="domcontentloaded")
        page.locator("#question-"+qid+" a.g9-related-chapter").wait_for(timeout=60000)
        assert page.locator("#question-"+qid+" a.g9-related-chapter").count()==1
        card=page.locator("#question-"+qid)
        # Preserve a committed first attempt across chapter/help navigation.
        card.locator('input[type="radio"]').first.check()
        card.locator("button").filter(has_text="Commit First Attempt").first.click()
        assert "Attempt Saved Locally" in card.inner_text()
        committed=page.evaluate("""id => Object.keys(localStorage)
          .filter(k => k.includes("candidate-attempt:v2:") && k.includes(encodeURIComponent(id)))
          .map(k => [k,localStorage.getItem(k)])""",qid)
        assert len(committed)==1,committed
        card.locator("a.g9-related-chapter").click()
        page.locator(".g9-question-return").wait_for()
        assert "Current Electricity" in page.locator("h1").inner_text()
        assert "exact question-to-lesson match is not independently verified" in page.locator(".g9-return-context").inner_text()
        # Follow reading route and use the native breadcrumb to return.
        chapter_overview=page.locator(".g9-chapter-resources a").first
        assert "curriculum/topics/PH11/index.html" in chapter_overview.get_attribute("href")
        chapter_overview.click()
        page.locator("#g9-learner-nav a").filter(has_text="Return to your question").wait_for()
        page.locator("#g9-learner-nav a").filter(has_text="Return to your question").click()
        page.locator("#question-"+qid).wait_for(timeout=60000)
        assert page.locator("#questions article.card").count()==1
        assert "Attempt Saved Locally" in page.locator("#question-"+qid).inner_text()
        for k,v in committed:
            assert page.evaluate("key => localStorage.getItem(key)",k)==v
        assert qid in page.url
        check_size(page,"Current Electricity question return")
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

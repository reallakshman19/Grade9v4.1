"""WPE-parity PH06 browser receipts; no simulated student mastery."""
import http.server,threading,json,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"artifacts/ph06-golden";ART.mkdir(parents=True,exist_ok=True)
PH="nsejs/physics/"
TASK="AUTHORED-PH06-U08-GOLDEN-MODEL-R1"
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT),**k)
    def log_message(self,*a):pass
def check(page):
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
    for img in page.locator("main img").all():
        expect(img).to_be_visible()
        assert img.evaluate("i=>i.complete&&i.naturalWidth>0")
def attempt(page,correct):
    expect(page.locator("#predictSave")).to_be_visible()
    assert page.locator("#hint,#reveal").count()==0
    page.locator("#prediction").fill("My original prediction")
    page.locator("#predictSave").click()
    expect(page.locator("#commit")).to_be_visible()
    assert page.locator("#hint,#reveal").count()==0
    page.locator("#a-depth").fill("10" if correct else "20")
    page.locator("#a-initial").select_option("Partly emerged, crosses interface")
    page.locator("#a-check").fill("Compare available displacement with weight")
    page.locator("#a-loaded").select_option("Fully submerged, crosses interface" if correct else "Partly emerged, crosses interface")
    page.locator("#a-top").fill("5" if correct else "-2")
    page.locator("#attempt").fill("My original reasoning")
    page.locator("#commit").click()
    expect(page.locator("#reveal")).to_be_visible()
def finish(page,correct):
    page.locator("#hint").click();expect(page.get_by_text("CLARIFY:",exact=False)).to_be_visible()
    assert page.get_by_text("CORRELATE:",exact=False).count()==0
    page.locator("#hint").click();expect(page.get_by_text("CORRELATE:",exact=False)).to_be_visible()
    page.locator("#hint").click();expect(page.get_by_text("OPEN THE WAY:",exact=False)).to_be_visible()
    page.reload();expect(page.locator("#reveal")).to_be_visible()
    page.locator("#reveal").click();expect(page.get_by_text("Pressure-walk check")).to_be_visible()
    expect(page.locator(".review-fields .match")).to_have_count(4 if correct else 1)
    expect(page.locator(".review-fields .mismatch")).to_have_count(0 if correct else 3)
    page.locator("summary").first.click();expect(page.get_by_text("My original reasoning",exact=True)).to_be_visible()
    check(page)
    page.locator("#compare").click();expect(page.locator("#firstIssue")).to_contain_text("All checked values/models match" if correct else "Initial upper-layer thickness")
    page.locator("#diagnosisField").select_option("reason" if correct else "depth")
    page.locator("#diagnosis").fill("Check the first model and its justification")
    page.locator("#diagnose").click();expect(page.locator("#repair")).to_be_visible()
    page.locator("#repair").fill("Compare actual intersection lengths and force balance")
    page.locator("#repairSave").click();expect(page.locator("#boundarySave")).to_be_visible()
    assert page.locator("#boundaryReveal").count()==0
    page.locator("#b-regime").select_option("Upper liquid only")
    page.locator("#b-bottom").fill("8.75")
    page.locator("#boundary").fill("Upper only; bottom above interface")
    page.locator("#boundarySave").click();expect(page.locator("#boundaryReveal")).to_be_visible()
    page.locator("#boundaryReveal").click();expect(page.locator("#sourceReturn")).to_be_visible()
    expect(page.locator(".review-fields .match")).to_have_count(2)
    check(page)
def run():
    srv=http.server.ThreadingHTTPServer(("127.0.0.1",0),Handler);threading.Thread(target=srv.serve_forever,daemon=True).start()
    url=f"http://127.0.0.1:{srv.server_port}/"+PH
    path=url+"core1/PH06/U08/index.html"
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for w,h in [(1000,1600),(1600,1000)]:
                ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                page=ctx.new_page()
                page.goto(url+"learn/chapter.html?ph=PH06")
                expect(page.locator(".g9-hold-note").first).to_contain_text("1 of 10 complete native Learn/Try pairs")
                page.goto(url+"ph06/source-checkpoint.html")
                expect(page.locator("#commit")).to_be_enabled()
                page.locator('input[value="B"]').check();page.locator("#prediction").fill("Source prediction");page.locator("#attempt").fill("Original source reasoning");page.locator("#commit").click()
                expect(page.get_by_role("link",name="Learn Archimedes")).to_be_visible()
                page.get_by_role("link",name="Learn Archimedes").click()
                expect(page.locator("#pt")).to_have_text("Top gauge: 1000 Pa")
                page.locator("#depth").focus();page.keyboard.press("End")
                expect(page.locator("#pb")).to_have_text("Bottom gauge: 5000 Pa")
                assert page.locator("#topArrow").get_attribute("d")=="M152 40V80"
                check(page);page.screenshot(path=str(ART/f"U06-{w}.png"),full_page=True)
                page.locator("#continue").click()
                expect(page.locator("#loadReadout")).to_contain_text("Upper only")
                for val,word in [("1.1","Partly emerged"),("1.8","Fully immersed"),("2.1","No equilibrium")]:
                    page.locator(f'[data-load="{val}"]').tap()
                    expect(page.locator("#loadReadout")).to_contain_text(word)
                assert page.locator("#loadPoint").evaluate("n=>getComputedStyle(n).visibility")=="hidden"
                page.locator('[data-load="1.8"]').tap()
                check(page);page.screenshot(path=str(ART/f"U08-learn-{w}.png"),full_page=True)
                page.locator("#try").click();expect(page.locator("#predictSave")).to_be_visible();check(page)
                assert "3.20 kg" not in page.locator("main").inner_text()
                expect(page.get_by_role("link",name="Return to Fluids Golden Sample →")).to_be_visible()
                page.screenshot(path=str(ART/f"U08-prompt-{w}.png"),full_page=True)
                attempt(page,correct=w==1600);finish(page,correct=w==1600)
                page.screenshot(path=str(ART/f"U08-boundary-{w}.png"),full_page=True)
                page.locator("#sourceReturn").click();expect(page.locator("#attempt")).to_have_value("Original source reasoning")
                expect(page.locator('input[value="B"]')).to_be_checked()
                page.locator("#retry").fill("Reconstruct by summing displaced liquid weights");page.locator("#retrySave").click();expect(page.locator("#retry")).to_be_disabled()
                print(f"{w}x{h} HTTP Chromium PASS: guide, keyboard, touch, structured response checks, exact source return and screenshots.")
                ctx.close()
            # Deny commit after prediction saved; no hint/reconstruction may appear.
            ctx=browser.new_context();page=ctx.new_page();page.goto(path)
            expect(page.locator("#predictSave")).to_be_visible();page.locator("#prediction").fill("P");page.locator("#predictSave").click()
            expect(page.locator("#commit")).to_be_visible()
            page.evaluate("() => { Storage.prototype.setItem=function(){throw Error('injected write denial')}; }")
            page.locator("#attempt").fill("R");page.locator("#commit").click();expect(page.locator("#stage")).to_contain_text("HOLD")
            assert page.locator("#hint,#reveal").count()==0
            print("SAVE_FAILURE FAIL_CLOSED: actual first-attempt write denied; no reveal.")
            ctx.close()
            ctx=browser.new_context();ctx.route("**/figures/u08-prompt.svg",lambda r:r.fulfill(status=404,body="missing"))
            page=ctx.new_page();page.goto(path);expect(page.locator("#root")).to_contain_text("HOLD");assert page.locator("#reveal,#predictSave").count()==0
            print("BAD_SOURCE_FIGURE FAIL_CLOSED: required authored prompt SVG missing; attempt unavailable (not original custody).")
            ctx.close()
            ctx=browser.new_context();page=ctx.new_page();page.goto(path);attempt(page,False)
            def altered(r):
                response=r.fetch();r.fulfill(response=response,body=response.text().replace("</svg>","<!-- altered revision --></svg>"))
            ctx.route("**/figures/u08-prompt.svg",altered);page.reload();expect(page.locator("#predictSave")).to_be_visible();assert page.locator("#reveal").count()==0
            print("STALE_REVISION REJECTED: changed SVG bytes do not rehydrate prior first attempt.")
            ctx.close()
            ctx=browser.new_context();page=ctx.new_page();page.goto(path);expect(page.locator("#predictSave")).to_be_visible()
            assert page.locator("#hint,#reveal").count()==0 and "3.20 kg" not in page.locator("main").inner_text()
            page.locator("#prediction").fill("P");page.locator("#predictSave").click();expect(page.locator("#commit")).to_be_visible()
            assert page.locator("#hint,#reveal").count()==0
            print("HINT_LEAK BLOCKED: no hint or solution control or solved value before first commit; public code is not secure.")
            ctx.close()
            # Complete challenge before entering source: must not retroactively unlock a source reattempt.
            ctx=browser.new_context();page=ctx.new_page();page.goto(path);attempt(page,True);finish(page,True);page.locator("#sourceReturn").click()
            expect(page.locator("#commit")).to_be_enabled();page.locator('input[value="A"]').check();page.locator("#prediction").fill("P");page.locator("#attempt").fill("Later source");page.locator("#commit").click()
            expect(page.get_by_role("link",name="Learn Archimedes")).to_be_visible();assert page.locator("#retry").count()==0
            expect(page.locator("#status")).to_contain_text("LOCAL_PRIOR_EXPOSURE_RECORDED")
            page.goto(path);expect(page.locator("#sourceReturn")).to_be_visible();page.locator("#sourceReturn").click();expect(page.locator("#attempt")).to_have_value("Later source");assert page.locator("#retry").count()==0
            print("SOURCE_CHRONOLOGY REJECTED: earlier transfer cannot unlock later source first attempt.")
            ctx.close();browser.close()
    finally:srv.shutdown();srv.server_close()
if __name__=="__main__":run()

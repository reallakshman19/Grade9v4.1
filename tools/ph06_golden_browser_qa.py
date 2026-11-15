"""Golden sample Chromium receipts — author-side technical verification only."""
import http.server,threading,json
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
def run():
    srv=http.server.ThreadingHTTPServer(("127.0.0.1",0),Handler);threading.Thread(target=srv.serve_forever,daemon=True).start()
    url=f"http://127.0.0.1:{srv.server_port}/"+PH
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for w,h in [(1000,1600),(1600,1000)]:
                ctx=browser.new_context(viewport={"width":w,"height":h});page=ctx.new_page()
                page.goto(url+"learn/chapter.html?ph=PH06")
                expect(page.get_by_text("Golden Sample only:",exact=False)).to_be_visible()
                expect(page.locator("#U08")).to_be_visible()
                page.goto(url+"ph06/source-checkpoint.html")
                expect(page.locator("#commit")).to_be_enabled()
                page.locator('input[value="B"]').check()
                page.locator("#prediction").fill("I think the upper liquid matters")
                page.locator("#attempt").fill("Initial source reasoning, incorrect option")
                page.locator("#commit").click()
                expect(page.get_by_role("link",name="Learn Archimedes")).to_be_visible()
                page.get_by_role("link",name="Learn Archimedes").click()
                expect(page.locator("#pt")).to_have_text("Top gauge: 1000 Pa")
                page.locator("#depth").fill("0.40")
                expect(page.locator("#pb")).to_have_text("Bottom gauge: 5000 Pa")
                check(page);page.screenshot(path=str(ART/f"U06-{w}.png"),full_page=True)
                page.locator("#continue").click()
                check(page);page.screenshot(path=str(ART/f"U08-learn-{w}.png"),full_page=True)
                page.locator("#try").click()
                expect(page.locator("#commit")).to_be_enabled()
                check(page)
                assert not page.locator("#post").inner_text().strip()
                assert "3.20 kg" not in page.locator("main").inner_text()
                page.screenshot(path=str(ART/f"U08-prompt-{w}.png"),full_page=True)
                # Independent first response, then assistance in order.
                page.locator("#prediction").fill("Top remains exposed (wrong)")
                page.locator("#attempt").fill("I used the same volume partition (wrong)")
                page.locator("#commit").click()
                expect(page.locator("#attempt")).to_be_disabled()
                page.locator("#hint").click()
                expect(page.get_by_text("CLARIFY:",exact=False)).to_be_visible()
                assert page.get_by_text("CORRELATE:",exact=False).count()==0
                page.locator("#hint").click();expect(page.get_by_text("CORRELATE:",exact=False)).to_be_visible()
                page.locator("#hint").click();expect(page.get_by_text("OPEN THE WAY:",exact=False)).to_be_visible()
                page.reload();expect(page.locator("#attempt")).to_have_value("I used the same volume partition (wrong)")
                page.locator("#reveal").click();expect(page.get_by_text("Pressure-walk check")).to_be_visible()
                page.locator("#diagnosis").fill("I continued the emerged regime")
                page.locator("#diagnose").click()
                page.locator("#repair").fill("Compare top-flush mass and solve submerged regime")
                page.locator("#repairSave").click()
                page.locator("#boundary").fill("Upper only; depth 8.75 cm")
                page.locator("#boundarySave").click()
                page.locator("#boundaryReveal").click()
                expect(page.get_by_text("8.75 cm",exact=False).last).to_be_visible()
                page.screenshot(path=str(ART/f"U08-repair-{w}.png"),full_page=True)
                page.locator("#sourceReturn").click()
                expect(page.locator("#attempt")).to_have_value("Initial source reasoning, incorrect option")
                expect(page.locator('input[value="B"]')).to_be_checked()
                page.locator("#retry").fill("Reconstruct by summing displaced liquid weights")
                page.locator("#retrySave").click();expect(page.locator("#retry")).to_be_disabled()
                ctx.close()
            path=url+"core1/PH06/U08/index.html"
            # Storage denial, and missing required figure.
            ctx=browser.new_context();ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw Error('denied')}})")
            page=ctx.new_page();page.goto(path);expect(page.locator("#status")).to_contain_text("HOLD");expect(page.locator("#commit")).to_be_disabled();assert not page.locator("#post").inner_text().strip();ctx.close()
            ctx=browser.new_context();ctx.route("**/figures/u08-prompt.svg",lambda r:r.fulfill(status=404,body="missing"))
            page=ctx.new_page();page.goto(path);expect(page.locator("#root")).to_contain_text("HOLD");assert page.locator("#reveal").count()==0;ctx.close()
            # Same browser, changed actual SVG bytes cannot rehydrate first response.
            ctx=browser.new_context();page=ctx.new_page();page.goto(path);expect(page.locator("#commit")).to_be_enabled()
            page.locator("#prediction").fill("prediction");page.locator("#attempt").fill("original");page.locator("#commit").click();expect(page.locator("#reveal")).to_be_visible()
            def altered(r):
                response=r.fetch()
                r.fulfill(response=response,body=response.text().replace("</svg>","<!-- altered revision --></svg>"))
            ctx.route("**/figures/u08-prompt.svg",altered);page.reload();expect(page.locator("#commit")).to_be_enabled();expect(page.locator("#attempt")).to_have_value("");assert page.locator("#reveal").count()==0
            ctx.close();browser.close()
        print("PH06 GOLDEN: 2 orientations, source roundtrip, ordered hints, persisted attempt, denied storage, missing and revised SVG checks PASS")
    finally:srv.shutdown();srv.server_close()
if __name__=="__main__":run()

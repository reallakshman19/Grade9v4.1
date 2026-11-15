"""Exact-head HTTP Chromium QA for source-led PH05 R2, not academic acceptance."""
import contextlib
import http.server
import json
import os
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
REL="nsejs/physics/ph05/source-led-r2"
DATA=json.loads((ROOT/REL/"packages.v1.json").read_text())
MODELS={t["uid"]:t for t in json.loads((ROOT/REL/"models.v1.json").read_text())["models"]}
ART=ROOT/"artifacts/ph05-r2"
ART.mkdir(parents=True,exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kw):super().__init__(*args,directory=str(ROOT),**kw)
    def log_message(self,*args):pass

def check_figure(page):
    for img in page.locator("img").all():
        expect(img).to_be_visible()
        assert img.evaluate("(i) => i.complete && i.naturalWidth > 0")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1"),page.url

def run():
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    url=f"http://127.0.0.1:{server.server_port}/{REL}/index.html"
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for w,h in [(1000,1600),(1600,1000)]:
                ctx=browser.new_context(viewport={"width":w,"height":h})
                page=ctx.new_page()
                for unit in DATA["stable_subtopics"]:
                    suffix=unit["id"][-3:]
                    for role,folder in [("learn","textbook"),("practice","core1")]:
                        page.goto(f"http://127.0.0.1:{server.server_port}/nsejs/physics/{folder}/PH05/{suffix}/index.html")
                        expect(page.locator("main h1")).to_contain_text(unit["title"])
                        assert page.locator("main a.action").count()>0
                        assert page.locator("main a").filter(has_text="Archived earlier candidate").count()==1
                for pack in DATA["packages"]:
                    p=pack["id"]
                    page.goto(f"{url}?package={p}&stage=learn")
                    expect(page.get_by_text("01 · Learn to reason")).to_be_visible()
                    check_figure(page)
                    if p=="P06":page.screenshot(path=str(ART/f"P06-guide-{w}.png"),full_page=True)
                    for t in pack["tasks"]:
                        uid=t["uid"]
                        page.goto(f"{url}?package={p}&task={uid}")
                        expect(page.locator("#commit")).to_be_enabled()
                        check_figure(page)
                        assert not page.locator("#post").inner_text().strip()
                        assert MODELS[uid]["reconstruction"] not in page.locator("body").inner_text()
                        if uid.endswith("P06-A"):page.screenshot(path=str(ART/f"P06-prompt-{w}.png"),full_page=True)
                        page.locator("#prediction").fill("First prediction")
                        page.locator("#attempt").fill("First reasoning response")
                        page.locator("#commit").click()
                        expect(page.locator("#reveal")).to_be_visible()
                        expect(page.locator("#attempt")).to_be_disabled()
                        page.locator("#hint").click()
                        expect(page.get_by_text("H1:",exact=False)).to_be_visible()
                        page.reload()
                        expect(page.locator("#attempt")).to_have_value("First reasoning response")
                        page.locator("#reveal").click()
                        expect(page.get_by_text("04 · Reconstruction")).to_be_visible()
                        page.locator("#diagnosis").fill("First divergence")
                        page.locator("#diagnose").click()
                        page.locator("#repair").fill("Repaired reasoning")
                        page.locator("#repairSave").click()
                        page.locator("#boundary").fill("Boundary reasoning")
                        page.locator("#boundarySave").click()
                        page.locator("#boundaryReveal").click()
                        expect(page.get_by_text("08 · Return to original source")).to_be_visible()
                ctx.close()
            ctx=browser.new_context()
            page=ctx.new_page()
            source="NSEJS-2022-C51-Q36"
            page.goto(f"{url}?package=P06&source={source}")
            expect(page.locator("#sc")).to_be_enabled()
            assert not page.locator("#next").inner_text().strip()
            page.locator("#sp").fill("Initial source prediction")
            page.locator("#sa").fill("Initial source reasoning")
            page.locator("#sc").click()
            page.get_by_role("link",name="Open Core1A guide").click()
            expect(page.get_by_text("01 · Learn to reason")).to_be_visible()
            page.get_by_role("link",name="D3.6 · candidate A").click()
            expect(page.locator("#commit")).to_be_enabled()
            page.locator("#prediction").fill("First transfer prediction")
            page.locator("#attempt").fill("First transfer reasoning")
            page.locator("#commit").click()
            expect(page.locator("#reveal")).to_be_visible()
            page.locator("#reveal").click()
            page.locator("#diagnosis").fill("Diagnosis")
            page.locator("#diagnose").click()
            page.locator("#repair").fill("Repair")
            page.locator("#repairSave").click()
            page.locator("#boundary").fill("Boundary")
            page.locator("#boundarySave").click()
            page.locator("#boundaryReveal").click()
            page.get_by_role("link",name=f"Return to source checkpoint: {source}").click()
            expect(page.locator("#sa")).to_have_value("Initial source reasoning")
            page.locator("#retry").fill("Reconstructed source reasoning")
            page.locator("#retrySave").click()
            expect(page.locator("#retry")).to_be_disabled()
            ctx.close()
            ctx=browser.new_context()
            ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('denied')}})")
            page=ctx.new_page()
            page.goto(f"{url}?package=P06&task=AUTHORED-PH05-R2-P06-A")
            expect(page.locator("#status")).to_contain_text("HOLD")
            expect(page.locator("#commit")).to_be_disabled()
            assert not page.locator("#post").inner_text().strip()
            ctx.close()
            browser.close()
    finally:
        server.shutdown();server.server_close()
    print("PH05 R2: 30 task journeys, 18 guides, 28 canonical route loads, exact source return, storage denial PASS")
if __name__=="__main__":run()

"""Verify published search UI and safe search-to-reader links at two viewport sizes."""
from __future__ import annotations
import http.server
import threading
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*args,**kw): super().__init__(*args,directory=str(ROOT),**kw)
    def log_message(self,*args): pass

def main():
    srv=http.server.ThreadingHTTPServer(("127.0.0.1",0),Handler)
    threading.Thread(target=srv.serve_forever,daemon=True).start()
    origin=f"http://127.0.0.1:{srv.server_port}/"
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            for w,h in [(1000,1600),(1600,1000)]:
                context=browser.new_context(viewport={"width":w,"height":h})
                page=context.new_page()
                cases=[
                    ("nsejs/index.html","AUTHORED-PH05-R2-P06-A","nsejs/physics/ph05/source-led-r2/index.html","task=AUTHORED-PH05-R2-P06-A"),
                    ("nsejs/physics/textbook/PH05/G03/index.html","CHEM-C14.01-study","", "subtopic=CHEM-C14.01"),
                    ("curriculum/chemistry/preview/C01.html","BIO-NSEJS-GEN-01","nsejs/biology/index.html","q=BIO-NSEJS-GEN-01"),
                    ("nsejs/biology/index.html","NSEJS-CIRC-L2-Q14","nsejs/physics/index.html","NSEJS-CIRC-L2-Q14"),
                    # New exact Physics V2 routes must resolve through the
                    # shared header search; don't promote them to exam PASS.
                    ("nsejs/index.html","AUTHORED-PH01-M05-R2-INVERSE-01","nsejs/physics/quality-r1/challenge.html","unit=PH01-M05"),
                    ("nsejs/physics/quality-r1/study.html?unit=PH07-02","QUALITY-PH08-08-CORE1A","nsejs/physics/quality-r1/study.html","unit=PH08-08"),
                    ("nsejs/physics/index.html","QUALITY-PH02-SOURCE-STATUS","nsejs/physics/quality-r1/source.html","ph=PH02"),
                ]
                for path,term,expected,query in cases:
                    page.goto(origin+path,wait_until="domcontentloaded")
                    page.wait_for_function("window.Grade9Search?.initialized === true")
                    page.keyboard.press("Control+k")
                    expect(page.locator("#g9SearchTitle")).to_have_text("Search NSEJS Junior Science")
                    expect(page.locator(".g9-search-dialog")).to_be_visible()
                    page.locator('.g9-search-dialog input[type="search"]').fill(term)
                    page.wait_for_function("(q)=>[...document.querySelectorAll('.g9-search-result')].some(a=>a.href.includes(q))",arg=query)
                    result=page.locator(".g9-search-result").filter(has=page.locator("span")).all()
                    links=[a.get_attribute("href") or "" for a in result]
                    assert any(query in u and (not expected or expected in u) for u in links),(term,links)
                    assert "official key:" not in page.locator(".g9-search-dialog").inner_text().lower()
                    page.keyboard.press("Escape")
                page.goto(origin+"nsejs/biology/index.html",wait_until="domcontentloaded")
                page.wait_for_function("window.Grade9Search?.initialized === true")
                page.evaluate("window.Grade9Search.open({scope:'biology',query:'genetics'})")
                expect(page.locator(".g9-search-result").first).to_be_visible()
                assert all("Biology" in x.inner_text() for x in page.locator(".g9-search-result").all())
                context.close()
            browser.close()
        print("NSEJS search: all subjects, nested page paths, exact results and scope PASS")
    finally:
        srv.shutdown();srv.server_close()
if __name__=="__main__":main()

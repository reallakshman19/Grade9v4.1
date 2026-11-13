#!/usr/bin/env python3
"""HTTP Chromium route and protected D4 candidate checks."""
import subprocess,sys,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from physics_ph01_r31_core1b_browser_qa import free_port
ROOT=Path(__file__).resolve().parents[1]
def main():
    port=free_port();origin=f"http://127.0.0.1:{port}"
    server=subprocess.Popen([sys.executable,"-m","http.server",str(port),"--bind","127.0.0.1","--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:urllib.request.urlopen(origin+"/nsejs/physics/textbook/PH01/core2-links/index.html",timeout=1).close();break
            except Exception:time.sleep(.1)
        else:raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for w,h in ((1000,1600),(1600,1000)):
                ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                page=ctx.new_page()
                uid="g9:pcb:physics:nsejs-2024-physics-r1:020"
                page.goto(origin+"/nsejs/core2/question-map.html#"+uid)
                row=page.locator("tr").filter(has=page.locator("code",has_text=uid))
                row.locator("[data-ph01-core2-link]").click()
                page.wait_for_url("**/core2-links/index.html#PH01-LINK-2024-51-Q60")
                panel=page.locator("#PH01-LINK-2024-51-Q60")
                panel.locator("summary").click()
                panel.locator("a[href*='PH01-M05-QRT-SYNTHESIZE-D4-R41-INSTANCE']").click()
                page.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Candidate task loaded')")
                assert page.locator("#cycleSelect").input_value()=="PH01-M05-QRT-SYNTHESIZE-D4-R41-INSTANCE"
                assert page.locator("#cycleSelect option").count()==4
                assert page.locator("#postAttempt").is_hidden()
                page.locator("#predictInput").fill("Independent prediction")
                page.locator("#attemptInput").fill("Independent graph reconstruction")
                if w==1000:page.locator("#saveFirst").tap()
                else:page.locator("#saveFirst").press("Enter")
                assert page.locator("#saveFirst").is_disabled()
                page.locator("#showReconstruct").click()
                assert page.locator("#reconstructAnswer").is_visible()
                assert page.locator("#showBoundary").is_disabled()
                page.locator("#core2-return a").click()
                page.wait_for_url("**/core2-links/index.html")
                page.go_back()
                page.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Candidate task loaded')")
                assert page.locator("#saveFirst").is_disabled()
                page.goto(origin+"/nsejs/physics/index.html?topic=mechanics#question-NSEJS-24-MECH-03")
                page.locator("#question-NSEJS-24-MECH-03 [data-ph01-core2-link]").click()
                page.wait_for_url("**/core2-links/index.html#PH01-LINK-2024-51-Q37")
                ctx.close()
            browser.close()
        print("PH01 source route and D4 protected first attempt PASS; academic HOLD")
    finally:server.terminate();server.wait(timeout=5)
if __name__=="__main__":main()

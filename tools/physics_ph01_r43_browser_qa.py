#!/usr/bin/env python3
"""HTTP Chromium protected APPLY/JUSTIFY paths and exact Core2 return."""
import json,subprocess,sys,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from physics_ph01_r31_core1b_browser_qa import free_port
ROOT=Path(__file__).resolve().parents[1]
def ready(page):page.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Candidate task loaded')")
def main():
    routes=json.loads((ROOT/"nsejs/physics/curriculum/agent1/PH01/ph01-subtopic-routes.r4_3.json").read_text())
    pack=json.loads((ROOT/"nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_3.json").read_text())
    port=free_port();origin=f"http://127.0.0.1:{port}"
    server=subprocess.Popen([sys.executable,"-m","http.server",str(port),"--bind","127.0.0.1","--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:urllib.request.urlopen(origin+"/nsejs/physics/textbook/PH01/core2-links-r43/index.html",timeout=1).close();break
            except Exception:time.sleep(.1)
        else:raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for w,h in ((1000,1600),(1600,1000)):
                ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                page=ctx.new_page()
                for u in routes["units"]:
                    m=u["subtopic_id"][-3:]
                    page.goto(origin+"/"+u["core1a"])
                    page.get_by_role("link",name=f"Open {m} R4.3 · D3/D4 practice").click();ready(page)
                    assert set(page.locator("#cycleSelect option").evaluate_all("(xs)=>xs.map(x=>x.value)"))==set(u["instance_ids"])
                    candidates=[c for c in pack["core1b"] if c["id"] in u["instance_ids"] and c["cell_id"] in ("D3.3","D3.7")]
                    for c in candidates:
                        cid=c["id"];page.locator("#cycleSelect").select_option(cid)
                        assert page.locator("#postAttempt").is_hidden()
                        page.locator("#predictInput").fill("My prediction")
                        page.locator("#attemptInput").fill("My independent "+m+" "+c["cell_id"]+" reasoning")
                        if w==1000:page.locator("#saveFirst").tap()
                        else:page.locator("#saveFirst").press("Enter")
                        assert page.locator("#saveFirst").is_disabled()
                        page.get_by_role("button",name="Open H1").click()
                        page.locator("#showReconstruct").click()
                        assert page.locator("#reconstructAnswer").is_visible()
                        assert page.locator("#showBoundary").is_disabled()
                        page.locator("#boundaryInput").fill("My changed-condition reasoning")
                        page.locator("#saveBoundary").click()
                        page.locator("#showBoundary").click()
                        assert page.locator("#boundaryAnswer").is_visible()
                        page.reload();ready(page);page.locator("#cycleSelect").select_option(cid)
                        assert page.locator("#saveFirst").is_disabled()
                        assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
                page.goto(origin+"/"+routes["integrated_main"]["path"]);ready(page)
                assert page.locator("#cycleSelect option").count()==8
                for cid in ("PH01-MAIN-D3.3-R43","PH01-MAIN-D3.7-R43"):
                    page.locator("#cycleSelect").select_option(cid)
                    assert page.locator("#postAttempt").is_hidden()
                page.goto(origin+"/nsejs/physics/index.html?topic=mechanics#question-NSEJS-24-MECH-03")
                page.locator("#question-NSEJS-24-MECH-03 [data-ph01-r43-link]").click()
                page.wait_for_url("**/core2-links-r43/index.html#PH01-LINK-2024-51-Q37")
                panel=page.locator("#PH01-LINK-2024-51-Q37");panel.locator("summary").click()
                panel.locator("a[href*='PH01-M08-QRT-APPLY-D3-R43-INSTANCE']").click();ready(page)
                assert page.locator("#cycleSelect").input_value()=="PH01-M08-QRT-APPLY-D3-R43-INSTANCE"
                page.locator("#core2-return a").click()
                page.wait_for_url("**/core2-links-r43/index.html#PH01-LINK-2024-51-Q37")
                ctx.close()
            browser.close()
        print("PH01 R4.3 all APPLY/JUSTIFY instances, eight MAIN selector and source return PASS; academic HOLD")
    finally:server.terminate();server.wait(timeout=5)
if __name__=="__main__":main()

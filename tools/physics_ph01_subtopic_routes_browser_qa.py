#!/usr/bin/env python3
"""HTTP Chromium QA for independent M01/M02 Core1A/B and MAIN routes."""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from physics_ph01_r31_core1b_browser_qa import free_port
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review-artifacts/physics-core1b/subtopic-routes"
BASE = "/nsejs/physics/"
RUNTIME = BASE + "core1/ph01-qrt-r31/index.html"
def ready(page):
    page.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Candidate task loaded')")
def record(page, cid):
    return page.evaluate("""cid => {
      const k=Object.keys(localStorage).find(k=>k.startsWith('G9V41:PH01:R31:') && k.endsWith(':'+cid));
      return k ? JSON.parse(localStorage.getItem(k)) : null;
    }""", cid)
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    port = free_port()
    server = subprocess.Popen([sys.executable,"-m","http.server",str(port),"--bind","127.0.0.1","--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    origin = f"http://127.0.0.1:{port}"
    receipt = {"task":"PH01_SUBTOPIC_ROUTES","academic_status":"HOLD","tests":[]}
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(origin+RUNTIME,timeout=1).close()
                break
            except Exception:
                time.sleep(.1)
        else:
            raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                for w,h in ((1000,1600),(1600,1000)):
                    ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                    page=ctx.new_page()
                    errors=[]
                    page.on("pageerror",lambda err:errors.append(str(err)))
                    page.on("console",lambda msg:errors.append(msg.text) if msg.type=="error" else None)
                    for sub in ("M01","M02"):
                        a=BASE+"textbook/PH01/"+sub+"/index.html"
                        b=BASE+"core1/ph01-"+sub.lower()+"-r31/index.html"
                        page.goto(origin+a)
                        assert "PH01-"+sub in page.locator("header").inner_text()
                        assert page.locator("svg[role=img]").count()==1
                        assert page.locator(".example").count()==3
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1")
                        page.screenshot(path=str(OUT/f"{sub}-core1a-{w}x{h}.png"),full_page=True)
                        page.get_by_role("link",name=f"Open {sub} Core1B").click()
                        page.wait_for_url("**"+b)
                        ready(page)
                        ids=page.locator("#cycleSelect option").evaluate_all("(xs)=>xs.map(x=>x.value)")
                        assert len(ids)==3 and all(x.startswith("PH01-"+sub+"-") and "INSTANCE" in x for x in ids)
                        cid=ids[0]
                        assert page.locator("#postAttempt").is_hidden()
                        page.locator("nav [data-textbook-help]").click()
                        page.wait_for_url("**"+a)
                        page.go_back()
                        ready(page)
                        page.locator("#predictInput").fill("My initial prediction.")
                        page.locator("#attemptInput").fill("My original reasoning for "+sub)
                        if w==1000: page.locator("#saveFirst").tap()
                        else: page.locator("#saveFirst").press("Enter")
                        first=record(page,cid)
                        assert first["first_answer"]["answer"]=="My original reasoning for "+sub
                        assert "TEXTBOOK_BEFORE_FIRST" in {x["kind"] for x in first["help_exposure"]}
                        page.get_by_role("button",name="Open H1").click()
                        page.locator("#showReconstruct").click()
                        assert page.locator("#reconstructAnswer").is_visible()
                        assert page.locator("#showBoundary").is_disabled()
                        page.locator("#boundaryInput").fill("A changed-condition response.")
                        page.locator("#saveBoundary").click()
                        page.locator("#showBoundary").click()
                        assert page.locator("#boundaryAnswer").is_visible()
                        page.reload()
                        ready(page)
                        assert page.locator("#saveFirst").is_disabled()
                        assert record(page,cid)["first_answer"]==first["first_answer"]
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1")
                        page.screenshot(path=str(OUT/f"{sub}-core1b-{w}x{h}.png"),full_page=True)
                        # The old combined view sees the same immutable first attempt.
                        page.goto(origin+RUNTIME)
                        ready(page)
                        page.locator("#cycleSelect").select_option(cid)
                        assert page.locator("#saveFirst").is_disabled()
                        assert record(page,cid)["first_answer"]==first["first_answer"]
                        page.goto(origin+b)
                        ready(page)
                        for other in ids[1:]:
                            page.locator("#cycleSelect").select_option(other)
                            assert page.locator("#postAttempt").is_hidden()
                            assert page.locator("#saveFirst").is_enabled()
                        receipt["tests"].append({"scope":sub,"viewport":f"{w}x{h}","three_instances":True,"same_first_attempt_across_views":True,"pre_first_help":True,"status":"PASS"})
                    page.goto(origin+BASE+"core1/ph01-main-r31/index.html")
                    ready(page)
                    mainids=page.locator("#cycleSelect option").evaluate_all("(xs)=>xs.map(x=>x.value)")
                    assert len(mainids)==3 and all(x.startswith("PH01-MAIN-") for x in mainids)
                    assert not errors,errors
                    receipt["tests"].append({"scope":"MAIN","viewport":f"{w}x{h}","three_main_only":True,"status":"PASS"})
                    ctx.close()
                ctx=browser.new_context()
                page=ctx.new_page()
                page.goto(origin+BASE+"core1/ph01-m01-r31/index.html")
                ready(page)
                page.evaluate("""()=>localStorage.setItem('G9V41:PH01:R31:old:PH01-M01-QRT-MODEL-D3-INSTANCE-R31',JSON.stringify({first_answer:{answer:'stale'}}))""")
                page.reload()
                ready(page)
                assert page.locator("#postAttempt").is_hidden()
                ctx.close()
                ctx=browser.new_context()
                ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})")
                page=ctx.new_page()
                page.goto(origin+BASE+"core1/ph01-m02-r31/index.html")
                page.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Storage unavailable')")
                assert page.locator("#saveFirst").is_disabled() and page.locator("#postAttempt").is_hidden()
                ctx.close()
                receipt["tests"].append({"scope":"M01/M02","stale_revision_ignored":True,"blocked_storage_fail_closed":True,"status":"PASS"})
            finally:
                browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)
    (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))
if __name__=="__main__":
    main()

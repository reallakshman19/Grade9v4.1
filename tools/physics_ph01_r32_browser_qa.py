#!/usr/bin/env python3
"""Exercise all new PH01 unit and MAIN pages over HTTP Chromium."""
import json, subprocess, sys, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from physics_ph01_r31_core1b_browser_qa import free_port
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"review-artifacts/physics-core1b/r32"
BASE="/nsejs/physics/"
def ready(p): p.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Candidate task loaded')")
def storage_record(page, cid):
    return page.evaluate("""cid => {
      const k = Object.keys(localStorage).find(k => k.endsWith(":"+cid) && k.startsWith("G9V41:PH01:"));
      return k ? JSON.parse(localStorage.getItem(k)) : null;
    }""", cid)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    routes=json.loads((ROOT/"nsejs/physics/curriculum/agent1/PH01/ph01-subtopic-routes.r3_2.json").read_text(encoding="utf-8"))
    port=free_port(); origin=f"http://127.0.0.1:{port}"
    server=subprocess.Popen([sys.executable,"-m","http.server",str(port),"--bind","127.0.0.1","--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    receipt={"task":"PH01_R32_ALL_UNITS","academic_status":"HOLD","tests":[]}
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(origin+BASE+"textbook/PH01/index.html",timeout=1).close()
                break
            except Exception: time.sleep(.1)
        else: raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            try:
                for w,h in ((1000,1600),(1600,1000)):
                    ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                    page=ctx.new_page(); errors=[]
                    page.on("pageerror",lambda e:errors.append(str(e)))
                    page.on("console",lambda m:errors.append(m.text) if m.type=="error" else None)
                    for u in routes["units"]:
                        m=u["subtopic_id"][-3:]
                        page.goto(origin+"/"+u["core1a"])
                        assert u["subtopic_id"] in page.locator("header.mast").inner_text()
                        assert page.locator("svg[role=img]").count()>=1
                        assert page.locator(".example").count()==3
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1")
                        page.screenshot(path=str(OUT/f"{m}-core1a-{w}x{h}.png"),full_page=True)
                        # Historical R3.2 remains available only in the reviewer archive.
                        page.locator("details.g9-review-versions summary").click()
                        page.locator("details.g9-review-versions").get_by_role("link",name=f"Open {m} Core1B").click()
                        page.wait_for_url("**/"+u["core1b"])
                        ready(page)
                        ids=page.locator("#cycleSelect option").evaluate_all("(xs)=>xs.map(x=>x.value)")
                        assert set(ids)==set(u["instance_ids"])
                        for cid in ids:
                            page.locator("#cycleSelect").select_option(cid)
                            assert page.locator("#postAttempt").is_hidden()
                            assert page.locator("#saveFirst").is_enabled()
                        page.locator("#cycleSelect").select_option(ids[0])
                        page.locator("nav [data-textbook-help]").click()
                        page.wait_for_url("**/"+u["core1a"])
                        page.go_back(); ready(page)
                        page.locator("#predictInput").fill("Initial prediction.")
                        page.locator("#attemptInput").fill("Original reasoning for "+m)
                        if w==1000: page.locator("#saveFirst").tap()
                        else: page.locator("#saveFirst").press("Enter")
                        assert page.locator("#saveFirst").is_disabled()
                        first=page.locator("#savedFirst").inner_text()
                        assert "Original reasoning for "+m in first
                        initial=storage_record(page,ids[0])
                        assert initial["first_answer"]["answer"]=="Original reasoning for "+m
                        assert "TEXTBOOK_BEFORE_FIRST" in {x["kind"] for x in initial["help_exposure"]}
                        assert page.get_by_role("button",name="Open H2").is_disabled()
                        page.get_by_role("button",name="Open H1").click()
                        page.get_by_role("button",name="Open H2").click()
                        page.get_by_role("button",name="Open H3").click()
                        page.locator("#showReconstruct").click()
                        assert page.locator("#reconstructAnswer").is_visible()
                        page.locator("#diagnoseInput").fill("My first divergence.")
                        page.locator("#saveDiagnose").click()
                        page.locator("#repairInput").fill("My revised reasoning.")
                        page.locator("#saveRepair").click()
                        assert page.locator("#showBoundary").is_disabled()
                        page.locator("#boundaryInput").fill("Changed condition reasoning.")
                        page.locator("#saveBoundary").click(); page.locator("#showBoundary").click()
                        assert page.locator("#boundaryAnswer").is_visible()
                        page.reload(); ready(page)
                        assert page.locator("#savedFirst").inner_text()==first
                        current=storage_record(page,ids[0])
                        assert current["first_answer"]==initial["first_answer"]
                        assert len(current["diagnosis_notes"])==len(current["revisions"])==len(current["boundary_attempts"])==1
                        assert {"TEXTBOOK_BEFORE_FIRST","H1","H2","H3","RECONSTRUCT","BOUNDARY_MODEL"} <= {x["kind"] for x in current["help_exposure"]}
                        assert current["mastery_status"]=="UNASSESSED"
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1")
                        page.screenshot(path=str(OUT/f"{m}-core1b-{w}x{h}.png"),full_page=True)
                        receipt["tests"].append({"unit":m,"viewport":f"{w}x{h}","three_instances":True,"status":"PASS"})
                    page.goto(origin+"/"+routes["integrated_main"]["path"]);ready(page)
                    assert set(page.locator("#cycleSelect option").evaluate_all("(xs)=>xs.map(x=>x.value)"))==set(routes["integrated_main"]["cycle_ids"])
                    for cid in routes["integrated_main"]["cycle_ids"]:
                        page.locator("#cycleSelect").select_option(cid)
                        assert page.locator("#postAttempt").is_hidden()
                        page.locator("#predictInput").fill("Initial chapter synthesis prediction.")
                        page.locator("#attemptInput").fill("First chapter synthesis reasoning.")
                        page.locator("#saveFirst").click()
                        assert page.locator("#saveFirst").is_disabled()
                        page.locator("#showReconstruct").click()
                        assert page.locator("#reconstructAnswer").is_visible()
                        assert page.locator("#showBoundary").is_disabled()
                    assert not errors,errors
                    receipt["tests"].append({"unit":"MAIN","viewport":f"{w}x{h}","three_main_only":True,"status":"PASS"})
                    ctx.close()
                ctx=browser.new_context(); page=ctx.new_page()
                page.goto(origin+BASE+"core1/ph01-m04-r32/index.html");ready(page)
                page.evaluate("()=>localStorage.setItem('G9V41:PH01:R32:old:PH01-M04-QRT-MODEL-D3-INSTANCE-R32',JSON.stringify({first_answer:{answer:'stale'}}))")
                page.reload();ready(page)
                assert page.locator("#postAttempt").is_hidden()
                ctx.close()
                ctx=browser.new_context();ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Blocked','SecurityError')}})")
                page=ctx.new_page();page.goto(origin+BASE+"core1/ph01-m08-r32/index.html")
                page.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Storage unavailable')")
                assert page.locator("#saveFirst").is_disabled() and page.locator("#postAttempt").is_hidden()
                ctx.close()
                receipt["tests"].append({"unit":"R32","stale_revision_ignored":True,"blocked_storage_fail_closed":True,"status":"PASS"})
            finally: browser.close()
    finally: server.terminate();server.wait(timeout=5)
    (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(receipt,indent=2))
if __name__=="__main__": main()

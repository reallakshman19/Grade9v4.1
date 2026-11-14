#!/usr/bin/env python3
"""R00 P1: full R4.4 and R4.5 MAIN journeys, five replacement INSTANCE journeys, stale revisions and failed writes."""
import hashlib,json,subprocess,sys,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from physics_ph01_r31_core1b_browser_qa import free_port
ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics/curriculum/agent1/PH01/"
def ready(page):page.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Candidate task loaded')")
def digest(rev):
    a=(PH/f"physics-topic-package.v1_1.r4_{rev}.json").read_bytes()
    b=(PH/f"ph01-core1b-support.r4_{rev}.json").read_bytes()
    return hashlib.sha256(a+b"\n"+b).hexdigest()
def storage_key(rev,cid):return f"G9V41:PH01:R4{rev}:{digest(rev)}:{cid}"
def record(page,key):return page.evaluate("(k)=>JSON.parse(localStorage.getItem(k))",key)
def load(page,url,cid):
    page.goto(url+"?cycle="+cid);ready(page)
    assert page.locator("#cycleSelect").input_value()==cid
def journey(page,url,cid,rev,w,prehelp=False):
    key=storage_key(rev,cid)
    load(page,url,cid)
    assert page.locator("#postAttempt").is_hidden()
    if prehelp:
        page.locator("#textbookLink").click()
        page.wait_for_url("**/textbook/PH01/index.html")
        page.go_back(wait_until="load");ready(page)
        assert page.locator("#cycleSelect").input_value()==cid
        pre=record(page,key)
        assert pre["first_answer"] is None
        assert [x["kind"] for x in pre["help_exposure"]]==["TEXTBOOK_BEFORE_FIRST"]
    page.locator("#predictInput").fill("Independent prediction "+cid)
    page.locator("#attemptInput").fill("Immutable original "+cid)
    if w==1000:page.locator("#saveFirst").tap()
    else:page.locator("#saveFirst").press("Enter")
    assert page.locator("#saveFirst").is_disabled() and page.locator("#attemptInput").is_disabled()
    first=record(page,key)["first_answer"]
    assert first["answer"]=="Immutable original "+cid
    if prehelp:assert "TEXTBOOK_BEFORE_FIRST" in [x["kind"] for x in record(page,key)["help_exposure"]]
    assert page.get_by_role("button",name="Open H2").is_disabled()
    assert page.get_by_role("button",name="Open H3").is_disabled()
    for hint in ("H1","H2","H3"):
        button=page.get_by_role("button",name="Open "+hint);assert button.is_enabled();button.click()
        assert hint+" ·" in page.locator("#hintsOpened").inner_text()
    assert page.locator("#reconstructAnswer").is_hidden()
    page.locator("#showReconstruct").click();assert page.locator("#reconstructAnswer").is_visible()
    page.locator("#diagnoseInput").fill("I identified the first mistaken condition.")
    page.locator("#saveDiagnose").click()
    page.locator("#repairInput").fill("I rebuilt the warrant with the right condition.")
    page.locator("#saveRepair").click()
    assert page.locator("#showBoundary").is_disabled() and page.locator("#boundaryAnswer").is_hidden()
    page.locator("#boundaryInput").fill("My changed-condition answer "+cid)
    page.locator("#saveBoundary").click()
    before=record(page,key)
    assert len(before["boundary_attempts"])==1
    assert "BOUNDARY_MODEL" not in before["boundary_attempts"][0]["exposed_before_attempt"]
    assert page.locator("#showBoundary").is_enabled()
    page.locator("#showBoundary").click();assert page.locator("#boundaryAnswer").is_visible()
    saved=record(page,key)
    expected={"H1","H2","H3","RECONSTRUCT","BOUNDARY_MODEL"}
    if prehelp:expected.add("TEXTBOOK_BEFORE_FIRST")
    assert {x["kind"] for x in saved["help_exposure"]}==expected
    assert saved["first_answer"]==first and saved["mastery_status"]=="UNASSESSED"
    assert len(saved["diagnosis_notes"])==1 and saved["diagnosis_notes"][0]["kind"]=="LEARNER_SELF_REPORT_NOT_DIAGNOSIS"
    assert len(saved["revisions"])==1 and saved["revisions"][0]["helped"]
    page.reload();ready(page)
    assert page.locator("#cycleSelect").input_value()==cid
    assert page.locator("#saveFirst").is_disabled() and page.locator("#reconstructAnswer").is_visible() and page.locator("#boundaryAnswer").is_visible()
    assert record(page,key)==saved
    if prehelp:
        page.locator("#textbookLink").click();page.wait_for_url("**/textbook/PH01/index.html")
        page.go_back(wait_until="load");ready(page)
        after=record(page,key)
        assert after["first_answer"]==first and "TEXTBOOK_AFTER_FIRST" in [x["kind"] for x in after["help_exposure"]]
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
    return record(page,key)
def blocked(browser,url,cid,w,h,rev):
    ctx=browser.new_context(viewport={"width":w,"height":h})
    ctx.add_init_script("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new DOMException('Blocked','SecurityError')}})")
    pg=ctx.new_page();pg.goto(url+"?cycle="+cid)
    pg.wait_for_function("document.querySelector('#runtimeStatus').textContent.includes('Storage unavailable')")
    assert pg.locator("#saveFirst").is_disabled() and pg.locator("#postAttempt").is_hidden()
    assert pg.locator("#attemptInput").is_enabled()
    pg.locator("#attemptInput").fill("Copyable unsaved work")
    assert pg.locator("#attemptInput").input_value()=="Copyable unsaved work"
    ctx.close()
def fail_mid(browser,url,cid,w,h,rev):
    key=storage_key(rev,cid);ctx=browser.new_context(viewport={"width":w,"height":h})
    pg=ctx.new_page();load(pg,url,cid)
    pg.locator("#predictInput").fill("Predict");pg.locator("#attemptInput").fill("First write fails")
    pg.evaluate("()=>{window.originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new DOMException('quota','QuotaExceededError')}}")
    pg.locator("#saveFirst").click()
    assert pg.locator("#postAttempt").is_hidden() and record(pg,key) is None
    assert pg.locator("#attemptInput").input_value()=="First write fails"
    if rev==5:assert pg.locator("#saveFirst").is_disabled()
    pg.reload();ready(pg)
    pg.locator("#predictInput").fill("Predict");pg.locator("#attemptInput").fill("Persisted before failure");pg.locator("#saveFirst").click()
    first=record(pg,key)
    pg.evaluate("()=>{Storage.prototype.setItem=function(){throw new DOMException('quota','QuotaExceededError')}}")
    pg.get_by_role("button",name="Open H1").click()
    assert "Hints remain closed" in pg.locator("#hintsOpened").inner_text()
    assert pg.locator("#reconstructAnswer").is_hidden() and pg.locator("#boundaryAnswer").is_hidden()
    assert record(pg,key)==first
    if rev==5:
        assert pg.get_by_role("button",name="Open H1").is_disabled()
        for ident in ("#showReconstruct","#saveDiagnose","#saveRepair","#saveBoundary","#showBoundary"):assert pg.locator(ident).is_disabled()
    ctx.close()
def main():
    routes=json.loads((PH/"ph01-subtopic-routes.r4_5.json").read_text())
    pack=json.loads((PH/"physics-topic-package.v1_1.r4_5.json").read_text())
    port=free_port();origin=f"http://127.0.0.1:{port}"
    server=subprocess.Popen([sys.executable,"-m","http.server",str(port),"--bind","127.0.0.1","--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:urllib.request.urlopen(origin+"/nsejs/physics/textbook/PH01/core2-links-r45/index.html",timeout=1).close();break
            except Exception:time.sleep(.1)
        else:raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for w,h in ((1000,1600),(1600,1000)):
                ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                pg=ctx.new_page()
                main4=origin+"/nsejs/physics/core1/ph01-main-r44/index.html"
                main5=origin+"/"+routes["integrated_main"]["path"]
                # Exercise the exact previously selector-only tasks as well as the corrected replacement tasks.
                for cell in ("D3.2","D4.7"):
                    old="PH01-MAIN-"+cell+"-R44";new=old.replace("R44","R45")
                    old_record=journey(pg,main4,old,4,w,True)
                    load(pg,main5,new)
                    assert pg.locator("#postAttempt").is_hidden() and record(pg,storage_key(5,new)) is None
                    # Old content in the CURRENT key must fail the revision check.
                    pg.evaluate("([key,value])=>localStorage.setItem(key,JSON.stringify(value))",[storage_key(5,new),old_record])
                    pg.reload();ready(pg)
                    assert pg.locator("#postAttempt").is_hidden() and pg.locator("#saveFirst").is_enabled()
                    pg.evaluate("(k)=>localStorage.removeItem(k)",storage_key(5,new))
                    journey(pg,main5,new,5,w,True)
                    assert record(pg,storage_key(4,old))==old_record
                    for rev,url,cid in ((4,main4,old),(5,main5,new)):
                        blocked(browser,url,cid,w,h,rev);fail_mid(browser,url,cid,w,h,rev)
                for u in routes["units"]:
                    m=u["subtopic_id"][-3:]
                    pg.goto(origin+"/"+u["core1a"])
                    pg.get_by_role("link",name=f"Open {m} R4.5 · D3/D4 practice").click();ready(pg)
                    assert set(pg.locator("#cycleSelect option").evaluate_all("(xs)=>xs.map(x=>x.value)"))==set(u["instance_ids"])
                    for c in [c for c in pack["core1b"] if c["id"] in u["instance_ids"] and c["id"].endswith("R45-INSTANCE")]:
                        journey(pg,origin+"/"+u["core1b"],c["id"],5,w)
                pg.goto(origin+"/nsejs/physics/index.html?topic=mechanics#question-NSEJS-24-MECH-03")
                pg.locator("#question-NSEJS-24-MECH-03 [data-ph01-r45-link]").click()
                pg.wait_for_url("**/core2-links-r45/index.html#PH01-LINK-2024-51-Q37")
                panel=pg.locator("#PH01-LINK-2024-51-Q37");panel.locator("summary").click()
                panel.locator("a[href*='PH01-M08-QRT-EXPLAIN-D3-R45-INSTANCE']").click();ready(pg)
                assert pg.locator("#cycleSelect").input_value()=="PH01-M08-QRT-EXPLAIN-D3-R45-INSTANCE"
                pg.locator("#core2-return a").click();pg.wait_for_url("**/core2-links-r45/index.html#PH01-LINK-2024-51-Q37")
                ctx.close()
            browser.close()
        print("PH01 R4.5 PASS: exact R44 and R45 MAIN full journeys x2 orientations, five replacement INSTANCE journeys x2, pre/post help, stale revision, blocked and quota writes, source return; academic HOLD")
    finally:server.terminate();server.wait(timeout=5)
if __name__=="__main__":main()

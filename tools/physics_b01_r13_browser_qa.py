#!/usr/bin/env python3
"""B01 takeover: 39 author routes + 89 exact-pin INSTANCE loader and sequence, HTTP Chromium.

This is localStorage behavioral QA only, NOT secure exam/academic/mastery acceptance.
"""
from __future__ import annotations
import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"review-artifacts/physics-b01-r13"
URL="/nsejs/physics/curriculum/topics/PH07/b01/learner-preview/index.html"
REG=ROOT/"nsejs/physics/curriculum/topics/PH07/b01/B01_INTEGRATED_CURRICULUM_PROPOSAL.v1.json"
CASES=(
    ("primary-calibration","PH07-01-B01-INSTANCE-MODEL-R2", "PRIMARY"),
    ("primary-reverberation","PH08-09-B01-INSTANCE-EXPLAIN-R2", "PRIMARY"),
    ("supplement-calibration","PH07-01-B01-NSEJS-2019-51-Q64-D3-MODEL-R1-INSTANCE", "SUPPLEMENTAL"),
)

def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1",0))
        return s.getsockname()[1]

def ready(pg):
    try:
        pg.wait_for_function("""() => { const s=document.querySelector('#status').textContent; return s.includes('Exact-version author candidate loaded') || s.includes('Fail closed'); }""",timeout=18000)
    except Exception as exc:
        message=pg.locator("#status").inner_text()
        script=pg.evaluate("""() => [...document.scripts].map(s=>({src:s.src,loaded:!!s.src}))""")
        raise AssertionError("B01 did not initialize: status="+message+" scripts="+str(script)+" readyState="+pg.evaluate("document.readyState")) from exc
    message=pg.locator("#status").inner_text()
    assert "Exact-version author candidate loaded" in message, "B01 loader failure: "+message

def state(pg):
    return pg.evaluate("""() => {
      const keys=Object.keys(localStorage).filter(k=>k.startsWith('g9-b01-r1:')&&!k.endsWith(':probe'));
      const k=keys.find(x=>localStorage.getItem(x)?.includes('"first_answer"'));
      return {key:k||null,record:k?JSON.parse(localStorage.getItem(k)):null};
    }""")

def all_routes(origin):
    p=json.loads(REG.read_text())
    paths=set()
    for g in p["groups"]:
        for entry in g["base_instances"]:
            a=entry["package_path"].replace("physics-topic-package.v1.json","core1a.html")
            b=entry["package_path"].replace("physics-topic-package.v1.json","core1b.html")
            paths.update([a,b])
    for e in p["supplements"]:
        paths.update([e["core1a"],e["core1b"]])
    assert len(paths)==78
    for path in paths:
        with urllib.request.urlopen(origin+"/"+path,timeout=4) as response:
            assert response.status==200,path
            assert "<html" in response.read(512).decode("utf-8",errors="ignore"),path
    return len(paths)

def journey(browser,origin,orientation,w,h,name,cid,kind):
    context=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
    pg=context.new_page()
    js_errors=[]
    pg.on("pageerror",lambda err:js_errors.append(str(err)))
    try:
        pg.goto(origin+URL+"?task="+cid,wait_until="load")
        ready(pg)
        assert pg.locator("#task-select option").count()==89
        assert pg.locator("#task-select").input_value()==cid
        assert kind in pg.locator("#task-meta").inner_text()
        assert pg.locator("#after-first").is_hidden()
        assert pg.locator("#h2").is_disabled() and pg.locator("#h3").is_disabled()
        assert pg.locator("#reconstruct-model").is_hidden()
        assert len(pg.locator("#revision").inner_text().split("SHA-256 "))==2
        pg.locator("#predict-input").fill("I predict the model may need checking: "+cid)
        pg.locator("#attempt-input").fill("I will distinguish physical constraints from an unverified shortcut: "+cid)
        pg.locator("#h1").click()
        assert pg.locator("#h2").is_enabled()
        pg.locator("#h2").click()
        assert pg.locator("#h3").is_enabled()
        pg.locator("#h3").click()
        assert pg.locator("#after-first").is_hidden()
        if w==1000:pg.locator("#save-first").tap()
        else:pg.locator("#save-first").press("Enter")
        assert pg.locator("#after-first").is_visible()
        assert pg.locator("#attempt-input").is_disabled()
        old=state(pg)["record"]["first_answer"]
        assert old["answer"].endswith(cid)
        assert pg.locator("#reconstruct-model").is_hidden()
        pg.locator("#reveal").click()
        assert pg.locator("#reconstruct-model").is_visible()
        assert pg.locator("#diagnosis-stage").is_visible()
        assert pg.locator("#repair-stage").is_hidden()
        pg.locator("#diagnose-input").fill("Mistake: did not check if physical conditions held.")
        pg.locator("#save-diagnosis").click()
        assert pg.locator("#repair-stage").is_visible()
        pg.locator("#repair-input").fill("Repair: establish measured constraints, then evaluate model sensitivity.")
        pg.locator("#save-repair").click()
        assert pg.locator("#boundary-stage").is_visible()
        assert pg.locator("#show-boundary").is_disabled()
        pg.locator("#boundary-input").fill("Boundary: assumptions changed; determine whether conclusion survives.")
        pg.locator("#save-boundary").click()
        assert pg.locator("#show-boundary").is_enabled()
        pg.locator("#show-boundary").click()
        assert pg.locator("#boundary-model").is_visible()
        snap=state(pg)["record"]
        assert snap["first_answer"]==old
        assert [x["kind"] for x in snap["help_exposure"]]==["H1","H2","H3","RECONSTRUCT","BOUNDARY_MODEL"]
        assert len(snap["diagnosis_notes"])==len(snap["repairs"])==len(snap["boundary_attempts"])==1
        assert snap["mastery_status"]=="UNASSESSED"
        assert snap["boundary_attempts"][0]["exposed_before_attempt"][-1]=="RECONSTRUCT"
        assert "BOUNDARY_MODEL" not in snap["boundary_attempts"][0]["exposed_before_attempt"]
        pg.reload()
        ready(pg)
        assert pg.locator("#task-select").input_value()==cid
        assert pg.locator("#reconstruct-model").is_visible()
        assert pg.locator("#boundary-model").is_visible()
        assert state(pg)["record"]==snap
        # Return to authored teaching and restore the unchanged first response.
        pg.locator("#core1a-link").click()
        assert "/core1a.html" in pg.url
        pg.go_back()
        ready(pg)
        assert state(pg)["record"]["first_answer"]==old
        assert pg.evaluate("document.documentElement.scrollWidth <= innerWidth+1")
        # Corrupt the selected content-revision-bound record: no silent answer reset.
        key=state(pg)["key"]
        pg.evaluate("(k)=>localStorage.setItem(k,'{corrupt')",key)
        pg.reload()
        pg.wait_for_function("document.querySelector('#status').textContent.includes('Fail closed')")
        assert pg.locator("#task-select").is_disabled()
        assert pg.locator("#learner").is_hidden()
        assert not js_errors,js_errors
        return {"case":name,"orientation":orientation,"kind":kind,"first_immutable":True,
                "stages":"PASS","source_return":"PASS","corrupt_state_lockout":"PASS"}
    finally:context.close()

def storage_blocked(browser,origin,w,h):
    ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
    ctx.add_init_script("""Object.defineProperty(window,'localStorage',{
      configurable:true,get(){throw new DOMException('Blocked','SecurityError')}
    })""")
    pg=ctx.new_page()
    try:
        pg.goto(origin+URL)
        pg.wait_for_function("document.querySelector('#status').textContent.includes('Fail closed')")
        assert pg.locator("#task-select").is_disabled()
        assert pg.locator("#learner").is_hidden()
    finally:ctx.close()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    port=free_port()
    origin="http://127.0.0.1:"+str(port)
    server=subprocess.Popen([sys.executable,"-m","http.server",str(port),"--bind","127.0.0.1",
                             "--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            if server.poll() is not None:raise RuntimeError("HTTP server exited")
            try:
                urllib.request.urlopen(origin+URL,timeout=1).close()
                break
            except Exception:time.sleep(.1)
        else:raise RuntimeError("HTTP server unavailable")
        receipt={"task":"B01_R13_AUTHOR_EXPOSED_TABLET_WORKBENCH",
                 "academic_status":"HOLD","source_qualification":"HOLD",
                 "p00_integration":"NOT_ACCEPTED","mastery":"UNASSESSED",
                 "candidate_routes":89,"canonical_mains":0,
                 "author_html_routes_checked":all_routes(origin),"journeys":[]}
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            for orientation,(w,h) in (("portrait",(1000,1600)),("landscape",(1600,1000))):
                for name,cid,kind in CASES:
                    receipt["journeys"].append(journey(browser,origin,orientation,w,h,name,cid,kind))
                storage_blocked(browser,origin,w,h)
            browser.close()
        receipt["status"]="PASS"
        (OUT/"b01-r13-learner-preview-chromium.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print("B01 R13 HTTP CHROMIUM PASS: 78 standalone author HTML routes; 89 revision-pinned INSTANCE candidates; six full first-attempt/reconstruction/diagnosis/repair/boundary journeys x2 orientations, source returns, corrupted and blocked storage; ACADEMIC_HOLD")
    finally:
        server.terminate();server.wait(timeout=5)

if __name__=="__main__":main()

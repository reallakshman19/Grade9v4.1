#!/usr/bin/env python3
"""P00 B01 bridge acceptance evidence: 25 primary routes and PH09–PH12 regressions.

Scope: source-neutral candidate readers and route integrity. This is not R01
science, canonical-main, hint-quality or exam-custody acceptance.
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
OUT=ROOT/"review-artifacts/physics-b01-r15-p00"
REG=ROOT/"nsejs/physics/curriculum/topics/PH07/b01/B01_INTEGRATED_CURRICULUM_PROPOSAL.v1.json"
BASE="/nsejs/physics/curriculum/topics"

def port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1",0))
        return sock.getsockname()[1]

def load_readable(page):
    page.wait_for_function("""() => {
        const s=document.querySelector('#status');
        return s && (s.textContent.includes('Exact-version author candidate loaded') ||
                     s.textContent.includes('Previous first answer restored'));
    }""",timeout=25000)
    assert page.locator("#task-select option").count()==89
    assert page.locator("#after-first").is_hidden()

def route_cases():
    reg=json.loads(REG.read_text())
    keys=set()
    for g in reg["groups"]:
        for e in g["base_instances"]:
            keys.add(e["subtopic_id"])
    assert len(keys)==25
    assert len([x for x in keys if x.startswith("PH07")])==12
    assert len([x for x in keys if x.startswith("PH08")])==13
    return sorted(keys)

def regression(page,topic,origin):
    page.goto(origin+BASE+"/"+topic+"/core1b-preview.html")
    page.wait_for_function("""() => {
       const s=document.querySelector('#status').textContent;
       return s.includes('Predict and attempt independently') ||
              s.includes('Saved first attempt restored');
    }""",timeout=16000)
    assert page.locator("main[data-agent2-core1b]").count()==1
    assert topic in page.url
    assert page.locator("#task-select option").count()==12
    assert page.locator("#reveal").is_disabled()
    page.locator("#first-predict").fill("Qualitative model before formula.")
    page.locator("#first-attempt").fill("Check assumptions, units and limiting case.")
    page.locator("#first-save").click()
    assert page.locator("#reveal").is_enabled()
    page.reload()
    page.wait_for_function(
      "document.querySelector('#status').textContent.includes('Saved first attempt restored')",
      timeout=16000)
    assert page.locator("#first-attempt").input_value()=="Check assumptions, units and limiting case."
    assert page.locator("#first-attempt").is_disabled()
    assert page.locator("#revealed").is_hidden()
    return {"topic":topic,"status":"PASS","legacy_runtime":"UNMODIFIED_STATE_MACHINE"}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    server_port=port()
    origin="http://127.0.0.1:"+str(server_port)
    server=subprocess.Popen([sys.executable,"-m","http.server",str(server_port),
        "--bind","127.0.0.1","--directory",str(ROOT)],
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    receipt={"task":"B01_P00_R15_CANDIDATE_ROUTE_COMPATIBILITY",
             "academic_status":"HOLD","P00_independent_reviewer":"NOT_ASSIGNED",
             "R01":"HOLD","canonical_mains":0,"core1b_legacy_paths":25,
             "candidate_instances":89,"source_admissions":0,"cases":[]}
    try:
        for _ in range(80):
            if server.poll() is not None:raise RuntimeError("Server stopped")
            try:
                urllib.request.urlopen(origin+BASE+"/PH09/core1b-preview.html",timeout=1).close()
                break
            except Exception:time.sleep(.1)
        else:raise RuntimeError("HTTP not ready")
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for orientation,w,h in (("portrait",1000,1600),("landscape",1600,1000)):
                    context=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                    page=context.new_page()
                    errors=[]
                    page.on("pageerror",lambda e:errors.append(str(e)))
                    try:
                        for subtopic in route_cases():
                            parent=subtopic[:4]
                            path=f"{BASE}/{parent}/b01/{subtopic}/core1b.html"
                            page.goto(origin+path,wait_until="domcontentloaded")
                            page.wait_for_url("**/learner-preview/index.html?subtopic="+subtopic,
                                              timeout=25000)
                            load_readable(page)
                            assert subtopic in page.locator("#task-meta").inner_text()
                            assert page.locator("#original-core1b-link").get_attribute("href").endswith(
                              "/core1b.html?legacy=1")
                            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
                            receipt["cases"].append({"case":"B01_PRIMARY_ROUTE_TO_R14",
                                "orientation":orientation,"subtopic":subtopic,"status":"PASS"})
                        legacy=BASE+"/PH07/b01/PH07-01/core1b.html?legacy=1"
                        page.goto(origin+legacy)
                        page.wait_for_function(
                            "document.querySelector('#task-select').options.length>0",timeout=16000)
                        assert "legacy=1" in page.url and "learner-preview" not in page.url
                        assert page.locator("main[data-agent2-core1b]").count()==1
                        receipt["cases"].append({"case":"B01_ORIGINAL_READER_OPT_IN_LEGACY",
                                                  "orientation":orientation,"status":"PASS"})
                        # PH09-PH12 must continue to load and retain prior in-app first attempts.
                        for topic in ["PH09","PH10","PH11","PH12"]:
                            new=browser.new_context(viewport={"width":w,"height":h})
                            other=new.new_page()
                            try:
                                result=regression(other,topic,origin)
                                result["orientation"]=orientation
                                result["case"]="AGENT2_SHARED_RUNTIME_REGRESSION"
                                receipt["cases"].append(result)
                            finally:new.close()
                        assert not errors,errors
                    finally:context.close()
            finally:browser.close()
        expected=2*(25+1+4)
        assert len(receipt["cases"])==expected
        receipt["status"]="TECHNICAL_BRIDGE_QA_PASS__ACADEMIC_HOLD"
        (OUT/"p00-r15-compatibility.json").write_text(
            json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"status":receipt["status"],"cases":len(receipt["cases"]),
                          "PH07_PH08_routes":50,"PH09_PH12_regression":8,
                          "legacy_reader":2,"P00":"INDEPENDENT_ACCEPTANCE_HOLD"},indent=2))
    finally:
        server.terminate()
        server.wait(timeout=5)

if __name__=="__main__":main()

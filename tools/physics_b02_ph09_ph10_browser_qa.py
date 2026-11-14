#!/usr/bin/env python3
"""PH09/PH10 B02 29 native pairs under real 12.7-inch HTTP Chromium.

Engineering QA only; R01 scientific source, R02 blind QRT, B1-B7 and academic
release remain HOLD. Browser localStorage is not a secure exam custody system.
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
OUT=ROOT/"review-artifacts"/"physics-b02-ph09-ph10"
BASE="/nsejs/physics/curriculum/topics"

def spare_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1",0))
        return sock.getsockname()[1]

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    port=spare_port()
    origin=f"http://127.0.0.1:{port}"
    process=subprocess.Popen([sys.executable,"-m","http.server",str(port),
           "--bind","127.0.0.1","--directory",str(ROOT)],
           stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    receipt={"mode":"AUTHOR_EXPOSED_ENGINEERING_BROWSER_QA",
             "release":"HOLD","r01":"HOLD","r02":"HOLD",
             "original_exam_admissions":0,"cases":[]}
    try:
        for _ in range(100):
            if process.poll() is not None:
                raise RuntimeError("HTTP server ended")
            try:
                urllib.request.urlopen(origin+BASE+"/PH09/subtopics/index.html",timeout=1).close()
                break
            except Exception:
                time.sleep(.1)
        else:
            raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for orientation,w,h in (("portrait",1000,1600),("landscape",1600,1000)):
                    context=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                    page=context.new_page()
                    js_errors=[]
                    page.on("pageerror",lambda err:js_errors.append(str(err)))
                    try:
                        for unit,count in (("PH09",12),("PH10",17)):
                            for n in range(1,count+1):
                                sid=f"{unit}-{n:02d}"
                                # One isolated localStorage namespace per new context/route.
                                page.goto(origin+f"{BASE}/{unit}/subtopics/{sid}/core1b.html",
                                          wait_until="domcontentloaded")
                                page.wait_for_function("""() => {
                                   const x=document.querySelector('#status');
                                   return x && (x.textContent.includes('Predict and attempt independently')
                                    || x.textContent.includes('Saved first attempt restored'));
                                }""", timeout=25000)
                                assert page.locator("main[data-agent2-core1b]").count()==1,sid
                                assert page.locator("#task-select option").count()>=1,sid
                                assert page.locator("#revealed").is_hidden(),sid
                                assert page.locator("#reveal").is_disabled(),sid
                                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1"),sid
                                answer=f"First independent reasoning for {sid}: state assumptions and units."
                                page.locator("#first-predict").fill(f"Prediction for {sid}, before feedback.")
                                page.locator("#first-attempt").fill(answer)
                                page.locator("#first-save").click()
                                assert page.locator("#reveal").is_enabled(),sid
                                page.reload(wait_until="domcontentloaded")
                                page.wait_for_function("""() => {
                                   const x=document.querySelector('#status');
                                   return x && x.textContent.includes('Saved first attempt restored');
                                }""",timeout=25000)
                                assert page.locator("#first-attempt").input_value()==answer,sid
                                assert page.locator("#first-attempt").is_disabled(),sid
                                assert page.locator("#revealed").is_hidden(),sid
                                receipt["cases"].append({"orientation":orientation,"subtopic":sid,
                                    "status":"PASS","checked":["loaded","first-attempt-gated","refresh","no-feedback-before-reveal","no-overflow"]})
                        assert len(js_errors)==0,js_errors
                    finally:
                        context.close()
            finally:
                browser.close()
        assert len(receipt["cases"])==58, len(receipt["cases"])
        receipt["status"]="PASS"
    except Exception as exc:
        receipt["status"]="FAIL"
        receipt["error"]=repr(exc)
        raise
    finally:
        (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
        process.terminate()
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired: process.kill()

if __name__=="__main__":
    main()

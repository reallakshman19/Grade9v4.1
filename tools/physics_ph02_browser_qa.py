#!/usr/bin/env python3
"""PH02 candidate HTTP Chromium QA (manual run): never certifies academic B1-B7.

Usage: python tools/physics_ph02_browser_qa.py
Requires playwright + installed Chromium. This script is not a CI receipt until run.
"""
from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "review-artifacts/physics-ph02"
PREFIX = "G9V41:PH02:"


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def loaded(page):
    page.wait_for_function(
        "() => ['Candidate task loaded','Candidate cycle loaded'].some(x => document.querySelector('#runtimeStatus')?.textContent.includes(x))"
    )


def state(page, uid):
    return page.evaluate(
        """prefix => {
          const keys = Object.keys(localStorage).filter(k => k.startsWith(prefix));
          const key = keys.find(k => k.includes('AUTHORED-') && !k.endsWith(':prehelp'));
          return key ? JSON.parse(localStorage.getItem(key)) : null;
        }""", f"{PREFIX}AUTHORED-PH02-{uid}-TRANSFER-01:"
    )


def test_one(page, uid):
    url = f"/nsejs/physics/core1/PH02/{uid}/index.html"
    page.goto(page.url.split("/nsejs/")[0] + url, wait_until="load")
    loaded(page)
    assert page.locator("#postAttempt").is_hidden()
    assert page.locator("#hintBtn").is_hidden()
    assert page.locator("#reconstructBtn").is_hidden()
    page.locator("#prediction").fill("My reasoned prediction before support.")
    page.locator("#attempt").fill("Independent signed force model and warrant; this is learner-like test input.")
    page.locator("#firstCommit").click()
    page.wait_for_function("() => !document.querySelector('#postAttempt').hidden")
    old = state(page,uid)
    assert old and old["first_answer"].startswith("Independent signed")
    assert old["revision"] and old["first_prediction"]
    for n in range(1,4):
        page.locator("#hintBtn").click()
        assert page.locator(f"#hint{n}").is_visible()
        assert state(page,uid)["hints_seen"] == n
    page.locator("#reconstructBtn").click()
    assert page.locator("#reconstruction").is_visible()
    page.locator("#diagnosis").fill("Incorrect first model was not isolated; checking the boundary.")
    page.locator("#diagnoseBtn").click()
    page.locator("#repair").fill("Repaired a precise model step with the correct system and sign.")
    page.locator("#repairBtn").click()
    assert page.locator("#boundaryModel").is_hidden()
    page.locator("#boundary").fill("Attempted new condition independently.")
    page.locator("#boundaryBtn").click()
    assert page.locator("#boundaryModel").is_hidden()
    page.locator("#boundaryRevealBtn").click()
    assert page.locator("#boundaryModel").is_visible()
    page.reload()
    loaded(page)
    assert page.locator("#attempt").input_value().startswith("Independent signed")
    assert page.locator("#attempt").is_disabled()
    assert page.locator("#boundaryModel").is_visible()
    assert state(page,uid)["first_answer"] == old["first_answer"]
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth") 
    return {"unit":uid,"first_immutable":True,"hint_order":3,"six_stages":True,"refresh":True}


def main():
    from playwright.sync_api import sync_playwright
    OUTPUT.mkdir(parents=True, exist_ok=True)
    port = free_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
         "--directory", str(ROOT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    receipt={"task":"PH02_AUTHORED_CHROMIUM_R1","source_status":"HOLD",
             "academic_status":"HOLD","disposition":"NOT_YET_VERIFIED","checks":[]}
    try:
        target=f"http://127.0.0.1:{port}/nsejs/physics/core1/PH02/F01/index.html"
        for _ in range(50):
            try:
                urllib.request.urlopen(target,timeout=1).close()
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise RuntimeError("HTTP server failed")
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for orientation,w,h in (("portrait",1000,1600),("landscape",1600,1000)):
                    context=browser.new_context(viewport={"width":w,"height":h},
                                                has_touch=True,device_scale_factor=1)
                    page=context.new_page()
                    page.on("pageerror",lambda error:receipt["checks"].append(
                        {"error":str(error),"orientation":orientation}))
                    for number in range(1,9):
                        uid=f"F{number:02d}"
                        page.goto(f"http://127.0.0.1:{port}/nsejs/physics/textbook/PH02/{uid}/index.html")
                        page.wait_for_selector("h2")
                        assert page.locator("h2").count() >= 9
                        assert page.locator("svg[role=img]").count() == 1
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                        result=test_one(page,uid)
                        receipt["checks"].append({"orientation":orientation,**result})
                    context.close()
                context=browser.new_context()
                page=context.new_page()
                page.goto(target)
                page.wait_for_selector("#firstCommit")
                page.locator("#prediction").fill("Prediction under storage denial")
                page.locator("#attempt").fill("Independent response under storage denial")
                page.evaluate("""() => {
                  const original=Storage.prototype.setItem;
                  Storage.prototype.setItem=function(){throw Error('QA injected denied write')};
                  window.__originalSetItem=original;
                }""")
                page.locator("#firstCommit").click()
                assert page.locator("#postAttempt").is_hidden()
                assert page.locator("#runtimeStatus").inner_text().startswith("HOLD:")
                receipt["checks"].append({"negative":"SAVE_FAILURE","result":"REJECTED","first_input_copyable":True})
                context.close()
            finally:
                browser.close()
        receipt["disposition"]="MECHANICAL_CHROMIUM_PASS__ACADEMIC_HOLD"
    except Exception as error:
        receipt["disposition"]="FAIL_CLOSED"
        receipt["error"]=repr(error)
        raise
    finally:
        server.terminate()
        try: server.wait(timeout=5)
        except subprocess.TimeoutExpired: server.kill()
        (OUTPUT/"PH02_BROWSER_QA_R1.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"disposition":receipt["disposition"],"checks":len(receipt["checks"])},indent=2))


if __name__=="__main__":
    main()

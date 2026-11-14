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
        "() => ['Candidate task loaded','Candidate cycle loaded'].some(x => document.querySelector('#runtimeStatus')?.textContent.includes(x))", timeout=8000
    )


def state(page, task_uid):
    return page.evaluate(
        """prefix => {
          const keys = Object.keys(localStorage).filter(k => k.startsWith(prefix));
          const key = keys.find(k => k.includes('AUTHORED-') && !k.endsWith(':prehelp'));
          return key ? JSON.parse(localStorage.getItem(key)) : null;
        }""", f"{PREFIX}{task_uid}:"
    )


def test_one(page, uid, task_uid=None, main=False):
    task_uid = task_uid or f"AUTHORED-PH02-{uid}-TRANSFER-01"
    url = f"/nsejs/physics/core1/PH02/{'main' if main else uid}/index.html"
    if main or task_uid != f"AUTHORED-PH02-{uid}-TRANSFER-01":
        url += f"?task={task_uid}"
    print("PH02_BROWSER_START", task_uid, "main", main, flush=True)
    page.goto(page.url.split("/nsejs/")[0] + url, wait_until="load", timeout=12000)
    loaded(page)
    assert page.locator("#postAttempt").is_hidden()
    assert page.locator("#hintBtn").is_hidden()
    assert page.locator("#reconstructBtn").is_hidden()
    assert page.locator("#reconstruction").inner_text() == ""  # HINT_LEAK negative DOM control
    assert page.locator("#boundaryModel").inner_text() == ""
    assert "Reviewed" not in page.locator("body").inner_text()
    page.locator("#prediction").fill("My reasoned prediction before support.")
    page.locator("#attempt").fill("Independent signed force model and warrant; this is learner-like test input.")
    page.locator("#firstCommit").click()
    page.wait_for_function("() => !document.querySelector('#postAttempt').hidden", timeout=8000)
    old = state(page,task_uid)
    assert old and old["first_answer"].startswith("Independent signed")
    assert old["revision"] and old["first_prediction"]
    for n in range(1,4):
        page.locator("#hintBtn").click()
        assert page.locator(f"#hint{n}").is_visible()
        assert state(page,task_uid)["hints_seen"] == n
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
    assert state(page,task_uid)["first_answer"] == old["first_answer"]
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth") 
    print("PH02_BROWSER_PASS", task_uid, flush=True)
    return {"unit":uid,"task_uid":task_uid,"main":main,"first_immutable":True,"hint_order":3,"six_stages":True,"refresh":True}


def main():
    from playwright.sync_api import sync_playwright
    OUTPUT.mkdir(parents=True, exist_ok=True)
    port = free_port()
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
         "--directory", str(ROOT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    receipt={"task":"PH02_AUTHORED_CHROMIUM_R2_FULL_30_CYCLES","source_status":"HOLD",
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
                    # Eight textbooks, 24 distinct INSTANCE tasks and six integrated MAIN.
                    qrt=json.loads((ROOT/"nsejs/physics/ph02/qrt-candidates.v1.json").read_text())
                    base=json.loads((ROOT/"nsejs/physics/ph02/units.v1.json").read_text())
                    for number in range(1,9):
                        uid=f"F{number:02d}"
                        page.goto(f"http://127.0.0.1:{port}/nsejs/physics/textbook/PH02/{uid}/index.html")
                        page.wait_for_selector("#additional-constructions", timeout=10000)
                        assert page.locator("#additional-constructions .example").count()==2
                        assert page.locator("h2").count() >= 10
                        assert page.locator("svg[role=img]").count() == 1
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                        result=test_one(page,uid)
                        receipt["checks"].append({"orientation":orientation,**result})
                    for t in qrt["tasks"]:
                        result=test_one(page,t["unit"].split("-")[-1],t["uid"])
                        receipt["checks"].append({"orientation":orientation,**result})
                    for m in qrt["main_cycles"]:
                        result=test_one(page,m["unit"].split("-")[-1],m["uid"],main=True)
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
                stale_context=browser.new_context()
                stale=stale_context.new_page()
                stale.goto(target)
                loaded(stale)
                stale.locator("#prediction").fill("First prediction before revision change.")
                stale.locator("#attempt").fill("Saved first response before a test-only revision mutation.")
                stale.locator("#firstCommit").click()
                original=state(stale,"AUTHORED-PH02-F01-TRANSFER-01")
                assert original and original["first_answer"]
                stale.evaluate("""() => {
                    const k=Object.keys(localStorage).find(x=>x.startsWith('G9V41:PH02:AUTHORED-PH02-F01-TRANSFER-01:') && !x.endsWith(':prehelp'));
                    const v=JSON.parse(localStorage.getItem(k));
                    v.revision='QA_MUTATED_STALE_REVISION';
                    localStorage.setItem(k,JSON.stringify(v));
                }""")
                stale.reload()
                assert stale.locator("#runtimeStatus").inner_text().startswith("HOLD:")
                assert stale.locator("#postAttempt").is_hidden()
                assert stale.locator("#firstCommit").is_disabled()
                receipt["checks"].append({"negative":"STALE_REVISION","result":"REJECTED","original_not_promoted":True})
                stale_context.close()
                wrong_context=browser.new_context()
                wrong=wrong_context.new_page()
                wrong.goto(target+"?task=AUTHORED-FAKE-SOURCE-UID")
                wrong.wait_for_function("() => document.querySelector('[data-ph02-practice]')?.textContent.includes('HOLD')")
                assert wrong.locator("#firstCommit").count()==0
                receipt["checks"].append({"negative":"UNKNOWN_TASK_UID","result":"REJECTED"})
                wrong_context.close()
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

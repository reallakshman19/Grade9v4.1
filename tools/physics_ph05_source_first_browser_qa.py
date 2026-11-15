#!/usr/bin/env python3
"""PH05 source-first official paper checkpoint: HTTP Chromium QA, academic HOLD.

Runs both 12.7-inch tablet orientations, source-first/reload/key confinement,
pre-help storage lock, exposure recording, stale revision and disabled storage.
This is TECHNICAL QA and does not admit original exam/QRT academic claims.
"""
from __future__ import annotations
import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"review-artifacts/physics-ph05-source-first"
IDS=("NSEJS-2022-C51-Q36","NSEJS-2023-C51-Q48")
PREFIX="G9V41:PH05:SOURCE_FIRST:"


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1",0))
        return sock.getsockname()[1]


def record(page, uid):
    return page.evaluate("""prefix => {
        const keys=Object.keys(localStorage).filter(k=>k.startsWith(prefix) && !k.endsWith(':probe'));
        if(keys.length!==1)return null;
        const val=JSON.parse(localStorage.getItem(keys[0]));
        return {key:keys[0],entry:val};
    }""",PREFIX+uid+":")


def load(page,url):
    page.goto(url,wait_until="load")
    page.locator("#firstPrediction").wait_for(timeout=15000)
    assert page.locator("#firstReasoning").is_visible()
    assert page.locator("#afterFirst").is_hidden()
    assert page.locator("iframe").count()==0
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")


def check_orientation(browser,base,orientation,w,h,receipts):
    context=browser.new_context(viewport={"width":w,"height":h},has_touch=True,device_scale_factor=1)
    page=context.new_page()
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    for uid in IDS:
        url=base+"/nsejs/physics/ph05/source-checkpoint.html?source="+uid
        load(page,url)
        assert page.locator("#afterFirst").is_hidden()
        assert page.get_by_text("Original question",exact=False).count()>=1
        official=page.get_by_role("link",name="Open the official IAPT question paper")
        assert official.get_attribute("href").startswith("https://iapt.org.in/")
        assert "solution" not in official.get_attribute("href").lower()
        visible=page.locator("#sourceCheckpoint").inner_text().lower()
        assert "answer: a" not in visible and "answer: d" not in visible
        assert page.get_by_role("link",name="Try protected author-created transfer").count()==0
        page.locator("#firstPrediction").fill("Prediction before learning: compare the physical states.")
        page.locator("#firstReasoning").fill("I will first identify the system boundary, derive a relation, and check dimensions independently.")
        page.get_by_role("button",name="Protect first attempt").click()
        page.wait_for_function("() => document.querySelector('#afterFirst')?.hidden===false",timeout=10000)
        rec=record(page,uid)
        assert rec and rec["entry"]["source_uid"]==uid
        assert rec["entry"]["prediction"].startswith("Prediction before learning")
        assert rec["entry"]["first_reasoning"].startswith("I will first identify")
        assert rec["entry"]["revision"] and len(rec["entry"]["revision"])==64
        assert page.locator("#firstPrediction").is_disabled()
        assert page.locator("#firstReasoning").is_disabled()
        assert page.get_by_role("link",name="Try protected author-created transfer").is_visible()
        # Visiting a teaching link is recorded without altering first attempt.
        page.get_by_role("link",name="Learn Core1A",exact=False).first.click()
        page.wait_for_url("**/textbook/PH05/G*/index.html",timeout=10000)
        page.goto(url,wait_until="load")
        page.locator("#firstPrediction").wait_for(timeout=10000)
        preserved=record(page,uid)
        assert preserved["entry"]["prediction"]==rec["entry"]["prediction"]
        assert preserved["entry"]["first_reasoning"]==rec["entry"]["first_reasoning"]
        assert any(ev["kind"].startswith("core1a_") for ev in preserved["entry"]["exposure"])
        assert page.locator("#firstPrediction").is_disabled()
        assert page.locator("#afterFirst").is_visible()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
        transfer_link=page.get_by_role("link",name="Try protected author-created transfer")
        href=transfer_link.get_attribute("href")
        assert "source="+uid in href and "task=" in href
        transfer_link.click()
        page.locator("#runtimeStatus").wait_for(timeout=12000)
        page.wait_for_function("() => document.querySelector('#runtimeStatus')?.textContent.includes('Candidate task loaded')",timeout=12000)
        assert page.locator("#postAttempt").is_hidden()
        back=page.get_by_role("link",name="Return to original NSEJS source checkpoint")
        assert back.is_visible()
        back.click()
        page.wait_for_url("**/source-checkpoint.html?source="+uid,timeout=12000)
        assert page.locator("#afterFirst").is_visible()
        assert page.locator("#firstPrediction").is_disabled()
        final=record(page,uid)
        assert final["entry"]["first_reasoning"]==rec["entry"]["first_reasoning"]
        assert any(x["kind"]=="core1b_transfer" for x in final["entry"]["exposure"])
        receipts.append({"source":uid,"orientation":orientation,"first_attempt_locked":True,
                         "revision_bound":True,"help_exposure_logged":True,"refresh":True})
        # Each source has its own state. Clear only at test end via new context.
        context.clear_cookies()
    assert not errors,errors
    context.close()


def check_denied_storage(browser,base,receipts):
    ctx=browser.new_context()
    ctx.add_init_script("""{
        const orig=Storage.prototype.setItem;
        Storage.prototype.setItem=function(){throw new Error('QA denied localStorage')};
    }""")
    page=ctx.new_page()
    url=base+"/nsejs/physics/ph05/source-checkpoint.html?source="+IDS[0]
    page.goto(url,wait_until="load")
    page.get_by_text("HOLD",exact=False).first.wait_for(timeout=12000)
    assert page.locator("#afterFirst").count()==0
    assert page.get_by_role("button",name="Protect first attempt").count()==0
    receipts.append({"negative":"storage_denied","fail_closed":True})
    ctx.close()


def check_stale_revision(browser,base,receipts):
    ctx=browser.new_context()
    page=ctx.new_page()
    url=base+"/nsejs/physics/ph05/source-checkpoint.html?source="+IDS[0]
    load(page,url)
    page.locator("#firstPrediction").fill("Initial prediction before any provided help.")
    page.locator("#firstReasoning").fill("A complete independent model with selected system and dimensional check.")
    page.get_by_role("button",name="Protect first attempt").click()
    assert record(page,IDS[0])
    page.evaluate("""prefix => {
        const key=Object.keys(localStorage).find(k=>k.startsWith(prefix) && !k.endsWith(':probe'));
        const x=JSON.parse(localStorage.getItem(key));
        x.revision='STALENESS_INJECTED_BY_QA';
        localStorage.setItem(key,JSON.stringify(x));
    }""",PREFIX)
    page.reload()
    page.get_by_text("HOLD",exact=False).first.wait_for(timeout=12000)
    assert page.locator("#afterFirst").count()==0
    assert page.get_by_role("button",name="Protect first attempt").count()==0
    receipts.append({"negative":"stale_stored_revision","fail_closed":True})
    ctx.close()


def main():
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True,exist_ok=True)
    port=free_port()
    proc=subprocess.Popen([sys.executable,"-m","http.server",str(port),"--bind","127.0.0.1",
            "--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    target=f"http://127.0.0.1:{port}"
    receipt={"test":"PH05_SOURCE_FIRST_HTTP_CHROMIUM_R2",
             "source_status":"HOLD","academic_status":"HOLD","disposition":"INCOMPLETE","cases":[]}
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(target+"/nsejs/physics/ph05/source-checkpoint.html",timeout=1).close()
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise RuntimeError("Local test HTTP server never became ready")
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for orientation,w,h in (("portrait",1000,1600),("landscape",1600,1000)):
                    check_orientation(browser,target,orientation,w,h,receipt["cases"])
                check_denied_storage(browser,target,receipt["cases"])
                check_stale_revision(browser,target,receipt["cases"])
            finally:
                browser.close()
        assert len(receipt["cases"])==6
        receipt["disposition"]="TECHNICAL_PASS__ACADEMIC_HOLD"
        print("PH05_SOURCE_FIRST_BROWSER_PASS",len(receipt["cases"]),flush=True)
    except Exception as err:
        receipt["disposition"]="TECHNICAL_FAIL"
        receipt["error"]=str(err)
        raise
    finally:
        (OUT/"browser-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
        proc.terminate()
        try: proc.wait(timeout=5)
        except subprocess.TimeoutExpired: proc.kill()


if __name__=="__main__":
    main()

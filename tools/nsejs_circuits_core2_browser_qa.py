#!/usr/bin/env python3
"""Circuit Core2 worksheet: HTTP Chromium candidate learner safety regression.

Engineering-only receipt: this does not authenticate exam source, rights, QRT or
independent academic acceptance. Run: python tools/nsejs_circuits_core2_browser_qa.py
"""
from __future__ import annotations

import json
import re
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review-artifacts" / "circuits-core2"
PREFIX = "g9:nsejs:core2:candidate-attempt:v2"


def port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_cards(page, expected):
    page.wait_for_function(
      """expected => document.querySelectorAll('#questions article.card').length === expected ||
        document.getElementById('status')?.classList.contains('error')""",
      arg=expected, timeout=60000)
    error=page.locator("#status.error")
    if error.count():
        raise AssertionError("Circuit reader fail-closed: "+error.inner_text())
    cards=page.locator("#questions article.card")
    assert cards.count()==expected, (cards.count(),expected)
    return cards


def commit_candidate(page, question_id, option="B"):
    card=page.locator("#question-"+question_id)
    assert card.count()==1
    assert card.locator("h3",has_text="Candidate derivation").count()==0
    helper=card.locator("button").filter(has_text="Progressive Hints").first
    assert "Hints (3)" in helper.inner_text()
    helper.click()
    assert "OPEN_THE_WAY" in card.inner_text()
    assert "Candidate derivation" not in card.inner_text()
    helper.click()
    card.locator(f'input[value="{option}"]').check()
    card.get_by_role("button",name=re.compile("Commit First Attempt")).click()
    assert card.locator("h3",has_text="Candidate derivation").count()==1
    assert "Hints (3)" in helper.inner_text()
    keys=page.evaluate(
      "prefix => Object.keys(localStorage).filter(k => k.startsWith(prefix))",PREFIX)
    assert len(keys)==1
    attempt=page.evaluate("k => JSON.parse(localStorage.getItem(k))",keys[0])
    assert attempt["selected"]==[option]
    assert re.fullmatch(r"[a-f0-9]{64}",attempt["content_revision_sha256"])
    helper.click()
    assert "OPEN_THE_WAY" in card.inner_text()
    return keys[0],attempt


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    p=port()
    url=f"http://127.0.0.1:{p}/nsejs/physics/index.html"
    receipt={"task":"PH11_CIRCUITS_CORE2_HTTP_CHROMIUM_R1",
             "engineering_status":"NOT_RUN","source_status":"HOLD",
             "qrt_status":"HOLD","academic_status":"HOLD","checks":[]}
    server=subprocess.Popen([sys.executable,"-m","http.server",str(p),
      "--directory",str(ROOT),"--bind","127.0.0.1"],
      stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(url,timeout=1).close()
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise AssertionError("HTTP server unavailable")

        with sync_playwright() as play:
            browser=play.chromium.launch(headless=True)
            try:
                for orient,width,height in [("portrait",1000,1600),("landscape",1600,1000)]:
                    context=browser.new_context(viewport={"width":width,"height":height},
                      has_touch=True,device_scale_factor=1)
                    page=context.new_page()
                    errors=[]
                    page.on("pageerror",lambda err:errors.append(str(err)))
                    page.goto(url+"?topic=circuits",wait_until="domcontentloaded",timeout=30000)
                    cards=wait_cards(page,66)
                    identifiers=[x.get_attribute("data-source-id") for x in cards.all()]
                    l1=[f"NSEJS-CIRC-L1-Q{i:02d}" for i in range(1,37)]
                    l2=[f"NSEJS-CIRC-L2-Q{i:02d}" for i in range(1,21)]
                    assert identifiers[10:46]==l1,identifiers[10:46]
                    assert identifiers[46:66]==l2,identifiers[46:66]
                    assert "66" in page.locator("#qbResultCount").inner_text()
                    assert not errors,errors
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"),"Horizontal overflow"
                    qid="NSEJS-CIRC-L1-Q01"
                    key,old=commit_candidate(page,qid,"B")
                    page.reload(wait_until="domcontentloaded")
                    wait_cards(page,66)
                    card=page.locator("#question-"+qid)
                    assert card.locator("h3",has_text="Candidate derivation").count()==1
                    assert card.get_by_role("button",name=re.compile("Attempt Saved Locally")).is_disabled()
                    assert page.evaluate("k => JSON.parse(localStorage.getItem(k))",key)==old
                    assert not errors,errors
                    page.screenshot(path=str(OUT/f"circuits-{orient}.png"),full_page=False)
                    receipt["checks"].append({"orientation":orient,"visible_candidates":66,
                      "l1_ordered":36,"l2_ordered":20,
                      "pre_attempt_H1_H3_nondecisive":True,"first_attempt_persists":True,
                      "reader_console_errors":0})
                    context.close()

                # Save-denial must never reveal key, answer DOM or Tier 3 help.
                denied=browser.new_context()
                fail=denied.new_page()
                fail.add_init_script("Storage.prototype.setItem=function(){throw Error('QA_STORAGE_DENIED')}")
                fail.goto(url+"?topic=circuits&q=NSEJS-CIRC-L1-Q01",wait_until="domcontentloaded")
                wait_cards(fail,1)
                card=fail.locator("#question-NSEJS-CIRC-L1-Q01")
                card.locator('input[value="B"]').check()
                card.get_by_role("button",name=re.compile("Commit First Attempt")).click()
                assert card.locator("h3",has_text="Candidate derivation").count()==0
                assert "Hints (3)" in card.get_by_role("button",name=re.compile("Show Progressive Hints")).inner_text()
                assert "storage unavailable" in card.inner_text()
                receipt["checks"].append({"negative":"STORAGE_DENIED","result":"FAIL_CLOSED"})
                denied.close()

                # Same-name figure bytes changed: prior attempt must not be replayed.
                stale=browser.new_context()
                page=stale.new_page()
                qid="NSEJS-CIRC-L1-Q03"
                page.goto(url+"?topic=circuits&q="+qid,wait_until="domcontentloaded")
                wait_cards(page,1)
                old_key,_=commit_candidate(page,qid,"A")
                def mutate(route):
                    response=route.fetch()
                    route.fulfill(response=response,body=response.body()+b"\n<!-- QA_IMAGE_CONTENT_REVISION -->\n")
                stale.route("**/nsejs/assets/fig_nsejs_circ_l1_q03.svg",mutate)
                page.reload(wait_until="domcontentloaded")
                wait_cards(page,1)
                card=page.locator("#question-"+qid)
                assert card.locator("h3",has_text="Candidate derivation").count()==0
                assert card.get_by_role("button",name=re.compile("Commit First Attempt")).is_enabled()
                keys=page.evaluate(
                  "prefix => Object.keys(localStorage).filter(k => k.startsWith(prefix))",PREFIX)
                assert keys==[old_key],keys
                receipt["checks"].append({"negative":"SAME_NAME_FIGURE_BYTE_CHANGE",
                  "result":"OLD_ATTEMPT_NOT_REPLAYED"})
                stale.close()
            finally:
                browser.close()
        receipt["engineering_status"]="CHROMIUM_PASS__ACADEMIC_HOLD"
    except Exception as exc:
        receipt["engineering_status"]="FAIL_CLOSED"
        receipt["error"]=repr(exc)
        raise
    finally:
        server.terminate()
        try:server.wait(timeout=5)
        except subprocess.TimeoutExpired:server.kill()
        (OUT/"circuits-browser-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps({"status":receipt["engineering_status"],
          "checks":len(receipt["checks"])}))


if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""R14 R00 adversarial QA for B01 preview; human academic/P00 acceptance remains HOLD."""
from __future__ import annotations

import json
import hashlib
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"review-artifacts/physics-b01-r14"
BASE="/nsejs/physics/curriculum/topics/PH07/b01/learner-preview/index.html"
TASK="PH07-01-B01-INSTANCE-MODEL-R2"

def legacy_r13_digest():
    path=ROOT/"nsejs/physics/curriculum/topics/PH07/b01/B01_INTEGRATED_CURRICULUM_PROPOSAL.v1.json"
    raw=path.read_text(encoding="utf-8")
    p=json.loads(raw)
    packages={}
    for g in p["groups"]:
        for e in g["base_instances"]:
            packages[e["package_path"]]=e["package_blob"]
    pack_lines="\n".join(sorted(p+":"+sha for p,sha in packages.items()))
    transfer_lines="\n".join(sorted(e["proposal_path"]+":"+e["proposal_blob"]
                                    for e in p["supplements"]))
    source=raw+"\n"+pack_lines+"\n"+transfer_lines
    return hashlib.sha256(source.encode("utf-8")).hexdigest()

def find_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1",0))
        return sock.getsockname()[1]

def ready(page):
    page.wait_for_function("""() => {
        const s=document.querySelector('#status').textContent;
        return s.includes('Exact-version author candidate loaded') ||
               s.includes('Previous first answer restored') ||
               s.includes('Fail closed');
    }""",timeout=22000)
    status=page.locator("#status").inner_text()
    assert "Fail closed" not in status,status

def saved(page):
    return page.evaluate("""() => {
        const key=Object.keys(localStorage).find(k=>k.startsWith('g9-b01-r1:') &&
            localStorage.getItem(k)?.includes('"first_answer"'));
        return [key,key?JSON.parse(localStorage.getItem(key)):null];
    }""")

def adversarial(browser,origin,orientation,width,height):
    url=origin+BASE+"?task="+TASK
    output=[]
    context=browser.new_context(viewport={"width":width,"height":height},has_touch=True)
    a=context.new_page()
    b=context.new_page()
    try:
        a.goto(url);ready(a)
        b.goto(url);ready(b)
        a.locator("#predict-input").fill("I predict a conditional calibration result.")
        a.locator("#attempt-input").fill("Check offset, slope and the unused reference reading.")
        a.locator("#save-first").click()
        original=saved(a)[1]["first_answer"]
        b.wait_for_function("document.querySelector('#status').textContent.includes('Fail closed')")
        assert b.locator("#learner").is_hidden()
        assert saved(a)[1]["first_answer"]==original
        output.append({"case":"TWO_TAB_STALE_WRITE_BLOCKED","orientation":orientation,"pass":True})
        # Hidden direct-click attacks must not skip RECONSTRUCT and its recorded exposure.
        a.evaluate("""() => {
          document.querySelector('#diagnose-input').value='premature diagnosis';
          document.querySelector('#save-diagnosis').click();
          document.querySelector('#repair-input').value='premature repair';
          document.querySelector('#save-repair').click();
          document.querySelector('#boundary-input').value='premature boundary';
          document.querySelector('#save-boundary').click();
        }""")
        row=saved(a)[1]
        assert row["first_answer"]==original
        assert row["diagnosis_notes"]==row["repairs"]==row["boundary_attempts"]==[]
        output.append({"case":"HIDDEN_STAGE_BYPASS_BLOCKED","orientation":orientation,"pass":True})
    finally:
        context.close()

    context=browser.new_context(viewport={"width":width,"height":height},has_touch=True)
    page=context.new_page()
    try:
        page.goto(url);ready(page)
        page.locator("#core1a-link").click()
        assert "/PH07-01/core1a.html" in page.url
        page.go_back();ready(page)
        before=saved(page)[1]
        assert "TEXTBOOK" in [x["kind"] for x in before["help_exposure"]]
        assert before["first_answer"] is None
        page.locator("#predict-input").fill("I read the textbook before committing.")
        page.locator("#attempt-input").fill("This assisted answer is not unexposed evidence.")
        page.locator("#save-first").click()
        first=saved(page)[1]["first_answer"]
        assert "TEXTBOOK" in first["help_before_first"]
        assert "TEXTBOOK" in page.locator("#saved-first").inner_text()
        page.reload();ready(page)
        assert saved(page)[1]["first_answer"]==first
        output.append({"case":"TEXTBOOK_PRE_FIRST_EXPOSURE_PERSISTS","orientation":orientation,"pass":True})
    finally:
        context.close()

    context=browser.new_context(viewport={"width":width,"height":height},has_touch=True)
    page=context.new_page()
    try:
        page.goto(url);ready(page)
        # A fresh attempt is still in memory; persist a legitimate H1 first.
        page.locator("#h1").click()
        key,record=saved(page)
        assert record is not None
        record["help_exposure"]=[{"kind":"RECONSTRUCT","at":"2026-11-14T00:00:00.000Z"}]
        page.evaluate("(p)=>localStorage.setItem(p[0],JSON.stringify(p[1]))",[key,record])
        page.reload()
        page.wait_for_function("document.querySelector('#status').textContent.includes('Fail closed')")
        assert page.locator("#learner").is_hidden()
        output.append({"case":"SEMANTICALLY_CORRUPT_STAGE_HISTORY_REJECTED",
                       "orientation":orientation,"pass":True})
    finally:
        context.close()

    context=browser.new_context(viewport={"width":width,"height":height},has_touch=True)
    page=context.new_page()
    try:
        page.route("**/PH07-01/core1a.html",lambda route:route.fulfill(
            status=200,content_type="text/html",
            body="<html><body>Modified figure and scientific teaching.</body></html>"))
        page.goto(url)
        page.wait_for_function("document.querySelector('#status').textContent.includes('Fail closed')",
                               timeout=22000)
        assert "Git blob mismatch" in page.locator("#status").inner_text()
        assert page.locator("#learner").is_hidden()
        output.append({"case":"CORE1A_INLINE_FIGURE_PAGE_BLOB_MISMATCH_REJECTED",
                       "orientation":orientation,"pass":True})
    finally:
        context.close()
    # R13 original keyed answers remain available after R14's stricter HTML/figure
    # revision digest. The linked new record discloses unverified old figure custody.
    context=browser.new_context(viewport={"width":width,"height":height},has_touch=True)
    page=context.new_page()
    try:
        page.goto(url);ready(page)
        old_key="g9-b01-r1:"+legacy_r13_digest()+":"+TASK
        record={
            "schema":"g9-b01-attempt-r1","task_id":TASK,
            "content_revision":legacy_r13_digest(),
            "first_answer":{"prediction":"Historical R13 prediction",
                            "answer":"Historical R13 physical reasoning",
                            "saved_at":"2026-11-13T12:00:00.000Z"},
            "help_exposure":[],"diagnosis_notes":[],"repairs":[],
            "boundary_attempts":[],"mastery_status":"UNASSESSED",
        }
        page.evaluate("(p)=>localStorage.setItem(p[0],JSON.stringify(p[1]))",
                      [old_key,record])
        page.reload()
        page.wait_for_function(
            "document.querySelector('#status').textContent.includes('Historical R13 first answer carried forward')",
            timeout=22000,
        )
        new_key,linked=saved(page)
        assert new_key is not None and new_key != old_key
        assert linked["first_answer"]==record["first_answer"]
        assert linked["migration_provenance"]["from_digest"]==legacy_r13_digest()
        assert linked["migration_provenance"]["figure_identity_at_old_attempt"]=="NOT_ESTABLISHED_R13"
        assert page.evaluate("(k)=>JSON.parse(localStorage.getItem(k))",old_key)==record
        assert page.locator("#attempt-input").is_disabled()
        assert "NOT ESTABLISHED" in page.locator("#saved-first").inner_text()
        output.append({"case":"R13_FIRST_ANSWER_NONDESTRUCTIVE_LINK_AND_FIGURE_CAVEAT",
                       "orientation":orientation,"pass":True})
    finally:
        context.close()
    return output

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    port=find_port()
    origin="http://127.0.0.1:"+str(port)
    server=subprocess.Popen([sys.executable,"-m","http.server",str(port),"--bind","127.0.0.1",
                             "--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    receipt={"task":"B01_R14_R00_ADVERSARIAL_PROTECTED_ATTEMPT",
             "P00":"HOLD","R01":"HOLD","academic_status":"HOLD",
             "source_custody":"CANDIDATE_AUTHOR_PAGE_BYTE_PINS",
             "cases":[]}
    try:
        for _ in range(100):
            if server.poll() is not None:raise RuntimeError("HTTP server exited")
            try:
                urllib.request.urlopen(origin+BASE,timeout=1).close()
                break
            except Exception:time.sleep(0.1)
        else:raise RuntimeError("HTTP unavailable")
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for orientation,w,h in (("portrait",1000,1600),("landscape",1600,1000)):
                receipt["cases"]+=adversarial(browser,origin,orientation,w,h)
            browser.close()
        assert len(receipt["cases"])==10
        receipt["status"]="R00_NEGATIVE_CONTROLS_PASS__ACADEMIC_HOLD"
        (OUT/"r14-negative-qa.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps(receipt,indent=2))
    finally:
        server.terminate()
        server.wait(timeout=6)

if __name__=="__main__":
    main()

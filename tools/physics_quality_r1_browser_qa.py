"""Exact-head HTTP Chromium journey QA for four WPE-style Physics R1 candidates.

Verifies technical gating and two tablet viewports, not independent academic
qualification, original exam fidelity, or tamper-proof storage.
"""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review-artifacts/physics-quality-r1"
UNITS = {"PH01-M05":("PH01","M05",8),"PH02-F04":("PH02","F04",8),
         "PH07-02":("PH07","PH07-02",12),"PH08-08":("PH08","PH08-08",13)}


def no_overflow(page, label):
    bounds=page.evaluate("""() => ({
      scroll:document.documentElement.scrollWidth,
      window:document.documentElement.clientWidth
    })""")
    assert bounds["scroll"] <= bounds["window"]+3,(label,bounds)


def inspect_case(origin, browser, size, ident, chapter, key, count):
    context=browser.new_context(viewport={"width":size[0],"height":size[1]})
    page=context.new_page()
    errors=[]
    requested=[]
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda request: requested.append(request.url))
    try:
        route=origin+"/nsejs/physics/learn/chapter.html?ph="+chapter
        page.goto(route,wait_until="domcontentloaded")
        page.get_by_role("link",name="Extra teaching · WPE-style").wait_for(timeout=15000)
        assert page.get_by_role("link",name="Fresh six-stage transfer · candidate").count()==1
        assert page.get_by_role("link",name="Inspect source evidence for this chapter (0 qualified exam items)").count()==1
        page.get_by_role("link",name="Extra teaching · WPE-style").click()
        page.locator(".stage").first.wait_for(timeout=15000)
        assert ident in page.url
        assert page.locator(".stage").count()==3
        assert page.locator("svg.figure").count()==1
        assert page.locator("h2").filter(has_text="Build the warranted model").count()==1
        assert any("study-data.v1.json" in x for x in requested)
        assert not any("postattempt-models.v1.json" in x for x in requested)
        assert not any("/cases.v1.json" in x for x in requested)
        no_overflow(page,ident+" study "+str(size))
        if size in ((1000,1600),(1280,800)):
            page.screenshot(path=str(OUT / f"{ident}-{size[0]}x{size[1]}-core1a.png"),full_page=True)

        page.get_by_role("link",name="Open changed-condition Core1B").click()
        page.get_by_role("button",name="Save protected first prediction + attempt").wait_for(timeout=15000)
        assert page.get_by_role("button",name="Reveal model after your saved first attempt").count()==0
        assert page.locator("blockquote").count()==0
        assert any("attempt-prompts.v1.json" in x for x in requested)
        assert not any("postattempt-models.v1.json" in x for x in requested)
        assert not any("/cases.v1.json" in x for x in requested)
        page.locator("#prediction").fill("I predict we must choose the physical model and check its conditions.")
        page.locator("#answer").fill("My first independent construction names the object, checks which equations apply, and verifies the units, signs and conditions explicitly.")
        page.get_by_role("button",name="Save protected first prediction + attempt").click()
        page.locator("blockquote").wait_for(timeout=15000)
        original=page.locator("blockquote").inner_text()
        assert original.startswith("My first independent construction")
        # Post-attempt key retrieval is asynchronous; wait for hash verification.
        page.get_by_role("button",name="Reveal H1").wait_for(timeout=15000)
        assert any("postattempt-models.v1.json" in x for x in requested)
        assert page.get_by_role("button",name="Reveal model after your saved first attempt").count()==1
        assert page.locator("#boundary").count()==0
        key_snapshot=page.evaluate("""() => Object.entries(localStorage)
          .filter(([k,v]) => k.startsWith('G9V41:QUALITY-R1:') && !k.endsWith(':prehelp'))""")
        assert len(key_snapshot)==1, (ident,key_snapshot)
        page.reload(wait_until="domcontentloaded")
        page.locator("blockquote").wait_for(timeout=15000)
        assert page.locator("blockquote").inner_text()==original
        assert page.get_by_role("button",name="Save protected first prediction + attempt").count()==0
        page.get_by_role("button",name="Reveal H1").click()
        assert page.get_by_role("button",name="Reveal H2").count()==1
        page.get_by_role("button",name="Reveal model after your saved first attempt").click()
        page.get_by_role("button",name="Record diagnosis").wait_for()
        page.locator("#diagnosis").fill("The first divergence was using a shortcut without checking the geometry, signs or system boundary.")
        page.get_by_role("button",name="Record diagnosis").click()
        page.get_by_role("button",name="Save separate repaired reasoning").wait_for()
        page.locator("#repair").fill("My corrected work selects the warranted model, checks dimensions and verifies the independent limiting condition.")
        page.get_by_role("button",name="Save separate repaired reasoning").click()
        page.get_by_role("button",name="Commit boundary attempt").wait_for()
        assert page.get_by_role("button",name="Reveal boundary model only after attempt").count()==0
        page.locator("#boundary").fill("I reconstruct the changed condition independently with a new model check, not by copying the solved numbers.")
        page.get_by_role("button",name="Commit boundary attempt").click()
        page.get_by_role("button",name="Reveal boundary model only after attempt").click()
        assert page.locator(".stage").last.inner_text().count("Conditional worked boundary reasoning:")==1
        after=page.evaluate("""() => Object.entries(localStorage)
          .filter(([k,v]) => k.startsWith('G9V41:QUALITY-R1:') && !k.endsWith(':prehelp'))""")
        assert len(after)==1 and after[0][0]==key_snapshot[0][0]
        assert page.locator("blockquote").inner_text()==original
        no_overflow(page,ident+" challenge "+str(size))
        if size in ((1000,1600),(1280,800)):
            page.screenshot(path=str(OUT / f"{ident}-{size[0]}x{size[1]}-core1b.png"),full_page=True)
        assert not errors,(ident,errors)

        page.goto(origin+"/nsejs/physics/quality-r1/source.html?ph="+chapter,wait_until="domcontentloaded")
        page.locator("tbody tr").first.wait_for(timeout=15000)
        assert page.locator("tbody tr").count()==count
        assert "zero original-question admissions" in page.locator("#quality-root").inner_text()
        assert not errors,errors
        return {"unit":ident,"viewport":f"{size[0]}x{size[1]}","status":"PASS"}
    finally:
        context.close()


def blocked_storage(origin, browser):
    context=browser.new_context()
    context.add_init_script("""Object.defineProperty(window,'localStorage',
      {configurable:true,get(){throw new Error('test storage denied')}});""")
    page=context.new_page()
    try:
        page.goto(origin+"/nsejs/physics/quality-r1/challenge.html?unit=PH02-F04",
                  wait_until="domcontentloaded")
        page.get_by_text("HOLD: local storage/digest/record verification failed",exact=False).wait_for(timeout=15000)
        assert page.get_by_role("button",name="Save protected first prediction + attempt").count()==0
        return {"disabled_storage":"FAIL_CLOSED_PASS"}
    finally:
        context.close()


def tampered_postattempt_model(origin,browser):
    # A stale or altered public JSON answer asset cannot be treated as a
    # compatible key for an already saved first attempt.
    context=browser.new_context()
    page=context.new_page()
    context.route("**/postattempt-models.v1.json",
                  lambda route:route.fulfill(status=200,content_type="application/json",
                                             body='{"schema":"tampered"}'))
    try:
        page.goto(origin+"/nsejs/physics/quality-r1/challenge.html?unit=PH08-08",
                  wait_until="domcontentloaded")
        page.get_by_role("button",name="Save protected first prediction + attempt").wait_for()
        page.locator("#prediction").fill("I first need to check the clock origin before choosing the geometry.")
        page.locator("#answer").fill("My independent first attempt compares both propagation paths, calculates their difference, and checks the detector threshold.")
        page.get_by_role("button",name="Save protected first prediction + attempt").click()
        page.get_by_text("HOLD: post-attempt model unavailable or mismatched",exact=False).wait_for(timeout=15000)
        assert page.get_by_role("button",name="Reveal model after your saved first attempt").count()==0
        assert page.locator("blockquote").count()==1 # first response survives
        assert page.get_by_role("button",name="Reveal H1").count()==0
        return {"tampered_answer_model":"FAIL_CLOSED_PASS"}
    finally:context.close()


def missing_source_pin(origin,browser):
    # A forged/unpinned public prompt manifest must not even expose
    # a protected first-attempt start action.
    import json
    bad=json.loads((ROOT/"nsejs/physics/quality-r1/attempt-prompts.v1.json").read_text(encoding="utf-8"))
    bad.pop("source_package_git_blob",None)
    context=browser.new_context()
    context.route("**/attempt-prompts.v1.json",
                  lambda route:route.fulfill(status=200,content_type="application/json",
                                             body=json.dumps(bad)))
    page=context.new_page()
    try:
        page.goto(origin+"/nsejs/physics/quality-r1/challenge.html?unit=PH01-M05",
                  wait_until="domcontentloaded")
        page.get_by_text("Pinned source and post-attempt model revisions required",exact=False).wait_for(timeout=15000)
        assert page.get_by_role("button",name="Save protected first prediction + attempt").count()==0
        return {"missing_prompt_source_pin":"FAIL_CLOSED_PASS"}
    finally:context.close()


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
    thread=Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:
        origin="http://127.0.0.1:"+str(server.server_port)
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for dims in ((1000,1600),(1600,1000),(1280,800),(1024,768),(900,1280),(800,1280)):
                    for ident,(ch,u,count) in UNITS.items():
                        print(inspect_case(origin,browser,dims,ident,ch,u,count),flush=True)
                print(blocked_storage(origin,browser),flush=True)
                print(tampered_postattempt_model(origin,browser),flush=True)
                print(missing_source_pin(origin,browser),flush=True)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=4)


if __name__=="__main__":
    main()

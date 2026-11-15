"""R2 Physics candidate QA: real HTTP Chromium, six tablet viewports, four units.

Technical candidate tests, not original exam admission, PH06 certification,
independent B3/B4 academic checks or an approved R3 production release.
"""
from __future__ import annotations

import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"nsejs/physics/quality-r1"
OUT=ROOT/"review-artifacts/physics-quality-r2"
CASES=json.loads((DIR/"cases.v2.json").read_text(encoding="utf-8"))
PROMPTS=json.loads((DIR/"attempt-prompts.v2.json").read_text(encoding="utf-8"))
GUIDES=json.loads((DIR/"postattempt-guidance.v2.json").read_text(encoding="utf-8"))
BOUNDARIES=json.loads((DIR/"boundary-models.v2.json").read_text(encoding="utf-8"))
UNITS=[c["unit"] for c in CASES["units"]]
VIEWPORTS=[(1000,1600),(1600,1000),(1280,800),(1024,768),(900,1280),(800,1280)]


def byunit(j,unit):
    return next(x for x in j["units"] if x["unit"]==unit)


def load(page,url):
    page.goto(url,wait_until="domcontentloaded")
    try:
        page.locator("#quality-root .card").first.wait_for(timeout=18000)
    except Exception:
        print("CANDIDATE_ROUTE_FAILURE",url,"DOM:",
              page.locator("#quality-root").inner_text()[:1400],flush=True)
        raise


def no_overflow(page,unit,size):
    doc=page.evaluate("() => [document.documentElement.scrollWidth,document.documentElement.clientWidth]")
    assert doc[0]<=doc[1]+3,(unit,size,doc)


def entered_correct_data(page,unit,variant):
    prompt=byunit(PROMPTS,unit)
    rules=byunit(GUIDES,unit)["rubric"]
    model=rules[0]
    for i,f in enumerate(prompt["fields"]):
        rule=next(r for r in rules if r["id"]==f["id"])
        correct=str(rule["expected"])
        if f["type"]=="select":
            options=f["options"]
            wrong=next(x for x in options if x!=correct and not x.startswith("Choose"))
            value=wrong if variant=="wrong_model" and i==0 else correct
            page.locator("#a-"+f["id"]).select_option(value)
        else:
            value=correct
            if variant=="wrong_number" and i==1:value=str(float(correct)+10.0)
            if variant=="missing_number" and i==1:value=""
            page.locator("#a-"+f["id"]).fill(value)


def one_journey(browser,origin,unit,size,variant):
    context=browser.new_context(viewport={"width":size[0],"height":size[1]})
    page=context.new_page()
    requested=[]
    errors=[]
    page.on("request",lambda req: requested.append(req.url))
    page.on("pageerror",lambda err: errors.append(str(err)))
    try:
        load(page,origin+"/nsejs/physics/quality-r1/study.html?unit="+unit)
        assert page.locator(".stage").count()==3
        assert page.locator("svg.figure").count()==1
        assert "LOCAL_GUIDE_VIEW_RECORDED" in page.locator("#quality-root").inner_text()
        assert not any("cases.v2.json" in x for x in requested)
        no_overflow(page,unit,size)
        page.get_by_role("link",name="Open changed-condition Core1B").click()
        page.get_by_role("button",name="Commit prediction").wait_for()
        assert any("prediction-prompts.v2.json" in x for x in requested)
        assert not any("attempt-prompts.v2.json" in x for x in requested)
        assert not any("postattempt-guidance.v2.json" in x for x in requested)
        assert not any("boundary-models.v2.json" in x for x in requested)
        page.locator("#prediction-r2").fill("I predict that a physical model choice and independent check are essential.")
        page.get_by_role("button",name="Commit prediction").click()
        page.get_by_role("button",name="Commit immutable first attempt").wait_for()
        assert any("attempt-prompts.v2.json" in x for x in requested)
        assert not any("postattempt-guidance.v2.json" in x for x in requested)
        entered_correct_data(page,unit,variant)
        first_reason="My first independent physics construction checks the system assumptions, signed equations and units before trusting any numerical answer."
        page.locator("#a-reason").fill(first_reason)
        page.get_by_role("button",name="Commit immutable first attempt").click()
        page.get_by_role("button",name="Reveal authored reconstruction").wait_for()
        assert any("postattempt-guidance.v2.json" in x for x in requested)
        assert not any("boundary-models.v2.json" in x for x in requested)
        page.get_by_role("button",name="Reveal next hint").click()
        page.get_by_role("button",name="Reveal authored reconstruction").click()
        page.get_by_role("button",name="Commit diagnosis").wait_for()
        result=page.locator("#quality-root").inner_text()
        if variant=="wrong_model":
            assert "Possible first divergence" in result and "Model selection" in result or "Which contact model" in result or "Identify the two energy" in result or "Select the geometric" in result
        if variant=="wrong_number":
            assert "Possible first divergence" in result
            assert "REVIEW" in result
        if variant=="correct":
            assert "All checked model/value fields match" in result
        if variant=="missing_number":
            assert "MISSING" in result
        # Verify first response is unchanged across refresh and task reconstruction.
        original=page.locator("details").first.text_content()
        assert first_reason in original
        page.reload(wait_until="domcontentloaded")
        page.get_by_role("button",name="Commit diagnosis").wait_for()
        assert first_reason in page.locator("details").first.text_content()
        page.locator("#diagnosis-select").select_option("reasoning_or_assumptions")
        page.locator("#diagnosis-reason").fill("The first decisive check is the physical model and its conditions, not just a matching number.")
        page.get_by_role("button",name="Commit diagnosis").click()
        page.get_by_role("button",name="Commit separate repair").wait_for()
        page.locator("#repair-reason").fill("The repaired reasoning checks the object boundary, model domain, signed equations and independently verifies the result.")
        page.get_by_role("button",name="Commit separate repair").click()
        page.get_by_role("button",name="Commit boundary answer before model key").wait_for()
        assert not any("boundary-models.v2.json" in x for x in requested)
        answer=byunit(BOUNDARIES,unit)
        for f in answer["boundaryRubric"]:
            page.locator("#b-"+f["id"]).fill(str(f["expected"]))
        page.locator("#boundary-reason").fill("I independently changed the physical constraint and checked the revised equation, signs and dimensions.")
        page.get_by_role("button",name="Commit boundary answer before model key").click()
        page.get_by_role("button",name="Reveal boundary model and structured checks").wait_for()
        assert any("boundary-models.v2.json" in x for x in requested)
        page.get_by_role("button",name="Reveal boundary model and structured checks").click()
        page.get_by_text("Candidate cycle complete",exact=False).wait_for()
        assert first_reason in page.locator("details").first.text_content()
        assert not errors,errors
        no_overflow(page,unit,size)
        if size in ((1000,1600),(1280,800)):
            page.screenshot(path=str(OUT/f"{unit}-{size[0]}x{size[1]}-completed.png"),full_page=True)
        # Source reader must not fetch denied review directory.
        page.goto(origin+"/nsejs/physics/quality-r1/source.html?ph="+unit[:4],wait_until="domcontentloaded")
        page.locator("tbody tr").first.wait_for(timeout=18000)
        assert any("public-source-status.v2.json" in x for x in requested)
        assert not any("/review/physics/" in x for x in requested)
        return {"unit":unit,"viewport":str(size),"model_case":variant,"result":"PASS"}
    finally:context.close()


def stale_two_tab(browser,origin):
    ctx=browser.new_context()
    p=ctx.new_page()
    q=ctx.new_page()
    # Keep Q on a stale DOM after P commits. Web Locks must read latest storage.
    q.add_init_script("""(() => {const original=window.addEventListener.bind(window);
      window.addEventListener=(name,callback,options) => {
        if(name==='storage') return;return original(name,callback,options)
      };})();""")
    path=origin+"/nsejs/physics/quality-r1/challenge.html?unit=PH02-F04"
    try:
        load(p,path);load(q,path)
        for page in (p,q):
            page.locator("#prediction-r2").fill("First prediction is recorded before the full problem appears.")
        p.get_by_role("button",name="Commit prediction").click()
        p.get_by_role("button",name="Commit immutable first attempt").wait_for()
        q.get_by_role("button",name="Commit prediction").click()
        q.get_by_text("Prediction already committed",exact=False).wait_for()
        assert p.locator("#a-model").count()==1
        # Q reloads to capture the shared prediction while retaining its
        # own future stale first-answer form.
        q.reload(wait_until="domcontentloaded")
        q.get_by_role("button",name="Commit immutable first attempt").wait_for()
        entered_correct_data(p,"PH02-F04","correct")
        p.locator("#a-reason").fill("Original first answer from tab A with physical assumptions and force equations preserved.")
        p.get_by_role("button",name="Commit immutable first attempt").click()
        p.get_by_role("button",name="Reveal authored reconstruction").wait_for()
        entered_correct_data(q,"PH02-F04","wrong_model")
        q.locator("#a-reason").fill("Competing stale tab answer must not replace tab A's recorded first model.")
        q.get_by_role("button",name="Commit immutable first attempt").click()
        q.get_by_text("Attempt advanced in another tab",exact=False).wait_for()
        q.reload(wait_until="domcontentloaded")
        q.get_by_role("button",name="Reveal authored reconstruction").wait_for()
        assert "Original first answer from tab A" in q.locator("details").first.text_content()
        assert "Competing stale tab answer" not in q.locator("details").first.text_content()
        return {"two_tab_prediction_and_first":"FAIL_CLOSED_PASS"}
    finally:ctx.close()


def storage_write_denied(browser,origin):
    ctx=browser.new_context();p=ctx.new_page()
    try:
        load(p,origin+"/nsejs/physics/quality-r1/challenge.html?unit=PH02-F04")
        p.locator("#prediction-r2").fill("Test a prediction and then deliberately block the real first write.")
        p.get_by_role("button",name="Commit prediction").click()
        p.get_by_role("button",name="Commit immutable first attempt").wait_for()
        entered_correct_data(p,"PH02-F04","correct")
        p.locator("#a-reason").fill("An attempted answer that must fail at localStorage's actual first-commit setItem.")
        p.evaluate("""() => {const original=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){
          if(k.startsWith('G9V41:PHYSICS:R2:')&&!k.endsWith(':probe'))throw Error('forced first write denial');
          return original.call(this,k,v);
        }}""")
        p.get_by_role("button",name="Commit immutable first attempt").click()
        p.get_by_text("forced first write denial",exact=False).wait_for()
        assert p.get_by_role("button",name="Reveal authored reconstruction").count()==0
        return {"actual_first_write_denial":"FAIL_CLOSED_PASS"}
    finally:ctx.close()


def tampered_pins_and_model(browser,origin):
    base=origin+"/nsejs/physics/quality-r1/challenge.html?unit=PH08-08"
    ctx=browser.new_context();p=ctx.new_page()
    try:
        # Valid 40-hex substitution is rejected against separately frozen pin manifest.
        public=json.loads((DIR/"prediction-prompts.v2.json").read_text(encoding="utf-8"))
        public["source_v2_git_blob"]="a"*40
        ctx.route("**/prediction-prompts.v2.json",lambda route:route.fulfill(status=200,content_type="application/json",body=json.dumps(public)))
        p.goto(base,wait_until="domcontentloaded")
        p.get_by_text("Pinned bytes mismatch: prediction-prompts.v2.json",exact=False).wait_for(timeout=15000)
        assert p.get_by_role("button",name="Commit prediction").count()==0
    finally:ctx.close()
    ctx=browser.new_context();p=ctx.new_page()
    try:
        ctx.route("**/postattempt-guidance.v2.json",lambda route:route.fulfill(status=200,content_type="application/json",body='{"schema":"forged"}'))
        load(p,base)
        p.locator("#prediction-r2").fill("Predict using a physical model before the first independent attempt.")
        p.get_by_role("button",name="Commit prediction").click()
        p.get_by_role("button",name="Commit immutable first attempt").wait_for()
        entered_correct_data(p,"PH08-08","correct")
        p.locator("#a-reason").fill("A first response saved despite a later tampered post-attempt key.")
        p.get_by_role("button",name="Commit immutable first attempt").click()
        p.get_by_text("Pinned bytes mismatch: postattempt-guidance.v2.json",exact=False).wait_for()
        assert p.get_by_role("button",name="Reveal authored reconstruction").count()==0
        assert "A first response saved" in p.evaluate("() => JSON.stringify(localStorage)")
        return {"valid_looking_wrong_source_pin":"FAIL_CLOSED_PASS","tampered_guidance":"FAIL_CLOSED_PASS"}
    finally:ctx.close()


def run():
    OUT.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        origin="http://127.0.0.1:"+str(server.server_port)
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(headless=True)
            try:
                variants=["wrong_model","wrong_number","correct","missing_number","correct","wrong_model"]
                for i,size in enumerate(VIEWPORTS):
                    for unit in UNITS:
                        print(one_journey(browser,origin,unit,size,variants[i]),flush=True)
                print(stale_two_tab(browser,origin),flush=True)
                print(storage_write_denied(browser,origin),flush=True)
                print(tampered_pins_and_model(browser,origin),flush=True)
            finally:browser.close()
    finally:server.shutdown();server.server_close();thread.join(timeout=5)


if __name__=="__main__":
    run()

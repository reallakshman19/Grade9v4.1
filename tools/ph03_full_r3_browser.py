"""Full PH03 R3 author-candidate browser witness; not academic acceptance.

Run against localhost HTTP Chromium. Includes 12 learner orientations, stage-by-stage
Skip/no-credit checks, answer-network gating, SHA failure, storage denial and two tabs.
"""
from __future__ import annotations

import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE_PATH="nsejs/physics"
DATA=ROOT/BASE_PATH/"ph03/complete-r3"
IDS=("P01","P02","P04","P05","P06","P07")
ART=ROOT/"artifacts/ph03-complete-r3"
ART.mkdir(parents=True,exist_ok=True)


def data(id):
    return json.loads((DATA/(id+".json")).read_text())


def post(id):
    return json.loads((DATA/("post-"+id+".json")).read_text())


def url(base,id,mode="practice"):
    kind="textbook" if mode=="learn" else "core1"
    return base+"/"+kind+"/PH03/"+id+"/index.html"


def saved(page,id):
    prefix="G9V41:PH03:R3:"+id+":"
    found=page.evaluate("""prefix => Object.entries(localStorage).filter(([k,v]) =>
      k.startsWith(prefix)).map(([key,raw])=>({key,data:JSON.parse(raw)}))""",prefix)
    return next((x for x in found if x["data"].get("first")),None)


def press_skip(page,field_id):
    control=page.locator('button[data-skip="'+field_id+'"]')
    expect(control).to_be_visible()
    control.click()
    expect(control).to_have_attribute("aria-pressed","true")
    target=page.locator("#"+field_id)
    assert target.evaluate("(el) => el.dataset.skipped==='true' && el.disabled")
    return control


def skip_fields(page,fields,prefix):
    for f in fields:
        press_skip(page,prefix+f["id"])


def fill_fields(page,fields,prefix,values):
    for f in fields:
        if f["type"]=="choice":
            page.locator('input[name="'+prefix+f["id"]+'"][value="'+str(values[f["id"]])+'"]').check()
        else:
            page.locator("#"+prefix+f["id"]).fill(str(values[f["id"]]))


def open_page(page,base,id,mode):
    page.goto(url(base,id,mode),wait_until="domcontentloaded")
    expect(page.locator("h1")).to_contain_text(data(id)["title"],timeout=15000)
    assert "academic hold" in page.locator(".hold").first.inner_text().lower()
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1")


def scenario(page,base,id,size,output):
    u=data(id)
    requests=[]
    page.on("request",lambda req: requests.append(req.url))
    open_page(page,base,id,"learn")
    expect(page.locator("#model-slider")).to_be_visible()
    expect(page.locator("section.worked")).to_have_count(3)
    old=page.locator("#model-output").inner_text()
    slider=page.locator("#model-slider")
    slider.fill(str(u["model"]["max"]))
    expect(page.locator("#model-output")).not_to_have_text(old)
    assert page.locator("img").count()>=1
    assert page.locator("img").first.evaluate("(i)=>i.complete&&i.naturalWidth>0")
    open_page(page,base,id,"practice")
    expect(page.locator("#save-first")).to_be_visible()
    assert not any("/post-"+id+".json" in x or id+"-solution.svg" in x for x in requests),requests
    assert page.locator("#next-hint").count()==0
    assert page.locator("#reveal").count()==0
    page.locator("#save-first").click()
    expect(page.locator("#ph03-status")).to_contain_text("Enter first-prediction")
    # Learner may skip all mandatory fields, but this never becomes a correct answer.
    press_skip(page,"first-prediction")
    press_skip(page,"first-reason")
    skip_fields(page,u["prompt"]["fields"],"first-")
    page.locator("#save-first").click()
    expect(page.locator("#ph03-status")).to_contain_text("First response saved",timeout=15000)
    assert any("/post-"+id+".json" in x for x in requests)
    assert not any(id+"-solution.svg" in x for x in requests)
    first=saved(page,id)
    assert first and first["data"]["first"]["prediction"] is None
    assert first["data"]["first"]["reason"] is None
    assert set(first["data"]["first"]["skipped"])=={
        "first-prediction","first-reason",
        *("first-"+f["id"] for f in u["prompt"]["fields"])
    }
    assert all(v is None for v in first["data"]["first"]["fields"].values())
    for n in range(1,4):
        page.locator("#next-hint").click()
        expect(page.locator(".hint")).to_have_count(n)
    page.locator("#reveal").click()
    expect(page.locator("#save-diagnosis")).to_be_visible(timeout=15000)
    assert any(id+"-solution.svg" in x for x in requests)
    expect(page.locator(".feedback").first).to_contain_text("First attempt contained explicit unanswered fields")
    press_skip(page,"diag-text")
    page.locator("#save-diagnosis").click()
    expect(page.locator("#save-repair")).to_be_visible()
    skip_fields(page,u["prompt"]["fields"],"repair-")
    press_skip(page,"repair-reason")
    page.locator("#save-repair").click()
    expect(page.locator("#save-boundary")).to_be_visible()
    skip_fields(page,u["prompt"]["boundaryFields"],"bound-")
    press_skip(page,"boundary-reason")
    page.locator("#save-boundary").click()
    expect(page.locator("#compare-boundary")).to_be_visible()
    page.locator("#compare-boundary").click()
    expect(page.locator("#record-return")).to_be_visible()
    expect(page.locator("#ph03-after")).to_contain_text("ungraded, no mastery credit")
    page.locator("#record-return").click()
    expect(page.locator("#ph03-after")).to_contain_text("Source status return recorded")
    page.reload(wait_until="domcontentloaded")
    expect(page.locator("#ph03-after")).to_contain_text("Source status return recorded")
    final=saved(page,id)["data"]
    assert final["first"]==first["data"]["first"],"Immutable first response changed"
    assert final["diagnosis"]["skipped"] is True
    assert final["repair"]["reason"] is None
    assert all(v is None for v in final["repair"]["fields"].values())
    assert final["boundary"]["reason"] is None
    assert all(v is None for v in final["boundary"]["fields"].values())
    assert final["sourceReturn"]["status"]=="SOURCE_AUTHENTICITY_HOLD"
    assert [x["kind"] for x in final["events"]]==[
        "first","hint","hint","hint","reveal","diagnosis",
        "repair","boundary","boundary-reveal","source-return"
    ]
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+1")
    assert page.locator("img").first.evaluate("(i)=>i.complete&&i.naturalWidth>0")
    page.screenshot(path=str(output/f"{id}-{size[0]}x{size[1]}-complete.png"),full_page=True)
    return {"unit":id,"viewport":size,"firstImmutable":True,"postFirstOnly":True,
            "noSkipCredit":True,"sourceStatus":"HOLD","eventCount":len(final["events"])}


def fully_answered_case(page,base,id):
    u=data(id)
    p=post(id)
    open_page(page,base,id,"practice")
    page.locator("#first-prediction").fill("I will choose a signed system and test its boundaries.")
    page.locator("#first-reason").fill("I will use the governing physical ledger, then check dimensions.")
    fill_fields(page,u["prompt"]["fields"],"first-",p["expected"])
    page.locator("#save-first").click()
    expect(page.locator("#reveal")).to_be_visible(timeout=15000)
    page.locator("#reveal").click()
    expect(page.locator(".feedback").first).to_contain_text("All structured values match")
    page.locator("#diag-text").fill("I checked the model against my own original steps.")
    page.locator("#save-diagnosis").click()
    expect(page.locator("#save-repair")).to_be_visible()
    fill_fields(page,u["prompt"]["fields"],"repair-",p["expected"])
    page.locator("#repair-reason").fill("Rebuild signed equation and independently check units.")
    page.locator("#save-repair").click()
    expect(page.locator("#save-boundary")).to_be_visible()
    fill_fields(page,u["prompt"]["boundaryFields"],"bound-",p["boundaryExpected"])
    page.locator("#boundary-reason").fill("Changing this condition changes the valid physical model.")
    page.locator("#save-boundary").click()
    expect(page.locator("#compare-boundary")).to_be_visible()
    page.locator("#compare-boundary").click()
    expect(page.locator("#ph03-after")).to_contain_text("Structured values match the author model")
    assert "written reasoning is NOT independently assessed" in page.locator("#ph03-after").inner_text()
    assert not saved(page,id)["data"]["first"]["skipped"]


def run():
    server=http.server.ThreadingHTTPServer(
        ("127.0.0.1",0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f"http://127.0.0.1:{server.server_port}/{BASE_PATH}"
    receipts=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for size in ((1000,1600),(1600,1000)):
                    for id in IDS:
                        context=browser.new_context(viewport={"width":size[0],"height":size[1]},
                                                    has_touch=True)
                        page=context.new_page()
                        receipts.append(scenario(page,base,id,size,ART))
                        context.close()
                # Positive controls are a separate storage context: every authored model/changed constraint.
                ctx=browser.new_context(viewport={"width":1280,"height":800})
                page=ctx.new_page()
                for id in IDS:
                    fully_answered_case(page,base,id)
                ctx.close()
                # Cooperative two-tab writes must not replace the first response.
                ctx=browser.new_context()
                a,b=ctx.new_page(),ctx.new_page()
                for pg in (a,b):
                    open_page(pg,base,"P01","practice")
                    pg.locator("#first-prediction").fill("Prediction from "+("A" if pg==a else "B"))
                    pg.locator("#first-reason").fill("My reasoning has a defined sign.")
                    skip_fields(pg,data("P01")["prompt"]["fields"],"first-")
                a.locator("#save-first").click()
                b.locator("#save-first").click()
                expect(a.locator("#ph03-status")).to_contain_text("First response saved",timeout=15000)
                expect(b.locator("#ph03-status")).to_contain_text("First response saved",timeout=15000)
                sa,sb=saved(a,"P01"),saved(b,"P01")
                assert sa["data"]["first"]==sb["data"]["first"]
                assert sa["data"]["first"]["prediction"] in ("Prediction from A","Prediction from B")
                receipts.append({"twoTabFirstImmutable":True})
                ctx.close()
                # Denied storage must not allow protected first attempt, even using Skip.
                ctx=browser.new_context()
                p=ctx.new_page()
                p.add_init_script("Storage.prototype.setItem=function(){throw Error('DENIED')}")
                p.goto(url(base,"P02","practice"))
                expect(p.locator(".hold")).to_contain_text("HOLD",timeout=15000)
                assert p.locator("#save-first").count()==0
                receipts.append({"storageDenied":"FAIL_CLOSED"})
                ctx.close()
                # Pin mismatch: modified answer bytes must not display hints/model.
                ctx=browser.new_context()
                p=ctx.new_page()
                p.route("**/post-P04.json",lambda route:route.fulfill(
                    status=200,content_type="application/json",
                    body=(DATA/"post-P04.json").read_bytes()+b"\n "))
                open_page(p,base,"P04","practice")
                press_skip(p,"first-prediction")
                press_skip(p,"first-reason")
                skip_fields(p,data("P04")["prompt"]["fields"],"first-")
                p.locator("#save-first").click()
                expect(p.locator(".hold").last).to_contain_text("Postattempt byte pin mismatch",timeout=15000)
                assert p.locator("#reveal").count()==0
                receipts.append({"tamperedPostBlob":"FAIL_CLOSED"})
                ctx.close()
                # Stored revision forgery is rejected.
                ctx=browser.new_context()
                p=ctx.new_page()
                open_page(p,base,"P05","practice")
                press_skip(p,"first-prediction")
                press_skip(p,"first-reason")
                skip_fields(p,data("P05")["prompt"]["fields"],"first-")
                p.locator("#save-first").click()
                expect(p.locator("#reveal")).to_be_visible()
                p.evaluate("""() => {const k=Object.keys(localStorage).find(k=>k.startsWith('G9V41:PH03:R3:P05:'));
                  const x=JSON.parse(localStorage.getItem(k));x.revision='INVALID';
                  localStorage.setItem(k,JSON.stringify(x))}""")
                p.reload(wait_until="domcontentloaded")
                expect(p.locator(".hold").last).to_contain_text("Invalid revision-bound record",timeout=15000)
                receipts.append({"tamperedRevision":"FAIL_CLOSED"})
                ctx.close()
            finally:
                browser.close()
        (ART/"receipt.json").write_text(json.dumps({
            "mode":"AUTHOR_EXPOSED_TECHNICAL_ONLY","academic":"HOLD",
            "authenticOriginalsAdmitted":0,"newPairs":6,"allNativePairs":7,
            "results":receipts},indent=2)+"\n")
    finally:
        server.shutdown()


if __name__=="__main__":
    run()

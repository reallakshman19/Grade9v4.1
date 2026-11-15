#!/usr/bin/env python3
"""Adversarial HTTP Chromium QA of PH11-07 native candidate, not academic acceptance."""
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REL = "/nsejs/physics/curriculum/topics/PH11/subtopics/PH11-07/"
OUT = ROOT / "review-artifacts" / "physics-ph11-native-r4"

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def log_message(self, *_args):
        pass

def ready(page):
    page.locator("#source-panel").wait_for(state="visible", timeout=25000)
    assert "PIN_MISMATCH" not in page.locator("#status").inner_text()

def source(page, answer="I see a series resistor feeding two parallel branches, so a drop exists upstream."):
    page.locator("#source-model").select_option("mixed")
    page.locator("#source-reason").fill(answer)
    page.locator("#save-source").click()
    page.locator("#study-panel").wait_for(state="visible")

def predict(page):
    page.locator("#predict").fill("The measured source current and the known branch constrain the missing branch.")
    page.locator("#save-prediction").click()
    page.locator("#first-panel").wait_for(state="visible")

def first(page, model="mixed", r="2", v="6", known="1", unknown="3", reason=None):
    page.locator("#task-model").select_option(model)
    for id_,val in [("r",r),("v",v),("known",known),("unknown",unknown)]:
        page.locator("#"+id_).fill(val)
    page.locator("#first-reason").fill(reason or "I used node-pair voltage after the series drop, then conserved junction current and checked both equations.")
    page.locator("#save-first").click()
    page.locator("#reconstruct-panel").wait_for(state="visible",timeout=25000)

def advance_to_boundary(page):
    assert page.locator("#return-panel").is_hidden()
    page.locator("#open-reconstruct").click()
    page.locator("#reconstruct-model").wait_for(state="visible")
    page.locator("#reconstruct-response").fill("I compare the first original selected model, the first voltage drop and both branch currents.")
    page.locator("#save-reconstruction").click()
    page.locator("#diagnose-panel").wait_for(state="visible")
    page.locator("#diagnosis-evidence").fill("The frozen original model selection and the numeric voltage value give the first divergence.")
    page.locator("#save-diagnosis").click()
    page.locator("#repair-panel").wait_for(state="visible")
    page.locator("#repair-answer").fill("I correct the node-pair drop and separately check KCL and source-loop voltage balance.")
    page.locator("#save-repair").click()
    page.locator("#boundary-panel").wait_for(state="visible")

def submit_boundary(page,prefix,high,low,lower,upper):
    page.locator("#"+prefix+"high").select_option(high)
    page.locator("#"+prefix+"low").select_option(low)
    page.locator("#"+prefix+"lower").fill(lower)
    page.locator("#"+prefix+"upper").fill(upper)
    page.locator("#"+prefix+"reason").fill("Only a finite positive unknown R is allowed, so the block equivalent is strictly between zero and the fixed branch.")

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),QuietHandler)
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    url=f"http://127.0.0.1:{server.server_port}"+REL+"core1b.html"
    receipt={"mode":"AUTHOR_EXPOSED_TECHNICAL_ONLY","source_authenticity":"HOLD",
             "independent_qrt":"NOT_RUN","b1_b7":"HOLD","owner_release":"HOLD",
             "cases":[]}
    try:
        # Stage graph is an unsigned diagnostic candidate, not a production
        # manifest. Refuse unexpected review assets and mismatched Git objects.
        import hashlib
        stage=json.loads((ROOT/"review/physics/ph11-07-r4/NATIVE_PUBLICATION_STAGING_MANIFEST_R4.json").read_text())
        assert stage["release_manifest_authority"]=="NONE_NO_SIGNATURE"
        assert len(stage["dependencies"])==6
        for dep in stage["dependencies"]:
            data=(ROOT/dep["path"]).read_bytes()
            expected=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
            assert expected==dep["git_blob_sha"]
            assert not dep["path"].startswith("review/")
        receipt["stage_deps"]=len(stage["dependencies"])
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for viewport in [{"width":1280,"height":800},{"width":1000,"height":1600},{"width":1600,"height":1000}]:
                    context=browser.new_context(viewport=viewport,has_touch=True)
                    page=context.new_page()
                    requests=[]
                    page.on("request",lambda req:requests.append(req.url))
                    response=page.goto(url,wait_until="domcontentloaded")
                    assert response and response.status==200
                    ready(page)
                    # All staged candidate paths resolve through HTTP; none
                    # requires review/ or an author adapter for normal use.
                    for dep in stage["dependencies"]:
                        response=context.request.get(f"http://127.0.0.1:{server.server_port}/"+dep["path"])
                        assert response.status==200,dep["path"]
                    assert not any("postattempt.v1.json" in x for x in requests)
                    assert any("prompt.v1.json" in x for x in requests)
                    assert "review/physics" not in page.content()
                    assert "topic-adapter.PH11" not in page.content()
                    assert page.locator("iframe").count()==0
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
                    source(page)
                    assert not any("postattempt.v1.json" in x for x in requests)
                    predict(page)
                    assert not any("postattempt.v1.json" in x for x in requests)
                    assert page.locator("#reconstruct-panel").is_hidden()
                    first(page,model="all_parallel")  # correct values, WRONG model
                    assert any("postattempt.v1.json" in x for x in requests)
                    page.locator("#open-reconstruct").click()
                    page.locator("#reconstruct-model").wait_for(state="visible")
                    page.reload(wait_until="domcontentloaded")
                    page.locator("#reconstruct-panel").wait_for(state="visible")
                    assert page.locator("#source-panel").is_hidden()
                    assert page.locator("#first-panel").is_hidden()
                    assert page.locator("#reconstruct-model").is_visible()
                    page.locator("#reconstruct-response").fill("I obtained the correct values while selecting an inconsistent graph, so I must repair the model.")
                    page.locator("#save-reconstruction").click()
                    page.locator("#diagnose-panel").wait_for(state="visible")
                    assert "numeric values match" in page.locator("#diagnosis-text").inner_text()
                    page.locator("#diagnosis-evidence").fill("My original choice said all resistors connect directly to the source, contrary to the series element.")
                    page.locator("#save-diagnosis").click()
                    page.locator("#repair-panel").wait_for(state="visible")
                    page.locator("#repair-answer").fill("The proper series drop is 12 V and the parallel block has 6 V; the branch currents sum to 4 A.")
                    page.locator("#save-repair").click()
                    page.locator("#boundary-panel").wait_for(state="visible")
                    submit_boundary(page,"boundary-","yes","yes","1","7")
                    page.locator("#save-boundary").click()
                    page.locator("#boundary-repair-panel").wait_for(state="visible")
                    assert page.locator("#return-panel").is_hidden()
                    submit_boundary(page,"correct-","no","no","2","6")
                    page.locator("#save-boundary-repair").click()
                    page.locator("#return-panel").wait_for(state="visible")
                    page.locator("#source-return").fill("For the original 9 V circuit the 3-ohm series resistor and 6||6-ohm block total 6 ohms, giving 1.5 A and 4.5 V across the branches.")
                    page.locator("#save-return").click()
                    page.locator("#complete-panel").wait_for(state="visible")
                    raw=page.evaluate("""() => {
                       const k=Object.keys(localStorage).find(k=>k.startsWith('g9:ph11-07:r4:')&&!k.endsWith(':probe'));
                       return JSON.parse(localStorage.getItem(k));
                    }""")
                    assert raw["source"]["reason"].startswith("I see a series")
                    assert raw["prediction"]["answer"].startswith("The measured")
                    assert raw["first"]["model"]=="all_parallel"
                    assert raw["boundary"]["checked"] is False
                    assert raw["boundaryRepair"]["checked"] is True
                    assert raw["boundaryRepair"]["assisted"] is True
                    assert raw["sourceReturn"]
                    assert raw["seq"]==10,raw["seq"]
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
                    receipt["cases"].append({"viewport":viewport,"result":"PASS",
                         "first_source_separate":True,"prediction_separate":True,
                         "answer_network_delayed":True,"correct_value_wrong_model":"DIAGNOSED",
                         "incorrect_boundary_locked":True,"corrected_boundary_assisted":True})
                    context.close()

                # Cooperating concurrent tabs cannot overwrite the first source record.
                context=browser.new_context()
                p1=context.new_page()
                p2=context.new_page()
                p2.add_init_script("window.addEventListener('storage',e=>e.stopImmediatePropagation(),true)")
                p1.goto(url,wait_until="domcontentloaded");ready(p1)
                p2.goto(url,wait_until="domcontentloaded");ready(p2)
                source(p1,answer="ORIGINAL WINNER first source model and reasoning is saved in the browser.")
                p2.locator("#source-model").select_option("direct")
                p2.locator("#source-reason").fill("LOSER second tab alternative source model and reasoning must not overwrite.")
                p2.locator("#save-source").click()
                p2.locator("#study-panel").wait_for(state="visible")
                original=p2.evaluate("""() => {
                   const k=Object.keys(localStorage).find(k=>k.startsWith('g9:ph11-07:r4:'));
                   return JSON.parse(localStorage.getItem(k)).source.reason
                }""")
                assert original.startswith("ORIGINAL WINNER"),original
                # Challenge race: predict on one tab, reload both to capture the
                # same uncommitted challenge stage, then freeze competing writes.
                predict(p1)
                p2.reload(wait_until="domcontentloaded")
                p2.locator("#first-panel").wait_for(state="visible")
                p1.locator("#first-panel").wait_for(state="visible")
                first(p1,model="mixed",r="2",v="6",known="1",unknown="3")
                p2.locator("#task-model").select_option("all_parallel")
                for id_,val in [("r","10"),("v","18"),("known","3"),("unknown","1")]:
                    p2.locator("#"+id_).fill(val)
                p2.locator("#first-reason").fill("LOSER from the concurrent second tab; must never replace the committed first answer.")
                p2.locator("#save-first").click()
                p2.wait_for_function("document.querySelector('#status').textContent.includes('Another tab committed')",timeout=15000)
                p2.reload(wait_until="domcontentloaded")
                p2.locator("#reconstruct-panel").wait_for(state="visible",timeout=25000)
                same=p2.evaluate("""() => {
                   const k=Object.keys(localStorage).find(k=>k.startsWith('g9:ph11-07:r4:'));
                   return JSON.parse(localStorage.getItem(k)).first
                }""")
                assert same["model"]=="mixed"
                assert "LOSER" not in same["reason"]
                receipt["two_tab_source_and_first"] = "PASS_NO_OVERWRITE"
                context.close()

                # A source-shaped but modified answer is rejected by both pinned hashes.
                context=browser.new_context()
                page=context.new_page()
                fake=json.loads((ROOT/(REL.lstrip("/")+"postattempt.v1.json")).read_text())
                fake["reconstruct"][0] += " Modified without a code pin."
                page.route("**/postattempt.v1.json",lambda route:route.fulfill(
                  status=200,content_type="application/json",body=json.dumps(fake)))
                page.goto(url,wait_until="domcontentloaded");ready(page)
                source(page);predict(page)
                page.locator("#task-model").select_option("mixed")
                for id_,val in [("r","2"),("v","6"),("known","1"),("unknown","3")]:
                    page.locator("#"+id_).fill(val)
                page.locator("#first-reason").fill("I know the node voltage and conserved branch currents and check both.")
                page.locator("#save-first").click()
                page.wait_for_function("document.querySelector('#status').textContent.includes('PIN_MISMATCH')",timeout=20000)
                assert page.locator("#open-reconstruct").is_disabled()
                receipt["modified_well_shaped_asset"] = "PASS_FAIL_CLOSED"
                context.close()

                # Another negative: source-first cannot start if writable storage denied.
                context=browser.new_context()
                context.add_init_script(
                  "Object.defineProperty(window,'localStorage',{get(){throw Error('Storage denied')}})")
                page=context.new_page();page.goto(url,wait_until="domcontentloaded")
                page.wait_for_function("document.querySelector('#status').textContent.includes('HOLD')",timeout=15000)
                assert page.locator("#save-source").is_disabled()
                receipt["storage_denied"] = "PASS_FAIL_CLOSED"
                context.close()
            finally:
                browser.close()
        receipt["status"]="PASS"
    except Exception as exc:
        receipt["status"]="FAIL";receipt["error"]=repr(exc)
        raise
    finally:
        (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
        server.shutdown();thread.join(timeout=5)

if __name__=="__main__":
    run()

"""P00 B02 native HTML review-only QA. 47 tasks × two tablet orientations.

Running this provides no academic/QRT qualification. The SVG stages are
deliberately POST-COMMIT ONLY pending independent R02 review.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8793/nsejs/chemistry/textbook/index.html"
B02 = ROOT / "curriculum" / "chemistry" / "agent-b"
OUTPUT = ROOT / "chemistry-p00-browser-evidence"
OUTPUT.mkdir(exist_ok=True)
VIEWS = {"landscape": (1600, 1000), "portrait": (1000, 1600)}


def jsfile(path):
    return json.loads(path.read_text(encoding="utf-8"))


def inventory():
    stages = jsfile(B02 / "qrt/B02-C10-C11-staged-visuals.v0.7.0.json")
    supplemental = jsfile(B02 / "qrt/B02-core2-targeted-transfers.v0.5.0.json")
    all_tasks = {}
    for unit in ("C10", "C11"):
        for task in jsfile(B02 / f"core1b/{unit}.core1b.v0.1.0.json")["cycles"]:
            all_tasks[task["cycle_id"]] = (unit, task["subtopic_ref"], "native")
    for task in supplemental["records"]:
        unit = task["subtopic_id"].split(".")[0].replace("CHEM-", "")
        all_tasks[task["task_id"]] = (unit, task["subtopic_id"], "supplemental")
    assert len(all_tasks) == 47
    assert len(stages["records"]) == 47
    assert {r["task_id"] for r in stages["records"]} == set(all_tasks)
    return all_tasks, stages


def check(cond, label):
    if not cond:
        raise AssertionError(label)


def wait_loaded(page, expected_id):
    page.locator("#original-answer").wait_for(timeout=25000)
    check(page.locator("#task-select").input_value() == expected_id,
          f"Wrong task selected: expected {expected_id}")
    check(page.locator("#notice").inner_text().find("FAIL_CLOSED") == -1,
          "Reader rejected trusted B02 files")
    check(page.locator(".stage").count() >= 2, "Missing predict/attempt stages")
    check(page.locator(".stage-figure").count() == 0, "Unreviewed visual leaked precommit")
    check(page.locator("text=Model response · POST-COMMIT").count() == 0,
          "Worked model leaked precommit")
    check(page.locator("text=S1–S3 candidate visual support (post-commit only)").count() == 0,
          "Unreviewed stage controls leaked precommit")
    dims=page.evaluate("() => ({width:document.documentElement.scrollWidth, inner:innerWidth})")
    check(dims["width"]<=dims["inner"]+3, f"Horizontal overflow {dims}")


def visit_task(page, unit, subtopic, task_id, orientation, run_stages):
    from urllib.parse import urlencode

    url = BASE + "?" + urlencode({
        "unit": unit, "subtopic": subtopic, "mode": "practice", "task": task_id
    })
    response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
    check(response is not None and response.status == 200, f"HTTP route {task_id}")
    wait_loaded(page, task_id)
    if not run_stages:
        return 0
    page.locator("#prediction-answer").fill(
        "I expect the proposed model needs testing against the measured conditions."
    )
    page.locator("#original-answer").fill(
        f"First independent reasoning for {task_id}: compare scientific observations, "
        "select a bounded explanation, and check a counterexample."
    )
    page.locator("#commit-attempt").click()
    page.locator("text=Model response · POST-COMMIT").wait_for(timeout=15000)
    check(page.locator("#original-answer").evaluate("(e) => e.readOnly"), "First answer not locked")
    check(page.locator(".stage-figure").count() == 0,
          "Visual should require explicit postcommit selection")
    revealed = 0
    for num,role in [("S1","CLARIFY"),("S2","CORRELATE"),("S3","OPEN_THE_WAY")]:
        trigger = page.get_by_role("button", name=f"Inspect {num} · {role} (unreviewed)")
        trigger.click()
        figure = page.locator(".stage-figure").nth(revealed)
        figure.locator("img").wait_for(timeout=15000)
        page.wait_for_function(
            """i => { const e=document.querySelectorAll('.stage-figure img')[i];
                       return !!e && e.complete && e.naturalWidth > 0; }""",
            arg=revealed, timeout=15000)
        check(figure.locator("img").get_attribute("alt").startswith(num+" "+role),
              f"Missing accessible stage description {task_id} {num}")
        revealed += 1
    check(page.locator(".stage-figure").count() == 3,
          f"Not all 3 stage assets displayed for {task_id}")
    check("STAGE_ASSET" not in page.locator("#notice").inner_text(),
          "Stage asset failed validation")
    return revealed


def check_revision_protection(page, ids):
    first = next(k for k,v in ids.items() if v[0]=="C10" and v[2]=="native")
    unit, subtopic, _ = ids[first]
    from urllib.parse import urlencode
    route = BASE + "?" + urlencode({
        "unit":unit, "subtopic":subtopic, "mode":"practice", "task":first
    })
    page.goto(route)
    page.locator("#original-answer").wait_for()
    check(page.locator("#original-answer").evaluate("(e) => e.readOnly"),
          "Original answer should survive unchanged refresh")
    stored = page.evaluate("""id => Object.keys(localStorage)
        .filter(k => k.startsWith("g9chem:attempt:v2:"+id+":"))
        .map(k => [k, JSON.parse(localStorage.getItem(k))])""", first)
    check(len(stored)==1, "Expected one original committed revision")
    first_text=stored[0][1]["attempt"]
    check(first_text in page.locator("#original-answer").input_value(),
          "Refresh overwrote the original answer")
    # This mutation changes only Core1A teaching, not attempt.prompt or model.
    # A partial task-only hash would incorrectly reuse the saved response.
    def mutate(route):
        response = route.fetch()
        book = response.json()
        book["sections"][0]["teaching"][0] += " P00 controlled revision mutation."
        route.fulfill(status=200, content_type="application/json", body=json.dumps(book))
    page.route("**/curriculum/chemistry/agent-b/learner/C10.reader.v0.1.0.json", mutate)
    page.goto(route)
    page.locator("#commit-attempt").wait_for(timeout=15000)
    check(not page.locator("#original-answer").evaluate("(e) => e.readOnly"),
          "Changed lesson incorrectly reused first attempt")
    check(page.locator(".stage-figure").count()==0, "Revised task exposed old visuals")
    preserved=page.evaluate("""id => Object.keys(localStorage)
        .filter(k => k.startsWith("g9chem:attempt:v2:"+id+":"))
        .map(k => JSON.parse(localStorage.getItem(k)).attempt)""", first)
    check(first_text in preserved, "Old revision attempt was erased")
    page.unroute("**/curriculum/chemistry/agent-b/learner/C10.reader.v0.1.0.json")


def check_help_and_source_return(browser, ids):
    first = next(k for k,v in ids.items() if v[0]=="C10" and v[2]=="native")
    unit,subtopic,_=ids[first]
    from urllib.parse import urlencode
    context=browser.new_context(viewport={"width":1000,"height":1600},has_touch=True)
    page=context.new_page()
    route=BASE+"?"+urlencode({"unit":unit,"subtopic":subtopic,
                              "mode":"practice","task":first,
                              "return":"../index.html","source":"CHEM-C10-TEST"})
    page.goto(route);wait_loaded(page,first)
    check(page.locator("#source-return a").count()==1,"Safe Chemistry source return absent")
    check(page.locator("#source-return a").get_attribute("href").endswith(
        "/nsejs/chemistry/index.html"),"Wrong source return destination")
    page.get_by_role("button",name="Reveal H1 (assisted, logged)").click()
    check("H1:" in page.locator(".task-actions").inner_text(),"H1 not exposed")
    check(page.locator("text=Model response · POST-COMMIT").count()==0,
          "H1 exposed solution prematurely")
    page.locator("#prediction-answer").fill("I predict the observation needs a carrier model.")
    page.locator("#original-answer").fill(
        "With one hint, I compare competing charge-carrier explanations and test conditions.")
    page.locator("#commit-attempt").click()
    page.locator("text=Model response · POST-COMMIT").wait_for()
    check("H1" in page.locator(".saved").locator("xpath=..").inner_text(),
          "Assisted attempt status omitted")
    keys=page.evaluate("""id => Object.keys(localStorage).filter(
      k => k.startsWith("g9chem:attempt:v2:"+id+":")).map(k=>JSON.parse(
      localStorage.getItem(k)))""",first)
    check(len(keys)==1 and keys[0]["help_exposure"]==["H1"],"Help exposure not bound")
    page.goto(BASE+"?unit=C10&mode=practice&task=INVENTED-TASK")
    page.locator("text=UNKNOWN_TASK_HOLD").wait_for(timeout=15000)
    page.goto(BASE+"?unit=C10&mode=study&return=https%3A%2F%2Fevil.example%2F")
    page.locator("#lesson h2").wait_for(timeout=15000)
    check(page.locator("#source-return a").count()==0,
          "Cross-origin source-return link accepted")
    context.close()


def check_storage_disabled(browser,ids):
    first=next(k for k,v in ids.items() if v[0]=="C11" and v[2]=="native")
    unit,subtopic,_=ids[first]
    ctx=browser.new_context(viewport={"width":1000,"height":1600})
    ctx.add_init_script("""Object.defineProperty(window,'localStorage',
      {configurable:true,get(){throw Error('storage disabled');}});""")
    page=ctx.new_page()
    from urllib.parse import urlencode
    page.goto(BASE+"?"+urlencode({"unit":unit,"subtopic":subtopic,
                                  "mode":"practice","task":first}))
    page.locator("text=Storage unavailable").first.wait_for(timeout=15000)
    check(page.locator("#commit-attempt").count()==0,
          "Model reveal must fail closed without persistent storage")
    check(page.locator(".stage-figure").count()==0,"Unreviewed stage leaked")
    ctx.close()


def check_task_only_deep_link_and_history(browser,ids):
    from urllib.parse import urlencode
    native=[(task_id,v) for task_id,v in ids.items()
            if v[0]=="C10" and v[1]=="CHEM-C10.01" and v[2]=="native"]
    assert len(native)==3
    task_a=native[0][0]
    task_b=native[1][0]
    context=browser.new_context(viewport={"width":1000,"height":1600},has_touch=True)
    page=context.new_page()
    # A task-only link must locate its owning subtopic and choose practice mode.
    page.goto(BASE+"?"+urlencode({"unit":"C10","task":task_a}))
    wait_loaded(page,task_a)
    page.locator("#task-select").select_option(task_b)
    wait_loaded(page,task_b)
    check("task="+task_b in page.url,"Task selection did not update URL")
    page.go_back()
    wait_loaded(page,task_a)
    check("task="+task_a in page.url,"Browser back did not restore the task")
    # Two rapid unit switches should never permit an old fetch to win.
    page.locator("#unit-select").select_option("C11")
    page.locator("#unit-select").select_option("C10")
    page.locator("#lesson .eyebrow").wait_for(timeout=20000)
    check(page.locator("#lesson .eyebrow").inner_text().startswith("CHEM-C10."),
          "Asynchronous C11 response polluted final C10 route")
    context.close()


def check_visual_blob_tampering_fail_closed(browser,ids):
    from urllib.parse import urlencode
    task_id=next(k for k,v in ids.items() if v[0]=="C11" and v[2]=="native")
    unit,subtopic,_=ids[task_id]
    context=browser.new_context(viewport={"width":1600,"height":1000})
    page=context.new_page()
    page.goto(BASE+"?"+urlencode({"unit":unit,"subtopic":subtopic,
                                  "mode":"practice","task":task_id}))
    wait_loaded(page,task_id)
    page.locator("#prediction-answer").fill(
        "My prediction is conditional on charge carriers and observed state."
    )
    page.locator("#original-answer").fill(
        "I independently compare the microscopic models and test the supplied conditions."
    )
    page.locator("#commit-attempt").click()
    page.locator("text=Model response · POST-COMMIT").wait_for()
    def tamper(route):
        route.fulfill(status=200,content_type="image/svg+xml",body=(
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<title>Corrupted staged asset</title><desc>Untrusted image</desc></svg>'
        ))
    page.route("**/curriculum/chemistry/agent-b/figures/b02-stages/*.svg",tamper)
    page.get_by_role("button",name="Inspect S1 · CLARIFY (unreviewed)").click()
    page.locator("#notice").get_by_text("STAGE_BLOB_MISMATCH_HOLD",exact=False).wait_for(
        timeout=15000)
    check(page.locator(".stage-figure").count()==0,
          "Tampered asset was rendered despite blob digest mismatch")
    exposed=page.evaluate("""id => Object.keys(localStorage)
      .filter(k=>k.startsWith("g9chem:stage-exposure:v2:"+id+":"))""",task_id)
    check(not exposed,"Failed visual was incorrectly recorded as exposed")
    context.close()



def check_delayed_unit_load_never_renders_previous_pack(browser, ids):
    """Intercept a slow C11 book fetch and try to trigger old C10 mode controls."""
    from urllib.parse import urlencode
    task_id = next(k for k,v in ids.items() if v[0]=="C10" and v[2]=="native")
    unit,subtopic,_ = ids[task_id]
    ctx = browser.new_context(viewport={"width":1000,"height":1600}, has_touch=True)
    page = ctx.new_page()
    page.add_init_script("""(() => {
      const originalFetch = window.fetch.bind(window);
      window.fetch = (url, ...args) => {
        if (String(url).includes("learner/C11.reader.v0.1.0.json")) {
          return new Promise(resolve => setTimeout(
            () => resolve(originalFetch(url, ...args)), 1500));
        }
        return originalFetch(url, ...args);
      };
    })();""")
    page.goto(BASE+"?"+urlencode({
        "unit":unit,"subtopic":subtopic,"mode":"practice","task":task_id
    }))
    wait_loaded(page, task_id)
    check("CHEM-C10" in page.locator("#lesson").inner_text(),
          "C10 must exist before changing units")
    page.locator("#unit-select").select_option("C11")
    check(page.locator("#lesson").inner_text().startswith("Loading C11"),
          "Previous pack must be removed immediately during C11 loading")
    check(page.locator("#lesson").get_attribute("aria-busy")=="true",
          "Loading must be announced to assistive technology")
    check(page.locator("#show-practice").is_disabled()
          and page.locator("#show-study").is_disabled(),
          "Stale C10 mode actions must be disabled during pending load")
    check(page.locator("#original-answer").count()==0 and
          page.locator("#sections button").count()==0,
          "Stale task or section control remained during loading")
    # Even a programmatic click must not re-render the previous unit.
    page.evaluate("() => document.querySelector('#show-practice').click()")
    check(page.locator("#lesson").inner_text().startswith("Loading C11"),
          "Programmatic mode click exposed stale C10 while C11 loaded")
    page.locator("#lesson .eyebrow").wait_for(timeout=25000)
    check(page.locator("#lesson .eyebrow").inner_text().startswith("CHEM-C11."),
          "Final loaded content was not C11")
    check(page.locator("#lesson").get_attribute("aria-busy")=="false",
          "Successful load must clear the busy status")
    check(page.locator("#show-practice").is_enabled() and
          page.locator("#show-study").is_enabled(),
          "Successful load must restore the study/practice controls")
    ctx.close()


def check_stage_order_survives_refresh(browser, ids):
    """No S2 or S3 before a separately persisted predecessor exposure."""
    from urllib.parse import urlencode
    task_id = next(k for k,v in ids.items() if v[0]=="C10" and v[2]=="native")
    unit,subtopic,_ = ids[task_id]
    ctx=browser.new_context(viewport={"width":1600,"height":1000},has_touch=True)
    page=ctx.new_page()
    page.goto(BASE+"?"+urlencode({
        "unit":unit,"subtopic":subtopic,"mode":"practice","task":task_id
    }))
    wait_loaded(page,task_id)
    page.locator("#prediction-answer").fill(
        "The predicted trend depends on the correct chemical identity.")
    page.locator("#original-answer").fill(
        "I will compare the candidate mechanism with each observed fact.")
    page.locator("#commit-attempt").click()
    page.get_by_role("button",name="Inspect S1 · CLARIFY (unreviewed)").wait_for()
    s1=page.get_by_role("button",name="Inspect S1 · CLARIFY (unreviewed)")
    s2=page.get_by_role("button",name="Inspect S2 · CORRELATE (unreviewed)")
    s3=page.get_by_role("button",name="Inspect S3 · OPEN_THE_WAY (unreviewed)")
    check(s1.is_enabled() and s2.is_disabled() and s3.is_disabled(),
          "S2/S3 must not be available before S1")
    s1.click()
    page.locator(".stage-figure").first.wait_for(timeout=15000)
    check(s2.is_enabled() and s3.is_disabled(),
          "S1 should unlock only S2")
    page.reload()
    page.get_by_role("button",name="Inspect S2 · CORRELATE (unreviewed)").wait_for()
    check(page.get_by_role("button",name="Inspect S2 · CORRELATE (unreviewed)").is_enabled()
          and page.get_by_role("button",name="Inspect S3 · OPEN_THE_WAY (unreviewed)").is_disabled(),
          "S1 exposure must survive refresh without silently unlocking S3")
    page.get_by_role("button",name="Inspect S2 · CORRELATE (unreviewed)").click()
    page.locator(".stage-figure").first.wait_for(timeout=15000)
    check(page.get_by_role("button",name="Inspect S3 · OPEN_THE_WAY (unreviewed)").is_enabled(),
          "Persisted S2 exposure must unlock S3")
    page.get_by_role("button",name="Inspect S3 · OPEN_THE_WAY (unreviewed)").click()
    page.locator(".stage-figure").nth(1).wait_for(timeout=15000)
    entry=page.evaluate("""id => Object.keys(localStorage)
        .filter(k=>k.startsWith("g9chem:stage-exposure:v2:"+id+":"))
        .map(k=>JSON.parse(localStorage.getItem(k)))""",task_id)
    check(len(entry)==1 and entry[0]["levels"]==["S1","S2","S3"],
          "Exposure register must retain sequential S1/S2/S3 history")
    ctx.close()


def check_keyboard_only_read_attempt_and_stages(browser, ids):
    """Exercise real keyboard event paths at the portrait tablet viewport."""
    from urllib.parse import urlencode
    task_id = next(k for k,v in ids.items() if v[0]=="C11" and v[2]=="native")
    unit,subtopic,_ = ids[task_id]
    ctx=browser.new_context(viewport={"width":1000,"height":1600})
    page=ctx.new_page()
    page.goto(BASE+"?"+urlencode({
        "unit":unit,"subtopic":subtopic,"mode":"study",
        "return":"../index.html"
    }))
    page.locator("#lesson .eyebrow").wait_for(timeout=15000)
    link=page.locator("#source-return a")
    check(link.count()==1 and link.get_attribute("href").endswith("/nsejs/chemistry/index.html"),
          "Accessible source return missing")
    link.focus()
    check(page.evaluate("() => document.activeElement.tagName")=="A",
          "Source link cannot receive keyboard focus")
    page.locator("#show-practice").focus()
    page.keyboard.press("Enter")
    page.locator("#original-answer").wait_for(timeout=15000)
    page.locator("#task-select").select_option(task_id)
    check(page.locator("#task-select").input_value()==task_id,
          "Keyboard review target not selected")
    page.locator("#prediction-answer").focus()
    page.keyboard.type("I predict a change in this system under stated conditions.")
    page.keyboard.press("Tab")
    check(page.evaluate("() => document.activeElement.id")=="original-answer",
          "Tab from prediction must reach independent answer field")
    page.keyboard.type(
        "I compare the original mechanism against the changed experiment.")
    page.locator("#commit-attempt").focus()
    page.keyboard.press("Enter")
    page.get_by_role("heading",name="Stage 3 — Reconstruct").wait_for(timeout=15000)
    check(page.evaluate("() => document.activeElement.textContent")
          .startswith("Stage 3 — Reconstruct"),
          "Keyboard focus must move to newly revealed reconstruction")
    s1=page.get_by_role("button",name="Inspect S1 · CLARIFY (unreviewed)")
    s1.focus()
    page.keyboard.press("Enter")
    page.locator(".stage-figure").first.wait_for(timeout=15000)
    s2=page.get_by_role("button",name="Inspect S2 · CORRELATE (unreviewed)")
    check(s2.is_enabled(),"Keyboard S1 activation did not unlock S2")
    s2.focus()
    page.keyboard.press("Space")
    page.locator(".stage-figure").nth(1).wait_for(timeout=15000)
    s3=page.get_by_role("button",name="Inspect S3 · OPEN_THE_WAY (unreviewed)")
    s3.focus()
    page.keyboard.press("Enter")
    page.locator(".stage-figure").nth(2).wait_for(timeout=15000)
    check(page.evaluate("() => document.activeElement.tagName")=="BUTTON",
          "Stage keyboard control lost its focus unexpectedly")
    ctx.close()


def check_all_units_still_load(browser):
    ctx=browser.new_context(viewport={"width":1000,"height":1600})
    page=ctx.new_page()
    for unit in ("C08","C09","C12","C13","C14"):
        page.goto(BASE+"?unit="+unit+"&mode=study")
        page.locator("#lesson .eyebrow").wait_for(timeout=25000)
        check("UNREVIEWED" in page.locator("#lesson .eyebrow").inner_text(),
              f"Existing {unit} reader regressed")
    ctx.close()


def main():
    ids,_=inventory()
    server=subprocess.Popen(
      [sys.executable,"-m","http.server","8793","--bind","127.0.0.1"],
      cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen("http://127.0.0.1:8793/",timeout=1)
                break
            except Exception:
                time.sleep(0.25)
        else:
            raise RuntimeError("HTTP test server unavailable")
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(
              headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
            try:
                total_stages=0
                for orientation,(width,height) in VIEWS.items():
                    ctx=browser.new_context(viewport={"width":width,"height":height},
                                           has_touch=True)
                    page=ctx.new_page()
                    errors=[]
                    page.on("pageerror",lambda exc:errors.append(str(exc)))
                    for task_id,(unit,subtopic,kind) in ids.items():
                        total_stages+=visit_task(
                            page,unit,subtopic,task_id,orientation,
                            run_stages=(orientation=="landscape"))
                    check(not errors,f"Uncaught browser errors in {orientation}: {errors}")
                    if orientation=="landscape":
                        check_revision_protection(page,ids)
                    page.goto(BASE+"?unit=C11&mode=practice")
                    page.locator("#original-answer").wait_for(timeout=15000)
                    page.screenshot(path=str(OUTPUT/f"C11-{orientation}.png"),
                                    full_page=False)
                    ctx.close()
                check(total_stages==141,f"Expected 141 verified SVG displays, got {total_stages}")
                check_help_and_source_return(browser,ids)
                check_storage_disabled(browser,ids)
                check_all_units_still_load(browser)
                check_task_only_deep_link_and_history(browser,ids)
                check_visual_blob_tampering_fail_closed(browser,ids)
                check_delayed_unit_load_never_renders_previous_pack(browser,ids)
                check_stage_order_survives_refresh(browser,ids)
                check_keyboard_only_read_attempt_and_stages(browser,ids)
            finally:
                browser.close()
        print(
          "PASS: 47 unique native task deep links at both 12.7-inch orientations; "
          "141/141 verified postcommit SVG renderings, 39 native+8 supplemental; "
          "unit, subtopic, task, return, H1 exposure, first-attempt refresh, "
          "full lesson revision mutation, disabled storage and other five units. "
          "No academic/QRT/source qualification inferred.")
    finally:
        server.terminate()
        server.wait(timeout=10)


if __name__=="__main__":
    main()

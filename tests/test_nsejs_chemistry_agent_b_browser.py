"""Real Chromium regression for the non-released Chemistry textbook preview."""
from __future__ import annotations
import contextlib
import json
import os
from pathlib import Path
import socket
import subprocess
import time
import urllib.request
import pytest
sync_playwright = pytest.importorskip("playwright.sync_api", reason="Dedicated Chromium workflow installs Playwright").sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PORT=8765
URL=f"http://127.0.0.1:{PORT}/nsejs/chemistry/textbook/index.html"

@pytest.fixture(scope="module")
def server():
    proc=subprocess.Popen(["python3","-m","http.server",str(PORT),"--bind","127.0.0.1"],cwd=ROOT,
                          stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(URL,timeout=1).read(12)
                break
            except Exception:
                time.sleep(.12)
        else:
            raise AssertionError("Local HTTP server failed to start")
        yield
    finally:
        proc.terminate()
        with contextlib.suppress(Exception):
            proc.wait(timeout=5)

@pytest.fixture(scope="module")
def browser(server):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True)
        try:yield b
        finally:b.close()

def open_page(browser,unit="C08",width=1600,height=1000,disable_storage=False):
    ctx=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1,
                            has_touch=True)
    if disable_storage:
        ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('storage disabled')}});")
    page=ctx.new_page()
    page.goto(URL+"?unit="+unit)
    page.get_by_role("heading",name="Chemistry — learn, then try it independently").wait_for()
    page.get_by_role("heading",name="Inside this chapter").wait_for()
    page.wait_for_function("document.querySelectorAll('#sections button').length>0")
    return ctx,page

@pytest.mark.parametrize("unit,count",[
    ("C08",6),("C09",6),("C10",6),("C11",7),("C12",5),("C13",5),("C14",5)])
@pytest.mark.parametrize("viewport",[(1600,1000),(1000,1600)])
def test_all_unit_navigation_and_tablet_viewports(browser,unit,count,viewport):
    ctx,page=open_page(browser,unit,*viewport)
    try:
        assert page.locator("#sections button").count()==count
        assert page.get_by_role("heading",level=2).count()>=2
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 3")
        assert page.locator("header").is_visible()
        assert page.locator(".banner").is_visible()
        assert page.locator("#unit-select").input_value()==unit
        page.locator("#show-practice").click()
        page.get_by_role("heading",name="Stage 1 — Predict").wait_for()
        assert page.locator("#task-select option").count()==3
        assert page.get_by_role("heading",name="Stage 3 — Reconstruct").count()==0
        assert page.locator("#commit-attempt").is_visible()
    finally:
        ctx.close()

def read_pinned_v2_attempt(page, task_id):
    """Read only the exact current v2 first attempt; reject ambiguous records."""
    return page.evaluate("""taskId => {
      const prefix='g9chem:attempt:v2:'+taskId+':';
      const keys=[];
      for(let i=0;i<localStorage.length;i++){
        const k=localStorage.key(i);
        if(k && k.startsWith(prefix))keys.push(k);
      }
      if(keys.length!==1)throw new Error('Missing or ambiguous v2 attempt');
      return JSON.parse(localStorage.getItem(keys[0]));
    }""", task_id)

def test_persisted_original_first_attempt_and_refresh(browser):
    ctx,page=open_page(browser)
    try:
        page.locator("#show-practice").click()
        page.get_by_role("heading",name="Stage 2 — Independent attempt").wait_for()
        assert page.get_by_text("Model response · POST-COMMIT").count()==0
        page.locator("#prediction-answer").fill("I predict the closed-system mass remains conserved.")
        page.locator("#original-answer").fill("Magnesium combines with oxygen from the air, and the mass increase reflects oxygen uptake.")
        page.locator("#commit-attempt").click()
        page.get_by_text("Model response · POST-COMMIT").wait_for()
        assert page.locator("#original-answer").get_attribute("readonly") is not None
        record=read_pinned_v2_attempt(page, "CORE1B-C08-01-1")
        assert record["source_role"]=="AUTHORED_PRACTICE"
        assert record["attempt"].startswith("Magnesium")
        page.reload()
        page.locator("#show-practice").click()
        page.get_by_text("Model response · POST-COMMIT").wait_for()
        assert page.locator("#original-answer").input_value()==record["attempt"]
    finally:
        ctx.close()

def test_first_attempt_hint_exposure_persisted(browser):
    ctx,page=open_page(browser)
    try:
        page.locator("#show-practice").click()
        page.get_by_role("button",name="Reveal H1 (assisted, logged)").click()
        page.locator("#prediction-answer").fill("I will check which substance supplies oxygen.")
        page.locator("#original-answer").fill("The product oxygen comes from outside the open crucible; conservation applies to closed systems.")
        page.locator("#commit-attempt").click()
        page.get_by_text("Model response · POST-COMMIT").wait_for()
        row=read_pinned_v2_attempt(page, "CORE1B-C08-01-1")
        assert "H1" in row["help_exposure"]
        assert "INDEPENDENT" not in str(row)
    finally:
        ctx.close()

def test_disabled_storage_prevents_answer_reveal(browser):
    ctx,page=open_page(browser,disable_storage=True)
    try:
        page.locator("#show-practice").click()
        page.get_by_text("STORAGE_UNAVAILABLE").wait_for()
        assert page.get_by_text("Model response · POST-COMMIT").count()==0
        assert page.locator("#commit-attempt").count()==0
    finally:
        ctx.close()

def test_stale_revision_fails_closed_and_preserves_record(browser):
    ctx,page=open_page(browser)
    try:
        page.locator("#show-practice").click()
        page.get_by_role("heading",name="Stage 1 — Predict").wait_for()
        page.evaluate("""() => {
          const stale='0'.repeat(64);
          localStorage.setItem('g9chem:attempt:v2:CORE1B-C08-01-1:'+stale,
            JSON.stringify({revision:stale, prediction:'Old prediction preserved',
              attempt:'Old original kept', source_role:'AUTHORED_PRACTICE'}));
        }""")
        page.reload()
        page.locator("#show-practice").click()
        page.get_by_text("STALE_REVISION_HOLD").wait_for()
        assert page.get_by_text("Model response · POST-COMMIT").count()==0
        assert page.evaluate("JSON.parse(localStorage.getItem('g9chem:attempt:v2:CORE1B-C08-01-1:'+'0'.repeat(64))).attempt")=="Old original kept"
    finally:
        ctx.close()

def test_c09_figures_and_keyboard_focus(browser):
    ctx,page=open_page(browser,unit="C09",width=1000,height=1600)
    try:
        page.locator("#sections button").nth(1).click()
        page.locator('img[src*="C09-neutralisation.svg"]').wait_for()
        page.wait_for_function("Array.from(document.images).some(el => el.src.includes('C09-neutralisation.svg') && el.complete && el.naturalWidth > 0)")
        page.locator("#sections button").nth(5).click()
        page.locator('img[src*="C09-phosphorus-connectivity.svg"]').wait_for()
        page.wait_for_function("Array.from(document.images).some(el => el.src.includes('C09-phosphorus-connectivity.svg') && el.complete && el.naturalWidth > 0)")
        page.locator("#show-practice").click()
        page.get_by_role("heading",name="Stage 1 — Predict").wait_for()
        page.locator("#unit-select").focus()
        assert page.evaluate("document.activeElement.id")=="unit-select"
        page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement.id")=="task-select"
    finally:
        ctx.close()


@pytest.mark.parametrize("unit,section,filename",[
    ("C08",0,"C08-reaction-atom-ledger.svg"),
    ("C10",2,"C10-ionic-mobility.svg"),
    ("C11",2,"C11-bond-order-hydrogens.svg"),
    ("C12",3,"C12-gas-phase-ledger.svg"),
    ("C13",2,"C13-electron-charge-ledger.svg"),
    ("C14",1,"C14-water-test-limits.svg")
])
def test_all_additional_diagram_assets_decode_in_browser(browser,unit,section,filename):
    ctx,page=open_page(browser,unit=unit,width=1000,height=1600)
    try:
        page.locator("#sections button").nth(section).click()
        page.wait_for_function(
            "(name) => Array.from(document.images).some(el => el.src.includes(name) && el.complete && el.naturalWidth>0)",
            arg=filename
        )
        assert page.locator("article .figure").count()>=1
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 3")
    finally:
        ctx.close()


# R4 author-exposed technical negative control; not B4 or independent QRT approval.
@pytest.mark.parametrize("unit,task_id", [
    ("C12","CORE1B-C12-01-1"),  # piston: pressure/volume constraints
    ("C09","CORE1B-C09-01-1"),  # acid ionisation, never hydrate
    ("C08","CORE1B-C08-04-1"),  # calcium-carbonate precipitation
    ("C08","CORE1B-C08-04-2"),  # silver-bromide precipitation
    ("C14","CORE1B-C14-02-1"), # boiling, nitrate and microbial checks
])
@pytest.mark.parametrize("viewport", [(1600,1000),(1000,1600)])
def test_r4_task_specific_hints_are_logged_and_model_hidden_until_commit(
        browser,unit,task_id,viewport):
    pack=json.loads((ROOT/"curriculum"/"chemistry"/"agent-b"/"core1b"/
                     f"{unit}.core1b.v0.1.0.json").read_text(encoding="utf-8"))
    task=next(t for t in pack["cycles"] if t["cycle_id"]==task_id)
    hints=[h["text"] for h in task["attempt"]["hints"]]
    ctx=browser.new_context(viewport={"width":viewport[0],"height":viewport[1]},
                            device_scale_factor=1,has_touch=True)
    try:
        page=ctx.new_page()
        page.goto(f"{URL}?unit={unit}&task={task_id}&mode=practice")
        page.get_by_role("heading",name="Stage 2 — Independent attempt").wait_for()
        assert page.locator("#task-select").input_value()==task_id
        assert page.get_by_text("Model response · POST-COMMIT").count()==0
        assert page.get_by_role("heading",name="Stage 3 — Reconstruct").count()==0
        assert not any(h in page.locator("#lesson").inner_text() for h in hints)
        for i,label in enumerate(("H1","H2","H3")):
            page.get_by_role("button",name=f"Reveal {label} (assisted, logged)").click()
            assert hints[i] in page.locator("#lesson").inner_text()
            assert all(h not in page.locator("#lesson").inner_text() for h in hints[i+1:])
            assert page.get_by_text("Model response · POST-COMMIT").count()==0
        page.locator("#prediction-answer").fill(
            "I will check the stated chemical or apparatus constraints before inference.")
        page.locator("#original-answer").fill(
            "My own first reasoning compares the specified measurements, the governing "
            "chemical or physical conservation law, and an independent test to falsify it.")
        page.locator("#commit-attempt").click()
        page.get_by_text("Model response · POST-COMMIT").wait_for()
        record=read_pinned_v2_attempt(page,task_id)
        assert record["help_exposure"]==["H1","H2","H3"]
        assert record["learner_status"]=="ASSISTED"
        assert record["source_role"]=="AUTHORED_PRACTICE"
        assert page.get_by_role("heading",name="Stage 3 — Reconstruct").count()==1
    finally:
        ctx.close()

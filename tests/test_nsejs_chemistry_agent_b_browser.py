"""Real Chromium regression for the non-released Chemistry textbook preview."""
from __future__ import annotations
import contextlib
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
    page.get_by_role("heading",name="Chemistry — textbook first, independent reasoning next").wait_for()
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
        page.get_by_role("button",name="Core1B independent practice").click()
        page.get_by_role("heading",name="Stage 1 — Predict").wait_for()
        assert page.locator("#task-select option").count()==3
        assert page.get_by_role("heading",name="Stage 3 — Reconstruct").count()==0
        assert page.locator("#commit-attempt").is_visible()
    finally:
        ctx.close()

def test_persisted_original_first_attempt_and_refresh(browser):
    ctx,page=open_page(browser)
    try:
        page.get_by_role("button",name="Core1B independent practice").click()
        page.get_by_role("heading",name="Stage 2 — Independent attempt").wait_for()
        assert page.get_by_text("Model response (post-commit)").count()==0
        page.locator("#prediction-answer").fill("I predict the closed-system mass remains conserved.")
        page.locator("#original-answer").fill("Magnesium combines with oxygen from the air, and the mass increase reflects oxygen uptake.")
        page.locator("#commit-attempt").click()
        page.get_by_text("Model response (post-commit)").wait_for()
        assert page.locator("#original-answer").get_attribute("readonly") is not None
        record=page.evaluate("JSON.parse(localStorage.getItem('g9chem:attempt:CORE1B-C08-01-1'))")
        assert record["source_role"]=="AUTHORED_PRACTICE"
        assert record["attempt"].startswith("Magnesium")
        page.reload()
        page.get_by_role("button",name="Core1B independent practice").click()
        page.get_by_text("Model response (post-commit)").wait_for()
        assert page.locator("#original-answer").input_value()==record["attempt"]
    finally:
        ctx.close()

def test_first_attempt_hint_exposure_persisted(browser):
    ctx,page=open_page(browser)
    try:
        page.get_by_role("button",name="Core1B independent practice").click()
        page.get_by_role("button",name="Reveal H1 (support exposure)").click()
        page.locator("#prediction-answer").fill("I will check which substance supplies oxygen.")
        page.locator("#original-answer").fill("The product oxygen comes from outside the open crucible; conservation applies to closed systems.")
        page.locator("#commit-attempt").click()
        page.get_by_text("Model response (post-commit)").wait_for()
        row=page.evaluate("JSON.parse(localStorage.getItem('g9chem:attempt:CORE1B-C08-01-1'))")
        assert "H1" in row["help_exposure"]
        assert "INDEPENDENT" not in str(row)
    finally:
        ctx.close()

def test_disabled_storage_prevents_answer_reveal(browser):
    ctx,page=open_page(browser,disable_storage=True)
    try:
        page.get_by_role("button",name="Core1B independent practice").click()
        page.get_by_text("STORAGE_UNAVAILABLE").wait_for()
        assert page.get_by_text("Model response (post-commit)").count()==0
        assert page.locator("#commit-attempt").count()==0
    finally:
        ctx.close()

def test_stale_revision_fails_closed_and_preserves_record(browser):
    ctx,page=open_page(browser)
    try:
        page.get_by_role("button",name="Core1B independent practice").click()
        page.get_by_role("heading",name="Stage 1 — Predict").wait_for()
        page.evaluate("""() => localStorage.setItem('g9chem:attempt:CORE1B-C08-01-1',
          JSON.stringify({revision:'0000000000000000000000000000000000000000000000000000000000000000',
          prediction:'Old attempt',attempt:'Old original kept'}))""")
        page.reload()
        page.get_by_role("button",name="Core1B independent practice").click()
        page.get_by_text("STALE_REVISION_HOLD").wait_for()
        assert page.get_by_text("Model response (post-commit)").count()==0
        assert page.evaluate("JSON.parse(localStorage.getItem('g9chem:attempt:CORE1B-C08-01-1')).attempt")=="Old original kept"
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
        page.get_by_role("button",name="Core1B independent practice").click()
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

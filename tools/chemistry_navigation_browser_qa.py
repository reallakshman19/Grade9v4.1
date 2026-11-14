"""NSEJS Chemistry 14-chapter navigation HTTP Chromium release check.

Grounded in the canonical registry; tests both the legacy C01-C07 preview reader
and native C08-C14 reader. Original authored content is NOT an authenticated
NSEJS exam-question admission.
"""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import urljoin
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE="http://127.0.0.1:8797/"
HOME=urljoin(BASE,"nsejs/chemistry/index.html")
MAP=urljoin(BASE,"nsejs/core2/question-map.html")
DATA=json.loads((ROOT/"nsejs/chemistry/learner-navigation.v1.json").read_text())
OUT=ROOT/"review-artifacts/chemistry-navigation"
OUT.mkdir(parents=True,exist_ok=True)
VIEWS={"tablet-portrait":{"width":1000,"height":1600},
       "tablet-landscape":{"width":1600,"height":1000}}

def ensure(value,claim):
    if not value:raise AssertionError(claim)

def loaded(page,unit):
    page.locator(".chem-journey-nav").first.wait_for(timeout=25000)
    ensure(page.locator(".chem-journey-nav").count()>=1,"missing shared learner steps "+unit)
    ensure(page.locator(".chem-journey-step").first.count()==1,"missing Learn step "+unit)
    ensure(page.locator(".chem-next").count()+page.locator(".chem-journey-edge").count()>=1,"missing next/edge "+unit)
    ensure(page.locator(".chem-journey-scope").first.inner_text().find("not necessarily readable original exam")>=0,
           "question map status misleading "+unit)
    width=page.evaluate("({scroll:document.documentElement.scrollWidth,inside:innerWidth})")
    ensure(width["scroll"]<=width["inside"]+3,f"horizontal overflow {unit}: {width}")

def source_url(item):
    return urljoin(HOME,item["chapter_href"])

def check_catalog(page,label):
    page.goto(HOME,wait_until="domcontentloaded",timeout=30000)
    page.locator("#chem-card-C14").wait_for(timeout=10000)
    ensure(page.locator(".chem-chapter-card").count()==14,"not 14 primary cards")
    ensure(page.locator("#chem-chapters details li a").count()==84,"not 84 subtopic links")
    ensure(page.locator("text=Peer-Audited Curriculum").count()==0,"misleading peer-reviewed badge")
    ensure(page.locator("#topicNav").count()==1,"legacy filter removed rather than demoted")
    page.screenshot(path=str(OUT/(label+"-chapters.png")),full_page=True)
    return [x.get_attribute("href") for x in page.locator("#chem-chapters details li a").all()]

def check_chapter(page,unit,chapter_href,label):
    page.goto(urljoin(HOME,chapter_href),wait_until="domcontentloaded",timeout=30000)
    loaded(page,unit)
    nav=page.locator(".chem-journey-nav").first
    ensure(nav.get_by_text("1 · Learn").count()==1,"Learn action missing "+unit)
    ensure(nav.get_by_text("2 · Try it").count()==1,"Try action missing "+unit)
    ensure(nav.get_by_text("3 · Exam practice / source status").count()==1,
           "Exam status action missing "+unit)
    ensure(nav.get_by_text("Need more help?").count()==1,"Help missing "+unit)
    ensure(nav.get_by_text("Chemistry chapters").count()==1,"chapter return missing "+unit)
    if unit in {"C01","C08","C14"}:
        page.screenshot(path=str(OUT/(label+"-"+unit+".png")),full_page=False)

def check_deep_links(page,links,label):
    count=0
    for href in links:
        page.goto(urljoin(HOME,href),wait_until="domcontentloaded",timeout=30000)
        loaded(page,href)
        if "curriculum/chemistry/preview" in href:
            ensure(page.locator("#chem-textbook .lesson").count()>=5,
                   "C01-C07 chapter sections absent: "+href)
        else:
            ensure(page.locator("#lesson h2").count()>=1,
                   "C08-C14 subtopic missing: "+href)
            ensure("FAIL_CLOSED" not in page.locator("#notice").inner_text(),"native reader fail closed: "+href)
        count+=1
        if count%14==0:print("CHEM_NAV_SUBTOPIC_PASS",label,count,flush=True)
    return count

def check_preview_practice(page):
    url=urljoin(HOME,"../../curriculum/chemistry/preview/C01.html?subtopic=CHEM-C01.01&mode=practice#practice-chem-c01-01")
    page.goto(url,wait_until="domcontentloaded",timeout=30000)
    page.locator("#practice-chem-c01-01 .attempt textarea").first.wait_for(timeout=25000)
    loaded(page,"C01/practice")
    first=page.locator("#practice-chem-c01-01")
    ensure(first.locator(".attempt details").first.is_hidden(),"preview hints leaked precommit")
    ensure(first.locator(".post").first.is_hidden(),"preview answer leaked precommit")
    first.locator("textarea").first.fill("An original independent attempt selecting a particle model and explaining the observation.")
    first.get_by_role("button",name="Save first attempt and reveal reconstruction").click()
    ensure(first.locator(".post").first.is_visible(),"preview reconstruction missing after commit")
    answer=first.locator("textarea").first.input_value()
    page.reload(wait_until="domcontentloaded")
    page.locator("#practice-chem-c01-01 .post").first.wait_for(timeout=25000,state="visible")
    ensure(page.locator("#practice-chem-c01-01 textarea").first.input_value()==answer,
           "C01 first answer not persisted on refresh")
    ensure(page.locator("#practice-chem-c01-01 textarea").first.is_disabled(),
           "C01 immutable first answer not locked")
    return True

def check_preview_storage_negative(browser,viewport):
    context=browser.new_context(viewport=viewport,has_touch=True)
    context.add_init_script("Storage.prototype.setItem=function(){throw new Error('storage blocked')}")
    page=context.new_page()
    url=urljoin(HOME,"../../curriculum/chemistry/preview/C02.html?subtopic=CHEM-C02.01&mode=practice")
    page.goto(url,wait_until="domcontentloaded")
    field=page.locator("#practice-chem-c02-01 textarea").first
    field.wait_for(timeout=25000)
    field.fill("First attempted reasoning cannot be recorded because browser storage is denied.")
    page.locator("#practice-chem-c02-01 button").first.click()
    ensure(page.locator("#practice-chem-c02-01 .post").first.is_hidden(),"storage failure revealed answer")
    ensure(page.locator("#practice-chem-c02-01 .attempt details").first.is_hidden(),"storage failure revealed hint")
    ensure(field.is_enabled(),"storage failure erased access to learner answer")
    ensure("Storage unavailable" in page.locator("#practice-chem-c02-01 .mini").last.inner_text(),
           "no storage failure message")
    context.close()
    return True

def check_cross_chapter(page):
    last="CHEM-C07.07"
    route=urljoin(HOME,"../../curriculum/chemistry/preview/C07.html?subtopic="+last+"#chem-c07-07")
    page.goto(route,wait_until="domcontentloaded")
    nav=page.locator("#chem-c07-07 > .chem-journey-nav")
    nav.wait_for(timeout=25000)
    next_url=nav.locator(".chem-next").get_attribute("href")
    ensure("unit=C08" in next_url and "subtopic=CHEM-C08.01" in next_url,"C07->C08 gap")
    nav.locator(".chem-next").click()
    loaded(page,"C08 cross-chapter")
    ensure("unit=C08" in page.url,"C08 next chapter not opened")
    prev=page.locator(".chem-journey-nav .chem-prev").get_attribute("href")
    ensure("C07.html" in prev and "CHEM-C07.07" in prev,"C08 previous chapter missing")
    return True

def check_native_practice_return(page):
    start=urljoin(HOME,"textbook/index.html?unit=C08&subtopic=CHEM-C08.01&mode=study")
    page.goto(start,wait_until="domcontentloaded")
    loaded(page,"C08")
    page.locator("#show-practice").click()
    page.locator("#original-answer").wait_for(timeout=25000)
    ensure("mode=practice" in page.url,"practice mode route not preserved")
    before=page.url
    page.locator(".chem-journey-nav .chem-exam-link").click()
    page.locator("#chemistry-lesson-return a").wait_for(timeout=25000)
    ensure(page.url.startswith(MAP),"question map not opened")
    return_link=page.locator("#chemistry-lesson-return a")
    ensure(return_link.get_attribute("href")==before,"exact subtopic/practice return lost")
    return_link.click()
    page.locator("#original-answer").wait_for(timeout=25000)
    ensure("mode=practice" in page.url and "subtopic=CHEM-C08.01" in page.url,"return lost student position")
    return True

def check_unsafe_return(page):
    page.goto(MAP+"?return=https%3A%2F%2Fevil.example%2Ffake%2Findex.html#chemistry")
    ensure(page.locator("#chemistry-lesson-return").count()==0,"unsafe external return accepted")
    return True

def main():
    server=subprocess.Popen([sys.executable,"-m","http.server","8797","--bind","127.0.0.1"],
                            cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    report={"schema":"chemistry-navigation-browser-r1","status":"TECHNICAL_QA_ONLY","viewports":{}}
    try:
        for _ in range(90):
            try:
                with urlopen(HOME,timeout=2) as r:
                    if r.status==200:break
            except OSError:time.sleep(.2)
        else:raise RuntimeError("HTTP server did not start")
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            try:
                for label,viewport in VIEWS.items():
                    context=browser.new_context(viewport=viewport,has_touch=True)
                    page=context.new_page()
                    page.set_default_timeout(25000)
                    try:
                        links=check_catalog(page,label)
                        for unit in DATA["units"]:
                            check_chapter(page,unit["id"],unit["chapter_href"],label)
                        count=check_deep_links(page,links,label)
                        preview=check_preview_practice(page)
                        cross=check_cross_chapter(page)
                        ret=check_native_practice_return(page)
                        unsafe=check_unsafe_return(page)
                        denial=check_preview_storage_negative(browser,viewport)
                        report["viewports"][label]={
                            "chapters":14,"subtopics":count,"preview_attempt_refresh":preview,
                            "C07_C08_transition":cross,"native_exam_return":ret,
                            "unsafe_return_rejected":unsafe,"storage_fail_closed":denial}
                        print("CHEM_NAV_VIEW_PASS",label,report["viewports"][label],flush=True)
                    finally:context.close()
            finally:browser.close()
        report["disposition"]="NAVIGATION_CHROMIUM_PASS__NO_EXAM_AUTHENTICITY_CLAIM"
        print(json.dumps(report,indent=2),flush=True)
    finally:
        (OUT/"navigation-receipt.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        server.terminate();server.wait(timeout=15)

if __name__=="__main__":main()

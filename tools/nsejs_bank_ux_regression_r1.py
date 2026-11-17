#!/usr/bin/env python3
"""NSEJS bank UX R1: real HTTP Chromium acceptance for three learner banks.
This verifies navigation and fails closed; it is NOT independent academic acceptance.
"""
from __future__ import annotations
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
BANKS = {
    "physics": {"topic": "optics", "total": 109, "topics": 6,
                "hidden_term": "representation",
                "break_asset": "physics-core2-integrity.v1.json"},
    "chemistry": {"topic": "atomic_structure", "total": 119, "topics": 6,
                  "hidden_term": "representation",
                  "break_asset": "chemistry-core2-candidates.v1.json"},
    "biology": {"topic": "living_world", "total": 119, "topics": 5,
                "hidden_term": "formulation",
                "break_asset": "biology-core2-candidates.v1.json"},
}
LESSONS = {
    "physics": "/nsejs/physics/learn/chapter.html?ph=PH03",
    "chemistry": "/nsejs/chemistry/textbook/index.html?unit=C08&mode=study",
    "biology": "/nsejs/biology/core1/bio-genetics-coordination-r1/index.html",
}


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        return


def inject_nav(page):
    page.evaluate("""() => new Promise((resolve,reject) => {
      if(document.querySelector('script[data-grade9-nav]')) {resolve();return;}
      const s=document.createElement('script');
      s.src='/site-nav.js';
      s.dataset.grade9Nav='r1';
      s.onload=resolve;s.onerror=()=>reject(Error('Shared nav script not loaded'));
      document.head.appendChild(s);
    })""")


def smoke_bank(page, origin, subject, info):
    url=origin+"/nsejs/"+subject+"/index.html?topic="+info["topic"]+"#topicWorkspace"
    page.goto(url,wait_until="domcontentloaded",timeout=25000)
    # The static progress message is *not* evidence of qualified data.
    expect(page.locator("#qbLoadNotice")).to_be_hidden(timeout=30000)
    expect(page.locator("#questions article.card").first).to_be_visible(timeout=30000)
    assert page.locator("#questions article.card").count() > 0
    options=page.locator("#qbTopicSelect option").first.inner_text()
    assert str(info["total"]) in options, (subject,options)
    assert str(info["topics"]) in options, (subject,options)
    assert page.locator("#topicNav button.topic-pill-btn").count() == info["topics"]+1
    assert page.locator("#qbResultCount").inner_text().strip() != "Checking verified candidate records…"

    # An answer-only word from the original *protected* derivation must not
    # return an otherwise unmatched question before a first attempt.
    page.locator("#qbSearch").fill(info["hidden_term"])
    expect(page.locator("#qbResultCount")).to_contain_text("Showing 0 ",timeout=12000)
    expect(page.locator("#questions article.card")).to_have_count(0,timeout=12000)
    assert page.locator(".official-key-line:visible").count()==0
    # The original back control must clear text+topic+filters, not merely
    # set topic=all while the active search still hides the overview.
    page.locator("#topicWorkspace button").filter(
        has_text="Return to all topics").first.click()
    expect(page.locator("#topicsGrid")).to_be_visible(timeout=8000)
    expect(page.locator("#qbResultCount")).to_contain_text(
        str(info["total"])+" candidate questions",timeout=8000)
    assert "q=" not in page.url and "topic=" not in page.url, page.url
    assert page.locator("#topicsGrid").evaluate(
        "(e)=>document.activeElement===e"), "return button must restore keyboard focus"
    return {"subject":subject,"total":info["total"],"topics":info["topics"],
            "answer_only_search":"ZERO","return":"VISIBLE"}


def failure_is_visible(page, origin, subject, info):
    pattern="**/"+info["break_asset"]
    page.route(pattern, lambda route: route.abort())
    url=origin+"/nsejs/"+subject+"/index.html?topic="+info["topic"]+"#topicWorkspace"
    page.goto(url,wait_until="domcontentloaded")
    expect(page.locator("#qbLoadNotice")).to_contain_text(
        "Question Bank unavailable",timeout=20000)
    expect(page.locator("#qbLoadNotice")).to_have_attribute("role","alert")
    retry=page.locator("#qbLoadNotice button.qb-retry")
    expect(retry).to_be_visible()
    assert page.locator("#questions article.card").count()==0
    # Retry must reload the original integrity path; it must never mark the
    # failed fetch successful or switch to unqualified data.
    page.unroute(pattern)
    retry.click()
    expect(page.locator("#qbLoadNotice")).to_be_hidden(timeout=30000)
    expect(page.locator("#questions article.card").first).to_be_visible(timeout=30000)


def resume_only_safe_lesson_urls(page, origin):
    # The source checkout does not itself contain the Pages-injected shared
    # header script. Inject the same site-nav.js explicitly over HTTP.
    for subject, lesson in LESSONS.items():
        page.goto(origin+lesson,wait_until="domcontentloaded")
        inject_nav(page)
        key="g9v41:last-lesson:"+subject
        page.wait_for_function("(key)=>!!localStorage.getItem(key)",arg=key)
        path=page.evaluate("(key)=>localStorage.getItem(key)",key)
        assert path.startswith("/nsejs/"+subject+"/"),path
        assert "answer=" not in path and "attempt=" not in path
        page.goto(origin+"/nsejs/"+subject+"/index.html",wait_until="domcontentloaded")
        inject_nav(page)
        link=page.locator('main a[data-g9-resume="'+subject+'"]')
        expect(link).to_be_visible(timeout=8000)
        assert link.get_attribute("href").endswith(path)
        assert "Continue last" in link.inner_text()
    # A malicious or cross-subject storage value must never become a link.
    page.goto(origin+"/nsejs/physics/index.html",wait_until="domcontentloaded")
    page.evaluate("""() => {
        localStorage.setItem('g9v41:last-lesson:physics','javascript:alert(1)');
        localStorage.setItem('g9-protected-attempt:fixture','unchanged-immutable');
    }""")
    inject_nav(page)
    assert page.locator('[data-g9-resume="physics"]').count()==0
    assert page.evaluate("localStorage.getItem('g9-protected-attempt:fixture')") == "unchanged-immutable"


def main():
    server=http.server.ThreadingHTTPServer(
        ("127.0.0.1",0),functools.partial(QuietHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    reports=[]
    try:
        origin="http://127.0.0.1:"+str(server.server_port)
        with sync_playwright() as playwright:
            browser=playwright.chromium.launch(headless=True,args=[
                "--no-sandbox","--disable-dev-shm-usage"])
            try:
                for width,height in ((1000,1600),(1600,1000)):
                    context=browser.new_context(viewport={"width":width,"height":height})
                    try:
                        for subject,info in BANKS.items():
                            page=context.new_page()
                            try:
                                reports.append({"viewport":f"{width}x{height}",
                                                **smoke_bank(page,origin,subject,info)})
                                failure_is_visible(page,origin,subject,info)
                            finally:page.close()
                    finally:context.close()
                context=browser.new_context(viewport={"width":1024,"height":768})
                try:
                    page=context.new_page()
                    resume_only_safe_lesson_urls(page,origin)
                    page.close()
                finally:context.close()
            finally:browser.close()
    finally:server.shutdown()
    assert len(reports)==6
    print("NSEJS_BANK_UX_R1_CHROMIUM_PASS",json.dumps(reports))


if __name__=="__main__":
    main()

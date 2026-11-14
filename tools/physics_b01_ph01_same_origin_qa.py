#!/usr/bin/env python3
"""Same-origin PH01 R4.7 + B01 R15 candidate compatibility in ephemeral merged tree.

No secure custody, academic admission, R01/B1-B7 or independent P00 approval.
"""
import json,socket,subprocess,sys,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"review-artifacts/physics-b01-ph01"
PH01="/nsejs/physics/core1/ph01-m05-r47/index.html"
B01="/nsejs/physics/curriculum/topics/PH07/b01/PH07-01/core1b.html"
CID="PH01-M05-QRT-REPRESENT-D3-R47-Q35-INSTANCE"
def port():
    with socket.socket() as s:
        s.bind(("127.0.0.1",0))
        return s.getsockname()[1]
def records(pg,prefix):
    return pg.evaluate("""p=>Object.fromEntries(Object.entries(localStorage)
      .filter(([k,v])=>k.startsWith(p)&&v.startsWith('{'))
      .map(([k,v])=>[k,JSON.parse(v)]))""",prefix)
def phready(pg):
    pg.wait_for_function("""() => (document.querySelector('#runtimeStatus')?.textContent||'')
       .includes('Candidate task loaded')""",timeout=25000)
def bready(pg):
    pg.wait_for_function("""() => {
      const s=document.querySelector('#status')?.textContent||'';
      return s.includes('Exact-version author candidate loaded')||
             s.includes('Previous first answer restored')||s.includes('Fail closed');
    }""",timeout=30000)
    s=pg.locator("#status").inner_text()
    assert "Fail closed" not in s,s
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    assert (ROOT/"nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_7.json").is_file()
    assert (ROOT/"nsejs/physics/curriculum/topics/PH07/b01/learner-preview/index.html").is_file()
    num=port();origin=f"http://127.0.0.1:{num}"
    server=subprocess.Popen([sys.executable,"-m","http.server",str(num),"--bind","127.0.0.1",
        "--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    receipt=[]
    try:
        for _ in range(80):
            if server.poll() is not None:raise RuntimeError("HTTP server exited")
            try:
                urllib.request.urlopen(origin+PH01,timeout=1).close();break
            except Exception:time.sleep(.1)
        else:raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            for label,(w,h) in (("portrait",(1000,1600)),("landscape",(1600,1000))):
                ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                pg=ctx.new_page();errors=[]
                pg.on("pageerror",lambda exc:errors.append(str(exc)))
                try:
                    pg.goto(origin+PH01+"?cycle="+CID);phready(pg)
                    assert pg.locator("#postAttempt").is_hidden()
                    pg.locator("#predictInput").fill("Signed area and reversal assumptions")
                    pg.locator("#attemptInput").fill("Independent area calculation with signs")
                    pg.locator("#saveFirst").click()
                    pr=records(pg,"G9V41:PH01:")
                    assert len(pr)==1 and next(iter(pr.values()))["first_answer"]
                    pg.goto(origin+B01);bready(pg)
                    assert "/learner-preview/index.html" in pg.url
                    assert pg.locator("#task-select option").count()==89
                    assert "PH07-01" in pg.locator("#task-meta").inner_text()
                    assert pg.locator("#after-first").is_hidden()
                    pg.locator("#predict-input").fill("Calibration can be biased")
                    pg.locator("#attempt-input").fill("Two anchors plus independent check")
                    pg.locator("#save-first").click()
                    br={k:v for k,v in records(pg,"g9-b01-r1:").items() if v.get("first_answer")}
                    assert len(br)==1 and next(iter(br.values()))["first_answer"]
                    assert records(pg,"G9V41:PH01:")==pr
                    pg.goto(origin+PH01+"?cycle="+CID);phready(pg)
                    assert pg.locator("#saveFirst").is_disabled()
                    assert records(pg,"G9V41:PH01:")==pr
                    pg.goto(origin+B01);bready(pg)
                    assert pg.locator("#after-first").is_visible()
                    assert pg.locator("#save-first").is_disabled()
                    assert {k:v for k,v in records(pg,"g9-b01-r1:").items() if v.get("first_answer")}==br
                    assert records(pg,"G9V41:PH01:")==pr
                    assert pg.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
                    assert not errors,errors
                    receipt.append({"orientation":label,"viewport":[w,h],
                        "PH01_first":"PRESERVED","B01_first":"PRESERVED",
                        "same_origin_storage_namespace":"ISOLATED","academic":"HOLD"})
                finally:ctx.close()
            browser.close()
        result={"status":"TECHNICAL_CANDIDATE_PASS","source_admission":"HOLD",
                "independent_P00":"NOT_PERFORMED","academic":"HOLD",
                "ephemeral_merge_not_committed_or_pushed":True,"cases":receipt}
        (OUT/"ph01-b01-same-origin.json").write_text(json.dumps(result,indent=2)+"\n")
        print("PH01+B01 SAME-ORIGIN CHROMIUM PASS: first attempts and content revisions independent in both tablet orientations. ACADEMIC HOLD.")
    finally:
        server.terminate();server.wait(timeout=5)
if __name__=="__main__":main()

#!/usr/bin/env python3
"""R00 PH01 R4.7 HTTP Chromium: exact Q35/Q33/Q60 source, graphs, six-stage custody."""
from __future__ import annotations
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright
from physics_ph01_r31_core1b_browser_qa import free_port
from physics_ph01_r45_browser_qa import blocked, journey, ready, record, storage_key

ROOT = Path(__file__).resolve().parents[1]
PH = ROOT / "nsejs/physics/curriculum/agent1/PH01"
OUT = ROOT / "review-artifacts/physics-r47"
TASKS = (
    ("PH01-LINK-2022-51-Q35","PH01-M05","PH01-M05-QRT-REPRESENT-D3-R47-Q35-INSTANCE",1),
    ("PH01-LINK-2024-51-Q33","PH01-M04","PH01-M04-QRT-MODEL-D3-R47-Q33-INSTANCE",0),
    ("PH01-LINK-2024-51-Q60","PH01-M05","PH01-M05-QRT-JUSTIFY-D3-R47-Q60-INSTANCE",3),
)
MAIN = ("PH01-MAIN-D3.4-R47","PH01-MAIN-D3.5-R47","PH01-MAIN-D3.7-R47")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    server = subprocess.Popen([sys.executable,"-m","http.server",str(port),
        "--bind","127.0.0.1","--directory",str(ROOT)],
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    receipt={"task":"PH01_R47_EXACT_HEAD_HTTP_CHROMIUM_R00","candidate":True,
        "academic_status":"HOLD","cases":[]}
    try:
        for _ in range(70):
            if server.poll() is not None: raise RuntimeError("Server exited")
            try:
                urllib.request.urlopen(base+"/nsejs/physics/textbook/PH01/core2-links-r47/index.html",timeout=1).close()
                break
            except Exception: time.sleep(.1)
        else: raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            for orientation,(w,h) in (("portrait",(1000,1600)),("landscape",(1600,1000))):
                for source,sub,cid,graph_count in TASKS:
                    context=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                    pg=context.new_page()
                    url=base+f"/nsejs/physics/core1/{sub.lower()}-r47/index.html"
                    try:
                        pg.goto(base+"/nsejs/physics/textbook/PH01/core2-links-r47/index.html#"+source)
                        card=pg.locator('[id="'+source+'"]')
                        assert card.count()==1
                        card.locator("summary").click()
                        candidate=card.locator('a[href*="'+cid+'"]')
                        assert candidate.count()==1,(source,cid)
                        candidate.click()
                        ready(pg)
                        assert pg.locator("#cycleSelect").input_value()==cid
                        assert pg.locator("#promptGraphs svg").count()==graph_count
                        if graph_count:
                            assert pg.locator("#promptGraphs polyline").count()>=graph_count
                            assert pg.locator("#promptGraphs figcaption").count()==graph_count
                        pg.locator("#core2-return a").click()
                        pg.wait_for_url("**/core2-links-r47/index.html#"+source)
                        # Fresh context: source return has been exposed before first answer.
                        pg.goto(base+"/nsejs/physics/textbook/PH01/index.html")
                        probe=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                        trial=probe.new_page()
                        saved=journey(trial,url,cid,7,w,False)
                        assert saved["mastery_status"]=="UNASSESSED"
                        assert saved["content_revision"]==storage_key(7,cid).split(":")[3]
                        probe.close()
                        blocked(browser,url,cid,w,h,7)
                        receipt["cases"].append({"orientation":orientation,"cycle":cid,
                            "graphs":graph_count,"source":source,"full_journey":"PASS",
                            "source_return":"PASS","storage_disabled":"PASS"})
                    finally: context.close()
                main_url=base+"/nsejs/physics/core1/ph01-main-r47/index.html"
                for cid in MAIN:
                    context=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                    pg=context.new_page()
                    try:
                        saved=journey(pg,main_url,cid,7,w,False)
                        assert saved["mastery_status"]=="UNASSESSED"
                        receipt["cases"].append({"orientation":orientation,
                            "cycle":cid,"full_journey":"PASS","kind":"MAIN"})
                    finally:context.close()
            browser.close()
        receipt["status"]="PASS"
        (OUT/"ph01-r47-chromium-r00.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print("PH01 R4.7 PASS: three source-proximal INSTANCE journeys, original graphs, three revised MAIN journeys, source return and blocked storage, portrait/landscape; academic HOLD")
    finally:
        server.terminate()
        server.wait(timeout=5)

if __name__=="__main__":
    main()

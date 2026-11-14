#!/usr/bin/env python3
"""R4.6 four 2025 locator transfers and two revised MAIN journeys on exact tablet scopes."""
import json,subprocess,sys,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from physics_ph01_r31_core1b_browser_qa import free_port
from physics_ph01_r45_browser_qa import journey,blocked,ready,record,storage_key
ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics/curriculum/agent1/PH01/"
def main():
    routes=json.loads((PH/"ph01-subtopic-routes.r4_6.json").read_text())
    loc=json.loads((PH/"ph01-2025-locator-transfers.r4_6.json").read_text())
    port=free_port();origin=f"http://127.0.0.1:{port}"
    server=subprocess.Popen([sys.executable,"-m","http.server",str(port),"--bind","127.0.0.1","--directory",str(ROOT)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:urllib.request.urlopen(origin+"/nsejs/physics/textbook/PH01/core2-links-r46/index.html",timeout=1).close();break
            except Exception:time.sleep(.1)
        else:raise RuntimeError("HTTP server unavailable")
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for w,h in ((1000,1600),(1600,1000)):
                ctx=browser.new_context(viewport={"width":w,"height":h},has_touch=True);pg=ctx.new_page()
                for u in routes["units"]:
                    m=u["subtopic_id"][-3:]
                    pg.goto(origin+"/"+u["core1a"])
                    pg.locator("details.g9-review-versions summary").click()
                    pg.locator("details.g9-review-versions").get_by_role("link",name=f"Open {m} R4.6 · D3/D4 practice").click();ready(pg)
                    assert set(pg.locator("#cycleSelect option").evaluate_all("(xs)=>xs.map(x=>x.value)"))==set(u["instance_ids"])
                for z in loc["records"]:
                    n=z["question_number"];cid=z["cycle_id"];url=origin+"/"+z["core1b"]
                    pg.goto(origin+"/nsejs/physics/textbook/PH01/core2-links-r46/index.html#locator-2025-51-Q"+str(n))
                    card=pg.locator("#locator-2025-51-Q"+str(n))
                    card.get_by_role("link",name="Protected Core1B exact transfer").click();ready(pg)
                    assert pg.locator("#cycleSelect").input_value()==cid
                    assert "not a Core2 record" in pg.locator("#core2-return a").inner_text()
                    pg.locator("#core2-return a").click()
                    pg.wait_for_url("**/core2-links-r46/index.html#locator-2025-51-Q"+str(n))
                    # separate context for unassisted attempt; prior locator visit is explicit help exposure
                    trial=browser.new_context(viewport={"width":w,"height":h},has_touch=True)
                    tpg=trial.new_page();journey(tpg,url,cid,6,w);trial.close()
                mainurl=origin+"/"+routes["integrated_main"]["path"]
                for cell in ("D3.3","D4.4"):
                    cid="PH01-MAIN-"+cell+"-R46"
                    journey(pg,mainurl,cid,6,w,True)
                    blocked(browser,mainurl,cid,w,h,6)
                pg.goto(origin+"/nsejs/physics/index.html?topic=mechanics#question-NSEJS-24-MECH-03")
                pg.locator("#question-NSEJS-24-MECH-03 [data-ph01-r46-link]").click()
                pg.wait_for_url("**/core2-links-r46/index.html#PH01-LINK-2024-51-Q37")
                ctx.close()
            browser.close()
        print("PH01 R4.6 PASS: eight scopes, four 2025 locator-only return routes, four full INSTANCE and two full MAIN journeys x2, blocked storage, existing Core2 reverse link; academic HOLD")
    finally:server.terminate();server.wait(timeout=5)
if __name__=="__main__":main()

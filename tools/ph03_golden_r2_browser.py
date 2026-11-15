"""Exact-head author QA: real selections, structured physics, changed models, negative controls."""
import functools,http.server,threading,json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
REL="nsejs/physics/ph03/source-led-r2"
ART=ROOT/"artifacts/ph03-golden-r2"
ART.mkdir(parents=True,exist_ok=True)
D=json.loads((ROOT/REL/"content.v2.json").read_text())
M=json.loads((ROOT/REL/"models.v2.json").read_text())
def first(page,pred,reason):
    page.locator("#prediction").fill(pred);page.locator("#reason").fill(reason)
def fields(page,prefix,values):
    for k,v in values.items():
        target=page.locator("#"+prefix+k)
        if target.evaluate("(x)=>x.tagName")== "SELECT":target.select_option(str(v))
        else:target.fill(str(v))
def load(page,url):
    page.goto(url)
    expect(page.locator("#commit")).to_be_enabled()
def image_check(page):
    for img in page.locator("img").all():
        expect(img).to_be_visible()
        assert img.evaluate("(i)=>i.complete&&i.naturalWidth>0")
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
def complete(page,url,tid,w):
    load(page,url+"?stage=challenge&task="+tid)
    image_check(page)
    assert page.locator("#hint").count()==0 and page.locator("#reveal").count()==0
    first(page,"The sign and timing matter","I will infer a signed intermediate and compare energy at the correct times." if tid=="A" else "I compare the reported momentum and energy changes.")
    # Incomplete response must not advance.
    page.locator("#commit").click()
    expect(page.locator("#status")).to_contain_text("Complete")
    assert page.locator("#reveal").count()==0
    wrong={"v":2,"u":12.5,"loss":183.75} if tid=="A" else {"j":-4,"isolation":"no","drop":24,"conversion":"yes"}
    fields(page,"first-",wrong)
    page.locator("#commit").click()
    expect(page.locator("#reveal")).to_be_visible()
    page.locator("#hint").click();expect(page.locator("#helpers")).to_contain_text("CLARIFY")
    assert "CORRELATE" not in page.locator("#helpers").inner_text()
    page.reload();expect(page.locator("#helpers")).to_contain_text("CLARIFY")
    page.locator("#hint").click();expect(page.locator("#helpers")).to_contain_text("CORRELATE")
    page.locator("#hint").click();expect(page.locator("#helpers")).to_contain_text("OPEN_THE_WAY")
    page.screenshot(path=str(ART/f"challenge-{tid}-{w}.png"),full_page=True)
    page.locator("#reveal").click()
    expect(page.locator("#post")).to_contain_text("Signed intermediate state" if tid=="A" else "Energy attribution")
    assert "52.5 J" not in page.locator("#post").inner_text() if tid=="A" else "18 J" not in page.locator("#post").inner_text()
    page.locator("#diagtext").fill("I chose the positive root despite leftward displacement." if tid=="A" else "I treated kinetic energy decrease as internal conversion without external work.")
    page.locator("#diagnose").click()
    expect(page.locator("#post")).to_contain_text("Draw the rough-strip displacement" if tid=="A" else "work measurement is missing")
    fields(page,"repair-",M[tid]["expected"])
    page.locator("#repairreason").fill("V=-2, signed momentum gives u=2.5 and 43.75-10=33.75 J." if tid=="A" else "P changes by -4 N s; K drops 24 J but external work is unknown.")
    page.locator("#repairSave").click()
    expect(page.locator("#post")).to_contain_text("Structured values match")
    page.locator("#boundarySave").click()
    expect(page.locator("#status")).to_contain_text("Explain")
    assert page.locator("#boundaryReveal").count()==0
    fields(page,"bound-",M[tid]["boundaryExpected"])
    page.locator("#boundaryreason").fill("External impulse changes momentum; external work is unspecified." if tid=="A" else "Contact is isolated; later impulse changes P and K separately.")
    page.locator("#boundarySave").click()
    expect(page.locator("#boundaryReveal")).to_be_visible()
    assert "52.5 J" not in page.locator("#post").inner_text() if tid=="A" else "18 J" not in page.locator("#post").inner_text()
    page.locator("#boundaryReveal").click()
    expect(page.locator("#post")).to_contain_text("52.5 J" if tid=="A" else "18 J")
    image_check(page)
    page.screenshot(path=str(ART/f"boundary-{tid}-{w}.png"),full_page=True)
    page.reload();expect(page.locator("#post")).to_contain_text("52.5 J" if tid=="A" else "18 J")
    expect(page.locator("#first-"+("v" if tid=="A" else "j"))).to_have_value(str(wrong["v" if tid=="A" else "j"]))
def run():
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    url=f"http://127.0.0.1:{server.server_port}/{REL}/index.html"
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch()
            for w,h in [(1000,1600),(1600,1000)]:
                ctx=browser.new_context(viewport={"width":w,"height":h})
                page=ctx.new_page()
                load(page,url+"?stage=source")
                first(page,"The post-contact swing uses a different relation","I predict the original answer by comparing impact and rise.")
                page.locator("#commit").click();expect(page.locator("#status")).to_contain_text("required selection")
                page.locator('input[name="opt"][value="B"]').check();page.locator("#commit").click()
                expect(page.locator("#post")).to_contain_text("Original selection and reasoning saved")
                assert page.locator("#retrySave").count()==0
                assert "9.81 m/s" not in page.locator("#post").inner_text()
                page.get_by_role("link",name="Open Core1A guide").click()
                expect(page.locator("#guide")).to_be_visible()
                image_check(page)
                for value,phrase in [("-8","Cancellation"),("-11","Reversal"),("4","Velocity matching")]:
                    page.locator("#speed").fill(value);expect(page.locator("#modelnote")).to_contain_text(phrase)
                page.screenshot(path=str(ART/f"guide-{w}.png"),full_page=True)
                complete(page,url,"A",w)
                page.goto(url+"?stage=source")
                expect(page.locator("#post")).to_contain_text("locked until both")
                complete(page,url,"B",w)
                page.goto(url+"?stage=source")
                expect(page.locator("#retrySave")).to_be_visible()
                page.locator('input[name="retryopt"][value="C"]').check()
                page.locator("#retryreason").fill("Separate momentum during impact and energy during the swing.")
                page.locator("#retrySave").click()
                expect(page.locator("#post")).to_contain_text("First selected B; return selected C")
                assert page.evaluate("Object.values(localStorage).some(x=>x.includes('transferReceipts'))")
                page.reload();expect(page.locator("#post")).to_contain_text("First selected B; return selected C")
                page.goto(url+"?stage=bank");expect(page.get_by_text("Core2 · PH03 Golden Sample bank")).to_be_visible()
                page.get_by_role("link",name="Attempt authored assessment").click()
                expect(page.locator("#commit")).to_be_enabled()
                first(page,"Stopping distance depends on joined speed","V=4, contact loss 48 J; remaining 24 J divided by 6 N.")
                page.locator('input[name="opt"][value="C"]').check();page.locator("#commit").click()
                page.locator("#reveal").click();expect(page.locator("#post")).to_contain_text("48 J")
                ctx.close()
            exposed=browser.new_context();page=exposed.new_page()
            page.goto(url+"?stage=learn");expect(page.locator("#guide")).to_be_visible()
            load(page,url+"?stage=source");expect(page.locator("#status")).to_contain_text("Prior R2 learning exposure")
            exposed.close()
            denied=browser.new_context();page=denied.new_page()
            page.add_init_script("Storage.prototype.setItem=function(){throw Error('DENIED')}")
            page.goto(url+"?stage=challenge&task=A");expect(page.locator("#status")).to_contain_text("HOLD")
            expect(page.locator("#commit")).to_be_disabled()
            assert page.locator("#reveal").count()==0;denied.close()
            missing=browser.new_context();page=missing.new_page()
            page.route("**/challenge-a.svg",lambda route:route.abort())
            page.goto(url+"?stage=challenge&task=A");expect(page.locator("#status")).to_contain_text("HOLD")
            expect(page.locator("#commit")).to_be_disabled();missing.close()
            stale=browser.new_context();page=stale.new_page()
            load(page,url+"?stage=challenge&task=A")
            first(page,"Left","Momentum and energy");fields(page,"first-",M["A"]["expected"])
            page.locator("#commit").click();expect(page.locator("#reveal")).to_be_visible()
            def mutate(route):
                r=route.fetch();route.fulfill(response=r,body=r.body()+b"<!-- mutation -->")
            page.route("**/challenge-a.svg",mutate);page.reload()
            expect(page.locator("#commit")).to_be_enabled()
            assert page.locator("#reveal").count()==0
            stale.close();browser.close()
        (ART/"receipt.json").write_text(json.dumps({"engineering":"PASS","academic":"HOLD","negative":["incomplete structured fields","source option required","boundary gated","prior learning exposure","storage denied","missing figure","stale SVG"],"viewports":[[1000,1600],[1600,1000]],"limitations":"Automated author QA, not observed learner mastery or visual review."},indent=2))
    finally: server.shutdown()
if __name__=="__main__":run()

"""Real Chromium technical fixtures. No learner, source or academic certification."""
import http.server, threading, json
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(HERE),**kw)
    def log_message(self,*a):pass
def click(p,name):
    p.get_by_role("button",name=name,exact=True).click()

def field(p,n,v):
    loc=p.locator(f'[name="{n}"]')
    try:
        loc.wait_for(state="visible",timeout=6000)
    except Exception as exc:
        status=p.locator("#status").inner_text(timeout=2000)
        contents=p.locator("main").inner_text(timeout=2000)[:1500]
        raise AssertionError(
            f"FIELD_NOT_RENDERED:{n}; status={status!r}; main={contents!r}; url={p.url}"
        ) from exc
    if loc.evaluate("el=>el.tagName")== "SELECT":loc.select_option(v)
    else:loc.fill(str(v))
def answer(p,model,value,kind):
    field(p,"model",model);field(p,"value",value);field(p,"reason","Fixture explanation, not independently graded.");click(p,kind)
def begin(p,model,value):
    click(p,"Open source prompt");answer(p,model,value,"Commit source attempt");click(p,"Open teaching");click(p,"Open fresh challenge");field(p,"prediction","Fixture prediction");click(p,"Commit prediction")
    # Await durable prediction before fault injection or racing browser tabs.
    # Otherwise Storage.setItem can be patched during the prediction commit,
    # creating a false negative for the first-attempt write-failure scenario.
    p.get_by_role("button",name="Commit first attempt",exact=True).wait_for()
def boundary(p,direction,magnitude,button):
    field(p,"direction",direction);field(p,"magnitude",magnitude);field(p,"reason","Fixture boundary explanation");click(p,button)
def main():
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f"http://127.0.0.1:{server.server_port}/fixtures/"
    rows=[]
    try:
      with sync_playwright() as pw:
        browser=pw.chromium.launch()
        for subject,src,wrong,correct,bd,mag in [("physics",3,"sum","difference","left",5),("chemistry",4,"lost","retained","same",2)]:
          for w,h in [(1000,1600),(1600,1000)]:
            ctx=browser.new_context(viewport={"width":w,"height":h});p=ctx.new_page();req=[];p.on("request",lambda r:req.append(r.url))
            p.goto(base+subject+"/index.html");p.get_by_role("button",name="Open source prompt").wait_for()
            begin(p,correct,src);assert not any("/feedback.json" in x or "/boundary" in x for x in req)
            val=5 if subject=="physics" else 7
            answer(p,wrong,val,"Commit first attempt")
            p.get_by_role("button",name="Open worked reconstruction").wait_for()
            assert not any("/feedback.json" in x for x in req)
            click(p,"Open worked reconstruction");p.get_by_text("First differing checked field: model").wait_for()
            assert any("/feedback.json" in x for x in req)
            p.reload();p.get_by_text("First differing checked field: model").wait_for()
            field(p,"comparison","Compare saved incorrect model against reconstruction.");click(p,"Commit comparison")
            p.get_by_label("First differing checked field").select_option("model");field(p,"diagnosis","The selected model does not match the actual reasoning.");click(p,"Commit diagnosis")
            answer(p,correct,val-1,"Commit repair");p.get_by_text("First differing checked field: value").wait_for()
            answer(p,correct,val,"Commit repair");click(p,"Open changed-condition prompt")
            p.get_by_role("img",name="Synthetic directional marker, not a solution.").wait_for()
            assert any("boundary-diagram.png" in x for x in req)
            assert not any("/boundary_feedback.json" in x for x in req)
            boundary(p,"right" if subject=="physics" else "changed",mag,"Commit boundary response")
            click(p,"Open boundary feedback")
            p.get_by_role("heading",name="Boundary correction").wait_for()
            boundary(p,bd,mag,"Commit boundary repair");answer(p,correct,src,"Commit source return");click(p,"Open source feedback")
            p.get_by_role("heading",name="Sequence complete — not mastery").wait_for()
            assert p.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
            assert "Academic HOLD" in p.locator("main").inner_text()
            rows.append({"subject":subject,"viewport":[w,h],"result":"PASS_TECHNICAL_ONLY","network_roles":sorted({x.split("/")[-1] for x in req if x.endswith(".json") or x.endswith(".png")})})
            ctx.close()
        # Real two-tab race: synchronize both before clicking, dispatch competing clicks.
        ctx=browser.new_context();a=ctx.new_page();b=ctx.new_page();url=base+"physics/index.html"
        a.goto(url);begin(a,"difference",3);b.goto(url);b.get_by_role("button",name="Commit first attempt").wait_for()
        for p,model,val in [(a,"difference",5),(b,"sum",99)]:
            field(p,"model",model);field(p,"value",val);field(p,"reason","Concurrent fixture response.")
        # Click handlers in same event-loop phase via JS; Web Locks serialize both tabs.
        a.evaluate("()=>{const button=[...document.querySelectorAll('main button')].find(x=>x.textContent==='Commit first attempt');setTimeout(()=>button.click(),250)}")
        b.evaluate("()=>{const button=[...document.querySelectorAll('main button')].find(x=>x.textContent==='Commit first attempt');setTimeout(()=>button.click(),250)}")
        a.get_by_role("button",name="Open worked reconstruction").wait_for();b.get_by_role("button",name="Open worked reconstruction").wait_for()
        record=a.evaluate("()=>JSON.parse(localStorage.getItem(Object.keys(localStorage).find(k=>k.startsWith('g9:assessment:'))))")
        first=[x for x in record["events"] if x["kind"]=="first"];assert len(first)==1 and first[0]["data"]["value"] in (5,99)
        ctx.close()
        # Deny actual first-write, not just initial storage getter.
        ctx=browser.new_context();p=ctx.new_page();requests=[];p.on("request",lambda r:requests.append(r.url));p.goto(url);begin(p,"difference",3)
        p.evaluate("()=>{Storage.prototype.setItem=function(){throw Error('fixture denied write')}}")
        answer(p,"difference",5,"Commit first attempt");p.get_by_text("fixture denied write",exact=False).wait_for()
        assert not any("feedback.json" in x for x in requests);ctx.close()
        # Pin mismatch on postattempt role.
        ctx=browser.new_context();p=ctx.new_page();p.route("**/feedback.json",lambda route:route.fulfill(status=200,body="{}"));p.goto(url);begin(p,"difference",3);answer(p,"difference",5,"Commit first attempt");click(p,"Open worked reconstruction");p.get_by_text("ASSET_HASH:feedback",exact=False).wait_for();ctx.close()
        browser.close()
      print(json.dumps({"academic_status":"HOLD","journeys":rows,"two_tab":"PASS","write_failure":"PASS","tamper":"PASS"},indent=2))
    finally:server.shutdown()
if __name__=="__main__":main()

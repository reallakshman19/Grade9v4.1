"""PH03 R2 semantic and negative controls; not independent qualification."""
import json, math, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"nsejs/physics/ph03/source-led-r2"
D=json.loads((P/"content.v2.json").read_text())
M=json.loads((P/"models.v2.json").read_text())

def solve_a(j=0):
    v=-math.sqrt(2*.25*10*.8)
    u=(5*v+15-j)/2
    return v,u,u*u+1.5*25-2.5*v*v

def model(u):
    P=8+u
    K=16+.5*u*u
    V=P/3
    after=1.5*V*V
    return P,V,K,after,K-after

def test_r2_science_and_negative_controls():
    assert solve_a()==(-2,2.5,33.75)
    assert solve_a(-5)==(-2,5,52.5)
    assert .5*(6/5)*(2.5+5)**2==33.75
    assert (2*5+2*(-1),.5*2*25+.5*2)==(8,26)
    assert 4*1-8==-4 and 26-.5*4*1==24
    assert 26-.5*4*2**2==18 and .5*4*2**2-.5*4*1==6
    assert model(-8)==(0,0,48,0,48)
    assert model(-11)[0:2]==(-3,-1)
    assert model(4)[4]==0
    assert math.isclose(5*math.sqrt(2*9.81*.196),9.805,abs_tol=.002)
    assert (12/3)**2/(2*.2*10)==4
    assert .5*1*12**2-.5*3*4**2==48
    # Wrong sign and dimension are falsifiable, not simply key agreement.
    assert (5*2+15)/2!=solve_a()[1]
    def dim_mul(a,b):return tuple(x+y for x,y in zip(a,b))
    def dim_div(a,b):return tuple(x-y for x,y in zip(a,b))
    g=(0,1,-2);length=(0,1,0);v2=(0,2,-2)
    assert dim_mul(g,length)==v2
    assert dim_div(g,length)!=v2
    assert M["A"]["boundaryExpected"]=={"u":5,"law":"impulse","energy":"no"}
    assert M["B"]["boundaryExpected"]=={"v":2,"loss":18,"later":6}

def test_r2_distinct_constructs_and_real_figures():
    assert D["release"]=="HOLD" and M["status"]=="AUTHOR_ONLY_HOLD"
    assert D["source"]["paper_sha256"] is None and D["source"]["rights"]=="HOLD"
    assert D["source"]["options"]==list("ABCD") and "key_option" not in D["source"]
    assert len(list((P/"figures").glob("*.svg")))==10
    for f in (P/"figures").glob("*.svg"):
        root=ET.parse(f).getroot()
        assert root.attrib["viewBox"].startswith("0 0 ")
        assert not any(x.tag.endswith("image") for x in root.iter())
    for name in ["challenge-a.svg","challenge-b.svg","core2.svg"]:
        s=(P/"figures"/name).read_text()
        assert all(x not in s for x in ["33.75","48 J","24 J","−4 N·s","2.5 m/s"])
    assert D["tasks"]["A"]["uid"]!=D["tasks"]["B"]["uid"]
    assert D["tasks"]["A"]["prompt"]!=D["core2"]["prompt"]
    assert "external horizontal impulse of −5" in D["tasks"]["A"]["boundaryPrompt"]
    assert "only AFTER" in D["tasks"]["B"]["boundaryPrompt"]
    assert "external work" in M["B"]["steps"][-1]
    assert "boundaryFigure" in M["B"] and "solutionFigure" not in M["B"]
    html=(P/"index.html").read_text()
    for anchor in ["foundation","connected","braking","pendulum","misconception","synthesis"]:
        assert f'id="{anchor}"' in html
    assert 'min="-12" max="4"' in html
    assert 'guide-pendulum.svg' in html and 'guide-energy.svg' in html
    js=(P/"reader.js").read_text()
    assert "markExposure()" in js and "transferReceipts:receipts" in js
    assert "rec.retry||completedTransfer()" in js and "old.first&&!old.revealed" in js
    assert "old.first?old" in js and "readRecord(ref)" in js
    assert "ref.figs.boundary" in js and "rec.boundaryReveal?" in js
    assert "x.first&&x.repair&&x.boundary&&x.boundaryReveal" in js
    assert "old.first&&!old.retry&&receipts" in js

def test_r2_legacy_kept_and_scope_hold():
    assert (ROOT/"nsejs/physics/ph03/source-led-r1/reader.js").exists()
    for role in ["textbook","core1"]:
        s=(ROOT/f"nsejs/physics/{role}/PH03/P03/index.html").read_text()
        assert "source-led-r2/index.html" in s and "source-led-r1/index.html" in s
    assert sum(x["delivery"]=="GOLDEN_DRAFT" for x in D["subtopics"])==1

def test_r2_impulse_anchor_is_separating():
    u_a,u_b=6,0
    v_a,v_b=u_a-5,u_b+5/4
    assert (v_a,v_b)==(1,1.25)
    assert v_a<v_b and v_a+4*v_b==6
    assert .5*v_a*v_a+2*v_b*v_b<.5*u_a*u_a

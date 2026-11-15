from pathlib import Path
import json, math, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"nsejs/physics/ph03/source-led-r1"
C=ROOT/"nsejs/physics/curriculum/topics/PH03"
D=json.loads((P/"content.v1.json").read_text())
M=json.loads((P/"models.v1.json").read_text())
def test_ph03_gold_source_hold_and_inventory():
    c=json.loads((C/"source-census.r1.json").read_text())
    assert c["indexed_cohorts"]==9 and c["preliminary_primary_leads"]==9
    assert c["exhaustively_screened_cohorts"]==c["admitted_originals"]==0
    assert D["release"]=="HOLD" and M["status"]=="AUTHOR_ONLY_HOLD"
    assert len(D["subtopics"])==7
    assert sum(x["delivery"]=="GOLDEN_DRAFT" for x in D["subtopics"])==1
    assert c["source_records"][1]["paper_sha256"] is None
    assert D["source"]["id"]==M["source"]["uid"]
    assert "key_option" not in D["source"] and "key" not in D["source"]
def solve(sign):
    v=sign*math.sqrt(2*.25*10*.8)
    u=(5*v+15)/2
    loss=u*u+1.5*25-2.5*v*v
    return u,loss
def test_ph03_science_and_sign_mutation():
    assert solve(-1)==(2.5,33.75)
    assert solve(1)==(12.5,183.75)
    assert .5*(6/5)*(2.5+5)**2==33.75
    assert .5*(6/5)*(12.5+5)**2==183.75
    assert 4*3+2*(-6)==0
    assert .5*4*3**2+.5*2*6**2==54
    assert math.isclose(5*math.sqrt(2*9.8*.196),9.8)
def test_ph03_real_neutral_svg_and_revision_gate():
    for name in ["p03-guide.svg","p03-challenge.svg","p03-core2.svg"]:
        r=ET.parse(P/"figures"/name).getroot()
        assert r.attrib["viewBox"]=="0 0 700 340"
        assert not any(x.tag.endswith("image") for x in r.iter())
    for name in ["p03-challenge.svg","p03-core2.svg"]:
        s=(P/"figures"/name).read_text()
        assert all(x not in s for x in ["33.75","183.75","54 J","2.5 m/s","12.5 m/s"])
    js=(P/"reader.js").read_text()
    assert "await $(\"promptfig\").decode()" in js
    assert "navigator.locks.request(storageKey" in js and "localStorage.getItem(storageKey)!==raw" in js
    assert "hash([t,model,figBytes,d.source.id])" in js
    assert "model.hints.slice(0,rec.hints)" in js
    assert "old.first?old" in js
    assert "if(rec.revealed)" in js
    assert sum(x["score"] for x in M["task"]["factors"].values())==7

def test_ph03_source_return_requires_exact_boundary():
    js=(P/"reader.js").read_text()
    assert "completedTransfer()" in js
    assert "return_evidence:evidence" in js
    assert "Source reattempt remains locked" in js
    assert "x.boundary&&x.boundaryReveal" in js

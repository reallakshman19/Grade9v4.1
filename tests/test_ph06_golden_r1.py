"""PH06 author-side falsification tests. These do not grant academic acceptance."""
from fractions import Fraction as F
from pathlib import Path
import json
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics"
P=PH/"ph06"
C=PH/"curriculum/topics/PH06"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def displaced_mass(top,H,d,A,rho1,rho2):
    bottom=top+H
    h1=max(F(0),min(bottom,d)-max(top,F(0)))
    h2=max(F(0),bottom-max(top,d))
    assert h1>=0 and h2>=0 and h1+h2<=H
    return A*(rho1*h1+rho2*h2),h1,h2
def pressure(z,d,r1,r2,g):
    return g*(r1*max(F(0),min(z,d))+r2*max(F(0),z-d))
def test_exact_inverse_and_regime_boundary():
    A=F(1,100);H=F(3,10);L=F(1,4);r1=800;r2=1200
    d=(r2*L-F(26,10)/A)/(r2-r1)
    assert d==F(1,10)
    assert displaced_mass(L-H,H,d,A,r1,r2)==(F(26,10),F(1,10),F(15,100))
    assert displaced_mass(F(0),H,d,A,r1,r2)[0]==F(32,10)
    assert displaced_mass(d,H,d,A,r1,r2)[0]==F(36,10)
    loaded=F(34,10)
    t=(loaded/A-r2*H+(r2-r1)*d)/(r2-r1)
    assert t==F(1,20) and 0<t<d
    assert displaced_mass(t,H,d,A,r1,r2)==(loaded,F(1,20),F(1,4))
    # Wrong model: keeping the upper layer fully occupied after top crosses surface.
    wrong_L=(loaded/A+(r2-r1)*d)/r2
    assert wrong_L>H
    assert A*(pressure(t+H,d,r1,r2,10)-pressure(t,d,r1,r2,10))==loaded*10
    assert A*pressure(L,d,r1,r2,10)==26
    # Removing ballast changes to upper-only regime.
    L2=F(7,10)/(A*r1)
    assert L2==F(7,80) and L2<d
    assert displaced_mass(L2-H,H,d,A,r1,r2)==(F(7,10),L2,F(0))
    assert A*r1*d==F(4,5)
def test_pressure_and_other_authored_witnesses():
    assert 1000*10*F(1,500)==20
    assert 15-1000*10*F(1,1000)==5
    assert 1000*10*F(1,1000)-6==4
    assert F(12,10000)==F(3,2500)
    assert F(3)/F(3,2500)==2500
    assert 700*F(1,1000)+1100*F(1,1000)==F(18,10)
    assert 900*F(1,1000)+1300*F(2,1000)==F(35,10)
    assert 800*F(75,100000)+1200*F(125,100000)==F(21,10)
    assert (F(8,10)+F(136,10))/2==F(72,10)
def test_source_custody_and_canonical_scope():
    a=load(C/"golden-author-handoff.v1.json")
    inv=load(PH/"curriculum/agent1/ph01-ph06-syllabus-inventory.v1.json")
    reg=next(x["subtopics"] for x in inv["chapters"] if x["topic_id"]=="PH06")
    assert len(reg)==10
    for name in ("primary","support"):
        row=a["canonical"][name]
        assert any(x["subtopic_id"]==row["id"] and x["scope_role"]==row["role"] for x in reg)
    src=load(C/"golden-source-review.v1.json")
    assert src["source"]["observed_key"]=="C" and src["source"]["paper_sha256"] is None
    assert src["SL1"]["eligible_for_native_original"] is False
    assert src["SL2"]["total"]==2 and src["SL2"]["cell"] is None
    census=load(C/"historical-census.r1.json")
    assert sum(len(x["leads"]) for x in census["cohorts"])==17
    assert census["closed_cohorts"]==census["original_admitted"]==0
    assert all(x["status"]=="HOLD" for x in a["B1_B7"])
def test_actual_svgs_and_protected_projection():
    task=load(P/"task.v1.json");model=load(P/"model.v1.json");src=load(P/"source.v1.json")
    assert task["uid"]==model["uid"] and task["revision"]==model["revision"]
    assert task["source_role"]=="AUTHORED_TRANSFER" and src["qualified"] is False
    assert len(model["hints"])==3 and model["proposal"]["total"]==7
    assert sum(x["score"] for x in model["proposal"]["factors"].values())==7
    assert not {"hints","reconstruction","alternative","boundaryModel","W"}.intersection(task)
    assert not {"observed_key","final_key"}.intersection(src)
    svgs=list((P/"figures").glob("*.svg"));assert len(svgs)==7
    for s in svgs:
        tree=ET.parse(s);assert tree.getroot().tag.endswith("svg")
        assert "viewBox" in tree.getroot().attrib
        assert not any(n.tag.endswith(("image","script","foreignObject")) for n in tree.iter())
    prompt=(P/task["figure"]).read_text()
    assert "0.10 m" not in prompt and "0.05 m" not in prompt and "3.20 kg" not in prompt
    for path in ("textbook/PH06/U06/index.html","textbook/PH06/U08/index.html","core1/PH06/U08/index.html"):
        assert (PH/path).is_file()
    reader=(P/"reader.js").read_text()
    assert "navigator.locks.request" in reader and "localStorage.getItem(key)!==raw" in reader
    assert "JSON.stringify([raw,modelRaw,sourceRaw,figure,solutionFigure,boundaryFigure])" in reader and ".decode()" in reader

def test_golden_only_catalog_integration():
    cat=load(PH/"learn/catalog.json")
    ch=next(x for x in cat["chapters"] if x["id"]=="PH06")
    assert ch["state"]=="learning-pairs" and len(ch["units"])==1
    assert ch["units"][0]["id"]=="U08"
    assert all((PH/ch["units"][0][k]).is_file() for k in ("learn","practice"))
    assert "Golden candidate · 1/10" in (PH/"index.html").read_text()

def test_guided_four_regimes_and_invalid_continuation():
    A=F(1,200);H=F(2,5);d=F(1,5)
    for b,m,h1,h2 in [(F(2,15),F(2,5),F(2,15),0),(F(3,10),F(11,10),d,F(1,10)),(F(1,2),F(9,5),F(1,10),F(3,10)),(F(3,5),F(2),0,H)]:
        assert displaced_mass(b-H,H,d,A,600,1000)==(m,h1,h2)
    assert displaced_mass(0,H,d,A,600,1000)[0]==F(8,5)
    assert F(21,10)>A*1000*H
    wrong=(F(9,5)/A+400*d)/1000
    assert wrong==F(11,25) and wrong>H
    assert displaced_mass(wrong-H,H,d,A,600,1000)[0]!=F(9,5)

def test_wrong_dimension_and_limit_negative_control():
    correct=1000*10*F(1,10)
    wrong=10*F(1,10)
    assert correct==1000 and wrong!=correct
    print("WRONG_DIMENSION REJECTED: missing density gives 1 instead of 1000 Pa; kg/m^3 factor required.")
    H=F(2,5);d=F(1,5);A=F(1,200)
    wrong=F(11,25)
    assert displaced_mass(wrong-H,H,d,A,600,1000)[0]!=F(9,5)
    print("WRONG_SIGN_OR_LIMIT REJECTED: 44 cm emerged continuation exceeds 40 cm height and fails true force balance.")

def test_structured_fields_no_answer_values():
    t=load(P/"task.v1.json");m=load(P/"model.v1.json")
    assert {r["id"] for r in m["rubric"]}<={r["id"] for r in t["fields"]}
    assert all("expected" not in r and "repair" not in r for r in t["fields"])
    assert t["revision"]=="r2-20261115"
    assert len(m["reasoningRubric"])==4 and len(m["reconstructionSteps"])==4
    guide=(PH/"textbook/PH06/U08/index.html").read_text()
    assert "1.60 kg" in guide and "0.44 m" in guide and "u08-regimes.svg" in guide
    assert "3.20 kg" not in guide and "5 cm below" not in guide

import json
from pathlib import Path
from fractions import Fraction
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"nsejs/physics/ph05/source-led-r2"
def load(name): return json.loads((D/name).read_text(encoding="utf-8"))
def test_source_led_inventory():
    d=load("packages.v1.json")
    assert d["release"]=="HOLD"
    assert len(d["packages"])==8
    assert len(d["census"]["source_records"])==10 and d["census"]["closed"]==0
    original=json.loads((ROOT/"nsejs/physics/curriculum/agent1/ph01-ph06-syllabus-inventory.v1.json").read_text())
    expected=next(c["subtopics"] for c in original["chapters"] if c["topic_id"]=="PH05")
    assert [(x["id"],x["title"],x["scope"]) for x in d["stable_subtopics"]]==[(x["subtopic_id"],x["title"],x["scope_role"]) for x in expected]
    assert all(x["packages"] for x in d["stable_subtopics"])
    tasks=[t for p in d["packages"] for t in p["tasks"]]
    assert len(tasks)==len({t["uid"] for t in tasks})==14
    assert sum(t["cell"].startswith("D4.") for t in tasks)==3
    assert all(t["nomination"]=="AUTHOR_ONLY_NOT_QUALIFIED" for t in tasks)
    assert sum(len(p["examples"]) for p in d["packages"][:6])==18
    assert len({s for p in d["packages"] for s in p["source_locators"]})==10
def test_figures_and_model_separation():
    d=load("packages.v1.json"); models=load("models.v1.json")
    assert models["status"]=="AUTHOR_ONLY_HOLD"
    assert len(list((D/"figures").glob("*.svg")))==23
    for p in d["packages"]:
        ET.parse(D/p["guide"])
        for t in p["tasks"]:
            assert not {"reconstruction","w","hints","boundaryModel"} & set(t)
            m=next(x for x in models["models"] if x["uid"]==t["uid"])
            assert m["revision"]==t["revision"] and len(m["hints"])==3
            assert all(m[x] for x in ("w","alternative","diagnosis","repair","boundaryPrompt","boundaryModel"))
            doc=ET.parse(D/t["figure"])
            assert doc.getroot().tag.endswith("svg")
            assert not any(x.tag.endswith(("script","foreignObject")) for x in doc.iter())
def test_math_witnesses():
    assert Fraction(9,13)<1 and 3*(1/Fraction(9,13)-1)==Fraction(4,3)
    assert 3*Fraction(2,3)==2
    assert Fraction(3,2)/3==Fraction(1,2)
    assert 3*Fraction(1,2)**3==Fraction(3,8)
    assert -8+3*3-5*2==-9
    assert 5*Fraction(9,5)**2+16*Fraction(9,5)==45
    assert 8*2==4**2
    assert 4**3==8**2
    assert (140000-120000)/(2000*5)==2
def test_protection_contract():
    s=(D/"reader.js").read_text()
    assert "navigator.locks.request" in s and "localStorage.getItem(key)!==raw" in s
    assert "JSON.stringify([task,model,fig])" in s
    assert "if(rec.boundaryReveal)" in s

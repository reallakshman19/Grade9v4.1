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
    assert len(d["packages"])==9
    assert len(d["census"]["source_records"])==14 and d["census"]["closed"]==0
    original=json.loads((ROOT/"nsejs/physics/curriculum/agent1/ph01-ph06-syllabus-inventory.v1.json").read_text())
    expected=next(c["subtopics"] for c in original["chapters"] if c["topic_id"]=="PH05")
    assert [(x["id"],x["title"],x["scope"]) for x in d["stable_subtopics"]]==[(x["subtopic_id"],x["title"],x["scope_role"]) for x in expected]
    assert all(x["packages"] for x in d["stable_subtopics"])
    tasks=[t for p in d["packages"] for t in p["tasks"]]
    assert len(tasks)==len({t["uid"] for t in tasks})==15
    assert sum(t["cell"].startswith("D4.") for t in tasks)==3
    assert all(t["nomination"]=="AUTHOR_ONLY_NOT_QUALIFIED" for t in tasks)
    assert sum(len(p["examples"]) for p in d["packages"][:6])==18
    assert len({s for p in d["packages"] for s in p["source_locators"]})==14
def test_figures_and_model_separation():
    d=load("packages.v1.json"); models=load("models.v1.json")
    assert models["status"]=="AUTHOR_ONLY_HOLD"
    assert len(list((D/"figures").glob("*.svg")))==25
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

def test_canonical_route_migration_and_review_rows():
    d=load("packages.v1.json");m=load("migration.v1.json")
    assert [x["id"] for x in m["canonical"]]==[x["id"] for x in d["stable_subtopics"]]
    for x in m["canonical"]:
        for k in ("learn","practice"):
            assert (D/x[k]).resolve().is_file()
        assert "?legacy=1" in x["legacy_learn"] and x["legacy_task_uid"]
    r=json.loads((ROOT/"review/physics/ph05-source-first-r1/R2_TASK_B1_B7_HANDOFF_R5.json").read_text())
    assert len(r["rows"])==15 and r["independent_pass_rows"]==0
    assert all(x["B"+str(i)]["status"]=="HOLD" for x in r["rows"] for i in range(1,8))
    ids={x["id"] for x in d["census"]["source_records"]}
    assert "IOQJS-2021-22-C51-Q02" not in ids and "IOQJS-2021-22-C51-Q19" in ids
    assert 2*(30+5)==40+6*5

def test_current_source_led_adapter_exact_join():
    d=load("packages.v1.json");m=load("models.v1.json")
    a=json.loads((ROOT/"nsejs/physics/curriculum/topics/PH05/adapter-gravitation.source-led.v0.2.json").read_text())
    assert a["academic_status"]=="HOLD"
    assert {x["uid"] for x in a["tasks"]}=={x["uid"] for x in m["models"]}
    assert {x["subtopic_id"]:x["title"] for x in a["subtopics"]}=={x["id"]:x["title"] for x in d["stable_subtopics"]}
    assert sum(len(x["instance_ids"]) for x in a["cells"])==15
    assert all(x["qrt"]=="HOLD" for x in a["tasks"])

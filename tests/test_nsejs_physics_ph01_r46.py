"""R4.6 batch: native C06 membership, 2025 locator-only status, old immutable history, exact numerical witnesses."""
import hashlib,importlib.util,json,math
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
PH="nsejs/physics/curriculum/agent1/PH01/"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def test_r46_native_and_membership():
    spec=importlib.util.spec_from_file_location("ph01_r46_validator",ROOT/"nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    receipt=mod.inspect_package(ROOT/"nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_6.json")
    assert receipt["issues"]==[],receipt
    assert receipt["mechanical_status"]=="PASS" and receipt["academic_status"]==receipt["release_status"]=="HOLD"
    p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_6.json");r=load("nsejs/physics/curriculum/agent1/PH01/ph01-subtopic-routes.r4_6.json")
    assert len(p["core1b"])==60 and len(p["subtopics"])==8
    assert p["topic_adapter"]==load(PH+"topic-adapter.PH01.v0.10.0.json")
    assert blob(PH+"physics-topic-package.v1_1.r4_5.json")==r["prior_r45_package_blob"]
    assert blob(PH+"ph01-core1b-support.r4_5.json")==r["prior_r45_support_blob"]
    owner={q["id"]:s["id"] for s in p["subtopics"] for q in s["qrt_targets"]}
    for cell,n,owners in [("D3.3",6,{"PH01-M01","PH01-M03","PH01-M04","PH01-M06","PH01-M08"}),("D4.4",4,{"PH01-M01","PH01-M02","PH01-M06","PH01-M08"})]:
        actual={c["qrt_target_id"] for c in p["core1b"] if c["kind"]=="INSTANCE" and c["cell_id"]==cell}
        main=next(c for c in p["core1b"] if c["kind"]=="MAIN" and c["cell_id"]==cell)
        adapter=next(c for c in p["topic_adapter"]["cells"] if c["cell_id"]==cell)
        assert len(actual)==n and set(main["instance_qrt_ids"])==actual==set(adapter["instance_ids"])
        assert {owner[q] for q in actual}==owners and main["id"].endswith("R46")
    old={c["id"]:c for c in load(PH+"physics-topic-package.v1_1.r4_5.json")["core1b"]}
    new={c["id"]:c for c in p["core1b"]}
    assert len(set(old)-set(new))==2 and len(set(new)-set(old))==6
    for cid in set(new)&set(old):assert new[cid]==old[cid]
    for u in r["units"]:
        assert all((ROOT/u[k]).is_file() for k in ("core1a","core1b","previous_core1b"))
        assert 'data-scope="'+u["subtopic_id"]+'"' in (ROOT/u["core1b"]).read_text()
def test_r46_source_locators_not_registry():
    m=load("nsejs/physics/curriculum/agent1/PH01/ph01-core2-construction-map.r4_6.json");old=load(PH+"ph01-core2-construction-map.r4_5.json")
    l=load("nsejs/physics/curriculum/agent1/PH01/ph01-2025-locator-transfers.r4_6.json");p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_6.json")
    assert m["counts"]==old["counts"]
    assert sum(len(x["preparation"]) for x in m["records"])==87
    for a,b in zip(m["records"],old["records"],strict=True):
        assert a["canonical_records"]==b["canonical_records"] and a["bank_record"]==b["bank_record"]
    assert l["counts"]=={"locators":4,"canonical_bindings":0,"bank_bindings":0,"authenticated":0,"qualified":0}
    assert {z["question_number"] for z in l["records"]}=={33,41,43,48}
    for z in l["records"]:
        assert z["canonical_uid"] is None and z["bank_id"] is None and z["source_band"]=="HOLD" and z["exact_fit"]=="HOLD"
        assert any(c["id"]==z["cycle_id"] and c["qrt_target_id"]==z["transfer_id"] for c in p["core1b"])
        assert (ROOT/z["core1b"]).is_file() and (ROOT/z["core1a"]).is_file()
        assert f'r46-q{z["question_number"]}' in (ROOT/z["core1a"]).read_text()
    q=load("nsejs/core2/question-map.v1.json")
    assert not any("2025" in (x.get("claimed_external_question_id") or "") for x in q["questions"] if x["subject"]=="PHYSICS")
def test_r46_numeric_witnesses():
    f=lambda s:F(6)+s+F(20)/s
    assert f(F(2))==18 and f(F(6))==F(46,3)
    assert 2<math.sqrt(20)<6 and 6+2*math.sqrt(20)<float(f(F(6)))
    for s in [F(1),F(2),F(6),F(7)]:assert f(s)>=F(46,3)
    assert 9*F(14,3)-42==0 and 9*F(34,3)-42==60
    assert 9*F(82,9)-82==0 and 3*6-18==0
    u=F(35,4);H=2*u+20
    assert H==F(75,2)==-10*u+125 and 2*u/10==F(7,4)
    assert u+20==F(115,4) and -2*u+50==F(65,2)
    assert F(360,6)+F(360,4)+30==180 and F(720,180)==4
    assert F(25)-F(3600,140)==F(-5,7)
    d=5*math.pi/2;L=10*math.pi
    U=(d+10.5)/2
    assert math.isclose(2*U,d+2*3+3**2/2)
    t=-2+math.sqrt(4+15*math.pi)
    assert 1<t<7 and math.isclose(d+2*t+t*t/2,L)
    assert F(12,4)*2+2==8

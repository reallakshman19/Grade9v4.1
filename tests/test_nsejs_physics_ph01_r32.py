"""PH01 eight-subtopic candidate package and route integrity; not academic qualification."""
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics/curriculum/agent1/PH01/"
def obj(name): return json.loads((PH/name).read_text(encoding="utf-8"))
def test_r32_contract_and_counts():
    spec=importlib.util.spec_from_file_location("ph01_r32_validator",ROOT/"nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    receipt=mod.inspect_package(PH/"physics-topic-package.v1_1.r3_2.json")
    assert receipt["issues"]==[],receipt
    assert receipt["mechanical_status"]=="PASS"
    assert receipt["academic_status"]==receipt["release_status"]=="HOLD"
    p=obj("physics-topic-package.v1_1.r3_2.json")
    assert len(p["subtopics"])==8
    assert len(p["core1a"])==8
    assert len(p["core1b"])==27
    assert p["topic_adapter"]==obj("topic-adapter.PH01.v0.4.0.json")
    assert not p["core2_sources"]
    for cell in p["topic_adapter"]["cells"]:
        assert len(cell["instance_ids"])==8
        main=[c for c in p["core1b"] if c["kind"]=="MAIN" and c["cell_id"]==cell["cell_id"]]
        assert len(main)==1 and set(main[0]["instance_qrt_ids"])==set(cell["instance_ids"])
    assert {c["id"] for c in p["core1b"]}=={c["cycle_id"] for c in obj("ph01-core1b-support.r3_2.json")["cycles"]}
    assert obj("ph01-subtopic-qrt-coverage.r3_2.json")["summary"]["qualified_qrt_targets"]==0
def test_r32_all_eight_independent_routes_and_prior_bytes():
    r=obj("ph01-subtopic-routes.r3_2.json")
    assert len(r["units"])==8 and r["release"]=="HOLD"
    import hashlib
    for path,sha in [(PH/"physics-topic-package.v1_1.r3_1.json",r["prior_package_blob"]),(PH/"ph01-core1b-support.r3_1.json",r["prior_support_blob"])]:
        b=path.read_bytes()
        assert hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==sha
    for u in r["units"]:
        a,b=ROOT/u["core1a"],ROOT/u["core1b"]
        assert a.is_file() and b.is_file()
        assert u["subtopic_id"] in a.read_text(encoding="utf-8")
        assert f'data-scope="{u["subtopic_id"]}"' in b.read_text(encoding="utf-8")
        p=json.loads((ROOT/u["delivery_package"]).read_text(encoding="utf-8"))
        assert set(u["instance_ids"])=={c["id"] for c in p["core1b"] if c["kind"]=="INSTANCE" and c["subtopic_id"]==u["subtopic_id"]}
        assert len(u["instance_ids"])==3 and u["qualified"]==0
    assert 'data-scope="MAIN"' in (ROOT/r["integrated_main"]["path"]).read_text(encoding="utf-8")
def test_r32_numeric_checks():
    from fractions import Fraction as F
    assert (-13+4*4)==3
    assert F(5,3)<4 and 7-4==3
    assert 12*2-F(3,2)*4==18 and 12*6-F(3,2)*36==18
    assert F(9,4)+F(9,4)+6==F(21,2)
    assert sum([-3,-1,1,3,8])==8 and sum(map(abs,[-3,-1,1,3,8]))==16
    assert 2*9+2*F(-3,2)==15 and 4*9+8*F(-3,2)==24
    assert F(106,7)==8+F(32,7)+F(18,7)
    assert F(24,16)==F(3,2)
    assert F(36,7)>2 and F(30,4)<9
    import math
    assert 2*math.pi+8<16
    assert (math.pi+math.pi+4)*4/2==4*math.pi+8

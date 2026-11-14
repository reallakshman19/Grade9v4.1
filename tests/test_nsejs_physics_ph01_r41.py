"""R4.1 native source-linked and D4 author candidate checks."""
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics/curriculum/agent1/PH01/"
def test_r41():
    spec=importlib.util.spec_from_file_location("ph01_r41_validator",ROOT/"nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    receipt=mod.inspect_package(PH/"physics-topic-package.v1_1.r4_1.json")
    assert receipt["issues"]==[],receipt
    assert receipt["mechanical_status"]=="PASS" and receipt["academic_status"]==receipt["release_status"]=="HOLD"
    p=json.loads((PH/"physics-topic-package.v1_1.r4_1.json").read_text())
    assert len(p["subtopics"])==8 and len(p["core1b"])==30
    assert len([c for c in p["core1b"] if c["cell_id"]=="D4.6"])==3
    assert len(p["core2_sources"])==4 and all(s["source_role"]=="PREREQUISITE_BRIDGE" and s["academic_status"]=="HOLD" for s in p["core2_sources"])
    m=json.loads((ROOT/"nsejs/physics/curriculum/agent1/PH01/ph01-core2-construction-map.r4_1.json").read_text())
    for r in m["records"]:
        for x in r["preparation"]:assert any(c["id"]==x["cycle_id"] for c in p["core1b"])
def test_numeric():
    from fractions import Fraction as F
    assert (F(19,15)+2)*F(30,7)==14 and 60-7*F(30,7)==30
    assert (F(11,19)+2)*F(38,7)==14 and 60-7*F(38,7)==22
    import math
    b=math.sqrt(5)+1; L=40/(4+b)
    assert abs(b*b*L/(2*(4+b))-4)<1e-10

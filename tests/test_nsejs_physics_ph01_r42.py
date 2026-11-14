"""PH01 R4.2 native package, source identities, preserved revisions and route checks."""
import hashlib, importlib.util, json
from pathlib import Path
from tools.ph01_source_pin_custody import pinned_blob_sha
ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics/curriculum/agent1/PH01/"
def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def test_r42_native_and_routes():
    spec=importlib.util.spec_from_file_location("ph01_r42_validator",ROOT/"nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    receipt=mod.inspect_package(PH/"physics-topic-package.v1_1.r4_2.json")
    assert receipt["issues"]==[],receipt
    assert receipt["mechanical_status"]=="PASS" and receipt["academic_status"]==receipt["release_status"]=="HOLD"
    p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_2.json");r=load("nsejs/physics/curriculum/agent1/PH01/ph01-subtopic-routes.r4_2.json")
    assert len(p["core1b"])==38 and len(p["subtopics"])==8
    assert p["topic_adapter"]==load("nsejs/physics/curriculum/agent1/PH01/topic-adapter.PH01.v0.6.0.json")
    assert blob("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_1.json")==r["prior_r41_package_blob"]
    assert blob("nsejs/physics/curriculum/agent1/PH01/ph01-core1b-support.r4_1.json")==r["prior_r41_support_blob"]
    assert len(r["integrated_main"]["cycle_ids"])==6
    for u in r["units"]:
        assert (ROOT/u["core1a"]).is_file() and (ROOT/u["core1b"]).is_file() and (ROOT/u["previous_core1b"]).is_file()
        assert len(u["instance_ids"])==4
        assert len([c for c in p["core1b"] if c["id"] in u["instance_ids"] and c["cell_id"].startswith("D4.")])==1
        assert 'data-scope="'+u["subtopic_id"]+'"' in (ROOT/u["core1b"]).read_text()
def test_r42_source_registry():
    m=load("nsejs/physics/curriculum/agent1/PH01/ph01-core2-construction-map.r4_2.json")
    assert m["counts"]=={"locators":15,"canonical_records":16,"bank_records":4,"primary":7,"cross_topic":7,"dropped":1,"qualified":0}
    for item in m["source_inventory"].values():
        if isinstance(item,dict) and "git_blob_sha" in item: assert pinned_blob_sha(ROOT,item)==item["git_blob_sha"]
    c={q["question_uid"]:q for q in load("nsejs/core2/question-map.v1.json")["questions"]}
    p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_2.json")
    for rec in m["records"]:
        assert rec["exact_fit"]==rec["source_status"]=="HOLD"
        for q in rec["canonical_records"]: assert c[q["question_uid"]]["content_revision_sha256"]==q["content_revision_sha256"]
        for q in rec["preparation"]:
            assert any(x["id"]==q["cycle_id"] and x["qrt_target_id"]==q["qrt_target_id"] for x in p["core1b"])
            assert (ROOT/q["core1b"]).is_file()
    assert any(q["claimed_external_question_id"]=="NSEJS-2020-P-Q05" for r in m["records"] for q in r["canonical_records"])
def test_numeric_witnesses():
    from fractions import Fraction as F
    assert (8-9)**2+6**2==37 and 8**2+6**2==100
    assert F(192,25)-F(42,25)==6 and F(56,25)+F(144,25)==8
    assert 600+90==690 and 600-90==510 and 120+45+135==300
    assert 6+24/3==14 and 12**2/(2*3)==24
    assert 240-30*F(23,3)==10 and 120-30*F(24,7)==F(120,7)
    assert F(18,20)*5==F(9,2) and F(36,10)+F(108,100)==F(468,100)
    assert 36-4*4==20 and 20+2*4.5==29
    assert 180-F(78,5)*10==24

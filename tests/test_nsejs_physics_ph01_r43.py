"""PH01 R4.3 operation-specific candidates, stable source identities and historical revisions."""
import hashlib,importlib.util,json
from pathlib import Path
from tools.ph01_source_pin_custody import pinned_blob_sha
ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics/curriculum/agent1/PH01/"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def test_r43_native():
    spec=importlib.util.spec_from_file_location("ph01_r43_validator",ROOT/"nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    receipt=mod.inspect_package(PH/"physics-topic-package.v1_1.r4_3.json")
    assert receipt["issues"]==[],receipt
    assert receipt["mechanical_status"]=="PASS" and receipt["academic_status"]==receipt["release_status"]=="HOLD"
    p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_3.json");r=load("nsejs/physics/curriculum/agent1/PH01/ph01-subtopic-routes.r4_3.json")
    assert len(p["core1b"])==49 and len(p["subtopics"])==8
    assert len(r["integrated_main"]["cycle_ids"])==8
    assert p["topic_adapter"]==load("nsejs/physics/curriculum/agent1/PH01/topic-adapter.PH01.v0.7.0.json")
    assert blob("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_2.json")==r["prior_r42_package_blob"]
    assert blob("nsejs/physics/curriculum/agent1/PH01/ph01-core1b-support.r4_2.json")==r["prior_r42_support_blob"]
    counts={u["subtopic_id"]:len(u["instance_ids"]) for u in r["units"]}
    assert sorted(counts.values())==[4,5,5,5,5,5,6,6]
    for cell,n in [("D3.3",4),("D3.7",5)]:
        assert len([c for c in p["core1b"] if c["cell_id"]==cell and c["kind"]=="INSTANCE"])==n
        main=next(c for c in p["core1b"] if c["cell_id"]==cell and c["kind"]=="MAIN")
        assert len(main["instance_qrt_ids"])==n
    for u in r["units"]:
        for key in ("core1a","core1b","previous_core1b"):assert (ROOT/u[key]).is_file()
        assert 'data-scope="'+u["subtopic_id"]+'"' in (ROOT/u["core1b"]).read_text()
        assert len([c for c in p["core1b"] if c["id"] in u["instance_ids"] and c["cell_id"].startswith("D4.")])==1
def test_r43_source_routes():
    m=load("nsejs/physics/curriculum/agent1/PH01/ph01-core2-construction-map.r4_3.json");p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_3.json")
    assert m["counts"]==load("nsejs/physics/curriculum/agent1/PH01/ph01-core2-construction-map.r4_2.json")["counts"]
    for item in m["source_inventory"].values():
        if isinstance(item,dict) and "git_blob_sha" in item:assert pinned_blob_sha(ROOT,item)==item["git_blob_sha"]
    c={q["question_uid"]:q for q in load("nsejs/core2/question-map.v1.json")["questions"]}
    for rec in m["records"]:
        assert rec["exact_fit"]==rec["source_status"]=="HOLD"
        for q in rec["canonical_records"]:assert c[q["question_uid"]]["content_revision_sha256"]==q["content_revision_sha256"]
        for q in rec["preparation"]:
            assert any(x["id"]==q["cycle_id"] and x["qrt_target_id"]==q["qrt_target_id"] for x in p["core1b"])
            assert (ROOT/q["core1b"]).is_file()
    for year,no,cell in [(2024,33,"D3.3"),(2024,37,"D3.3"),(2024,46,"D3.7"),(2024,60,"D3.7"),(2023,60,"D3.7")]:
        rec=next(x for x in m["records"] if x["year"]==year and x["question_number"]==no)
        assert any(q["cell_id"]==cell and q["fit"]=="AUTHORED_OPERATION_SPECIFIC_TRANSFER_NOT_SOURCE_BAND" for q in rec["preparation"])
def test_numeric_and_proof_witnesses():
    from fractions import Fraction as F
    assert (-5-15)/2.5==-8 and F(20,6)==F(10,3)
    assert F(9,2)*2-2*4==1 and F(1,9)!=F(5,6)
    assert 15*4-F(5,2)*16==20 and 225-10*F(45,2)==0 and 225-10*F(55,2)==-50
    assert F(3,8)/F(3,10)==F(5,4) and F(5,2)/F(3,4)==F(10,3)
    assert (38-14)//2==12 and (38+14)//2==26
    assert F(36,8)==F(9,2) and F(9,2)!=6
    assert F(1,2)*F(1,2)==F(1,4) and 12+2*F(1,4)==F(25,2)
    assert F(1,2)*F(1,2)*F(1,4)==F(1,16)
    assert F(1,2)+2*F(1,16)==F(5,8)

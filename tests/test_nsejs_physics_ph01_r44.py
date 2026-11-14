"""PH01 R4.4 causal/proof candidates, immutable source identities and historical revisions."""
import hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics/curriculum/agent1/PH01/"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def test_r44_native():
    spec=importlib.util.spec_from_file_location("ph01_r44_validator",ROOT/"nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    receipt=mod.inspect_package(PH/"physics-topic-package.v1_1.r4_4.json")
    assert receipt["issues"]==[],receipt
    assert receipt["mechanical_status"]=="PASS" and receipt["academic_status"]==receipt["release_status"]=="HOLD"
    p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_4.json");r=load("nsejs/physics/curriculum/agent1/PH01/ph01-subtopic-routes.r4_4.json")
    assert len(p["core1b"])==56 and len(p["subtopics"])==8
    assert len(r["integrated_main"]["cycle_ids"])==10
    assert p["topic_adapter"]==load("nsejs/physics/curriculum/agent1/PH01/topic-adapter.PH01.v0.8.0.json")
    assert blob("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_3.json")==r["prior_r43_package_blob"]
    assert blob("nsejs/physics/curriculum/agent1/PH01/ph01-core1b-support.r4_3.json")==r["prior_r43_support_blob"]
    assert sorted(len(u["instance_ids"]) for u in r["units"])==[4,5,5,5,6,7,7,7]
    for cell,n in [("D3.2",3),("D4.7",2)]:
        assert len([c for c in p["core1b"] if c["cell_id"]==cell and c["kind"]=="INSTANCE"])==n
        main=next(c for c in p["core1b"] if c["cell_id"]==cell and c["kind"]=="MAIN")
        assert len(main["instance_qrt_ids"])==n
    for u in r["units"]:
        for key in ("core1a","core1b","previous_core1b"):assert (ROOT/u[key]).is_file()
        assert 'data-scope="'+u["subtopic_id"]+'"' in (ROOT/u["core1b"]).read_text()
        assert any(c["id"] in u["instance_ids"] and c["cell_id"].startswith("D4.") for c in p["core1b"])
def test_r44_source_routes():
    m=load("nsejs/physics/curriculum/agent1/PH01/ph01-core2-construction-map.r4_4.json");p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_4.json")
    assert m["counts"]==load("nsejs/physics/curriculum/agent1/PH01/ph01-core2-construction-map.r4_3.json")["counts"]
    for item in m["source_inventory"].values():
        if isinstance(item,dict) and "git_blob_sha" in item:assert blob(item["path"])==item["git_blob_sha"]
    c={q["question_uid"]:q for q in load("nsejs/core2/question-map.v1.json")["questions"]}
    for rec in m["records"]:
        assert rec["exact_fit"]==rec["source_status"]=="HOLD"
        for q in rec["canonical_records"]:assert c[q["question_uid"]]["content_revision_sha256"]==q["content_revision_sha256"]
        for q in rec["preparation"]:
            assert any(x["id"]==q["cycle_id"] and x["qrt_target_id"]==q["qrt_target_id"] for x in p["core1b"])
            assert (ROOT/q["core1b"]).is_file()
    for year,no,cell in [(2022,35,"D3.2"),(2024,37,"D3.2"),(2024,46,"D4.7"),(2024,60,"D4.7"),(2023,60,"D4.7")]:
        rec=next(x for x in m["records"] if x["year"]==year and x["question_number"]==no)
        assert any(q["cell_id"]==cell and q["fit"]=="AUTHORED_CAUSAL_OR_PROOF_TRANSFER_NOT_SOURCE_BAND" for q in rec["preparation"])
def test_proof_witnesses():
    from fractions import Fraction as F
    def dx(u,a,p,b,q):return u*p+a*p*p/2+(u+a*p)*q+b*q*q/2
    for u in (F(0),F(5),F(-5)):
        a,b,p,q=F(2),F(-2),F(2),F(2)
        assert dx(u,a,p,b,q)-dx(u,b,q,a,p)==(a-b)*p*q==16
    assert dx(F(0),a,p,b,q)==8 and dx(F(0),b,q,a,p)==-8
    assert dx(F(5),a,p,b,q)==28 and dx(F(5),b,q,a,p)==12
    assert (F(1,3)+F(1,2))/2==F(5,12)
    v=[F(1),F(7,8),F(1,8),F(0)]; t=[F(0),F(1,4),F(3,4),F(1)]
    assert sum((v[i]+v[i+1])*(t[i+1]-t[i])/2 for i in range(3))==F(1,2)
    assert len(set((v[i+1]-v[i])/(t[i+1]-t[i]) for i in range(3)))==2
    a,b,p,q,u=F(-1,2),F(-3,2),F(1,2),F(1,2),F(1)
    assert dx(u,a,p,b,q)==F(5,8) and dx(u,b,q,a,p)==F(3,8)

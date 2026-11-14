"""R4.5 author correction: exact native membership, new identities, immutable history and independent numerical witnesses."""
import hashlib,importlib.util,json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
PH="nsejs/physics/curriculum/agent1/PH01/"
def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def test_r45_native_and_exact_membership():
    spec=importlib.util.spec_from_file_location("ph01_r45_validator",ROOT/"nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    receipt=mod.inspect_package(ROOT/"nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_5.json")
    assert receipt["issues"]==[],receipt
    assert receipt["mechanical_status"]=="PASS" and receipt["academic_status"]==receipt["release_status"]=="HOLD"
    p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_5.json");r=load("nsejs/physics/curriculum/agent1/PH01/ph01-subtopic-routes.r4_5.json")
    assert len(p["core1b"])==56 and len(p["subtopics"])==8
    assert p["topic_adapter"]==load(PH+"topic-adapter.PH01.v0.9.0.json")
    assert blob(PH+"physics-topic-package.v1_1.r4_4.json")==r["prior_r44_package_blob"]
    assert blob(PH+"ph01-core1b-support.r4_4.json")==r["prior_r44_support_blob"]
    target_owner={q["id"]:s["id"] for s in p["subtopics"] for q in s["qrt_targets"]}
    for cell,owners in [("D3.2",{"PH01-M04","PH01-M05","PH01-M08"}),("D4.7",{"PH01-M05","PH01-M06"})]:
        actual={c["qrt_target_id"] for c in p["core1b"] if c["kind"]=="INSTANCE" and c["cell_id"]==cell}
        main=next(c for c in p["core1b"] if c["kind"]=="MAIN" and c["cell_id"]==cell)
        adapter=next(c for c in p["topic_adapter"]["cells"] if c["cell_id"]==cell)
        assert set(main["instance_qrt_ids"])==actual==set(adapter["instance_ids"])
        assert {target_owner[q] for q in actual}==owners
        assert all(q.endswith("R45") for q in actual) and main["id"].endswith("R45")
    prior=load(PH+"physics-topic-package.v1_1.r4_4.json")
    old={c["id"]:c for c in prior["core1b"]};new={c["id"]:c for c in p["core1b"]}
    assert len(set(old)-set(new))==len(set(new)-set(old))==7
    for cid in set(new)-set(old):
        c=new[cid];o=old[cid.replace("R45","R44")]
        assert c["fresh_task"]!=o["fresh_task"] and c["stages"]["diagnose"]!=o["stages"]["diagnose"]
        assert c["stages"]["repair"]!=o["stages"]["repair"]
    for cid in set(new)&set(old):assert new[cid]==old[cid]
    for u in r["units"]:
        assert all((ROOT/u[k]).is_file() for k in ("core1a","core1b","previous_core1b"))
        assert 'data-scope="'+u["subtopic_id"]+'"' in (ROOT/u["core1b"]).read_text()
def test_r45_source_and_packet():
    m=load("nsejs/physics/curriculum/agent1/PH01/ph01-core2-construction-map.r4_5.json");old=load(PH+"ph01-core2-construction-map.r4_4.json");p=load("nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.r4_5.json")
    assert m["counts"]==old["counts"]
    assert sum(len(x["preparation"]) for x in m["records"])==87
    canonical={q["question_uid"]:q for q in load("nsejs/core2/question-map.v1.json")["questions"]}
    for r,o in zip(m["records"],old["records"],strict=True):
        assert r["id"]==o["id"] and r["canonical_records"]==o["canonical_records"] and r["bank_record"]==o["bank_record"]
        assert r["source_status"]==r["exact_fit"]=="HOLD"
        for q in r["canonical_records"]:assert canonical[q["question_uid"]]["content_revision_sha256"]==q["content_revision_sha256"]
        for z in r["preparation"]:assert any(c["id"]==z["cycle_id"] and c["qrt_target_id"]==z["qrt_target_id"] for c in p["core1b"])
    packet=load(PH+"ph01-r45-review-packet.json")
    assert packet["status"]=="AUTHOR_EXPOSED_HOLD" and len(packet["items"])==7
    assert packet["statistics"]["authenticated_core2_items"]==packet["statistics"]["independently_qualified_qrts"]==0
    assert packet["statistics"]["authored_preparation_associations"]==87
    for x in packet["items"]:
        assert len(x["factor_evidence"])==5 and x["review"]=="HOLD"
        assert all(x["B"+str(i)] for i in range(1,8))
def test_r45_exact_fresh_witnesses():
    def vertices(u,rates,h):
        v=[F(u)]
        for a in rates:v.append(v[-1]+a*h)
        return v
    def signed(v,h):return sum((a+b)*h/2 for a,b in zip(v,v[1:]))
    def path(v,h):
        return sum((abs(a)+abs(b))*h/2 if a*b>=0 else (a*a+b*b)*h/(2*(abs(a)+abs(b))) for a,b in zip(v,v[1:]))
    for a,b,c in [(F(1),F(-3),F(5)),(F(2),F(3),F(-4))]:
        x=vertices(0,[a,b,c],F(1));y=vertices(0,[b,c,a],F(1))
        assert signed(x,F(1))-signed(y,F(1))==2*a-b-c and x[-1]==y[-1]
    x=vertices(0,[1,-3,5],F(1));y=vertices(0,[-3,5,1],F(1))
    assert signed(x,F(1))==signed(y,F(1))==F(1,2)
    assert path(x,F(1))==F(79,30) and path(y,F(1))==F(53,10)
    assert path([v+4 for v in x],F(1))==path([v+4 for v in y],F(1))==F(25,2)
    for z in [F(1,2),F(2,3),F(3,4)]:
        v=[F(1),z,1-z,F(0)]
        assert signed(v,F(1,3))==F(1,2)
        assert max(abs((b-a)*3) for a,b in zip(v,v[1:]))<=F(3,2)
        assert F(1,4)<=(1+z)/6<=F(7,24)
    assert (1+F(2,3))/6==F(5,18)
    for k,ratio in [(F(3,4),F(5,12)),(F(1),F(1,2)),(F(5,4),F(7,12)),(F(3,2),F(2,3))]:
        a=c=-k;b=-(3-2*k);h=F(1,3)
        assert max(abs(a),abs(b),abs(c))<=F(3,2)
        X=vertices(1,[a,b,c],h);Y=vertices(1,[c,b,a],h);Z=vertices(1,[b,a,c],h)
        assert X[-1]==Y[-1]==Z[-1]==0 and min(X+Y+Z)==0
        assert signed(X,h)==signed(Y,h)==F(1,2) and signed(Z,h)==ratio

"""PH03 R4 changed-W scientific arithmetic and exact R3 custody; author-side only.

A green result never means independent QRT/B1-B7 academic acceptance.
"""
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"nsejs/physics/ph03/complete-r3"
IDS=("P01","P04","P05","P06","P07")
EXPECTED_OLD={
 "P01":("8c24d5e08f3134d2ff6a875d4c7f57a0c4f0cfaa","5c0ac573990e576e1f9960324d5dcac32cca9354"),
 "P04":("ab04f102d7a799f3ffc9d5cfb01b6784969eeefb","6c27443a840b7eaf408f64cb7fe943ef8a4a1c63"),
 "P05":("19fa90246adfcd88da53479ff4b68007ef84ca22","63a8ce797d8f1d59d1fb23051cf55e58091720b9"),
 "P06":("b5cf1a49f5b2b320f9c9c293498c116e6cf6c33d","6ae027b72acc9824150e6383d6ef138b951adb0a"),
 "P07":("9407d60a91c99644362b54317c139b950e6b7e32","499eb72722c5d87a89d75e14cf5c0dc149bbda2e"),
}

def blob_sha1(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def task(id):
    return read(SRC/f"{id}.r4.json")

def post(id):
    return read(SRC/f"post-{id}.r4.json")

def test_original_r3_bytes_and_attempt_links_remain_unchanged():
    for id,(task_sha,post_sha) in EXPECTED_OLD.items():
        assert blob_sha1(SRC/f"{id}.json")==task_sha
        assert blob_sha1(SRC/f"post-{id}.json")==post_sha
        assert read(SRC/f"{id}.json")["revision"]=="ph03-complete-r3-20261116"
        assert task(id)["revision"]=="ph03-core1ab-r4-20261117"
    code=(SRC/"reader.js").read_text()
    assert 'get("revision")==="r3"' in code
    assert 'const taskFile=usesR4?unit+".r4.json":unit+".json"' in code
    assert 'const postFile=usesR4?"post-"+unit+".r4.json":"post-"+unit+".json"' in code
    assert 'Review earlier R3 attempts/version' in code
    assert 'storeKey="G9V41:PH03:R3:"+unit+":"+revision' in code

def test_r4_task_field_manifest_and_postattempt_byte_pins():
    for id in IDS:
        t,p=task(id),post(id)
        assert t["id"]==p["id"]==id
        assert t["academic"]==p["academic"]=="HOLD"
        assert t["taskVariant"]=="CORE1AB_R4_NOVEL_W_CANDIDATE"
        assert t["sourceRole"]=="AUTHOR_EXPOSITION_AND_TRANSFER_NOT_EXAM"
        assert t["revision"]==p["revision"]
        assert t["postBlobSha1"]==blob_sha1(SRC/f"post-{id}.r4.json")
        assert t["solutionBlobSha1"]==blob_sha1(SRC/t["figures"]["solution"])
        assert t["figures"]["prompt"].endswith("-prompt-r4.svg")
        assert t["figures"]["solution"].endswith("-solution-r4.svg")
        assert set(p["expected"])=={f["id"] for f in t["prompt"]["fields"]}
        assert set(p["boundaryExpected"])=={f["id"] for f in t["prompt"]["boundaryFields"]}
        assert set(p["firstErrorOrder"])==set(p["expected"])
        assert len(p["hints"])==3 and len(p["steps"])>=4
        assert all(h.startswith(s) for h,s in zip(p["hints"],("CLARIFY:","CORRELATE:","OPEN THE WAY:")))
        assert len(t["sections"])>=5 and len(t["worked"])>=3
        assert len(t["sections"][-1]["body"])>350
        assert t["researchNote"] and t["prompt"]["stem"]!=read(SRC/f"{id}.json")["prompt"]["stem"]
        assert not {"expected","reconstructionSteps","boundaryExpected"}.intersection(t)
        for role in ("prompt","solution"):
            raw=(SRC/t["figures"][role]).read_text()
            root=ET.fromstring(raw)
            assert root.attrib["viewBox"]=="0 0 940 345"
            assert not any(el.tag.endswith(("script","image","foreignObject")) for el in root.iter())
            labels=[el for el in root.iter() if el.tag.endswith("text")]
            assert len(labels)>=8
            assert min(int(el.attrib["font-size"]) for el in labels)>=18
        prompt=(SRC/t["figures"]["prompt"]).read_text()
        assert "Checked result" not in prompt
        assert "Reconstruction after attempt" not in prompt
    assert all(task(id)["revision"]!=read(SRC/f"{id}.json")["revision"] for id in IDS)

def test_independent_exact_arithmetic_five_redesigns():
    # P01: simultaneous inverse momentum and energy requirements.
    a_p=2*3
    a_k=F(1,2)*2*3**2
    b_p=0-a_p
    b_k=15-a_k
    b_m=F(b_p*b_p,2*b_k)
    b_v=F(b_p,b_m)
    assert (b_m,b_v,b_p,b_k)==(3,-2,-6,6)
    assert post("P01")["expected"]=={"hiddenMass":3,"hiddenV":-2,"hiddenP":-6,"hiddenK":6}
    assert post("P01")["boundaryExpected"]=={"feasible":"no","hiddenP":-6}
    assert 9-a_k==0 and b_p!=0  # nonzero p cannot yield zero K for finite positive mass
    # P04: pair plus each skater, with individually measured A.
    total=4;pa=2*(-2);pb=total-pa
    va_ext=pa-(-6);vb_ext=pb-(+6)
    assert (F(pb,3),va_ext,vb_ext)==(F(8,3),2,2)
    exp=post("P04")["expected"]
    assert F(str(exp["vB"])).limit_denominator(300)==F(8,3)
    assert exp["externalA"]==va_ext and exp["externalB"]==vb_ext
    assert exp["totalP"]==total and va_ext+vb_ext==total
    assert post("P04")["boundaryExpected"]=={"unique":"no","totalP":4}
    # P05: relative-to-lab translation with initially moving pair.
    p0=(8+2)*1;vp=F(p0-2*5,8+2);vload=vp+5
    assert (vp,vload,p0,F(p0,10))==(0,5,10,1)
    assert post("P05")["expected"]=={"platformV":0,"loadLab":5,"totalP":10,"cmV":1}
    assert post("P05")["boundaryExpected"]=={"platformV":0.25,"relativeSpeed":3.75}
    assert F(p0-2*4,8)==F(1,4)
    # P06: inverse restitution from observed outgoing A speed.
    vb=F(3*4-3*2,2);e=F(vb-2,4)
    ki=F(1,2)*3*4**2
    kf=F(1,2)*3*2**2+F(1,2)*2*vb**2
    assert (vb,e,ki-kf)==(3,F(1,4),9)
    assert post("P06")["expected"]=={"vB":3,"restitution":0.25,"loss":9,"admissible":"yes"}
    assert post("P06")["boundaryExpected"]=={"restitution":2.125,"admissible":"no"}
    assert F((3*4-3*(-1)),2)==F(15,2)
    # P07: threshold before collision, not a guaranteed event.
    v1=F(6,3);L=F(3,4);mu=F(1,5)
    mu_max=v1*v1/(2*10*L)
    pre2=v1*v1-2*mu*10*L
    assert mu_max==F(4,15) and pre2==1
    p=post("P07")["expected"]
    assert p["firstV"]==2 and F(str(p["thresholdMu"])).limit_denominator(500)==mu_max
    assert p["reach"]=="yes" and p["preImpact"]==1 and p["finalV"]==0.75
    assert post("P07")["boundaryExpected"]=={"reach":"no","stopDistance":2/3}

def test_r4_b3_b4_evidence_is_author_candidate_and_approval_remains_hold():
    for id in IDS:
        t=task(id)
        assert "candidate" in t["taskVariant"].lower() or "CANDIDATE" in t["taskVariant"]
        assert "HOLD"==t["academic"]
        b=t["sections"][-1]["body"].lower()
        if id=="P01": assert "p²=2mk" in b and "finite positive mass" in b
        if id=="P04": assert "external" in b and "individual" in b
        if id=="P05": assert "relative" in b and "centre-of-mass" in b
        if id=="P06": assert "restitution" in b and "0≤e≤1" in b
        if id=="P07": assert "μ_crit" in b and "stopping distance" in b
    science=read(SRC/"science-evidence.v1.json")
    assert all(all(x=="HOLD" for x in t["B1_B7"].values()) for t in science["topics"])

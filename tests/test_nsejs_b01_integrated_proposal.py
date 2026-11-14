"""Batch 12 author-side integration proposal checks; not independent acceptance."""
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/"nsejs/physics/curriculum/topics/PH07/b01"
def load(n):
    return json.loads((D/n).read_text(encoding="utf-8"))
def blob(p):
    b=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
C=load("B01_CUMULATIVE_SOURCE_TO_LEARNING.v2.json")
P=load("B01_INTEGRATED_CURRICULUM_PROPOSAL.v1.json")
E=load("B01_SOURCE_REVIEW_OVERLAY.v1.json")
Q=load("B01_R01_REVIEW_QUEUE.v1.json")

def test_old_register_and_source_conflicts_preserved():
    old=load("B01_CUMULATIVE_SOURCE_TO_LEARNING.v1.json")
    assert C["previous_register_blob"]==blob(D/"B01_CUMULATIVE_SOURCE_TO_LEARNING.v1.json")
    for a,b in zip(C["source_inventory"][:27],old["source_inventory"]):
        assert all(a[k]==v for k,v in b.items())
    assert len(C["source_inventory"])==len({r["identity"] for r in C["source_inventory"]})==32
    assert len(E["new_observations"])==5
    assert all(x["academic_admission"]=="HOLD" and x["source_bytes_sha256"] is None for x in E["new_observations"])
    assert {x["bank_source_id"] for x in E["identity_review_queue"]}=={"NSEJS-18-MAG-01","NSEJS-17-ELEC-01"}
    assert all(x["status"]=="OWNER_REVIEW_REQUIRED" for x in E["identity_review_queue"])
    q9=next(x for x in C["source_inventory"] if x["identity"]=="NSEJS-2018-JS511-Q9")
    assert q9["source"]["map_binding"] is not None
    assert q9["effective_map_binding"] is None
    assert q9["effective_identity_status"]=="REJECTED_IDENTITY_BINDING"
    assert sum(bool(x["effective_map_binding"]) for x in C["source_inventory"])==C["counts"]["metadata_bindings"]==12
    b=E["previous_source_followups"][0]
    assert "404" in b["official_paper_status"] and "THIRD_PARTY" in b["visual_copy_status"]
    assert C["counts"]["direct_exam_admissions"]==0
    assert C["counts"]["subtopics_with_primary_or_supporting_observations"]==24
    assert [r["subtopic_id"] for r in C["subtopic_rows"] if not r["primary_source_identities"] and not r["supporting_source_identities"]]==["PH08-09"]
    s=next(r for r in C["subtopic_rows"] if r["subtopic_id"]=="PH07-03")
    assert not s["primary_source_identities"] and s["supporting_source_identities"]==["NSEJS-2017-JS534-Q10"]
    for r in C["subtopic_rows"]:
        assert r["primary_source_identities"]==[x["identity"] for x in C["source_inventory"] if x["primary_subtopic"]==r["subtopic_id"]]
        assert r["supporting_source_identities"]==[x["identity"] for x in C["source_inventory"] if r["subtopic_id"] in x["supporting_subtopics"]]

def test_consolidated_exact_instance_binding_and_review_queue():
    pins={"registry":"B01_ADAPTER_RECONCILIATION.v1.json","mixed_main":"B01_MIXED_MAIN_PROPOSAL.v1.json","cumulative_v1":"B01_CUMULATIVE_SOURCE_TO_LEARNING.v1.json","cumulative_v2":"B01_CUMULATIVE_SOURCE_TO_LEARNING.v2.json","source_overlay":"B01_SOURCE_REVIEW_OVERLAY.v1.json","prior_supplement":"B01_PUBLISHER_LOCATOR_SUPPLEMENT.v1.json","earlier_screening":"B01_EARLIER_PUBLISHER_SCREENING.v1.json","session_screening":"B01_2018_2020_2021_SCREENING.v1.json"}
    for k,v in pins.items():
        assert P["source_pins"][k]==blob(D/v)
    assert len(P["groups"])==16
    ids=[]
    for g in P["groups"]:
        assert g["canonical_main"] is None and g["qualification"]=="HOLD"
        assert g["prior_mixed_main_proposal"] or g.get("new_mixed_main_proposal")
        for t in g["base_instances"]:
            ids.append(t["target_id"])
            assert blob(ROOT/t["package_path"])==t["package_blob"]
        for t in g["supplemental_instances"]:
            ids.append(t["target_id"])
            f=ROOT/t["proposal_path"]
            assert blob(f)==t["proposal_blob"]
            p=json.loads(f.read_text(encoding="utf-8"))
            assert p["target"]["id"]==t["target_id"]
            assert p["target"]["task_identity"]==t["task_identity"]
            assert p["target"]["cell"]==g["cell"]
            assert p["existing_package_pin"]["blob"]==t["base_package_blob"]
            assert p["existing_package_pin"]["version"]==t["base_package_version"]
            assert p["scope_role"]==t["scope_role"]
            assert t["instance_cycle"]==next(x["id"] for x in p["core1b"] if x["kind"]=="INSTANCE")
            assert t["prior_main_placeholder"]==next(x["id"] for x in p["core1b"] if x["kind"]=="MAIN_PLACEHOLDER")
            assert t["selection"]=="AUTHOR_PROPOSED_NOT_CANONICAL"
    assert len(ids)==len(set(ids))==89
    assert len(P["supplements"])==14
    assert {r["target_id"] for r in Q["targets"]}==set(ids)
    assert all(x["independent_score"] is None and x["review_status"]=="R01_NOT_RUN" for x in Q["targets"])
    assert len(Q["mixed_mains"])==16
    assert P["counts"]["selected_canonical_mains"]==0

def test_extension_gap_proposal_oracle():
    g=next(g for g in P["groups"] if g["tile_id"]=="PHY-PH07-D3.3")
    p=g["new_mixed_main_proposal"]
    assert p["scope"]=="EXTENSION_DEPENDENT" and p["academic_status"]=="HOLD"
    assert p["score"]==sum(x["score"] for x in p["factor_evidence"].values())==7
    R=F(3,4); E=(500+100)*15
    assert F(E,120-10)==F(900,11)
    assert E/(120/R-10)==60
    assert F(60)/F(900,11)==F(11,15)
    assert E/(120*R-10)==F(225,2)

def test_integrated_html_local_routes():
    class Links(HTMLParser):
        def __init__(self,s):
            super().__init__();self.links=[];self.feed(s)
        def handle_starttag(self,tag,attrs):
            if tag=="a" and "href" in dict(attrs):self.links.append(dict(attrs)["href"])
    p=D/"integrated-curriculum-review.html"
    text=p.read_text(encoding="utf-8")
    assert "ACADEMIC_HOLD" in text
    for href in Links(text).links:
        u=urlsplit(href)
        if not u.scheme and u.path:
            assert (p.parent/u.path).resolve().is_file(),href

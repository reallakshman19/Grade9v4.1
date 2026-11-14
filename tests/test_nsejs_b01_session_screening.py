"""Batch 11 source custody and cumulative crosswalk; author-side tests only."""
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"nsejs/physics/curriculum/topics/PH07/b01"
S=json.loads((DIR/"B01_2018_2020_2021_SCREENING.v1.json").read_text(encoding="utf-8"))
C=json.loads((DIR/"B01_CUMULATIVE_SOURCE_TO_LEARNING.v1.json").read_text(encoding="utf-8"))
MAP=json.loads((ROOT/"nsejs/core2/question-map.v1.json").read_text(encoding="utf-8"))["questions"]
BANK=json.loads((ROOT/"nsejs/data/physics-core2-candidates.v1.json").read_text(encoding="utf-8"))["questions"]

def blob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

class Links(HTMLParser):
    def __init__(self,s):
        super().__init__()
        self.links=[]
        self.feed(s)
    def handle_starttag(self,tag,attrs):
        if tag=="a" and "href" in dict(attrs):
            self.links.append(dict(attrs)["href"])

def local_links(file):
    for href in Links(file.read_text(encoding="utf-8")).links:
        p=urlsplit(href)
        if not p.scheme and not p.netloc and p.path:
            assert (file.parent/p.path).resolve().is_file(),(file,href)

def test_session_source_identity_and_custody():
    pins={"question_map":ROOT/"nsejs/core2/question-map.v1.json","candidate_corpus":ROOT/"nsejs/data/physics-core2-candidates.v1.json","adapter_registry":DIR/"B01_ADAPTER_RECONCILIATION.v1.json","previous_supplement":DIR/"B01_PUBLISHER_LOCATOR_SUPPLEMENT.v1.json","earlier_screening":DIR/"B01_EARLIER_PUBLISHER_SCREENING.v1.json","base_coverage":DIR/"B01_CORE2_COVERAGE.v1.json","reverse_routes":DIR/"B01_CORE2_REVERSE_ROUTE_PROPOSAL.v1.json"}
    for k,p in pins.items():
        assert S["source_pins"][k]==C["source_pins"][k]==blob(p)
    observed=S["observations"]
    assert len(observed)==len({x["locator_id"] for x in observed})==11
    assert sum(x["map_binding"] is not None for x in observed)==6
    for x in observed:
        assert x["rights_status"]==x["exact_source_revision_status"]==x["academic_admission"]=="HOLD"
        assert x["source_bytes_sha256"] is None and x["bank_binding"] is None
        assert x["source_band"]=="NOT_QUALIFIED"
        if x["year"]==2018:
            assert x["paper_code"]=="JS511"
        elif x["year"]==2020:
            assert x["exam_date"]=="2021-01-17" and x["paper_code"]=="51"
            assert "404" in x["paper_visual_status"]
        else:
            assert x["exam_date"]=="2022-03-06" and x["paper_code"]=="51"
        subject="P" if x["subject"]=="PHYSICS" else "C"
        claim=f'NSEJS-{x["year"]}-{subject}-Q{x["question_number"]:02d}'
        matches=[m for m in MAP if m["claimed_external_question_id"]==claim]
        if matches:
            m,=matches
            assert x["map_binding"]["question_uid"]==m["question_uid"]
            assert x["map_binding"]["content_revision_sha256"]==m["content_revision_sha256"]
        else:
            assert x["map_binding"] is None
    q9,=[x for x in observed if x["locator_id"]=="NSEJS-2018-JS511-Q9"]
    b,=[x for x in BANK if x["id"]=="NSEJS-2018-P-Q09"]
    assert q9["bank_identity_conflict"][0]["source_id"]==b["source_id"]=="NSEJS-18-MAG-01"
    assert q9["bank_identity_conflict"][0]["status"]=="REJECTED_IDENTITY_BINDING"
    deleted,=[x for x in observed if x["publisher_disposition"]=="DELETED_JS511"]
    assert deleted["locator_id"]=="NSEJS-2018-JS511-Q16" and deleted["publisher_key"]==[]

def test_all_new_transfer_pairs_distinct_and_held():
    observed={x["locator_id"]:x for x in S["observations"]}
    ids=set();tasks=set()
    assert len(S["new_transfers"])==6
    for r in S["new_transfers"]:
        p=json.loads((ROOT/r["proposal"]).read_text(encoding="utf-8"))
        assert p["source"]==observed[r["primary_locator"]]
        assert p["related_source_observations"]==[observed[x] for x in r["related_locators"]]
        assert p["target"]["source_role"]=="AUTHORED_TRANSFER"
        assert p["acceptance"]["release"]=="HOLD"
        pin=p["existing_package_pin"]
        assert pin["blob"]==blob(ROOT/pin["path"])
        t=p["target"];score=sum(v["score"] for v in t["factor_evidence"].values())
        assert score==t["score"] and t["id"]==r["target_id"]
        assert score in (6,7) if t["band"]=="D3" else 8<=score<=10
        for c in p["core1b"]:
            assert c["id"] not in ids and c["task"] not in tasks
            ids.add(c["id"]);tasks.add(c["task"])
            assert c["task"] not in t["decisive_route"]
            assert c["task"]!=p["core1a"]["worked_anchor"]["task"]
            assert c["protected_work"] not in c["stages"]["predict"]
            assert c["boundary_response_criterion"] and c["runtime_verification"]=="NOT_RUN"
        for name in ("core1a","core1b"):
            f=ROOT/r[name]
            assert "ACADEMIC_HOLD" in f.read_text(encoding="utf-8")
            local_links(f)
    assert len(ids)==len(tasks)==12
    for r in S["existing_routes"]:
        assert r["locator_id"] in observed
        assert (ROOT/r["core1a"]).is_file() and (ROOT/r["core1b"]).is_file()

def test_cumulative_source_register_exact_routes_and_counts():
    rows=C["source_inventory"]
    assert len(rows)==len({r["identity"] for r in rows})==27
    assert C["counts"]["publisher_locators"]==26
    assert sum(r["relation"]=="DROPPED_DIAGNOSTIC_ONLY" for r in rows)==2
    assert sum(r["relation"]=="BANK_ONLY_PREREQUISITE_HOLD" for r in rows)==1
    assert sum(r["relation"]=="PRIMARY_BANK_CANDIDATE_AND_PUBLISHER_OBSERVATION" for r in rows)==1
    assert sum(bool(r["source"].get("map_binding") or r["source"].get("question_map_uid")) for r in rows)==13
    assert all(r["exam_admission"]=="HOLD" for r in rows)
    sub=C["subtopic_rows"]
    assert len(sub)==25
    assert {r["subtopic_id"] for r in sub}=={f"PH07-{i:02d}" for i in range(1,13)}|{f"PH08-{i:02d}" for i in range(1,14)}
    assert sum(bool(r["primary_source_identities"]) for r in sub)==14
    assert sum(bool(r["primary_source_identities"] or r["supporting_source_identities"]) for r in sub)==C["counts"]["subtopics_with_primary_or_supporting_observations"]
    assert sum(len(r["supplemental_transfers"]) for r in sub)==14
    for r in rows:
        route=r["learning_route"]
        assert (ROOT/route["core1a"]).is_file() and (ROOT/route["core1b"]).is_file()
        if "proposal" in route:
            p=json.loads((ROOT/route["proposal"]).read_text(encoding="utf-8"))
            assert blob(ROOT/route["proposal"])==route["proposal_blob"]
            assert r["supporting_subtopics"]==p["prerequisite_support"]
            assert route["target_id"]==p["target"]["id"]
    for r in sub:
        sid=r["subtopic_id"]
        assert r["primary_source_identities"]==[x["identity"] for x in rows if x["primary_subtopic"]==sid]
        assert r["supporting_source_identities"]==[x["identity"] for x in rows if sid in x["supporting_subtopics"]]
        assert (ROOT/r["primary_core1a"]).is_file() and (ROOT/r["primary_core1b"]).is_file()
        for t in r["supplemental_transfers"]:
            assert blob(ROOT/t["proposal"])==t["proposal_blob"]
    assert C["counts"]["author_target_nominations"]==89
    assert C["counts"]["provisional_cycles"]==178
    assert C["counts"]["direct_exam_admissions"]==0
    local_links(DIR/"source-to-learning-review.html")

def test_inverse_wave_ratio_and_damped_trace_oracles():
    v=F(96,100)/(F(1,125)-F(1,200))
    assert v==320
    assert v/125==F(64,25) and v/200==F(8,5)
    assert v/250==F(32,25)
    assert F(11,10)/(F(1,150)-F(1,300))==330
    times=[1,6,11,16];amps=[12,9,6,3]
    assert [b-a for a,b in zip(times,times[1:])]==[5,5,5]
    assert [F(a,amps[0])**2 for a in amps]==[1,F(9,16),F(1,4),F(1,16)]
    assert F(4,10)/F(1,2)==F(4,5)

def test_relative_volume_and_cooling_energy_oracles():
    assert 500-F(4999,10)*F(9998,10000)==F(9999,50000)
    assert F(501)-F(500)/F(999,1000)==F(499,999)
    assert 1000-F(9995,10)*F(9999,10000)==F(11999,20000)
    cop=F(6-3)/F(1); leakage=cop*F(3,2)-3
    assert (cop,leakage)==(3,F(3,2))
    assert 3*(2+F(5,2)+leakage)/cop==6
    assert (18-F(3,2))/cop==F(11,2)
    assert F(15-3,5)==F(12,5)

def test_moving_echo_image_order_oracle():
    def arrivals(L,s,v,u):
        images=[-s,2*L-s,s-2*L,s+2*L]
        values=[F(s-x,v-u) if x<s else F(x-s,v+u) for x in images]
        return sorted(values)
    assert arrivals(360,180,330,30)==[1,F(6,5),2,F(12,5)]
    assert arrivals(240,90,320,40)==[F(9,14),F(5,6),F(4,3),F(12,7)]
    assert arrivals(300,150,330,-30)==[F(5,6),1,F(5,3),2]
    assert arrivals(240,90,320,0)==[F(9,16),F(15,16),F(3,2),F(3,2)]

"""Earlier publisher screening: author-side regressions, not independent admission."""
import hashlib
import json
from pathlib import Path
from tools.ph01_source_pin_custody import pinned_json, pinned_blob_sha
from fractions import Fraction as F
from html.parser import HTMLParser
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"nsejs/physics/curriculum/topics/PH07/b01"
LEDGER=json.loads((DIR/"B01_EARLIER_PUBLISHER_SCREENING.v1.json").read_text(encoding="utf-8"))
MAP=json.loads((ROOT/"nsejs/core2/question-map.v1.json").read_text(encoding="utf-8"))["questions"]
BANK=pinned_json(ROOT,{"path":"nsejs/data/physics-core2-candidates.v1.json","git_blob_sha":LEDGER["source_pins"]["candidate_corpus"]})["questions"]

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

def test_earlier_publisher_locator_identity_and_drop():
    pins=LEDGER["source_pins"]
    assert pins["question_map"]==blob(ROOT/"nsejs/core2/question-map.v1.json")
    assert pins["candidate_corpus"]==pinned_blob_sha(ROOT,{"path":"nsejs/data/physics-core2-candidates.v1.json","git_blob_sha":pins["candidate_corpus"]})
    assert pins["adapter_registry"]==blob(DIR/"B01_ADAPTER_RECONCILIATION.v1.json")
    assert pins["previous_supplement"]==blob(DIR/"B01_PUBLISHER_LOCATOR_SUPPLEMENT.v1.json")
    observed=LEDGER["observations"]
    assert len(observed)==len({s["locator_id"] for s in observed})==11
    assert sum(s["map_binding"] is not None for s in observed)==4
    for s in observed:
        assert s["academic_admission"]==s["rights_status"]==s["exact_source_revision_status"]=="HOLD"
        assert s["source_band"]=="NOT_QUALIFIED"
        assert s["source_bytes_sha256"] is None and s["bank_binding"] is None
        assert s["key_visual_status"]=="FINAL_KEY_VISUALLY_INSPECTED"
        claim=f'NSEJS-{s["year"]}-P-Q{s["question_number"]}'
        assert not any(q["id"]==claim for q in BANK)
        matches=[m for m in MAP if m["claimed_external_question_id"]==claim]
        if matches:
            m,=matches
            assert s["map_binding"]["question_uid"]==m["question_uid"]
            assert s["map_binding"]["content_revision_sha256"]==m["content_revision_sha256"]
            assert s["map_binding"]["identity_status"]=="METADATA_MATCH_ONLY_EXACT_CONTENT_HOLD"
        else:
            assert s["map_binding"] is None
        if s["year"]==2022:
            assert "SCREENSHOT_FAILED" in s["paper_visual_status"]
        else:
            assert s["paper_visual_status"]=="PAGE_VISUALLY_INSPECTED"
    drop,=[s for s in observed if s["publisher_disposition"]=="DROPPED_CODE_51"]
    assert drop["locator_id"]=="NSEJS-2022-51-Q48" and drop["publisher_key"]==[]
    assert all(r["primary_locator"]!=drop["locator_id"] for r in LEDGER["new_transfers"])

def test_earlier_supplement_freshness_and_routes():
    observed={s["locator_id"]:s for s in LEDGER["observations"]}
    ids=set(); tasks=set()
    for r in LEDGER["new_transfers"]:
        p=json.loads((ROOT/r["proposal"]).read_text(encoding="utf-8"))
        assert p["source"]==observed[r["primary_locator"]]
        assert p["related_source_observations"]==[observed[x] for x in r["related_locators"]]
        assert p["acceptance"]["release"]=="HOLD"
        pin=p["existing_package_pin"]
        assert pin["blob"]==blob(ROOT/pin["path"])
        t=p["target"]
        assert t["id"]==r["target_id"] and t["cell"]==r["cell"]
        assert t["source_role"]=="AUTHORED_TRANSFER"
        score=sum(f["score"] for f in t["factor_evidence"].values())
        assert score==t["score"]
        assert score in (6,7) if t["band"]=="D3" else 8<=score<=10
        assert len(p["core1b"])==2
        for c in p["core1b"]:
            assert c["id"] not in ids
            ids.add(c["id"])
            assert c["task"] not in tasks
            tasks.add(c["task"])
            assert c["task"] not in t["decisive_route"]
            assert c["task"]!=p["core1a"]["worked_anchor"]["task"]
            assert c["task"]==c["stages"]["attempt"]
            assert c["protected_work"] not in c["stages"]["predict"]
            assert c["boundary_response_criterion"]
            assert c["runtime_verification"]=="NOT_RUN"
        for name in ("core1a","core1b"):
            file=ROOT/r[name]
            raw=file.read_text(encoding="utf-8")
            assert "ACADEMIC_HOLD" in raw
            for href in Links(raw).links:
                parsed=urlsplit(href)
                if not parsed.scheme and not parsed.netloc and parsed.path:
                    assert (file.parent/parsed.path).resolve().is_file(),href
        nav=(ROOT/r["core1a"]).parents[2]/"core1b-chapter.html"
        assert f'source-transfers/{r["primary_locator"]}/core1a.html' in nav.read_text(encoding="utf-8")
    assert len(ids)==len(tasks)==10
    assert len(LEDGER["new_transfers"])==5
    for r in LEDGER["existing_routes"]:
        assert r["locator_id"] in observed
        assert r["selection"]=="RELATED_EXISTING_ROUTE_HOLD"
        assert (ROOT/r["core1a"]).is_file() and (ROOT/r["core1b"]).is_file()
    used={r["primary_locator"] for r in LEDGER["new_transfers"]}|{x for r in LEDGER["new_transfers"] for x in r["related_locators"]}|{r["locator_id"] for r in LEDGER["existing_routes"]}
    assert used==set(observed)

def test_affine_calibration_and_interval_oracle():
    a=F(69-24,42-12); b=24-a*12
    assert (a,b)==(F(3,2),6)
    assert a*32+b==54
    assert ((39-b)/a,(51-b)/a)==(22,30)
    assert F(51-39)/a==8
    assert F(3)/a==2
    assert 2*20+15==55!=58
    assert F(75-35,2)==20

def test_acoustic_temperature_and_delay_oracle():
    def calibrate(l1,l2,t1,t2):
        v=(l2-l1)/(t2-t1)
        return v,t1-l1/v
    a=calibrate(F(24,10),F(48,10),F(12,1000),F(22,1000))
    b=calibrate(F(27,10),F(54,10),F(13,1000),F(23,1000))
    assert a==(240,F(2,1000)) and b==(270,F(3,1000))
    assert a[0]**2/256==b[0]**2/324
    assert a[1]!=b[1]
    assert b[1]+F(81,10)/b[0]==F(33,1000)
    a=calibrate(F(17,10),F(34,10),F(7,1000),F(12,1000))
    b=calibrate(F(2),F(4),F(7,1000),F(12,1000))
    assert a==(340,F(2,1000)) and b==(400,F(2,1000))
    assert a[0]**2/289==b[0]**2/400==400
    assert b[1]+6/b[0]==F(17,1000)
    # Publisher Q35, separate from transfer nomination.
    theta=F(27315,100)*(F(360,332)**2-1)
    assert 47<float(theta)<49

def test_signed_waveform_inverse_oracle():
    a=[3,-2,0,1]; b=[-1,2,-3,1]
    assert [x+y for x,y in zip(a,b)]==[2,0,-3,2]
    r=[0,1,-1,3]
    assert [x-y for x,y in zip(r,a)]==[-3,3,-1,2]
    r=[-2,4,0,1,-3]; a=[1,2,-1,0,-2]
    b=[x-y for x,y in zip(r,a)]
    assert b==[-3,2,1,1,-1]
    assert [x-y for x,y in zip(a,b)]==[4,0,-2,-1,-1]

def test_floating_ice_density_oracle():
    # Initial submerged displacement equals ice mass / initial density.
    def delta_mm(m,rho0,rhof,area,loss=0):
        return 10*((m-loss)/rhof-m/rho0)/area
    assert delta_mm(F(800),F(1),F(1),80)==0
    assert abs(float(delta_mm(F(800),F(1),F(9998,10000),80))-.020004)<1e-6
    assert abs(float(delta_mm(F(500),F(1),F(998,1000),50))-.2004008)<1e-6
    assert delta_mm(F(500),F(1),F(998,1000),50,1)==0

def test_string_air_countermodels():
    assert F(125,250)==F(1,2) and F(350,250)==F(7,5)
    assert F(6,3)**2==4
    # Unequal impedances may defeat the same-pressure-ratio intensity claim.
    assert F(6,3)**2*F(1,4)==1
    q80=next(x for x in LEDGER["observations"] if x["locator_id"]=="NSEJS-2019-51-Q80")
    assert q80["publisher_key"]==["D"]
    assert "perceived loudness" in q80["reasoning_observation"]

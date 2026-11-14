"""Author-side source-locator transfer regression; no exam or QRT admission."""
import hashlib
import json
from pathlib import Path
from tools.ph01_source_pin_custody import pinned_json, pinned_blob_sha
from fractions import Fraction as F
from html.parser import HTMLParser
from urllib.parse import urlsplit
import pytest

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"nsejs/physics/curriculum/topics/PH07/b01"
LEDGER=json.loads((DIR/"B01_PUBLISHER_LOCATOR_SUPPLEMENT.v1.json").read_text(encoding="utf-8"))
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

def test_source_locator_bindings_are_conservative_and_exact():
    pins=LEDGER["source_pins"]
    assert pins["question_map"]==blob(ROOT/"nsejs/core2/question-map.v1.json")
    assert pins["candidate_corpus"]==pinned_blob_sha(ROOT,{"path":"nsejs/data/physics-core2-candidates.v1.json","git_blob_sha":pins["candidate_corpus"]})
    assert pins["adapter_registry"]==blob(DIR/"B01_ADAPTER_RECONCILIATION.v1.json")
    assert len(LEDGER["rows"])==3
    assert LEDGER["existing_related_source_observation"]["publisher_key"]==["C"]
    for row in LEDGER["rows"]:
        s=row["locator"]
        assert s["academic_admission"]==s["rights_status"]==s["exact_source_revision_status"]=="HOLD"
        assert s["source_band"]=="NOT_QUALIFIED" and s["source_bytes_sha256"] is None
        assert s["bank_binding"] is None
        assert not any(q["id"]==f'NSEJS-{s["year"]}-P-Q{s["question_number"]}' for q in BANK)
        claim=f'NSEJS-{s["year"]}-P-Q{s["question_number"]}'
        if s["year"]==2024:
            m,=[m for m in MAP if m["claimed_external_question_id"]==claim]
            assert s["map_binding"]["question_uid"]==m["question_uid"]
            assert s["map_binding"]["content_revision_sha256"]==m["content_revision_sha256"]
            assert s["paper_visual_status"]=="PAGE_VISUALLY_INSPECTED"
        else:
            assert not any(m["claimed_external_question_id"]==claim for m in MAP)
            assert s["map_binding"] is None
            assert s["paper_visual_status"]=="TEXT_RETRIEVED_PAGE_SCREENSHOT_FAILED_502"

def test_fresh_transfer_pairs_and_links():
    ids=set(); tasks=set()
    for row in LEDGER["rows"]:
        p=json.loads((ROOT/row["proposal"]).read_text(encoding="utf-8"))
        assert p["source"]==row["locator"]
        assert p["acceptance"]["release"]=="HOLD"
        pin=p["existing_package_pin"]
        assert pin["blob"]==blob(ROOT/pin["path"])
        t=p["target"]
        score=sum(f["score"] for f in t["factor_evidence"].values())
        assert score==t["score"]
        assert score in (6,7) if t["band"]=="D3" else 8<=score<=10
        assert t["source_role"]=="AUTHORED_TRANSFER"
        assert len(p["core1b"])==2
        for c in p["core1b"]:
            assert c["id"] not in ids
            ids.add(c["id"])
            assert c["task"] not in tasks
            tasks.add(c["task"])
            assert c["task"] not in t["decisive_route"]
            assert c["task"]!=p["core1a"]["worked_anchor"]["task"]
            assert c["protected_work"] not in c["stages"]["predict"]
            assert c["task"]==c["stages"]["attempt"]
            assert c["boundary_response_criterion"]
            assert c["runtime_verification"]=="NOT_RUN"
        for name in ("core1a","core1b"):
            file=ROOT/row[name]; raw=file.read_text(encoding="utf-8")
            assert "ACADEMIC_HOLD" in raw
            for href in Links(raw).links:
                parsed=urlsplit(href)
                if not parsed.scheme and not parsed.netloc and parsed.path:
                    assert (file.parent/parsed.path).resolve().is_file(),href
        nav=(ROOT/row["core1a"]).parents[2]/"core1b-chapter.html"
        assert f'source-transfers/{row["locator"]["locator_id"]}/core1a.html' in nav.read_text(encoding="utf-8")
    assert len(ids)==len(tasks)==6

def test_fixed_voltage_geometry_and_energy_oracle():
    r=F(3,2)/4
    p=180*F(3,4)**2/r
    assert r==F(3,8) and p==270
    assert F(36000,p-30)==150
    assert F(36000,180-30)==240
    r=F(2)/F(3,2)**2
    assert r==F(8,9)
    assert F(24000,160/r-40)==F(1200,7)
    assert F(24000,160*r-40)==F(5400,23)
    assert F(2)/4==F(1,2) # original source geometry, not an admission

def test_joint_heat_loss_model_oracle():
    E=18000
    pa,pb=120,90
    la=pa-F(E,180);lb=pb-E/F(E,70)
    assert la==lb==20
    assert F(E,pa+pb-la)==F(1800,19)
    joint=pa+pb-F(E,100)
    assert joint==30
    assert F(E,190-joint)==F(225,2)
    assert F(1,3)-F(1,4)==F(1,12) # ideal publisher endpoint relation
    assert 150-F(24000,200)==30
    assert 100-F(24000,300)==20 # neither common-single-loss model fits

def test_moving_echo_geometry_and_wavelength_oracle():
    # Solve independently from reception worldline: total path = initial + final wall distance.
    def encounter(d,v,u):
        t=F(2*d,v+u)
        final=d-u*t
        assert v*t==d+final
        assert t>=F(d,v) and final>0
        return t,final
    assert encounter(140,340,20)==(F(7,9),F(1120,9))
    assert encounter(105,315,-15)==(F(7,10),F(231,2))
    assert F(340-20,300)==F(16,15)
    assert F(340+20)/F(16,15)==F(675,2)
    assert F(315-15)/F(315+15,300)==F(3000,11)
    assert encounter(1200,330,30)==(F(20,3),1000)
    assert F(330,550)==F(3,5)
    assert F(330-30,550)==F(6,11)
    assert F(330,550)!=F(330-30,550)
    q59=next(r["locator"] for r in LEDGER["rows"] if r["locator"]["question_number"]==59)
    assert q59["publisher_key"]==["A","B","C","D"]
    assert "adjudicate" in q59["reasoning_observation"]

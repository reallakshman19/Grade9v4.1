"""B01 integration-preparation checks; no independent academic or browser acceptance."""
import hashlib
import json
import re
from fractions import Fraction as F
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import pytest

ROOT=Path(__file__).resolve().parents[1]
TOPICS=ROOT/"nsejs/physics/curriculum/topics"
HEAT=TOPICS/"PH07/b01"
REG=json.loads((HEAT/"B01_ADAPTER_RECONCILIATION.v1.json").read_text(encoding="utf-8"))
COVER=json.loads((HEAT/"B01_CORE2_COVERAGE.v1.json").read_text(encoding="utf-8"))
MAIN=json.loads((HEAT/"B01_MIXED_MAIN_PROPOSAL.v1.json").read_text(encoding="utf-8"))
MATRIX=json.loads((HEAT/"B01_D3D4_CELL_COVERAGE.v1.json").read_text(encoding="utf-8"))
REVERSE=json.loads((HEAT/"B01_CORE2_REVERSE_ROUTE_PROPOSAL.v1.json").read_text(encoding="utf-8"))

def blob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids=[]
        self.hrefs=[]
        self.references=[]
        self.svg_count=0
        self.units=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag=="a" and "href" in a:
            self.hrefs.append(a["href"])
        if tag=="svg":
            self.svg_count+=1
        if tag=="section" and a.get("class")=="unit" and "id" in a:
            self.units.append(a["id"])
        for key in ("aria-labelledby","aria-describedby"):
            if key in a:
                self.references.extend(a[key].split())

def verify_local_links(path):
    page=Page(path.read_text(encoding="utf-8"))
    assert len(page.ids)==len(set(page.ids)),path
    for x in page.references:
        assert x in page.ids,(path,x)
    for href in page.hrefs:
        parsed=urlsplit(href)
        if parsed.scheme or parsed.netloc:
            continue
        if parsed.path:
            target=(path.parent/unquote(parsed.path)).resolve()
            assert target.is_file(),(path,href,target)
        elif parsed.fragment:
            assert parsed.fragment in page.ids,(path,href)
    return page

def original_body(source, sid):
    # Reproduce exactly the documented assembly transforms, preserving all authored
    # prose, figure labels, examples, exit reasoning and source boundaries.
    body=re.search(r"</header>([\s\S]*?)</main>",source).group(1)
    body=re.sub(r"<(/?)h3\b",r"<\1h4",body)
    body=re.sub(r"<(/?)h2\b",r"<\1h3",body)
    body=re.sub(r'href="([^"]+)"',lambda m:m.group(0) if re.match(r"^(https?:|mailto:|#)",m.group(1)) else f'href="{sid}/{m.group(1)}"',body)
    ids=re.findall(r'\bid="([^"]+)"',body)
    for old in dict.fromkeys(ids):
        new=f"{sid}-{old}"
        body=body.replace(f'id="{old}"',f'id="{new}"').replace(f'href="#{old}"',f'href="#{new}"').replace(f'url(#{old})',f'url(#{new})')
    return re.sub(r'(aria-labelledby|aria-describedby)="([^"]+)"',lambda m:f'{m.group(1)}="'+" ".join(f"{sid}-{x}" if x in ids else x for x in m.group(2).split(" "))+'"',body)

@pytest.mark.parametrize("topic,count",[("PH07",12),("PH08",13)])
def test_continuous_chapter_preserves_exact_author_sources(topic,count):
    folder=TOPICS/topic/"b01"
    p=folder/"core1a-chapter.html"
    text=p.read_text(encoding="utf-8")
    source_map=json.loads((folder/"B01_CORE1A_CHAPTER_SOURCES.v1.json").read_text(encoding="utf-8"))
    ids=[f"{topic}-{i:02d}" for i in range(1,count+1)]
    assert source_map["order"]==ids
    assert source_map["academic_status"]=="HOLD"
    page=verify_local_links(p)
    assert page.units==ids
    assert page.svg_count==count
    assert len(re.findall(r"<h4>",text))==3*count
    for pin in source_map["units"]:
        source=ROOT/pin["path"]
        assert blob(source)==pin["blob"]
        assert pin["source_commit"]==source_map["source_commit"]
        assert original_body(source.read_text(encoding="utf-8"),pin["subtopic_id"]) in text
    pathway=folder/"core1b-chapter.html"
    nav=verify_local_links(pathway)
    assert set(f"{sid}/core1b.html" for sid in ids)<=set(nav.hrefs)
    assert set(f"core1a-chapter.html#{sid}" for sid in ids)<=set(nav.hrefs)
    assert "B5 HOLD" in pathway.read_text(encoding="utf-8")
    chapter=(TOPICS/topic/"index.html").read_text(encoding="utf-8")
    assert 'href="b01/core1a-chapter.html"' in chapter
    assert 'href="b01/core1b-chapter.html"' in chapter

def test_complete_cell_review_and_no_inferred_applicability():
    blueprint=ROOT/"templates/physics-blueprint/physics-blueprint.D3-D4.resolved.v0.2.0.json"
    assert blob(blueprint)==MATRIX["blueprint_blob"]==MAIN["blueprint"]["blob"]
    assert blob(HEAT/"B01_ADAPTER_RECONCILIATION.v1.json")==MATRIX["registry_blob"]==MAIN["registry_blob"]
    cells=json.loads(blueprint.read_text(encoding="utf-8"))["cells"]
    assert len(MATRIX["rows"])==25
    positions=[p for r in MATRIX["rows"] for p in r["positions"]]
    assert len(positions)==350
    assert sum(p["status"]=="AUTHORED_TARGET_PROPOSED" for p in positions)==75
    assert sum(p["status"]=="PAUSED" for p in positions)==25
    assert sum(p["status"]=="NO_CANDIDATE_APPLICABILITY_UNASSESSED" for p in positions)==250
    pins={p["subtopics"][0]["id"]:p for p in REG["isolated_slices"]}
    for r in MATRIX["rows"]:
        assert {p["cell"] for p in r["positions"]}==set(cells)
        targets={t["cell"]:t for t in pins[r["subtopic_id"]]["subtopics"][0]["targets"]}
        for p in r["positions"]:
            assert p["operation"]==cells[p["cell"]]["column"]["demand"]
            assert p["target_id"]==(targets[p["cell"]]["id"] if p["cell"] in targets else None)
            assert p["direct_exam_admission"]=="HOLD"
            assert p["independent_qualification"]=="NOT_RUN"

def test_mixed_main_is_proposal_and_all_instances_are_exactly_bound():
    assert MAIN["status"]=="AUTHOR_PROPOSAL_ONLY__INTEGRATION_HOLD"
    groups=MAIN["groups"]
    assert len(groups)==16
    assert sum(g["proposed_mixed_main"] is not None for g in groups)==15
    assert sum(len(g["instances"]) for g in groups)==75
    seen=set()
    prompts=set()
    registry={p["subtopics"][0]["id"]:p for p in REG["isolated_slices"]}
    for g in groups:
        assert g["selected_canonical_main"] is None
        assert g["compatibility_status"]=="NOT_QUALIFIED"
        candidate=g["proposed_mixed_main"]
        if candidate is None:
            assert g["tile_id"]=="PHY-PH07-D3.3"
            assert len(g["instances"])==1 and g["gap"]
        else:
            assert len(set(candidate["mixed_subtopics"]))>=2
            assert set(candidate["mixed_subtopics"])<={i["subtopic_id"] for i in g["instances"]}
            assert set(g["unmixed_instances"])=={i["subtopic_id"] for i in g["instances"]}-set(candidate["mixed_subtopics"])
            assert candidate["first_attempt"] not in prompts
            prompts.add(candidate["first_attempt"])
            assert candidate["protected_work"] not in candidate["predict"]
            score=sum(x["score"] for x in candidate["factor_evidence"].values())
            assert score==candidate["score"]
            assert score in (6,7) if candidate["band"]=="D3" else 8<=score<=10
            assert candidate["academic_status"]=="HOLD"
            assert candidate["runtime_status"]=="NOT_IMPLEMENTED"
        for i in g["instances"]:
            p=registry[i["subtopic_id"]]
            assert i["package_blob"]==p["blob"]==blob(ROOT/i["package_path"])
            assert i["package_version"]==p["version"]
            t,=[t for t in p["subtopics"][0]["targets"] if t["id"]==i["target_id"]]
            assert t["cell"]==g["cell"]
            assert t["identity"]==i["task_identity"]
            assert i["instance_cycle"] in t["cycle_ids"] and "-INSTANCE-" in i["instance_cycle"]
            assert i["prior_main_placeholder"] in t["cycle_ids"] and "-MAIN-" in i["prior_main_placeholder"]
            assert t["id"] not in seen
            seen.add(t["id"])
    assert len(seen)==75

def test_reverse_routes_are_exact_and_not_admitted():
    assert REVERSE["status"]=="SHARED_READER_OWNER_REVIEW_REQUIRED"
    assert REVERSE["no_shared_reader_change"] is True
    assert len(REVERSE["entries"])==2
    assert len(REVERSE["unmatched"])==17
    assert {r["source_id"] for r in REVERSE["entries"]}=={"NSEJS-FND-CIRC-04","NSEJS-24-MECH-07"}
    rows={r["subtopic_id"]:r for r in COVER["rows"]}
    assert REVERSE["source_pins"]==COVER["source_pins"]
    for r in REVERSE["entries"]:
        primary=r["primary"]
        path=ROOT/primary["core1a"]
        link=json.loads((path.parent/"core2-link.v1.json").read_text(encoding="utf-8"))
        assert r["question_uid"]==link["candidate"]["question_uid"]
        assert r["observed_question_revision_sha256"]==link["candidate"]["observed_question_revision_sha256"]
        assert r["observed_stem_sha256"]==link["candidate"]["observed_stem_sha256"]
        assert r["core2_reader"]==link["core2_return"]
        assert r["producer_band"]=="D2"
        assert r["activation"]=="NOT_IMPLEMENTED" and r["admission"]=="HOLD"
        assert rows[primary["subtopic_id"]]["relation"]=="PRIMARY_RELATED_CANDIDATE_HOLD"
        assert len(r["supporting"])==3
        for route in [primary,*r["supporting"]]:
            assert (ROOT/route["core1a"]).is_file()
            assert (ROOT/route["core1b"]).is_file()
            assert r["source_id"] in rows[route["subtopic_id"]]["related_candidate_ids"]
    assert {r["subtopic_id"] for r in REVERSE["unmatched"]}=={r["subtopic_id"] for r in COVER["rows"] if r["relation"]=="NO_MATCH_IN_INSPECTABLE_BANK"}

def test_mixed_heat_model_oracles():
    # Distinguish fixed vs proportional extra loss from slope and independent evidence.
    c=400
    p1,p2=100,180
    n1,n2=c*F(25,1000),c*F(125,1000)
    alpha=(n2-n1)/(p2-p1)
    evaporation=alpha*p1-20-n1
    assert (alpha,evaporation)==(F(1,2),20)
    alpha_prop=alpha/F(8,10)
    assert alpha_prop==F(5,8)
    assert F(8,10)*alpha_prop*100-20==30!=n1
    assert alpha_prop*100*F(2,10)==F(25,2)
    assert (alpha*140-20-evaporation)/c==F(75,1000)
    # Composite calorimeter and phase transition after an engine cycle.
    vessel=F(1200,8)
    reject=30000-9000
    melt=F(5,100)*300000
    total_c=vessel+F(5,100)*4000
    assert (reject*F(8,10)-melt)/total_c==F(36,7)
    assert melt+4*total_c==16400
    assert F(5,100)-reject*F(2,3)/300000==F(1,300)

def test_mixed_wave_model_oracles():
    # Enumerate the phase aliases independently, then compare finite-pulse groups.
    lam=F(6,10); dt=F(4,1000)
    candidates=[(F(2,10)+n*lam)/dt for n in range(-10,11)]
    speeds=[v for v in candidates if 100<=v<=400]
    assert speeds==[200,350]
    ends=[2+2000/v for v in speeds]
    assert ends==[12,F(54,7)]
    assert 1000/speeds[0]-2>=1 and 1000/speeds[1]-2<1
    assert all(abs(float(x)-8.154)>.001 for x in ends)
    # One-way calibration and displaced inverse echo model.
    v=F(3,2)/F(5,1000)
    delay=F(7,1000)-F(3,2)/v
    assert (v,delay)==(300,F(2,1000))
    width=(F(62,1000)-delay)*v/2
    first=(F(22,1000)-delay)*v/2
    assert (width,first)==(9,3)
    predicted=[sorted([delay+2*(a+1)/v,delay+2*(b-1)/v]) for a,b in [(3,6),(6,3)]]
    assert predicted[0]==[F(86,3000),F(106,3000)]
    assert predicted[1]==[F(46,3000),F(146,3000)]
    assert delay+2*(width-first)/v==F(42,1000)

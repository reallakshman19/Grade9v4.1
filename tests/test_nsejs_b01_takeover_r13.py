"""B01 takeover: exact source pins, 39 author routes, 89 scoped INSTANCE tasks.

Static structural tests do NOT establish Physics/QRT or B1-B7 academic qualification.
"""
from __future__ import annotations
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT=Path(__file__).resolve().parents[1]
B01=Path("nsejs/physics/curriculum/topics/PH07/b01")
PH08=Path("nsejs/physics/curriculum/topics/PH08/b01")

def data(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def blob(path):
    b=(ROOT/path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

class Anchors(HTMLParser):
    def __init__(self): super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a": self.links += [dict(attrs).get("href","")]

def test_b01_takeover_pinned_89_instances_and_no_selected_main():
    proposal=data(B01/"B01_INTEGRATED_CURRICULUM_PROPOSAL.v1.json")
    assert proposal["status"]=="AUTHOR_PROPOSAL_ONLY__INTEGRATION_HOLD"
    assert proposal["academic_status"]==proposal["source_admission"]=="HOLD"
    assert proposal["runtime_status"]=="NOT_IMPLEMENTED"
    assert proposal["counts"]=={
        "primary_instances":75,"supplemental_instances":14,"total_instances":89,
        "topic_cell_groups":16,"mixed_main_proposals":16,
        "extension_dependent_new_main":1,"selected_canonical_mains":0,
        "selected_canonical_adapters":0}
    assert len(proposal["groups"])==16 and len(proposal["supplements"])==14
    packages={}
    instance_ids=set()
    target_ids=set()
    main_ids=set()
    for group in proposal["groups"]:
        assert group["qualification"]=="HOLD" and group["canonical_main"] is None
        assert group["prior_mixed_main_proposal"] is None or group["prior_mixed_main_proposal"]["id"]
        for e in group["base_instances"]:
            path=Path(e["package_path"]); assert path.is_file() or (ROOT/path).is_file()
            assert blob(path)==e["package_blob"]
            if path not in packages:
                pkg=data(path)
                assert pkg["version"]==e["package_version"]
                assert pkg["status"]=="DRAFT_AUTHOR_EXPOSED"
                assert pkg["owner_agent"]=="AGENT_2"
                assert pkg["acceptance"]["release"]=="HOLD"
                assert all(g["status"]=="HOLD" for g in pkg["acceptance"]["b1_b7"].values())
                assert len(pkg["core1b"])==6
                packages[path]=pkg
            cycle=next(x for x in packages[path]["core1b"] if x["id"]==e["instance_cycle"])
            assert cycle["kind"]=="INSTANCE" and cycle["qrt_target_id"]==e["target_id"]
            assert cycle["attempt_policy"]["save_first_answer_before_hint"]
            assert cycle["runtime_verification"]=="NOT_RUN"
            assert cycle["id"] not in instance_ids
            instance_ids.add(cycle["id"])
            target_ids.add(e["target_id"])
            main_ids.add(e["prior_main_placeholder"])
        for e in group["supplemental_instances"]:
            assert e["selection"]=="AUTHOR_PROPOSED_NOT_CANONICAL"
    assert len(packages)==25 and len(instance_ids)==len(target_ids)==len(main_ids)==75
    for sup in proposal["supplements"]:
        path=Path(sup["proposal_path"])
        assert blob(path)==sup["proposal_blob"]
        pkg=data(path)
        assert pkg["status"]=="AUTHOR_EXPOSED_NOT_INDEPENDENTLY_QUALIFIED"
        assert pkg["existing_package_pin"]["blob"]==sup["base_package_blob"]
        assert pkg["existing_package_pin"]["version"]==sup["base_package_version"]
        assert pkg["acceptance"]["release"]=="HOLD"
        assert pkg["acceptance"]["canonical_integration"]=="NOT_SELECTED"
        assert pkg["target"]["id"]==sup["target_id"]
        selected=[c for c in pkg["core1b"] if c["id"]==sup["instance_cycle"]]
        assert len(selected)==1 and selected[0]["kind"]=="INSTANCE"
        assert sup["instance_cycle"] not in instance_ids
        instance_ids.add(sup["instance_cycle"])
    assert len(instance_ids)==89
    queue=data(B01/"B01_R01_REVIEW_QUEUE.v1.json")
    assert len(queue["targets"])==89 and len(queue["mixed_mains"])==16
    assert {x["target_id"] for x in queue["targets"]}==target_ids|{e["target_id"] for e in proposal["supplements"]}
    assert queue["all_gates"]=="HOLD"

def test_b01_takeover_all_39_author_pairs_exist_and_linked():
    p=data(B01/"B01_INTEGRATED_CURRICULUM_PROPOSAL.v1.json")
    pages=[]
    for entry in p["groups"]:
        for task in entry["base_instances"]:
            root=Path(task["package_path"]).parent
            pages += [root/"core1a.html",root/"core1b.html"]
    # Deduplicate three operations per primary subtopic.
    pages=sorted(set(pages))
    assert len(pages)==50
    for s in p["supplements"]:
        pages.extend([Path(s["core1a"]),Path(s["core1b"])])
    assert len(pages)==78 and all((ROOT/path).is_file() for path in pages)
    index=ROOT/B01/"integrated-curriculum-review.html"
    preview=ROOT/B01/"learner-preview/index.html"
    assert preview.is_file()
    text=index.read_text()
    assert "learner-preview/index.html" in text
    links=Anchors();links.feed(text)
    for path in pages:
        relative=path.as_posix()
        assert any(relative.endswith(urlsplit(x).path.rsplit("nsejs/",1)[-1]) and "nsejs/" in x
                   for x in links.links),relative

def test_b01_takeover_rejected_paper_binding_is_not_effective_metadata():
    overlay=data(B01/"B01_SOURCE_REVIEW_OVERLAY.v1.json")
    source=data(B01/"B01_CUMULATIVE_SOURCE_TO_LEARNING.v2.json")
    assert len(overlay["identity_review_queue"])==2
    assert {x["locator"] for x in overlay["identity_review_queue"]}=={
        "NSEJS-2018-JS511-Q9","NSEJS-2017-JS534-Q1"}
    assert source["counts"]["publisher_locators"]==31
    assert source["counts"]["metadata_bindings"]==12
    assert source["counts"]["subtopics_with_primary_or_supporting_observations"]==24
    assert source["counts"]["subtopics_without_any_source_observation"]==1
    assert source["counts"]["direct_exam_admissions"]==0
    review={x["identity"]:x for x in source["source_inventory"]}
    for x in overlay["identity_review_queue"]:
        assert review[x["locator"]]["effective_map_binding"] is None
    gap=next(x for x in source["subtopic_rows"] if x["subtopic_id"]=="PH08-09")
    assert not gap["primary_source_identities"] and not gap["supporting_source_identities"]

def test_b01_takeover_runtime_boundaries_are_explicit():
    root=ROOT/B01/"learner-preview"
    html=(root/"index.html").read_text()
    js=(root/"runtime.js").read_text()
    assert 'src="./runtime.js"' in html and "<iframe" not in html
    for name in ("h1","h2","h3","save-first","reveal","save-diagnosis","save-repair","save-boundary","show-boundary"):
        assert 'id="'+name+'"' in html
    for term in ("crypto.subtle.digest('SHA-1'","crypto.subtle.digest('SHA-256'",
                 "content_revision","first_answer","RECONSTRUCT","BOUNDARY_MODEL",
                 "localStorage.setItem","NON_EXISTENT_TOKEN_SHOULD_NOT_APPEAR"):
        if term.startswith("NON_EXISTENT"):
            assert term not in js
        else:
            assert term in js or (term=="crypto.subtle.digest('SHA-1'" and "hash('SHA-1'" in js) or (term=="crypto.subtle.digest('SHA-256'" and "hash(revisionMaterial,'SHA-256')" in js)
    assert "No verified hint taxonomy" in html
    assert "not secure or tamper-proof" in html
    assert "automatic grading" in js

from __future__ import annotations
import importlib.util
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from search_learner_pages import build_public_learner_documents,public_pages
from build_search_index import normalize_text

def test_complete_current_registries_and_public_pages():
    docs,pages=build_public_learner_documents(ROOT,normalize_text)
    urls={d["url"] for d in docs}
    assert len(urls)==len(docs)
    assert set(d["subject"] for d in docs)>={"Physics","Chemistry","Biology"}
    assert all((ROOT/urlsplit(u).path).is_file() for u in urls)
    physics=json.loads((ROOT/"nsejs/physics/learn/catalog.json").read_text())
    assert sum(d["id"].startswith("ROUTE-PH0") and d["category"]=="curriculum" for d in docs)>=9
    for chapter in physics["chapters"]:
        for unit in chapter["units"]:
            for role in ("learn","practice"):
                assert "nsejs/physics/"+unit[role] in urls
    chem=json.loads((ROOT/"nsejs/chemistry/learner-navigation.v1.json").read_text())
    for unit in chem["units"]:
        for sub in unit["subtopics"]:
            for mode in ("study","practice"):
                assert any(d["original_id"]==sub["id"]+"-"+mode for d in docs)
    grav=json.loads((ROOT/"nsejs/physics/ph05/source-led-r2/packages.v1.json").read_text())
    for p in grav["packages"]:
        for task in p["tasks"]:
            assert any(d["original_id"]==task["uid"] and d["category"]=="question" for d in docs)
    covered={urlsplit(u).path for u in urls}
    assert set(pages)<=covered|{"nsejs/physics/ph05/source-checkpoint.html"}
    assert len(pages)==len(set(pages))
    assert all(not any(x in p.split("/") for x in ("agent1","review","evidence","archive")) for p in pages)

def test_committed_index_no_protected_payloads():
    docs=json.loads((ROOT/"data/learner-search-index.v1.json").read_text())
    assert len({d["id"] for d in docs})==len(docs)
    assert len({d["url"] for d in docs})==len(docs)
    assert all((ROOT/urlsplit(d["url"]).path).is_file() for d in docs)
    assert all(d.get("hints",[])==[] for d in docs if d["category"]=="question")
    banned={"answer","steps","reconstruction","alternative","boundaryModel","repair","diagnosis","official_option","key"}
    assert all(not banned.intersection(d) for d in docs)
    assert any(d["original_id"]=="AUTHORED-PH05-R2-P06-A" for d in docs)
    assert any(d["original_id"]=="CHEM-C14.01-study" for d in docs)
    assert any(d["subject"]=="Biology" and d["category"]=="tablet" for d in docs)
    source=next(d for d in docs if d["original_id"]=="NSEJS-2019-C51-Q61")
    assert "equal gravitational forces" not in source["search_text"]
    bohr=next(d for d in docs if d["original_id"]=="CHEM-NSEJS-ATOM-01")
    assert "option b is confirmed" not in bohr["search_text"]
    assert "27/32" not in bohr["search_text"]
    assert parse_qs(urlsplit(bohr["url"]).query)["q"]==["CHEM-NSEJS-ATOM-01"]

def test_shared_search_default_and_publish_rebuild():
    runtime=(ROOT/"js/site-search.js").read_text()
    assert "let currentScope = 'nsejs'" in runtime
    assert "Search NSEJS Junior Science" in runtime
    assert "new URL(\"../\", script.src).href" in runtime
    assert "appendBankBridges" in runtime
    # R3 separates deterministic search preparation from signed publication.
    assert "build_search_index.py --install-search" in (ROOT/".github/workflows/nsejs-search-r1.yml").read_text()
    deploy=(ROOT/".github/workflows/deploy.yaml").read_text()
    assert "production-control-r3/release.py" in deploy
    assert "build_search_index.py --install-search" not in deploy
    assert "workflow_dispatch:" in deploy and "path: public" in deploy


def test_physics_r2_candidate_study_transfer_and_source_status_are_indexed_without_keys():
    from urllib.parse import urlencode
    docs,pages=build_public_learner_documents(ROOT,normalize_text)
    direct={d["original_id"]:d for d in docs}
    committed=json.loads((ROOT/"data/learner-search-index.v1.json").read_text())
    by_id={d["original_id"]:d for d in committed}
    catalog=json.loads((ROOT/"nsejs/physics/learn/catalog.json").read_text())
    tasks=json.loads((ROOT/"nsejs/physics/quality-r1/attempt-prompts.v2.json").read_text())
    assert tasks["status"]=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"
    assert len(tasks["units"])==4
    for task in tasks["units"]:
        uid=task["unit"]
        ch=task["chapter"]
        expected={
            "QUALITY-"+uid+"-CORE1A":"nsejs/physics/quality-r1/study.html?unit="+uid,
            task["uid"]:"nsejs/physics/quality-r1/challenge.html?unit="+uid,
        }
        for identity,url in expected.items():
            assert identity in direct and identity in by_id,identity
            for item in (direct[identity],by_id[identity]):
                assert item["url"]==url
                assert item["subject"]=="Physics" and item["is_nsejs"] is True
                assert item["category"]=="tablet"
                assert "HOLD" in item["badge"]
                assert "source" not in item or item["source"] is None
                assert not any(k in item for k in ("answer","solution","reconstruction","boundaryModel","repair","diagnosis","hints"))
                assert (ROOT/urlsplit(item["url"]).path).is_file()
        source_id="QUALITY-"+ch+"-SOURCE-STATUS"
        assert source_id in direct and source_id in by_id
        assert by_id[source_id]["url"]=="nsejs/physics/quality-r1/source.html?ph="+ch
        assert "NO ORIGINAL EXAM ADMISSION" in by_id[source_id]["badge"]
    assert sum(x["original_id"].startswith("QUALITY-") and
               "quality-r1/" in x["url"] for x in committed)==8
    # All four transfer UIDs are discoverable, without exposing first-attempt
    # solutions or presenting these as accepted original examinations.
    for task in tasks["units"]:
        hit=by_id[task["uid"]]
        assert task["uid"].lower() in hit["search_text"]
        assert hit["type"]=="LESSON"
    assert not any(d["url"] in {
        "nsejs/physics/quality-r1/study.html",
        "nsejs/physics/quality-r1/challenge.html",
        "nsejs/physics/quality-r1/source.html"} for d in committed)
    assert (ROOT/"data/learner-search-index.v1.json").read_bytes()==(
        ROOT/"nsejs/data/learner-search-index.v1.json").read_bytes()


def test_26_new_search_records_match_deterministic_generator_exactly():
    # Earlier static search snapshots lagged new PH03/PH06/PH11/PH12 and
    # Chemistry custody pages. Avoid merely counting 26 entries that differ
    # in content from what the release's deterministic generator produces.
    import hashlib
    actual=json.loads((ROOT/"data/learner-search-index.v1.json").read_text())
    actual_by_url={x["url"]:x for x in actual}
    dynamic,_=build_public_learner_documents(ROOT,normalize_text)
    special=[]
    for x in dynamic:
        if x["url"].startswith("nsejs/physics/quality-r1/"):
            special.append(x)
        elif x["url"] in {
            "nsejs/chemistry/core2-custody.html",
            "nsejs/physics/core1/PH03/P03/index.html",
            "nsejs/physics/core1/PH06/U08/index.html",
            "nsejs/physics/curriculum/topics/PH11/subtopics/PH11-07/core1a.html",
            "nsejs/physics/curriculum/topics/PH11/subtopics/PH11-07/core1b.html",
            "nsejs/physics/curriculum/topics/PH12/subtopics/PH12-09/core1a.html",
            "nsejs/physics/curriculum/topics/PH12/subtopics/PH12-09/core1b.html",
            "nsejs/physics/ph03/source-led-r1/index.html",
            "nsejs/physics/ph03/source-led-r2/index.html",
            "nsejs/physics/ph06/source-checkpoint.html",
            "nsejs/physics/textbook/PH03/P03/index.html",
            "nsejs/physics/textbook/PH06/U06/index.html",
            "nsejs/physics/textbook/PH06/U08/index.html",
            "nsejs/physics/textbook/PH06/index.html",
        }:
            special.append(x)
    assert len(special)==26
    for generated in special:
        item=generated.copy()
        if item["category"]!="question":
            item["search_text"]=normalize_text(
                " ".join(str(item.get(k,"")) for k in
                         ("id","title","subject","topic","badge","breadcrumb","url"))
                +(" nsejs junior science" if item.get("is_nsejs") else ""))
            if item.get("is_nsejs") and "HOLD" not in item["badge"]:
                item["badge"]="LEARNING CANDIDATE · HOLD"
        got=actual_by_url.get(item["url"])
        assert got==item, (item["url"], {k:(got.get(k) if got else None,v)
                 for k,v in item.items() if not got or got.get(k)!=v})
    # The immutable committed search snapshot has 1012 entries. The exact
    # preview rebuild adds the two newly discoverable question-bank routes.
    bank_ids={"CHEMISTRY-QUESTION-BANK","BIOLOGY-QUESTION-BANK"}
    found={d["original_id"] for d in actual if d["original_id"] in bank_ids}
    assert found in (set(),bank_ids), "Incomplete new bank search coverage"
    expected=1012+len(found)
    assert len(actual)==expected and len({d["url"] for d in actual})==expected
    if found:
        for subject,slug in (("CHEMISTRY","atomic_structure"),("BIOLOGY","living_world")):
            bank=next(x for x in actual if x["original_id"]==subject+"-QUESTION-BANK")
            assert bank["url"].endswith("index.html?topic="+slug+"#topicWorkspace")
            assert "HOLD" in bank["badge"] and bank["category"]=="page"
            assert not any(k in bank for k in ("answer","options","hints","steps","reconstruction"))
    assert (ROOT/"data/learner-search-index.v1.json").read_bytes()==(
        ROOT/"nsejs/data/learner-search-index.v1.json").read_bytes()
    manifest=json.loads((ROOT/"data/learner-search-manifest.v1.json").read_text())
    payload=(ROOT/"data/learner-search-index.v1.json").read_bytes()
    assert manifest["sha256"]==hashlib.sha256(payload).hexdigest()
    assert manifest["total_documents"]==expected
    assert manifest["public_html_pages"]==372

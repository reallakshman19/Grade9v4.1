"""Chemistry C01–C14 learner navigation structural checks.

These prove destinations, preserved authored content and truthful labelling,
not independent academic review or authentic original NSEJS paper admission.
"""
from __future__ import annotations
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse, unquote

ROOT=Path(__file__).resolve().parents[1]
HUB=ROOT/"nsejs/chemistry/index.html"
NAV=ROOT/"nsejs/chemistry/learner-navigation.v1.json"
NATIVE=ROOT/"nsejs/chemistry/textbook/index.html"
PREVIEW=ROOT/"curriculum/chemistry/preview"
MAP=ROOT/"nsejs/core2/question-map.html"

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):self.ids.add(a["id"])
        if tag=="a" and a.get("href"):self.links.append(a["href"])

def read(path:Path)->str:return path.read_text(encoding="utf-8")
def registry():return json.loads(read(NAV))
def syllabus():return json.loads(read(ROOT/"curriculum/chemistry/syllabus/chemistry-syllabus.v1.json"))


def test_all_14_chapters_and_84_subtopics_have_one_canonical_primary_spine():
    nav=registry();s=syllabus()
    assert nav["schema"]=="g9v41-chemistry-learner-navigation/v1"
    assert len(nav["units"])==len(s["units"])==14
    assert sum(len(u["subtopics"]) for u in nav["units"])==84
    assert [u["id"] for u in nav["units"]]==[u["id"] for u in s["units"]]
    for item,source in zip(nav["units"],s["units"],strict=True):
        assert item["title"]==source["title"]
        assert [q["id"] for q in item["subtopics"]]==[q["id"] for q in source["subtopics"]]
        assert all(q["title"]==r["title"] for q,r in zip(item["subtopics"],source["subtopics"],strict=True))
        assert item["reader"]==("preview" if int(item["id"][1:])<=7 else "native")
        if item["reader"]=="preview":
            path=ROOT/"curriculum/chemistry/preview"/(item["id"]+".html")
        else:path=NATIVE
        assert path.is_file(),str(path)
        assert 'learner-navigation.js' in read(path)
    assert nav["rules"]["recovery_contextual_only"]
    assert nav["status"]=="AUTHORED_LEARNING_PATHS__NOT_EXAM_SOURCE_ADMISSION"


def test_home_page_has_fourteen_direct_chapter_cards_and_subtopic_routes():
    s=read(HUB);parsed=LinkParser();parsed.feed(s)
    reg=registry()
    assert "chem-chapters" in parsed.ids
    assert "Chemistry textbook · 14 chapters" in s
    assert "119" in s and "87-row identity map" in s
    assert "Peer-Audited Curriculum" not in s
    assert "Core 2: Reviewed" not in s
    assert "javascript:void(0)" not in s
    assert 'aria-label="Chemistry question bank category filters"' in s
    for unit in reg["units"]:
        assert "chem-card-"+unit["id"] in parsed.ids
        assert ('../../curriculum/chemistry/preview/'+unit["id"]+'.html' in parsed.links
                if unit["reader"]=="preview" else
                'textbook/index.html?unit='+unit["id"]+'&mode=study' in parsed.links)
        for sub in unit["subtopics"]:
            assert any(unquote(sub["id"]) in unquote(h) for h in parsed.links
                       if h.startswith("../../curriculum/chemistry/preview/") or h.startswith("textbook/index.html?"))
    assert len([x for x in parsed.ids if re.fullmatch(r"chem-card-C\d{2}",x)])==14


def test_both_readers_expose_same_journey_without_copying_attempts():
    preview=read(PREVIEW/"reader.js");native=read(ROOT/"nsejs/chemistry/textbook/reader.js")
    shared=read(ROOT/"nsejs/chemistry/learner-navigation.js")
    assert "window.ChemLearnerNav.mountPreview" in preview
    assert "window.ChemLearnerNav.mountNative" in native
    assert "Chemistry lesson steps and next subtopic" in shared
    assert "1 · Learn" in shared and "2 · Try it" in shared and "3 · Exam practice" in shared
    assert "Need more help?" in shared
    assert "Previous · " in shared and "Next · " in shared
    assert "Chapter list" in shared
    assert "return" in shared and "question-map.html" in shared
    assert 'mode==="practice"' in preview
    assert 'wrap.id="practice-"+safeId(subId)' in preview
    assert "const key=\"g9chem-first-attempt:\"" in preview
    assert "field.disabled=true" in preview
    assert "post.hidden=true" in preview
    assert "if(!ok){" in preview and "Nothing is unlocked" in preview
    assert "hints.forEach(hint=>{hint.hidden=false})" in preview
    assert 'revisionKey("attempt",task)' in native
    assert "updateUrl(push);updateSourceReturn();" in native


def test_contextual_help_and_safe_question_map_return():
    nav=registry()
    assert sum(len(u["help"]) for u in nav["units"])==7
    for unit in nav["units"]:
        for entry in unit["help"]:
            assert entry["href"].startswith("core1/")
            assert (ROOT/"nsejs/chemistry"/entry["href"]).is_file(),entry["href"]
    s=read(MAP)
    assert 'id="chemistry"' in s
    assert 'id="chemistry-lesson-return"' in s
    assert "target.origin!==location.origin" in s
    assert 'target.pathname===native' in s
    assert "Return to my Chemistry lesson" in s


def test_school_chemistry_page_no_longer_claims_all_chapters_missing():
    s=read(ROOT/"chemistry/index.html")
    assert "The first Chemistry chapter is being planned" not in s
    assert "Chemistry chapters: coming soon" not in s
    assert '../nsejs/chemistry/index.html#chem-chapters' in s
    assert "School Chemistry — separate track" in s

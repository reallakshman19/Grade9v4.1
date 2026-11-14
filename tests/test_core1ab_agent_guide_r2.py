"""Guide R2 integration checks. Static navigation, full authoring chapters, scoped policy.

This verifies current HTML and actual repository link targets. It is NOT an
independent teaching or academic quality decision, nor a rendered browser test.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GUIDE=ROOT/"architecture/core1ab-agent-guide.html"
POLICY=ROOT/"docs/agent-entry/quality-gate-r2/quality-policy.v1.json"
R2=ROOT/"docs/agent-entry/quality-gate-r2"

LEGACY_IDS=[
    "start","workflow","intake","scope","research","coverage","sl1sl2",
    "solve","operations","difficulty","blueprint","adapter","warrants",
    "core1a","visuals","freshness","journey","main","diagnosis","worked",
    "binder","implementation","qa","review","batch","templates","done",
    "references",
]


class GuideParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]
        self.links=[]
        self.r2=False
        self.r2_links=[]
        self.open_sections=0
        self.bad_sections=0
        self.nav=[]
        self.in_navigation=False

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="section" and a.get("class")=="field-section":
            self.open_sections+=1
            if self.open_sections>1:self.bad_sections+=1
            if "id" in a:self.ids.append(a["id"])
            if a.get("id")=="evidence-gate-r2":
                self.r2=True
                assert a.get("data-contract")=="quality-gate-r2"
        if tag=="nav" and a.get("class")=="field-nav":
            self.in_navigation=True
        if tag=="a" and a.get("href"):
            href=a["href"]
            self.links.append(href)
            if self.r2:self.r2_links.append(href)
            if self.in_navigation:self.nav.append(href)

    def handle_endtag(self,tag):
        if tag=="section":
            if self.r2:self.r2=False
            self.open_sections=max(0,self.open_sections-1)
        if tag=="nav":self.in_navigation=False


def read():
    text=GUIDE.read_text(encoding="utf-8")
    p=GuideParser()
    p.feed(text)
    return text,p


def test_all_legacy_chapters_remain_and_r2_is_an_early_chapter():
    text,p=read()
    assert p.bad_sections==0
    assert len(p.ids)==29
    assert len(set(p.ids))==29
    assert [x for x in p.ids if x!="evidence-gate-r2"]==LEGACY_IDS
    assert p.ids.index("evidence-gate-r2")==1
    assert p.nav[1]=="#evidence-gate-r2"
    assert all("#"+section in p.nav for section in p.ids)


def test_all_r2_links_are_real_files_on_this_stacked_branch():
    _,p=read()
    assert len(p.r2_links)>=9
    for href in p.r2_links:
        if href.startswith("#"):continue
        assert not href.startswith("http"),"Use repo-local, versioned R2 guide links"
        target=(GUIDE.parent/href).resolve()
        assert target.is_relative_to(ROOT)
        assert target.is_file(),f"R2 link broken: {href}"


def test_science_teaching_transfer_and_eight_negative_controls_are_visible():
    text,_=read()
    section=text.split('id="evidence-gate-r2" data-contract="quality-gate-r2"')[1].split("</section>")[0]
    assert "Physics R2" in section
    assert "Core1A" in section and "Core1B" in section and "Core2" in section
    for name in (
        "WRONG_DIMENSION","WRONG_SIGN_OR_LIMIT","NUMERIC_CLONE","HINT_LEAK",
        "BAD_SOURCE_FIGURE","SAVE_FAILURE","STALE_REVISION","FALSE_REVIEW_BADGE",
    ):
        assert name in section
    for role in ("R00","R01","B1–B7","SHA-256","PILOT_NOT_ENFORCED"):
        assert role in section
    assert "per-question" in section or "routine question" in section


def test_quality_policy_is_pilot_and_owner_golden_once_not_auto_promotion():
    p=json.loads(POLICY.read_text(encoding="utf-8"))
    assert p["activation"]=="PILOT_AWAITING_OWNER_GOLDEN"
    assert p["production_enabled"] is False
    assert p["owner_accepted_golden_head"] is None
    assert p["reviewer_controls"]["owner_per_item"] is False
    assert p["reviewer_controls"]["owner_golden_once"] is True
    guide=GUIDE.read_text(encoding="utf-8")
    assert "one complete Golden exemplar" in guide
    assert "not separately for every routine question" in guide
    assert "This branch contains the guide integration" in (R2/"README.md").read_text(encoding="utf-8")


def test_existing_core1a_and_core1b_method_is_not_replaced_with_checklist():
    text,_=read()
    for phrase in (
        "Core1A: write a real textbook, not a task bank",
        "Core1B: engineer a genuinely fresh task",
        "The six-stage Core1B learning journey",
        "Build the disciplinary claim and warrant register",
        "seven operations",
        "H1 CLARIFY",
        "H2 CORRELATE",
        "H3 OPEN_THE_WAY",
        "not when a page looks polished",
    ):
        assert phrase.lower() in text.lower()

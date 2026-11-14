"""Architecture R3: the audit guide is reviewer-facing; the eight-stage pipeline is Core2-led.

Static/structural tests verify paths, authority labels, cross-links and legacy
URL preservation. They do NOT certify Physics correctness or real browser UX.
"""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ARCH=ROOT/"architecture"
AUDIT=ARCH/"review-guide.html"
PIPE=ARCH/"core2-source-to-learning-pipeline.html"
LEGACY=ARCH/"pipeline-flowchart.html"
POLICY=ROOT/"docs/agent-entry/quality-gate-r2/quality-policy.v1.json"
NAV=[ROOT/"index.html",ARCH/"index.html",ROOT/"nsejs/index.html",
     ARCH/"guidebook.html",ARCH/"core1ab-agent-guide.html"]


class HTMLScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[]
        self.links=[]
        self.titles=[]
        self.h1=[]
        self.heading=None
        self.meta=[]
        self.main_count=0

    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):self.ids.append(a["id"])
        if tag=="a" and a.get("href"):self.links.append(a["href"])
        if tag=="main":self.main_count+=1
        if tag=="meta":self.meta.append(a)
        if tag in ("title","h1"):self.heading=tag

    def handle_endtag(self,tag):
        if tag==self.heading:self.heading=None

    def handle_data(self,text):
        if self.heading=="title":self.titles.append(text)
        if self.heading=="h1":self.h1.append(text)


def scan(path):
    s=path.read_text(encoding="utf-8")
    obj=HTMLScan()
    obj.feed(s)
    return s,obj


def test_reviewer_guide_has_exactly_fourteen_audit_sections_and_independent_roles():
    source,o=scan(AUDIT)
    expected=["scope","roles","intake","science","core1a","core1b","core2",
              "qrt","runtime","coverage","findings","receipt","golden","references"]
    assert o.main_count==1
    assert "Independent Audit Field Guide" in " ".join(o.titles)
    assert "Independent Audit Field Guide" in " ".join(o.h1)
    assert len(set(expected))==14
    assert all(o.ids.count(x)==1 for x in expected)
    assert all("#"+x in o.links for x in expected)
    assert "R00" in source and "R01" in source
    assert "author-exposed" not in " ".join(o.h1).lower()
    assert "NOT_OBSERVED" in source
    assert "HOLD_BLOCKER" in source and "REQUEST_CHANGES" in source
    assert "TECHNICAL_PASS_PENDING_ACADEMIC" in source


def test_auditor_content_quality_and_first_attempt_fail_closed_are_explicit():
    s,_=scan(AUDIT)
    for required in [
       "A1–A3", "A4–A5", "A6–A7", "A8–A9",
       "B1 Target", "B2 Construction", "B3 Core1A", "B4 Core1B",
       "B5 Protection", "B6 Repair/Boundary", "B7 Physics/Provenance",
       "Core2", "H1/H2/H3", "immutable", "counterexample", "1000×1600",
       "1600×1000", "WRONG_DIMENSION", "WRONG_SIGN_OR_LIMIT", "NUMERIC_CLONE",
       "HINT_LEAK", "BAD_SOURCE_FIGURE", "SAVE_FAILURE",
       "STALE_REVISION", "FALSE_REVIEW_BADGE",
       "EVIDENCE_STRUCTURALLY_GROUNDED",
    ]:
        assert required in s,required
    assert "first answer" in s and "new linked revision" in s
    assert "Owner approves" in s and "Golden" in s
    assert "not required to approve each" in s or "Not required to approve each" in s


def test_audit_links_are_to_real_versioned_files():
    s,o=scan(AUDIT)
    assert "<iframe" not in s.lower()
    for href in o.links:
        if href.startswith(("#","http:","https:","mailto:")):continue
        path=(AUDIT.parent/href.split("#")[0].split("?")[0]).resolve()
        assert path.is_relative_to(ROOT),href
        assert path.is_file(),f"Broken auditor link: {href}"
    assert "core2-source-to-learning-pipeline.html" in o.links
    assert "core1ab-agent-guide.html" in o.links


def test_pipeline_is_clearly_core2_led_with_eight_original_stage_anchors():
    s,o=scan(PIPE)
    assert o.main_count==1
    assert "Core2-Led Source-to-Learning Pipeline" in " ".join(o.h1)
    assert "Core2-Led Source-to-Learning Pipeline" in " ".join(o.titles)
    assert all(o.ids.count("stage-"+str(i))==1 for i in range(1,9))
    assert "curriculum-first Core1A" in s
    assert "Owner approves" in s or "Owner approves" in s.replace("&amp;","&")
    assert "PILOT_AWAITING_OWNER_GOLDEN" in s
    assert "Independent Audit Field Guide" in s
    assert "1000×1600" in s and "1600×1000" in s
    assert "All questions strictly labeled" not in s
    assert "Source Rights Clearance" not in s
    assert "owner-registry.json" not in s
    assert "scripts/verify_playwright_template.js" not in s


def test_pipeline_source_reference_links_exist():
    _,o=scan(PIPE)
    for href in o.links:
        if href.startswith(("#","http:","https:","mailto:")):continue
        file=(PIPE.parent/href.split("#")[0].split("?")[0]).resolve()
        assert file.is_relative_to(ROOT),href
        assert file.is_file(),f"Broken Core2 pipeline link: {href}"


def test_old_pipeline_url_preserves_stage_hash_and_accessible_fallback():
    s,o=scan(LEGACY)
    assert len(o.meta)>0
    assert any(m.get("http-equiv")=="refresh" and
               "core2-source-to-learning-pipeline.html" in m.get("content","")
               for m in o.meta)
    assert 'window.location.search + window.location.hash' in s
    assert "core2-source-to-learning-pipeline.html" in o.links
    assert "review-guide.html" in o.links
    assert "core1ab-agent-guide.html" in o.links
    assert o.main_count==1


def test_all_primary_navigation_links_to_new_pipeline_and_not_old():
    for path in NAV:
        s,o=scan(path)
        assert "pipeline-flowchart.html" not in s,str(path)
        assert any("core2-source-to-learning-pipeline.html" in link for link in o.links),path


def test_policy_remains_explicit_pilot_and_owner_golden_once():
    policy=json.loads(POLICY.read_text(encoding="utf-8"))
    assert policy["activation"]=="PILOT_AWAITING_OWNER_GOLDEN"
    assert policy["production_enabled"] is False
    assert policy["owner_accepted_golden_head"] is None
    assert policy["reviewer_controls"]["owner_per_item"] is False
    assert policy["reviewer_controls"]["owner_golden_once"] is True
    s,_=scan(AUDIT)
    assert "production_enabled=false" in s
    assert "20%" in s
    assert "not required to approve each" in s.lower()

"""Learner-first NSEJS Physics route inventory and non-destructive navigation R1."""
from __future__ import annotations
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
PH = ROOT / "nsejs/physics"
CAT = json.loads((PH/"learn/catalog.json").read_text(encoding="utf-8"))

class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            data = dict(attrs)
            if "href" in data:
                self.links.append(data["href"])

def test_chapter_catalog_is_real_and_single_entry():
    assert CAT["schema"] == "g9v41-physics-learner-catalog/v1"
    assert CAT["candidate_only"] is True
    chapters = CAT["chapters"]
    assert [x["id"] for x in chapters] == [f"PH{i:02d}" for i in range(1,13)]
    assert Counter(c["state"] for c in chapters) == {
        "learning-pairs":6,"unavailable":4,"chapter-preview":2}
    assert {c["id"]:len(c["units"]) for c in chapters} == {
        "PH01":8,"PH02":8,"PH03":0,"PH04":0,"PH05":0,"PH06":0,
        "PH07":12,"PH08":13,"PH09":12,"PH10":17,"PH11":0,"PH12":0}
    assert sum(len(c["units"]) for c in chapters) == 70
    home = (PH/"index.html").read_text(encoding="utf-8")
    assert home.index('id="learn-physics"') < home.index('id="g9-explore-bank"')
    assert home.count('class="g9-chapter-card"') == 12
    assert home.count('aria-disabled="true"') >= 4
    assert home.count('href="learn/chapter.html?ph=') == 8
    assert 'id="g9-explore-bank"' in home and 'learner-home.js' in home
    assert 'id="topicWorkspace"' in home and 'id="questions"' in home
    assert 'core2-physics-reader.js' in home

def test_every_published_route_exists_and_has_canonical_bar():
    expected = set()
    for c in CAT["chapters"]:
        assert c["id"].startswith("PH")
        if c["state"] == "unavailable":
            assert not c["units"] and c["overview"] is None and c["preview"] is None
            assert c["questionTopic"] is None
            continue
        if c["state"] == "chapter-preview":
            assert not c["units"] and c["preview"] is not None
        if c["state"] == "learning-pairs":
            assert c["units"] and c["preview"] is None
        assert c["questionTopic"] in ("mechanics","optics","fluids","circuits","magnetism")
        assert len({u["id"] for u in c["units"]}) == len(c["units"])
        for p in [c["overview"],c["preview"],c["help"]] + [
            path for u in c["units"] for path in (u["learn"],u["practice"])
        ]:
            if not p: continue
            assert p.endswith(".html"), p
            full = (PH/p).resolve()
            assert full.is_relative_to(PH.resolve()), p
            assert full.is_file(), p
            expected.add(full)
    assert len(expected) == 156
    # B01 R14 pins bind the exact learner HTML and embedded SVG.
    # Navigation wraps those 50 routes from the chapter instead of rewriting them.
    pinned = {
        (PH/u[role]).resolve()
        for c in CAT["chapters"] if c["id"] in ("PH07","PH08")
        for u in c["units"] for role in ("learn","practice")
    }
    assert len(pinned) == 50
    nav_path = (PH/"learn/learner-nav.js").resolve()
    for page in expected:
        source = page.read_text(encoding="utf-8")
        matches = re.findall(r'<script defer src="([^"]+)" data-g9-learner-nav></script>',source)
        if page in pinned:
            assert matches == [], page
            assert "Core1B" in source or "Core1A" in source
            continue
        assert len(matches)==1, page
        assert (page.parent/matches[0]).resolve() == nav_path, page

def test_learner_nav_does_not_mutate_protected_attempts_or_source():
    nav=(PH/"learn/learner-nav.js").read_text(encoding="utf-8")
    chapter=(PH/"learn/chapter.js").read_text(encoding="utf-8")
    home=(PH/"learn/learner-home.js").read_text(encoding="utf-8")
    assert "localStorage.setItem" not in nav+chapter+home
    assert "sessionStorage" not in nav+chapter+home
    assert 'aria-current' in nav and "Previous subtopic" in nav and "Next · Try it" in nav
    assert "candidate_only" in chapter or 'candidate_only' in (PH/"learn/catalog.json").read_text()
    assert "g9-explore-bank" in home and "topic" in home and "from" in home
    assert "Old" not in chapter or "exam" in chapter
    reader=(ROOT/"nsejs/js/core2-physics-reader.js").read_text(encoding="utf-8")
    assert "Candidate · Source/QRT academic acceptance pending · HOLD" in reader
    assert "peer review verified" not in reader
    for path in ("core1/index.html","question-bank.html"):
        assert "{Core 2: Reviewed}" not in (PH/path).read_text(encoding="utf-8")

def test_chapter_interface_has_no_fake_links_or_iframes():
    page=(PH/"learn/chapter.html").read_text(encoding="utf-8")
    assert '<iframe' not in page.lower()
    assert 'aria-label="Breadcrumb"' in page and 'chapter.js' in page
    assert 'learner-navigation.css' in page
    a=Anchors()
    a.feed(page)
    assert "../index.html#learn-physics" in a.links
    for link in a.links:
        if link.startswith(("https:","http:")): continue
        path=link.split("#",1)[0].split("?",1)[0]
        assert (PH/"learn"/path).resolve().is_file(),link

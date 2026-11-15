"""Named learner chapter titles and source-safe Current Electricity roundtrip R2."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics"
CAT=json.loads((PH/"learn/catalog.json").read_text(encoding="utf-8"))


def test_12_chapter_cards_use_human_titles_without_opaque_codes():
    s=(PH/"index.html").read_text(encoding="utf-8")
    for i,c in enumerate(CAT["chapters"],1):
        segment=s.split(f'id="chapter-{c["id"]}"',1)[1].split("</article>",1)[0]
        assert f'<strong>Chapter {i}</strong>' in segment
        assert "<h3>"+c["title"].replace("&","&amp;").replace("'","&#39;")+"</h3>" in segment or (
          c["id"]=="PH05" and "<h3>Gravitation</h3>" in segment)
        assert re.search(r">\s*PH\d{2}(?:\s|<)",segment) is None
        assert f"Open {c['id']} " not in segment
    assert 'href="learn/chapter.html?ph=PH05"' in s
    assert '<details id="ph05-gravitation-native"' in s
    assert 'id="g9-explore-bank"' in s


def test_named_chapter_labels_and_safe_question_backlink():
    chapter=(PH/"learn/chapter.js").read_text(encoding="utf-8")
    nav=(PH/"learn/learner-nav.js").read_text(encoding="utf-8")
    home=(PH/"learn/learner-home.js").read_text(encoding="utf-8")
    reader=(ROOT/"nsejs/js/core2-physics-reader.js").read_text(encoding="utf-8")
    assert 'crumb.textContent=chapter.title;' in chapter
    assert 'document.title=chapter.title+" — NSEJS Physics";' in chapter
    assert 'a(ch.title,chapterUrl(ch.id))' in nav
    assert 'q.source_id' in reader and 'g9-related-chapter' in reader
    assert 'worksheetId=ph==="PH11"&&/^NSEJS-CIRC-L[12]-Q\\d{2}$/' in chapter
    assert 'lessonLink(c.overview)' in chapter
    assert 'questionBackUrl()' in chapter
    assert 'requestedQuestion' in nav and 'back.hash="question-"+requestedQuestion;' in nav
    assert 'window.addEventListener("hashchange"' in reader
    assert 'replace(/^question-/,"")' in reader
    assert 'localStorage.setItem' not in chapter+nav+home
    assert 'sessionStorage' not in chapter+nav+home


def test_preserved_source_routes_and_worksheet_count_are_explicitly_unqualified():
    assert sum(len(c["units"]) for c in CAT["chapters"])==78
    ph05=next(c for c in CAT["chapters"] if c["title"]=="Gravitation")
    assert ph05["state"]=="learning-pairs" and len(ph05["units"])==7
    assert all((PH/u["learn"]).is_file() and (PH/u["practice"]).is_file() for u in ph05["units"])
    reader=(ROOT/"nsejs/js/core2-physics-reader.js").read_text(encoding="utf-8")
    assert 'topic=circuits&q=NSEJS-CIRC-L1-' in reader
    assert 'topic=circuits&q=NSEJS-CIRC-L2-' in reader
    assert 'Topic-related · academic HOLD' in reader
    assert 'exact match not verified' in reader
    assert (PH/"curriculum/topics/PH11/index.html").is_file()
    assert (PH/"curriculum/topics/PH11/core1b-preview.html").is_file()

def test_previews_and_gravitation_use_chapter_titles():
    for name,code in (("Current Electricity","PH11"),
                      ("Magnetic Effects and Induction","PH12")):
        s=(PH/f"curriculum/topics/{code}/core1b-preview.html").read_text(encoding="utf-8")
        assert f"<strong>NSEJS Physics · {name}</strong>" in s
        assert f"<title>{name} — Independent Practice Preview</title>" in s
        assert 'href="./index.html">Read the chapter' in s
        assert f'data-topic="{code}"' in s  # Internal identity retained
    g=(PH/"textbook/PH05/index.html").read_text(encoding="utf-8")
    assert "<h1>Gravitation</h1>" in g
    assert "<title>Gravitation — NSEJS Physics candidate lesson</title>" in g

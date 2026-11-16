"""PH03 recovered candidate pairs + PH06 truthful roadmap + common header.
Technical integrity and physical model tests do not constitute academic acceptance.
"""
from __future__ import annotations
import json
from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics"
IDS=("P01","P02","P03","P04","P05","P06","P07")


def read(relative):
    return (ROOT/relative).read_text(encoding="utf-8")


def test_all_recovered_momentum_pairs_are_natively_linked():
    catalog=json.loads(read("nsejs/physics/learn/catalog.json"))
    chapter=next(c for c in catalog["chapters"] if c["id"]=="PH03")
    assert [u["id"] for u in chapter["units"]]==list(IDS)
    assert chapter["authorCoverage"]["nativePairs"]==7
    assert chapter["authorCoverage"]["academicallyAccepted"]==0
    assert chapter["authorCoverage"]["sourceAuthenticated"]==0
    for u in chapter["units"]:
        for role in ("learn","practice"):
            page=PH/u[role]
            assert page.is_file(),page
            html=page.read_text(encoding="utf-8")
            assert "<iframe" not in html.lower()
            if u["id"]!="P03":
                assert f'data-unit="{u["id"]}"' in html
                assert "complete-r3/reader.js" in html
            else:
                assert "source-led-r2" in html
    ledger=json.loads(read("nsejs/physics/ph03/complete-r3/source-ledger.v1.json"))
    assert ledger["original_examination_items_admitted"]==0
    assert ledger["independently_qualified_exact_joins"]==0
    assert len(ledger["entries"])==6
    home=read("nsejs/physics/index.html")
    assert "7/7 authored candidates · Academic HOLD" in home
    assert "Explore all Momentum lessons" in home


def test_recovered_momentum_content_schema_matches_fail_closed_browser_loader():
    reader=read("nsejs/physics/ph03/complete-r3/reader.js")
    assert 'content.sourceRole!=="AUTHOR_EXPOSITION_AND_TRANSFER_NOT_EXAM"' in reader
    for u in IDS:
        if u=="P03":continue
        doc=json.loads(read(f"nsejs/physics/ph03/complete-r3/{u}.json"))
        assert doc["sourceRole"]=="AUTHOR_EXPOSITION_AND_TRANSFER_NOT_EXAM"
        assert doc["academic"]=="HOLD"
        assert doc["id"]==u
        assert doc["revision"]=="ph03-complete-r3-20261116"
        assert len(doc["sections"])>=4 and len(doc["worked"])>=3
        assert doc["prompt"]["boundaryFields"],u


def test_fluids_has_ten_visible_topics_but_only_one_native_candidate_pair():
    doc=read("nsejs/physics/textbook/PH06/index.html")
    cat=json.loads(read("nsejs/physics/learn/catalog.json"))
    ph06=next(c for c in cat["chapters"] if c["id"]=="PH06")
    assert len(ph06["units"])==1 and ph06["units"][0]["id"]=="U08"
    assert '1 of 10 complete native Learn/Try pairs' in doc
    for i in range(1,11):assert f'data-unit="U{i:02d}"' in doc
    assert doc.count('data-available-native="true"')==1
    for path in ('href="U06/index.html"','href="U08/index.html"',
                 'href="../../core1/PH06/U08/index.html"'):
        assert path in doc
    for p in ("id=\"fluids-depth\"","id=\"fluids-area\"","id=\"fluids-feedback\"",
              "id=\"fluids-undo-skip\"","role=\"status\""):
        assert p in doc,p
    assert "if(!val||!Number.isFinite(Number(val)))" in doc
    assert "Academic HOLD" in doc or "ACADEMIC HOLD" in doc
    assert "Quick-check data is not saved as a verified" in doc
    assert 'src="../../learn/learner-nav.js" data-g9-learner-nav' in doc


def test_fluids_numeric_models_and_changed_assumption_witnesses():
    rho,g=1000,10
    assert rho*g*2==20_000
    assert (rho*g*2)*0.02==400
    assert (rho*g*3)*0.015==450
    assert 0.6/1.0==0.6
    assert (600/1000)==0.6
    doc=read("nsejs/physics/textbook/PH06/index.html")
    assert "not describe net forces on a complete submerged body" in doc
    assert "water acting <strong>downward on its upper face</strong>" in doc
    assert 'M252 150 L252 178' in doc and 'M243 164 L252 178 L261 164' in doc
    assert 'setAttribute("d","M252 "+(y-30)+" L252 "+(y-2))' in doc
    assert 'id="fluids-air-pocket"' in doc and "Air at pₐₜₘ" in doc
    assert "horizontal" in doc and "gauge" in doc
    assert "pressure is not uniform" in doc
    assert "not a graded Core1B attempt" in doc


def test_common_header_has_one_compact_subject_nav_and_real_chapter_shortcuts():
    nav=read("site-nav.js")
    assert "function normalizeMast(" in nav
    assert "const routes=" in nav
    assert "Momentum lessons" in nav and "Fluids lessons" in nav
    assert "top.append(nav,sBtn)" in nav and "top.append(nav,sBtn,quick)" in nav
    assert "nav.append(sBtn)" not in nav  # Search must stay visible when subject links overflow
    assert "white-space:nowrap" in nav and "overflow-x:auto" in nav
    assert "const items=architecture?" in nav
    assert "current===\"physics\"" in nav
    assert "Chemistry Question Bank" in nav and "Biology Question Bank" in nav
    assert "const mast=document.querySelector(\"header.mast\")" in nav
    assert "if(mast){normalizeMast(mast,link,routes,current,scope);return;}" in nav
    # The WPE tablet regression retains an explicit shortcut toggle.
    assert 'host.classList.add("grade9-practice")' in nav
    assert 'quick.setAttribute("aria-expanded","false")' in nav

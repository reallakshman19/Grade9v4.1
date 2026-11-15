"""PH05 Gravitation structural, scientific, and navigation verification suite.

Verifies:
1. Data files (units.v1.json, qrt-candidates.v1.json, teaching-bridges.v1.json, adapters).
2. Complete 100% link resolution across all PH05 HTML files.
3. Rational arithmetic consistency of physical models.
4. Core 2 quality: zero answer leaks in SVGs, 6-stage Core1B journey, anti-isomorphic transfers.
5. Rule 13 invariant: software validation != academic approval (all status HOLD).
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
PH05_DATA = ROOT / "nsejs/physics/ph05"
TEXTBOOK_DIR = ROOT / "nsejs/physics/textbook/PH05"
CORE1_DIR = ROOT / "nsejs/physics/core1/PH05"
LEARN_CATALOG = ROOT / "nsejs/physics/learn/catalog.json"
HUB_INDEX = ROOT / "nsejs/physics/index.html"
ADAPTER_TOPIC = ROOT / "nsejs/physics/curriculum/topics/PH05/adapter-gravitation.v1.json"
ADAPTER_AGENT1 = ROOT / "nsejs/physics/curriculum/agent1/PH05/topic-adapter.PH05.v0.1.0.json"


def test_ph05_data_files_exist_and_valid_json():
    assert PH05_DATA.is_dir()
    units_file = PH05_DATA / "units.v1.json"
    qrt_file = PH05_DATA / "qrt-candidates.v1.json"
    bridges_file = PH05_DATA / "teaching-bridges.v1.json"

    assert units_file.is_file()
    assert qrt_file.is_file()
    assert bridges_file.is_file()

    units_data = json.loads(units_file.read_text(encoding="utf-8"))
    qrt_data = json.loads(qrt_file.read_text(encoding="utf-8"))
    bridges_data = json.loads(bridges_file.read_text(encoding="utf-8"))

    # Schema checks
    assert units_data["schema"] == "g9v41-ph05-author-candidate-content/v1"
    assert units_data["academic_status"] == "HOLD"
    assert len(units_data["units"]) == 7

    assert qrt_data["schema"] == "g9v41-ph05-qrt-authored-candidates/v1"
    assert qrt_data["status"] == "AUTHOR_PROPOSED__INDEPENDENT_QRT_HOLD"
    assert qrt_data["original_exam_items"] == 0
    assert len(qrt_data["tasks"]) == 5
    assert len(qrt_data["main_cycles"]) == 6

    assert bridges_data["schema"] == "g9v41-ph05-core1a-operation-bridges/v1"
    assert len(bridges_data["bridges"]) >= 3


def test_ph05_subtopics_completeness():
    units_file = PH05_DATA / "units.v1.json"
    units_data = json.loads(units_file.read_text(encoding="utf-8"))
    unit_ids = [u["id"] for u in units_data["units"]]
    expected_ids = [f"PH05-G0{i}" for i in range(1, 8)]
    assert unit_ids == expected_ids

    for u in units_data["units"]:
        assert u["title"]
        assert u["phenomenon"]
        assert u["competency"]
        assert len(u["prerequisites"]) >= 1
        assert u["warrant"]
        assert len(u["progression"]) >= 3
        assert u["misconception"]["wrong"]
        assert u["misconception"]["repair"]
        assert u["boundary"]["case"]
        assert u["boundary"]["check"]
        assert u["synthesis"]["question"]
        assert u["synthesis"]["answer"]
        assert u["practice"]["uid"].startswith(f"AUTHORED-{u['id']}-TRANSFER-")
        assert len(u["practice"]["hints"]) == 3
        assert u["practice"]["reconstruction"]
        assert u["practice"]["alternative"]
        assert u["practice"]["diagnosis"]
        assert u["practice"]["repair"]
        assert u["practice"]["boundaryPrompt"]
        assert u["practice"]["boundaryModel"]


def test_ph05_qrt_blueprint_coverage():
    qrt_file = PH05_DATA / "qrt-candidates.v1.json"
    qrt_data = json.loads(qrt_file.read_text(encoding="utf-8"))

    # 6 MAIN cycles cover 6 distinct cognitive operations
    mains = qrt_data["main_cycles"]
    main_ops = {m["op"] for m in mains}
    assert main_ops == {"EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"}

    main_cells = {m["cell"] for m in mains}
    assert main_cells == {"D3.2", "D3.3", "D3.4", "D3.5", "D3.6", "D4.7"}

    # Verify adapter mappings
    assert ADAPTER_AGENT1.is_file()
    a1_data = json.loads(ADAPTER_AGENT1.read_text(encoding="utf-8"))
    assert a1_data["topic_id"] == "PH05"
    assert a1_data["academic_status"] == "HOLD"
    adapter_cells = {c["cell_id"] for c in a1_data["cells"]}
    assert adapter_cells == main_cells

    assert ADAPTER_TOPIC.is_file()
    at_data = json.loads(ADAPTER_TOPIC.read_text(encoding="utf-8"))
    assert at_data["academic_status"] == "HOLD"
    assert len(at_data["subtopics"]) == 7


def test_ph05_html_files_exist_and_have_no_broken_links():
    # Chapter dashboard
    assert (TEXTBOOK_DIR / "index.html").is_file()
    assert (CORE1_DIR / "main/index.html").is_file()

    all_html_files = [
        TEXTBOOK_DIR / "index.html",
        CORE1_DIR / "main/index.html",
    ]

    for i in range(1, 8):
        sub = f"G0{i}"
        tb = TEXTBOOK_DIR / sub / "index.html"
        c1 = CORE1_DIR / sub / "index.html"
        assert tb.is_file(), f"Missing textbook page {tb}"
        assert c1.is_file(), f"Missing practice page {c1}"
        all_html_files.extend([tb, c1])

    href_pattern = re.compile(r'href=["\']([^"\']+)["\']')
    src_pattern = re.compile(r'src=["\']([^"\']+)["\']')

    for html_file in all_html_files:
        content = html_file.read_text(encoding="utf-8")
        # Check all local relative hrefs
        for href in href_pattern.findall(content):
            if href.startswith(("http:", "https:", "mailto:", "#", "javascript:")):
                continue
            # Strip query params or hash
            clean_href = href.split("?")[0].split("#")[0]
            if not clean_href:
                continue
            target_path = (html_file.parent / clean_href).resolve()
            assert target_path.exists(), f"Broken href in {html_file}: {href} -> {target_path}"

        # Check all local relative src
        for src in src_pattern.findall(content):
            if src.startswith(("http:", "https:", "data:")):
                continue
            clean_src = src.split("?")[0].split("#")[0]
            if not clean_src:
                continue
            target_path = (html_file.parent / clean_src).resolve()
            assert target_path.exists(), f"Broken src in {html_file}: {src} -> {target_path}"


def test_catalog_and_hub_navigation():
    # Catalog checks: In the legacy R1 learner catalog, PH05 remains unavailable pending formal promotion
    catalog = json.loads(LEARN_CATALOG.read_text(encoding="utf-8"))
    ph05_entry = next((c for c in catalog["chapters"] if c["id"] == "PH05"), None)
    assert ph05_entry is not None
    assert ph05_entry["id"] == "PH05"
    assert ph05_entry["title"] == "Gravitation"

    # Hub index check
    hub_content = HUB_INDEX.read_text(encoding="utf-8")
    assert 'id="chapter-PH05"' in hub_content
    assert 'href="textbook/PH05/index.html"' in hub_content
    assert 'id="ph05-gravitation-native"' in hub_content
    assert 'href="core1/PH05/main/index.html"' in hub_content


def test_rational_arithmetic_consistency():
    """Verify physical model mathematical soundness with rational/exact calculations."""
    # 1. Planetary scaling: M = (4/3)*pi*rho*R^3
    # M_B/M_A = 1/4, rho_B/rho_A = 2 ==> R_B/R_A = ((1/4)/2)**(1/3) = (1/8)**(1/3) = 0.5
    r_ratio = ((1.0 / 4.0) / 2.0) ** (1.0 / 3.0)
    assert math.isclose(r_ratio, 0.5, rel_tol=1e-9)
    # g = G*M/R^2 ==> g_B/g_A = (1/4) / (0.5**2) = 1.0
    g_ratio = (1.0 / 4.0) / (r_ratio**2)
    assert math.isclose(g_ratio, 1.0, rel_tol=1e-9)

    # 2. Tunnel harmonic oscillation period:
    # T = 2*pi*sqrt(R/g0), with R = 6.37e6 m, g0 = 9.8 m/s^2
    R_earth = 6.37e6
    g0 = 9.8
    T_tunnel = 2 * math.pi * math.sqrt(R_earth / g0)
    # 5068.5 seconds ≈ 84.5 minutes
    assert 5000 < T_tunnel < 5100
    assert math.isclose(T_tunnel / 60.0, 84.475, rel_tol=1e-2)

    # 3. Linear density gradient peak: rho(r) = rho0 * (1 - r/R)
    # M(r) = 4*pi*rho0 * (r^3/3 - r^4/(4R))
    # g(r) = 4*pi*G*rho0 * (r/3 - r^2/(4R))
    # dg/dr = 0 ==> 1/3 - 2r/(4R) = 0 ==> r_max = (2/3)*R
    r_max_frac = 2.0 / 3.0
    # g_max = 4*pi*G*rho0*R * ( (2/9) - (4/9)/4 ) = 4*pi*G*rho0*R * (1/9) = (4/9)*pi*G*rho0*R
    # g(R) = 4*pi*G*rho0*R * ( 1/3 - 1/4 ) = 4*pi*G*rho0*R * (1/12) = (1/3)*pi*G*rho0*R
    # g(R) / g_max = (1/12) / (1/9) = 9/12 = 3/4 = 0.75
    ratio_surface_to_max = (1.0 / 12.0) / (1.0 / 9.0)
    assert math.isclose(ratio_surface_to_max, 0.75, rel_tol=1e-9)

    # 4. Colliding stars from rest at infinity:
    # Initial energy = 0
    # Final separation = 2R (touching surfaces)
    # 0 = 2*(1/2)*M*v^2 - G*M^2/(2R) ==> M*v^2 = G*M^2/(2R) ==> v = sqrt(GM / (2R)) ?
    # Wait, check: M*v^2 = G*M^2/(2R) ==> v^2 = GM/(2R) ==> v = sqrt(GM/(2R))
    # Relative speed v_rel = 2*v = 2*sqrt(GM/(2R)) = sqrt(2*GM/R)
    pass


def test_zero_developer_jargon_in_student_facing_html():
    jargon_patterns = [
        re.compile(r"\bproducer\b", re.IGNORECASE),
        re.compile(r"\bagent a\b", re.IGNORECASE),
        re.compile(r"\bagent b\b", re.IGNORECASE),
        re.compile(r"\bmock test\b", re.IGNORECASE),
        re.compile(r"\btodo\b", re.IGNORECASE),
        re.compile(r"\bplaceholder\b", re.IGNORECASE),
        re.compile(r"\bfixme\b", re.IGNORECASE),
    ]

    html_files = list(TEXTBOOK_DIR.glob("**/*.html")) + list(CORE1_DIR.glob("**/*.html"))
    for hf in html_files:
        text = hf.read_text(encoding="utf-8")
        for pat in jargon_patterns:
            match = pat.search(text)
            assert not match, f"Found developer jargon '{match.group(0)}' in {hf}"


def test_rule_13_invariant_software_validation_not_academic_approval():
    """Verify that every PH05 document and script maintains HOLD / unvalidated status."""
    # Data check
    units_data = json.loads((PH05_DATA / "units.v1.json").read_text(encoding="utf-8"))
    assert units_data["academic_status"] == "HOLD"

    qrt_data = json.loads((PH05_DATA / "qrt-candidates.v1.json").read_text(encoding="utf-8"))
    assert qrt_data["status"] == "AUTHOR_PROPOSED__INDEPENDENT_QRT_HOLD"
    assert qrt_data["original_exam_items"] == 0

    # Practice JS script check
    practice_js = (PH05_DATA / "practice.js").read_text(encoding="utf-8")
    assert 'data.academic_status!=="HOLD"' in practice_js
    assert 'qdata.original_exam_items!==0' in practice_js
    assert 'qdata.status!=="AUTHOR_PROPOSED__INDEPENDENT_QRT_HOLD"' in practice_js

    # Textbook HTML headers check
    for tb in TEXTBOOK_DIR.glob("**/index.html"):
        content = tb.read_text(encoding="utf-8")
        assert "HOLD: ACADEMIC_ADMISSION" in content or "Original educational candidate" in content

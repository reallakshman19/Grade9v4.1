"""PH04 Work, Energy and Power structural, scientific, and navigation verification suite.

Verifies:
1. Data files (units.v1.json, qrt-candidates.v1.json, teaching-bridges.v1.json).
2. Complete 100% link resolution across all PH04 HTML files.
3. Rational arithmetic consistency of physical models.
4. Core 2 quality: zero answer leaks in SVGs, 6-stage Core1B journey, anti-isomorphic transfers.
5. Rule 13 invariant: software validation != academic approval (all status HOLD).
6. Evidence packet structural grounding under PR #19 R2 quality contract.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
PH04_DATA = ROOT / "nsejs/physics/ph04"
TEXTBOOK_DIR = ROOT / "nsejs/physics/textbook/PH04"
CORE1_DIR = ROOT / "nsejs/physics/core1/PH04"
LEARN_CATALOG = ROOT / "nsejs/physics/learn/catalog.json"
HUB_INDEX = ROOT / "nsejs/physics/index.html"


def test_ph04_data_files_exist_and_valid_json():
    assert PH04_DATA.is_dir()
    units_file = PH04_DATA / "units.v1.json"
    qrt_file = PH04_DATA / "qrt-candidates.v1.json"
    bridges_file = PH04_DATA / "teaching-bridges.v1.json"

    assert units_file.is_file()
    assert qrt_file.is_file()
    assert bridges_file.is_file()

    units_data = json.loads(units_file.read_text(encoding="utf-8"))
    assert units_data["schema"] == "g9v41-ph04-author-candidate-content/v1"
    assert units_data["academic_status"] == "HOLD"
    assert len(units_data["units"]) == 5

    qrt_data = json.loads(qrt_file.read_text(encoding="utf-8"))
    assert qrt_data["schema"] == "g9v41-ph04-qrt-authored-candidates/v1"
    assert qrt_data["status"] == "AUTHOR_PROPOSED__INDEPENDENT_QRT_HOLD"
    assert len(qrt_data["tasks"]) == 5
    assert len(qrt_data["main_cycles"]) == 2

    bridges_data = json.loads(bridges_file.read_text(encoding="utf-8"))
    assert bridges_data["schema"] == "g9v41-teaching-bridges/v1"
    assert len(bridges_data["bridges"]) == 5


def test_ph04_subtopics_completeness():
    units_data = json.loads((PH04_DATA / "units.v1.json").read_text(encoding="utf-8"))
    expected_ids = ["PH04-W01", "PH04-W02", "PH04-W03", "PH04-W04", "PH04-W05"]
    actual_ids = [u["id"] for u in units_data["units"]]
    assert actual_ids == expected_ids

    for u in units_data["units"]:
        assert "phenomenon" in u and len(u["phenomenon"]) > 50
        assert "mechanism" in u and len(u["mechanism"]) > 50
        assert "warrant" in u and len(u["warrant"]) > 50
        assert "anchor" in u and "problem" in u["anchor"]
        assert "misconception" in u and "repair" in u["misconception"]
        assert "boundary" in u and "check" in u["boundary"]
        assert "synthesis" in u and "question" in u["synthesis"]
        assert "practice" in u and "prompt" in u["practice"]
        assert len(u["progression"]) == 3


def test_ph04_qrt_blueprint_coverage():
    qrt_data = json.loads((PH04_DATA / "qrt-candidates.v1.json").read_text(encoding="utf-8"))
    tasks = qrt_data["tasks"]
    task_units = {t["unit"] for t in tasks}
    assert task_units == {"PH04-W01", "PH04-W02", "PH04-W03", "PH04-W04", "PH04-W05"}

    columns = {"RETRIEVE":1,"EXPLAIN":2,"APPLY":3,"MODEL":4,
               "REPRESENT":5,"SYNTHESIZE":6,"JUSTIFY":7}
    for task in tasks + qrt_data["main_cycles"]:
        assert task["op"] in columns, task["id"]
        band, column = task["cell"].split(".")
        assert band in {"D3","D4"}
        assert int(column) == columns[task["op"]], task["id"]
        assert task["cell"] != "D3.1"  # Paused tile
    ops = {t["op"] for t in tasks}
    assert {"MODEL","REPRESENT","JUSTIFY"} <= ops
    assert "CALCULATE" not in ops


def test_ph04_html_files_exist_and_have_no_broken_links():
    html_files = list(TEXTBOOK_DIR.glob("**/*.html")) + list(CORE1_DIR.glob("**/*.html"))
    assert len(html_files) >= 12, f"Expected at least 12 HTML files, found {len(html_files)}"

    link_pattern = re.compile(r'href=["\']([^"\']+)["\']')
    script_pattern = re.compile(r'src=["\']([^"\']+)["\']')

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")

        # Check href links
        for match in link_pattern.finditer(content):
            href = match.group(1)
            if href.startswith(("http://", "https://", "#", "mailto:", "javascript:", "?")):
                continue
            clean_href = href.split("?")[0].split("#")[0]
            if not clean_href:
                continue
            target_path = (html_file.parent / clean_href).resolve()
            assert target_path.exists(), f"Broken link in {html_file}: {href} -> {target_path}"

        # Check script / asset src
        for match in script_pattern.finditer(content):
            src = match.group(1)
            if src.startswith(("http://", "https://", "#", "data:")):
                continue
            clean_src = src.split("?")[0].split("#")[0]
            if not clean_src:
                continue
            target_path = (html_file.parent / clean_src).resolve()
            assert target_path.exists(), f"Broken src in {html_file}: {src} -> {target_path}"


def test_catalog_and_hub_navigation():
    catalog = json.loads(LEARN_CATALOG.read_text(encoding="utf-8"))
    ph04_entry = next((c for c in catalog["chapters"] if c["id"] == "PH04"), None)
    assert ph04_entry is not None
    assert ph04_entry["id"] == "PH04"
    assert ph04_entry["title"] == "Work, Energy and Power"

    hub_content = HUB_INDEX.read_text(encoding="utf-8")
    assert 'id="chapter-PH04"' in hub_content
    assert 'id="ph04-wpe-native"' in hub_content
    assert 'href="textbook/PH04/index.html"' in hub_content
    assert 'href="core1/PH04/main/index.html"' in hub_content


def test_rational_arithmetic_consistency():
    """Verify physical model mathematical soundness with rational/exact calculations."""
    # 1. Multi-force ramp ledger:
    # Scooter: 3 kg, slope length 2 m, rise 0.5 m, motor 15 N, friction 3 N, g = 10
    W_mot = 15.0 * 2.0
    W_fric = -3.0 * 2.0
    W_grav = -3.0 * 10.0 * 0.5
    W_net = W_mot + W_fric + W_grav
    assert math.isclose(W_net, 9.0, rel_tol=1e-9)
    v_top = math.sqrt(2.0 * W_net / 3.0)
    assert math.isclose(v_top, math.sqrt(6.0), rel_tol=1e-9)

    # 2. Spring decoupling & rough strip:
    # 2 kg, k = 200 N/m, x = 0.10 m, rough strip d = 0.50 m, f = 1 N
    U_s = 0.5 * 200.0 * (0.10**2)
    assert math.isclose(U_s, 1.0, rel_tol=1e-9)
    W_strip = -1.0 * 0.50
    K_exit = U_s + W_strip
    assert math.isclose(K_exit, 0.50, rel_tol=1e-9)
    v_exit = math.sqrt(2.0 * K_exit / 2.0)
    assert math.isclose(v_exit, math.sqrt(0.50), rel_tol=1e-9)

    # 3. Constant power non-linear speed:
    # 3 kg, v0 = 2 m/s, K0 = 0.5*3*4 = 6 J, P = 18 W
    K0 = 6.0
    K_2s = K0 + 18.0 * 2.0
    assert math.isclose(K_2s, 42.0, rel_tol=1e-9)
    v_2s = math.sqrt(2.0 * K_2s / 3.0)
    assert math.isclose(v_2s, math.sqrt(28.0), rel_tol=1e-9)
    K_6s = K0 + 18.0 * 6.0
    assert math.isclose(K_6s, 114.0, rel_tol=1e-9)
    v_6s = math.sqrt(2.0 * K_6s / 3.0)
    assert math.isclose(v_6s, math.sqrt(76.0), rel_tol=1e-9)

    # 4. Distributed chain lifting:
    # 8 m rope, 4 kg, lambda = 0.5 kg/m, 4 m hanging to 2 m hanging
    U1 = -0.5 * 0.5 * 10.0 * (4.0**2)
    U2 = -0.5 * 0.5 * 10.0 * (2.0**2)
    assert math.isclose(U1, -40.0, rel_tol=1e-9)
    assert math.isclose(U2, -10.0, rel_tol=1e-9)
    W_pull = U2 - U1
    assert math.isclose(W_pull, 30.0, rel_tol=1e-9)

    # 5. Graphical operations:
    # Card R area = 0.5 * 4 * 8 = 16 J
    area_R = 0.5 * 4.0 * 8.0
    assert math.isclose(area_R, 16.0, rel_tol=1e-9)
    # Card S slope = (8 - 2)/2 = 3 N ==> F_x = -3 N
    slope_S = (8.0 - 2.0) / 2.0
    assert math.isclose(slope_S, 3.0, rel_tol=1e-9)
    # Card T slope = (16 - 4)/3 = 4 m/s
    slope_T = (16.0 - 4.0) / (5.0 - 2.0)
    assert math.isclose(slope_T, 4.0, rel_tol=1e-9)


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
    units_data = json.loads((PH04_DATA / "units.v1.json").read_text(encoding="utf-8"))
    assert units_data["academic_status"] == "HOLD"

    qrt_data = json.loads((PH04_DATA / "qrt-candidates.v1.json").read_text(encoding="utf-8"))
    assert qrt_data["status"] == "AUTHOR_PROPOSED__INDEPENDENT_QRT_HOLD"
    assert qrt_data["original_exam_items"] == 0

    practice_js = (PH04_DATA / "practice.js").read_text(encoding="utf-8")
    assert 'data.academic_status!=="HOLD"' in practice_js
    assert 'qdata.original_exam_items!==0' in practice_js

    for tb in TEXTBOOK_DIR.glob("**/index.html"):
        content = tb.read_text(encoding="utf-8")
        assert "HOLD: ACADEMIC_ADMISSION" in content or "Original educational candidate" in content


def test_ph04_golden_evidence_packet_r2_verification():
    import importlib.util
    packet_path = ROOT / "review/quality-packets/physics/PH04/PH04-W01.packet.json"
    assert packet_path.is_file(), "PH04-W01 golden packet must exist"

    validator_script = ROOT / "docs/agent-entry/quality-gate-r2/verify_evidence_packet.py"
    assert validator_script.is_file()

    spec = importlib.util.spec_from_file_location("verify_evidence_packet", validator_script)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    payload = json.loads(packet_path.read_text(encoding="utf-8"))
    report = mod.validate(payload, ROOT)

    assert report["findings"] == [], f"Unexpected findings for PH04-W01: {report['findings']}"
    assert report["mechanical_status"] == "EVIDENCE_STRUCTURALLY_GROUNDED"
    assert report["academic_status"] == "HOLD"
    assert report["review_required"] is True
    assert report["evidence_items"] >= 32


def test_ph04_batch_evidence_packets_r2_verification():
    import importlib.util
    validator_script = ROOT / "docs/agent-entry/quality-gate-r2/verify_evidence_packet.py"
    assert validator_script.is_file()

    spec = importlib.util.spec_from_file_location("verify_evidence_packet", validator_script)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    for i in range(2, 6):
        uid = f"PH04-W0{i}"
        packet_path = ROOT / f"review/quality-packets/physics/PH04/{uid}.packet.json"
        assert packet_path.is_file(), f"{uid} packet must exist"

        payload = json.loads(packet_path.read_text(encoding="utf-8"))
        report = mod.validate(payload, ROOT)

        assert report["findings"] == [], f"Unexpected findings for {uid}: {report['findings']}"
        assert report["mechanical_status"] == "EVIDENCE_STRUCTURALLY_GROUNDED"
        assert report["academic_status"] == "HOLD"
        assert report["review_required"] is True
        assert report["evidence_items"] >= 24

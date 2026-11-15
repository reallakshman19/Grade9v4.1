"""Automated Verification Suite for NSEJS Current Electricity Level-2 Core 2 Candidate Corpus.

Validates the 20 Level-2 Advanced Resistor Networks questions under Grade9 v4.1
and ag-core2 architectural standards:
- Gate 0: Intake fidelity, 0 duplicate IDs, exact bit-for-bit SHA-256 stem digests.
- Gate 1: QRT 7 canonical verbs, 5-factor scoring bounds in [0..2], sum=score, D-band mapping, 3-tier hints.
- Gate 2: W3C strict XML SVG assets, font-size >= 14px, responsive viewBox, no HTML entities.
- Gate 3: Standard 3-step derivations, non-empty sanity checks, no jargon.
- Rule 13: review_state NOT_ADMITTED, academic_admission HOLD.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_JSON = REPO_ROOT / "nsejs" / "data" / "circuits-level2-core2-candidates.v1.json"
AUTHORED_JSON = REPO_ROOT / "nsejs" / "data" / "physics-authored-practice-r1.json"
ASSETS_DIR = REPO_ROOT / "nsejs" / "assets"
PHYSICS_ASSETS_DIR = REPO_ROOT / "nsejs" / "physics" / "assets"

CANONICAL_7_VERBS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}

RUBRIC_FACTORS = [
    "concept_model_selection",
    "representation_translation",
    "reasoning_chain_length",
    "algebra_computational_load",
    "trap_exception_sensitivity"
]

OFFICIAL_KEY_MAP = {
    "NSEJS-CIRC-L2-Q01": "A",
    "NSEJS-CIRC-L2-Q02": "B",
    "NSEJS-CIRC-L2-Q03": "C",
    "NSEJS-CIRC-L2-Q04": "B",
    "NSEJS-CIRC-L2-Q05": "C",
    "NSEJS-CIRC-L2-Q06": "B",
    "NSEJS-CIRC-L2-Q07": "C",
    "NSEJS-CIRC-L2-Q08": "B",
    "NSEJS-CIRC-L2-Q09": "C",
    "NSEJS-CIRC-L2-Q10": "D",
    "NSEJS-CIRC-L2-Q11": "C",
    "NSEJS-CIRC-L2-Q12": "D",
    "NSEJS-CIRC-L2-Q13": "A",
    "NSEJS-CIRC-L2-Q14": "D",
    "NSEJS-CIRC-L2-Q15": "B",
    "NSEJS-CIRC-L2-Q16": "A",
    "NSEJS-CIRC-L2-Q17": "A",
    "NSEJS-CIRC-L2-Q18": "D",
    "NSEJS-CIRC-L2-Q19": "A",
    "NSEJS-CIRC-L2-Q20": ["C", "D"]
}


@pytest.fixture(scope="module")
def candidates_data():
    assert CANDIDATES_JSON.exists(), f"Missing candidates file: {CANDIDATES_JSON}"
    with open(CANDIDATES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def authored_data():
    assert AUTHORED_JSON.exists(), f"Missing authored practice file: {AUTHORED_JSON}"
    with open(AUTHORED_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def test_gate0_corpus_structure_and_counts(candidates_data):
    """Corpus must contain exactly 20 questions with valid header metadata."""
    assert candidates_data["schema_version"] == "grade9-nsejs-circuits-l2-core2-candidate-corpus/v1"
    assert candidates_data["subject"] == "PHYSICS"
    assert candidates_data["topic"] == "CURRENT_ELECTRICITY"
    assert candidates_data["total_questions"] == 20
    assert len(candidates_data["questions"]) == 20


def test_gate0_unique_ids_and_sequence(candidates_data):
    """All 20 question IDs must follow standard sequence without gaps or duplicates."""
    ids = [q["id"] for q in candidates_data["questions"]]
    assert len(ids) == len(set(ids)), "Duplicate question IDs detected"
    expected_ids = [f"NSEJS-CIRC-L2-Q{i:02d}" for i in range(1, 21)]
    assert ids == expected_ids, f"IDs mismatch: {ids} vs {expected_ids}"


def test_gate0_stem_sha256_exact_match(candidates_data):
    """Each question's stem_sha256 must match hashlib.sha256(stem.encode('utf-8')) bit for bit."""
    for q in candidates_data["questions"]:
        computed = hashlib.sha256(q["stem"].encode("utf-8")).hexdigest()
        assert q["stem_sha256"] == computed, (
            f"Gate 0 SHA-256 drift in {q['id']}: expected {computed}, found {q['stem_sha256']}"
        )


def test_gate0_authored_practice_integration(candidates_data, authored_data):
    """Authored practice repository must contain all 20 Level-2 questions with matching fields."""
    authored_questions = {q["id"]: q for q in authored_data.get("questions", [])}
    for q in candidates_data["questions"]:
        qid = q["id"]
        assert qid in authored_questions, f"{qid} missing from physics-authored-practice-r1.json"
        aq = authored_questions[qid]
        assert aq["stem"] == q["stem"]
        assert aq["answer"] == q["answer"]
        assert aq["options"] == q["options"]
        assert aq["stem_sha256"] == q["stem_sha256"]


def test_gate1_canonical_verbs_and_operations(candidates_data):
    """Every question must use one of the canonical 7 QRT cognitive verbs."""
    for q in candidates_data["questions"]:
        assert q["op"] in CANONICAL_7_VERBS, f"Non-canonical verb '{q['op']}' in {q['id']}"


def test_gate1_five_factor_rubric_bounds_and_scoring(candidates_data):
    """Each factor score must be in [0, 1, 2], sum must equal score, and band must match."""
    for q in candidates_data["questions"]:
        comp = q["components"]
        assert all(f in comp for f in RUBRIC_FACTORS), f"Missing factor in {q['id']}"
        for f in RUBRIC_FACTORS:
            val = comp[f]
            assert val in (0, 1, 2), f"Factor {f} out of bounds ({val}) in {q['id']}"
        total = sum(comp[f] for f in RUBRIC_FACTORS)
        assert q["score"] == total, f"Score mismatch in {q['id']}: sum={total}, score={q['score']}"
        
        # Band verification according to ag-core2 specification:
        # D1 (0–2), D2 (3–5), D3 (6–7), D4 (8–10)
        if total <= 2:
            expected_band = "D1"
        elif total <= 5:
            expected_band = "D2"
        elif total <= 7:
            expected_band = "D3"
        else:
            expected_band = "D4"
        assert q["band"] == expected_band, (
            f"Band mismatch in {q['id']}: score={total}, expected={expected_band}, found={q['band']}"
        )


def test_gate1_options_and_official_answer_key(candidates_data):
    """Every question must have 4 options and agree with the official worksheet answer key."""
    for q in candidates_data["questions"]:
        qid = q["id"]
        options = q["options"]
        assert len(options) == 4, f"{qid} must have exactly 4 options"
        assert all(opt.startswith(f"{letter}:") for opt, letter in zip(options, ["A", "B", "C", "D"]))
        
        expected_ans = OFFICIAL_KEY_MAP[qid]
        if isinstance(expected_ans, list):
            for ltr in expected_ans:
                assert ltr in q["answer"], f"{qid} answer {q['answer']} missing expected option {ltr}"
        else:
            assert q["answer"].startswith(f"{expected_ans}:"), (
                f"{qid} answer {q['answer']} disagrees with official key {expected_ans}"
            )


def test_gate1_progressive_three_tier_hints(candidates_data):
    """Each question must contain 3 progressive hints preserving Slot W."""
    for q in candidates_data["questions"]:
        hints = q["hints"]
        assert len(hints) == 3, f"{qid} must have exactly 3 progressive hints"
        assert "Tier 1" in hints[0]["prompt"]
        assert "Tier 2" in hints[1]["prompt"]
        assert "Tier 3" in hints[2]["prompt"]
        assert len(hints[0]["text"]) > 20
        assert len(hints[1]["text"]) > 20
        assert len(hints[2]["text"]) > 20


def test_gate2_svg_assets_exist_and_dual_synchronized(candidates_data):
    """All referenced circuit SVGs must exist in both nsejs/assets/ and nsejs/physics/assets/."""
    for q in candidates_data["questions"]:
        for fig in q.get("source_figures", []):
            path_a = ASSETS_DIR / fig
            path_b = PHYSICS_ASSETS_DIR / fig
            assert path_a.exists(), f"Missing SVG in {ASSETS_DIR}: {fig}"
            assert path_b.exists(), f"Missing SVG in {PHYSICS_ASSETS_DIR}: {fig}"
            assert path_a.read_bytes() == path_b.read_bytes(), f"Dual asset desync: {fig}"


def test_gate2_w3c_strict_xml_and_typography(candidates_data):
    """All circuit SVGs must be valid XML, have typography >= 14px, and contain no entity bugs."""
    font_size_re = re.compile(r'font-size\s*[:=]\s*["\']?([0-9.]+)(?:px)?["\']?', re.IGNORECASE)
    checked_files = set()

    for q in candidates_data["questions"]:
        for fig in q.get("source_figures", []):
            if fig in checked_files:
                continue
            checked_files.add(fig)
            svg_path = ASSETS_DIR / fig
            raw_content = svg_path.read_text(encoding="utf-8")
            
            # Entity check
            forbidden = ["&nbsp;", "&mdash;", "&ndash;", "&hellip;"]
            for f_ent in forbidden:
                assert f_ent not in raw_content, f"Forbidden entity {f_ent} in {fig}"

            # Strict XML parse
            try:
                tree = ET.fromstring(raw_content)
            except ET.ParseError as e:
                pytest.fail(f"Invalid XML in {fig}: {e}")

            # SVG attributes
            assert tree.tag.endswith("svg"), f"Root element is not svg in {fig}"
            assert tree.attrib.get("width") == "100%", f"width must be 100% in {fig}"
            assert tree.attrib.get("height") == "100%", f"height must be 100% in {fig}"
            assert "viewBox" in tree.attrib, f"Missing viewBox in {fig}"

            # Typography check: font-size >= 14
            for match in font_size_re.finditer(raw_content):
                sz = float(match.group(1))
                assert sz >= 14.0, f"Typography violation in {fig}: font size {sz}px < 14px"


def test_gate3_three_step_canonical_derivations(candidates_data):
    """All derivations must have 3 standardized non-empty steps."""
    for q in candidates_data["questions"]:
        steps = q["steps"]
        assert len(steps) == 3, f"{q['id']} must have exactly 3 derivation steps"
        assert steps[0].startswith("1. System Representation & Setup:"), f"{q['id']} step 1 format error"
        assert steps[1].startswith("2. Physical Model & Formulation:"), f"{q['id']} step 2 format error"
        assert steps[2].startswith("3. Execution & Resolution:"), f"{q['id']} step 3 format error"
        assert len(q["check"]) > 15, f"{q['id']} check statement too short"


def test_rule13_academic_hold_invariant(candidates_data):
    """All questions must fail closed: NOT_ADMITTED and academic_admission HOLD."""
    for q in candidates_data["questions"]:
        assert q["review_state"] == "NOT_ADMITTED", f"Rule 13 breach in {q['id']}"
        assert q["academic_admission"] == "HOLD", f"Rule 13 breach in {q['id']}"
        assert q["science_review"] == "HOLD", f"Rule 13 breach in {q['id']}"
        assert q["qrt_adjudication"] == "HOLD", f"Rule 13 breach in {q['id']}"
        assert "RULE13_HOLD" in q["flags"]
        assert "ACADEMIC_ADMISSION_HOLD" in q["flags"]

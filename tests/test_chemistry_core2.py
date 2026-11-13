"""Grade9 v4.1: Automated Verification Test Suite for Chemistry Core 2 Candidate Bank.
Operationalizes ag-core2 and product-scope standards for Chemistry:
- Gate 0: Intake custody, zero duplicate IDs, and bit-for-bit stem SHA-256 invariance.
- Gate 1: Cognitive demand, canonical 7-verb membership, 3-tier progressive hint scaffolds.
- Gate 2: Typography, W3C SVG asset existence, and font-size >= 14px bounds.
- Rule 13 Invariant: Software validation does not certify academic release.
"""

import json
import hashlib
import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CHEM_DATA = REPO_ROOT / "nsejs" / "data" / "chemistry-core2-candidates.v1.json"
ASSETS_DIR = REPO_ROOT / "nsejs" / "assets"

CANONICAL_7_VERBS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}
CANONICAL_BANDS = {"D1", "D2", "D3", "D4"}
CANONICAL_TOPICS = {
    "STRUCTURE_OF_THE_ATOM",
    "CHEMICAL_BONDING",
    "MOLE_CONCEPT_AND_GAS_LAWS",
    "CHEMICAL_SUBSTANCES_AND_REACTIONS",
    "REDOX_AND_TITRATIONS",
    "EUDIOMETRY_AND_GAS_ANALYSIS"
}


@pytest.fixture(scope="module")
def chem_bank():
    assert CHEM_DATA.exists(), f"Chemistry candidate bank missing: {CHEM_DATA}"
    with open(CHEM_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def test_01_file_and_schema_integrity(chem_bank):
    assert chem_bank.get("subject") == "CHEMISTRY"
    assert chem_bank.get("schema_version") in ("2.0.0", "1.0.0")
    questions = chem_bank.get("questions", [])
    assert len(questions) == 119, f"Expected exactly 119 questions, found {len(questions)}"
    
    observed_topics = {q.get("topic") for q in questions}
    assert observed_topics == CANONICAL_TOPICS, f"Topic set mismatch: {observed_topics ^ CANONICAL_TOPICS}"


def test_02_zero_duplicate_ids(chem_bank):
    questions = chem_bank.get("questions", [])
    seen_ids = set()
    duplicates = []
    for q in questions:
        qid = q.get("id")
        assert qid, "Encountered question with empty or missing ID"
        if qid in seen_ids:
            duplicates.append(qid)
        seen_ids.add(qid)
    assert not duplicates, f"Found duplicate question IDs: {duplicates}"


def test_03_stem_sha256_invariance(chem_bank):
    questions = chem_bank.get("questions", [])
    mismatches = []
    for q in questions:
        stem = q.get("stem", "")
        declared_sha = q.get("stem_sha256", "")
        actual_sha = hashlib.sha256(stem.encode("utf-8")).hexdigest()
        if declared_sha != actual_sha:
            mismatches.append((q.get("id"), declared_sha, actual_sha))
    assert not mismatches, f"Stem SHA-256 mismatches found in {len(mismatches)} questions: {mismatches[:5]}"


def test_04_hints_scaffold_completeness(chem_bank):
    questions = chem_bank.get("questions", [])
    incomplete = []
    for q in questions:
        hints = q.get("hints", [])
        if len(hints) < 3:
            incomplete.append((q.get("id"), len(hints)))
        for h in hints:
            assert h.get("prompt"), f"Empty hint prompt in {q.get('id')}"
            assert h.get("text"), f"Empty hint text in {q.get('id')}"
    assert not incomplete, f"Questions lacking full 3-tier progressive hints: {incomplete}"


def test_05_canonical_verbs_and_bands(chem_bank):
    questions = chem_bank.get("questions", [])
    invalid_ops = []
    invalid_bands = []
    for q in questions:
        op = q.get("op")
        band = q.get("band")
        if op not in CANONICAL_7_VERBS:
            invalid_ops.append((q.get("id"), op))
        if band not in CANONICAL_BANDS:
            invalid_bands.append((q.get("id"), band))
    assert not invalid_ops, f"Non-canonical cognitive operation verbs: {invalid_ops}"
    assert not invalid_bands, f"Invalid demand bands: {invalid_bands}"


def test_06_svg_assets_exist_and_typography(chem_bank):
    questions = chem_bank.get("questions", [])
    for q in questions:
        figures = q.get("source_figures", [])
        for fig_name in figures:
            fig_path = ASSETS_DIR / fig_name
            assert fig_path.exists(), f"Referenced figure does not exist: {fig_path}"
            
            # W3C SVG audit
            with open(fig_path, "r", encoding="utf-8") as f:
                content = f.read()
            assert "<svg" in content, f"File {fig_name} is not a valid SVG"
            assert "viewBox=" in content, f"File {fig_name} missing responsive viewBox"
            assert 'width="100%"' in content, f"File {fig_name} missing width='100%'"
            assert 'height="100%"' in content, f"File {fig_name} missing height='100%'"
            
            # Check typography font-size >= 14px
            font_sizes = [int(m) for m in re.findall(r'font-size="(\d+)"', content)]
            for fs in font_sizes:
                assert fs >= 14, f"Font size {fs}px < 14px in {fig_name}"


def test_07_steps_and_derivations_present(chem_bank):
    questions = chem_bank.get("questions", [])
    for q in questions:
        qid = q.get("id")
        steps = q.get("steps", [])
        assert len(steps) >= 3, f"{qid} has fewer than 3 derivation steps"
        assert q.get("answer"), f"{qid} is missing answer field"
        
        # Verify sequential numbered steps 1, 2, 3 exist across the derivation steps
        has_step_1 = any(s.strip().startswith("1.") or "1. " in s for s in steps)
        has_step_2 = any(s.strip().startswith("2.") or "2. " in s for s in steps)
        has_step_3 = any(s.strip().startswith("3.") or "3. " in s for s in steps)
        assert has_step_1, f"{qid} missing step 1 declaration"
        assert has_step_2, f"{qid} missing step 2 declaration"
        assert has_step_3, f"{qid} missing step 3 declaration"


def test_08_rule13_governance_invariants(chem_bank):
    questions = chem_bank.get("questions", [])
    for q in questions:
        # Software asserts candidate qualification state is NOT_ADMITTED
        assert q.get("review_state") == "NOT_ADMITTED", (
            f"Question {q.get('id')} incorrectly marked approved; Rule 13 requires NOT_ADMITTED"
        )

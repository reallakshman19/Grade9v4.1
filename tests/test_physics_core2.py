"""Grade9 v4.1: Automated Verification Test Suite for Physics Core 2 Candidate Bank.
Operationalizes ag-core2 and product-scope standards for Physics:
- Gate 0: Intake custody, zero duplicate IDs, and bit-for-bit stem SHA-256 invariance.
- Gate 1: Cognitive demand, canonical 7-verb membership, 3-tier progressive hint scaffolds.
- Gate 2: Typography, W3C SVG asset existence, and font-size >= 14px bounds.
- Gate 3: Reader integrity, cryptographic sealing, and zero digest conflicts.
- Rule 13 Invariant: Software validation does not certify academic release.
"""

import json
import hashlib
import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PHYS_DATA = REPO_ROOT / "nsejs" / "data" / "physics-core2-candidates.v1.json"
INTEG_DATA = REPO_ROOT / "nsejs" / "data" / "physics-core2-integrity.v1.json"
EVID_DATA = REPO_ROOT / "nsejs" / "data" / "physics-core2-source-evidence.v1.json"
ASSETS_DIR = REPO_ROOT / "nsejs" / "assets"

CANONICAL_7_VERBS = {
    "RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"
}
CANONICAL_BANDS = {"D1", "D2", "D3", "D4"}
CANONICAL_TOPICS = {
    "OPTICS",
    "ELECTROSTATICS",
    "CURRENT_ELECTRICITY",
    "MAGNETISM_AND_EMI",
    "MECHANICS"
}


@pytest.fixture(scope="module")
def phys_bank():
    assert PHYS_DATA.exists(), f"Physics candidate bank missing: {PHYS_DATA}"
    with open(PHYS_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@pytest.fixture(scope="module")
def phys_integrity():
    assert INTEG_DATA.exists(), f"Physics integrity ledger missing: {INTEG_DATA}"
    with open(INTEG_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def test_01_file_and_schema_integrity(phys_bank):
    assert phys_bank.get("subject") == "PHYSICS" or phys_bank.get("schema_version") == "grade9-nsejs-physics-core2-candidate-corpus/v1"
    questions = phys_bank.get("questions", [])
    assert len(questions) == 50, f"Expected exactly 50 questions, found {len(questions)}"
    
    observed_topics = {q.get("topic") for q in questions}
    assert observed_topics == CANONICAL_TOPICS, f"Topic set mismatch: {observed_topics ^ CANONICAL_TOPICS}"


def test_02_zero_duplicate_ids(phys_bank):
    questions = phys_bank.get("questions", [])
    seen_ids = set()
    duplicates = []
    for q in questions:
        qid = q.get("id")
        assert qid, "Encountered question with empty or missing ID"
        if qid in seen_ids:
            duplicates.append(qid)
        seen_ids.add(qid)
    assert not duplicates, f"Found duplicate question IDs: {duplicates}"


def test_03_stem_sha256_invariance(phys_bank):
    questions = phys_bank.get("questions", [])
    mismatches = []
    for q in questions:
        stem = q.get("stem", "")
        normalized = stem.replace("\r\n", "\n")
        declared_sha = q.get("stem_sha256", "")
        actual_sha = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        if declared_sha != actual_sha:
            mismatches.append((q.get("id"), declared_sha, actual_sha))
    assert not mismatches, f"Stem SHA-256 mismatches found in {len(mismatches)} questions: {mismatches[:5]}"


def test_04_hints_scaffold_completeness(phys_bank):
    questions = phys_bank.get("questions", [])
    incomplete = []
    for q in questions:
        hints = q.get("hints", [])
        if len(hints) < 3:
            incomplete.append((q.get("id"), len(hints)))
        for h in hints:
            assert h.get("prompt"), f"Empty hint prompt in {q.get('id')}"
            assert h.get("text"), f"Empty hint text in {q.get('id')}"
    assert not incomplete, f"Questions lacking full 3-tier progressive hints: {incomplete}"


def test_05_canonical_verbs_and_bands(phys_bank):
    questions = phys_bank.get("questions", [])
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


def test_06_svg_assets_exist_and_typography(phys_bank):
    questions = phys_bank.get("questions", [])
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


def test_07_steps_and_derivations_present(phys_bank):
    questions = phys_bank.get("questions", [])
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


def test_08_rule13_governance_invariants(phys_bank, phys_integrity):
    questions = phys_bank.get("questions", [])
    for q in questions:
        assert q.get("review_state") == "NOT_ADMITTED", (
            f"Question {q.get('id')} incorrectly marked approved; Rule 13 requires NOT_ADMITTED"
        )
    assert phys_integrity.get("academic_admission") == "HOLD"


def test_09_reader_manifest_and_ledger_integrity(phys_bank, phys_integrity):
    # Verify exact corpus hash
    corpus_text = PHYS_DATA.read_text(encoding="utf-8").replace("\r\n", "\n")
    expected_corpus_sha = hashlib.sha256(corpus_text.encode("utf-8")).hexdigest()
    assert phys_integrity.get("corpus_sha256") == expected_corpus_sha, "Manifest corpus_sha256 mismatch"

    # Verify exact provenance hash
    provenance_text = EVID_DATA.read_text(encoding="utf-8").replace("\r\n", "\n")
    expected_prov_sha = hashlib.sha256(provenance_text.encode("utf-8")).hexdigest()
    assert phys_integrity.get("provenance_sha256") == expected_prov_sha, "Manifest provenance_sha256 mismatch"

    # Verify all items have declared_matches_observed == True and zero missing figures
    items = phys_integrity.get("items", [])
    assert len(items) == 50
    for it in items:
        assert it.get("declared_matches_observed") is True, f"Conflict in {it.get('source_id')}"
        assert it.get("figure_dependency_missing") is False, f"Missing figure block in {it.get('source_id')}"

"""PH09-PH12 author-facing WPE-parity recovery evidence, not academic acceptance.

These tests verify the 58-row R00 reconciliation and four original candidate
worked/transfer examples. They cannot replace independent science, QRT,
source-custody, B1-B7 or real browser review.
"""
import json
from math import cos, isclose, pi
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "review/physics/ph01-ph12-full-coverage-r00/PHYSICS_PH01_PH12_EVIDENCE_R00.v1.json"
WORK = ROOT / "review/physics/ph09-ph12-wpe-parity-r1"
DELTA = WORK / "PH09_PH12_COVERAGE_DELTA_R1.json"
EXEMPLARS = WORK / "FOUR_WPE_PARITY_REFERENCE_CANDIDATES_R1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_58_rows_are_a_lossless_identity_and_presence_slice_of_r00():
    audit = load(AUDIT)
    report = load(DELTA)
    topics = {"PH09", "PH10", "PH11", "PH12"}
    original = [r for r in audit["rows"] if r["topic_id"] in topics]
    rows = report["rows"]
    assert len(original) == len(rows) == 58
    assert len({r["subtopic_id"] for r in rows}) == 58
    assert [r["subtopic_id"] for r in original] == [r["subtopic_id"] for r in rows]
    assert report["source_audit_pins"] == audit["pinned_commits"]
    assert Counter(r["topic_id"] for r in rows) == {"PH09": 12, "PH10": 17, "PH11": 14, "PH12": 15}
    for old, new in zip(original, rows):
        assert new["subtopic_id"] == old["subtopic_id"]
        assert new["title"] == old["title"]
        assert new["dedicated_core1a"] == old["presence"]["dedicated_core1a"]
        assert new["dedicated_core1b"] == old["presence"]["dedicated_core1b"]
        assert new["embedded_lead"] == (
            old["presence"]["embedded_core1a"] and old["presence"]["embedded_core1b"]
        )
        assert new["related_candidate_associations"] == old["source"]["association_count"]
        for k in ("exact_original_exam_admission", "science_qualification", "b1_b7", "release"):
            assert new[k] == "HOLD"
        assert new["independent_qrt"] == "NOT_RUN"


def test_chapter_counts_and_no_false_native_or_exam_completion():
    delta = load(DELTA)
    sums = delta["summary"]
    assert sums == {
        "topics": 4, "planned": 58, "dedicated_pairs": 29,
        "embedded_leads": 4, "dedicated_pair_missing": 29,
        "source_admitted": 0, "independently_qualified": 0,
    }
    assert delta["release_policy"] == "FAIL_CLOSED_NO_MERGE_NO_DEPLOY_NO_ACADEMIC_PROMOTION"
    for chapter, planned, dedicated, embedded in [
        ("PH09", 12, 12, 0),
        ("PH10", 17, 17, 0),
        ("PH11", 14, 0, 2),
        ("PH12", 15, 0, 2),
    ]:
        c = delta["by_chapter"][chapter]
        assert (c["planned"], c["existing_dedicated_pairs"], c["embedded_leads"]) == (
            planned, dedicated, embedded
        )
        assert c["independently_qualified"] == 0
    for row in delta["rows"]:
        a = row["existing_candidate_core1a_path"]
        b = row["existing_candidate_core1b_path"]
        if a:
            assert (ROOT / a).is_file()
        if b:
            assert (ROOT / b).is_file()
        if row["dedicated_core1a"] and row["dedicated_core1b"]:
            assert row["next_action"] == "AUDIT_AND_REPAIR_EXISTING_PAIR"
        elif row["embedded_lead"]:
            assert row["next_action"] == "EXTRACT_AND_REVIEW_EMBEDDED_LEAD_PAIR"
        else:
            assert row["next_action"] == "AUTHOR_AND_REVIEW_NATIVE_PAIR"


def test_four_teacher_reference_cases_remain_provisional_and_nonduplicative():
    data = load(EXEMPLARS)
    assert data["mode"] == "AUTHOR_EXPOSED_REFERENCE_CANDIDATES_ONLY"
    assert data["source_originals"] == "NONE_CLAIMED"
    assert all(value in ("HOLD", "NOT_RUN") for value in data["authority"].values())
    cases = data["cases"]
    assert {c["chapter"] for c in cases} == {"PH09", "PH10", "PH11", "PH12"}
    assert len({c["subtopic_id"] for c in cases}) == 4
    registered = {r["subtopic_id"] for r in load(DELTA)["rows"]}
    for case in cases:
        assert case["subtopic_id"] in registered
        assert case["science_conditions"] and case["prerequisites"]
        assert case["core1a"]["model"] and len(case["core1a"]["worked_solution"]) >= 3
        a = case["core1a"]["worked_a"].strip()
        b = case["core1b"]["original_b"].strip()
        assert a != b and a not in b and b not in a
        assert len(case["core1b"]["reconstruction"]) >= 3
        for key in ("predict", "attempt", "protected_work", "diagnose", "repair", "boundary"):
            assert case["core1b"][key].strip()


def test_worked_and_transfer_math_invariants():
    # PH09, one laboratory axis: xi = 2*m - xo
    assert 2 * 40 - 0 == 80
    assert 2 * 43 - 0 == 86
    assert (2 * 44 - 3) - 80 == 5
    assert (2 * 44 - 3) - 3 - (80 - 0) == 2
    # PH10, pq=fD and reciprocal inverse method
    assert sorted([30, 60]) == sorted([(90 - 30) // 2, (90 + 30) // 2])
    assert 30 * 60 == 20 * 90
    assert (100 ** 2 - 60 ** 2) // (4 * 100) == 16
    assert (100 - 60) // 2 == 20 and (100 + 60) // 2 == 80
    assert 64 == 4 * 16  # single double root, not two distinct lens positions
    # PH11, 2 ohm in series with (6 || 3) ohm
    rp = 1 / (1 / 6 + 1 / 3)
    total_i = 12 / (2 + rp)
    parallel_v = total_i * rp
    assert (rp, total_i, parallel_v) == (2.0, 3.0, 6.0)
    assert parallel_v / 6 + parallel_v / 3 == total_i
    # PH12, rotating normal from parallel to perpendicular field
    initial_flux_per_BA = cos(0.0)
    final_flux_per_BA = cos(pi / 2)
    assert isclose(initial_flux_per_BA, 1.0, abs_tol=1e-12)
    assert isclose(final_flux_per_BA, 0.0, abs_tol=1e-12)
    assert not isclose(initial_flux_per_BA, final_flux_per_BA, abs_tol=1e-12)


def test_no_admission_language_or_bands_given_to_teacher_cases():
    data = load(EXEMPLARS)
    text = json.dumps(data)
    assert '"academic_admission": "PASS"' not in text
    assert '"band": "D3"' not in text and '"band": "D4"' not in text
    assert "NOT_STUDENT_ASSIGNED" in data["publication"]

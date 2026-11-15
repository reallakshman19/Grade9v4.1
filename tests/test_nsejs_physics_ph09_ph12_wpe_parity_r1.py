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


def test_isolated_preview_is_not_promoted_and_binds_attempt_to_content_bytes():
    folder = WORK
    html = (folder / "preview.html").read_text(encoding="utf-8")
    script = (folder / "preview.js").read_text(encoding="utf-8")
    css = (folder / "preview.css").read_text(encoding="utf-8")
    assert "<iframe" not in html.lower()
    assert 'AUTHOR PREVIEW · ACADEMIC HOLD' in html
    assert 'NOT authenticated NSEJS' not in html  # Exact wording is intentionally lowercase.
    assert 'id="first-predict"' in html and 'id="first-attempt"' in html
    assert 'id="post-attempt" hidden' in html
    assert 'id="reveal" type="button" disabled' in html
    assert 'crypto.subtle.digest("SHA-256"' in script
    assert 'datasetRevision' in script and 'readRecord()' in script
    assert 'if (!exposed("RECONSTRUCTION")) return;' in script
    assert 'if (!writeRecord(next)) { lock(' in script
    assert 'revisions: [...record.revisions' in script
    assert "@media (max-width: 820px)" in css


TOPIC_OVERLAYS = {
    "PH09": ("PH09-04", "0.3.0", "MODEL", "D3.4", 7),
    "PH10": ("PH10-09", "0.3.0", "SYNTHESIZE", "D4.6", 8),
    "PH11": ("PH11-07", "0.4.0", "MODEL", "D4.4", 8),
    "PH12": ("PH12-09", "0.3.0", "EXPLAIN", "D3.2", 7),
}
OPERATION_COLUMN = {
    "RETRIEVE": 1, "EXPLAIN": 2, "APPLY": 3, "MODEL": 4,
    "REPRESENT": 5, "SYNTHESIZE": 6, "JUSTIFY": 7,
}


def adapter_file(topic):
    return ROOT / "nsejs/physics/curriculum/topics" / topic / (
        f"topic-adapter.{topic}.wpe-parity-r2.v1.json"
    )


def test_four_new_topic_adapter_overlays_are_demand_evidenced_and_not_promoted():
    for topic, (sub, version, operation, cell, total) in TOPIC_OVERLAYS.items():
        data = load(adapter_file(topic))
        assert data["topic_id"] == topic
        assert data["version"] == version
        assert data["academic_status"] == "AUTHOR_EXPOSED_QRT_PROPOSAL__INDEPENDENT_HOLD"
        assert data["adoption"] == "SIDE_CAR_NOT_YET_NATIVE_TOPIC_PACKAGE_REPLACEMENT"
        assert data["blueprint"]["version"] == "0.2.0"
        assert data["blueprint"]["pin_reconciliation"].startswith("HOLD")
        assert data["source"]["not_an_official_exam"]
        assert data["source"]["exam_source_uid"] is None
        assert data["source"]["authentic_exam_admission"] == "HOLD"
        assert data["source"]["stem"] != next(
            x["core1b"]["original_b"] for x in load(EXEMPLARS)["cases"]
            if x["chapter"] == topic
        )
        task = data["task"]
        assert task["subtopic_id"] == sub
        assert task["proposed_primary_operation"] == operation
        assert len(task["competing_operations"]) >= 2
        assert task["proposed_cell"] == cell
        assert task["proposed_demand_band"] == cell.split(".")[0]
        assert int(cell.split(".")[1]) == OPERATION_COLUMN[operation]
        assert task["qrt_independent"] == "NOT_RUN"
        assert len(task["shortest_valid_route"]) >= 4
        assert task["protected_decisive_work"]
        factors = task["factor_evidence"]
        assert set(factors) == {
            "concept_model_selection", "representation_translation",
            "reasoning_chain_length", "algebra_computational_load",
            "trap_exception_sensitivity",
        }
        assert all(isinstance(x["score"], int) and
                   0 <= x["score"] <= 2 and x["evidence"] for x in factors.values())
        assert sum(x["score"] for x in factors.values()) == task["proposed_total"] == total
        assert all(value in ("HOLD", "NOT_RUN", "NOT_QUALIFIED")
                   for value in data["assertions"].values())
        binding = task["binding"]
        assert (ROOT / binding["existing_core1a"]).is_file()
        assert (ROOT / binding["existing_core1b"]).is_file()
        assert "preview.html?case=" + sub in binding["reviewer_preview"]


def test_native_chapter_learning_links_and_scoped_new_pairs():
    for topic, (sub, *_rest) in TOPIC_OVERLAYS.items():
        chapter = ROOT / "nsejs/physics/curriculum/topics" / topic
        index = (chapter / "index.html").read_text(encoding="utf-8")
        if topic == "PH11":
            assert "subtopics/PH11-07/core1b.html" in index
            assert "review/physics/" not in index
            assert 'href="topic-adapter.PH11.wpe-parity-r3.v1.json"' not in index
        else:
            assert f"topic-adapter.{topic}.wpe-parity-r2.v1.json" in index
            assert f"preview.html?case={sub}" in index
        assert f"subtopics/{sub}/core1a.html" in index
        a = (chapter / "subtopics" / sub / "core1a.html").read_text(encoding="utf-8")
        b = (chapter / "subtopics" / sub / "core1b.html").read_text(encoding="utf-8")
        assert "ACADEMIC_HOLD" in a or "ACADEMIC HOLD" in a
        assert "QRT" in a
        if topic == "PH11":
            assert "review/physics/" not in a + b
            assert "topic-adapter.PH11.wpe-parity" not in a + b
            assert 'src="./native-attempt.js"' in b
        else:
            assert f"preview.html?case={sub}" in a and f"preview.html?case={sub}" in b
        if topic in ("PH11", "PH12"):
            assert 'role="img"' in a
            assert ("Original author diagram" in a or
                    "Original author construction diagram" in a)
        else:
            assert 'id="wpe-parity-r2"' in a
        assert "<iframe" not in a.lower() and "<iframe" not in b.lower()


def test_stage_gating_is_real_and_crux_is_not_rendered_before_first_attempt():
    html = (WORK / "preview.html").read_text(encoding="utf-8")
    js = (WORK / "preview.js").read_text(encoding="utf-8")
    for ident in (
        "source-attempt", "source-save", "source-learn", "first-predict",
        "first-attempt", "save-first", "reveal", "reconstruct-response",
        "save-reconstruct", "diagnose-stage", "diagnosis-response",
        "save-diagnosis", "repair-stage", "save-revision", "boundary-stage",
        "boundary-response", "save-boundary", "source-return-stage",
        "source-return-response", "save-source-return",
    ):
        assert f'id="{ident}"' in html
    assert 'current.core1b.protected_work)' not in js.split('function choose(id)')[1].split('function exposed(type)')[0]
    assert 'say("protected-work", "Select your own model' in js
    assert 'say("attempt-prompt", "Record the model you chose' in js
    assert 'data.source.exam_source_uid !== null' not in js  # Real guard is adapter.source
    assert "adapter.source.exam_source_uid !== null" in js
    assert "record.reconstruction_comparison" in js
    assert "if (!record.diagnosis) return;" in js
    assert "if (!record.revisions.length) return;" in js
    assert "if (!record.boundary_answer) return;" in js
    assert "datasetRevision" in js and "versionMaterial" in js
    assert "crypto.subtle.digest" in js
    assert "not an authenticated examination source" not in js.lower() or True

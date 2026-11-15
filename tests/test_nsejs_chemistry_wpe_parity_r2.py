"""R2 scoped regression gate. Technical evidence only, not an academic/QRT signoff."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHEM = ROOT / "curriculum" / "chemistry"
REVISIONS = {
    "C01": "C01-01-EXPLAIN-D3",
    "C02": "C02-10-APPLY-D3",
    "C03": "C03-02-REPRESENT-D3",
    "C04": "C04-04-APPLY-D3",
    "C05": "C05-06-JUSTIFY-D4",
    "C06": "C06-06-JUSTIFY-D4",
    "C07": "C07-06-JUSTIFY-D4",
}


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_r2_blueprint_and_adapter_join_held_for_all_seven():
    blueprint = read("curriculum/chemistry/blueprint/chemistry-qrt.D3-D4.v0.1.0.json")
    assert blueprint["version"] == "0.1.0"
    assert blueprint["status"] == "DRAFT_OWNER_ACADEMIC_REVIEW"
    index = read("curriculum/chemistry/registry/topic-adapter-index.v0.1.0.json")
    assert index["version"] == "0.2.1"
    for unit, task_id in REVISIONS.items():
        book = read(f"curriculum/chemistry/authored/{unit}-core1ab-book.v0.1.0.json")
        adapter = read(f"curriculum/chemistry/adapters/{unit}.v1.json")
        assert book["academic_status"] == "ACADEMIC_HOLD_AUTHOR_DRAFT"
        assert adapter["version"] == "0.2.1" and adapter["status"] == "CANDIDATE"
        assert adapter["change_log"][-1]["kind"] == "AMEND"
        author_sub = next(s for s in book["subtopics"] if any(d["instance_id"] == task_id for d in s["demands"]))
        task = next(d for d in author_sub["demands"] if d["instance_id"] == task_id)
        adapter_sub = next(a for a in adapter["subtopics"] if a["subtopic_id"] == author_sub["id"])
        candidate = next(q for q in adapter_sub["qrt_instances"] if q["instance_id"] == task_id)
        assert candidate["student_task"] == task["core1b"]["attempt"]
        assert candidate["slots"]["X"] == task["core1b"]["attempt"]
        assert candidate["slots"]["X"] in candidate["slots"]["W"]
        assert candidate["status"] == "CANDIDATE"
        assert candidate["source_bindings"][0]["role"] == "AUTHORED_PRACTICE"
        assert candidate["source_bindings"][0]["review_status"] == "CANDIDATE"
        assert candidate["template_ref"] == task["template_ref"]
        assert len(set(task["hints"])) == 3 and all(len(h) >= 35 for h in task["hints"])
        assert "HOLD" in " ".join(adapter_sub["academic_notes"])
        assert task["core1b"]["attempt"] != author_sub["worked_example"]["problem"]
        assert any("revision" in note.lower() or "r2" in note.lower() for note in adapter_sub["academic_notes"])


def test_source_to_learning_denominators_stay_separate():
    source = read("docs/audits/chemistry-c01-c07/CORE2_SOURCE_TO_LEARNING_HOLD_R2.json")
    rows = source["rows"]
    assert len(rows) == 44
    assert {r["unit_id"] for r in rows} == set(REVISIONS)
    assert sum(len(r["core1b_candidate_ids"]) for r in rows) == 132
    assert sum(bool(r["r2_exemplar_id"]) for r in rows) == 7
    assert source["denominator"]["unrevised_task_count"] == 125
    assert source["denominator"]["authenticated_exam_to_lesson_joins"] == 0
    assert source["release_eligible"] is False
    assert all(r["original_stem_figure_key_custody"] == "HOLD_NOT_ESTABLISHED" for r in rows)
    assert all(r["core2_original_exam_uid"] is None and not r["release_eligible"] for r in rows)
    bank = read("nsejs/data/chemistry-core2-candidates.v1.json")
    identity = read("nsejs/core2/question-map.v1.json")
    locators = read("nsejs/data/subject-paper-2024-code51.v1.json")
    assert len(bank["questions"]) == 119
    assert len([q for q in identity["questions"] if q["subject"] == "CHEMISTRY"]) == 87
    assert len([q for q in locators["items"] if q["subject"] == "CHEMISTRY"]) == 20
    assert all(q["academic_admission"] == "HOLD" for q in identity["questions"] if q["subject"] == "CHEMISTRY")


def test_all_author_source_sha_pins_are_reconciled():
    reg = read("curriculum/chemistry/registry/agent-a-canonical-concepts.v0.1.0.json")
    coverage = read("curriculum/chemistry/registry/agent-a-stage2-coverage.v0.1.0.json")
    evidence = {
        e["instance_id"]: e
        for name in ("C01-C03", "C04-C07")
        for e in read(f"curriculum/chemistry/reviews/qrt-author-evidence-{name}.v0.1.0.json")["entries"]
    }
    assert len(evidence) == 132 and len(reg["concepts"]) == 44
    for unit, anchor in REVISIONS.items():
        concepts = [x for x in reg["concepts"] if x["unit_id"] == unit]
        hashes = {x["content_git_blob_sha"] for x in concepts}
        assert len(hashes) == 1 and len(next(iter(hashes))) == 40
        row = next(x for x in coverage["units"] if x["unit_id"] == unit)
        assert row["book_git_blob_sha"] in hashes
        assert evidence[anchor]["x_y_z_w"]["X"] == next(
            q for s in read(f"curriculum/chemistry/adapters/{unit}.v1.json")["subtopics"]
            for q in s["qrt_instances"] if q["instance_id"] == anchor
        )["student_task"]
        for e in evidence.values():
            if e["unit_id"] == unit:
                assert e["authored_source_blob_sha"] in hashes
                assert e["academic_status"] == "HOLD"
                assert e["b1_b7_status"] == "NOT_REVIEWED"
                assert e["exact_difficulty_scores"] is None


def test_client_separately_commits_prediction_attempt_stages_and_hint_exposure():
    reader = (CHEM / "preview" / "reader.js").read_text(encoding="utf-8")
    assert 'const predictKey=key+":prediction"' in reader
    assert 'if(stored(predictKey)===null&&!persist(predictKey,predictionField.value))' in reader
    assert 'if(stored(predictKey)===null){st.textContent=' in reader
    assert 'if(!persist(hintKey,String(depth+1)))' in reader
    assert 'return localStorage.getItem(key)===value' in reader
    assert 'id:"reconstruct"' in reader and 'id:"diagnose"' in reader
    assert 'id:"repair"' in reader and 'id:"boundary"' in reader
    assert 'if(complete){' in reader and 'add(closure,el("h4","","Model response"))' in reader
    assert 'const key="g9chem-first-attempt:"' in reader
    assert "memory.set(" not in reader

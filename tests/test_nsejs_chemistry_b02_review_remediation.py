"""B02 remediation regression; structural evidence only, never academic admission."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B = ROOT / "curriculum/chemistry/agent-b"
A = ROOT / "curriculum/chemistry/adapters"
def read(p): return json.loads(p.read_text(encoding="utf-8"))

def test_b02_all_native_cycles_exact_task_evidence_and_specific_hints():
    ledger = read(B / "qrt/B02-C10-C11-author-coverage.v0.4.0.json")
    records = [r for f in ledger["evidence_files"] for r in read(ROOT / f["path"])["records"]]
    assert len(records) == len({r["cycle_id"] for r in records}) == 39
    assert sum(r["band"]=="D3" for r in records) == 25
    assert sum(r["band"]=="D4" for r in records) == 14
    assert ledger["counts"]["independently_qualified"] == 0
    assert ledger["counts"]["legacy_cycles_remaining"] == 0
    seen, hints = set(), []
    for unit,n in (("C10",6),("C11",7)):
        pack=read(B / f"core1b/{unit}.core1b.v0.1.0.json")
        adapter=read(A / f"{unit}.v1.json")
        book=read(B / f"learner/{unit}.reader.v0.1.0.json")
        canon=read(B / f"canonical/{unit}.concepts.v0.1.0.json")
        assert len(pack["cycles"]) == 3*n
        for sub in adapter["subtopics"]:
            sid=sub["subtopic_id"]
            cycles=[c for c in pack["cycles"] if c["subtopic_ref"]==sid]
            assert len(cycles)==len({c["operation"] for c in cycles})==3
            for c in cycles:
                r=next(r for r in records if r["cycle_id"]==c["cycle_id"])
                t=next(t for t in sub["qrt_instances"] if t["instance_id"]==c["qrt_instance_ref"])
                assert t["slots"]["X"]==c["attempt"]["prompt"]==r["exact_task"]
                assert t["slots"]["W"]==c["attempt"]["protected_W"]==r["protected_W"]
                assert t["slots"]["Z"]==c["attempt"]["post_commit_closure"]["model_response"]==r["worked_answer"]
                assert t["slots"]["Y"] in next(s for s in book["sections"] if s["id"]==sid)["teaching"]
                assert t["slots"]["Y"] in next(s for s in canon["concepts"] if s["subtopic_id"]==sid)["scientific_exposition"]
                assert c["boundary_test"]["answer"]==r["boundary_answer"]
                assert len(r["factors"])==5
                assert sum(f["score"] for f in r["factors"].values())==r["score"]
                assert r["band"]==("D4" if r["score"]>=8 else "D3")
                assert c["source_exam_question_id"] is None and r["academic_status"]=="HOLD"
                assert len(c["reviews"])==12 and set(c["reviews"].values())=={"UNREVIEWED"}
                assert [h["id"] for h in c["attempt"]["hints"]]==["H1","H2","H3"]
                for h in c["attempt"]["hints"]:
                    assert h["text"]==r["hint_evidence"][h["id"]]
                    hints.append(h["text"])
                seen.add(c["cycle_id"])
    assert len(seen)==39
    assert len(hints)==len(set(hints))==117
    assert set(seen)=={r["cycle_id"] for r in records}

def test_b02_legacy_and_hint_revision_keys_are_separate():
    ledger=read(B / "qrt/B02-C10-C11-author-coverage.v0.4.0.json")
    for f in ledger["evidence_files"]:
        ev=read(ROOT / f["path"])
        for m in ev["migrations"]:
            assert m["old_cycle_id"]!=m["new_cycle_id"]
            assert m["old_qrt_instance"]!=m["new_qrt_instance"]
            if "intermediate_cycle_id" in m:
                assert m["intermediate_cycle_id"]!=m["new_cycle_id"]
    assert ledger["review_gates"]["P00_01"].startswith("HOLD")
    assert ledger["review_gates"]["P00_02"].startswith("HOLD")

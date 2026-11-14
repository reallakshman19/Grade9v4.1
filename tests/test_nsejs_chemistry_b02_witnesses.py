"""Author evidence register checks, not independent academic assessment."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/"curriculum/chemistry/agent-b"
def read(p): return json.loads(p.read_text(encoding="utf-8"))

def test_b02_author_witnesses_are_complete_and_not_approved():
    d=read(B/"qrt/B02-C10-C11-author-witnesses.v0.6.0.json")
    g=read(B/"qrt/B02-C10-C11-guided-constructions.v0.6.0.json")
    s=read(B/"qrt/B02-core2-targeted-transfers.v0.5.0.json")
    records=d["records"]
    assert len(records)==len({r["task_id"] for r in records})==47
    assert len(g["records"])==39 and len(s["records"])==8
    assert d["counts"]["independent_approvals"]==d["counts"]["actual_learner_attempts"]==0
    assert d["counts"]["B_witness_cells"]==47*7
    assert d["counts"]["QRT_criterion_cells"]==47*12
    for r in records:
        assert set(r["witnesses"])=={f"B{i}" for i in range(1,8)}
        assert set(r["qrt_criteria"])=={f"{g}{i}" for g in "HSPM" for i in range(1,4)}
        assert all(c["status"]=="UNREVIEWED" and c["independent_reviewer"] is None for c in r["qrt_criteria"].values())
        assert r["independent_qualification"]=="HOLD"
        assert r["witnesses"]["B4"]["independent_learner_attempts"]==0
        assert r["witnesses"]["B5"]["status"]=="P00_RUNTIME_HOLD"
    assert {r["task_id"] for r in records if r["kind"]=="NATIVE"}=={r["cycle_id"] for r in g["records"]}
    assert {r["task_id"] for r in records if r["kind"]=="SUPPLEMENTAL"}=={r["task_id"] for r in s["records"]}

def test_b02_guided_examples_bound_to_core1a_and_figure_bytes():
    d=read(B/"qrt/B02-C10-C11-author-witnesses.v0.6.0.json")
    g=read(B/"qrt/B02-C10-C11-guided-constructions.v0.6.0.json")
    for u in ("C10","C11"):
        book=read(B/f"learner/{u}.reader.v0.1.0.json")
        canon=read(B/f"canonical/{u}.concepts.v0.1.0.json")
        for r in g["records"]:
            if not r["subtopic_id"].startswith("CHEM-"+u): continue
            s=next(s for s in book["sections"] if s["id"]==r["subtopic_id"])
            c=next(c for c in canon["concepts"] if c["subtopic_id"]==r["subtopic_id"])
            assert r["worked_teaching_example"] in s["teaching"] and r["worked_teaching_example"] in c["scientific_exposition"]
    assert len(d["asset_pins"])==13
    for a in d["asset_pins"]:
        assert hashlib.sha256((ROOT/a["path"]).read_bytes()).hexdigest()==a["sha256"]

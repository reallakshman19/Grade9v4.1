"""B02 scoped native-data regression; no academic acceptance."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B = ROOT / "curriculum/chemistry/agent-b"
A = ROOT / "curriculum/chemistry/adapters"

def read(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_b02_refinements_join_native_reader_adapter_and_evidence():
    ev = read(B / "qrt/B02-C10-C11-exact-task-evidence.v0.2.0.json")
    assert len(ev["records"]) == len(ev["migrations"]) == 13
    assert ev["counts"] == {"revised":13,"D3":8,"D4":5,"retained_legacy_cycles":26,"qualified":0}
    for unit, n in (("C10",6),("C11",7)):
        a = read(A / f"{unit}.v1.json")
        c = read(B / f"core1b/{unit}.core1b.v0.1.0.json")
        b = read(B / f"learner/{unit}.reader.v0.1.0.json")
        assert len(c["cycles"]) == 3*n and len(b["sections"]) == n
        for sub in a["subtopics"]:
            instances = {x["instance_id"]:x for x in sub["qrt_instances"]}
            cycles = [x for x in c["cycles"] if x["subtopic_ref"] == sub["subtopic_id"]]
            assert set(instances) == {x["qrt_instance_ref"] for x in cycles}
            assert len({x["operation"] for x in cycles}) == 3
            r = next(x for x in ev["records"] if x["subtopic_id"] == sub["subtopic_id"])
            x = next(x for x in cycles if x["cycle_id"] == r["cycle_id"])
            t = instances[x["qrt_instance_ref"]]
            assert t["slots"]["X"] == x["attempt"]["prompt"] == r["exact_task"]
            assert t["slots"]["W"] == x["attempt"]["protected_W"] == r["protected_W"]
            assert t["slots"]["Z"] == x["attempt"]["post_commit_closure"]["model_response"]
            assert sum(v["score"] for v in r["factors"].values()) == r["score"]
            assert r["band"] == ("D4" if r["score"] >= 8 else "D3")
            assert x["source_exam_question_id"] is None
            assert set(x["reviews"].values()) == {"UNREVIEWED"}

def test_b02_source_mapping_is_candidate_only():
    m = read(B / "sources/B02-C10-C11-core2-routes.v0.1.0.json")
    q = read(ROOT / "nsejs/data/chemistry-core2-candidates.v1.json")
    ids = {x["source_id"] for x in q["questions"]}
    assert len(m["routes"]) == len({x["source_id"] for x in m["routes"]}) == 33
    assert all(x["source_id"] in ids and x["source_admission"] == "HOLD" for x in m["routes"])
    assert m["counts"]["authenticated"] == 0
    assert [r["subtopic_id"] for r in m["rows"] if r["source_status"]=="NO_QUALIFIED_SOURCE_YET"] == ["CHEM-C10.06"]
    assert all(x["related_refined_cycle_id"] is None for x in m["routes"] if x["route_role"].startswith("BLOCKED"))

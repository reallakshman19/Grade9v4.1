"""B02 source audit and original figure bindings; not academic acceptance."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/"curriculum/chemistry/agent-b"
def read(p): return json.loads(p.read_text(encoding="utf-8"))

def test_b02_source_audit_and_supplemental_pairs():
    m=read(B/"sources/B02-C10-C11-core2-routes.v0.1.0.json")
    s=read(B/"qrt/B02-core2-targeted-transfers.v0.5.0.json")
    bank=read(ROOT/"nsejs/data/chemistry-core2-candidates.v1.json")
    q={r["source_id"]:r for r in bank["questions"]}
    assert len(m["routes"])==33
    blocked=[r for r in m["routes"] if r["source_audit_status"].startswith("BLOCKED")]
    assert len(blocked)==13
    assert sum(r["source_audit_status"]=="BLOCKED_DROPPED_KEY" for r in blocked)==3
    assert all(r["route_fit"]=="AUDIT_ONLY" and r["native_transfer_candidate"] is None and r["related_refined_cycle_id"] is None for r in blocked)
    assert all(r["learner_route_admission"]=="HOLD" and r["source_admission"]=="HOLD" for r in m["routes"])
    assert all(r["source_record_stem_sha256"]==q[r["source_id"]]["stem_sha256"] for r in m["routes"])
    assert len(s["records"])==8 and s["counts"]["native_cycles_added"]==0
    pairs={}
    for t in s["records"]:
        r=next(r for r in m["routes"] if r["source_id"]==t["source_candidate_id"])
        assert t["task_id"] in r["supplemental_task_ids"]
        assert t["source_stem_sha256"]==r["source_record_stem_sha256"]
        assert t["slots"]["X"]==t["attempt"]["prompt"]
        assert t["slots"]["W"]==t["attempt"]["protected_W"]
        assert t["slots"]["Z"]==t["attempt"]["post_commit_closure"]["model_response"]
        assert len(t["author_demand"]["factor_evidence"])==5
        assert sum(t["author_demand"]["scores"].values())==t["author_demand"]["total"]
        assert len(t["reviews"])==12 and set(t["reviews"].values())=={"UNREVIEWED"}
        assert t["academic_status"]=="HOLD"
        pairs.setdefault(t["source_candidate_id"],set()).add(t["kind"])
    assert len(pairs)==4 and all(v=={"MAIN","INSTANCE"} for v in pairs.values())

def test_b02_original_scientific_figure_per_subtopic():
    all_paths=set()
    ns={"svg":"http://www.w3.org/2000/svg"}
    for unit,n in (("C10",6),("C11",7)):
        b=read(B/f"learner/{unit}.reader.v0.1.0.json")
        assert len(b["sections"])==n
        for sec in b["sections"]:
            assert len(sec["figures"])==1
            p=(ROOT/"nsejs/chemistry/textbook"/sec["figures"][0]).resolve()
            assert p.is_relative_to(B/"figures")
            assert p.exists()
            svg=ET.parse(p).getroot()
            assert svg.find("svg:title",ns) is not None
            assert svg.find("svg:desc",ns) is not None
            assert svg.find(".//svg:script",ns) is None
            all_paths.add(p)
    assert len(all_paths)==13

"""B02 freshness and staged visual author evidence, not learner qualification."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/"curriculum/chemistry/agent-b"
def read(p): return json.loads(p.read_text(encoding="utf-8"))

def test_b02_freshness_revisions_join_current_witnesses_and_stages():
    c=read(B/"qrt/B02-C10-C11-author-coverage.v0.4.0.json")
    v=read(B/"qrt/B02-C10-C11-staged-visuals.v0.7.0.json")
    w=read(B/"qrt/B02-C10-C11-author-witnesses.v0.6.0.json")
    s=read(B/"qrt/B02-core2-targeted-transfers.v0.5.0.json")
    native=[t for u in ("C10","C11") for t in read(B/f"core1b/{u}.core1b.v0.1.0.json")["cycles"]]
    tasks={t["cycle_id"]:t for t in native}
    tasks.update({t["task_id"]:t for t in s["records"]})
    assert len(tasks)==47
    assert len(c["freshness_revision_history"])==11
    for m in c["freshness_revision_history"]:
        old=m.get("old_cycle_id",m.get("old_task_id"))
        new=m.get("new_cycle_id",m.get("new_task_id"))
        assert old not in tasks and new in tasks
    assert len(v["records"])==11 and v["counts"]["other_tasks_without_exact_stages"]==36
    files=set()
    for r in v["records"]:
        assert r["task_id"] in tasks
        witness=next(t for t in w["records"] if t["task_id"]==r["task_id"])
        assert witness["independent_qualification"]=="HOLD"
        assert [a["id"] for a in r["stages"]]==["S1","S2","S3"]
        for a in r["stages"]:
            p=ROOT/a["path"]
            root=ET.parse(p).getroot()
            assert root.tag=="{http://www.w3.org/2000/svg}svg"
            assert root.find("{http://www.w3.org/2000/svg}title") is not None
            assert witness["qrt_criteria"][a["id"]]["candidate_evidence"]==a["path"]
            assert a["independent_status"]=="UNREVIEWED"
            files.add(p)
    assert len(files)==33
    assert all(wr["witnesses"]["B1"]["task"]==tasks[wr["task_id"]]["attempt"]["prompt"] for wr in w["records"])

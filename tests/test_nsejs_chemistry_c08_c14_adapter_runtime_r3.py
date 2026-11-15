"""R3 exact Chemistry Topic Adapter ↔ Core1B runtime contract smoke tests."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
CHEM=ROOT/"curriculum"/"chemistry"
RUN=ROOT/"nsejs"/"chemistry"/"textbook"/"reader.js"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_all_seven_adapters_bind_exact_native_x_z_w_and_remain_held():
    total=0
    for i in range(8,15):
        u=f"C{i:02d}"
        a=load(CHEM/"adapters"/f"{u}.v1.json")
        b=load(CHEM/"agent-b"/"core1b"/f"{u}.core1b.v0.1.0.json")
        tasks={t["qrt_instance_ref"]:t for t in b["cycles"]}
        assert a["status"]=="ACADEMIC_HOLD" and b["release"]["qrt_adjudication"]=="HOLD"
        assert len(a["subtopics"])==len(b["cycles"])//3
        for s in a["subtopics"]:
            assert len(s["qrt_instances"])==3
            assert len({q["primary_operation"] for q in s["qrt_instances"]})==3
            for q in s["qrt_instances"]:
                t=tasks[q["instance_id"]]
                assert t["subtopic_ref"]==s["subtopic_id"]
                assert q["slots"]["X"]==q["student_task"]==t["attempt"]["prompt"]
                assert q["slots"]["Z"]==t["attempt"]["post_commit_closure"]["model_response"]
                assert q["slots"]["W"]==t["attempt"]["protected_W"]
                assert not q["slots"]["W"].startswith("The learner independently completes")
                assert len(q["slots"]["W"])>75
                assert q["status"]=="ACADEMIC_HOLD"
                assert t["source_role"]=="AUTHORED_PRACTICE" and t["source_exam_question_id"] is None
                total+=1
    assert total==120

def test_runtime_joins_adapter_and_binds_revision_to_xyzw():
    js=RUN.read_text(encoding="utf-8")
    assert "function validTopicAdapter" in js
    assert "TOPIC_ADAPTER_XYZW_MISMATCH_HOLD" in js
    assert "q.slots?.X!==t.attempt?.prompt" in js
    assert "q.slots?.Z!==t.attempt?.post_commit_closure?.model_response" in js
    assert "q.slots?.W!==t.attempt?.protected_W" in js
    assert 'ADAPTER_ROOT+unit+".v1.json"' in js
    assert "g9chem-full-unit-v3" in js
    assert "supplemental:supplemental||[],visuals:visuals||null,adapter" in js
    assert "localStorage.getItem" in js and "validAttemptRecord" in js

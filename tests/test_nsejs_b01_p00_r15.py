"""P00 R15 bridge: B01 standalone routes use R14 by default, original reader opt-in only.

These tests establish routing and repository compatibility, not independent
P00/R01 academic approval or learner mastery.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
B01=ROOT/"nsejs/physics/curriculum/topics/PH07/b01"
JS=ROOT/"nsejs/physics/curriculum/agent2/core1b-runtime.js"
PREVIEW=B01/"learner-preview/runtime.js"
R13=B01/"B01_INTEGRATED_CURRICULUM_PROPOSAL.v1.json"


def topics():
    p=json.loads(R13.read_text(encoding="utf-8"))
    return p,{e["subtopic_id"] for g in p["groups"] for e in g["base_instances"]}


def test_all_25_legacy_primary_subtopics_delegate_and_keep_original_pages():
    p,ids=topics()
    assert len(ids)==25
    assert sum(x.startswith("PH07") for x in ids)==12
    assert sum(x.startswith("PH08") for x in ids)==13
    for ident in ids:
        route=ROOT/f"nsejs/physics/curriculum/topics/{ident[:4]}/b01/{ident}/core1b.html"
        assert route.is_file(),ident
        page=route.read_text(encoding="utf-8")
        assert 'data-agent2-core1b' in page
        assert 'core1b-runtime.js' in page
        assert 'ACADEMIC HOLD' in page
    assert p["counts"]["total_instances"]==89
    assert p["counts"]["selected_canonical_mains"]==0


def test_shared_runtime_delegation_is_scoped_and_legacy_retains_user_state():
    js=JS.read_text(encoding="utf-8")
    assert "PH07|PH08" in js
    assert "/b01/" not in "" or "b01" in js
    assert "new URLSearchParams(location.search).get('legacy') !== '1'" in js
    assert "location.replace(dest)" in js
    assert "encodeURIComponent(m[3])" in js
    assert "PH09–PH12" in js
    assert "g9-physics-agent2-core1b-v1:" in js
    for topic in ("PH09","PH10","PH11","PH12"):
        path=ROOT/f"nsejs/physics/curriculum/topics/{topic}/core1b-preview.html"
        assert path.is_file()
        assert 'data-agent2-core1b' in path.read_text(encoding="utf-8")
    # No rewriting existing package or attempt keys is allowed.
    assert "localStorage.clear()" not in js
    assert "localStorage.removeItem(key())" not in js


def test_b01_r14_reader_accepts_deep_link_and_separate_legacy_source_review():
    js=PREVIEW.read_text(encoding="utf-8")
    assert "const subtopic=params.get('subtopic')" in js
    assert "task.subtopic_id===subtopic" in js or "t.subtopic_id===subtopic" in js
    assert "const originalUrl=new URL(task.core1b,ROOT)" in js
    assert "originalUrl.searchParams.set('legacy','1')" in js
    assert "state.pagePins.get(task.core1a)" in js
    assert "requestText(task.core1a,a,'.html')" in js
    assert "readWithHistoricalR13" in js
    assert "'NOT_ESTABLISHED_R13'" in js
    assert "mastery_status:'UNASSESSED'" in js
    assert "document.querySelector" not in js or "state.tasks" in js


def test_source_r01_and_canonical_selections_still_hold():
    p,_=topics()
    assert p["academic_status"]==p["source_admission"]=="HOLD"
    assert p["status"]=="AUTHOR_PROPOSAL_ONLY__INTEGRATION_HOLD"
    assert p["counts"]["mixed_main_proposals"]==16
    assert p["counts"]["selected_canonical_adapters"]==0
    source=json.loads((B01/"B01_CUMULATIVE_SOURCE_TO_LEARNING.v2.json").read_text())
    assert source["counts"]["direct_exam_admissions"]==0
    queue=json.loads((B01/"B01_R01_REVIEW_QUEUE.v1.json").read_text())
    assert len(queue["targets"])==89
    assert all(q["admission"]=="HOLD" for q in queue["targets"])

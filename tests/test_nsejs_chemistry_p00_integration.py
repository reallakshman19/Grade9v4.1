"""P00 integration contracts: author candidates remain held and all 47 assets join.

These structural tests do not substitute for HTTP Chromium or independent QRT review.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "curriculum/chemistry/agent-b"
R = ROOT / "nsejs/chemistry/textbook"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def material():
    visuals=read(C/"qrt/B02-C10-C11-staged-visuals.v0.7.0.json")
    supplemental=read(C/"qrt/B02-core2-targeted-transfers.v0.5.0.json")
    natives={u:read(C/f"core1b/{u}.core1b.v0.1.0.json") for u in ("C10","C11")}
    books={u:read(C/f"learner/{u}.reader.v0.1.0.json") for u in ("C10","C11")}
    return visuals,supplemental,natives,books


def test_b02_exact_47_task_join_with_39_native_8_supplemental():
    visuals,supp,natives,books=material()
    native = [task for pack in natives.values() for task in pack["cycles"]]
    other=supp["records"]
    assert len(native)==39
    assert len(other)==8
    ids=[task["cycle_id"] for task in native]+[task["task_id"] for task in other]
    assert len(set(ids))==47
    assert len(visuals["records"])==47
    assert set(ids)=={v["task_id"] for v in visuals["records"]}
    assert sum(1 for x in other if x["subtopic_id"].startswith("CHEM-C10."))==4
    assert sum(1 for x in other if x["subtopic_id"].startswith("CHEM-C11."))==4
    assert all(v["source_role"]=="AUTHORED_TRANSFER_NOT_ORIGINAL_EXAM"
               and v["source_admission"]=="HOLD" for v in other)
    for unit in ("C10","C11"):
        assert len(natives[unit]["cycles"]) == len(books[unit]["sections"])*3


def test_stage_paths_sha_integrity_and_holds():
    visuals,*_=material()
    seen=set()
    stages=visuals["records"]
    assert visuals["counts"]=={"tasks":47,"stages":141,"native":39,
        "supplemental":8,"other_tasks_without_exact_stages":0,"qualified":0}
    for task in stages:
        assert task["status"]=="AUTHOR_VISUAL_CANDIDATE_RUNTIME_HOLD"
        assert len(task["stages"])==3
        for i,stage in enumerate(task["stages"],1):
            assert stage["id"]==f"S{i}"
            assert stage["independent_status"]=="UNREVIEWED"
            assert stage["exposure"]=="P00_SEQUENCED_OPTIONAL_PRE_ATTEMPT_HOLD"
            assert stage["path"] not in seen
            seen.add(stage["path"])
            path=ROOT/stage["path"]
            raw=path.read_bytes()
            assert hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()==stage["git_blob"]
            doc=ET.fromstring(raw)
            svg="{http://www.w3.org/2000/svg}"
            assert doc.tag==svg+"svg"
            assert doc.find(svg+"title") is not None
            assert doc.find(svg+"desc") is not None
            assert not any(node.tag in {svg+"script",svg+"foreignObject"} for node in doc.iter())
    assert len(seen)==141


def test_native_reader_fail_closed_full_revision_and_stage_exposure_code():
    reader=(R/"reader.js").read_text(encoding="utf-8")
    html=(R/"index.html").read_text(encoding="utf-8")
    assert "g9chem-full-unit-v2" in reader
    assert "schema:\"g9chem-full-unit-v2\",book,practice" in reader
    assert "supplemental:supplemental||[],visuals:visuals||null" in reader
    assert 'digestHex("SHA-256"' in reader
    assert 'digestHex("SHA-1",blob)' in reader
    assert "STAGE_BLOB_MISMATCH_HOLD" in reader
    assert "AUTHOR_VISUAL_CANDIDATE_RUNTIME_HOLD" in reader
    assert "POST-COMMIT ONLY" in reader
    assert "visualStages(task,renderEpoch)" in reader
    assert reader.index("if(!saved){") < reader.index("if(B02.has(view.unit))visualStages")
    assert "storeStageExposure(task,asset.id,view.revision)" in reader
    assert "revisionKey(\"attempt\",task)" in reader
    assert "STALE_REVISION" not in reader or "revision" in reader
    assert "UNKNOWN_TASK_HOLD" in reader and "TASK_SUBTOPIC_MISMATCH" in reader
    assert "NO_SECURE_REVISION_HASH" in reader
    assert "STORAGE_UNAVAILABLE" in reader
    assert "source-return" in html
    assert "script defer src=\"reader.js\"" in html
    assert "56px" in html


def test_other_five_chemistry_reader_units_remain_available():
    for unit in ("C08","C09","C12","C13","C14"):
        book=read(C/f"learner/{unit}.reader.v0.1.0.json")
        native=read(C/f"core1b/{unit}.core1b.v0.1.0.json")
        assert book["unit_id"]==unit
        assert native["unit_id"]==unit
        assert book["academic_status"]=="DRAFT_ACADEMIC_HOLD"
        assert native["release"]["scientific_review"]=="HOLD"
        assert len(native["cycles"])==len(book["sections"])*3


def test_loading_never_reuses_previous_unit_state():
    reader=(R/"reader.js").read_text(encoding="utf-8")
    assert "function resetActivePack()" in reader
    assert "function setLoading(busy)" in reader
    load=reader[reader.index("async function load("):reader.index("function fail(code)")]
    assert "resetActivePack();" in load
    assert load.index("resetActivePack();") < load.index("await Promise.all(urls.map(fetchJson))")
    assert "setLoading(true);" in load
    assert load.index("setLoading(true);") < load.index("await Promise.all(urls.map(fetchJson))")
    assert load.index("setLoading(false);") > load.index("view.book=book")
    assert 'lesson.setAttribute("aria-busy",String(busy));' in reader
    assert reader.count("if(!view.book||!view.practice)return;") >= 4


def test_progressive_stage_controls_enforce_persisted_order():
    reader=(R/"reader.js").read_text(encoding="utf-8")
    assert 'const sequence=["S1","S2","S3"];' in reader
    assert 'index>0&&!levels.includes(sequence[index-1])' in reader
    assert 'exposed.add(asset.id);' in reader
    assert 'control.disabled=!permitted;' in reader
    assert 'exposure.value?.revision===view.revision' in reader
    assert 'STAGE_ORDER_OR_EXPOSURE_HOLD' in reader
    assert 'Progression: inspect S1 first, then S2, then S3.' in reader


def test_browser_qa_exercises_reviewed_failure_paths():
    script=(ROOT/"tools/chemistry_p00_b02_browser_qa.py").read_text(encoding="utf-8")
    for check_name in ("check_delayed_unit_load_never_renders_previous_pack",
                       "check_stage_order_survives_refresh",
                       "check_keyboard_only_read_attempt_and_stages",
                       "check_visual_blob_tampering_fail_closed"):
        assert f"def {check_name}(" in script
        assert script.count(check_name+"(browser,ids)") == 1
    assert 'page.keyboard.press("Tab")' in script
    assert 'page.keyboard.press("Enter")' in script
    assert 'page.keyboard.press("Space")' in script

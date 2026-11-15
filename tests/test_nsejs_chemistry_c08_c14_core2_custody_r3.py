"""C08–C14 Core2 custody gate and safe authored-lesson linking (no exam admission)."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
CHEM=ROOT/"nsejs"/"chemistry"
SOURCE=ROOT/"curriculum"/"chemistry"/"agent-b"/"sources"/"C08-C14_PRIMARY_SCOPE_REGISTER_R2.json"

def get(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_exact_40_row_source_to_authored_route_without_exam_promotion():
    m=get(CHEM/"core2-c08-c14-custody.v1.json")
    scope=get(SOURCE)
    legacy=get(ROOT/"nsejs"/"core2"/"inventory.v1.json")
    assert len(m["units"])==7
    rows=[s for u in m["units"] for s in u["subtopics"]]
    assert len(rows)==40
    assert {s["subtopic_id"] for s in rows}=={s["subtopic_id"] for s in scope["rows"]}
    assert m["authenticated_original_question_routes"]==0
    assert m["authenticated_exam_figures"]==m["authenticated_exam_answer_keys"]==0
    assert m["independent_question_qrt_reviews"]==0
    assert m["student_release"]=="HOLD"
    assert m["legacy_chemistry_identity_records"]==sum(
        r["unverified_candidate_question_count"] for r in legacy["items"] if r["subject"]=="CHEMISTRY"
    )==87
    assert m["separate_chemistry_candidate_registry_entries"]==119
    for u in m["units"]:
        assert u["authenticated_original_questions"]==0
        for s in u["subtopics"]:
            assert all(s[x] is None for x in ("source_exam_question_id","original_stem_digest","original_figure_digest","official_key_digest","core2_reader_route"))
            assert s["source_identity_join"]=="NOT_ADMITTED" and s["academic_admission"]=="HOLD"
            assert s["core1a_authored_route"].startswith(f"textbook/index.html?unit={u['unit_id']}&subtopic={s['subtopic_id']}")
            assert s["core1b_authored_route"].endswith("mode=practice")
    page=(CHEM/"core2-custody.html").read_text(encoding="utf-8")
    hub=(CHEM/"index.html").read_text(encoding="utf-8")
    assert "core2-custody.html" in hub and "87-item" in page
    assert all(s["subtopic_id"] in page for s in rows)
    assert "0 authenticated original-question routes" in page
    assert "iframe" not in page.lower()

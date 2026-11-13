"""Agent B Chemistry C08–C14: authored depth and linkage tests (technical only)."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/"curriculum"/"chemistry"/"agent-b"
CHEM=ROOT/"curriculum"/"chemistry"
UNITS=[f"C{i:02d}" for i in range(8,15)]
EXPECTED={"C08":6,"C09":6,"C10":6,"C11":7,"C12":5,"C13":5,"C14":5}
OPS={"RETRIEVE","EXPLAIN","APPLY","MODEL","REPRESENT","SYNTHESIZE","JUSTIFY"}
GATES={g+str(i) for g in ("H","S","P","M") for i in range(1,4)}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_all_authored_units_match_pinned_stage0_and_blueprint():
    syllabus=load(CHEM/"syllabus"/"chemistry-syllabus.v1.json")
    expected={u["id"]:u for u in syllabus["units"]}
    total_subtopics=total_cycles=total_bindings=0
    for unit in UNITS:
        a=load(CHEM/"adapters"/f"{unit}.v1.json")
        source=expected[unit]["subtopics"]
        b=load(B/"learner"/f"{unit}.reader.v0.1.0.json")
        c=load(B/"core1b"/f"{unit}.core1b.v0.1.0.json")
        concept=load(B/"canonical"/f"{unit}.concepts.v0.1.0.json")
        assert len(source)==len(b["sections"])==len(a["subtopics"])==len(concept["concepts"])==EXPECTED[unit]
        assert len(c["cycles"])==3*EXPECTED[unit]
        assert a["blueprint_ref"]=="CHEM-QRT-BLUEPRINT@0.1.0"
        assert c["release"]["scientific_review"]=="HOLD"
        assert b["academic_status"]=="DRAFT_ACADEMIC_HOLD"
        assert {s["id"] for s in source}=={s["id"] for s in b["sections"]}
        assert {s["id"] for s in source}=={s["subtopic_id"] for s in a["subtopics"]}
        assert {x["concept_id"] for x in concept["concepts"]}=={s["subtopic_id"]+"-CONCEPT" for s in a["subtopics"]}
        adapter_ids={t["instance_id"] for s in a["subtopics"] for t in s["qrt_instances"]}
        assert adapter_ids=={x["qrt_instance_ref"] for x in c["cycles"]}
        for sub in a["subtopics"]:
            operations=[q["primary_operation"] for q in sub["qrt_instances"]]
            assert len(set(operations))>=3
            for q in sub["qrt_instances"]:
                assert q["template_ref"]==f'QRT-{q["primary_operation"]}-{q["band"]}'
                assert q["primary_operation"] in OPS
                assert q["status"]=="ACADEMIC_HOLD"
                total_bindings+=1
        for idx,s in enumerate(b["sections"]):
            assert s["id"]==source[idx]["id"]
            assert s["scope"]==source[idx]["scope"]
            assert len(s["hook"])>=60
            assert len(s["teaching"])>= (1 if unit=="C09" else 3)
            assert all(len(t)>=90 for t in s["teaching"])
            assert len(s["worked"])>=130
            assert len(s["misconception"])>=40
            assert len(s["boundary"])>=40
        for x in c["cycles"]:
            assert x["source_role"]=="AUTHORED_PRACTICE"
            assert x["source_exam_question_id"] is None
            assert x["attempt"]["initial_answer_visibility"]=="HIDDEN"
            assert x["attempt"]["first_attempt_must_be_saved_before_feedback"] is True
            assert [h["id"] for h in x["attempt"]["hints"]]==["H1","H2","H3"]
            assert x["attempt"]["post_commit_closure"]["model_response"]
            assert x["boundary_test"]["answer"]
            assert set(x["reviews"])==GATES
            assert all(v=="UNREVIEWED" for v in x["reviews"].values())
            assert x["academic_status"]=="AUTHOR_CANDIDATE_REQUIRES_INDEPENDENT_REVIEW"
            total_cycles+=1
        total_subtopics+=len(source)
    assert (total_subtopics,total_bindings,total_cycles)==(40,120,120)

def test_all_seven_manuscripts_are_connected_and_full_scope():
    for unit in UNITS:
        text=(B/"textbook"/f"{unit}.core1a.md").read_text(encoding="utf-8")
        sections=EXPECTED[unit]
        for i in range(1,sections+1):
            assert f"{unit}.{i:02d}" in text
        assert len(text.split())>= 2100, (unit,len(text.split()))
        assert "HOLD" in text
        assert any(x in text.lower() for x in ("worked","construction"))
        assert any(x in text.lower() for x in ("independent","check"))
        assert "NSEJS" in text or "nsejs" in text
    c12=(B/"textbook"/"C12.core1a.md").read_text(encoding="utf-8")
    c13=(B/"textbook"/"C13.core1a.md").read_text(encoding="utf-8")
    c09=(B/"textbook"/"C09.core1a.md").read_text(encoding="utf-8")
    assert "EXTENSION" in c12 and "ENRICHMENT" in c12
    assert "EXTENSION" in c13 and "ENRICHMENT" in c13
    assert "EXTENSION" in c09

def test_b_prerequisites_not_falsely_qualified():
    for unit in UNITS:
        canon=load(B/"canonical"/f"{unit}.concepts.v0.1.0.json")
        adapter=load(CHEM/"adapters"/f"{unit}.v1.json")
        for row in canon["concepts"]:
            assert row["academic_status"]=="DRAFT_UNREVIEWED"
            assert row["exam_provenance_claim"]=="NONE"
            assert row["core1a_complete"] and row["core1b_complete"]
        for row in adapter["subtopics"]:
            assert row["canonical_truth_status"]!="QUALIFIED"
            assert row["missing_prerequisite_refs"]

def test_reader_makes_no_source_or_student_release_claim():
    html=(ROOT/"nsejs"/"chemistry"/"textbook"/"index.html").read_text(encoding="utf-8")
    js=(ROOT/"nsejs"/"chemistry"/"textbook"/"reader.js").read_text(encoding="utf-8")
    assert "ACADEMIC HOLD" in html and "D3/D4 labels are author proposals" in html
    assert "VALIDATED" not in html.upper().replace("NOT REVIEWED", "")
    assert "first_attempt_must_be_saved_before_feedback" in js
    assert "NO_SECURE_REVISION_HASH" in js
    assert "STALE_REVISION_HOLD" in js
    assert "STORAGE_UNAVAILABLE" in js
    assert "content_revision" not in html.lower()
    assert "innerHTML" not in js
    assert "MODEL_RESPONSE" not in html.upper()

def test_c09_new_figures_present_and_valid_svg_signatures():
    for name in ("C09-neutralisation.svg","C09-phosphorus-connectivity.svg"):
        fig=B/"figures"/name
        assert fig.exists()
        text=fig.read_text(encoding="utf-8")
        assert "<svg " in text and "</svg>" in text
        assert '<title id="t">' in text and '<desc id="d">' in text
        assert "<script" not in text

def test_all_reader_json_have_bounded_source_claims():
    for unit in UNITS:
        reader=load(B/"learner"/f"{unit}.reader.v0.1.0.json")
        assert reader["content_origin"]=="AUTHORED_PEDAGOGICAL"
        assert reader["syllabus_ref"]=="chemistry-syllabus.v1.json@0.1.0"
        assert reader["academic_status"]=="DRAFT_ACADEMIC_HOLD"
        for row in reader["sections"]:
            if row["scope"] in ("EXTENSION","ENRICHMENT"):
                assert row["id"] in {"CHEM-C09.06","CHEM-C12.02","CHEM-C12.05","CHEM-C13.03","CHEM-C13.04","CHEM-C13.05"}


def test_all_qrt_capstones_and_exact_source_scope_fail_closed():
    import re
    scope=load(B/"sources"/"C08-C14_PRIMARY_SCOPE_REGISTER_R2.json")
    assert len(scope["rows"])==40
    assert scope["counts"]["authenticated_exam_questions"]==0
    assert all(r["status"]=="CANDIDATE_PAGE_SECTION_MAPPED_NOT_INDEPENDENTLY_REVIEWED"
               and r["source_question_ids_verified"]==0 for r in scope["rows"])
    scopes={r["subtopic_id"]:r for r in scope["rows"]}
    expected_advanced={"CHEM-C09.06":"EXTENSION","CHEM-C12.02":"EXTENSION",
        "CHEM-C12.05":"ENRICHMENT","CHEM-C13.03":"EXTENSION",
        "CHEM-C13.04":"EXTENSION","CHEM-C13.05":"ENRICHMENT"}
    for ref,classification in expected_advanced.items():
        assert scopes[ref]["chemistry_source_support"]==classification
    manifest=load(B/"qrt"/"D3D4_EVIDENCE_MANIFEST_R2.json")
    assert manifest["policy"]["candidate_QRT_bindings"]==120
    assert manifest["policy"]["qualified_QRT_bindings"]==0
    assert manifest["policy"]["independent_review"]=="DEFERRED_BY_OWNER"
    total=0
    unique=set()
    for unit in UNITS:
        cap=load(B/"qrt"/f"{unit}-D3D4-capstone-evidence.v0.1.0.json")
        assert cap["status"]=="DRAFT_HOLD"
        assert cap["policy"]["academic_release"]=="HOLD"
        assert len(cap["tasks"])==(12 if unit=="C09" else 2)
        for t in cap["tasks"]:
            assert t["task_id"] not in unique
            unique.add(t["task_id"])
            assert t["subtopic_id"] in scopes and t["subtopic_id"].startswith("CHEM-"+unit+".")
            assert t["author_task_type"]=="AUTHORED_TRANSFER"
            assert t["source_question_ref"] is None
            assert t["original_exam_claim"]=="NONE"
            assert t["academic_review"]=="HOLD"
            assert len(t["prompt"])>100 and len(t["post_commit_worked_answer"])>130
            assert t["template_ref"]==f'QRT-{t["primary_operation"]}-{t["band_candidate"]}'
            vector=t["self_score_proposal"]
            assert vector["status"]=="AUTHOR_PROPOSAL_NOT_INDEPENDENT"
            assert len(vector["scores"])==5
            assert all(0<=score<=2 for score in vector["scores"].values())
            assert sum(vector["scores"].values())==vector["total"]
            lo,hi={"D3":(6,7),"D4":(8,10)}[t["band_candidate"]]
            assert lo<=vector["total"]<=hi
            total+=1
    assert total==24

def test_all_eight_original_scientific_figures_and_reader_bindings():
    expected={
        "C08":"C08-reaction-atom-ledger.svg",
        "C09":"C09-neutralisation.svg",
        "C10":"C10-ionic-mobility.svg",
        "C11":"C11-bond-order-hydrogens.svg",
        "C12":"C12-gas-phase-ledger.svg",
        "C13":"C13-electron-charge-ledger.svg",
        "C14":"C14-water-test-limits.svg"
    }
    for unit,filename in expected.items():
        book=load(B/"learner"/f"{unit}.reader.v0.1.0.json")
        refs=[x for s in book["sections"] for x in s.get("figures",[])]
        assert any(filename in x for x in refs)
        fig=(B/"figures"/filename)
        assert fig.exists()
        txt=fig.read_text(encoding="utf-8")
        assert '<svg ' in txt and '<title id="t">' in txt
        assert '<desc id="d">' in txt and '</svg>' in txt
        assert "<script" not in txt
    assert (B/"figures"/"C09-phosphorus-connectivity.svg").exists()

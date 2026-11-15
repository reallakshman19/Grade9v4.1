"""PH11 Circuit worksheet adapter R1: blueprint and C04 fail-closed bindings.

This is an AUTHOR-EXPOSED self-review; passing tests never grants independent QRT,
source rights, exact Core1A/Core1B join, or publication authority.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PH11=ROOT/"nsejs/physics/curriculum/topics/PH11"
DATA=ROOT/"nsejs/data"
ADAPTER=json.loads((PH11/"topic-adapter.PH11.worksheet.v0.3.0.json").read_text())
PACKAGE=json.loads((PH11/"physics-topic-package.v1.json").read_text())
L1=json.loads((DATA/"circuits-level1-core2-candidates.v1.json").read_text())
L2=json.loads((DATA/"circuits-level2-core2-candidates.v1.json").read_text())
BLUEPRINT=json.loads((ROOT/"templates/physics-blueprint/physics-blueprint.D3-D4.json").read_text())
OPERATIONS=["RETRIEVE","EXPLAIN","APPLY","MODEL","REPRESENT","SYNTHESIZE","JUSTIFY"]
SOURCE="1d7f16219d4353bf74e6dd29ebd9c3e9b770ad3d2b402d46aed81165bb4e3c4e"


def test_adapter_pin_is_subject_specific_and_does_not_mutate_blueprint():
    assert BLUEPRINT["blueprint_id"]=="PHYS-QRT-BLUEPRINT"
    assert BLUEPRINT["version"]=="0.2.0" and BLUEPRINT["status"]=="DRAFT_OWNER_REVIEW"
    assert ADAPTER["adapter_id"]=="PHYS-TOPIC-PH11" and ADAPTER["topic_id"]=="PH11"
    assert ADAPTER["version"]=="0.3.0" and PACKAGE["version"]=="0.3.0"
    assert PACKAGE["topic_adapter"]["version"]==PACKAGE["pins"]["topic_adapter_version"]=="0.3.0"
    assert PACKAGE["topic_adapter"]["for_blueprint"]==ADAPTER["for_blueprint"]=="PHYS-QRT-BLUEPRINT 0.2.0"
    assert ADAPTER["operations"]==OPERATIONS
    assert ADAPTER["source_pdf"]["sha256"]==SOURCE
    assert ADAPTER["source_pdf"]["redistribution_rights"]=="HOLD"
    assert ADAPTER["scope"]["real_exam_sources_admitted"]==0
    assert not PACKAGE["core2_sources"]
    assert PACKAGE["acceptance"]["release"]=="HOLD"
    assert all(w["status"]=="HOLD" for w in PACKAGE["acceptance"]["b1_b7"].values())
    assert all(v in ("HOLD","NOT_RUN") for v in PACKAGE["acceptance"]["gates"].values())


def test_existing_ph11_qrt_witnesses_not_relabelled_by_worksheet():
    tasks={t["id"]:t for st in PACKAGE["subtopics"] for t in st["qrt_targets"]}
    old={uid for c in PACKAGE["topic_adapter"]["cells"] for uid in c["instance_ids"]}
    assert len(tasks)==len(old)==6 and set(tasks)==old
    assert ADAPTER["current_blueprint_cells"]==PACKAGE["topic_adapter"]["cells"]
    assert all(t["qrt_status"]=="PROPOSED" and t["source_role"]=="AUTHORED_TRANSFER" for t in tasks.values())
    for c in ADAPTER["current_blueprint_cells"]:
        assert c["cell_id"].startswith("D3.")
        assert c["cell_id"] in {t["blueprint_cell"] for t in tasks.values()}
    assert ADAPTER["author_review_status"]=="AUTHOR_EXPOSED_SELF_REVIEW"


def test_56_source_question_bindings_are_complete_disjoint_and_fail_closed():
    rows=ADAPTER["question_bindings"]
    qs={q["source_id"]:q for q in L1["questions"]+L2["questions"]}
    assert len(rows)==len(qs)==56
    assert set(r["question_uid"] for r in rows)==set(qs)
    assert len({r["question_uid"] for r in rows})==56
    assert [r["question_uid"] for r in rows]==[
      f"NSEJS-CIRC-L1-Q{i:02d}" for i in range(1,37)]+[
      f"NSEJS-CIRC-L2-Q{i:02d}" for i in range(1,21)]
    assert all(r["source_pdf_sha256"]==SOURCE for r in rows)
    assert all(r["source_qualification"]=="UNAUTHENTICATED_WORKSHEET__NOT_DIRECT_EXAM_EVIDENCE" for r in rows)
    assert all(not r["native_exam_source"] and r["source_role"]=="UNQUALIFIED_EXTERNAL_WORKSHEET" for r in rows)
    assert all(r["source_rights"]==r["academic_admission"]==r["qrt_status"]==r["science_status"]=="HOLD" for r in rows)
    assert all(r["learning_join"]=="TOPIC_RELATED_ONLY__EXACT_QRT_LESSON_JOIN_NOT_VERIFIED" for r in rows)
    assert all(r["figure_assets"]==qs[r["question_uid"]]["source_figures"] for r in rows)
    assert all((ROOT/r["teaching_route"]).is_file() and (ROOT/r["candidate_core1b_route"]).is_file() for r in rows)
    assert all(r["proposed_operation"]==qs[r["question_uid"]]["op"] for r in rows)


def test_blueprint_cells_are_proposals_for_7_d3_d4_only():
    cells=ADAPTER["worksheet_candidate_cells"]
    found={r["question_uid"] for c in cells for r in ADAPTER["question_bindings"] if r["question_uid"] in c["question_uids"]}
    assert sum(len(c["question_uids"]) for c in cells)==len(found)==7
    assert {c["cell_id"]:len(c["question_uids"]) for c in cells}=={
      "D3.4":1,"D3.6":3,"D3.7":1,"D4.6":2}
    factor_keys={
      "concept_model_selection","representation_translation","reasoning_chain_length",
      "algebra_computational_load","trap_exception_sensitivity"}
    for row in ADAPTER["question_bindings"]:
        q=(L1 if row["worksheet_level"]==1 else L2)["questions"][row["worksheet_question_number"]-1]
        if row["proposed_band"] in ("D3","D4"):
            assert row["draft_blueprint_cell"]==row["proposed_band"]+"."+str(OPERATIONS.index(q["op"])+1)
            factors=row["proposed_factors"]
            assert set(factors)==factor_keys
            assert all(isinstance(v,int) and 0<=v<=2 for v in factors.values())
            total=sum(factors.values())
            assert total==row["proposed_factor_score"]==q["score"]
            assert 6<=total<=7 if row["proposed_band"]=="D3" else 8<=total<=10
        else:
            assert row["draft_blueprint_cell"] is None
            assert row["cell_status"]=="NOT_APPLICABLE_D1D2_SPEC_PENDING_OR_UNADJUDICATED"
    assert all(c["status"]=="AUTHOR_PROPOSED__INDEPENDENT_QRT_HOLD" and not c["admission"] for c in cells)


def test_worksheet_groups_exhaust_and_do_not_rename_ph11_topic_ids():
    groups=ADAPTER["worksheet_groups"]
    assert len(groups)==11
    assert {g["id"] for g in groups}=={r["worksheet_group_id"] for r in ADAPTER["question_bindings"]}
    assert sum(g["max"]-g["min"]+1 for g in groups)==56
    assert len({(g["level"],x) for g in groups for x in range(g["min"],g["max"]+1)})==56
    assert all(g["id"].startswith("PH11-WS-") and g["min"]<=g["max"] for g in groups)
    assert {s["id"] for s in PACKAGE["subtopics"]}=={"PH11-07","PH11-10"}
    for row in ADAPTER["question_bindings"]:
        g=next(g for g in groups if g["id"]==row["worksheet_group_id"])
        assert row["worksheet_level"]==g["level"]
        assert g["min"]<=row["worksheet_question_number"]<=g["max"]
        assert all("#"+sid in (PH11/"index.html").read_text() or
                   f'id="{sid}"' in (PH11/"index.html").read_text()
                   for sid in g["section_refs"])
    assert "D1_D2_COMMON_BLUEPRINT_SPEC_PENDING" in " ".join(ADAPTER["unresolved"])

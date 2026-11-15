"""Protect R01/R02 40/120 independent-review worksheet from author-exposed score inflation."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"docs"/"audits"/"chemistry-c08-c14"
def test_r4_handoff_is_complete_but_claims_no_independent_acceptance():
    o=json.loads((A/"CHEMISTRY_C08_C14_R01_R02_REVIEW_WORKSHEET_R4.json").read_text(encoding="utf-8"))
    assert o["counts"]=={"chapters":7,"subtopics":40,"core1b_cycles":120,
         "independent_qrt_review_cells":1440,"independently_verified_tasks":0}
    assert len(o["subtopics"])==40 and len(o["cycles"])==120
    ids=set()
    for sub in o["subtopics"]:
        assert sub["science_review"]["status"]=="NOT_RUN"
        assert sub["science_review"]["reviewer"] is None
        assert sub["b3_teaching_review"]["verdict"] is None
        assert sub["source_question_ids_verified"]==0
    for task in o["cycles"]:
        assert task["cycle_id"] not in ids
        ids.add(task["cycle_id"])
        assert task["science_review"]["status"]=="NOT_RUN"
        q=task["blind_qrt"]
        assert q["status"]=="NOT_RUN" and q["reviewer"] is None
        assert q["unexposed_first_pass_digest"] is None
        assert q["semantic_freshness_verdict"] is None
        assert q["final_verdict"] is None
        assert all(x is None for x in q["independent_factor_scores"].values())
        assert set(q["criterion_reviews"])=={f"{group}{i}" for group in "HSPM" for i in (1,2,3)}
        assert all(v["status"]=="UNREVIEWED" and v["reviewer"] is None
                   for v in q["criterion_reviews"].values())
        assert set(q["b1_to_b7"])=={"B1","B2","B3","B4","B5","B6","B7"}
        assert all(x["status"]=="NOT_RUN" for x in q["b1_to_b7"].values())
        assert task["source_role"]=="AUTHORED_PRACTICE"
        assert task["source_exam_question_id"] is None
    assert o["source_admission"]=="HOLD_ZERO_AUTHENTICATED_ORIGINALS"

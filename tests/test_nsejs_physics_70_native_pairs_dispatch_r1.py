"""Metadata-only regression for the Physics 70-row native content dispatch.
No lesson or Physics/QRT academic PASS is inferred by this test.
"""
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"review"/"physics"/"ph01-ph12-full-coverage-r00"
def test_all_70_gap_rows_and_four_embedded_leads_remain_unqualified():
    baseline=json.loads((ROOT/"PHYSICS_PH01_PH12_EVIDENCE_R00.v1.json").read_text())
    plan=json.loads((ROOT/"PHYSICS_70_NATIVE_PAIRS_DISPATCH_R1.json").read_text())
    missing=[r for r in baseline["rows"] if not r["presence"]["dedicated_core1a"] or not r["presence"]["dedicated_core1b"]]
    records=plan["records"]
    assert len(missing)==len(records)==70
    assert {r["subtopic_id"] for r in missing}=={r["subtopic_id"] for r in records}
    assert Counter(r["priority"] for r in records)=={"P0":41,"P1":29}
    assert Counter(r["topic_id"] for r in records)=={"PH02":8,"PH03":7,"PH04":9,"PH05":7,"PH06":10,"PH11":14,"PH12":15}
    assert plan["source"]["matrix_blob_sha"]=="131c7640f80cdf3d5db6c1df3cecd6b746f15b48"
    assert sum(r["current_embedded_lead"] for r in records)==4
    assert all(r["release"]=="HOLD" and r["science_r01"]=="HOLD" and r["qrt_r02"]=="HOLD" for r in records)
    assert plan["totals"]["currently_completed_in_this_workpack"]==0

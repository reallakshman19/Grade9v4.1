"""41-topic native structural audit checks, not B1–B7 academic acceptance."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"tools/physics_41_structural_audit_r1.py"
spec=spec_from_file_location("physics_41_structural_audit_r1",SCRIPT)
mod=module_from_spec(spec)
spec.loader.exec_module(mod)


def test_all_41_native_packages_are_inspected_without_academic_promotion():
    report=mod.audit()
    c=report["counts"]
    assert report["schema"]=="g9v41-four-chapter-native-structural-audit-r1/v1"
    assert c["chapters"]==4 and c["subtopics"]==41
    assert c["per_chapter"]=={"PH01":8,"PH02":8,"PH07":12,"PH08":13}
    assert c["new_quality_r1_examples"]==4
    assert c["new_quality_r1_remaining"]==37
    assert c["original_exam_items_independently_admitted_in_this_audit"]==0
    assert len(report["rows"])==41
    assert len({r["subtopic_id"] for r in report["rows"]})==41
    assert report["wpe_comparator"]["five_synthetic_learn_challenge_pairs"]==5
    assert report["wpe_comparator"]["independent_b3_b4"]=="NOT_ESTABLISHED"
    assert report["academic_disposition"]=="HOLD"
    assert sum(bool(r["warnings"]) for r in report["rows"])==c["native_structural_warning_rows"]
    for row in report["rows"]:
        assert row["academic_status"]=="HOLD"
        assert row["qualified_original_exam_count_in_this_audit"]==0
        assert row["independent_qrt"]=="NOT_RUN"
        assert row["b3_teaching_sufficiency"]=="NOT_INDEPENDENTLY_REVIEWED"
        assert row["b4_fresh_transfer"]=="NOT_INDEPENDENTLY_REVIEWED"
        assert row["native_core1a_count"]==1
        assert row["native_qrt_targets"]>=1

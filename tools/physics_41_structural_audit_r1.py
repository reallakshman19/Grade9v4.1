"""PH01/PH02/PH07/PH08: inspect all 41 current authored native packages.

This report measures file-backed structure only, never academic B1–B7
sufficiency, independent Physics accuracy, QRT demand, or original-exam custody.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics"
FOCUS={"PH01":8,"PH02":8,"PH07":12,"PH08":13}
REQUIRED_STAGES={"predict","attempt","reconstruct","diagnose","repair","boundary_test"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def package_path(ch,uid):
    if ch=="PH01":
        return PH/"curriculum/agent1/PH01/physics-topic-package.v1_1.r4_7.json"
    if ch=="PH02":
        return PH/"curriculum/agent1/PH02/physics-topic-package.v1_1.json"
    return PH/f"curriculum/topics/{ch}/b01/{uid}/physics-topic-package.v1.json"


def audit():
    cat=load(PH/"learn/catalog.json")
    scope=[c for c in cat["chapters"] if c["id"] in FOCUS]
    assert {c["id"]:len(c["units"]) for c in scope}==FOCUS
    rows=[]
    package_cache={}
    for ch in scope:
        for item in ch["units"]:
            uid=(ch["id"]+"-"+item["id"] if ch["id"] in ("PH01","PH02") else item["id"])
            path=package_path(ch["id"],uid)
            if path not in package_cache:
                package_cache[path]=load(path)
            pkg=package_cache[path]
            if pkg.get("topic_id")!=ch["id"] or pkg.get("status")!="DRAFT_AUTHOR_EXPOSED":
                raise ValueError(f"Unexpected package status or topic: {path}")
            st=[x for x in pkg.get("subtopics",[]) if x["id"]==uid]
            a=[x for x in pkg.get("core1a",[]) if x["subtopic_id"]==uid]
            tasks=[x for x in pkg.get("core1b",[]) if x["subtopic_id"]==uid]
            assert len(st)==1 and len(a)==1,(uid,len(st),len(a))
            st,a=st[0],a[0]
            cells=pkg.get("topic_adapter",{}).get("cells",[])
            mapped={v for cell in cells for v in cell.get("instance_ids",[])}
            targets={v["id"] for v in st.get("qrt_targets",[])}
            b_refs={t.get("qrt_target_id") for t in tasks}
            r1=uid in {"PH01-M05","PH02-F04","PH07-02","PH08-08"}
            missing_stages=[t["id"] for t in tasks if not REQUIRED_STAGES.issubset(t.get("stages",{}))]
            false_policy=[t["id"] for t in tasks if not all(t.get("attempt_policy",{}).get(k) is True
                for k in ("save_first_answer_before_hint","track_help_exposure","preserve_original_revision","fail_closed_on_storage_error"))]
            reported_source=[x for x in pkg.get("core2_sources",[]) if x.get("academic_status") in ("APPROVED","ADMITTED","PASS")]
            warnings=[]
            if len(a.get("progressive_examples",[]))<3:warnings.append("FEWER_THAN_THREE_GUIDED_EXAMPLES_IN_NATIVE")
            if not a.get("figures"):warnings.append("NO_FIGURE_IN_NATIVE")
            if not a.get("model_limits"):warnings.append("NO_MODEL_LIMITS_IN_NATIVE")
            if not a.get("misconception"):warnings.append("NO_MISCONCEPTION_REPAIR_IN_NATIVE")
            if not a.get("exit_check"):warnings.append("NO_EXIT_CHECK_IN_NATIVE")
            if not tasks:warnings.append("NO_NATIVE_FRESH_TRANSFER")
            if missing_stages:warnings.append("NATIVE_TRANSFER_MISSING_STAGES")
            if false_policy:warnings.append("NATIVE_ATTEMPT_POLICY_INCOMPLETE")
            if targets-mapped:warnings.append("SUBTOPIC_QRT_NOT_IN_NATIVE_TOPIC_ADAPTER")
            if b_refs-targets:warnings.append("TASK_TO_SUBTOPIC_QRT_JOIN_MISSING")
            if reported_source:warnings.append("SOURCE_ADMISSION_REQUIRES_INDEPENDENT_VERIFICATION")
            if not (PH/item["learn"]).is_file():warnings.append("PUBLIC_CORE1A_ROUTE_MISSING")
            if not (PH/item["practice"]).is_file():warnings.append("PUBLIC_CORE1B_ROUTE_MISSING")
            rows.append({
               "chapter":ch["id"],"subtopic_id":uid,"title":item["title"],
               "package":str(path.relative_to(ROOT)),
               "native_core1a_count":len([a]),"native_guided_example_count":len(a.get("progressive_examples",[])),
               "native_science_records":len([v for v in pkg.get("science_records",[])
                                              if v["id"] in st.get("science_ref_ids",[])]),
               "native_figures_count":len(a.get("figures",[])),
               "native_core1b_tasks":len(tasks),
               "native_six_stage_task_count":len(tasks)-len(missing_stages),
               "native_protected_policy_task_count":len(tasks)-len(false_policy),
               "native_qrt_targets":len(targets),
               "native_adapter_matched_qrt_targets":len(targets&mapped),
               "native_core2_source_entries":len(pkg.get("core2_sources",[])),
               "qualified_original_exam_count_in_this_audit":0,
               "new_R1_deep_construction":r1,
               "b3_teaching_sufficiency":"NOT_INDEPENDENTLY_REVIEWED",
               "b4_fresh_transfer":"NOT_INDEPENDENTLY_REVIEWED",
               "independent_qrt":"NOT_RUN",
               "academic_status":"HOLD",
               "warnings":sorted(set(warnings)),
            })
    assert len(rows)==41 and len({r["subtopic_id"] for r in rows})==41
    wpe=load(ROOT/"physics/wpe/learn-challenge-source-map.json")
    evidence=load(ROOT/"review/physics/ph01-ph02-ph07-ph08-r00/PHYSICS_41_ROUTE_AND_QUALITY_GATE_R00.v1.json")
    assert len(wpe["program"])==5 and evidence["counts"]["subtopic_rows"]==41
    summary={
      "schema":"g9v41-four-chapter-native-structural-audit-r1/v1",
      "review_scope":"AUTHOR_EXPOSED_STRUCTURAL_ONLY",
      "counts":{
        "chapters":4,"subtopics":41,
        "per_chapter":dict(Counter(r["chapter"] for r in rows)),
        "with_three_native_guided_examples":sum(r["native_guided_example_count"]>=3 for r in rows),
        "with_native_figures":sum(r["native_figures_count"]>0 for r in rows),
        "with_any_native_core1b":sum(r["native_core1b_tasks"]>0 for r in rows),
        "with_full_native_stage_keys":sum(r["native_core1b_tasks"]>0 and r["native_six_stage_task_count"]==r["native_core1b_tasks"] for r in rows),
        "with_complete_native_attempt_policies":sum(r["native_core1b_tasks"]>0 and r["native_protected_policy_task_count"]==r["native_core1b_tasks"] for r in rows),
        "with_full_native_qrt_target_mapping":sum(r["native_qrt_targets"]>0 and r["native_qrt_targets"]==r["native_adapter_matched_qrt_targets"] for r in rows),
        "new_quality_r1_examples":sum(r["new_R1_deep_construction"] for r in rows),
        "new_quality_r1_remaining":sum(not r["new_R1_deep_construction"] for r in rows),
        "original_exam_items_independently_admitted_in_this_audit":0,
        "native_structural_warning_rows":sum(bool(r["warnings"]) for r in rows)
      },
      "wpe_comparator":{"five_synthetic_learn_challenge_pairs":len(wpe["program"]),"academic_role":wpe["auth"]["native_core1a"],"independent_b3_b4":"NOT_ESTABLISHED"},
      "warnings_by_type":dict(Counter(w for r in rows for w in r["warnings"])),
      "academic_disposition":"HOLD",
      "rows":rows
    }
    return summary


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="review-artifacts/physics-quality-r1/41-native-structure.json")
    ap.add_argument("--csv",default="review-artifacts/physics-quality-r1/41-native-structure.csv")
    args=ap.parse_args()
    report=audit()
    jsonpath=ROOT/args.output;csvpath=ROOT/args.csv
    jsonpath.parent.mkdir(parents=True,exist_ok=True);csvpath.parent.mkdir(parents=True,exist_ok=True)
    jsonpath.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    cols=[k for k in report["rows"][0] if k!="warnings"]+["warnings"]
    with csvpath.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols);writer.writeheader()
        for r in report["rows"]:writer.writerow({**r,"warnings":";".join(r["warnings"])})
    print(json.dumps(report["counts"],sort_keys=True))
    print("ACADEMIC_HOLD: structural measures do not certify B3/B4, science, source or QRT.")


if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Prepare exact-byte, line-quoted PH02 task evidence for all 24 INSTANCE and six MAIN.

NOT official R2 v2 packets: source custody, Owner Golden and independent R01
review are absent. No fake receipts, source SHA or release admission are issued.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATHS={
 "unit":ROOT/"nsejs/physics/ph02/units.v1.json",
 "qrt":ROOT/"nsejs/physics/ph02/qrt-candidates.v1.json",
 "bridge":ROOT/"nsejs/physics/ph02/teaching-bridges.v1.json",
 "native":ROOT/"nsejs/physics/curriculum/agent1/PH02/physics-topic-package.v1_1.json",
}
TEXT={k:p.read_text(encoding="utf-8").splitlines() for k,p in PATHS.items()}
SHA={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in PATHS.items()}
UNIT=json.loads(PATHS["unit"].read_text(encoding="utf-8"))
QRT=json.loads(PATHS["qrt"].read_text(encoding="utf-8"))
NATIVE=json.loads(PATHS["native"].read_text(encoding="utf-8"))
BRIDGES=json.loads(PATHS["bridge"].read_text(encoding="utf-8"))["bridges"]
OUT=ROOT/"review-artifacts/physics-ph02/task-evidence-prep"


def witness(source:str,marker:str,role:str):
    lines=TEXT[source]
    matches=[(i,line) for i,line in enumerate(lines) if marker in line]
    if len(matches)!=1:
        raise ValueError(f"{source} {role} must match exactly one source line, got {len(matches)}: {marker[:80]}")
    i,line=matches[0]
    return dict(role=role,path=PATHS[source].relative_to(ROOT).as_posix(),
        sha256=SHA[source],start_line=i+1,end_line=i+1,excerpt=line.strip())


def by_body(source:str,key:str,body:str,role:str):
    lines=TEXT[source]
    matches=[(i,line) for i,line in enumerate(lines)
             if f'"{key}":' in line and body[:36] in line]
    if len(matches)!=1:
        raise ValueError(f"{source} {role} body must match once, got {len(matches)} for {body[:50]}")
    i,line=matches[0]
    return dict(role=role,path=PATHS[source].relative_to(ROOT).as_posix(),
        sha256=SHA[source],start_line=i+1,end_line=i+1,excerpt=line.strip())


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    base={u["practice"]["uid"]:(u,u["practice"]) for u in UNIT["units"]}
    add={t["uid"]:(next(u for u in UNIT["units"] if u["id"]==t["unit"]),t) for t in QRT["tasks"]}
    mains={t["uid"]:(next(u for u in UNIT["units"] if u["id"]==t["unit"]),t) for t in QRT["main_cycles"]}
    tasks={**base,**add,**mains}
    assert len(base)==8 and len(add)==16 and len(mains)==6 and len(tasks)==30
    # The v1.1 native contract uses author UIDs for INSTANCE but canonical
    # PH02-MAIN-* IDs for MAIN; runtime UIDs add AUTHORED- for MAIN.
    native_ids={x["id"] if x["kind"]=="INSTANCE" else "AUTHORED-"+x["id"]
                for x in NATIVE["core1b"]}
    assert set(tasks)==native_ids, {
        "missing_from_native":sorted(set(tasks)-native_ids),
        "missing_from_source":sorted(native_ids-set(tasks)),
    }
    items=[]
    for uid,(u,t) in tasks.items():
        source="unit" if uid in base else "qrt"
        if uid in mains:
            bind=witness("native",f'"id": "{t["id"]}"',"NATIVE_MAIN_BINDING")
        else:
            bind=witness("native",f'"task_identity": "{uid}"',"NATIVE_INSTANCE_TARGET")
        detail=[
            by_body(source,"prompt",t["prompt"],"CORE1B_FRESH_TASK"),
            by_body(source,"reconstruction",t["reconstruction"],"CORE1B_MODEL_ROUTE"),
            by_body(source,"boundaryPrompt",t["boundaryPrompt"],"CORE1B_BOUNDARY_TRANSFER"),
            by_body("unit","mechanism",u["mechanism"],"CORE1A_CAUSAL_EXPLANATION"),
            bind,
        ]
        for bridge in BRIDGES[u["id"]]:
            detail.append(by_body("bridge","teaching",bridge["teaching"],
                                   "CORE1A_ADDITIONAL_"+bridge["op"]))
        for x in detail:
            assert x["excerpt"] in TEXT[{"unit":"unit","qrt":"qrt","bridge":"bridge","native":"native"}[
                next(k for k,p in PATHS.items() if p.relative_to(ROOT).as_posix()==x["path"]) ]][x["start_line"]-1]
        packet={"schema":"g9v41-ph02-task-evidence-prep/v1",
          "task_uid":uid,"kind":"MAIN" if uid in mains else "INSTANCE",
          "subtopic_id":u["id"],"head_sha":head,
          "content_source_revision":t["revision"],
          "R2_status":"PREPARATION_ONLY_GOLDEN_NOT_ACCEPTED",
          "source_authenticity":"HOLD","academic_status":"HOLD",
          "independent_science_qrt":"NOT_RUN",
          "owner_golden_sha":None,"r00_receipt":None,"r01_receipt":None,
          "evidence":detail,"known_missing":["R2_SCHEMA_ACCEPTANCE","OWNER_GOLDEN",
           "ORIGINAL_EXAM_SOURCE_CUSTODY","ALL_REQUIRED_NEGATIVE_LOGS",
           "INDEPENDENT_R01_B1_B7_AND_QRT","RELEASE_AUTHORITY"]}
        (OUT/(uid+".prepacket.json")).write_text(json.dumps(packet,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        items.append({"uid":uid,"evidence_count":len(detail),"status":"HOLD"})
    (OUT/"INDEX.json").write_text(json.dumps({"head":head,"items":items,
        "status":"AUTHOR_PREP_NOT_INDEPENDENT_REVIEW","count":len(items)},indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"head":head,"prepared_task_packets":len(items),
        "byte_grounded_witnesses":sum(x["evidence_count"] for x in items),
        "disposition":"PREP_ONLY_ACADEMIC_HOLD"},indent=2))
if __name__=="__main__":
    main()

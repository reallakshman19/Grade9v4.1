#!/usr/bin/env python3
"""PR-level production guard. Pilot mode never silently counts as enforcement.

Owner activates only after accepting the Golden exemplar; GitHub required checks
and CODEOWNERS must then independently require this workflow and policy review.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
POLICY_PATH=HERE/"quality-policy.v1.json"
V=HERE/"verify_evidence_packet.py"


def load_validator():
    s=importlib.util.spec_from_file_location("quality_evidence_author_packet",V)
    if not s or not s.loader:
        raise RuntimeError("Evidence validator is unavailable")
    mod=importlib.util.module_from_spec(s)
    s.loader.exec_module(mod)
    return mod


def changed_paths(repo:Path,base:str)->list[str]:
    if not re.fullmatch("[0-9a-f]{40}",base):
        raise ValueError("Exact 40-digit base SHA required")
    result=subprocess.run(["git","diff","--name-only",base,"HEAD"],
                          cwd=repo,capture_output=True,text=True,check=True)
    return sorted({p.strip() for p in result.stdout.splitlines() if p.strip()})


def scoped_changes(files:list[str],policy:dict)->list[str]:
    """No blind globbing. File changes outside these explicit paths stay out."""
    return [p for p in files if any(p.startswith(prefix) for prefix in policy["protected_paths"])
            and not p.endswith(("/README.md","/MANIFEST.md"))]


def changed_core2_question_ids(repo:Path,base:str,changed:list[str])->list[str]:
    path="nsejs/data/physics-core2-candidates.v1.json"
    if path not in changed:
        return []
    try:
        old_text=subprocess.run(["git","show",base+":"+path],cwd=repo,
                                capture_output=True,text=True,check=True).stdout
        old=json.loads(old_text)
    except subprocess.CalledProcessError:
        old={"questions":[]}
    current=json.loads((repo/path).read_text(encoding="utf-8"))
    def keyed(payload):
        questions=payload.get("questions",[])
        return {(q.get("source_id") or q.get("id")):q for q in questions}
    earlier=keyed(old);now=keyed(current)
    changed_ids=[k for k in sorted(set(earlier)|set(now)) if earlier.get(k)!=now.get(k)]
    return changed_ids


def enforce(repo:Path,base:str|None=None)->dict:
    repo=repo.resolve()
    policy=json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    if policy.get("schema_version")!="g9v41-physics-quality-policy/v1":
        return {"status":"BLOCKED","issues":["UNSUPPORTED_POLICY_SCHEMA"]}
    mode=policy.get("activation")
    if mode=="PILOT_AWAITING_OWNER_GOLDEN" and not policy.get("production_enabled"):
        return {"status":"PILOT_NOT_ENFORCED",
                "academic_status":"HOLD",
                "message":"Schema and adversarial unit tests run; first Golden acceptance and required-check activation are still pending.",
                "owner_per_question_approval_required":False,
                "issues":[]}
    if mode!="ACTIVE_AFTER_OWNER_GOLDEN" or policy.get("production_enabled") is not True:
        return {"status":"BLOCKED","issues":["POLICY_ACTIVATION_CONTRADICTION"]}
    golden=policy.get("owner_accepted_golden_head")
    receipt=policy.get("owner_golden_receipt_path")
    if not isinstance(golden,str) or not re.fullmatch("[0-9a-f]{40}",golden):
        return {"status":"BLOCKED","issues":["OWNER_GOLDEN_HEAD_MISSING"]}
    if not isinstance(receipt,str) or not (repo/receipt).is_file():
        return {"status":"BLOCKED","issues":["OWNER_GOLDEN_RECEIPT_MISSING"]}
    if base is None:
        return {"status":"BLOCKED","issues":["EXACT_PR_BASE_REQUIRED"]}
    files=changed_paths(repo,base)
    guarded=scoped_changes(files,policy)
    if not guarded:
        return {"status":"NO_GOVERNED_PHYSICS_CHANGES","issues":[],
                "owner_per_question_approval_required":False}
    packet_files=sorted(repo.glob(policy["packet_glob"]))
    if not packet_files:
        return {"status":"BLOCKED","issues":["NO_AUTHOR_EVIDENCE_PACKETS_FOR_CHANGED_PHYSICS_CONTENT"],
                "changed":guarded}
    validator=load_validator()
    coverage=set()
    identities=set()
    issues=[]
    for file in packet_files:
        try:
            pack=json.loads(file.read_text(encoding="utf-8"))
            if pack.get("task",{}).get("golden_sample_sha")!=golden:
                issues.append("WRONG_GOLDEN_PIN:"+str(file.relative_to(repo)))
                continue
            audit=validator.validate(pack,repo)
            if audit["mechanical_status"]!="EVIDENCE_STRUCTURALLY_GROUNDED":
                issues.append("PACKET_NOT_GROUNDED:"+str(file.relative_to(repo))+":"+
                              ",".join(audit.get("findings",[])[:5]))
                continue
            coverage.update(e["path"] for e in pack["evidence"])
            identities.add(pack["core2"]["identity"])
        except (ValueError,KeyError,OSError,TypeError) as exc:
            issues.append("PACKET_UNREADABLE:"+str(file)+":"+str(exc)[:150])
    for changed in guarded:
        if changed not in coverage:
            issues.append("NO_PACKET_EXACT_SOURCE_EVIDENCE:"+changed)
    for qid in changed_core2_question_ids(repo,base,guarded):
        if qid not in identities:
            issues.append("CORE2_CHANGED_ITEM_WITHOUT_OWN_PACKET:"+qid)
    return {
        "status":"BLOCKED" if issues else "PACKETS_STRUCTURALLY_GROUNDED_REVIEW_STILL_REQUIRED",
        "academic_status":"HOLD","changed":guarded,"packets_checked":len(packet_files),
        "issues":sorted(set(issues)),
        "owner_per_question_approval_required":False
    }


def main(argv=None)->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root",type=Path,default=HERE.parents[2])
    p.add_argument("--base",type=str)
    args=p.parse_args(argv)
    try:result=enforce(args.repo_root,args.base)
    except (ValueError,subprocess.CalledProcessError,OSError,TypeError) as e:
        result={"status":"BLOCKED","issues":["GATE_FAILED_CLOSED:"+str(e)[:200]]}
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 2 if result["status"]=="BLOCKED" else 0


if __name__=="__main__":
    sys.exit(main())

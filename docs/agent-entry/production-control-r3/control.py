#!/usr/bin/env python3
"""R3 independent production control. Trusted base code; never executes PR code.

A structural gate cannot infer scientific truth or reviewer independence.
The freeze is deliberately stronger than pilot R2. Unknown paths are content.
"""
from __future__ import annotations
import argparse, base64, hashlib, importlib.util, json, os, re, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
from jsonschema import Draft202012Validator

HERE=Path(__file__).resolve().parent
REL="docs/agent-entry/production-control-r3/"
POLICY=REL+"policy.v1.json"
EVID="review/production-control-r3/"
PACKETS="review/quality-packets/"
SHA40=re.compile(r"^[0-9a-f]{40}$")
SHA64=re.compile(r"^[0-9a-f]{64}$")
ID=re.compile(r"^[A-Za-z0-9_.:-]+$")
GATES={"B"+str(n) for n in range(1,8)}
ROLES={"OWNER","DESIGN","R00","R01_SOURCE","R01_SCIENCE","R01_QRT","R01_LEARNING","RELEASE"}
PIN_ROLES={"SHARED","SYLLABUS","SL1","SL2","BLUEPRINT","ADAPTER","QUALITY_CONTRACT","WPE_COMPARATOR"}
OPS={"RETRIEVE","EXPLAIN","APPLY","MODEL","REPRESENT","SYNTHESIZE","JUSTIFY"}
class Block(Exception): pass
def require(ok,why):
    if not ok: raise Block(why)
def canonical(obj): return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
def sha(data): return hashlib.sha256(data).hexdigest()
def no_duplicates(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,"DUPLICATE_JSON_KEY:"+k);result[k]=v
    return result
def parse(data): return json.loads(data,object_pairs_hook=no_duplicates,parse_constant=lambda x: (_ for _ in ()).throw(Block("INVALID_JSON_CONSTANT:"+x)))
def git(repo,*args): return subprocess.check_output(["git","-C",str(repo),*args],stderr=subprocess.PIPE)
def commit(repo,ref):
    require(bool(SHA40.fullmatch(ref)),"EXACT_COMMIT_SHA_REQUIRED")
    resolved=git(repo,"rev-parse","--verify",ref+"^{commit}").decode().strip()
    require(resolved==ref,"COMMIT_ID_MISMATCH");return resolved
def path_ok(p):
    require(isinstance(p,str) and p and not p.startswith("/") and "\\" not in p and "\0" not in p and "\n" not in p and all(x not in ("",".","..",".git") for x in p.split("/")),"UNSAFE_PATH:"+str(p))
    return p
def tree(repo,rev):
    commit(repo,rev);items={}
    for entry in git(repo,"ls-tree","-r","-z",rev).split(b"\0"):
        if not entry:continue
        meta,p=entry.split(b"\t",1);mode,kind,oid=meta.decode().split()
        p=path_ok(p.decode("utf-8"));items[p]=(mode,kind,oid)
    return items
def blob(repo,rev,path,items=None):
    path_ok(path);items=tree(repo,rev) if items is None else items
    require(path in items,"MISSING_FILE:"+path)
    mode,kind,oid=items[path];require(mode in ("100644","100755") and kind=="blob","NON_REGULAR_FILE:"+path)
    return git(repo,"cat-file","blob",oid)
def read_json(repo,rev,path,items=None): return parse(blob(repo,rev,path,items))
def changed(repo,base,head):
    commit(repo,base);commit(repo,head)
    return sorted(path_ok(x.decode("utf-8")) for x in git(repo,"diff","--name-only","--no-renames","-z",base,head).split(b"\0") if x)
def ancestor(repo,a,b):
    return subprocess.run(["git","-C",str(repo),"merge-base","--is-ancestor",a,b],capture_output=True).returncode==0
def evidence_path(path):
    return path.startswith((EVID,PACKETS))
def fingerprint(items):
    # SHA-256 over exact path/mode/type/Git object identity; file evidence uses byte SHA-256.
    # Only receipt/packet namespaces are excluded to avoid a self-reference cycle.
    return sha(canonical([[p,*v] for p,v in sorted(items.items()) if not evidence_path(p)]))
def classify(path,policy):
    if evidence_path(path): return "EVIDENCE"
    if path in policy["governance_paths"] or any(path.startswith(x) for x in policy["governance_prefixes"]): return "GOVERNANCE"
    return "CONTENT"
def load_policy(repo,rev,items=None):
    p=read_json(repo,rev,POLICY,items)
    require(p["schema"]=="g9-production-control/v1","POLICY_SCHEMA")
    require(p["phase"] in ("FREEZE_PENDING_GOLDEN","ACTIVE_AFTER_OWNER_GOLDEN"),"UNKNOWN_POLICY_PHASE")
    require(p["d31"]=="PAUSED","D31_NOT_PAUSED")
    require(p["evidence_prefixes"]==[EVID,PACKETS],"EVIDENCE_EXCLUSION_CHANGED")
    require((p["phase"]=="ACTIVE_AFTER_OWNER_GOLDEN")==bool(p["production_enabled"]),"POLICY_CONTRADICTION")
    return p
def trust_from_env():
    raw=os.environ.get("G9_R3_TRUST_JSON","")
    return parse(raw) if raw else {"schema":"g9-r3-trust/v1","keys":[]}
def trust_keys(trust):
    require(trust.get("schema")=="g9-r3-trust/v1","TRUST_SCHEMA")
    keys={}
    for k in trust.get("keys",[]):
        require(set(k)=={"id","principal","roles","public_key_pem"} and ID.fullmatch(k["id"]) and k["principal"] and k["id"] not in keys and k["roles"] and set(k["roles"])<=ROLES,"INVALID_TRUST_KEY")
        require("PRIVATE KEY" not in k["public_key_pem"] and "BEGIN PUBLIC KEY" in k["public_key_pem"],"INVALID_PUBLIC_KEY")
        keys[k["id"]]=k
    return keys
def signed(receipt,trust,purpose,binding,subject,decision,role,authors=()):
    require(set(receipt)=={"record","signature"},"RECEIPT_SHAPE")
    r=receipt["record"]
    require(set(r)=={"schema","key_id","purpose","binding","subject","decision","issued_at","details"} and r["schema"]=="g9-r3-receipt/v1","RECEIPT_RECORD_SHAPE")
    require((r["purpose"],r["binding"],r["subject"],r["decision"])==(purpose,binding,subject,decision),"RECEIPT_SCOPE_OR_REVISION_MISMATCH:"+purpose)
    key=trust_keys(trust).get(r["key_id"])
    require(key is not None and role in key["roles"],"UNTRUSTED_SIGNER:"+role)
    require(key["principal"] not in authors,"AUTHOR_SELF_APPROVAL:"+role)
    t=datetime.fromisoformat(r["issued_at"].replace("Z","+00:00"))
    require(t.tzinfo is not None and t<=datetime.now(timezone.utc),"INVALID_RECEIPT_TIME")
    require(isinstance(r["details"],dict),"RECEIPT_DETAILS")
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp);(d/"key.pem").write_text(key["public_key_pem"]);(d/"record").write_bytes(canonical(r));(d/"sig").write_bytes(base64.b64decode(receipt["signature"],validate=True))
        result=subprocess.run(["openssl","pkeyutl","-verify","-pubin","-inkey",str(d/"key.pem"),"-rawin","-in",str(d/"record"),"-sigfile",str(d/"sig")],capture_output=True)
        require(result.returncode==0,"INVALID_RECEIPT_SIGNATURE:"+purpose)
    return key["principal"],r["details"]
def validate_schema(obj,name):
    schema=parse((HERE/name).read_bytes());errors=sorted(Draft202012Validator(schema).iter_errors(obj),key=lambda e:str(e.path))
    require(not errors,"SCHEMA:"+name+":"+("; ".join("/".join(map(str,e.path))+":"+e.message for e in errors[:5])))
def check_witness(repo,rev,w,items):
    data=blob(repo,rev,w["path"],items)
    require(sha(data)==w["sha256"],"PIN_HASH_MISMATCH:"+w["path"])
    if "start_line" in w:
        lines=data.decode().splitlines();a,b=w["start_line"],w["end_line"]
        require(1<=a<=b<=len(lines) and w["excerpt"] in "\n".join(lines[a-1:b]),"WITNESS_LINE_MISMATCH:"+w["path"])
def workpack_design(repo,head,workpack,items):
    validate_schema(workpack,"workpack.schema.json")
    require(workpack["subject"]=="Physics","SUBJECT_AUTHORITY_NOT_ACTIVATED")
    require({p["role"] for p in workpack["pins"]}==PIN_ROLES and len(workpack["pins"])==len(PIN_ROLES),"MISSING_OR_DUPLICATE_AUTHORITY_PIN")
    require(len({p["path"] for p in workpack["pins"]})==len(PIN_ROLES),"AUTHORITY_PIN_REUSE")
    for pin in workpack["pins"]:check_witness(repo,head,pin,items)
    comparator=next(p for p in workpack["pins"] if p["role"]=="WPE_COMPARATOR")
    require(comparator["path"].startswith(("physics/wpe/","WPE_Source_to_Core1A_Concept/")),"WPE_COMPARATOR_NOT_ACTUAL_PILOT")
    ids=[i["uid"] for i in workpack["items"]];require(len(ids)==len(set(ids)),"DUPLICATE_TASK_UID")
    for item in workpack["items"]:
        require(item["subtopic_id"].startswith(workpack["topic_id"]+"-"),"CROSS_TOPIC_ID")
        require(item["cell"]!="D3.1","D31_PAUSED")
        require(item["source_role"]!="DIRECT_EXAM_EVIDENCE" or any(x["role"]=="DIRECT_EXAM_EVIDENCE" for x in item["sources"]),"DIRECT_EXAM_WITHOUT_SOURCE")
        for source in item["sources"]:
            if source["role"]=="DIRECT_EXAM_EVIDENCE":
                require(source["paper_sha256"] and source["key_sha256"] and source["rights"]=="VERIFIED_BY_CUSTODIAN","DIRECT_SOURCE_CUSTODY_HOLD:"+source["identity"])
                require(source["figure_need"]=="NOT_REQUIRED" or (source["figure_need"]=="REQUIRED" and source["figure_sha256"]),"DIRECT_SOURCE_FIGURE_MISSING:"+source["identity"])
        require(item["source_role"]=="DIRECT_EXAM_EVIDENCE" or item["direct_exam_credit"]==0,"AUTHORED_TRANSFER_FALSE_EXAM_CREDIT")
        require(len(set(item["construction"]["teaching_obligations"]))==len(item["construction"]["teaching_obligations"]),"DUPLICATE_TEACHING_OBLIGATION")
        require(item["construction"]["anchor_W"].strip()!=item["construction"]["fresh_W"].strip(),"IDENTICAL_DECISIVE_W")
        for path in item["paths"]:path_ok(path)
    return workpack
def receipt_path(workpack,purpose,uid=None):return EVID+"receipts/"+workpack+"/"+purpose+("-"+uid if uid else "")+".json"
def get_receipt(repo,head,items,trust,workpack,purpose,binding,subject,decision,role,authors=(),uid=None):
    return signed(read_json(repo,head,receipt_path(workpack,purpose,uid),items),trust,purpose,binding,subject,decision,role,authors)
def check_active(repo,base,head,items,policy,trust,pr_author,content,golden_lane=False):
    # Active is deliberately not obtainable by changing an author packet.
    golden=policy["accepted_golden"]
    if not golden_lane:
        require(isinstance(golden,dict) and set(golden)=={"head","fingerprint","receipt_path"},"GOLDEN_NOT_ADOPTED")
        gi=tree(repo,golden["head"]);require(fingerprint(gi)==golden["fingerprint"],"GOLDEN_CONTENT_MISMATCH")
        signed(read_json(repo,base,golden["receipt_path"]),trust,"OWNER_GOLDEN",golden["fingerprint"],golden["head"],"ACCEPTED","OWNER")
    paths=[p for p in changed(repo,base,head) if p.startswith(EVID+"submissions/") and p.endswith(".json")]
    require(len(paths)==1,"EXACTLY_ONE_SUBMISSION_REQUIRED")
    sub=read_json(repo,head,paths[0],items);require(set(sub)=={"workpack_path","design_commit","packet_paths"},"SUBMISSION_SHAPE")
    design_path=path_ok(sub["workpack_path"]);require(design_path.startswith(EVID+"workpacks/"),"WORKPACK_PATH")
    d=commit(repo,sub["design_commit"]);require(ancestor(repo,d,head) and d!=head,"DESIGN_NOT_PRIOR_ANCESTOR")
    require(ancestor(repo,base,d) or ancestor(repo,d,base),"DESIGN_NOT_ON_BASE_LINE")
    if ancestor(repo,base,d):require(not [p for p in changed(repo,base,d) if classify(p,policy)=="CONTENT"],"CONTENT_PRECEDES_DESIGN")
    raw=blob(repo,head,design_path,items);require(raw==blob(repo,d,design_path),"DESIGN_CHANGED_AFTER_APPROVAL")
    w=workpack_design(repo,d,parse(raw),tree(repo,d));wid=w["id"];authors=w["authors"]
    require(w["delivery_kind"]==("GOLDEN_SAMPLE" if golden_lane else "BATCH_ITEM"),"WRONG_WORKPACK_PHASE")
    require(pr_author and pr_author in authors,"PR_AUTHOR_NOT_DECLARED")
    wd=sha(raw)
    owner,_=get_receipt(repo,head,items,trust,wid,"OWNER_SCOPE",wd,wid,"AUTHORIZED","OWNER")
    designer,_=get_receipt(repo,d,tree(repo,d),trust,wid,"DESIGN",wd,wid,"ACCEPTED","DESIGN",authors)
    require(owner!=designer,"DESIGN_REVIEWER_NOT_SEPARATE")
    # The signed design must already be present in the design ancestor.
    get_receipt(repo,d,tree(repo,d),trust,wid,"OWNER_SCOPE",wd,wid,"AUTHORIZED","OWNER")
    covered={p for i in w["items"] for p in i["paths"]}
    require(all(classify(p,policy)=="CONTENT" for p in covered),"DESIGN_SCOPE_MUST_BE_CONTENT_PATHS")
    core2="nsejs/data/physics-core2-candidates.v1.json"
    if core2 in content:
        def keyed(rev):
            try: data=read_json(repo,rev,core2)
            except Block: return {}
            rows=data["questions"]
            ids=[q.get("source_id") or q.get("id") for q in rows]
            require(all(ids) and len(set(ids))==len(ids),"CORE2_DUPLICATE_OR_MISSING_ID")
            return dict(zip(ids,rows))
        before,after=keyed(base),keyed(head)
        changed_ids={k for k in set(before)|set(after) if before.get(k)!=after.get(k)}
        covered_ids={i["core2_identity"] for i in w["items"] if core2 in i["paths"]}
        require(changed_ids<=covered_ids,"CORE2_CHANGED_UID_NOT_COVERED:"+",".join(sorted(changed_ids-covered_ids)))
    require(set(content)<=covered,"UNCOVERED_CHANGED_CONTENT:"+",".join(sorted(set(content)-covered)))
    require(set(sub["packet_paths"])=={i["uid"] for i in w["items"]},"PACKET_DENOMINATOR_MISMATCH")
    fp=fingerprint(items)
    # Work on a read-only-in-intent checkout for legacy validator; never import PR Python.
    r2=HERE.parent/"quality-gate-r2/verify_evidence_packet.py"
    spec=importlib.util.spec_from_file_location("trusted_r2",r2);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    require(git(repo,"rev-parse","HEAD").decode().strip()==head,"CANDIDATE_CHECKOUT_HEAD_MISMATCH")
    require(not git(repo,"status","--porcelain","--untracked-files=no").strip(),"DIRTY_CANDIDATE_CHECKOUT")
    for i in w["items"]:
        uid=i["uid"];p=path_ok(sub["packet_paths"][uid]);require(p.startswith(PACKETS),"PACKET_PATH")
        raw_packet=blob(repo,head,p,items);pack=parse(raw_packet)
        t=pack["task"];require(t["task_id"]==uid and t["subtopic_id"]==i["subtopic_id"] and t["base_sha"]==base and t["delivery_kind"]==w["delivery_kind"] and t["golden_sample_sha"]==(t["head_sha"] if golden_lane else golden["head"]) and pack["core2"]["identity"]==i["core2_identity"],"PACKET_IDENTITY_MISMATCH:"+uid)
        tested=commit(repo,t["head_sha"]);require(ancestor(repo,tested,head) and fingerprint(tree(repo,tested))==fp,"STALE_PACKET_CONTENT:"+uid)
        result=mod.validate(pack,repo)
        require(result["mechanical_status"]=="EVIDENCE_STRUCTURALLY_GROUNDED","R2_PACKET_BLOCKED:"+uid)
        require(set(i["paths"])<={e["path"] for e in pack["evidence"]},"PACKET_FILE_COVERAGE_MISSING:"+uid)
        binding=sha(canonical({"content":fp,"packet":sha(raw_packet),"task":uid,"design":wd}))
        reviewers=[]
        for role in ("R00","R01_SOURCE","R01_SCIENCE","R01_QRT","R01_LEARNING"):
            principal,details=get_receipt(repo,head,items,trust,wid,role,binding,uid,"ACCEPTED",role,authors,uid)
            reviewers.append(principal)
            require(details.get("evidence_path","").startswith(EVID) and SHA64.fullmatch(details.get("evidence_sha256","")),"REVIEW_EVIDENCE_MISSING:"+role)
            require(sha(blob(repo,head,details["evidence_path"],items))==details["evidence_sha256"],"REVIEW_EVIDENCE_HASH_MISMATCH:"+role)
            if role=="R00":require(details.get("tested_commit")==tested and details.get("browser")=="PASS" and details.get("negative_controls")=="PASS","R00_TEST_RECEIPT_MISSING")
            if role=="R01_SOURCE":require(details.get("source_role")==i["source_role"] and details.get("rights")=="PASS" and details.get("custody")=="PASS","SOURCE_REVIEW_HOLD")
            if role=="R01_SCIENCE":require(details.get("independent_derivation")=="PASS" and details.get("units_signs_limits")=="PASS","SCIENCE_REVIEW_HOLD")
            if role=="R01_QRT":require(details.get("exposure")=="UNEXPOSED" and SHA64.fullmatch(details.get("sealed_first_pass_sha256","")) and details.get("operation") in OPS and details.get("cell")==i["cell"],"QRT_REVIEW_HOLD")
            if role=="R01_LEARNING":require(details.get("B1_B7")=={g:"PASS" for g in GATES} and details.get("cold_reconstruction")=="PASS","LEARNING_REVIEW_HOLD")
        require(len(set(reviewers))==len(reviewers) and owner not in reviewers and designer not in reviewers,"REVIEWER_ROLE_COLLISION")
    if golden_lane:
        require(any(i["source_role"]=="DIRECT_EXAM_EVIDENCE" for i in w["items"]),"GOLDEN_REQUIRES_DIRECT_EXAM_SOURCE")
        accepted=sha(canonical({"content":fp,"design":wd,"packets":{uid:sha(blob(repo,head,path,items)) for uid,path in sub["packet_paths"].items()}}))
        get_receipt(repo,head,items,trust,wid,"OWNER_GOLDEN",accepted,wid,"ACCEPTED","OWNER")
        return {"status":"SCOPED_GOLDEN_RECEIPTS_VERIFIED","academic_status":"SCOPED_SIGNED_RECEIPTS_ONLY","content_fingerprint":fp,"workpack":wid,"items":len(w["items"]),"golden_binding":accepted}
    return {"status":"DELEGATED_ACCEPTANCE_RECEIPTS_VERIFIED","academic_status":"SCOPED_SIGNED_RECEIPTS_ONLY","content_fingerprint":fp,"workpack":wid,"items":len(w["items"])}
def gate(repo,base,head,trust,pr_author=""):
    try:
        bi=tree(repo,base);hi=tree(repo,head);policy=load_policy(repo,base,bi)
        require(ancestor(repo,base,head),"STALE_BRANCH_REBASE_REQUIRED")
        files=changed(repo,base,head);groups={k:[p for p in files if classify(p,policy)==k] for k in ("CONTENT","GOVERNANCE","EVIDENCE")}
        fp=fingerprint(hi)
        for p in groups["EVIDENCE"]:
            if p in hi:
                require(Path(p).suffix.lower() in {".json",".txt",".md",".csv",".png",".jpg",".jpeg",".webp"},"NON_EVIDENCE_FILE_IN_RECEIPT_NAMESPACE:"+p)
                require(hi[p][0]=="100644" and hi[p][1]=="blob","NON_REGULAR_EVIDENCE:"+p)
        if groups["CONTENT"] and policy["phase"]=="FREEZE_PENDING_GOLDEN":
            # A normal draft remains frozen. The only exception is a fully signed,
            # independently reviewed, representative Golden on an earlier design.
            if not any(p.startswith(EVID+"submissions/") and p.endswith(".json") for p in groups["EVIDENCE"]):
                raise Block("NEW_LEARNER_CONTENT_FROZEN:"+",".join(groups["CONTENT"]))
            require(not groups["GOVERNANCE"],"GOVERNANCE_AND_CONTENT_MUST_BE_SEPARATE")
            return check_active(repo,base,head,hi,policy,trust,pr_author,groups["CONTENT"],golden_lane=True)
        if groups["GOVERNANCE"]:
            # A candidate cannot change the policy that judges itself.
            require(not groups["CONTENT"],"GOVERNANCE_AND_CONTENT_MUST_BE_SEPARATE")
            signed(read_json(repo,head,EVID+"governance-receipt.json",hi),trust,"GOVERNANCE",fp,base,"AUTHORIZED","OWNER")
            # Activation is deliberately a later, separately reviewed migration.
            # Do not allow a signed policy edit alone to stand in for Golden adoption.
            next_policy=load_policy(repo,head,hi)
            require(next_policy["phase"]==policy["phase"] and next_policy["production_enabled"]==policy["production_enabled"] and next_policy["academic_release_enabled"]==policy["academic_release_enabled"] and next_policy["accepted_golden"]==policy["accepted_golden"],"ACTIVATION_REQUIRES_SEPARATE_ADOPTION_WORKPACK")
        if groups["CONTENT"]:
            return check_active(repo,base,head,hi,policy,trust,pr_author,groups["CONTENT"])
        # New design records must be valid and externally approved before merging.
        for p in groups["EVIDENCE"]:
            if p.startswith(EVID+"workpacks/") and p.endswith(".json"):
                raw=blob(repo,head,p,hi);w=workpack_design(repo,head,parse(raw),hi);wd=sha(raw)
                owner,_=get_receipt(repo,head,hi,trust,w["id"],"OWNER_SCOPE",wd,w["id"],"AUTHORIZED","OWNER")
                designer,_=get_receipt(repo,head,hi,trust,w["id"],"DESIGN",wd,w["id"],"ACCEPTED","DESIGN",w["authors"])
                require(owner!=designer,"DESIGN_REVIEWER_NOT_SEPARATE")
        return {"status":"CONTROL_OR_EVIDENCE_ONLY","academic_status":"HOLD","changed":groups,"content_fingerprint":fp}
    except (Block,KeyError,TypeError,ValueError,OSError,subprocess.CalledProcessError) as e:
        return {"status":"BLOCKED","academic_status":"HOLD","reason":str(e)}
def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--base",required=True);p.add_argument("--head",required=True);p.add_argument("--pr-author",default="")
    a=p.parse_args();r=gate(a.repo,a.base,a.head,trust_from_env(),a.pr_author);print(json.dumps(r,indent=2));return 2 if r["status"]=="BLOCKED" else 0
if __name__=="__main__":sys.exit(main())

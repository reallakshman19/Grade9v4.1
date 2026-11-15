#!/usr/bin/env python3
"""Stage only exact, signed public bytes. No deployment from an unapproved tree."""
from __future__ import annotations
import argparse, json, shutil, sys
from pathlib import Path
from control import (Block, EVID, PACKETS, SHA64, ancestor, blob, changed, classify, commit,
                     fingerprint, load_policy, parse, path_ok, require, sha, signed,
                     tree, trust_from_env)
ROOTS={"nsejs","physics","mathematics","chemistry","biology","curriculum","architecture","preview","css","js","data","assets","images","fonts"}
EXTENSIONS={".html",".htm",".css",".js",".mjs",".json",".svg",".png",".jpg",".jpeg",".webp",".ico",".woff",".woff2",".ttf",".txt",".xml",".webmanifest"}
DENIED={"review","reviews","review-artifacts","review_artifacts","evidence","receipts","source-custody","source_custody","private","workspace","fixtures","tests","qa","agent1","contracts","archives","archive","sources","answer-keys","answer_keys","originals","node_modules"}
EXACT_PUBLIC_DOCS={"docs/agent-entry/concept-report-v4.html"}
ROOT_PUBLIC={"index.html","404.html","robots.txt","sitemap.xml","favicon.ico","manifest.webmanifest",".nojekyll"}
def public_path(p):
    path_ok(p);parts=p.split("/")
    if p in ROOT_PUBLIC:return True
    if p in EXACT_PUBLIC_DOCS:return True
    if parts[0] not in ROOTS or any(x.lower() in DENIED or x.startswith(".") for x in parts):return False
    if Path(p).suffix.lower() not in EXTENSIONS:return False
    name=Path(p).stem.lower()
    return not any(x in name for x in ("final-answer-key","official-answer-key","review-receipt","quality-packet","source-custody","source_custody","review-report","private-key"))
def stage(repo,rev,manifest_path,output,trust,control_rev):
    ci=tree(repo,control_rev);policy=load_policy(repo,control_rev,ci)
    require(ancestor(repo,control_rev,rev),"CONTROL_REVISION_NOT_ANCESTOR")
    items=tree(repo,rev);fp=fingerprint(items)
    require(policy["phase"]=="FREEZE_PENDING_GOLDEN" and not policy["academic_release_enabled"],"ACADEMIC_RELEASE_REQUIRES_SEPARATE_ADOPTED_PROTOCOL")
    # Even a signed preview cannot silently include new learner content during freeze.
    changes=changed(repo,policy["legacy_preview_baseline"],rev)
    require(not [p for p in changes if classify(p,policy)=="CONTENT"],"FROZEN_CONTENT_IN_RELEASE_TREE")
    raw=blob(repo,rev,manifest_path,items);m=parse(raw)
    require(set(m)=={"schema","kind","content_fingerprint","files"} and m["schema"]=="g9-r3-publication/v1" and m["kind"]=="TECHNICAL_PREVIEW_ONLY","RELEASE_MANIFEST_SHAPE_OR_KIND")
    require(m["content_fingerprint"]==fp,"STALE_RELEASE_MANIFEST")
    auth=parse(blob(repo,rev,EVID+"release-receipt.json",items))
    binding=sha(raw)
    signed(auth,trust,"PREVIEW_RELEASE",binding,fp,"AUTHORIZED","OWNER")
    require(isinstance(m["files"],list) and m["files"],"EMPTY_RELEASE_MANIFEST")
    require(not output.exists(),"OUTPUT_MUST_NOT_EXIST")
    seen=set();payload=[]
    for entry in m["files"]:
        require(set(entry)=={"path","sha256"},"RELEASE_FILE_SHAPE")
        p=entry["path"];require(public_path(p),"NONPUBLIC_RELEASE_PATH:"+p)
        require(p not in seen,"DUPLICATE_RELEASE_PATH:"+p);seen.add(p)
        data=blob(repo,rev,p,items)
        require(SHA64.fullmatch(entry["sha256"]) and sha(data)==entry["sha256"],"RELEASE_BYTE_MISMATCH:"+p)
        payload.append((p,data))
    require("index.html" in seen,"RELEASE_ENTRYPOINT_MISSING")
    # Search is a release dependency, not a second publication pipeline.
    for p in ("data/learner-search-index.v1.json","nsejs/data/learner-search-index.v1.json"):
        if p in seen:
            index=parse(dict(payload)[p])
            require(isinstance(index,list),"SEARCH_INDEX_SHAPE")
            for row in index:
                u=urlsplit(row["url"])
                require(not u.scheme and not u.netloc and u.path in seen,"SEARCH_TARGET_NOT_PUBLISHED:"+row["url"])
            require(not any(row.get("hints") or row.get("answer") or row.get("steps") for row in index if row.get("category")=="question"),"SEARCH_PROTECTED_PAYLOAD")
    if "data/learner-search-index.v1.json" in seen and "nsejs/data/learner-search-index.v1.json" in seen:
        require(dict(payload)["data/learner-search-index.v1.json"]==dict(payload)["nsejs/data/learner-search-index.v1.json"],"SEARCH_MIRROR_MISMATCH")
    try:
        output.mkdir(parents=True,exist_ok=False)
        for p,data in payload:
            target=output/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        # No regeneration, mutation or untracked assets after byte verification.
        actual={p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
        require(actual==seen,"STAGING_FILE_SET_MISMATCH")
    except Exception:
        if output.exists():shutil.rmtree(output)
        raise
    return {"status":"AUTHORIZED_TECHNICAL_PREVIEW_STAGED","academic_status":"HOLD","content_fingerprint":fp,"files":len(seen),"manifest_sha256":binding}
def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",required=True,type=Path);p.add_argument("--head",required=True);p.add_argument("--control",required=True);p.add_argument("--output",required=True,type=Path);p.add_argument("--manifest",default=EVID+"publication-manifest.json")
    a=p.parse_args()
    try:r=stage(a.repo,a.head,a.manifest,a.output,trust_from_env(),a.control)
    except (Block,ValueError,KeyError,TypeError,OSError) as e:r={"status":"BLOCKED","academic_status":"HOLD","reason":str(e)}
    print(json.dumps(r,indent=2));return 2 if r["status"]=="BLOCKED" else 0
if __name__=="__main__":sys.exit(main())

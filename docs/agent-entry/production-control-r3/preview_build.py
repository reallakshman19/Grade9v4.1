"""Reproduce the existing unified search build using only frozen, pinned code.
The output is untrusted until every public file is checked against a signed manifest.
"""
from __future__ import annotations
import argparse, os, shutil, subprocess, sys, tarfile, tempfile
from pathlib import Path
from contextlib import contextmanager
from control import Block, blob, fingerprint, git, load_policy, parse, path_ok, require, sha, tree
BUILDERS=("tools/build_search_index.py","tools/search_learner_pages.py")
OUTPUTS={prefix+"/"+name for prefix in ("data","nsejs/data") for name in ("learner-search-index.v1.json","learner-search-manifest.v1.json","keyword-synonyms.v1.json")}
@contextmanager
def frozen_build(repo,rev,policy):
    # Verify the two executable builder files are byte-identical to the frozen
    # baseline. The trusted parent process uses only those files for generation.
    base=policy["legacy_preview_baseline"];items=tree(repo,rev);baseline=tree(repo,base)
    for p in BUILDERS:
        require(blob(repo,rev,p,items)==blob(repo,base,p,baseline),"SEARCH_BUILDER_CHANGED:"+p)
    with tempfile.TemporaryDirectory(prefix="g9-preview-") as d:
        root=Path(d)
        with subprocess.Popen(["git","-C",str(repo),"archive","--format=tar",rev],stdout=subprocess.PIPE,stderr=subprocess.PIPE) as proc:
            with tarfile.open(fileobj=proc.stdout,mode="r|") as tar:
                for member in tar:
                    if not member.isfile():continue
                    p=path_ok(member.name);require(p in items and items[p][0] in ("100644","100755"),"ARCHIVE_FILE_NOT_TRACKED:"+p)
                    target=root/p;target.parent.mkdir(parents=True,exist_ok=True)
                    with tar.extractfile(member) as src, target.open("wb") as dest:shutil.copyfileobj(src,dest)
            require(proc.wait()==0,"GIT_ARCHIVE_FAILED")
        for p in BUILDERS:
            require((root/p).read_bytes()==blob(repo,base,p,baseline),"EXPORTED_BUILDER_CHANGED:"+p)
        # No token, trust roster or GitHub environment passed to the builder.
        env={"PATH":os.environ.get("PATH",""),"PYTHONHASHSEED":"0","PYTHONIOENCODING":"utf-8","LC_ALL":"C.UTF-8","TZ":"UTC"}
        result=subprocess.run([sys.executable,"-I",str(root/BUILDERS[0]),"--install-search"],cwd=root,env=env,capture_output=True,text=True,timeout=180)
        require(result.returncode==0,"FROZEN_SEARCH_BUILD_FAILED:"+result.stderr[-1000:])
        yield root
def built_bytes(root,items,p):
    require(p in items or p in OUTPUTS,"GENERATED_PATH_NOT_PERMITTED:"+p)
    target=root/p
    require(target.is_file() and not target.is_symlink(),"MISSING_GENERATED_FILE:"+p)
    return target.read_bytes()
def audit(repo,rev,control_rev):
    from release import public_path
    policy=load_policy(repo,control_rev);items=tree(repo,rev)
    with frozen_build(repo,rev,policy) as root:
        left=(root/"data/learner-search-index.v1.json").read_bytes();right=(root/"nsejs/data/learner-search-index.v1.json").read_bytes()
        require(left==right,"SEARCH_MIRROR_MISMATCH")
        rows=parse(left);subjects={r["subject"] for r in rows}
        require({"Physics","Chemistry","Biology"}<=subjects,"MISSING_SEARCH_SUBJECT")
        from urllib.parse import urlsplit
        targets={urlsplit(r["url"]).path for r in rows};excluded=sorted(p for p in targets if not public_path(p))
        require(all((root/p).is_file() for p in targets),"BROKEN_SEARCH_TARGET_IN_BUILD")
        return {"status":"FROZEN_SEARCH_BUILD_REPRODUCED_NOT_RELEASED","documents":len(rows),"subjects":sorted(subjects),"unique_targets":len(targets),"search_sha256":sha(left),"targets_needing_manifest_scope_review":excluded}
def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--head",required=True);p.add_argument("--control",required=True);a=p.parse_args()
    import json
    print(json.dumps(audit(a.repo,a.head,a.control),indent=2))
if __name__=="__main__":main()

"""Author preparation only: compute exact design or explicit public manifest bytes.
No receipt is signed and no release or academic status is granted here.
"""
import argparse,json,sys
from pathlib import Path
from contextlib import nullcontext
from control import blob, changed, classify, fingerprint, load_policy, parse, require, sha, tree, workpack_design
from release import public_path
from preview_build import frozen_build,built_bytes
def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--head",required=True);p.add_argument("--control",required=True)
    p.add_argument("--design");p.add_argument("--paths-file",type=Path);p.add_argument("--build-mode",choices=["TRACKED_ONLY","FROZEN_SEARCH_R1"],default="FROZEN_SEARCH_R1");p.add_argument("--output",type=Path)
    a=p.parse_args();items=tree(a.repo,a.head);policy=load_policy(a.repo,a.control)
    if a.design:
        raw=blob(a.repo,a.head,a.design,items);w=workpack_design(a.repo,a.head,parse(raw),items)
        print(json.dumps({"status":"DESIGN_STRUCTURAL_PREFLIGHT_ONLY","workpack":w["id"],"design_sha256":sha(raw),"content_fingerprint":fingerprint(items),"review":"HOLD"},indent=2));return
    require(a.paths_file and a.output,"EXPLICIT_PATHS_AND_OUTPUT_REQUIRED")
    require(not [p for p in changed(a.repo,policy["legacy_preview_baseline"],a.head) if classify(p,policy)=="CONTENT"],"FROZEN_CONTENT_IN_RELEASE_TREE")
    paths=parse(a.paths_file.read_bytes());require(isinstance(paths,list) and paths and len(set(paths))==len(paths),"INVALID_EXPLICIT_PATH_LIST")
    require("index.html" in paths,"RELEASE_ENTRYPOINT_MISSING")
    rows=[]
    with (frozen_build(a.repo,a.head,policy) if a.build_mode=="FROZEN_SEARCH_R1" else nullcontext(None)) as build:
        for path in sorted(paths):
            require(public_path(path),"NONPUBLIC_RELEASE_PATH:"+path)
            data=built_bytes(build,items,path) if build is not None else blob(a.repo,a.head,path,items)
            rows.append({"path":path,"sha256":sha(data)})
    m={"schema":"g9-r3-publication/v1","kind":"TECHNICAL_PREVIEW_ONLY","content_fingerprint":fingerprint(items),"build_mode":a.build_mode,"files":rows}
    raw=json.dumps(m,ensure_ascii=False,indent=2).encode()+b"\n";require(not a.output.exists(),"OUTPUT_ALREADY_EXISTS");a.output.write_bytes(raw)
    print(json.dumps({"status":"UNSIGNED_MANIFEST_PREP_ONLY","files":len(rows),"manifest_sha256":sha(raw),"content_fingerprint":m["content_fingerprint"]},indent=2))
if __name__=="__main__":main()

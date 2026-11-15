"""Main-owned read-only stacked PR audit. Never evaluate target-branch workflow code.
A stacked candidate is diagnostic only even if its cumulative diff is evidence-only.
"""
from __future__ import annotations
import json,os,subprocess,sys
from pathlib import Path
from control import Block, changed,classify,commit,git,load_policy,ancestor,require
def audit(repo,main,head,target):
    commit(repo,main);commit(repo,head)
    policy=load_policy(repo,main)
    fork=git(repo,"merge-base",main,head).decode().strip();commit(repo,fork)
    paths=changed(repo,fork,head)
    groups={k:[p for p in paths if classify(p,policy)==k] for k in ("CONTENT","GOVERNANCE","EVIDENCE")}
    return {"status":"STACKED_DIAGNOSTIC_ONLY" if target!="main" else "MAIN_CANDIDATE_REQUIRES_TRUSTED_DECISION","academic_status":"HOLD","main":main,"head":head,"fork":fork,"target":target,"up_to_date":ancestor(repo,main,head),"counts":{k:len(v) for k,v in groups.items()},"content_paths":groups["CONTENT"],"freeze":policy["phase"]}
def gh(*args):return subprocess.check_output(["gh","api",*args],text=True)
def main():
    repo=Path.cwd();main=git(repo,"rev-parse","HEAD").decode().strip();commit(repo,main)
    repository=os.environ["GITHUB_REPOSITORY"]
    prs=json.loads(gh("--paginate","--slurp",f"repos/{repository}/pulls?state=open&per_page=100"))
    # gh --slurp produces list of pages.
    rows=[];errors=[]
    for page in prs:
        for pr in page:
            n=pr["number"];head=pr["head"]["sha"];target=pr["base"]["ref"]
            if target=="main":continue
            try:
                subprocess.run(["git","fetch","--no-tags","origin",f"+refs/pull/{n}/head:refs/r3-audit/{n}"],check=True,capture_output=True,timeout=60)
                fetched=git(repo,"rev-parse",f"refs/r3-audit/{n}").decode().strip()
                require(fetched==head,"PR_HEAD_CHANGED_DURING_AUDIT")
                result=audit(repo,main,head,target);rows.append({"pr":n,**result})
                gh("--method","POST",f"repos/{repository}/statuses/{head}","-f","state=failure","-f","context=g9/r3-cumulative-audit","-f","description=Stacked PR: diagnostic only; main decision required")
            except Exception as exc:
                errors.append({"pr":n,"head":head,"reason":str(exc)})
    print(json.dumps({"main":main,"academic_status":"HOLD","rows":rows,"errors":errors},indent=2))
    return 2 if errors else 0
if __name__=="__main__":sys.exit(main())

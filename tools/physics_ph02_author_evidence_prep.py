#!/usr/bin/env python3
"""Create byte/line-grounded PH02 author evidence PREP; not a valid R2/Golden approval packet.

Runs on checked-out commit; SHA-256 is computed on actual file bytes.
Does NOT fabricate Golden receipt, source key/figure custody, independent academic
review, B1-B7 PASS or negative-control logs. The output is review preparation.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"nsejs/physics/ph02/units.v1.json"
QRT=ROOT/"nsejs/physics/ph02/qrt-candidates.v1.json"
JS=ROOT/"nsejs/physics/ph02/practice.js"
OUT=ROOT/"review-artifacts/physics-ph02/author-evidence-prep"
SOURCE=json.loads(DATA.read_text(encoding="utf-8"))
BASE=DATA.read_text(encoding="utf-8").splitlines(keepends=True)
JSLINES=JS.read_text(encoding="utf-8").splitlines(keepends=True)
CONTENT=SOURCE["units"]
UNIT_STARTS={u["id"]: next(i for i,s in enumerate(BASE) if f'"id": "{u["id"]}"' in s) for u in CONTENT}
def sha256(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def quote(path:Path, lines:list[str], start:int, end:int, role:str, claim:str, warrant:str):
    excerpt="".join(lines[start:end]).strip()
    assert len(excerpt)>=24, (role, excerpt)
    assert excerpt=="".join(path.read_text(encoding="utf-8").splitlines(keepends=True)[start:end]).strip()
    assert len(claim)>=30 and len(warrant)>=45, role
    return dict(id=role,role=role,path=path.relative_to(ROOT).as_posix(),sha256=sha256(path),
        start_line=start+1,end_line=end,excerpt=excerpt,claim=claim,why_this_proves_claim=warrant)
def search(lines:list[str],marker:str,a:int,b:int)->int:
    return next(i for i in range(a,b) if marker in lines[i])
def main()->None:
    OUT.mkdir(parents=True,exist_ok=True)
    head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    rows=[]
    for i,u in enumerate(CONTENT):
        ident=u["id"];start=UNIT_STARTS[ident];end=UNIT_STARTS[CONTENT[i+1]["id"]] if i+1<len(CONTENT) else len(BASE)
        required=[
            ("SCIENCE_PRIMARY_DERIVATION",'"warrant":',f"{ident} contains a candidate physics law with its units and assumptions.",
             "The file locates the exact author statement for science review; this does not establish its truth."),
            ("SCIENCE_INDEPENDENT_CHECK",'"solution":',f"{ident} author anchor includes a reasoned calculation and checking method.",
             "The quoted worked anchor gives reviewers a second inspectable source for physical checks, not independent review."),
            ("SCIENCE_UNITS_AND_SIGNS",'"warrant":',f"{ident} candidate science statement specifies units and signed axes.",
             "The exact same author warrant needs dimension and sign falsification before science acceptance."),
            ("SCIENCE_ASSUMPTIONS_AND_LIMIT",'"case":',f"{ident} states an applicability or changed-contact boundary.",
             "This boundary passage can be challenged independently; the source identity remains author-only."),
            ("SCIENCE_COUNTEREXAMPLE",'"check":',f"{ident} provides a changed-condition numerical or conceptual check.",
             "A changed-condition check is a falsifier candidate, not proof of independent academic qualification."),
            ("CORE1A_PHENOMENON",'"phenomenon":',f"{ident} has a learner-facing physical phenomenon.",
             "The passage identifies the real behaviour being taught and can be reviewed for cold readability."),
            ("CORE1A_CAUSAL_EXPLANATION",'"mechanism":',f"{ident} has a stepwise explanatory causal narrative.",
             "The text claims a physical mechanism; the reviewer must verify the actual validity of every inference."),
            ("CORE1A_PREREQUISITE",'"prerequisites":',f"{ident} declares prerequisite identifiers before advanced tasks.",
             "Explicit prerequisites enable a cold-learner gap check but are not proof that each bridge is taught."),
            ("CORE1A_DIAGRAM",'"caption":',f"{ident} declares a labelled original educational figure purpose.",
             "The corresponding SVG must still be inspected for geometry, axes, signed data and precommit leakage."),
            ("CORE1A_WORKED_FOUNDATION",'"FOUNDATION",',f"{ident} includes a foundation-tier worked example.",
             "The original example is independently visible for challenge; presence alone does not prove teaching quality."),
            ("CORE1A_WORKED_CONNECTED",'"CONNECTED",',f"{ident} includes a connected-tier worked example.",
             "The intermediate problem can be challenged for whether it genuinely connects prior concepts."),
            ("CORE1A_WORKED_ADVANCED",'"ADVANCED",',f"{ident} includes an advanced-tier worked example.",
             "The advanced problem requires semantic verification against the learner's prerequisite knowledge."),
            ("CORE1A_MISCONCEPTION_REPAIR",'"repair":',f"{ident} offers a candidate repair to a specific mistaken model.",
             "The line is a concrete repair proposal, not an automatic diagnosis of a student."),
            ("CORE1A_SYNTHESIS",'"question":',f"{ident} presents an independently answerable synthesis question.",
             "An author-authored exit question is inspectable; no real pupil trial or mastery is implied."),
            ("CORE1B_FRESH_TASK",'"prompt":',f"{ident} contains a distinct proposed learner transfer problem.",
             "The exact attempt wording is available to compare against the worked anchor and decide W novelty."),
            ("CORE1B_MODEL_ROUTE",'"reconstruction":',f"{ident} supplies a post-attempt model route.",
             "The model can be independently re-solved and tested against the new problem, not assumed correct."),
            ("CORE1B_BOUNDARY_TRANSFER",'"boundaryPrompt":',f"{ident} supplies a changed-condition boundary question.",
             "This is independent assessment material that must be protected until a saved prior attempt.")
        ]
        witnesses=[]
        for role,marker,claim,warrant in required:
            idx=search(BASE,marker,start,end)
            # Multi-line prerequisite array: capture more than an empty leading line.
            span=2 if role in {"CORE1A_PREREQUISITE","CORE1A_WORKED_FOUNDATION","CORE1A_WORKED_CONNECTED","CORE1A_WORKED_ADVANCED"} else 1
            witnesses.append(quote(DATA,BASE,idx,min(end,idx+span),role,claim,warrant))
        for role,marker in [
            ("CORE1B_HINT_NONLEAK",'if(!rec?.first_answer)return fail("Commit a first attempt before hints.");'),
            ("CORE1B_FIRST_SAVE","localStorage.setItem(key,serialized)"),
            ("CORE1B_REVISION_RETURN","invalid or stale stored revision")
        ]:
            idx=search(JSLINES,marker,0,len(JSLINES))
            witnesses.append(quote(JS,JSLINES,idx,idx+1,role,
                f"{ident} references the PH02 runtime's {role} guard.",
                "The runtime source line supports a mechanical behavior to challenge with HTTP Chromium and fault-injection logs."))
        packet={"schema":"g9v41-ph02-author-evidence-prep/v1",
            "R2_status":"PREP_ONLY_NOT_SCHEMA_ACCEPTED",
            "must_not_count_as_r2_packet":True,"task_id":"G9V41-PHYS-C1AB-A02-PH02-R1",
            "subtopic_id":ident,"exact_content_head":head,"writer":"AUTHOR_EXPOSED",
            "academic_status":"HOLD","source_authenticity":"HOLD","qrt_status":"UNREVIEWED",
            "owner_accepted_golden_sha":None,"independent_reviewer_receipt":None,
            "evidence":witnesses,"known_missing":["GOLDEN_SAMPLE_OWNER_G0","R01_SCIENCE_QRT",
              "CORE2_SOURCE_PAPER_BYTES_SHA256_AND_VISUAL_FIGURE_KEY",
              "R2_SCHEMA_VALIDATION_AND_ALL_EIGHT_FAULT_FAMILIES",
              "B1_B7_SEMANTIC_ACCEPTANCE","RELEASE_AUTHORITY"]}
        dest=OUT/(ident+".author-prep.json")
        dest.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        rows.append({"subtopic":ident,"witnesses":len(witnesses),"status":"PREP_ONLY_HOLD"})
    (OUT/"INDEX.json").write_text(json.dumps({"head":head,"count":len(rows),
       "status":"BYTE_GROUNDED_PREPARATION_ONLY__ACADEMIC_HOLD","items":rows},indent=2)+"\n")
    print(json.dumps({"generated":len(rows),"witnesses":sum(x["witnesses"] for x in rows),
        "disposition":"AUTHOR_EVIDENCE_PREP_ONLY__ACADEMIC_HOLD","head":head},indent=2))
if __name__=="__main__":main()

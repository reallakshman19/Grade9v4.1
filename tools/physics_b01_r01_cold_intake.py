#!/usr/bin/env python3
"""Produce a genuinely author-label-free Stage A intake for an independent R01.

This is a reproducible author-side PREPARATION, not a cold academic review.
No D-band, QRT operation, decisive W, solution, teacher key or source-admission
claim is exposed inside the Stage A candidate file. R01 keeps their own
frozen, signed independent answers before opening the crosswalk or author JSON.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
B01=ROOT/"nsejs/physics/curriculum/topics/PH07/b01"
SOURCE=B01/"B01_INTEGRATED_CURRICULUM_PROPOSAL.v1.json"
OUT=B01/"r01-cold"
BLIND=OUT/"B01_R01_STAGE_A_PROMPTS.v1.json"
AFTER=OUT/"B01_R01_STAGE_B_CROSSWALK.v1.json"
EXPECTED_BASELINE="0f045746c8269b741e77ba7da8a6fb4569dd07f2"

def git_blob(path:Path)->str:
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()

def payload(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def collect():
    p=json.loads(SOURCE.read_text(encoding="utf-8"))
    assert p["status"]=="AUTHOR_PROPOSAL_ONLY__INTEGRATION_HOLD"
    assert p["academic_status"]==p["source_admission"]=="HOLD"
    assert p["counts"]["primary_instances"]==75
    assert p["counts"]["supplemental_instances"]==14
    assert p["counts"]["mixed_main_proposals"]==16
    assert p["counts"]["selected_canonical_mains"]==0
    items=[]
    for g in p["groups"]:
        assert g["canonical_main"] is None
        assert g["qualification"]=="HOLD"
        for e in g["base_instances"]:
            path=e["package_path"]
            assert git_blob(ROOT/path)==e["package_blob"],path
            pack=payload(path)
            assert pack["version"]==e["package_version"]
            cycle=next((t for t in pack["core1b"] if t["id"]==e["instance_cycle"]),None)
            assert cycle and cycle["kind"]=="INSTANCE"
            assert cycle["qrt_target_id"]==e["target_id"]
            items.append({"cycle":cycle,"source_kind":"PRIMARY",
                          "subtopic":e["subtopic_id"],"target":e["target_id"],
                          "package":path,"git_blob":e["package_blob"],
                          "version":e["package_version"],"author_cell":g["cell"]})
    for e in p["supplements"]:
        path=e["proposal_path"]
        assert git_blob(ROOT/path)==e["proposal_blob"],path
        pack=payload(path)
        assert pack["target"]["id"]==e["target_id"]
        assert pack["acceptance"]["release"]=="HOLD"
        cycle=next((t for t in pack["core1b"] if t["id"]==e["instance_cycle"]),None)
        assert cycle and cycle["kind"]=="INSTANCE"
        group=next((g for g in p["groups"]
                    if any(t["target_id"]==e["target_id"] for t in g["supplemental_instances"])),None)
        assert group
        items.append({"cycle":cycle,"source_kind":"SUPPLEMENTAL",
                      "subtopic":e["subtopic_id"],"target":e["target_id"],
                      "package":path,"git_blob":e["proposal_blob"],
                      "version":pack.get("version","CANDIDATE_SUPPLEMENT"),
                      "author_cell":group["cell"]})
    assert len(items)==89
    assert len(set(x["cycle"]["id"] for x in items))==89
    assert len(set(x["target"] for x in items))==89
    for item in items:
        stages=item["cycle"]["stages"]
        assert isinstance(stages.get("attempt"),str) and len(stages["attempt"].strip())>20
    # Stable author-side ordering; the blind packet exposes only opaque sequential IDs.
    items.sort(key=lambda x:x["cycle"]["id"])
    candidates=[]
    crosswalk=[]
    for index,item in enumerate(items,1):
        blind_id=f"B01-COLD-{index:03}"
        stages=item["cycle"]["stages"]
        prompt=stages["attempt"].strip()
        visual_needed=bool(re.search(r"\b(diagram|graph|plot|ray|sketch|figure|image|circuit|draw)\b",prompt,re.I))
        candidates.append({
            "blind_id":blind_id,
            "prompt":prompt,
            "figure_intake":"REVIEWER_MUST_CONFIRM_REQUIRED_VISUAL_PRESENT" if visual_needed
                           else "VISUAL_DEPENDENCY_NOT_YET_REVIEWED",
            "stage_a_submission":"FROZEN_INDEPENDENT_REVIEW_REQUIRED",
            "qualification":"HOLD"
        })
        crosswalk.append({
            "blind_id":blind_id,
            "target_id":item["target"],
            "instance_cycle":item["cycle"]["id"],
            "subtopic_id":item["subtopic"],
            "source_kind":item["source_kind"],
            "author_claimed_cell":item["author_cell"],
            "package_path":item["package"],
            "package_git_blob":item["git_blob"],
            "package_version":item["version"],
            "author_solution_access":"OPEN_ONLY_AFTER_STAGE_A_FROZEN",
            "independent_admission":"HOLD"
        })
    blind={
        "schema":"g9v41-b01-r01-cold-prompts/v1",
        "origin_authoring_baseline_sha":EXPECTED_BASELINE,
        "academic_status":"HOLD",
        "scope":"89 candidate INSTANCE prompts / 16 MAIN proposals separately held",
        "reviewer_instruction":"Do NOT open the Stage B crosswalk, author package, solution, D-band, QRT operation or predicted W before freezing your independent Stage A record. Derive science, assumptions, units, limits, counterexample, primary operation and five-factor evidence independently. Record unavailable diagrams as HOLD. A blind packet does not appoint a reviewer.",
        "intake_count":89,
        "items":candidates
    }
    post={
        "schema":"g9v41-b01-r01-after-freeze-crosswalk/v1",
        "origin_authoring_baseline_sha":EXPECTED_BASELINE,
        "access_gate":"ONLY_AFTER_SIGNED_STAGE_A_INDEPENDENT_REASONING",
        "academic_status":"HOLD",
        "independent_reviewer":"NOT_ASSIGNED",
        "admitted_count":0,
        "selected_canonical_mains":0,
        "rows":crosswalk
    }
    forbidden_keys={"qrt_target_id","band","factor_evidence","primary_operation",
                    "protected_work","decisive_route","reconstruct","author_claimed_cell",
                    "target_id","subtopic_id","package_path","instance_cycle"}
    assert all(not forbidden_keys.intersection(row) for row in candidates)
    assert all("Shortest valid route:" not in row["prompt"] for row in candidates)
    return blind,post

def main():
    blind,post=collect()
    OUT.mkdir(parents=True,exist_ok=True)
    BLIND.write_text(json.dumps(blind,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    AFTER.write_text(json.dumps(post,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"B01 R01 cold intake authored: 89 blind prompts, 89 sealed crosswalk links, 0 independent accepts.")

if __name__=="__main__":
    main()

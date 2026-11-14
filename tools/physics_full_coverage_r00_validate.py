#!/usr/bin/env python3
"""Verify all 132 PH01-PH12 audit rows against pinned source Git trees.

R00 exposure warning: structural and identity checks ONLY. This must never be
interpreted as source/academic approval or a 100%-covered science course.
CI checks out audit PR, then fetches the three pinned author heads.
"""
from __future__ import annotations
import csv
import functools
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT/"review/physics/ph01-ph12-full-coverage-r00"
EVID = DIR/"PHYSICS_PH01_PH12_EVIDENCE_R00.v1.json"
GAPS = DIR/"PHYSICS_PH01_PH12_GAPS_R00.v1.json"
CSV = DIR/"PHYSICS_PH01_PH12_MATRIX_R00.csv"

def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT)

@functools.lru_cache(maxsize=None)
def tree(sha):
    parsed = {}
    for line in git("ls-tree","-r",sha).decode("utf-8").splitlines():
        meta,path=line.split("\t",1)
        mode,kind,blob=meta.split()
        if kind=="blob":parsed[path]=blob
    return parsed

@functools.lru_cache(maxsize=None)
def content_json(sha,path):
    return json.loads(git("show",f"{sha}:{path}").decode("utf-8"))

def check_evidence(e, refs):
    if e is None:return
    assert e["ref"] in ("A","B","C"),e
    ref=refs[e["ref"]]
    assert tree(ref).get(e["path"])==e["blob"],e

def verify():
    audit=json.loads(EVID.read_text(encoding="utf-8"))
    gaps=json.loads(GAPS.read_text(encoding="utf-8"))
    refs=audit["pinned_commits"]
    assert audit["schema"]=="g9v41-physics-full-coverage-r00/v1"
    assert audit["mode"]=="R00_AUTHOR_EXPOSED_TECHNICAL_COVERAGE__NOT_R01"
    assert audit["disposition"]=="FAIL_FULL_COVERAGE__ACADEMIC_HOLD__SOURCE_HOLD"
    assert refs=={
        "A":"b5472589a067593e55edd23fd0866c21704d1574",
        "B":"7e1dcc8de824308f4643c3aa162725ad23440b95",
        "C":"6e7e3b39958605c69643260b06c6084b71838cbc",
        "M":"4f04677cb161d9eb32f6cd701411201ad0764421"}
    for entry in audit["pinned_source_blobs"].values():
        ref=refs[entry["ref"]]
        assert tree(ref).get(entry["path"])==entry["blob"],entry

    IA=content_json(refs["A"],audit["pinned_source_blobs"]["IA"]["path"])
    IB=content_json(refs["B"],audit["pinned_source_blobs"]["IB"]["path"])
    PH=content_json(refs["A"],audit["pinned_source_blobs"]["P"]["path"])
    QR=content_json(refs["A"],audit["pinned_source_blobs"]["Q"]["path"])
    U=content_json(refs["B"],audit["pinned_source_blobs"]["U"]["path"])
    S=content_json(refs["B"],audit["pinned_source_blobs"]["S"]["path"])
    R=content_json(refs["B"],audit["pinned_source_blobs"]["R"]["path"])
    V=content_json(refs["C"],audit["pinned_source_blobs"]["V"]["path"])
    M9=content_json(refs["C"],audit["pinned_source_blobs"]["D09"]["path"])
    M10=content_json(refs["C"],audit["pinned_source_blobs"]["D10"]["path"])
    L11=content_json(refs["B"],audit["pinned_source_blobs"]["L11"]["path"])
    L12=content_json(refs["B"],audit["pinned_source_blobs"]["L12"]["path"])

    ids=[s["subtopic_id"] for c in IA["chapters"] for s in c["subtopics"]]
    ids += [s["id"] for s in IB["subtopics"]]
    assert len(ids)==132 and len(set(ids))==132
    rows=audit["rows"]
    assert len(rows)==132 and {r["subtopic_id"] for r in rows}==set(ids)
    rowmap={r["subtopic_id"]:r for r in rows}
    csvrows=list(csv.DictReader(CSV.open(encoding="utf-8",newline="")))
    assert len(csvrows)==132 and [x["subtopic_id"] for x in csvrows]==[x["subtopic_id"] for x in rows]
    assert gaps["pins"]==refs and len(gaps["row_gaps"])==132
    assert {x["subtopic_id"] for x in gaps["row_gaps"]}==set(ids)

    associated_ph={}
    for x in QR["association_review"]:
        associated_ph.setdefault(x["subtopic_id"],set()).add(x["source_locator"])
    bsrc={x["subtopic_id"]:x for x in S["subtopic_rows"]}
    brows={}
    for x in R["targets"]:brows.setdefault(x["subtopic_id"],[]).append(x)
    cadv={x["subtopic_id"]:x for x in V["subtopics"]}
    cman={x["id"]:x for x in M9["subtopics"]+M10["subtopics"]}
    leads={}
    for p in (L11,L12):
        for s in p["subtopics"]:leads[s["id"]]=p

    assert U["counts"]["primary_instances"]==75
    assert U["counts"]["supplemental_instances"]==14
    assert U["counts"]["total_instances"]==len(R["targets"])==89
    assert U["counts"]["selected_canonical_mains"]==0
    assert U["counts"]["mixed_main_proposals"]==16
    assert len(PH["core1b"])==63 and sum(x["kind"]=="INSTANCE" for x in PH["core1b"])==53
    assert len(V["subtopics"])==29
    assert V["counts"]["total_MAIN_assessments"]==99
    assert (V["counts"]["D3"],V["counts"]["D4"],V["counts"]["below_cutoff_or_paused"])==(53,7,39)
    assert (M9["counts"]["subtopics"],M10["counts"]["subtopics"])==(12,17)
    assert (L11["subtopics"][0]["id"].startswith("PH11"),L12["subtopics"][0]["id"].startswith("PH12"))==(True,True)

    for row in rows:
        ident=row["subtopic_id"]
        topic=row["topic_id"]
        assert ident[:4]==topic
        for evidence in row["evidence"].values():
            check_evidence(evidence,refs)
        pr=row["presence"]
        assert pr["chapter_draft"]==bool(row["evidence"]["chapter"])
        assert pr["dedicated_core1a"]==bool(row["evidence"]["core1a"])
        assert pr["dedicated_core1b"]==bool(row["evidence"]["core1b"])
        assert row["source"]["exact_original_exam_admission"]=="HOLD"
        assert row["qrt"]["independent_qrt"]=="NOT_RUN"
        assert set(row["acceptance"])=={"B1","B2","B3","B4","B5","B6","B7","release"}
        assert all(x=="HOLD" for x in row["acceptance"].values())
        if pr["dedicated_core1a"] and pr["dedicated_core1b"]:
            assert row["audit_result"]=="HOLD_UNQUALIFIED"
        else:assert row["audit_result"]=="FAIL_UNAUTHORED_OR_NOT_ROUTED"
        gaps_for=next(x for x in gaps["row_gaps"] if x["subtopic_id"]==ident)
        assert gaps_for["missing"]==row["gap_codes"]
        if topic=="PH01":
            assert pr["dedicated_core1a"] and pr["dedicated_core1b"]
            assert len([x for x in PH["core1b"] if x["subtopic_id"]==ident])==row["qrt"]["authored_cycles"]
            assert row["source"]["association_count"]==len(associated_ph.get(ident,set()))
        elif topic in ("PH02","PH03","PH04","PH05","PH06"):
            assert not pr["chapter_draft"] and not pr["dedicated_core1a"] and not pr["dedicated_core1b"]
            assert not row["qrt"]["authored_cycles"]
        elif topic in ("PH07","PH08"):
            package=content_json(refs["B"],row["evidence"]["package"]["path"])
            assert package["status"]=="DRAFT_AUTHOR_EXPOSED"
            assert package["acceptance"]["release"]=="HOLD"
            assert len(package["core1a"])==1 and len(package["core1b"])==6
            assert package["subtopics"][0]["id"]==ident
            assert row["qrt"]["target_nominations"]==len(brows[ident])
            assert row["qrt"]["authored_cycles"]==6+2*(len(brows[ident])-3)
            assert row["source"]["association_count"]==(
                len(bsrc[ident]["primary_source_identities"])+
                len(bsrc[ident]["supporting_source_identities"]))
        elif topic in ("PH09","PH10"):
            pkg=content_json(refs["C"],row["evidence"]["package"]["path"])
            assert pkg["status"]=="DRAFT_AUTHOR_EXPOSED"
            assert pkg["acceptance"]["academic"]=="HOLD"
            assert pkg["acceptance"]["native_contract"]=="NOT_VALIDATED"
            assert len(pkg["core1b"])==6
            assert row["qrt"]["authored_cycles"]==cman[ident]["journeys"]==6
            assert row["qrt"]["d3_author_nominations"]==cadv[ident]["D3"]
            assert row["qrt"]["d4_author_nominations"]==cadv[ident]["D4"]
            assert row["source"]["association_count"]==len(cadv[ident]["related_core2"])
        else:
            assert topic in ("PH11","PH12")
            assert not pr["dedicated_core1a"] and not pr["dedicated_core1b"]
            embedded=ident in leads
            assert pr["embedded_core1a"]==pr["embedded_core1b"]==embedded
            if embedded:
                p=leads[ident]
                assert p["acceptance"]["release"]=="HOLD"
                assert row["qrt"]["authored_cycles"]==len([c for c in p["core1b"] if c["subtopic_id"]==ident])==6
            else: assert row["qrt"]["authored_cycles"]==0

    t=Counter(x["topic_id"] for x in rows)
    assert t==dict(zip(["PH01","PH02","PH03","PH04","PH05","PH06","PH07","PH08","PH09","PH10","PH11","PH12"],[8,8,7,9,7,10,12,13,12,17,14,15]))
    chapters=audit["chapters"]
    assert len(chapters)==12
    for summary in chapters:
        sub=[x for x in rows if x["topic_id"]==summary["topic_id"]]
        assert summary["planned"]==len(sub)
        assert summary["dedicated_core1a"]==sum(x["presence"]["dedicated_core1a"] for x in sub)
        assert summary["dedicated_core1b"]==sum(x["presence"]["dedicated_core1b"] for x in sub)
        assert summary["source_associated"]==sum(x["source"]["association_count"]>0 for x in sub)
    totals=audit["summary"]
    assert totals=={"planned":132,"chapter_drafts":91,"dedicated_core1a":62,
       "dedicated_core1b":62,"embedded_leads":4,"source_associated":49,
       "unqualified_full":132,"source_admitted":0,"fail_rows":70,"hold_rows":62}
    print("PHYSICS R00 PINNED EVIDENCE PASS: 132/132 inventory rows; 62 pairs, 4 embedded leads, "
          "49 source-associated rows (0 admitted); 70 missing native pairs; 0/132 B1–B7 qualified. "
          "100% COURSE COVERAGE FAIL / ACADEMIC HOLD.")

if __name__=="__main__":
    verify()

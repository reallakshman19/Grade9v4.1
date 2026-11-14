#!/usr/bin/env python3
"""R00: compare pinned main Physics source revisions with historical PH01 stack.

Byte and metadata verification only: never asserts exact official exam fidelity.
Requires two separately checked out repository trees; no network or source scans.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

PH = Path("nsejs/physics/curriculum/agent1/PH01")
PATHS = [
    "nsejs/data/physics-core2-candidates.v1.json",
    "nsejs/data/physics-core2-integrity.v1.json",
    "nsejs/data/physics-core2-source-evidence.v1.json",
    "nsejs/core2/question-map.v1.json",
]
TARGET_IDS = (
    ("2022-51-Q35","NSEJS-2022-P-Q35","g9:pcb:physics:nsejs-2022-physics-r1:003",None),
    ("2024-51-Q33","NSEJS-2024-P-Q33","g9:pcb:physics:nsejs-2024-physics-r1:001","NSEJS-24-MECH-02"),
    ("2024-51-Q60","NSEJS-2024-P-Q60","g9:pcb:physics:nsejs-2024-physics-r1:020",None),
)

def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

def load(root, rel):
    return json.loads((root/rel).read_text(encoding="utf-8"))

def diff_keys(a,b):
    return {k for k in a.keys()|b.keys() if a.get(k) != b.get(k)}

def verify(stack_root:Path, main_root:Path):
    audit = load(stack_root, PH/"PH01_R47_SOURCE_REVISION_R00.v1.json")
    assert audit["schema"] == "g9v41-ph01-r47-source-revision-reconciliation/v1"
    assert audit["inputs"]["historical_branch_head"] == "cd33ae87a8f4f2ea8a81dc6b200550d581272a66"
    assert audit["inputs"]["pinned_main_head"] == "44f29f8c077505db0616c91fbec2c90464e9c92f"
    for rel in PATHS:
        pins = audit["inputs"]["paths"][rel]
        assert blob(stack_root/rel) == pins["historical_git_blob_sha"], rel
        assert blob(main_root/rel) == pins["pinned_main_git_blob_sha"], rel
    oc, oi, oe, oq = [load(stack_root,p) for p in PATHS]
    nc, ni, ne, nq = [load(main_root,p) for p in PATHS]
    assert oq == nq and len(oq["questions"]) == 267
    physics = [q for q in nq["questions"] if q["subject"] == "PHYSICS"]
    assert len(physics) == audit["canonical"]["physics_rows"] == 95
    assert audit["canonical"]["byte_exact_blob_equal"] is True
    by_uid = {q["question_uid"]:q for q in physics}
    assert len(by_uid) == 95

    old = {q["source_id"]:q for q in oc["questions"]}
    new = {q["source_id"]:q for q in nc["questions"]}
    assert len(old) == len(new) == 50 and set(old) == set(new)
    counts = {"stem_sha256":0,"id":0,"source_figures":0,"figure_note":0}
    allow = set(counts)
    for sid,a in old.items():
        b = new[sid]
        changed = diff_keys(a,b)
        assert changed <= allow, (sid,sorted(changed))
        for key in changed:
            counts[key] += 1
    assert counts == {"stem_sha256":48,"id":4,"source_figures":3,"figure_note":5}
    assert not any(old[k]["stem"] != new[k]["stem"] for k in old)
    assert audit["corpus"]["actual_stems_options_answers_steps_unchanged"]
    assert audit["corpus"]["size"] == 50
    assert oi["academic_admission"] == ni["academic_admission"] == "HOLD"

    orig_integrity = {x["source_id"]:x for x in oi["items"]}
    current_integrity = {x["source_id"]:x for x in ni["items"]}
    assert set(orig_integrity) == set(current_integrity) == set(new)
    assert sum(bool(v["declared_matches_observed"]) for v in orig_integrity.values()) == 2
    assert sum(bool(v["declared_matches_observed"]) for v in current_integrity.values()) == 50
    changed_evidence = sum(
        orig_integrity[sid]["source_evidence_status"] != current_integrity[sid]["source_evidence_status"]
        for sid in orig_integrity
    )
    changed_figures = sum(
        orig_integrity[sid]["figure_dependency_missing"] != current_integrity[sid]["figure_dependency_missing"]
        for sid in orig_integrity
    )
    assert (changed_evidence,changed_figures) == (25,6)
    assert all(x["source_exact_fidelity"] not in ("ACCEPTED","APPROVED","VERIFIED")
               and x["academic_admission"] not in ("ACCEPTED","APPROVED","ADMITTED")
               for x in current_integrity.values())
    assert audit["integrity"]["academic_admission"] == "HOLD"

    older_ledger={x["source_id"]:x for x in oe["source_ledger"]}
    main_ledger={x["source_id"]:x for x in ne["source_ledger"]}
    assert len(older_ledger)==11 and len(main_ledger)==36
    assert all(main_ledger[k] == v for k,v in older_ledger.items())
    assert len(set(main_ledger)-set(older_ledger)) == 25
    assert all(x["digital_stem_options_figure_fidelity"] == "HOLD"
               and x["academic_admission"] == "HOLD" for x in main_ledger.values())
    assert ne["independent_academic_acceptance"] == "HOLD"

    targets = {x["loc"]:x for x in audit["targets"]}
    for loc,external,uid,candidate_id in TARGET_IDS:
        t=targets[loc]
        assert t["uid"] == uid and t["canonical_external_id"] == external
        assert by_uid[uid]["claimed_external_question_id"] == external
        assert by_uid[uid]["source_custody"] == by_uid[uid]["academic_admission"] == "HOLD"
        matches=[q for q in nc["questions"] if q["id"]==external]
        assert len(matches) == (1 if candidate_id else 0),loc
        if candidate_id:
            assert matches[0]["source_id"] == candidate_id
            assert t["bank_source_id"] == candidate_id
            assert t["bank_current_declared_sha256"] == matches[0]["stem_sha256"]
            assert current_integrity[candidate_id]["academic_admission"] == "NOT_ADMITTED"
        else:
            assert t["bank_source_id"] is None
        assert t["admission"] == t["exact_fidelity"] == "HOLD"
    assert audit["release"]["approved_to_merge"] is False
    print("R00_SOURCE_REVISION_PINNED_PASS: canonical 95 identical, 50 unchanged question stems, "
          "48 declared digest changes, 4 display-ID corrections, ledger 11->36, "
          "Q35/Q33/Q60 canonical match, exact source admission 0; ACADEMIC_HOLD")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stack-root",type=Path,required=True)
    p.add_argument("--main-root",type=Path,required=True)
    a=p.parse_args()
    verify(a.stack_root.resolve(),a.main_root.resolve())

if __name__=="__main__":
    main()

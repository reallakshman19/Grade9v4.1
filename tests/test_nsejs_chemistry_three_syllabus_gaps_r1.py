"""Owner-directed repairs for the three CBSE Chemistry content omissions in audit PR #27.

This suite checks authored source-visible content, exact task identity retention,
and scientifically bounded models. It does not grant independent academic/QRT PASS.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
B=ROOT/"curriculum/chemistry/agent-b"


def read(unit,subdir,extension):
    path=B/subdir/f"{unit}.{extension}"
    if extension.endswith("json"):
        return json.loads(path.read_text(encoding="utf-8"))
    return path.read_text(encoding="utf-8")


def section(unit,subtopic):
    doc=read(unit,"learner","reader.v0.1.0.json")
    return next(x for x in doc["sections"] if x["id"]==subtopic)


def cycles(unit,subtopic):
    doc=read(unit,"core1b","core1b.v0.1.0.json")
    return [x for x in doc["cycles"] if x["subtopic_ref"]==subtopic]


def test_c11_05_haloalkane_content_and_boundary_transfer():
    s=section("C11","CHEM-C11.05")
    text=" ".join(s["teaching"])
    assert "haloalkane" in text.lower()
    assert "CH₃Cl" in text and "bromoethane" in text
    assert "Cl⁻" in text and "covalent" in text
    assert "1-chloropropane" in text and "2-chloropropane" in text
    assert "functional" in text.lower()
    tasks=cycles("C11","CHEM-C11.05")
    assert len(tasks)==3
    task=next(x for x in tasks if x["operation"]=="REPRESENT")
    boundary=task["boundary_test"]
    assert "C₃H₇Cl" in boundary["prompt"]
    assert "independently draw" in boundary["prompt"].lower()
    assert "1-chloropropane" in boundary["answer"]
    assert "2-chloropropane" in boundary["answer"]
    assert "ethanol" in boundary["answer"].lower()
    assert task["attempt"]["first_attempt_must_be_saved_before_feedback"] is True
    assert task["academic_status"] not in ("QUALIFIED","PASS")
    manuscript=read("C11","textbook","core1a.md")
    assert "Halo functional groups" in manuscript
    assert "CH₃Cl" in manuscript


def test_c14_01_ozone_depletion_cause_and_distinction():
    s=section("C14","CHEM-C14.01")
    txt=" ".join(s["teaching"])
    for value in ("stratospheric ozone","depletion","chlorofluorocarbons","CFC","Cl·",
                  "ClO·","O₃","UV"):
        assert value.lower() in txt.lower()
    assert "ground-level" in txt
    task=next(x for x in cycles("C14","CHEM-C14.01") if x["operation"]=="MODEL")
    assert "stratospheric" in task["attempt"]["prompt"]
    assert "CFC" in task["attempt"]["prompt"]
    model=task["attempt"]["post_commit_closure"]["model_response"]
    assert "Cl·+O₃" in model and "ClO·+O" in model
    assert "satellite" in model.lower()
    assert "next month" in task["boundary_test"]["prompt"]
    assert "not instantaneous" in task["boundary_test"]["answer"]
    assert task["attempt"]["first_attempt_must_be_saved_before_feedback"] is True
    manuscript=read("C14","textbook","core1a.md")
    assert "Stratospheric ozone depletion" in manuscript


def test_c14_05_biodegradable_vs_nonbiodegradable():
    s=section("C14","CHEM-C14.05")
    txt=" ".join(s["teaching"])
    for term in ("Biodegradable","non-biodegradable","microorganisms","polyethylene",
                 "glass","recyclable","compost"):
        assert term.lower() in txt.lower()
    task=next(x for x in cycles("C14","CHEM-C14.05") if x["operation"]=="EXPLAIN")
    prompt=task["attempt"]["prompt"]
    assert "polyethylene" in prompt and "glass" in prompt
    assert "classify" in prompt.lower()
    assert "dry" in task["boundary_test"]["prompt"]
    assert "non-biodegradable" in task["attempt"]["post_commit_closure"]["model_response"]
    assert task["attempt"]["first_attempt_must_be_saved_before_feedback"] is True
    manuscript=read("C14","textbook","core1a.md")
    assert "Biodegradable versus non-biodegradable" in manuscript


def test_all_original_36_core1b_ids_preserved_and_hold():
    c11=read("C11","core1b","core1b.v0.1.0.json")
    c14=read("C14","core1b","core1b.v0.1.0.json")
    assert len(c11["cycles"])==21
    assert len(c14["cycles"])==15
    all_ids=[x["cycle_id"] for x in c11["cycles"]+c14["cycles"]]
    assert len(set(all_ids))==36
    assert all(x["source_role"]=="AUTHORED_PRACTICE" for x in c11["cycles"]+c14["cycles"])
    assert all(x["academic_status"] not in ("PASS","QUALIFIED")
               for x in c11["cycles"]+c14["cycles"])
    assert len(read("C11","learner","reader.v0.1.0.json")["sections"])==7
    assert len(read("C14","learner","reader.v0.1.0.json")["sections"])==5


def test_source_remediation_not_equal_to_independent_qualification():
    s11=section("C11","CHEM-C11.05")
    s14a=section("C14","CHEM-C14.01")
    s14e=section("C14","CHEM-C14.05")
    assert all(x.get("scope") for x in (s11,s14a,s14e))
    for u in ("C11","C14"):
        data=read(u,"learner","reader.v0.1.0.json")
        assert data["academic_status"]=="DRAFT_ACADEMIC_HOLD"


def test_c14_revised_qrt_slots_and_canonical_truth_match_native_pack():
    adapter=json.loads((ROOT/"curriculum/chemistry/adapters/C14.v1.json").read_text(encoding="utf-8"))
    canonical=json.loads((B/"canonical/C14.concepts.v0.1.0.json").read_text(encoding="utf-8"))
    pack=read("C14","core1b","core1b.v0.1.0.json")
    book=read("C14","learner","reader.v0.1.0.json")
    for cycle_id in ("CORE1B-C14-01-2","CORE1B-C14-05-1"):
        cycle=next(c for c in pack["cycles"] if c["cycle_id"]==cycle_id)
        sid=cycle["subtopic_ref"]
        sub=next(s for s in adapter["subtopics"] if s["subtopic_id"]==sid)
        q=next(q for q in sub["qrt_instances"]
               if q["instance_id"]==cycle["qrt_instance_ref"])
        concept=next(c for c in canonical["concepts"] if c["subtopic_id"]==sid)
        section=next(s for s in book["sections"] if s["id"]==sid)
        assert q["slots"]["X"]==cycle["attempt"]["prompt"]
        assert q["slots"]["W"]==cycle["attempt"]["protected_W"]
        assert q["slots"]["Z"]==cycle["attempt"]["post_commit_closure"]["model_response"]
        assert q["slots"]["Y"] in concept["scientific_exposition"]
        assert q["slots"]["Y"] in section["teaching"]
        assert q["status"]=="ACADEMIC_HOLD"
        assert concept["academic_status"]=="DRAFT_UNREVIEWED"


def test_c11_canonical_halo_authority_contains_both_isomers():
    canonical=json.loads((B/"canonical/C11.concepts.v0.1.0.json").read_text(encoding="utf-8"))
    c=next(x for x in canonical["concepts"] if x["subtopic_id"]=="CHEM-C11.05")
    prose=" ".join(c["scientific_exposition"])
    assert "haloalkane" in prose.lower()
    assert "1-chloropropane" in prose and "2-chloropropane" in prose
    assert c["academic_status"]=="DRAFT_UNREVIEWED"


def test_revised_c11_boundary_has_exact_author_evidence_blob_pin():
    import hashlib
    ledger=json.loads((B/"qrt/B02-C10-C11-author-coverage.v0.4.0.json").read_text(encoding="utf-8"))
    evidence=next(x for x in ledger["evidence_files"] if x["path"].endswith(
        "B02-C11-legacy-refinement-evidence.v0.4.0.json"))
    raw=(ROOT/evidence["path"]).read_bytes()
    assert hashlib.sha1(("blob "+str(len(raw))+"\\0").encode()+raw).hexdigest()==evidence["blob_sha"]
    records=json.loads(raw.decode("utf-8"))["records"]
    item=next(x for x in records if x["cycle_id"]=="CORE1B-C11-05-1-B02-R2")
    cycle=next(x for x in read("C11","core1b","core1b.v0.1.0.json")["cycles"]
               if x["cycle_id"]==item["cycle_id"])
    assert item["boundary_prompt"]==cycle["boundary_test"]["prompt"]
    assert item["boundary_answer"]==cycle["boundary_test"]["answer"]
    assert item["independent_review"]=="NOT_RUN" and item["academic_status"]=="HOLD"

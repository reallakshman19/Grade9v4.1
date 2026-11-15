"""Four original PH01/02/07/08 source-safe teaching and transfer case guards.

Static author QA only: no original-exam authentication or independent R01 Physics/QRT
approval may be inferred from a passing test.
"""
import json
import hashlib
from collections import Counter
from pathlib import Path
from math import sqrt

ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics"
CASES=PH/"quality-r1/cases.v1.json"
FOCUS={"PH01-M05":"PH01","PH02-F04":"PH02","PH07-02":"PH07","PH08-08":"PH08"}


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def test_four_original_constructions_are_distinct_and_scoped():
    d=load(CASES)
    assert d["schema"]=="g9v41-four-physics-deep-reconstruction/v1"
    assert d["status"]=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"
    assert d["existing_41_unit_scope"]=="FOUR_SELECTED_DEMONSTRATORS_ONLY__37_OTHERS_UNCHANGED"
    units=d["units"]
    assert len(units)==4 and {u["unit"] for u in units}==set(FOCUS)
    assert len({u["challenge"]["uid"] for u in units})==4
    assert len({u["revision"] for u in units})==4
    allowed={"MODEL":"D3.4","REPRESENT":"D3.5","JUSTIFY":"D3.7"}
    for u in units:
        assert u["chapter"]==FOCUS[u["unit"]]
        assert len(u["study"]["examples"])==3
        assert len({x["prompt"] for x in u["study"]["examples"]})==3
        assert all(len(x["solution"])>90 and len(x["check"])>20 for x in u["study"]["examples"])
        assert all(u["study"].get(k) for k in ("phenomenon","goal","model","assumptions","misconception","exit","figure"))
        assert u["source"]["role"]=="AUTHORED_TRANSFER"
        assert u["source"]["original_exam_admission"]=="HOLD"
        assert u["source"]["exact_original_paper"] is None
        assert u["source"]["independent_qrt"]=="NOT_RUN"
        assert u["adapter"]["cell"]==allowed[u["adapter"]["operation"]]
        assert u["adapter"]["status"]=="AUTHOR_PROPOSED_UNSCORED"
        assert u["adapter"]["five_factor_scores"] is None
        proposed=u["adapter"]["author_qrt_hypothesis"]
        assert proposed["status"]=="AUTHOR_EXPOSED__NOT_BLIND"
        assert proposed["proposed_band"]=="D3"
        assert proposed["independent_score"] is None and proposed["can_promote"] is False
        factors=proposed["factors"]
        assert set(factors)=={"concept_model_selection","representation_translation","reasoning_chain_length","algebra_computational_load","trap_exception_sensitivity"}
        assert all(isinstance(f["author_score"],int) and 0<=f["author_score"]<=2 and len(f["evidence"])>30 for f in factors.values())
        assert sum(f["author_score"] for f in factors.values())==proposed["proposed_total"]
        assert 6<=proposed["proposed_total"]<=7
        assert u["adapter"]["independent_witness_status"]=="HOLD"
        assert u["adapter"]["selected_as_canonical"] is False
        assert len(u["challenge"]["hints"])==2
        assert len(u["challenge"]["prompt"])>170
        assert len(u["challenge"]["reconstruct"])>180
        assert len(u["challenge"]["boundaryPrompt"])>120
        assert len(u["challenge"]["boundaryModel"])>120
        assert len(u["challenge"]["transfer_difference"])>80
        assert not any(u["challenge"]["prompt"]==x["prompt"] for x in u["study"]["examples"])


def test_four_versioned_topic_adapters_are_real_and_have_exact_task_join():
    d=load(CASES)
    expected_base={"PH01":53,"PH02":24,"PH07":43,"PH08":46}
    for u in d["units"]:
        a=load(ROOT/u["adapter"]["artifact_path"])
        assert a["status"]=="CANDIDATE_ONLY"
        assert a["topic_id"]==u["chapter"]
        assert a["version"]==u["adapter"]["version"]
        assert a["for_blueprint"]=="PHYS-QRT-BLUEPRINT 0.2.0"
        assert a["independent_qrt"]=="NOT_RUN"
        assert a["canonical_selection"]=="NOT_SELECTED"
        assert a["quality_r1_extension"]["task_id"]==u["challenge"]["uid"]
        assert a["quality_r1_extension"]["original_paper_admission"]=="HOLD"
        assert a["quality_r1_extension"]["five_factor_independent_scores"] is None
        assert a["quality_r1_extension"]["b1_b7"]=="HOLD"
        author=a["quality_r1_extension"]["author_five_factor_hypothesis"]
        assert author==u["adapter"]["author_qrt_hypothesis"]
        raw=CASES.read_bytes()
        git_blob=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+bytes([0])+raw).hexdigest()
        assert a["quality_r1_extension"]["r1_case_file_git_blob"]==git_blob
        assert a["quality_r1_extension"]["five_factor_independent_scores"] is None
        candidates=[i for c in a["cells"] for i in c["instance_ids"]]
        assert len(candidates)==expected_base[u["chapter"]]+1
        assert len(set(candidates))==len(candidates)
        assert sum(c["instance_ids"].count(u["challenge"]["uid"]) for c in a["cells"])==1
        assert any(c["cell_id"]==u["adapter"]["cell"] and
                   u["challenge"]["uid"] in c["instance_ids"] for c in a["cells"])


def test_four_chapter_catalog_links_integrated_without_replacing_existing():
    cat=load(PH/"learn/catalog.json")
    manifest=load(ROOT/"review/physics/ph01-ph02-ph07-ph08-r00/PHYSICS_41_ROUTE_AND_QUALITY_GATE_R00.v1.json")
    assert manifest["counts"]["subtopic_rows"]==41
    link_count=0
    for c in cat["chapters"]:
        if c["id"] in ("PH01","PH02","PH07","PH08"):
            assert c["sourceLedgerR1"]=="quality-r1/source.html?ph="+c["id"]
            for item in c["units"]:
                full=(c["id"]+"-"+item["id"] if c["id"] in ("PH01","PH02")
                      else item["id"])
                if full not in FOCUS:
                    assert not item.get("qualityR1"),full
                    continue
                links=item["qualityR1"]
                assert links["source_role"]=="AUTHORED_TRANSFER"
                assert links["independent_academic"]=="HOLD"
                assert links["study"]=="quality-r1/study.html?unit="+full
                assert links["practice"]=="quality-r1/challenge.html?unit="+full
                assert (PH/item["learn"]).is_file()
                assert (PH/item["practice"]).is_file()
                link_count+=1
    assert link_count==4
    assert len(manifest["rows"])==41
    assert Counter(r["chapter"] for r in manifest["rows"])==Counter({"PH01":8,"PH02":8,"PH07":12,"PH08":13})


def test_physics_arithmetic_independent_of_exercise_answer_text():
    assert [round((b[1]-a[1])/(b[0]-a[0]),2)
            for a,b in zip([(0,1),(2,9),(5,3)],[(2,9),(5,3),(7,3)])]==[4.0,-2.0,0.0]
    assert sum([8,6,0])==14 and 3-1==2
    assert 18-3*2==2*4+4==12
    assert (18-4)/(3+2)==(3*2+2*4)/(3+2)==2.8
    assert round(-30/200,2)==-0.15 and round(-40/400,2)==-0.10
    direct=sqrt(12**2+(7-3)**2)
    reflected=sqrt(12**2+(7+3)**2)
    assert 8.7 < (reflected-direct)/340*1000 < 8.8
    assert (reflected-direct)/340*1000 < 10


def test_runtime_enforces_order_and_identity_and_does_not_claim_exam_authenticity():
    js=(PH/"quality-r1/runtime.js").read_text(encoding="utf-8")
    assert 'crypto.subtle.digest("SHA-256"' in js
    assert 'record.first' in js and 'localStorage.setItem(key,raw)' in js
    assert 'localStorage.getItem(key)!==raw' in js
    assert 'linked_study_before_first' in js
    assert 'record.boundary' in js and 'boundary_attempt' in js
    assert 'if(!record?.first)' in js
    assert 'if(!record.reconstruction)return' in js
    assert 'if(!record.diagnosis)return' in js
    assert 'if(!record.repair)return' in js
    assert "No original examination stem" in js
    assert 'eval(' not in js
    for mode in ("study","challenge","source"):
        page=(PH/f"quality-r1/{mode}.html").read_text(encoding="utf-8")
        assert f'data-mode="{mode}"' in page
        assert 'type="module" src="./runtime.js"' in page
        assert '<iframe' not in page.lower()

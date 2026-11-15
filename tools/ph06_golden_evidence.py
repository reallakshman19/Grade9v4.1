"""Create the exact-head, deliberately HOLD R2 evidence packet from actual test logs.
No fabricated reviewer, original source bytes, Owner acceptance, or test receipts.
Run only after the dedicated science and Chromium tests complete successfully.
"""
import hashlib, json, subprocess, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P="nsejs/physics/ph06/"
C="nsejs/physics/curriculum/topics/PH06/"
U="nsejs/physics/textbook/PH06/"
A="artifacts/ph06-golden/"
HEAD=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
BASE="d96ee920f4ee249d74790c616cd273fde8d77382"
E=[]
def ev(role,path,marker,claim,warrant,tag=None,span=1):
    file=ROOT/path
    lines=file.read_text(encoding="utf-8").splitlines()
    i=next(i for i,s in enumerate(lines) if marker in s)
    excerpt="\n".join(lines[i:i+span]).strip()
    assert len(excerpt)>=24,(role,marker)
    uid=tag or role
    E.append(dict(id=uid,role=role,path=path,sha256=hashlib.sha256(file.read_bytes()).hexdigest(),start_line=i+1,end_line=i+span,excerpt=excerpt,claim=claim,why_this_proves_claim=warrant))
    return uid
def main():
    spec=importlib.util.spec_from_file_location("gate",ROOT/"docs/agent-entry/quality-gate-r2/verify_evidence_packet.py")
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    g=U+"U08/index.html";u=U+"U06/index.html";m=P+"model.v1.json";t=P+"task.v1.json";r=P+"reader.js";pr="nsejs/physics/core1/PH06/U08/index.html"
    def bind(role,path,marker,claim,warrant,span=1):
        return ev(role,path,marker,claim,warrant,span=span)
    science={
      "primary_derivation_ref":bind("SCIENCE_PRIMARY_DERIVATION",u,'<section id="mechanism">',"Upward pressure resultant equals weight of the displaced fluid.","Force balance on opposite horizontal faces gives pressure difference multiplied by area; fluid replacement generalizes it."),
      "independent_check_ref":bind("SCIENCE_INDEPENDENT_CHECK",m,'"alternative":',"Pressure-walk independently recomputes author numerical buoyancy.","Top and bottom gauge pressure differences give 26 and 34 N, independently of the displaced-length algebra; not independent reviewer."),
      "units_signs_ref":bind("SCIENCE_UNITS_AND_SIGNS",u,'<section id="prerequisite">',"Finite slice balance establishes pressure units and positive depth.","Mass of a liquid slice is density times volume; force balance cancels area and gives pressure in pascals."),
      "assumptions_limit_ref":bind("SCIENCE_ASSUMPTIONS_AND_LIMIT",m,'"conditions":',"Explicit model conditions exclude vertical external guide support.","Only fluid pressure and weight contribute vertically under stated conditions; rotational stability is outside the constraint."),
      "counterexample_ref":bind("SCIENCE_COUNTEREXAMPLE",g,'<h3>Work each regime',"Wrong continued emerged model predicts impossible immersion lengths.","Computed bottom depth 44 cm exceeds the 40 cm height and requires a new fully submerged intersection model."),
      "model_version":"r2-20261115"}
    a={"student_ready_path":g,
       "phenomenon_ref":bind("CORE1A_PHENOMENON",g,'<section id="phenomenon">',"Two-liquid interface is not a rigid supporting surface.","The learner-facing explanation ties vertical force to actual fluid displacement rather than contact with an interface."),
       "prerequisite_ref":bind("CORE1A_PREREQUISITE",g,'<section id="prerequisite">',"The lesson recalls force balance and links prerequisite teaching.","U06 explains hydrostatic pressure; the U08 passage specifies upward sign and no vertical support."),
       "causal_explanation_ref":bind("CORE1A_CAUSAL_EXPLANATION",g,'<section id="mechanism">',"Add the masses of each displaced fluid region without overlap.","Pressure continuity and fluid replacement produce the sum of weights of the actually displaced volumes."),
       "diagram_ref":bind("CORE1A_DIAGRAM",P+"figures/u08-regimes.svg","Four load regimes","Four guide states share a common scale for height and layer depth.","The geometry distinguishes upper-only, emerged interface, fully immersed and no equilibrium; inspection remains required."),
       "foundation_ref":bind("CORE1A_WORKED_FOUNDATION",g,'<section id="foundation">',"Foundation example computes buoyancy from prescribed partition.","One litre in each liquid contributes separate masses; addition gives eighteen newtons."),
       "connected_ref":bind("CORE1A_WORKED_CONNECTED",g,'<section id="connected">',"Connected example determines the required direction of a tether.","Displaced mass exceeds body mass, so the external support must point downward to balance upward resultant."),
       "advanced_ref":bind("CORE1A_WORKED_ADVANCED",g,'<h3>First find the three transition loads',"Three explicit transition loads delimit the equilibrium regimes.","Mass capacity at each geometric boundary distinguishes which lengths can be used in the next calculation."),
       "misconception_ref":bind("CORE1A_MISCONCEPTION_REPAIR",g,'<section id="limits">',"Arithmetic mean fails when displaced volumes are unequal.","The volume weighted density is necessary when two regions differ in volume; an emerged part is not liquid volume."),
       "synthesis_ref":bind("CORE1A_SYNTHESIS",g,'<section id="exit">',"The exit check changes the fluid composition rather than task numbers.","Replacing the lower liquid removes the supporting density contrast; the learner must test total displacement capacity."),
       "self_teaching_test":{"learner_can_explain":"An author cold-review prompt asks whether two-liquid support survives replacing the lower fluid by the upper one; the learner must compare mass with maximum displaced mass, not recall a number.","novice_dependency_check":"A novice must first convert centimetre area and litre volume, distinguish gauge pressure and force, derive hydrostatic force from a fluid slice, and understand actual intersection lengths. These are taught in U06 and linked U08; independent novice testing has not occurred.","unassisted_question":"A sealed 1.1 kg body of volume one litre is supported by two liquids, densities 900 and 1300 kg per cubic metre. Can it remain unsupported if the lower liquid is replaced by the upper one?","expected_reasoning":"With the lower liquid replaced, the maximum displaced mass is density multiplied by total body volume, only 0.9 kg. The body requires 1.1 kg of displaced mass. No submerged position in this single uniform liquid can supply enough buoyancy without support.","counterfactual_reasoning":"If the lower liquid remains denser, some partition can support the required mass provided the geometry permits it. If extra upward support is introduced or the body changes volume, the two-force equilibrium equation no longer alone determines the state."}}
    b={"student_ready_path":pr,
       "anchor_problem":"Known interface depth 20 cm; upright 40 cm prism of area 50 cm squared, densities 600 and 1000. Calculate the four equilibrium regimes for given loads using the known boundaries.",
       "new_problem":json.loads((ROOT/t).read_text())["prompt"],
       "anchor_crux":"Given fixed geometry and layer depth, determine support capacities at the boundaries and use each prescribed load to calculate the corresponding forward equilibrium state.",
       "new_crux":"Use a measured initial equilibrium and unknown interface thickness as an inverse constraint before deciding the new physical immersion regime under an added load.",
       "novelty_mechanism":"INVERSE_CONSTRAINT","numeric_swap_rejected":"Changing numbers in the forward guided case does not recover the missing interface depth. The reserved task must reconstruct the initial geometric partition from observed bottom depth and mass before considering the changed state.",
       "fresh_task_ref":bind("CORE1B_FRESH_TASK",t,'"prompt":',"Fresh assessment begins from an unknown layer thickness.","The measured equilibrium supplies an inverse constraint that is absent from the forward guided example."),
       "model_route_ref":bind("CORE1B_MODEL_ROUTE",m,'"reconstruction":',"Reconstruction solves the inverse and checks the new regime.","The worked model calculates top-flush capacity, rejects the previous regime and verifies the resulting displacement."),
       "boundary_ref":bind("CORE1B_BOUNDARY_TRANSFER",m,'"boundaryPrompt":',"Removing load leads to a different upper-only equilibrium.","The learner must compare with the interface threshold and select a different volume equation rather than reusing the loaded equation."),
       "hint_nonleak_ref":bind("CORE1B_HINT_NONLEAK",r,'if(stage<2)',"Precommit stages have no model or hint rendering branch.","Predict and Attempt render only task prompt and neutral fields; hints occur in the saved stage two branch.",span=5),
       "first_save_ref":bind("CORE1B_FIRST_SAVE",r,'const save=async fn',"Storage writes are serialized and checked before rendering.","The lock re-reads previous state, persists the serialized value and compares actual stored bytes before drawing."),
       "revision_return_ref":bind("CORE1B_REVISION_RETURN",r,'btn("sourceReturn"',"Exact source return requires matching source first-response chronology.","The callback checks source identity and first timestamp against the task start and writes a separate return receipt."),
       "stages":{"predict":"Commit an independent written prediction as a separate stage before seeing the attempt form.","attempt":"Preserve structured model choices, numerical values and the written reasoning with a durable local first save.","reconstruct":"Compare saved fields, ordered optional hints and the author worked model, including the pressure walk and solved geometry.","diagnose":"Suggest the first mismatched model/value field from the saved response and require learner-owned explanation.","repair":"Save the revised reasoning separately and preserve the original model and numeric entries for comparison.","boundary_test":"Commit a changed load and upper-only model before feedback; compare structured response and changed-condition SVG."},
       "hints":{"H1":json.loads((ROOT/m).read_text())["hints"][0],"H2":json.loads((ROOT/m).read_text())["hints"][1],"H3":json.loads((ROOT/m).read_text())["hints"][2],"blocked_until_first_save":True},
       "multiple_subtopic_main":{"contract_applies":False,"instance_ids":["AUTHORED-PH06-U08-GOLDEN-MODEL-R1"],"subtopic_ids":["PH06-U06","PH06-U08"],"integrated_reasoning":"This is the scoped Golden INSTANCE with a prerequisite lesson, not a multi-subtopic MAIN; the v1.1 MAIN coverage gate remains unresolved and cannot be waived by the author."}}
    ev("CORE1B_FRESH_TASK",pr,'<div id="root"',"Actual native challenge route mounts the protected reader.","The HTML supplies the exact learner destination and script, separately from the author model payload.",tag="CORE1B_ROUTE")
    core2={"identity":"NSEJS-2022-C51-Q38","source_role":"DIRECT_EXAM_CANDIDATE",
       "stem_figure_ref":bind("CORE2_STEM_AND_FIGURE",C+"golden-source-review.v1.json",'"notes":',"Source locator is observed, not verified original source bytes.","Archive visual and indexed publisher text were examined; exact stem and rights are not admitted or reproduced."),
       "derivation_key_ref":bind("CORE2_REASONING_KEY",C+"golden-source-review.v1.json",'"author_check":',"Author calculation is consistent with the observed final key.","Weighted equal volumes give the stated candidate density; publisher byte custody and independent check remain HOLD."),
       "figure_need":"NOT_REQUIRED","figure_status":"NO_FIGURE_NEEDED","original_source_fidelity":"NOT_SELF_APPROVED","exam_question_count_claim":0}
    neg=[]
    for kind,log,mutation,expected in [
        ("WRONG_DIMENSION","science-tests.txt","Omit the density factor from the hydrostatic pressure difference.","Incorrect numerical pressure difference is rejected by independent arithmetic."),
        ("WRONG_SIGN_OR_LIMIT","science-tests.txt","Continue the emerged equation beyond the allowed total float height.","The result must violate the geometry and fail actual force balance."),
        ("SAVE_FAILURE","browser-tests.txt","Inject localStorage write denial after prediction but before first commit.","The first save must fail closed and no reconstruction control may appear."),
        ("BAD_SOURCE_FIGURE","browser-tests.txt","Return HTTP 404 for the required authored question-facing SVG.","The affected challenge is unavailable; no hint or reveal may appear."),
        ("STALE_REVISION","browser-tests.txt","Alter the actual prompt SVG bytes after saving an earlier attempt.","Changed digest must start a new protected attempt without old reconstruction."),
        ("HINT_LEAK","browser-tests.txt","Inspect the actual Predict and Attempt DOM before a saved reasoning response.","No solved value, hint or reconstruction control may appear before commitment.")]:
        ref=ev("QA_NEGATIVE_LOG",A+log,kind+" ",mutation,expected+" The log is from the actual executed negative case.",tag="NEG-"+kind)
        line=next(e["excerpt"] for e in E if e["id"]==ref)
        neg.append(dict(case=kind,mutation=mutation,expected_failure=expected,observed_failure=line,reproduction_command="python tools/ph06_golden_browser_qa.py" if log.startswith("browser") else "python -m pytest -q -s tests/test_ph06_golden_r1.py",log_ref=ref))
    browser={"head_sha":HEAD,"portrait_receipt_ref":ev("QA_BROWSER_RECEIPT",A+"browser-tests.txt","1000x1600 HTTP Chromium PASS","Portrait tablet journey executed against local HTTP.","The log records the actual completed learner journey, not a test-count proxy.",tag="PORTRAIT"),"landscape_receipt_ref":ev("QA_BROWSER_RECEIPT",A+"browser-tests.txt","1600x1000 HTTP Chromium PASS","Landscape tablet journey executed against local HTTP.","The log records the actual completed learner journey, not academic acceptance.",tag="LANDSCAPE"),"keyboard_and_touch":"PASS","storage_failure":"PASS","stale_revision":"PASS","pre_first_help":"PASS","figure_render":"PASS","outcome":"MECHANICAL_ONLY_NOT_ACADEMIC_APPROVAL"}
    packet={"schema_version":"g9v41-physics-evidence-packet/v2","task":{"task_id":"G9V41-PH06-GOLDEN-R2","owner_workpack":"Issue-50-Golden","topic_id":"PH06","subtopic_id":"PH06-U08","base_sha":BASE,"head_sha":HEAD,"contract_version":"1.1.0","blueprint_version":"0.2.0-DRAFT_OWNER_REVIEW","golden_sample_sha":HEAD,"delivery_kind":"GOLDEN_SAMPLE"},"declarations":{"source_status":"HOLD","science_status":"AUTHOR_UNVERIFIED","qrt_status":"AUTHOR_PROPOSED","academic_status":"HOLD","owner_release_status":"NOT_REQUESTED","reviewer_independent":False},"evidence":E,"science":science,"core1a":a,"core1b":b,"core2":core2,"negative_tests":neg,"browser":browser,"self_audit":{"red_team_hypotheses":["A positive solution from the wrong emerged geometry can violate the actual full-height constraint; test the piecewise volume intersection directly.","An incorrect initial interface model can accidentally produce a final numeric depth; compare earlier fields and require written justification separately.","A prior transfer completion must never count as a new source-first journey after a later source attempt; test chronological binding."],"known_defects":["Publisher source bytes and rights unresolved; no native SL1/SL2 checker receipt.","No independent science, QRT or cold learner evidence; no Owner-accepted Golden.","Full multi-subtopic MAIN outside scoped instance; native contract decision unresolved.","Browser screenshots need independent visual inspection; static client answer payload is not secure."],"rejected_alternatives":["A duplicate given-partition challenge would merely substitute numbers and would not require the independent inverse interface reconstruction.","Copying the old WPE reset and side-by-side answer consultation would weaken first-attempt integrity and confound the learner evidence."],"evidence_completeness":"INCOMPLETE_HOLD","self_disposition":"CANDIDATE_REVIEW_REQUESTED","review_requested":True}}
    # Exercise the actual validator on two injected faults, preserve original draft bytes.
    import copy
    bad=copy.deepcopy(packet);bad["core1b"]["new_problem"]=bad["core1b"]["anchor_problem"]
    assert "NUMERIC_REPARAMETERIZATION_DETECTED" in gate.validate(bad,ROOT)["findings"]
    lesson=ROOT/g;original=lesson.read_bytes()
    try:
        lesson.write_bytes(original+b"\n<!-- {Reviewed} -->\n")
        assert any(x.startswith("UNSUPPORTED_REVIEW_BADGE:") for x in gate.validate(packet,ROOT)["findings"])
    finally:lesson.write_bytes(original)
    (ROOT/(A+"validator-negatives.txt")).write_text("NUMERIC_CLONE REJECTED: injected duplicate problem detected by repository R2 validator.\nFALSE_REVIEW_BADGE REJECTED: injected unapproved review badge detected by repository R2 validator.\n",encoding="utf-8")
    for kind,mutation in [("NUMERIC_CLONE","Replace the new problem with the guided anchor in an actual packet."),("FALSE_REVIEW_BADGE","Inject an unsupported review badge into the actual lesson HTML temporarily.")]:
        ref=ev("QA_NEGATIVE_LOG",A+"validator-negatives.txt",kind,mutation,"Repository validator must detect the injected contradiction without accepting it.",tag="NEG-"+kind)
        line=next(e["excerpt"] for e in E if e["id"]==ref)
        neg.append(dict(case=kind,mutation=mutation,expected_failure="The native R2 validator must reject the injected contradiction.",observed_failure=line,reproduction_command="python tools/ph06_golden_evidence.py",log_ref=ref))
    result=gate.validate(packet,ROOT)
    (ROOT/(A+"author-packet.json")).write_text(json.dumps(packet,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/(A+"validator-result.json")).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    assert result["mechanical_status"]=="BLOCKED" and result["academic_status"]=="HOLD"
    assert not any(x.startswith("SCHEMA:") for x in result["findings"]),result
if __name__=="__main__":main()

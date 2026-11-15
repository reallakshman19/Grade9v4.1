"""Native PH11-07 R4 technical candidate controls; never an academic acceptance."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"nsejs/physics/curriculum/topics/PH11/subtopics/PH11-07"
HTML=(BASE/"core1b.html").read_text(encoding="utf-8")
LESSON=(BASE/"core1a.html").read_text(encoding="utf-8")
JS=(BASE/"native-attempt.js").read_text(encoding="utf-8")
PROMPT=(BASE/"prompt.v1.json").read_text(encoding="utf-8")
MODEL=(BASE/"postattempt.v1.json").read_text(encoding="utf-8")

def sha(raw):
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def blob(raw):
    data=raw.encode("utf-8")
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def test_exact_trusted_expected_sha256_and_git_blob_pins_in_runtime():
    for name,raw in [("prompt",PROMPT),("postattempt",MODEL)]:
        assert f'{name}_sha256: "{sha(raw)}"' in JS
        assert f'{name}: "{blob(raw)}"' in JS
        assert len(sha(raw))==64 and len(blob(raw))==40
    assert 'strongDigest!==pinSha256' in JS
    assert 'gitBlobDigest(raw)!==pin' in JS
    assert 'PIN_MISMATCH:' in JS
    assert 'crypto.subtle.digest("SHA-256"' in JS
    assert 'crypto.subtle.digest("SHA-1"' in JS

def test_pre_attempt_assets_contain_only_original_prompts():
    prompt=json.loads(PROMPT);model=json.loads(MODEL)
    assert prompt["source"]["role"]=="ORIGINAL_AUTHOR_ONLY_NOT_NSEJS"
    assert prompt["status"]=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"
    assert "reconstruct" not in PROMPT and "boundaryModel" not in PROMPT
    assert not re.search(r'(?:unknown resistance|unknown branch).*?(?:2 ohm|2 Ω)',PROMPT,flags=re.I|re.S)
    assert "R=6/3=2 ohm" in MODEL
    assert "2 A < I_total < 18/3=6 A" in MODEL
    assert "free-text" in MODEL.lower()
    assert "fetchPinned(\"postattempt.v1.json\",PIN.postattempt,PIN.postattempt_sha256)" in JS
    assert 'if(feedback||blocked||!state?.first||loadingFeedback)' in JS
    assert JS.index('if(feedback||blocked||!state?.first||loadingFeedback)') < JS.index(
        'fetchPinned("postattempt.v1.json"')
    assert "async function start()" in JS

def test_native_learner_routes_do_not_link_to_review_or_adapter():
    index=(ROOT/"nsejs/physics/curriculum/topics/PH11/index.html").read_text(encoding="utf-8")
    for text in [HTML,LESSON,index]:
        assert 'href="../../../../../review/' not in text
        assert "review/physics/" not in text
        assert 'href="../../topic-adapter.PH11' not in text
    assert 'src="./native-attempt.js"' in HTML
    assert "subtopics/PH11-07/core1b.html" in index
    assert 'href="core1b.html"' in LESSON
    assert "ACADEMIC HOLD" in HTML and "ACADEMIC HOLD" in LESSON
    assert '<iframe' not in HTML.lower()

def test_source_prediction_attempt_and_stage_writes_are_distinct_and_monotonic():
    assert 'navigator.locks.request(KEY,{mode:"exclusive"}' in JS
    assert 'const latest=freshRead(); // never write a stale cached state' in JS
    assert 'if(latest[stage]!==null' in JS
    assert 'localStorage.getItem(KEY)!==raw' in JS
    assert 'window.addEventListener("storage"' in JS
    assert 'commit("source"' in JS and 'commit("prediction"' in JS
    assert 'commit("first"' in JS
    assert 'commit("reconstructionExposure"' in JS
    assert 'commit("reconstruction"' in JS
    assert 'commit("diagnosis"' in JS
    assert 'commit("repair"' in JS
    assert 'commit("boundary"' in JS
    assert 'commit("boundaryRepair"' in JS
    assert 'commit("sourceReturn"' in JS
    assert 'if(!feedback||!state?.reconstructionExposure' in JS
    assert "editable browser storage" in JS.lower() or "browser-local" in HTML.lower()

def test_diagnosis_and_boundary_use_actual_selected_model_and_values():
    assert 'const modelRight=f.model==="mixed";' in JS
    for scenario in ("right_values_wrong_model","wrong_topology","correct_model_wrong_values","matched"):
        assert scenario in JS
        assert scenario in MODEL
    assert 'boundaryCheck(opts)' in JS
    assert 'opts.high==="no"&&opts.low==="no"' in JS
    assert 'matches(Number(opts.lower),2)' in JS
    assert 'matches(Number(opts.upper),6)' in JS
    assert '"return-panel",Boolean(state.boundary?.checked||state.boundaryRepair?.checked)' in JS
    assert "free_text_graded:false" in JS
    assert "assisted:true" in JS
    assert "grading:\"UNGRADED_TEXT\"" in JS

def test_progressive_teaching_and_strict_finite_feasibility():
    assert "Worked inverse construction" in LESSON
    assert "V/(R_s+R_k)" in LESSON
    assert "0 &lt; R_p &lt; R_k" in LESSON
    assert "5/3 A &lt; I_total &lt; 5 A" in LESSON
    assert "as X tends to infinity" in LESSON
    assert "as x tends to zero" in LESSON.lower()
    # 20V example, 4Ω series + known8Ω || unknown4Ω, measured source3A
    rp=Fraction(8*4,8+4)
    assert rp==Fraction(8,3)
    assert Fraction(20,1)/(4+rp)==3
    assert 20/12 < 3 < 20/4
    assert 2 < 4 < 6   # 18V 3Ω + 6Ω || 2Ω fresh task sits in feasible interval

def test_publication_candidate_is_not_authorized_release_or_exam():
    prompt=json.loads(PROMPT);model=json.loads(MODEL)
    assert prompt["review_gate"].startswith("SCIENCE_AND_QRT_INDEPENDENT_HOLD")
    assert "ACADEMIC_HOLD" in model["status"]
    assert "HOLD" in HTML and "HOLD" in LESSON
    assert "not secure examination custody" in LESSON


def test_staged_candidate_dependency_manifest_is_exact_and_not_release_authority():
    manifest=ROOT/"review/physics/ph11-07-r4/NATIVE_PUBLICATION_STAGING_MANIFEST_R4.json"
    d=json.loads(manifest.read_text(encoding="utf-8"))
    assert d["schema"]=="g9v41-ph11-07-native-candidate-staged-deps/v1"
    assert d["status"]=="AUTHOR_EXPOSED_REVIEW_ONLY__ACADEMIC_HOLD"
    assert d["trusted_production_gate"]=="NOT_RUN_ON_STACKED_PR_AND_NOT_AUTHORIZED"
    assert d["release_manifest_authority"]=="NONE_NO_SIGNATURE"
    expected={"core1a.html","core1b.html","native-attempt.js",
              "prompt.v1.json","postattempt.v1.json","textbook-reader.css"}
    assert {Path(x["path"]).name for x in d["dependencies"]}==expected
    assert len(d["dependencies"])==len(expected)
    for item in d["dependencies"]:
        assert not item["path"].startswith(("review/","tests/","tools/"))
        src=ROOT/item["path"]
        assert src.is_file(),src
        assert blob(src.read_text(encoding="utf-8"))==item["git_blob_sha"]
    assert "review/**" in d["network_phase_policy"]["publication_exclude"]
    assert "NOT" in d["network_phase_policy"]["before_source_first"]

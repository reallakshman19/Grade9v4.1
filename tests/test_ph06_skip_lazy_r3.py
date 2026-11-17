"""PH06 R3 no-credit native skips and after-first asset gating.

Technical author-side checks only. No scientific/QRT/academic admission.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
PH=ROOT/"nsejs/physics/ph06"

def blob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

def test_lazy_manifest_exact_asset_pins_and_historical_r2_reader():
    manifest=json.loads((PH/"protected-assets.r3.json").read_text())
    task=json.loads((PH/"task.v1.json").read_text())
    assert manifest["schema"]=="g9v41-ph06-protected-assets/v1"
    assert manifest["task_uid"]==task["uid"]
    assert manifest["task_revision"]==task["revision"]
    assert manifest["status"]=="AUTHOR_CANDIDATE_ACADEMIC_HOLD"
    assert manifest["model_blob_sha1"]==blob(PH/"model.v1.json")
    assert manifest["solution_blob_sha1"]==blob(PH/"figures/u08-reconstruct.svg")
    assert manifest["boundary_blob_sha1"]==blob(PH/"figures/u08-boundary.svg")
    legacy=PH/"reader-r2-legacy.js"
    assert blob(legacy)=="724d6a90570a91d422a5997456bfa77c8f13c3f7"
    old_page=(PH/"legacy-u08.html").read_text()
    assert 'src="reader-r2-legacy.js"' in old_page
    assert 'data-role="challenge"' in old_page
    assert "Earlier R2 attempts" in (ROOT/"nsejs/physics/core1/PH06/U08/index.html").read_text()

def test_no_answer_asset_requested_before_saved_first_attempt_in_native_reader():
    r=(PH/"reader.js").read_text()
    assert 'fetchText("protected-assets.r3.json")' in r
    assert 'JSON.stringify([raw,sourceRaw,figure,manifestRaw])' in r
    assert 'key="G9V41:PH06:R3:"+task.uid+":"+hash' in r
    assert "async function ensurePost()" in r
    assert 'if(stage>=2){if(!r?.first)throw Error("Postattempt access without durable first response");await ensurePost();}' in r
    assert r.index('async function ensurePost()') < r.index('async function render(r)')
    # model JSON and answer diagrams are accessed only inside post-commit function.
    before=r[r.index("const raw=await fetchText(\"task.v1.json\")"):r.index("async function ensurePost()")]
    assert 'fetchText("model.v1.json")' not in before
    assert 'fetchText("figures/u08-reconstruct.svg")' not in before
    assert "await sha1Blob(modelRaw)" in r and "manifest.model_blob_sha1" in r
    assert 'throw Error("Postattempt asset byte pin mismatch")' in r
    assert 'await render(next)' in r
    assert 'if(stage>=2)' in r
    assert 'if(!r?.first)' in r

def test_six_stage_skip_unanswered_and_no_source_credit_contract():
    r=(PH/"reader.js").read_text()
    for token in ('nativeSkipButton("prediction")','nativeSkipButton("attempt")',
                  'nativeSkipButton("diagnosis")','nativeSkipButton("repair")',
                  'nativeSkipButton("boundary")','nativeSkipButton(prefix+x.id)'):
        assert token in r, token
    assert 'field.dataset.skipped=String(next)' in r
    assert 'field.disabled=next' in r
    assert 'aria-pressed' in r and 'Undo skip' in r
    assert 'return[x.id,null]' in r
    assert 'reasoning:why,fields:entries,skipped:skips' in r
    assert 'diagnosis:{field:why===null?"skipped":field,why,skipped:why===null}' in r
    assert 'repairSkipped:why===null' in r
    assert 'boundary:{why,fields:vals,skipped,at:timestamp()}' in r
    assert 'r.first.skipped?.length?"Insufficient evidence' in r
    assert 'no misconception inferred' in r
    assert 'if(r.predictionSkipped||r.first.skipped?.length||r.diagnosis?.skipped||r.repairSkipped||r.boundary?.skipped?.length)return' in r
    assert 'r.first?.reasoning' not in r[r.index("async function render(r)"):r.index("function ensurePost") if "function ensurePost" in r[r.index("async function render(r)"):] else len(r)]
    assert "academic" in (PH/"task.v1.json").read_text()

def test_manifest_mutations_fail_closed_against_actual_bytes():
    manifest=json.loads((PH/"protected-assets.r3.json").read_text())
    model_raw=(PH/"model.v1.json").read_bytes()
    altered=model_raw+b" "
    def sha1_blob(raw):
        return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
    assert sha1_blob(altered)!=manifest["model_blob_sha1"]
    svg=(PH/"figures/u08-reconstruct.svg").read_bytes()
    assert sha1_blob(svg+b"<!-- altered -->")!=manifest["solution_blob_sha1"]
    assert not json.loads((PH/"source.v1.json").read_text())["qualified"]

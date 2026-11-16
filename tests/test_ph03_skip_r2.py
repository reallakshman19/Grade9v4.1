"""PH03 field-level Skip contract: technical review only, academic HOLD."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "nsejs/physics/ph03/source-led-r2"
JS = (R2 / "reader.js").read_text(encoding="utf-8")
HTML = (R2 / "index.html").read_text(encoding="utf-8")


def test_explicit_skip_controls_cover_every_mandatory_prose_field():
    for field in (
        "prediction", "reason", "diagtext", "repairreason",
        "boundaryreason", "retryreason"
    ):
        assert f'textArea("{field}"' in JS
    assert 'data-skip-target=' in JS
    assert 'Undo skip' in JS
    assert 'aria-pressed' in JS
    assert 'aria-label' in JS
    assert 'textArea(' in JS and 'skipButton(' in JS


def test_numeric_and_choice_inputs_have_skip_option_without_guessing():
    assert 'const fieldHTML=' in JS
    assert 'skipButton(id,disabled,wasSkipped)' in JS
    assert 'const skippedFields=' in JS
    assert 'const selection=' in JS
    assert 'skipButton("fieldset-"+name,disabled,wasSkipped)' in JS
    assert 'selected=name=>skipped("fieldset-"+name)?null' in JS


def test_missing_is_not_graded_as_correct_or_fabricated_value():
    assert 'if(skipped(id)){result[k]=null;continue}' in JS
    assert 'Object.values(fields).some(x=>x===null)' in JS
    assert 'return "insufficient"' in JS
    assert 'ungraded and earns no mastery credit' in JS
    assert 'Some first fields were skipped; no correct-answer credit' in JS
    assert 'reason=skipped("repairreason")?null' in JS
    assert 'reason=skipped("boundaryreason")?null' in JS
    assert 'const prediction=skipped("prediction")?null' in JS
    assert 'skipped:sk' in JS


def test_skips_are_explicit_separate_and_revision_preserving():
    assert 'sk.includes("reason")' in JS and 'sk.includes("prediction")' in JS
    assert 'old.first?old' in JS
    assert 'revisionFor(t,model)' in JS
    assert 'navigator.locks.request(ref.key' in JS
    assert 'localStorage.getItem(ref.key)!==raw' in JS
    assert 'events:[...old.events,' in JS
    assert 'transferReceipts:receipts' in JS
    assert 'stageSave("diagnosis",skip?{reason:null,skipped:true}:v' in JS


def test_accessible_skip_notice_does_not_claim_mastery_or_release():
    assert 'id="skip-policy"' in HTML
    assert 'Undo skip' in HTML
    assert 'earn no credit' in HTML
    assert '.skip-field[aria-pressed=true]' in HTML
    assert '.skip-recorded' in HTML
    assert 'academic HOLD' in HTML.lower() or 'academic HOLD' in HTML
    for path in (
        ROOT / "nsejs/physics/ph03/source-led-r1/reader.js",
        ROOT / "nsejs/physics/learn/catalog.json",
        ROOT / "nsejs/physics/textbook/PH03/P03/index.html",
        ROOT / "nsejs/physics/core1/PH03/P03/index.html",
    ):
        assert path.is_file()


def test_actual_browser_regression_covers_source_to_return_and_fail_closed():
    qa = (ROOT / "tools/ph03_skip_browser_qa.py").read_text(encoding="utf-8")
    for phrase in ("source", "challenge", "diagnose", "repair", "boundary",
                   "retryreason", "core2", "storage_denied", "Undo skip", "first"):
        assert phrase.lower() in qa.lower()
    assert 'has_touch=True' in qa

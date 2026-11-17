"""Sitewide Skip control: fail closed without falsifying assessment progress."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "tools/audit_skip_coverage.py"
SKIP = ROOT / "nsejs/js/skip-mandatory-response.js"


def load_audit():
    spec = importlib.util.spec_from_file_location("g9_skip_coverage", AUDIT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_all_subject_learner_response_pages_offer_skip_navigation():
    report = load_audit().audit()
    assert report["response_pages"] > 40, (
        "Audit unexpectedly stopped seeing real learner response pages"
    )
    assert report["uncovered_response_pages"] == [], report
    assert report["missing_dynamic_entrypoints"] == [], report
    assert report["audit_is_academic_acceptance"] is False


def test_skip_does_not_fake_answer_submit_reveal_or_grade():
    code = SKIP.read_text(encoding="utf-8")
    assert "SKIPPED_UNASSESSED" in code
    assert "skip.type='button'" in code
    assert "advance.type='button'" in code
    assert "button.type='button'" in code
    assert "field.value =" not in code
    assert "document.body.append(dock)" in code
    assert "field.insertAdjacentElement('afterend',wrap)" in code
    assert ".click()" not in code
    assert "localStorage.setItem" not in code
    assert "sessionStorage.setItem" not in code
    assert "dispatchEvent(new CustomEvent('g9:skip-response'" in code
    assert "Protected model feedback remains locked" in code
    assert "min-height:48px" in code
    assert "version:'r3'" in code


def test_skip_is_visible_at_each_eligible_question_without_focus_and_never_commits():
    code = SKIP.read_text(encoding="utf-8")
    assert "function createInline(field)" in code
    assert "field.dataset.g9SkipInline='r3'" in code
    assert "document.querySelectorAll(questionSelectors).forEach(enhance)" in code
    assert "function nextResponse(field)" in code
    assert "function nextTaskSelector()" in code
    assert "function advanceWithoutAnswer(field)" in code
    assert "option.disabled" in code
    assert "following.scrollIntoView({block:'center'})" in code
    assert "following.tagName==='FIELDSET'" in code
    assert "field.dataset.g9SkipStatus='SKIPPED_UNASSESSED'" in code
    assert "field.removeAttribute('data-g9-skip-status')" in code
    assert "radioGroup=tag==='fieldset'" in code
    assert "questionSelect=tag==='select'" in code
    assert "field.closest('header,nav,footer,[data-g9-skip-ignore]" in code
    assert "Never fabricate answers, trigger form validation, commit an attempt" in code


def test_three_subject_hubs_load_skip_control():
    for subject in ("physics", "chemistry", "biology"):
        html = (ROOT / "nsejs" / subject / "index.html").read_text(encoding="utf-8")
        assert 'data-g9-skip-script="r1"' in html
    assert SKIP.is_file()

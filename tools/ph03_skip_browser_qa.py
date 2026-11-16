"""PH03 R2 opt-out text input QA. No academic or mastery qualification."""
import functools
import http.server
import json
import threading
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REL = "nsejs/physics/ph03/source-led-r2"
OUT = ROOT / "artifacts/ph03-r2-skip"
OUT.mkdir(parents=True, exist_ok=True)


def open_stage(page, base, stage):
    page.goto(base + stage, wait_until="domcontentloaded")
    expect(page.locator("#commit")).to_be_enabled(timeout=20000)
    assert page.locator("#skip-policy").count() == 1


def skip(page, *ids):
    for name in ids:
        button = page.locator(f'button[data-skip-target="{name}"]')
        expect(button).to_be_visible()
        button.click()
        expect(button).to_have_attribute("aria-pressed", "true")
        if name.startswith("fieldset-"):
            # Fieldset's disabled state disables descendant radios; Playwright
            # does not always classify the fieldset itself as a disabled input.
            assert page.locator("#" + name).evaluate(
                "(el) => el.disabled && [...el.querySelectorAll('input')].every(x => x.matches(':disabled'))")
        else:
            expect(page.locator("#" + name)).to_be_disabled()


def storage_records(page):
    return page.evaluate("""() => Object.entries(localStorage).filter(([k,v]) =>
      k.startsWith('G9V41:PH03:R2:') && v.includes('"revision"'))
      .map(([key,raw])=>({key,record:JSON.parse(raw)}))""")


def challenge(page, base, name):
    open_stage(page, base, "?stage=challenge&task=" + name)
    # Empty fields alone must never masquerade as a committed response.
    page.locator("#commit").click()
    expect(page.locator("#status")).to_contain_text("necessary", timeout=10000)
    skip(page, "prediction", "reason")
    ids = page.locator('#firstform .field-slot input, #firstform .field-slot select').evaluate_all(
        "(nodes) => nodes.map(n => n.id)")
    skip(page, *ids)
    page.locator("#commit").click()
    expect(page.locator("#status")).to_contain_text("Skipped fields:", timeout=10000)
    expect(page.locator("#reveal")).to_be_visible()
    page.reload(wait_until="domcontentloaded")
    expect(page.locator("#status")).to_contain_text("Skipped fields:")
    expect(page.locator("#prediction")).to_be_disabled()
    assert "Skipped · no credit" in page.locator("#firstform").inner_text()
    page.locator("#reveal").click()
    expect(page.locator("#post")).to_contain_text("Insufficient structured evidence")
    skip(page, "diagtext")
    page.locator("#diagnose").click()
    expect(page.locator("#post")).to_contain_text("Diagnosis skipped · no credit")
    expect(page.locator("#repairreason")).to_be_visible()
    repair_fields = page.locator('input[id^="repair-"], select[id^="repair-"]').evaluate_all(
        "(nodes) => nodes.map(n => n.id)")
    skip(page, *repair_fields, "repairreason")
    page.locator("#repairSave").click()
    expect(page.locator("#post")).to_contain_text("Repair explanation skipped · no credit")
    expect(page.locator("#boundaryreason")).to_be_visible()
    boundary_fields = page.locator('input[id^="bound-"], select[id^="bound-"]').evaluate_all(
        "(nodes) => nodes.map(n => n.id)")
    skip(page, *boundary_fields, "boundaryreason")
    page.locator("#boundarySave").click()
    expect(page.locator("#boundaryReveal")).to_be_visible()
    page.locator("#boundaryReveal").click()
    expect(page.locator("#post")).to_contain_text("ungraded and earns no mastery credit")
    page.reload(wait_until="domcontentloaded")
    expect(page.locator("#post")).to_contain_text("ungraded and earns no mastery credit")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
    records = storage_records(page)
    matching = [x["record"] for x in records if x["record"].get("first", {}).get("skipped")
                and x["record"]["first"]["skipped"][:2] == ["prediction", "reason"]]
    assert matching
    item = next(x for x in matching if x.get("diagnosis") is not None and x.get("repair") is not None)
    assert item["first"]["prediction"] is None and item["first"]["reason"] is None
    assert all(v is None for v in item["first"]["fields"].values())
    assert item["diagnosis"] == {"reason": None, "skipped": True}
    assert item["repair"]["reason"] is None and all(v is None for v in item["repair"]["fields"].values())
    assert item["boundary"]["reason"] is None and all(v is None for v in item["boundary"]["fields"].values())
    event_kinds = [event["kind"] for event in item["events"]]
    # Persisted chronology can include later legitimate exposures; require
    # every named stage to exist rather than assuming the final event's label.
    for required in ("first", "revealed", "diagnosis", "repair", "boundary", "boundaryReveal"):
        assert required in event_kinds, event_kinds


def run():
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(
            http.server.SimpleHTTPRequestHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/{REL}/index.html"
    results = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                for size in [(1000, 1600), (1600, 1000)]:
                    ctx = browser.new_context(viewport={"width": size[0], "height": size[1]},
                                              has_touch=True)
                    page = ctx.new_page()
                    open_stage(page, base, "?stage=source")
                    # All mandatory text/choice fields may be skipped, with no guess.
                    skip(page, "prediction", "reason", "fieldset-opt")
                    page.locator("#commit").click()
                    expect(page.locator("#status")).to_contain_text("Skipped fields:", timeout=10000)
                    page.reload(wait_until="domcontentloaded")
                    expect(page.locator("#post")).to_contain_text("Original selection and reasoning saved")
                    original = next(x["record"] for x in storage_records(page)
                                    if x["record"].get("first"))
                    assert original["first"]["option"] is None
                    assert original["first"]["reason"] is None
                    assert set(original["first"]["skipped"]) == {"prediction", "reason", "opt"}
                    # Return is still locked before both challenge boundaries.
                    assert page.locator("#retrySave").count() == 0
                    challenge(page, base, "A")
                    challenge(page, base, "B")
                    page.goto(base + "?stage=source")
                    expect(page.locator("#retrySave")).to_be_visible(timeout=20000)
                    skip(page, "fieldset-retryopt", "retryreason")
                    page.locator("#retrySave").click()
                    expect(page.locator("#post")).to_contain_text("return selected (skipped)")
                    page.reload(wait_until="domcontentloaded")
                    expect(page.locator("#post")).to_contain_text("return selected (skipped)")
                    page.goto(base + "?stage=core2")
                    expect(page.locator("#commit")).to_be_enabled(timeout=20000)
                    skip(page, "prediction", "reason", "fieldset-opt")
                    page.locator("#commit").click()
                    expect(page.locator("#status")).to_contain_text("Skipped fields:", timeout=10000)
                    page.locator("#reveal").click()
                    expect(page.locator("#post")).to_contain_text("no correct-answer credit")
                    page.screenshot(path=str(OUT / f"skip-journey-{size[0]}x{size[1]}.png"),
                                    full_page=True)
                    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
                    results.append({"viewport": size, "source_first": "SKIPPED_NO_CREDIT",
                                    "challenge_a": "SKIPPED_NO_CREDIT",
                                    "challenge_b": "SKIPPED_NO_CREDIT",
                                    "source_return": "SKIPPED_NO_CREDIT",
                                    "core2": "SKIPPED_NO_CREDIT",
                                    "status": "PASS"})
                    ctx.close()
                # Undo skip is reversible until first durable submission.
                ctx = browser.new_context()
                page = ctx.new_page()
                open_stage(page, base, "?stage=core2")
                skip(page, "reason")
                undo = page.locator('button[data-skip-target="reason"]')
                undo.click()
                expect(undo).to_have_attribute("aria-pressed", "false")
                expect(page.locator("#reason")).to_be_enabled()
                page.locator("#reason").fill("Independent reasoning restored before commitment.")
                assert page.locator("#reason").input_value()
                results.append({"undo_skip": "PASS"})
                ctx.close()
                # Storage denial: Skip must not defeat fail-closed persistence.
                ctx = browser.new_context()
                page = ctx.new_page()
                page.add_init_script("Storage.prototype.setItem = function(){ throw Error('DENIED') }")
                page.goto(base + "?stage=challenge&task=A")
                expect(page.locator("#status")).to_contain_text("HOLD", timeout=20000)
                expect(page.locator("#commit")).to_be_disabled()
                results.append({"storage_denied": "PASS_FAIL_CLOSED"})
                ctx.close()
            finally:
                browser.close()
        (OUT / "receipt.json").write_text(
            json.dumps({"head_check": "AUTHOR_EXPOSED_TECHNICAL_ONLY",
                        "academic": "HOLD", "results": results}, indent=2) + "\n")
    finally:
        server.shutdown()


if __name__ == "__main__":
    run()

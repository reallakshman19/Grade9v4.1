"""PH02 semantic reconstruction regression: an authored QRT W is not its full worked answer."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "nsejs/physics/curriculum/agent1/PH02/physics-topic-package.v1_1.json"
Q = ROOT / "nsejs/physics/ph02/qrt-candidates.v1.json"


def test_ph02_all_sixteen_qrts_show_real_solutions_after_attempt():
    q = json.loads(Q.read_text(encoding="utf-8"))
    pkg = json.loads(PKG.read_text(encoding="utf-8"))
    assert len(q["tasks"]) == 16
    for task in q["tasks"]:
        # Full worked derivation, not a brief restatement of the decisive cognitive operation.
        assert len(task["reconstruction"]) > len(task["w"]), task["id"]
        assert "=" in task["reconstruction"], task["id"]
        assert task["reconstruction"] != task["w"], task["id"]
        sub = next(s for s in pkg["subtopics"] if s["id"] == task["unit"])
        target = next(x for x in sub["qrt_targets"] if x["id"] == task["id"])
        cycle = next(c for c in pkg["core1b"] if c["id"] == task["uid"])
        assert target["protected_work"] == task["w"]
        assert target["decisive_route"] == task["reconstruction"]
        assert cycle["protected_work"] == task["w"]
        assert cycle["stages"]["reconstruct"] == task["reconstruction"]


def test_ph02_attempts_digest_exact_content_and_restore_only_same_fingerprint():
    js = (ROOT / "nsejs/physics/ph02/practice.js").read_text(encoding="utf-8")
    assert 'crypto.subtle.digest("SHA-256",bytes)' in js
    assert 'x.content_fingerprint!==contentFingerprint' in js
    assert 'content_fingerprint:contentFingerprint' in js
    assert 'ptask.reconstruction,ptask.alternative,ptask.hints' in js
    assert 'ptask.boundaryPrompt,ptask.boundaryModel' in js


def test_ph02_entry_link_present():
    page = (ROOT / "nsejs/physics/index.html").read_text(encoding="utf-8")
    assert 'id="ph02-forces-native"' in page
    assert 'href="textbook/PH02/index.html"' in page
    assert 'href="core1/PH02/main/index.html"' in page

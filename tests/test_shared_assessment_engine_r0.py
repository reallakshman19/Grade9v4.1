"""Shared assessment R0 candidate: execute the actual Node state-machine regressions.

This is a technical preflight, never a B1–B7 / academic approval.
The separate genuine Chromium two-tab test is still required.
"""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "shared-assessment" / "engine.mjs"
TEST = ROOT / "tools" / "shared-assessment" / "engine.test.mjs"


def test_shared_engine_exact_node_suite():
    node = shutil.which("node")
    assert node is not None, "Node is required for the shared-engine validation"
    command = [node, "--test", str(TEST)]
    result = subprocess.run(
        command, cwd=ROOT, check=False, capture_output=True, text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        "shared-engine Node tests failed:\n" + result.stdout + "\n" + result.stderr
    )
    assert "# fail 0" in result.stdout
    assert "# pass 13" in result.stdout


def test_shared_engine_isolated_from_unapproved_learner_pages():
    assert MODULE.is_file() and TEST.is_file()
    code = MODULE.read_text(encoding="utf-8")
    assert "IndexedDbAttemptStore" in code
    assert "REVEAL_BOUNDARY_FEEDBACK" in code
    assert "NOT_EVALUATED" in code
    assert "localStorage." not in code
    assert "ACADEMIC_PASS" not in code

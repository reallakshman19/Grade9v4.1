"""Real Chromium two-tab IndexedDB regression for shared engine R0.

Runs only when Chrome is actually installed. A skipped browser check is
unqualified evidence, not a successful browser acceptance result.
"""
from pathlib import Path
import os
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "shared-assessment" / "browser-race.mjs"


def test_shared_assessment_real_browser_two_tab_race():
    node = shutil.which("node")
    chrome = next(
        (shutil.which(name) for name in
         ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
         if shutil.which(name)),
        None,
    )
    assert node is not None, "Node is required for shared assessment QA"
    assert SCRIPT.is_file(), "Real-browser race QA script missing"
    if not chrome:
        pytest.skip("Chrome not installed; browser acceptance remains NOT_RUN")
    env = dict(os.environ, CHROME_BINARY=chrome)
    check = subprocess.run(
        [node, str(SCRIPT)], cwd=ROOT, env=env,
        text=True, capture_output=True, timeout=90, check=False,
    )
    assert check.returncode == 0, (
        "Real Chrome race failed (not a browser pass):\n"
        + check.stdout + "\n" + check.stderr
    )
    assert "CHROME_IDB_TWO_TAB_PASS:" in check.stdout
    assert '"academic":"NOT_EVALUATED"' in check.stdout

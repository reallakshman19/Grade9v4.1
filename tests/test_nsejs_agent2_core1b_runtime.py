"""Mechanical Core1B state transitions, not browser or B1–B7 approval."""
from __future__ import annotations
import shutil
import subprocess
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "nsejs/physics/curriculum/agent2/core1b-runtime.js"
SMOKE = ROOT / "nsejs/physics/curriculum/agent2/tests/runtime-smoke.cjs"

def test_agent2_runtime_node_smoke():
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node executable unavailable; actual browser evidence remains NOT_RUN")
    for command in ([node, "--check", str(RUNTIME)], [node, str(SMOKE)]):
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=ROOT)
        assert result.returncode == 0, result.stdout + "\n" + result.stderr
    assert "AGENT2_NODE_RUNTIME_PASS" in result.stdout

@pytest.mark.parametrize("topic", ["PH07","PH08","PH09","PH10","PH11","PH12"])
def test_six_core1b_preview_pages_have_declared_data_and_draft_boundaries(topic):
    page = (ROOT / f"nsejs/physics/curriculum/topics/{topic}/core1b-preview.html").read_text()
    assert f'data-topic="{topic}"' in page
    assert 'data-package="./physics-topic-package.v1.json"' in page
    assert 'AUTHOR-EXPOSED' in page
    assert 'ACADEMIC HOLD' in page
    assert 'first-predict' in page and 'first-attempt' in page
    assert 'core1b-runtime.js' in page

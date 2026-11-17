"""Fail-closed Pages preflight: precise diagnostics without new release authority."""
from pathlib import Path
import os
import subprocess
import textwrap

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/deploy-r3-signed.yaml"


def preflight_script():
    data = WORKFLOW.read_text(encoding="utf-8")
    label = "      - name: Check externally authorized release prerequisites (fail closed)"
    begin = data.index(label)
    assert "        id: pin" in data[begin:]
    run = data.index("        run: |\n", begin) + len("        run: |\n")
    end = data.index("      - name: Checkout externally pinned control code", run)
    return textwrap.dedent(data[run:end])


def test_release_preflight_reports_all_missing_inputs_and_never_emits_a_pin(tmp_path):
    script = preflight_script()
    (tmp_path / "candidate").mkdir()
    output = tmp_path / "output"
    env = dict(os.environ,
               CONTROL_SHA="", TRUST_JSON="", REF="refs/heads/main",
               GITHUB_SHA="a" * 40, GITHUB_OUTPUT=str(output))
    result = subprocess.run(["bash", "-e", "-c", script], cwd=tmp_path,
                            env=env, capture_output=True, text=True, check=False)
    assert result.returncode != 0
    for name in ("G9_R3_CONTROL_SHA", "G9_R3_TRUST_JSON",
                 "publication-manifest.json", "release-receipt.json"):
        assert name in result.stdout, (name, result.stdout, result.stderr)
    assert "R3 Pages deployment blocked" in result.stdout
    assert not output.exists(), "Failed release must not emit a verified control pin"


def test_deploy_still_requires_signed_exact_bytes_and_manual_review():
    data = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in data
    assert "branches: [main]" not in data
    assert "ref: $" + "{{ steps.pin.outputs.sha }}" in data
    assert "python trusted/docs/agent-entry/production-control-r3/release.py" in data
    assert "G9_R3_TRUST_JSON: $" + "{{ vars.G9_R3_TRUST_JSON }}" in data
    assert "environment:" in data and "name: github-pages" in data
    script = preflight_script()
    assert "merge-base --is-ancestor" in script
    assert "if (( errors != 0 )); then" in script
    assert 'echo "sha=$CONTROL_SHA" >> "$GITHUB_OUTPUT"' in script
    assert script.index("if (( errors != 0 )); then") < script.index('echo "sha=$CONTROL_SHA"')

"""Fail-closed Pages preflight: precise diagnostics without new release authority."""
from pathlib import Path
import json
import os
import subprocess
import textwrap

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/deploy.yaml"


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



def _git(repo, *arguments):
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip()


def _candidate_with_frozen_policy(tmp_path, content_change):
    repo = tmp_path / "candidate"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "r3-test@example.invalid")
    _git(repo, "config", "user.name", "R3 test")
    (repo / "index.html").write_text("<h1>Frozen preview</h1>\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "frozen preview baseline")
    baseline = _git(repo, "rev-parse", "HEAD")

    policy_file = repo / "docs/agent-entry/production-control-r3/policy.v1.json"
    policy_file.parent.mkdir(parents=True)
    policy_file.write_text(json.dumps({
        "phase": "FREEZE_PENDING_GOLDEN",
        "legacy_preview_baseline": baseline,
        "governance_paths": [],
        "governance_prefixes": ["docs/agent-entry/production-control-r3/"],
        "evidence_prefixes": ["review/production-control-r3/"],
    }))
    for name in ("publication-manifest.json", "release-receipt.json"):
        evidence = repo / "review/production-control-r3" / name
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text("{}\n")  # existence only; NOT valid authorization
    if content_change:
        content = repo / "nsejs/physics/reader.js"
        content.parent.mkdir(parents=True)
        content.write_text("console.log('new content');\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "release candidate")
    return repo, baseline, _git(repo, "rev-parse", "HEAD")


def _run_candidate_preflight(tmp_path, baseline, head):
    output = tmp_path / "output"
    env = dict(
        os.environ,
        CONTROL_SHA=baseline,
        TRUST_JSON='{"schema":"g9-r3-trust/v1","keys":[]}',
        REF="refs/heads/main",
        GITHUB_SHA=head,
        GITHUB_OUTPUT=str(output),
    )
    run = subprocess.run(
        ["bash", "-e", "-c", preflight_script()],
        cwd=tmp_path, env=env, capture_output=True, text=True, check=False,
    )
    return run, output


def test_preflight_rejects_frozen_content_despite_present_variables_and_receipt_files(tmp_path):
    _, baseline, head = _candidate_with_frozen_policy(tmp_path, content_change=True)
    result, output = _run_candidate_preflight(tmp_path, baseline, head)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "FROZEN_CONTENT_IN_RELEASE_TREE" in result.stdout
    assert "1 CONTENT path(s)" in result.stdout
    assert "nsejs/physics/reader.js" in result.stdout
    assert not output.exists(), "An ineligible candidate must never emit a verified pin"


def test_governance_only_candidate_can_reach_but_not_skip_signed_release_verifier(tmp_path):
    _, baseline, head = _candidate_with_frozen_policy(tmp_path, content_change=False)
    result, output = _run_candidate_preflight(tmp_path, baseline, head)
    assert result.returncode == 0, result.stdout + result.stderr
    assert output.read_text().strip() == "sha=" + baseline
    # Passing a diagnostic is not release approval; receipt contents here
    # are deliberately invalid and the separately pinned release.py must run.
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "python trusted/docs/agent-entry/production-control-r3/release.py" in workflow
    assert "steps.pin.outputs.sha" in workflow


def test_frozen_content_preflight_uses_exact_git_diff_without_rename_suppression():
    script = preflight_script()
    assert 'git", "-C", repo, "show"' in script
    assert '"--no-renames", "-z", base, head' in script
    assert 'if policy["phase"] == "FREEZE_PENDING_GOLDEN":' in script
    assert "FROZEN_CONTENT_IN_RELEASE_TREE" in script

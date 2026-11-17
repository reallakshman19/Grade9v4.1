"""Read-only R3 audit tests. Never authorize, sign, or deploy from the audit."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "tools/r3_release_readiness.py"
spec = importlib.util.spec_from_file_location("r3_release_readiness", SRC)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)


def git(path, *args):
    return subprocess.check_output(["git", "-C", str(path), *args], stderr=subprocess.PIPE).decode().strip()


def write(repo, name, value):
    target = repo / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def build(repo):
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Readiness fixture")
    git(repo, "config", "user.email", "fixture@example.invalid")
    write(repo, "index.html", "<title>frozen</title>")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "Frozen baseline")
    base = git(repo, "rev-parse", "HEAD")
    policy = {
        "schema": "g9-production-control/v1",
        "phase": "FREEZE_PENDING_GOLDEN",
        "legacy_preview_baseline": base,
        "governance_paths": ["AGENTS.md"],
        "governance_prefixes": ["docs/agent-entry/production-control-r3/"],
        "evidence_prefixes": list(R.EVIDENCE_PREFIXES),
        "accepted_golden": None,
        "production_enabled": False,
    }
    write(repo, R.POLICY_PATH, json.dumps(policy))
    write(repo, "nsejs/physics/learn/changed.html", "new unaccepted learner lesson")
    write(repo, "AGENTS.md", "governance text")
    write(repo, "review/production-control-r3/example-receipt.json", "{}")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "Candidate contains frozen content")
    return base, git(repo, "rev-parse", "HEAD")


def test_frozen_content_report_is_complete_and_stays_blocked(tmp_path):
    repo = tmp_path / "repo"
    base, head = build(repo)
    out = R.report(repo, head)
    assert out["head"] == head and out["frozen_baseline"] == base
    assert out["status"] == "BLOCKED_OR_REQUIRES_INDEPENDENT_AUTHORITY"
    assert out["release_authorized"] is out["staged"] is out["deployed"] is False
    assert out["counts"] == {"CONTENT": 1, "GOVERNANCE": 2, "EVIDENCE": 1}
    assert out["changed_paths"]["CONTENT"] == ["nsejs/physics/learn/changed.html"]
    assert R.MANIFEST in out["input_statuses"]
    assert R.RECEIPT in out["input_statuses"]
    assert "FROZEN_CONTENT_IN_RELEASE_TREE" in out["blockers"]
    assert "OWNER_GOLDEN_NOT_ACCEPTED" in out["blockers"]
    assert out["policy_source"] == "CANDIDATE_TREE_DIAGNOSTIC_ONLY_NOT_PINNED_CONTROL"
    assert not (repo / "public").exists()


def test_even_external_variable_presence_cannot_authorize_frozen_content(tmp_path):
    repo = tmp_path / "repo"
    base, head = build(repo)
    write(repo, R.MANIFEST, '{"fake":"not signed"}')
    write(repo, R.RECEIPT, '{"fake":"not signed"}')
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "Unverified artifacts exist")
    head = git(repo, "rev-parse", "HEAD")
    out = R.report(repo, head, control_sha=base, trust_configured=True)
    assert out["input_statuses"]["G9_R3_CONTROL_SHA"] == "configured_ancestor_only_not_independent_approval"
    assert out["input_statuses"]["G9_R3_TRUST_JSON"] == "configured_but_not_signature_verified"
    assert out["input_statuses"][R.MANIFEST] == "present_unverified"
    assert out["input_statuses"][R.RECEIPT] == "present_unverified"
    assert "FROZEN_CONTENT_IN_RELEASE_TREE" in out["blockers"]
    assert out["release_authorized"] is False
    assert "signed" not in str(out["input_statuses"][R.RECEIPT])


def test_strict_exact_sha_and_candidate_policy_fail_closed(tmp_path):
    repo = tmp_path / "repo"
    _, head = build(repo)
    try:
        R.report(repo, "main")
    except R.AuditError as exc:
        assert "HEAD_NOT_AN_EXACT_SHA40" in str(exc)
    else:
        assert False, "nonexact ref must be rejected"
    try:
        R.report(repo, head, control_sha="not-a-sha")
    except R.AuditError:
        assert False, "bad control is a blocked status, not a crash"
    out = R.report(repo, head, control_sha="not-a-sha")
    assert out["input_statuses"]["G9_R3_CONTROL_SHA"] == "invalid_or_unverified"


def test_cli_writes_only_readonly_diagnostic_and_redacts_roster(tmp_path):
    repo = tmp_path / "repo"
    _, head = build(repo)
    output, md = tmp_path / "report.json", tmp_path / "summary.md"
    env = dict(os.environ, G9_R3_CONTROL_SHA="", G9_R3_TRUST_CONFIGURED="false",
               G9_R3_TRUST_JSON='{"private_key":"LEAK_ME_NEVER"}')
    p = subprocess.run(
        [sys.executable, str(SRC), "--repo", str(repo), "--head", head,
         "--json-output", str(output), "--summary-output", str(md)],
        env=env, capture_output=True, text=True, check=False,
    )
    assert p.returncode == 0, (p.stdout, p.stderr)
    txt = output.read_text() + md.read_text()
    assert "LEAK_ME_NEVER" not in txt
    assert "BLOCKED" in txt and "NOT AUTHORIZED" in txt
    assert "FROZEN_CONTENT_IN_RELEASE_TREE" in txt
    assert not (repo / "public").exists()
    assert not (repo / R.MANIFEST).exists()
    assert not (repo / R.RECEIPT).exists()

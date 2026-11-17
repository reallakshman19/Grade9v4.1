#!/usr/bin/env python3
"""Read-only R3 release-readiness inventory. NOT a release, review, or signature validator.

This deliberately never emits a usable release pin, signed receipt, deployment,
publication manifest, or academic decision. The pinned trusted release.py is
the authority and this output cannot substitute for it.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SHA40 = re.compile(r"^[0-9a-f]{40}$")
POLICY_PATH = "docs/agent-entry/production-control-r3/policy.v1.json"
MANIFEST = "review/production-control-r3/publication-manifest.json"
RECEIPT = "review/production-control-r3/release-receipt.json"
EVIDENCE_PREFIXES = ("review/production-control-r3/", "review/quality-packets/")


class AuditError(Exception):
    pass


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def exact_commit(repo: Path, value: str, label: str) -> str:
    if not SHA40.fullmatch(value):
        raise AuditError(label + "_NOT_AN_EXACT_SHA40")
    try:
        resolved = git(repo, "rev-parse", "--verify", value + "^{commit}").decode().strip()
    except subprocess.CalledProcessError as exc:
        raise AuditError(label + "_NOT_FOUND") from exc
    if resolved != value:
        raise AuditError(label + "_NOT_AN_EXACT_COMMIT")
    return value


def tree_has(repo: Path, commit: str, path: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", commit + ":" + path],
        capture_output=True, check=False,
    ).returncode == 0


def is_ancestor(repo: Path, older: str, newer: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", older, newer],
        capture_output=True, check=False,
    ).returncode == 0


def classify(path: str, policy: dict) -> str:
    if path.startswith(EVIDENCE_PREFIXES):
        return "EVIDENCE"
    if path in policy["governance_paths"] or any(
        path.startswith(prefix) for prefix in policy["governance_prefixes"]
    ):
        return "GOVERNANCE"
    return "CONTENT"


def report(repo: Path, head: str, control_sha: str = "", trust_configured: bool = False) -> dict:
    head = exact_commit(repo, head, "HEAD")
    try:
        policy = json.loads(git(repo, "show", head + ":" + POLICY_PATH))
    except (subprocess.CalledProcessError, ValueError) as exc:
        raise AuditError("POLICY_UNREADABLE") from exc
    if (policy.get("schema") != "g9-production-control/v1" or
            policy.get("evidence_prefixes") != list(EVIDENCE_PREFIXES)):
        raise AuditError("POLICY_INVALID_OR_EVIDENCE_CLASSIFICATION_CHANGED")
    if policy.get("phase") not in {"FREEZE_PENDING_GOLDEN", "ACTIVE_AFTER_OWNER_GOLDEN"}:
        raise AuditError("UNKNOWN_POLICY_PHASE")
    base = exact_commit(repo, policy["legacy_preview_baseline"], "FROZEN_BASELINE")
    if not is_ancestor(repo, base, head):
        raise AuditError("FROZEN_BASELINE_NOT_ANCESTOR")
    raw = git(repo, "diff", "--name-only", "--no-renames", "-z", base, head)
    paths = sorted(x.decode("utf-8") for x in raw.split(bytes([0])) if x)
    if any("\n" in p or "\r" in p for p in paths):
        raise AuditError("UNSAFE_PATH_IN_DIAGNOSTIC")
    categories = {k: [] for k in ("CONTENT", "GOVERNANCE", "EVIDENCE")}
    for path in paths:
        categories[classify(path, policy)].append(path)

    control = "missing"
    if control_sha:
        control = "invalid_or_unverified"
        if SHA40.fullmatch(control_sha):
            try:
                exact_commit(repo, control_sha, "CONTROL")
                if is_ancestor(repo, control_sha, head):
                    control = "configured_ancestor_only_not_independent_approval"
            except AuditError:
                pass

    inputs = {
        "G9_R3_CONTROL_SHA": control,
        "G9_R3_TRUST_JSON": ("configured_but_not_signature_verified"
                              if trust_configured else "missing"),
        MANIFEST: "present_unverified" if tree_has(repo, head, MANIFEST) else "missing",
        RECEIPT: "present_unverified" if tree_has(repo, head, RECEIPT) else "missing",
    }
    blockers = []
    if control != "configured_ancestor_only_not_independent_approval":
        blockers.append("EXTERNAL_REVIEWED_CONTROL_PIN_REQUIRED")
    if not trust_configured:
        blockers.append("ADMIN_PUBLIC_KEY_TRUST_ROSTER_REQUIRED")
    if inputs[MANIFEST] == "missing":
        blockers.append("INDEPENDENTLY_REVIEWED_EXACT_BYTE_MANIFEST_REQUIRED")
    if inputs[RECEIPT] == "missing":
        blockers.append("GENUINELY_SIGNED_OWNER_PREVIEW_RELEASE_RECEIPT_REQUIRED")
    if policy["phase"] == "FREEZE_PENDING_GOLDEN" and categories["CONTENT"]:
        blockers.append("FROZEN_CONTENT_IN_RELEASE_TREE")
    if policy.get("accepted_golden") is None:
        blockers.append("OWNER_GOLDEN_NOT_ACCEPTED")
    if not policy.get("production_enabled"):
        blockers.append("PRODUCTION_DISABLED_BY_POLICY")

    return {
        "schema": "g9-r3-readonly-readiness/v1",
        "kind": "INFORMATIONAL_DIAGNOSTIC_ONLY",
        "status": "BLOCKED_OR_REQUIRES_INDEPENDENT_AUTHORITY",
        "release_authorized": False,
        "staged": False,
        "deployed": False,
        "not_a_valid_trust_or_signature_verification": True,
        "head": head,
        "policy_source": "CANDIDATE_TREE_DIAGNOSTIC_ONLY_NOT_PINNED_CONTROL",
        "frozen_baseline": base,
        "phase": policy["phase"],
        "accepted_golden_present": policy.get("accepted_golden") is not None,
        "production_enabled": bool(policy.get("production_enabled")),
        "input_statuses": inputs,
        "blockers": blockers,
        "counts": {k: len(v) for k, v in categories.items()},
        "changed_paths": categories,
        "next_action": "Independent R3/Owner adoption and externally authorized release workflow; do not edit policy or invent signatures to make this pass.",
    }


def summary_markdown(data: dict) -> str:
    rows = [
        "## R3 release-readiness — read-only diagnostic",
        "",
        "**BLOCKED / NOT AUTHORIZED.** No file staging, signing, deployment or release approval occurred.",
        "",
        "This run is informational only, not a substitute for the externally pinned trusted release verifier.",
        "",
        "- Exact commit: `" + data["head"] + "`",
        "- Frozen baseline: `" + data["frozen_baseline"] + "`",
        "- Phase: `" + data["phase"] + "`",
        "- Changed paths: " + ", ".join(
            k + "=" + str(data["counts"][k]) for k in ("CONTENT", "GOVERNANCE", "EVIDENCE")),
        "",
        "### Blockers",
        "",
    ]
    rows.extend("- " + name for name in data["blockers"])
    rows.extend(["", "### Configuration presence (not approval)", ""])
    rows.extend("- " + k + ": " + v for k, v in data["input_statuses"].items())
    rows.extend(["", "Full changed-path inventory is in the accompanying JSON artifact.",
                 "Private signing keys must remain outside GitHub. No bypass is permitted.", ""])
    return "\n".join(rows)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    args = parser.parse_args(argv)
    try:
        data = report(
            args.repo, args.head,
            control_sha=os.environ.get("G9_R3_CONTROL_SHA", ""),
            trust_configured=os.environ.get("G9_R3_TRUST_CONFIGURED") == "true",
        )
    except (AuditError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "AUDIT_UNABLE_TO_VERIFY", "release_authorized": False,
                          "reason": str(exc)}), file=sys.stderr)
        return 2
    raw = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if args.json_output:
        args.json_output.write_text(raw, encoding="utf-8")
    else:
        print(raw, end="")
    if args.summary_output:
        args.summary_output.write_text(summary_markdown(data), encoding="utf-8")
    # Exit success means audit generated a report, NEVER that release can proceed.
    return 0


if __name__ == "__main__":
    sys.exit(main())

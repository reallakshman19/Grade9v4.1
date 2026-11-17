# Administrator activation checklist — required, NOT performed by author
1. Review this infrastructure-only PR and its exact-head candidate tests. Install it on main only with Owner authorization. Confirm it does not alter any chapter or academic admission. Existing Pages site remains at the last deployment until an explicit authorized release.
2. Create an external Ed25519 trust roster in repository/organization Actions variable G9_R3_TRUST_JSON (public keys only, schema g9-r3-trust/v1, keys list of id/principal/roles/public_key_pem). Private signing keys stay with authorized independent humans or governed external review service. No shared author/reviewer credentials; no credentials in PR.
3. Configure repository ruleset / required workflow for main: require pull requests and strict up-to-date branches; prohibit force pushes/direct pushes/deletion; dismiss stale approvals; require independent code-owner review; require exact-head g9/r3-production-decision plus existing exact-head tests. Restrict status-writing authority to trusted base workflow or independent GitHub App; required status name alone is not a secure origin boundary. Prefer organization-required workflow or independently operated status app if repository plan supports it. Do not allow author-owned workflows to impersonate the trusted status. Disable bypass for administrators except documented emergency policy. Do not use merge queue until its candidate validation is explicitly wired and tested.
4. Add actual CODEOWNERS with Owner/infrastructure security reviewer identities for .github/, AGENTS.md, architecture/, docs/agent-entry/production-control-r3/, quality-gate-r2/, reviewer receipts and native policy. No invented account or team in this draft.
5. Configure G9_R3_CONTROL_SHA outside Git to the exact reviewed control commit; configure github-pages environment to allow main only and require an independent release approver, prevent self-review/bypass when available. Restrict Actions permissions and deployment credentials. No raw push trigger; no unsigned manifest.
6. Prove externally: open a throwaway PR changing PH06 runtime, and one changing the gate itself; both must fail required status and be unmergeable. Attempt a stale-head approval, an unsigned preview release and an untrusted workflow status spoof; verify rejection. Verify allowed governance PR signed by Owner passes. Record actual GitHub ruleset IDs, protection screenshots/API receipts, status origin and run URLs. Until these checks are observed, claim only IMPLEMENTED / NOT ENFORCED AT REPOSITORY LEVEL.
7. Owner authorizes exactly one representative Golden after source/rights, native authority, R00, independent R01 and B1–B7. Use scoped signed Golden lane; no policy activation from author edit. Implement a separately reviewed adoption migration only after real receipts exist. The present academic release remains disabled even if the R2 workflow is green.
8. Before next Pages release, prepare full explicit manifest of approved technical preview assets and routes with prepare.py (FROZEN_SEARCH_R1 reproducible build or TRACKED_ONLY), review search completeness and client code exposure, sign exact file set, test on staging. No publication of restricted originals or review records. The previous preview can remain live; do not confuse availability with qualified educational content.

**Known connector limit:** GitHub repository administration/ruleset/environment settings cannot be inspected or mutated by the author tools in this workpack. This checklist is the real remaining external authority step, not evidence that protection has been enabled.

## Deployment #86 RCA and administrator setup (2026-11-16)

- Failed run: https://github.com/reallakshman19/Grade9v4.1/actions/runs/43789426180
- Exact release SHA: `308a8cef0d0b7d4ce5f1b79b21f01f76acc81acc`.
- The `stage` job stopped at **Resolve externally pinned control revision** before running `release.py`.
- The job log confirmed `CONTROL_SHA:` was **empty**, while `REF: refs/heads/main` was valid. The Node.js 20 notice was an unrelated warning.
- Owner action (requires repository settings access): open **Settings → Secrets and variables → Actions → Variables** and configure `G9_R3_CONTROL_SHA` as the **40-character SHA of the independently reviewed control commit**, not the candidate release SHA. This value must be pinned externally to Git.
- Configure `G9_R3_TRUST_JSON` in the same Actions Variables section with the administrator-approved **public-key-only** trust roster; keep private signing keys outside the repository and Actions.
- The exact release tree also lacks `review/production-control-r3/publication-manifest.json` and `review/production-control-r3/release-receipt.json`. A dedicated release workpack must create a byte-pinned manifest and obtain a genuinely signed `PREVIEW_RELEASE` Owner receipt from the trusted roster. Do not fabricate receipts, automatically sign them in Actions, or accept author self-review.
- **Separate blocker:** `policy.v1.json` still says `FREEZE_PENDING_GOLDEN`, `accepted_golden: null`, `production_enabled: false`; `release.py` rejects all CONTENT changes after its frozen baseline with `FROZEN_CONTENT_IN_RELEASE_TREE`. The Skip UI merged in PR #75 is therefore not currently an authorized release candidate. Fixing the variable or adding unsigned files is **not** permission to deploy it.
- Repository branch protections/rulesets are not demonstrated as enforced. Verify ruleset/admin receipts and independent release approval before any staging attempt. Do not disable or spoof the gate to make this run green.
- The improved `deploy.yaml` preflight reports *all* missing prerequisites as named GitHub errors, never prints trust keys or inserts a fallback control SHA. Its success would still mean only that configuration exists; `release.py` and the protected Pages environment remain mandatory.

## Pages run #87: second-stage blocker now reported up front (2026-11-16)

- Failed manually dispatched run: https://github.com/reallakshman19/Grade9v4.1/actions/runs/43849806250 at exact main SHA `564ad2a07fddc0fdd30d103674b3eca61235a54b`.
- The previous preflight correctly reported missing administrator control SHA, trust roster, publication manifest and Owner receipt, but concealed a second deterministic blocker: the pinned release verifier rejects changed learner CONTENT while `FREEZE_PENDING_GOLDEN` is active.
- At this incident head, the frozen baseline comparison has 240 changed paths: 202 CONTENT, 33 GOVERNANCE and 5 EVIDENCE under the committed R3 policy classifier. Releasing this exact main commit fails `FROZEN_CONTENT_IN_RELEASE_TREE` even after filling the other four fields.
- The revised workflow adds an **advisory exact-head Git-diff preflight** that reports the frozen-content count and examples before the signed release stage. It fails closed and never invents credentials or receipts. Its candidate-policy classification is *diagnostic only*; the pinned trusted `release.py` remains the independent authority and continues to reject noncompliant content.
- **This is not deployment authorization.** A substantive new-learner-content release needs independent R3 review and Owner-approved adoption/migration; the frozen baseline technical preview requires a genuinely signed manifest plus real Owner approval and valid release eligibility. Do not rewrite the policy, move the control pin, falsify signatures or merge a candidate to bypass the freeze.
- Because this is a governance-path change, independently signed `GOVERNANCE` approval and trusted `g9/r3-production-decision` are mandatory before merging the workpack, even if standalone regression tests pass. GitHub branch protection must be separately demonstrated.

## CI separation: frozen-search reconstruction vs R3 trusted decision (2026-11-16)

- The routine candidate-regression PR workflow no longer executes the frozen-search reconstruction step, because a previously modified `tools/search_learner_pages.py` already differs from the frozen baseline. A green unrelated coding PR must not be described as authorizing that changed builder or its content.
- The same reconstruction command is retained on manual `workflow_dispatch` and still reports `SEARCH_BUILDER_CHANGED` until its source integrity problem is independently reconciled. This changes only the **diagnostic frequency**, not the authorized publication set.
- **Do not remove** `g9/r3-production-decision` from `pull_request_target`: it is the only implemented fail-closed independent decision on changed PR heads. Existing `main` is not protected by a ruleset, so hiding this check would further weaken unapproved-merge detection. External trust and signed governance receipt are required; absent evidence must remain BLOCKED.
- Signed `release.py`, frozen baseline checks, manual Pages dispatch, pinned control, release manifest, and PREVIEW_RELEASE Owner receipt remain mandatory and unchanged. The Pages failures cannot be resolved by removing CI jobs.


## Read-only release-readiness audit R1 — 2026-11-17 (no deployment authority)

The failed `.github/workflows/deploy.yaml` manual dispatch that reports
`G9_R3_CONTROL_SHA`, `G9_R3_TRUST_JSON`, the publication manifest, an Owner
`PREVIEW_RELEASE` receipt and
`FROZEN_CONTENT_IN_RELEASE_TREE: 305 CONTENT path(s)` is **correctly blocked**.
The count is specific to the exact failed-run main commit, not a blanket
classification of every future revision. Recompute it when HEAD changes.

A separate read-only diagnosis now exists:

- **Actions → R3 release-readiness inventory (diagnostic only; NEVER deploys) → Run workflow.**
- Or run `python tools/r3_release_readiness.py --repo . --head "$(git rev-parse HEAD)" --json-output /tmp/r3-readiness.json --summary-output /tmp/r3-readiness.md` after a full-history checkout.
- The resulting artifact lists ALL exact changed paths, split into CONTENT,
  GOVERNANCE and EVIDENCE, plus whether required external variables and files
  are present. It never prints public-key roster contents and never requests
  private signing keys. A successful audit run is **not** successful release
  authorization and cannot be used as a required production-decision status.
- The audit uses the *candidate-tree policy diagnostically* and explicitly
  says so. `trusted/docs/agent-entry/production-control-r3/release.py`, from
  the administrator-pinned independent control commit, remains the sole
  authoritative release-stage validator.
- This audit has no `pages: write` or `id-token: write` permissions and
  cannot stage or deploy anything. `deploy.yaml` is intentionally unchanged.

### Required Owner / independent reviewer decisions

1. **Decide the release scope before signing.** Under
   `FREEZE_PENDING_GOLDEN` and no accepted Golden, a main revision with any
   changed CONTENT paths remains ineligible for ordinary Pages release. New
   learner content requires the separately approved R3/Owner Golden adoption
   or migration workpack. Do not classify unknown content as governance or
   move the frozen baseline just to reduce the count.
2. **Pin reviewed control infrastructure.** Independently review the control
   commit; the administrator sets `G9_R3_CONTROL_SHA` in
   **Settings → Secrets and variables → Actions → Variables** to that exact
   reviewed 40-character commit. Never substitute the candidate, HEAD or a
   test-generated SHA.
3. **Establish real trust.** The administrator sets `G9_R3_TRUST_JSON` to the
   independent, public-keys-only schema `g9-r3-trust/v1`. Store all private
   keys outside GitHub and the repository. Treat key presence as unverified
   until trusted signature verification passes.
4. **Create the independently inspected publication set.** Only after a
   legitimately eligible release tree is approved, create an explicit list
   of releasable paths; run the pre-existing `prepare.py` against a trusted
   control revision to produce an **unsigned** byte-pinned candidate manifest.
   Independent reviewer checks every path, source blob and digest.
5. **Obtain independently authorized receipts.** A real Owner, using a
   governed signer identity distinct from the author, signs a
   `PREVIEW_RELEASE` record bound to the exact manifest SHA-256 and content
   fingerprint. Commit the manifest and receipt without changing the
   approved content fingerprint. Do not generate signatures in CI.
6. **Verify the environment and run the real gate.** Demonstrate `main`
   branch protection, CODEOWNERS and protected `github-pages` environment.
   Run the **manual** `Deploy to GitHub Pages` workflow only when the actual
   frozen-content and authority constraints are satisfied. Do not interpret
   a green author test, read-only audit or owner-directed unreviewed preview
   as signed R3 production authorization.

**External blockers cannot be fixed by a GitHub code agent:** it cannot
assert independent review, supply approved public keys, sign in a human
Owner's name, install administrator variables through a PR, or override
the freeze. The red production job is the expected result until those
specific conditions are met.

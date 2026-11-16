# R3-C0/C1 — Containment and exact-tree reconciliation

**Status: PROPOSED RECOVERY / ACADEMIC HOLD / NO MERGE OR DEPLOY.** Native governing task: #62. Author-side recovery preparation; not independent review or Owner receipt.

## Observed incident

R3 installation checkpoint `c7338903b523bf6b03e90cb8efd2fe7805f8e754` (tree `4b4a44e97a7547d7df06b15e2cf226982c7fd984`). Observed main `76d60743c7ac51b44b3bf3cd37745db163e6a4bd` (tree `f840ed25ddaa994d2d32a50efaa27ddce7f12f42`), 216 commits ahead. GitHub branch metadata protected=false, rulesets empty. R3 policy still FREEZE_PENDING_GOLDEN; accepted_golden=null, production and academic release disabled. Six direct-to-main PR heads carried failure of g9/r3-production-decision (#68, #57, #56, #70, #54, #55). #63 merged into parent and is reachable through #54; #65 merged into parent but its merge commit is NOT an ancestor of observed main (do not claim all PH11 recovery landed). #71 evidence-only success did not certify its inherited base. A valid incremental decision does not retroactively approve a contaminated ancestor.

## Complete inventory

Both recursive Git trees returned non-truncated. 2,525 baseline leaves and 2,613 observed leaves; 154 changed paths (88 added, 66 modified, no deleted). Exact mode/type/object IDs in [inventory](PATH_RECONCILIATION.v1.json). 149 CONTENT paths per installed policy: Physics 60, Chemistry 55, test/runtime infrastructure 34. Five R3 intake evidence files, all regular tracked blobs, retained unchanged; retention is not endorsement of their claims. No governance paths changed in the net diff. No source question, QRT, B1–B7, academic qualification or rights decision inferred.

## Recovery construction

Preserve observed main at branch quarantine/r3-freeze-breach-76d60743 and immutable commit above. Construct a descendant of observed main using the exact installation tree plus the five evidence additions and this two-file reconciliation record. No force push or history removal. All 149 content paths return to their exact baseline objects (or baseline absence). All useful post-freeze work remains in the observed commit, quarantine ref, original PRs and history. Baseline is frozen technical reference ONLY, not an accepted Golden. No cherry-picking of learner routes or code from #69/#70 while recovering baseline.

## Publication

Current manual-dispatch deployment definition is unchanged. Actions query event=workflow_dispatch returned zero runs at intake. No deployment or external serving state verified; do not claim rollback of the live site. Existing release gate compares content to frozen baseline and requires independent external control pin and signed preview manifest. No publication requested.

## Required disposition and next actor

1. Owner/admin: activate no-bypass strict required PR protection and isolate status issuer; verify the exact required check cannot be produced by untrusted candidate workflows. Personal repository limitations may require independently controlled GitHub App or organization required workflow. Do not use temporary exemptions or merge a knowingly blocked candidate. Verify external trust roster and protected Pages environment. See #62 and ADMIN_SETUP.md at the installed checkpoint.
2. Owner + independent control reviewer: approve or reject this exact proposed restoration. Existing R3 gate correctly blocks ordinary content changes, including reversal. Recovery requires an explicit separately authorized, tightly bounded trusted recovery mechanism binding compromised base, prior trusted tree, exact proposed recovery tree/non-evidence fingerprint and Owner receipt, checking complete tree equality outside evidence. No general rollback exception; no author-generated trust keys or receipts. Do not merge this proposal while blocked.
3. Trusted enforcement must compare cumulative changes against last accepted production checkpoint, not merely the immediate base; tainted main must not be an authority anchor. Test a real rejection and status-spoof defense after admin configuration. No branch advance invalidates the incident record; regenerate candidate if main changes.
4. IR findings F01–F09 remain open, PR #69 remains diagnostic NO-GO; #70 is unapproved alternative infrastructure, not an accepted migration. Only after recovery and actual enforcement, reconcile reusable work on a new governed design, re-run positive and adversarial staged browser checks, then obtain independent Golden authority.

No academic acceptance, release, or verified administrator change. No main update performed by this workpack.

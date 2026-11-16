# Shared Assessment Engine R0 — isolated candidate, NOT production

Scope: Issue #67. R3 freeze remains effective. This is author-exposed prototype source; neither DESIGN/OWNER_SCOPE nor independent source/science/QRT/learning receipts exist. No accepted Golden.

Consumers: none. Neither Physics nor Chemistry learner reader imports this module. It does not fix the deployed learner pages.

## Staged feedback cycle
1. PREDICT saves hypothesis and conditions.
2. Optional HINT 1–3 saves monotonic exposure, permanently recording ASSISTED vs UNASSISTED first attempt.
3. ATTEMPT commits structured claim/model/reasoning/check.
4. REVEAL_RECONSTRUCTION records feedback exposure; the caller may then fetch verified model feedback. RECONSTRUCT requires explicit own-step/model-step/difference comparisons.
5. DIAGNOSE anchors the proposed first divergence to protected original attempt text. REVEAL_DIAGNOSTIC must precede model-specific repair.
6. REPAIR records corrected reasoning and independent check. REVEAL_BOUNDARY_TASK records a changed-condition task.
7. BOUNDARY saves fresh prediction/reasoning/falsifier BEFORE REVEAL_BOUNDARY_FEEDBACK.

Every record remains NOT_EVALUATED. Structural fields and a quoted original response alone are not semantic verification or proof of fresh cognition. Independent science-specific adapters and B1–B7 acceptance are not yet implemented.

## Storage
IndexedDbAttemptStore.commit performs read, expected-sequence CAS, append and write in ONE IndexedDB readwrite transaction for each task. A conflicting browser tab should get CONCURRENT_UPDATE, refresh and reconcile rather than overwrite. Corrupt/changed history, wrong revision, blocked IndexedDB, missing digest and invalid stage order fail closed; no localStorage fallback.

Local storage can be modified or deleted: event replay is not cryptographic tamper-proof security. A secure exam requires authenticated server-side submission and guarded answer access. Existing Physics/Chemistry localStorage history is NOT migrated and must not be silently overwritten.

## Assets
fetchPinnedAsset verifies bytes against SHA-256 supplied by a separately trusted manifest. The caller MUST commit the corresponding REVEAL event before downloading or mounting each answer-bearing asset, and MUST show HOLD when fetch fails. No preloading whole answer books in the final UI.

Public static assets can be downloaded directly regardless of client sequencing. Do not claim exam secrecy on GitHub Pages; mark PRACTICE_ONLY or build controlled backend.

## Tests
Run: node --test tools/shared-assessment/engine.test.mjs
Run: python -m pytest -q tests/test_shared_assessment_engine_r0.py
13 Node tests cover stage order, first-attempt immutability, assistance, response anchoring, replay/sequence corruption, digest and blocked storage.

Still required: real HTTP Chromium multi-tab IndexedDB race, quota/transaction-abort injection, network and DOM precommit answer leakage, 12.7-inch touch/keyboard/refresh, and real Physics/Chemistry adapter science tests. Local Chromium HTTP navigation was blocked by administrator policy (net::ERR_BLOCKED_BY_ADMINISTRATOR), so no real browser PASS is claimed.

## R3 hold
Main is FREEZE_PENDING_GOLDEN with no accepted Golden and Chemistry authority pending. New executable files are content under R3 even when isolated. This candidate will remain DRAFT and unmerged until an authorized infrastructure exception, signed independent workpack, accepted trusted decision and Owner approval are actually present. No academic approval inferred from software validation.

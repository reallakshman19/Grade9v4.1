# PH02 Forces — A02 R2 native integration and evidence handoff

**Task:** `G9V41-PHYS-C1AB-A02-PH02-R1` · [Issue #33](https://github.com/reallakshman19/Grade9v4.1/issues/33) · [Draft PR #34](https://github.com/reallakshman19/Grade9v4.1/pull/34).  
**Base:** PH01 PR #3 branch; starting SHA `6dd8c0000e710fc923e9d347123f78c17449ed7b`.  
**Scope:** A02 / PH02 only; candidate-only content with a narrowly scoped inherited CI runner fix.  
**Status:** `AUTHOR_EXPOSED · MECHANICAL_CANDIDATE · SCIENCE_HOLD · SOURCE_HOLD · QRT_HOLD · B1_B7_HOLD · NO_RELEASE`.

## Implemented content

- **Eight** independently addressable Core1A units at `nsejs/physics/textbook/PH02/F01...F08/index.html`. Chapter navigation: `nsejs/physics/textbook/PH02/index.html`.
- **Twenty-four** original Core1B INSTANCE task identities, three proposed distinct cognitive operations for each of the eight subtopics, using `?task=<exact-authored-UID>` on each subtopic route.
- **Six** cross-subtopic candidate MAIN cycles (EXPLAIN, APPLY, MODEL, REPRESENT, SYNTHESIZE, JUSTIFY), all accessible through `nsejs/physics/core1/PH02/main/index.html`. These are physically integrated author proposals, not validated B4 or D3 admissions.
- **Eight** native Core1A records, 24 QRT targets, 24 native INSTANCE and 6 MAIN records in `physics-topic-package.v1_1.json`; standalone adapter `topic-adapter.PH02.v0.1.0.json`. C01–C08 v1.1 mechanical package test added.
- Full authored content and science assumptions in `nsejs/physics/ph02/units.v1.json`; 16 additional non-clone candidate constructions + six integrated MAIN problems in `nsejs/physics/ph02/qrt-candidates.v1.json`.
- Controlled learning runtime: first prediction and explanation saved together, same task-revision immutable original, help H1/H2/H3 after successful persistence, reconstructed solution/diagnosis/repair in separate stages, fresh boundary attempt before its answer, fail-closed on denied storage, prior-revision keys retained. Public JS remains inspectable: not secure high-stakes invigilation.
- Dedicated Chromium workflow `.github/workflows/physics-ph02-browser-qa.yml` pinned to ubuntu-24.04; one-line inherited PH01 workflow compatibility fix in `.github/workflows/nsejs-physics-textbook-qa.yml` for Playwright 1.55.0.

## Verification receipts (exact revisions matter)

- [Run 43578559003](https://github.com/reallakshman19/Grade9v4.1/actions/runs/43578559003): unchanged Python 3.11 + 3.12 full suites, **393 passed, 1 warning** each, including new C01–C08 PH02 validator checks at that historical candidate SHA.
- [Run 43578558958](https://github.com/reallakshman19/Grade9v4.1/actions/runs/43578558958): supported-runner PH02 Chromium **61 checks**; 24 INSTANCE+6 MAIN ×2 viewports + failed-storage negative; reports `MECHANICAL_CHROMIUM_PASS__ACADEMIC_HOLD`.
- [Run 43579185656](https://github.com/reallakshman19/Grade9v4.1/actions/runs/43579185656): **inherited Physics textbook browser workflow PASS** after the ubuntu-24.04 pin.
- Newest exact HEAD requires its own CI inspection; older green runs are not inherited as approval for modified bytes.

## Official curriculum and exam custody

1. [CBSE Class IX 2026–27 Science curriculum](https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceSt_SecP1_2026-27.pdf), Force and Laws of Motion section, printed p.15: primary Newton laws/balanced force/friction; F05 representation support. F07 inclined planes and F08 connected-body events remain **advanced-extension scope HOLD**.
2. [IAPT 2026](https://iapt.org.in/) identifies NSEJS as PCB up to Class X; this is an examination scope statement, not an original question identity.
3. `official-2025-source-locators.v1.json` records publisher **2025 code 51 Q34** (string breaking, final key B) and **Q35** (bicycle friction, final key D). Source paper/text and final-key tables were publisher-indexed, but live visual PDF screenshot failed (502/challenge). Neither original PDF bytes nor stem/figure hash was acquired. These are **external locator-only source proposals**; the native Core2 source array correctly remains empty. DO NOT import their question text or keys into public learner runtime without source/rights/reviewer gates.

## R2 evidence packet status

The R2 quality policy on `main` is `PILOT_AWAITING_OWNER_GOLDEN`, `production_enabled=false`. The parent PR #3 branch does not yet include the R2 v2 schema/validator; the Owner-accepted Golden Sample SHA and scoped R01 reviewer receipts are missing.

`tools/physics_ph02_author_evidence_prep.py` generates eight **byte-grounded PREP, not official R2 packets**, from checked-out source lines, with actual SHA-256 and quoted snippets. The CI workflow uploads these as inspectable artifacts. It does **not** fabricate a Golden SHA, eight fault-family negative cases, authenticated original source, independent reviewers or an `EVIDENCE_STRUCTURALLY_GROUNDED` R2 result.

## Required next acceptance, in order

1. Exact-head QA: confirm full pytest, both browser workflows, 30-cycle native QA, real evidence-prep artifacts. Verify keyboard, stale content-revision and precommit hint attacks individually.
2. Independently review science derivations, figure physics, source scope and actual learner sufficiency for all eight; specifically challenge potential F04 instantaneous-contact, F08 taut-string and F07 incline caveats.
3. Cold source-only reviewer R01 must solve and score every actual target (shortest W and five factors, no D3 by assumption), verify B1–B7, anchor→fresh novelty and MAIN integration. Any failed item returns to author with exact SHA.
4. Source custodian must verify original examination papers, key version, figures and rights; admit authentic Core2 UIDs only after identity/version custody. External locators do not grant reader admission.
5. Owner selects a single representative complete Golden exemplar after genuine R00/R01 receipts; activate R2 policy/branch protection separately. Only then submit compatible R2 v2 packets for each governed content revision and risk-based batch review.
6. Do not merge/deploy or promote academic/release labels until Owner explicitly authorizes the exact reviewed revision. No Owner signature for every routine candidate after Golden adoption.

**No academic approval inferred from software validation.**

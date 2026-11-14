# Agent A Stage 2 — C07 and C01–C06 textbook candidate handoff

**Task:** `G9V41-NSEJS-CHEM-A-CORE1AB-C01-C07-R2`  
**Branch:** `feat/nsejs-chem-a-core1ab-c07-c01-c06-r2`  
**Parent contract branch:** `feat/nsejs-chem-a-stage0-stage1-contracts-r1` / Draft PR #1  
**Academic mode:** SOURCE_FIRST · QRT_CANDIDATE · CHEMISTRY_ONLY · FAIL_CLOSED.

## What has been authored

- 7 versioned connected Chemistry chapter packs: C01 matter, C02 mixtures, C03 chemical laws, C04 mole/stoichiometry, C05 atomic structure, C06 periodicity, C07 bonding/molecular structure.
- All **44 Agent A syllabus subtopics** mapped by stable IDs and explicit scope classifications.
- **132 distinct authored primary QRT demand instances** (88 proposed D3; 44 proposed D4), each with explanatory Core1A steps and separate Core1B predict/attempt/reconstruct/diagnose/repair/boundary/model-response fields, plus three hint levels.
- 7 Topic Adapter JSON files conforming to the existing Stage 1 candidate schema; every subtopic has 3 **distinct primary cognitive operations**. This is not 132 new QRT template definitions or academically accepted cells.
- Canonical author-draft concept registry with 44 source-path/blob refs and preserved C07 alias mapping for Agent B.
- One shared HTTP candidate reader, 7 unit routes, a contents route, 4 accessible C07 scientific SVGs, and localStorage first-attempt protection keyed to the SHA-256 bytes of the **entire** authored content revision.
- Python `jsonschema`/QRT/content contract tests and HTTP Chromium candidate tablet test script and workflow.

## Why this is textbook-first

The learner reads connected scientific mechanism, observations, representation and worked example **before** the demand cards. The Core1B tasks ask for a new inference and initially conceal the solution until a first response is saved.

The candidate HTML is a pedagogical review preview. It is deliberately **not linked into the public NSEJS hub**, and no existing source or exam question page has been replaced.

## Detailed counts

| Unit | Subtopics | Core1B candidate tasks |
| --- | ---: | ---: |
| C01 States of Matter | 6 | 18 |
| C02 Mixtures and Separation | 7 | 21 |
| C03 Atoms and Chemical Laws | 6 | 18 |
| C04 Mole Concept | 6 | 18 |
| C05 Atomic Structure | 6 | 18 |
| C06 Periodicity | 6 | 18 |
| C07 Chemical Bonding | 7 | 21 |
| **Total** | **44** | **132** |

**Changes relative to Stage 0 planned operation sets:** 17 of 44 subtopics select a different combination of three operations after actual authoring. These deviations are recorded in `registry/agent-a-stage2-coverage.v0.1.0.json`, not silently declared identical.

## Review qualifications and strict HOLDs

- **Academic content truth:** author-draft; not independently reviewed by a qualified Chemistry academic.
- **D3/D4 bands:** proposals only; the five-factor rubric has not been independently scored or compared with nearby levels.
- **12 per-QRT criteria:** source QRT templates remain pinned. A semantic 12-question QRT/B1–B7 review receipt is **not** automatically produced.
- **Curriculum source fidelity:** exact lower-grade crosswalk and edition-by-edition academic admission remain open. C04 advanced ratios/yield, C05 subshells and C07 geometry are explicitly scope-labelled.
- **Exam source/keys and copyright:** existing source HOLDs are preserved; this package claims **no** official NSEJS question identity.
- **UI/runtime:** HTTP browser QA is separate from Python structural CI and must be checked on the exact PR head. The preview does not guarantee secure concealment from browser developer tools; it provides learner-flow attempt protection, not security for high-stakes testing.
- **Student release:** NOT_AUTHORIZED.

## Agent B cross-unit consumption

Agent B should reference canonical IDs under `registry/agent-a-canonical-concepts.v0.1.0.json`. For C09 acids and oxyacids use C03.04 formula/charge, C04.03 mole ratios, C07.01–.05 bonding/connectivity. For C11 organic chemistry reference C07.03–.07. For C13 redox reuse C04.04 and C05.05. **These concept records remain author-drafts**, so dependencies are usable for draft composition but not for academic acceptance.

## Review path

1. Run full Python QA on PR exact head.
2. Run HTTP Chromium portrait 1000×1600 and landscape 1600×1000; test first-answer save, refresh, disabled storage, layout overflow, figures and keyboard.
3. Perform independent scientific accuracy and scope review of each chapter, starting with C07 (high-priority) and C04/C05 (advanced-scope risk).
4. Run individual QRT band and 12-question semantic review per construction; collect B1–B7 where applicable.
5. Publish qualified content only with owner approval and complete relevant review receipts.

**No academic approval inferred from software validation.** No merge or deployment requested.

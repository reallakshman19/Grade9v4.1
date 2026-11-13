# Agent 1 — PH01 Motion and Kinematics R2 (author-exposed candidate)

**Task:** G9V41-NSEJS-PHYSICS-AGENT1-PH01-R2
**Parent contracts:** C01–C08 v1.0.0 in Draft PR #2; candidate C06 v1.1.0 amendment on this branch.
**Branch/PR:** feat/nsejs-physics-agent1-ph01-kinematics-r1 / Draft PR #3.
**Authority:** ENGINEERING_CANDIDATE · SCIENTIFIC_HOLD · INDEPENDENT_QRT_HOLD · B1–B7_HOLD · NO_MERGE_OR_DEPLOY.

Agent 1 owns PH01–PH06; Agent 2 owns PH07–PH12. PH02–PH06 are **inventoried, not authored or qualified**.

## What exists now

| Deliverable | Actual state |
|---|---|
| [PH01 readable textbook](../../../textbook/PH01/index.html) | Authored: 11 connected sections, two accessible original SVG diagrams, interactive reference-frame exploration, worked derivations and five textbook investigations |
| [PH01 scope and QRT coverage ledger](ph01-subtopic-qrt-coverage.v1.json) | Eight textbook subtopics, **three with draft QRT constructions**, five QRT gaps |
| [PH01 R2 topic package](physics-topic-package.v1_1.json) | Three Core1A subtopic constructions, nine proposed D3 tasks across MODEL, REPRESENT and SYNTHESIZE |
| [PH01 R2 adapter](topic-adapter.PH01.v0.2.0.json) | Three Blueprint cells D3.4/D3.5/D3.6, each with three subtopic instances |
| [Candidate Core1B learner page](../../../core1/ph01-qrt-r2/index.html) | Twelve cycles: three combined MAIN, nine INSTANCE; first-answer protection, hints, repair and boundary testing |
| [H1/H2/H3 and boundary support](ph01-core1b-support.v1.json) | Task-specific hints and complete changed-condition explanations for all 12 cycles |
| [C06 resolution record](contract-gap-C06-MAIN-join-resolution.v1.json) | Engineering candidate resolution; Owner/Oracle and academic acceptance pending |

The earlier [v1 topic package](physics-topic-package.v1.json) and [v0.1 adapter](topic-adapter.PH01.v0.1.0.json) remain unchanged for compatibility.

## Three PH01 subtopics now carrying draft QRTs

| Subtopic | MODEL D3.4 | REPRESENT D3.5 | SYNTHESIZE D3.6 |
|---|---|---|---|
| PH01-M03 — Speed and velocity | Choose a path/displacement average model | Translate signed travel legs into position history | Recover unknown leg lengths and test feasibility |
| PH01-M05 — Motion graphs | Choose slope/area model for the question | Translate position samples to signed velocity intervals | Recover missing velocity from signed areas |
| PH01-M07 — Relative and piecewise motion | Select observer, frame and stage model | Translate positions across observers | Reject an out-of-domain meeting root and rebuild the correct stage |

All nine D3 labels and five-factor scores are author proposals, not independent academic QRT verdicts. There are **zero** accepted D4 targets and **zero** qualified authentic exam-source items.

## Five PH01 QRT gaps

PH01-M01 measurement/reference directions; PH01-M02 distance/displacement; PH01-M04 acceleration; PH01-M06 constant-acceleration equations; PH01-M08 elementary circular motion.

These five have textbook sections but lack standalone three-operation QRT packs, independent science checking and B1–B7 qualification. Do not mistake a textbook section for a completed learning route.

## C06 MAIN integration contract

Original v1 had no way to guarantee a single MAIN combines multiple subtopic instances. In the candidate v1.1 amendment:

- [Versioned C06 contract](../../contracts/core-contracts.v1_1.json)
- [Versioned topic-package schema](../../contracts/physics-topic-package.v1_1.schema.json)
- [Version-aware validator](../../contracts/tools/validate_physics_contracts.py)

The validator requires exactly one MAIN per cell, at least two distinct subtopic instances, coverage of all the cell's instances, no cross-cell contamination, and one INSTANCE cycle per target. The earlier v1 files remain valid. The original [gap record](contract-gap-C06-MAIN-join.v1.json) is preserved; its [candidate resolution](contract-gap-C06-MAIN-join-resolution.v1.json) is still pending Owner/Oracle approval. **No Physics Blueprint rule was altered.**

## Protected attempt runtime and limits

The Core1B page uses same-origin JSON package/support, computes a SHA-256 content revision from their exact bytes, and stores the first prediction/answer in a revision-specific browser storage key before hints or reconstruction are unlocked. H1/H2/H3 support, diagnosis self-report, repair, boundary attempt, and linked textbook help exposure are recorded separately. When storage is disabled, learners can type and copy their work but hints/answers remain locked.

The runtime marks mastery as UNASSESSED. Client-side self-study cannot be called secure invigilation, independent academic review or observed child mastery. Qualitative B3/B4/B6 and all remaining B1–B7 scientific evidence are still HOLD.

## Verify

    python -m pip install -e ".[dev]"
    python nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1_1.json
    python -m pytest -q
    python tools/physics_textbook_browser_qa.py
    python tools/physics_ph01_core1b_browser_qa.py

Chromium QA uses 1000×1600 portrait and 1600×1000 landscape. It checks protected first answer, staged hints, revisions, changed-condition answers, refresh, help exposure, stale revisions, disabled storage, responsive overflow and errors. Exact-head workflow receipts are linked from Draft PR #3.

**All scientific and release gates HOLD.** The Physics Blueprint remains DRAFT_OWNER_REVIEW, D3.1 PAUSED, WPE selected adapter UNSELECTED and D1/D2 SPEC_PENDING. No merge or deployment without Owner approval and independent academic review.

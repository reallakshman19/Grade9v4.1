# Agent 2 — PH07–PH12 authoring first slice

Task: `G9V41-NSEJS-PHYSICS-AGENT2-PH07-PH12-R1`  
Owner: AGENT_2 · AUTHOR_EXPOSED · PHYSICS_ONLY · FAIL_CLOSED

This **stacked, draft** slice introduces six separately schema-shaped authoring **lead constructions**, one per assigned topic, and carries forward the 83-subtopic Phase 0 planning register. The Core1A leads have worked examples, scientific conditions and misconception repair; the separate Core1B records are authored task specifications, **not functional assessed browser journeys**.

**Not claimed:** six finished chapters, 83 completed subtopics, tested learner mastery, independently approved D3/D4 questions, authenticated Core2 questions, B1–B7 pass, rights clearance or permission to release. Academic/release status is HOLD.

| Topic | Proposed subtopics in Phase 0 | Authored lead | Candidate QRT operations | Remaining unwritten |
|---|---:|---|---|---:|
| PH07 | 12 | PH07-05 | EXPLAIN / MODEL / SYNTHESIZE | 11 |
| PH08 | 13 | PH08-08 | MODEL / APPLY / REPRESENT | 12 |
| PH09 | 12 | PH09-08 | EXPLAIN / MODEL / JUSTIFY | 11 |
| PH10 | 17 | PH10-09 | MODEL / SYNTHESIZE / JUSTIFY | 16 |
| PH11 | 14 | PH11-07 | MODEL / APPLY / REPRESENT | 13 |
| PH12 | 15 | PH12-09 | EXPLAIN / MODEL / REPRESENT | 14 |

## Parent contracts and pins
- Stacked base: `feat/nsejs-physics-core-contracts-c01-c08-r1` @ `330f9524fe37cff53f20b6f094c85e4739da3a66` (Draft PR #2; not merged)
- C01–C08: v1.0.0 engineering candidate
- Physics Blueprint: v0.2.0, blob `700dafcbe86d76442637bcf214eeb544497cf4ea`, DRAFT_OWNER_REVIEW
- Shared 28 QRT: Grade9v3.5 @ `574c7fe2`, blob `e2409aef11ae7d98444593bfbe1a38eb00c97cef`, EXTERNAL_PIN_UNQUALIFIED
- D1/D2: SPEC_PENDING; WPE adapter: UNSELECTED. D3.1 remains PAUSED.

## Verification
Run separately for each of six candidate packages:

```bash
python nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py nsejs/physics/curriculum/topics/PH08/physics-topic-package.v1.json
python -m pytest -q
```

Mechanical validation requires exact pins, valid references, >=3 distinct proposed QRT operations per authored lead, C05 examples in FOUNDATION/CONNECTED/ADVANCED tiers, and Core1B MAIN+INSTANCE cycles. The schema validator intentionally **does not** prove pedagogical quality, task novelty or correctness.

## Explicit outstanding work
- Expand all remaining 77 subtopics into full continuous Core1A chapters.
- Write and independently verify original figures, physical warrants and full solutions for all task stages.
- Build learner-facing Core1B runtime with protected first attempts, refresh, keyboard and storage-disabled tests.
- Reconcile original optical, circuit and magnetism candidate source questions without copying nonpublic source material; zero authenticated Core2 admissions.
- Obtain independent physics/QRT/B1–B7 reviews and Owner decision before any academic promotion, merge or deployment.

**No academic approval inferred from software validation.**

## Continuous textbook pilots added after first-slice authoring

- `topics/PH08/CHAPTER_CONTINUOUS_DRAFT.md`: connected Sound & Waves manuscript spanning 13 teaching sections, with original echo diagram `topics/PH08/figures/lead-concept.svg`.
- `topics/PH10/CHAPTER_CONTINUOUS_DRAFT.md`: connected Refraction/Lenses/Human Eye manuscript spanning 17 teaching sections, with a geometric lens-position diagram `topics/PH10/figures/lead-concept.svg`.

These manuscripts introduce the wider curriculum narrative but **are not** yet native C05/C06 accepted constructions for all listed subtopics. They require scientific and pedagogy review, native data binding and complete learner-runtime QA. Do not count their headings as an accepted chapter-completeness tally.

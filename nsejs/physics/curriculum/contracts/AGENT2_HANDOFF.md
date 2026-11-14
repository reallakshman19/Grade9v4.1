# Owner → Agent 2: PH07–PH12 Physics Authoring Onboarding (R1)

**Task:** G9V41-NSEJS-PHYSICS-AGENT2-PH07-PH12-R1
**Mode:** AUTHOR_EXPOSED · PHYSICS_ONLY · D3/D4_PRIORITY · READ_BEFORE_WRITE · FAIL_CLOSED
**Repository:** https://github.com/reallakshman19/Grade9v4.1
**Planning base:** 82a782f12c57b5d9d25e9b1eb8d2053a56dfabc0. Reconfirm current upstream HEAD before creating your own branch.
**Shared contract candidate:** nsejs/physics/curriculum/contracts/core-contracts.v1.json, version 1.0.0
**Authoring package schema:** nsejs/physics/curriculum/contracts/physics-topic-package.v1.schema.json

## Your exclusive topic ownership

| Topic | Scope | Key advanced constructions |
|---|---|---|
| PH07 | Heat and thermal physics | Thermal exchange, heating/phase transitions, competing heat-transfer assumptions |
| PH08 | Sound and waves | Reflection/echo timing, multiple path lengths, source/reflector motion |
| PH09 | Reflection and mirrors | Moving images, sign conventions, coupled mirror configurations |
| PH10 | Refraction, lenses, human eye | Conjugate imaging, multiple optical stages, inverse image problems |
| PH11 | Current electricity | Circuit loading, resistance and power constraints, equivalent networks |
| PH12 | Magnetic effects and induction | Field direction, current reversal, magnetic forces, induction boundaries |

Do not modify PH01–PH06, shared manifests, Shared 28 QRT templates, Physics Blueprint, WPE pilot schema, or external source-status ledgers. Agent 1 owns shared contracts and reconciles the integrated syllabus.

## First phase: inventory (read-only)

1. Read AGENTS.md, Start_here.md, CURRENT_CHECKPOINT.md, docs/product-scope.md, docs/agent-entry/CURRENT_CONCEPT_COMPANION.md, docs/agent-entry/03-blueprint-adapters.md, architecture/guidebook.html and the C01–C08 README.
2. Read the existing Physics Blueprint v0.2.0 and the actual 28 Shared QRT templates at the pinned source; disclose that the Shared source is external.
3. Identify each PH07–PH12 subtopic and all prerequisites from official CBSE/IAPT/NCERT evidence. Mark expansions beyond the verified syllabus as EXTENSION, never quietly mandatory.
4. Inventory the existing nsejs/physics pages, public candidate Core2 records and authored preview/recovery materials, preserving their existing identities and HOLDs.
5. Return a *read-only* table: topic/subtopic ID, official source reference, scientific model, missing textbook coverage, three candidate cognitive operations, likely D3/D4 target tasks, exact source custody, dependencies, and unresolved scientific/academic HOLD.

## Second phase: candidate packages (after C01–C08 branch becomes an accepted common base)

For each assigned topic author a separate candidate package conforming to the strict schema. The available synthetic PH01 fixture is a **schema illustration only**; do not reuse its science, evidence wording, operation choices, or factor scores for your topics.

Populate:

- C01 syllabus identity, references and stable subtopics;
- C02 verified/candidate scientific knowledge, limits, signs and source-specific warrants;
- C03 at least three defensible distinct primary operations per substantive subtopic, with task-specific five-factor demand evidence;
- C04 candidate adapter cells bound to Physics Blueprint v0.2.0 and your local topic instances;
- C05 a genuinely readable explanatory Core1A chapter, not an exam-answer-key collage;
- C06 MAIN-plus-instance six-stage fresh transfer tasks, protected W, saved first attempt and exposure semantics;
- C07 source-specific Core2 metadata, distinguishing authentic exam items from authored/bridging questions;
- C08 seven separate acceptance gates, B1–B7 and Owner decision HOLD.

Use candidate adapter IDs PHYS-TOPIC-PH07 … PHYS-TOPIC-PH12. Reuse and pin canonical Physics scientific references; never duplicate inconsistent law definitions. The D1/D2 shared Blueprint is SPEC_PENDING, so teach elementary foundations without claiming final D1/D2 QRT qualification.

## Checks

Run from repository root:

    python -m pip install -e ".[dev]"
    python nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py <your-topic-package.json>
    python -m pytest -q tests/test_nsejs_physics_core_contracts.py
    python -m pytest -q

A mechanical PASS means only that the candidate file meets the shape, references, owner partition and fail-closed requirements. Never interpret it as physics correctness, source authenticity, independent QRT, child mastery or release.

Also provide your actual chapter/figure review evidence, syntax regressions, and (when runtime changes are proposed) real Chromium 12.7-inch portrait/landscape checks including keyboard, refresh, help exposure and blocked storage.

## Contract change request procedure

If a scientifically valid PH07–PH12 construction cannot be expressed using the candidate schema or Physics Blueprint:

1. Stop the affected construction only; retain other independent progress.
2. Identify exact topic/subtopic, QRT task and protected W.
3. Report missing field or shared rule, actual file hash/version and reproducible candidate failure.
4. Separate **topic-adapter extension** (which you may author in your scope) from **generic Core Contract/Blueprint gap** (which Agent 1 must reconcile and the designated authority must approve).
5. Do not patch the shared source, invent new D4 thresholds, bypass source rights, or promote a HOLD.

## Handoff to Agent 1

Return six topic-package paths and content versions; science/source/QRT coverage registers; chapter and figure inventories; direct-exam/source-role map; overlap/dependency list; exact validation receipts and remaining academic HOLDs.

Create a separate **draft PR** against the mutually pinned contract base, not main independently if contract compatibility is unresolved. No merge, deployment, public source disclosure, or academic publication without explicit Owner approval and separate independent qualification.

**Known prerequisites still on HOLD:** Physics Blueprint v0.2.0 remains DRAFT_OWNER_REVIEW, D3.1 is PAUSED, WPE canonical adapter is unselected, the 28 Shared templates are external to v4.1, and current repo material does not prove full syllabus coverage.

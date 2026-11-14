# NSEJS Physics — Core Contracts C01–C08 (engineering R1)

**Task:** G9V41-NSEJS-PHYSICS-TWO-AGENT-D3D4-R1
**Contract version:** 1.0.0
**State:** ENGINEERING_CANDIDATE__ACADEMIC_HOLD
**Subject:** Physics only; academic track NSEJS
**Owner:** Agent 1 (contracts and PH01–PH06); Agent 2 owns PH07–PH12 content.
**Baseline:** reallakshman19/Grade9v4.1 @ 82a782f12c57b5d9d25e9b1eb8d2053a56dfabc0.

This folder is a working, testable **engineering interface**, not an accepted scientific curriculum, examination-custody receipt, independent QRT verdict, B1–B7 pass, verified lesson or authorization to deploy. It does **not** modify the Shared 28-QRT source, Physics Blueprint, historical WPE pilot IDs, or live NSEJS pages. The provenance and review rules already enforced by AGENTS.md and architecture/guidebook.html remain above it.

## Pinned dependencies and conflicts

| Dependency | Exact source | Disposition |
|---|---|---|
| 28 Shared QRT templates | Grade9v3.5 @ 574c7fe2, Shared/quality/question-demand-templates.v1.json, blob e2409aef11ae7d98444593bfbe1a38eb00c97cef | External pin; content was inspected, but not bundled or independently qualified |
| Physics Blueprint | templates/physics-blueprint/physics-blueprint.D3-D4.json, v0.2.0, blob 700dafcbe86d76442637bcf214eeb544497cf4ea | DRAFT_OWNER_REVIEW, 14 D3/D4 cells |
| Resolved Physics Blueprint | templates/physics-blueprint/physics-blueprint.D3-D4.resolved.v0.2.0.json, blob b53b970d9ff99e696e84fe6b77805dbf25e0c544 | A derived draft; no approval inferred |
| D3 subtile addendum | templates/physics-blueprint/subtiles/physics-blueprint.D3.v0.2.1.json, blob b5294b8e510098bef5b3cb3d50658f8748bfda8b | DRAFT; D3.1 remains PAUSED |
| WPE topic adapter | Historical owner-local workspace/subjects/physics/adapters/root-draft/topic-adapter.work-power-energy.json | Not present in current public tree; no approved selected variant |
| D1/D2 shared Blueprint | SPEC_PENDING | Foundation teaching can proceed; no invented D1/D2 approval/scoring |
| Upstream master issue | https://github.com/reallakshman19/Grade9v4.0/issues/1 | Connector returned 404 on this review; preserve existing AGENTS rules and do not claim a fully verified upstream specification |

The local validator checks the bytes of the three Physics Blueprint files against pinned *Git blob SHA-1* identities. An external Shared QRT library is not authenticated merely by a checksum declaration. Content science and learner behavior require independent evidence even when every local test passes.

## Authority separation and versioning

1. **Shared/Owner:** canonical learning roles, source/rights custody, review and release authority.
2. **Physics Blueprint:** Physics-only D3/D4 cognitive rules and seven operations; versioned separately.
3. **Physics subject library:** scientifically reviewed laws, assumptions and warrants.
4. **Topic Adapter:** topic-specific instances and references; no custom cognitive definitions.
5. **Task-specific QRT reviewer:** independent primary-operation, demand and source-role adjudication.
6. **Core1A/B author:** teaching and fresh learning problems without assuming review authority.
7. **Grade9QA:** mechanical reconciliation, structural tests and evidence gap reporting, never reviewer replacement.

A builder changes topic-specific facts only in its topic adapter (and appropriate draft manuscript/knowledge candidate), NOT the shared library's demand definitions. If a required teaching operation is missing from the Blueprint, submit a versioned gap note with the exact task, required slot, current versions, what failed, and proposed general rule. A separate Blueprint owner/Oracle decision is required before changing that Blueprint. The WPE D3.1 pause is not cleared by creating this contract.

For new Physics topics, use topic IDs PH01–PH12 and candidate adapter IDs PHYS-TOPIC-PH01 through PHYS-TOPIC-PH12. **Do not rename old WEP task IDs or rewrite the WPE v1 schemas.** PH04 must reconcile the authentic WPE adapter before a migration can be accepted; a PH04 candidate shell is not an approved WPE replacement.

For changes: append new subtopics with stable IDs and semantically versioned adapter content; correct a fact with an explicit changelog and affected-dependency audit; never retroactively change an earlier learner attempt or source digest. Changing an existing scientific model or a protected decision requires a semantic review, not just a patch-number increment.

## C01 — Syllabus registry

Each chapter/subtopic has stable topic- and subtopic-scoped IDs; a syllabus source locator; scope role (SYLLABUS_CORE_CANDIDATE, PREREQUISITE_BRIDGE, EXTENSION); stated prerequisites; and a standalone learning objective. Classify each official-content claim individually rather than treating a coaching-list title as authoritative. PH00 measurement and PH13 experimental synthesis are shared strands, not extra topics counted toward the 6+6 allocation. Topic scope is a candidate until source review.

**Failure examples:** orphan subtopic ID; PH11 content placed under PH01; absent official syllabus reference; advanced Bernoulli or electrostatics silently promoted to required syllabus.

**Engineering acceptance:** complete registry shape, disjoint ownership, machine-valid prerequisites and an explicit coverage register. Actual syllabus completeness remains subject to separate source-level review.

## C02 — Physics scientific knowledge and warrants

Store a single reusable canonical law or model per science record, with statement, assumptions, applicability bounds, reference identity, consistent units/sign convention and science-review disposition. Topic adapters reference these records rather than copying unverified formula fragments. Exposition and textbook figures form a **separate source route** from question-bank identity/QRT classification; both meet only after reviewed requirements are available.

**Failure examples:** buoyancy in a non-inertial frame without frame conditions; conflating signed displacement and path length; missing source support for an advanced law; converting provisional formula metadata into verified scientific truth.

**Engineering acceptance:** structured law/assumption/limit metadata, valid reference graph and explicit HOLD for unreviewed science.

## C03 — QRT and demand bindings

Use the existing seven operations exactly and in order:

    1 RETRIEVE  2 EXPLAIN  3 APPLY  4 MODEL
    5 REPRESENT  6 SYNTHESIZE  7 JUSTIFY

Each exact target task has one primary operation, its D3/D4 candidate band, the matching Physics cell, an explicitly protected learner decision W, the shortest credible reasoning route, and the five 0–2 factor evidence records. D3 means total 6–7 and D4 total 8–10 **under the current draft Physics method**. These mechanical totals are never automatic QRT/admission decisions.

Each substantive subtopic is required to propose at least three **distinct** cognitive operations. A cell should not be filled with artificial D4 tasks simply to achieve numerical coverage. An unsuitable target is marked HOLD or replaced with a better candidate in the *same operation* only if scientifically justified; alternatively record a genuine exception/gap for Owner review. A single task is counted in only its reviewed primary operation, even when secondary operations contribute.

The 28 shared templates are a matrix of 7 operations × D1–D4. The currently adopted Physics *candidate* implements only the 14 D3/D4 tiles. D1/D2 textbook progression is pedagogical until the separate D1/D2 common Blueprint is specified.

**Engineering acceptance:** exact D3.n/D4.n mapping to the operation's position, evidence-bearing factor scores, protected-work definitions and independent review status. No derived claim of approved D4.

## C04 — Topic Adapter

Topic-specific adapter records bind verified/candidate scientific references, subtopic instances, QRT cell IDs, scenarios, misconceptions, figures and examination anchors to the Physics Blueprint. The adapter ID, topic ID, semantic version, Blueprint version and content hash form the identity. A cell references its instance IDs rather than making its own demand definition.

Agent 1 owns PH01–PH06; Agent 2 owns PH07–PH12. The adapter can be appended or amended under its owning topic. The Blueprint, Shared QRT library, generic source contracts and native validators are **not** part of the agent's writable surface.

**Engineering acceptance:** no duplicated/cross-topic instances, stable references, no broken prior version, all declared QRT tasks bound to a valid adapter cell.

## C05 — Core1A textbook

The learner reads a **continuous textbook topic**, not a set of difficult question keys. At minimum, the author's topic package contains:

- A physical phenomenon, accessible explanatory narrative and scientifically correct prerequisites.
- Progressive model construction and derivation steps with a **why valid** warrant.
- Limits, assumptions, units and sign conventions, with original useful illustrations.
- Three example *teaching tiers*: FOUNDATION, CONNECTED and ADVANCED (these are not automatically certified D1/D2/D3 bands).
- A plausible misconception, discriminating diagnostic and a repaired model.
- An exit question with complete answer and justification.
- Exact references from the appropriate scientific and syllabus records.

The book is a top-level narrative; individual QRT tile pages may retain the existing exam → Core1A → Core1B → return-to-exam sequence. This contract does **not** silently change the native Blueprint page anatomy.

**Engineering acceptance:** structurally complete manuscript, topic-QRT link consistency and scientific review requirements. Actual pedagogical sufficiency (B3) is qualitative and cannot be proved by word count or field population.

## C06 — Core1B protected transfer

For every QRT construction, provide its candidate MAIN plus per-instance fresh reconstruction cycles. Every cycle must have Predict → Attempt → Reconstruct → Diagnose → Repair → Boundary test. The protected first answer and timestamp are retained before hints/answer reveal, exposure history is separate, revisions are separate, and disabled storage does not unlock the answer in an unrecorded state. The true decisive step W must remain withheld before first submission.

A synthetic JSON assertion that a task is "fresh" is not itself B4 proof; exact wording and cognitive isomorphism require review. The runtime must demonstrate keyboard use, refresh behavior, source return, and storage-disabled fail-closed behavior.

**Engineering acceptance:** cycles/refs present, non-duplicate attempt tasks, native review evidence. Completion counters or helped correct answers are not independent mastery claims.

## C07 — Core2 source custody

Separate DIRECT_EXAM_EVIDENCE, PREREQUISITE_BRIDGE and AUTHORED_TRANSFER. For a real examination claim, pin exact exam/year/paper/code/question/figure/key provenance, source digest and custodian review. A generated diagram, a transcription or an answer key cannot manufacture source authenticity. Do not publish restricted source texts or figures merely because a private local ZIP is available.

The zero-exam synthetic fixture here has an empty core2_sources list. The tile UI must say "No qualified exam question yet" rather than fabricate one. An authored D4 challenge can teach transfer but cannot count toward the direct-exam target.

**Engineering acceptance:** exact-source link identity and a non-compensatory source HOLD until independently verified.

## C08 — Acceptance and release

Seven independent gates must be recorded separately:

    source_authenticity
    content_correctness
    cognitive_qualification
    teaching_sufficiency
    assessment_validity
    implementation
    release_authority

In addition, preserve B1 Target, B2 Signature, B3 Teaching sufficiency, B4 Fresh reconstruction, B5 Protected attempt, B6 Diagnosis/transfer and B7 Physics/provenance. The author cannot grant a reviewed status simply by submitting a filled form. Independent QRT is sealed from source-only input without author labels or answer/key exposure; the author may not impersonate the reviewer.

This candidate schema only permits **HOLD** or **NOT_RUN** gate states and **HOLD** release. Positive academic and release receipts must pass through the separately authorized acceptance system. Native QA results or a schema PASS are not review receipts.

## Interface and file boundaries

The manifest and native candidate schema live here:

    nsejs/physics/curriculum/contracts/core-contracts.v1.json
    nsejs/physics/curriculum/contracts/physics-topic-package.v1.schema.json

Each agent writes candidate packages under its own topic directory, with an adapter, science records, Core1A manuscript, Core1B cycles and source references. The present schema intentionally models a **candidate package**; final publication does not rely on changing a candidate's status to APPROVED in place.

The first synthetic fixture:

    nsejs/physics/curriculum/contracts/fixtures/physics-topic.synthetic.valid.json

It contains one PH01 synthetic subtopic with three candidate operations and no real examination claim. It is neither a finished PH01 textbook nor approved scientific evidence. Do not count it as produced curriculum.

## Mechanical verification

From the repository root after installing Python 3.11+ dev requirements:

    python -m pip install -e ".[dev]"
    python nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py nsejs/physics/curriculum/contracts/fixtures/physics-topic.synthetic.valid.json
    python -m pytest -q tests/test_nsejs_physics_core_contracts.py

Expected on the unchanged pinned branch: **mechanical_status PASS**, **academic_status HOLD**, **release_status HOLD**. Test authors must run and record results; do not claim success from this document alone. No network or protected source files are required for this synthetic contract fixture.

The local validator additionally checks: exact topic owner partition, pinned Physics Blueprint file bytes, QRT operation/score/cell consistency, minimum three distinct operations, uniqueness, science and syllabus references, adapter cell coverage, Core1A progressive levels, Core1B MAIN and per-instance cycles, source authenticity links and fail-closed gates.

It does **not** establish actual Physics correctness, authenticated external QRT bytes, visual quality, independent QRT, source publication rights, 12.7-inch Chromium behavior or learner mastery.

## Work split and sequencing

- **Agent 1:** the eight shared engineering contracts and global reconciliation; candidate content PH01 Motion/Kinematics, PH02 Forces, PH03 Momentum/Collisions, PH04 WPE, PH05 Gravitation, PH06 Fluids.
- **Agent 2:** candidate content PH07 Heat, PH08 Sound, PH09 Mirrors, PH10 Lenses/Eye, PH11 Current Electricity, PH12 Magnetic Effects/Induction.
- **Shared:** PH00 measurement/graphs and PH13 experimental integration, with Agent 1 maintaining registry identifiers and Agent 2 permitted to reference them.
- **Authoring order:** read-only syllabus inventory and reviewed reference sources first; topic/adapters and scientific warrants next; full textbook narrative; fresh Core1B; source-qualified Core2; independent academic and browser gates.
- **Integration:** merge *candidate work* only upon explicit Owner direction after reviewed PR-level evidence. No CI status can override an academic HOLD.

## Known outstanding decisions

1. The upstream v4.0 Issue #1 was not retrievable through the connected GitHub tool during this implementation; do not claim its entire text has been revalidated.
2. The root WPE adapter in Owner-local workspace is not available in the public v4.1 tree, and competing variants exist. The actual selected version remains UNSELECTED.
3. The 28 shared QRT template bytes are pinned to an external Grade9v3.5 commit, not copied into this branch.
4. Physics Blueprint v0.2.0 remains DRAFT_OWNER_REVIEW, D3.1 PAUSED; the D1/D2 shared Blueprint remains SPEC_PENDING.
5. The present contract fixture and tests are synthetic, and no authored PH01–PH12 chapter is academically qualified by this PR.
6. Topic-by-topic official syllabus scope, source rights, independent science review and real-browser acceptance still require separate evidence.

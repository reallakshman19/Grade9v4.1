# PH09–PH12 — WPE-parity recovery R1

**Mode:** `AUTHOR_EXPOSED · SOURCE_FIRST · TECHNICAL_RECONCILIATION · FAIL_CLOSED`  
**Repository:** `reallakshman19/Grade9v4.1`  
**Base:** `main@36198f29c1c002a958c5ce941e6f5de292069ebb` (2026-11-15 review baseline)  
**Disposition:** **DRAFT WORKPACK · ACADEMIC HOLD · NO MERGE / NO DEPLOY / NO CLAIM OF NSEJS QUESTION AUTHENTICITY**.

## Why this batch exists

The WPE pilot offered a coherent, bounded `teach → attempt a fresh decision → reconstruct → diagnose → repair → boundary-test` experience. Its educational usefulness did **not** grant academic admission. NSEJS has more content candidates but has not established the same source-exact, scientific, cognitive and learner-journey evidence across the intended syllabus. The response is to qualify existing work before expanding page counts.

The older Agent 2 register still shows just **two lead native candidates per chapter** for PH09–PH12. It is a **historical planning snapshot**, not the current page inventory. In particular, PH09 and PH10 were subsequently expanded into dedicated candidate pairs. Do not circulate the old '50 unauthored across PH09–PH12' tally as present-day coverage.

## Pinned, row-level scope and current native evidence

Authoritative structural input: `review/physics/ph01-ph12-full-coverage-r00/PHYSICS_PH01_PH12_EVIDENCE_R00.v1.json`. R00 is an author-exposed **technical** inventory, not independent R01/R02 acceptance. The exact 58-row filtered delta is recorded in [PH09_PH12_COVERAGE_DELTA_R1.json](PH09_PH12_COVERAGE_DELTA_R1.json).

| Chapter | Planned subtopics | Dedicated Core1A/B candidate pairs | Embedded lead-only candidates | No dedicated pair | Independently qualified |
|---|---:|---:|---:|---:|---:|
| PH09 — Reflection and Mirrors | 12 | 12 | 0 | 0 | 0 |
| PH10 — Refraction, Lenses and Human Eye | 17 | 17 | 0 | 0 | 0 |
| PH11 — Current Electricity | 14 | 0 | 2 | 14 | 0 |
| PH12 — Magnetic Effects and Induction | 15 | 0 | 2 | 15 | 0 |
| **Total** | **58** | **29** | **4** | **29** | **0** |

**Not equivalent measurements:** 29 dedicated candidate pairs + four embedded lead-only constructions do not equal 33 qualified native units. `No dedicated pair` does not mean there is no chapter explanation, worksheet, or older agent material. PH11 and PH12 each have a continuous chapter draft and 12 candidate Core1B cycles in their topic package; these are not per-subtopic native routes.

## Four bounded scientific/teaching reference candidates

The newly authored, **non-examination** cases in [FOUR_WPE_PARITY_REFERENCE_CANDIDATES_R1.json](FOUR_WPE_PARITY_REFERENCE_CANDIDATES_R1.json) are review workpaper exemplars, **not student-facing approved tests, Golden Samples, independent QRT scores, or authentic paper questions**.

| Chapter and subtopic | Core1A decisive model | Fresh Core1B work owned by learner | Boundary falsifier |
|---|---|---|---|
| PH09-04 · plane-mirror relative motion | `x_i=2m−x_o` under one lab axis | Move *both* object and mirror; separate image motion from object–image distance | Equal rigid translation of mirror/object |
| PH10-09 · two real lens positions | `p+q=D`, `pq=fD`; require `D>4f` for distinct positions | Infer focal length from two measured positions; challenge a claimed second position at `D=4f` | `D<4f` admits no real between-object-and-screen solution |
| PH11-07 · branch topology | Common node pair means same voltage; Kirchhoff charge continuity | Recognize parallel branches *behind a series resistor*; compute actual 6 V branch voltage instead of uncritically applying 12 V | Remove upstream resistor to recover direct parallel |
| PH12-09 · induction | Changing linked flux, not merely presence of B, is decisive | Rotate a loop in **constant** field; distinguish emf from closed-loop current | Spin about fixed area normal: unchanged linkage in ideal uniform field |

Science conditions, complete worked steps, proposed first-prediction/attempt text, post-attempt reconstruction, evidence-dependent diagnosis, repair and a novel boundary test are in each JSON case. These are candidate designs requiring **independent** review of scientific sufficiency, novelty, age suitability and the shortest valid solution. This R1 does not assign a D3/D4 band.

## Isolated learner-feel preview (new, author-only)

[Open the four-case preview](preview.html) on a running HTTP server. It uses the new [preview runtime](preview.js) and responsive [preview stylesheet](preview.css) to display worked Core1A and a separate Core1B task, commit the first prediction and reasoning locally, then deliberately reveal reconstruction, diagnosis, repair and boundary. A separate revision is recorded without overwriting the original. A storage-denial or corrupt record locks commitment and reconstruction.

**Limit:** the reconstruction text is in a public same-origin JSON file, and `localStorage` is user-editable. This is a browser-UX rehearsal, **not cryptographically secured assessment custody**. There is no link from the student-facing canonical navigation and no release authorization.

The dedicated Playwright test `python tools/physics_ph09_ph12_wpe_parity_browser_qa.py` checks four viewport dimensions, 4×4 chapter/view combinations, first-attempt gating and persistence, separate revision, chapter changes, no iframe, overflow, disabled storage and corrupt storage. **Browser execution is NOT_RUN until an actual receipt is produced**.

## Source and authoring risk register

- **PH09/PH10** — the source-related optics mappings are `RELATED_CANDIDATE_ONLY`, not verified original exam joins. The separate Physics candidate corpus has recorded false 2024 optics locators and missing figure requirements. Verify exact question, answer key, original figure, paper code and rights before B1/B7 or Core2 approval.
- **PH11** — 56 circuit worksheet questions (36 L1 + 20 L2) and the separate ten source-claimed candidates are different inventories. None automatically becomes an admitted NSEJS question. Diagram topologies, graph labels, keys and source rights require independent inspection. Upstream source voltage and branch node voltage must not be conflated.
- **PH12** — source-claimed magnetism candidates remain on exact-source HOLD, including figure custody. Teaching must explicitly distinguish magnetic field, changing linkage, induced emf, circulating current, viewing side and the curricular boundary between FORMATIVE and EXTENSION.
- **All four** — no verified exact Core2→Core1A→Core1B→protected transfer→source return sequence has been independently signed off. All seven B1–B7 gates remain HOLD. Physics R2 quality gate remains a pilot awaiting Owner Golden Sample authority.

Sources already in repository:
`nsejs/data/physics-core2-source-evidence.v1.json`,
`nsejs/physics/curriculum/agent2/CORE2_SOURCE_RECONCILIATION.md`,
`nsejs/physics/curriculum/topics/PH11/CIRCUITS_SOURCE_COVERAGE_AUDIT_R1.md`.

## Execution order — do not parallelize away the qualification gates

1. **PH09–PH10, audit existing 29 pairs:** inspect each Core1A for actual explanatory depth, equation domains, matched authentic source where possible, misleading example repetition and science claims. Inspect Core1B MAIN/INSTANCE for a genuinely new independent operation, not only changed numbers. Repair instead of cloning new pages. Proposed QRT D3/D4 labels remain author proposals.
2. **PH11, create native pairs after full lesson review:** start with PH11-02/03/04/06/07/09/10/11, then remaining syllabus and extension nodes. Promote the existing PH11-07/10 embedded leads only after reviewing what the new page actually teaches and requires the learner to decide. Do not treat the 56 worksheet candidates as original NSEJS paper questions.
3. **PH12, create native pairs after scientific source review:** start with PH12-02 through PH12-07 and PH12-09/10; keep motor/generator FORMATIVE and quantitative Faraday/terminal-velocity constructions EXTENSION unless separately authorized. Reuse reviewed chapter narrative, not duplicated generic tasks.
4. **Bind source and QRT:** independently obtain and check per-question original source, exact variant/figure/key, SL1/SL2 shortest route, owner-selected Blueprint, operation and demand, legal/custodial status; require explicit exact links rather than a shared topic label.
5. **Review a full vertical chain per chapter:** independently sign B1–B7, scientific warrant, lesson sufficiency, freshness, misconception diagnosis and the source-return route for one complete candidate unit. Only then apply the demonstrated method to the remaining subtopics.
6. **Engineering:** exact-head tests plus real HTTP Chromium at 1280×800, 1024×768, 900×1280, 800×1280, 1365×768 and 390×844. Verify direct native route/no iframe, keyboard/touch, math/figures, first answer persisted before help or reconstruction, revision separation, refresh, version mismatch, disabled storage, and source return.
7. **Release:** independent academic/QRT and Owner release authorization. Technical tests alone do not turn candidate work into approved teaching or authentic NSEJS examination materials. No autonomous merge or deploy.

## R1 acceptance and falsifiers

Technical evidence is valid only for the exact content revision. The regression `tests/test_nsejs_physics_ph09_ph12_wpe_parity_r1.py` guards the 58 IDs, native/embedded distinction, ZERO admitted count, presence of four distinct authored cases and representative physical arithmetic.

This R1 **does not** claim Python CI/Chromium PASS until those suites have actually executed on the exact PR head. **FAIL/HOLD** if any row is dropped, a candidate is promoted by a passing test alone, a source locator is fabricated, a draft D-band is presented as independent QRT, protected post-attempt work leaks before recorded submission, or an extension topic silently becomes syllabus core.

**Review handoff:** request a cold science/QRT review of one chosen subtopic per chapter using original-source-only entry where required; then a separate teaching/UX review. Author-visible exemplars above must not be used as purported blind science evidence.

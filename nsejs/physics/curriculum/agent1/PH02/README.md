# A02 / PH02 Forces — eight authored native-route candidates (R1)

**Task**: `G9V41-PHYS-C1AB-A02-PH02-R1`  
**Issue**: [#33](https://github.com/reallakshman19/Grade9v4.1/issues/33)  
**Parent**: Draft PR #3 branch `feat/nsejs-physics-agent1-ph01-kinematics-r1`, starting commit `6dd8c0000e710fc923e9d347123f78c17449ed7b`  
**Mode**: `AUTHOR_EXPOSED_CANDIDATE · EDUCATIONAL_SOURCE_FIRST · FAIL_CLOSED`  
**Academic**: `HOLD` · **Original exam items authenticated**: 0 · **Independent QRT**: 0 · **Merge/deploy**: prohibited without independent review and Owner approval.

This workpack is a *draft authoring slice*, not a completed C01–C08 native topic package or a production-ready lesson. No change to Shared, the Physics Blueprint, C01–C08 contracts, PH01 content, root nav, main, or the 132-row R00 independent-qualification matrix is included.

## Source custody and scope

- **Official IAPT NSEJS 2026 announcement**: [IAPT](https://iapt.org.in/) describes NSEJS scope as Physics/Chemistry/Biology up to CBSE Class X. This does not authenticate any past-paper question.
- **2026–27 CBSE Class IX Science (086)**: [official curriculum PDF](https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceSt_SecP1_2026-27.pdf), **printed page 15, PDF zero-based index 14**, section *Force and Laws of Motion*, competencies **C-2.1 and C-8.1**. The official table visibly specifies balanced/unbalanced forces, friction, Newton's first/second/third laws, force direction, SI unit and modelling. The chapter carries 13 periods.
- **Boundary**: PH02-F05 is a teaching construction under model/representation outcomes, not a separately named 2026–27 CBSE heading; F07 (inclined-plane components) and F08 (two-body changing contact) are **advanced authored extensions** without a claim of named Force-chapter coverage. Reconcile cross-topic placement and NSEJS inclusion independently.
- **Authentic Core2 source custody**: no original paper/printed source item, figure, option order or final key verified, admitted or copied. All Core1B tasks in this branch are *authored transfer*, not past NSEJS items. Source-to-question matching remains HOLD.

## Candidate route tally

| Subtopic | Core1A HTML | Core1B HTML | Native C01–C08 package | Academic |
| --- | --- | --- | --- | --- |
| F01 Balanced/unbalanced | `nsejs/physics/textbook/PH02/F01/index.html` | `nsejs/physics/core1/PH02/F01/index.html` | NOT_BUILT | HOLD |
| F02 First law/inertia | `nsejs/physics/textbook/PH02/F02/index.html` | `nsejs/physics/core1/PH02/F02/index.html` | NOT_BUILT | HOLD |
| F03 Second law/mass | `nsejs/physics/textbook/PH02/F03/index.html` | `nsejs/physics/core1/PH02/F03/index.html` | NOT_BUILT | HOLD |
| F04 Third law/interactions | `nsejs/physics/textbook/PH02/F04/index.html` | `nsejs/physics/core1/PH02/F04/index.html` | NOT_BUILT | HOLD |
| F05 Free-body diagrams | `nsejs/physics/textbook/PH02/F05/index.html` | `nsejs/physics/core1/PH02/F05/index.html` | NOT_BUILT | HOLD |
| F06 Friction/contact | `nsejs/physics/textbook/PH02/F06/index.html` | `nsejs/physics/core1/PH02/F06/index.html` | NOT_BUILT | HOLD |
| F07 Inclined planes | `nsejs/physics/textbook/PH02/F07/index.html` | `nsejs/physics/core1/PH02/F07/index.html` | NOT_BUILT | HOLD |
| F08 Connected bodies | `nsejs/physics/textbook/PH02/F08/index.html` | `nsejs/physics/core1/PH02/F08/index.html` | NOT_BUILT | HOLD |

**16 physical HTML URLs (8 original authoring pairs), 8 authored transfer prompts, 8 distinct content-revision identifiers.** They load a shared candidate-only content ledger. This is **not** equivalent to eight verified C01–C08 native package pairs, QRT D3/D4 cycles, Main integrations, or independent B1–B7 approval.

## Implementation structure and learner protection

`nsejs/physics/ph02/units.v1.json` owns original teaching cases, Figure captions, the nine A1–A9 teaching witnesses and one differentiated transfer/diagnosis/boundary task per subtopic. `lesson.js` renders the Core1A page; `practice.js` implements the six-stage learner journey (predict → attempt → reconstruct → diagnose → repair → boundary), with revision-bound immutable first response, sequential H1–H3 after persistence, separate diagnosis/repair, and closed answer gates when storage fails. It retains earlier revision keys and does not award mastery. Browser source inspection remains possible: this is an educational exposure contract, **not** secure examination invigilation.

The figures are original schematic SVG. A diagram/data/geometry audit remains compulsory, especially the incline figure (schematic, not drawn to numerical scale). No exam figure is copied or reconstructed.

## Engineering checks

Added `tests/test_ph02_candidate_routes.py` (data integrity, physical routes, script guards, title/attempt coverage) and `tools/physics_ph02_browser_qa.py` (HTTP Chromium, 1000×1600 and 1600×1000; full journey for eight cases, refresh and storage denial).

**Execution status at author handoff:** Exact Python suite: **NOT_RUN**. New pytest: **NOT_RUN**. HTTP Chromium: **NOT_RUN**. CI: **NOT_YET_RECONCILED**. Source-file JavaScript parse check was performed by stripping module-only tokens and compiling via a V8 parser: lesson.js and practice.js syntax **PARSE_PASS**, which is not a browser test.

Required commands from a checked-out exact head:

```sh
git rev-parse HEAD
python -m pytest -q tests/test_ph02_candidate_routes.py
python -m pytest -q
python tools/physics_ph02_browser_qa.py
```

Do not claim these tests passed without actual output and SHA-bound receipts.

## Gate-by-gate disposition

| Gate | Current | Next witness |
|---|---|---|
| G0 checkout/collision | CANDIDATE isolated | Rebase/check exact-head PR3, ownership and branch collision |
| G1 source/curriculum | PARTIAL / HOLD | Review official IX/X detailed scope, authenticate individual Core2 originals and rights |
| G2 Core1A | AUTHOR DRAFT | Full scientific, sufficiency, figure and independent checks under R2 |
| G3 QRT/binder | HOLD | Resolve shortest W, operation, five factors, source role and native package; no forced D3/D4 |
| G4 Core1B | AUTHOR DRAFT | Independent freshness audit, leakage and six-stage browser receipts |
| G5 technical | NOT_RUN | Native validator + unchanged pytest + HTTP Chromium + faults |
| G6 academic/release | HOLD | R00 review, genuinely independent R01 Physics/QRT B1–B7 and Owner release |

**R2**: `PILOT_AWAITING_OWNER_GOLDEN` (not active). An R2 `*.packet.json` **has not been produced or validated**: exact SHA-256/line quotes, negative logs, real browser receipts and independent reviewer-owned forms are prerequisites. Do not create fake PASSED evidence or edit `quality-policy.v1.json` to make a candidate eligible.

## Next technical correction batch

1. Independently check every worked derivation, unit/sign/limit and every figure for physical fidelity; confirm F05–F08 prerequisite readiness and cross-topic scope.
2. Run and fix new tests, unchanged full pytest, two-orientation Chromium, blocked storage, stale revisions, keyboard, accessible diagrams and source return.
3. Build a valid C01–C08 v1.1 native topic package, topic adapter, warrant ledger, INSTANCE and genuinely integrated MAIN obligations **only for defensible cells**, preserving candidate status and dependencies.
4. Create per-task R2 evidence packets with actual repository byte SHA-256, source line excerpts and observed failure-injection logs; seek independent R00/R01 receipts.
5. Update the Issue #33 matrix **only after new pinned implementation and corresponding evidence exists**; do not count these draft pages as independently qualified.

**No academic approval inferred from software validation.**

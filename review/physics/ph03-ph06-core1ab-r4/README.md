# PH03 + PH06 Core1A/Core1B R4 — Candidate Technical and Teaching Evidence

**Disposition: AUTHOR-EXPOSED CANDIDATE · SCIENCE/QRT/B1–B7 HOLD · NOT RELEASED**

**Reference:** `architecture/core1ab-agent-guide.html` §§7, 13–18, 20–23, and
`docs/agent-entry/quality-gate-r2/`. Base main at initial work:
`b180c5fc44c7c3b77e9a19584351688fcdf979f7`.
Working draft: [PR #89](https://github.com/reallakshman19/Grade9v4.1/pull/89).

This dossier is a **producible author-side evidence brief**, not a blinded
R01 report. Authors have seen the correct models and prior guide. A separate
source-only review must seal its original solution and rubric BEFORE comparing
with this packet; do not present it to a blind reviewer first.

## A. Exact preserved attempt revision

Five earlier question JSON and postattempt JSON files remain byte-identical to
main: `P01/P04/P05/P06/P07.json` and `post-Pxx.json`. Their revision is
`ph03-complete-r3-20261116`. New question, model and figure bytes are
`Pxx.r4.json`, `post-Pxx.r4.json`,
`figures/Pxx-prompt-r4.svg`, `figures/Pxx-solution-r4.svg`,
with revision `ph03-core1ab-r4-20261117`.
The default Learn/Try links present R4; a link to `?revision=r3` reopens the
actual historical content and its separately keyed local first response.
P02 remains on the same R3 task; P03 Golden R2 retains its own runtime.
Do not migrate or count historical responses as new R4 first attempts.

`tests/test_ph03_core1ab_r4.py` verifies original Git blob SHAs,
new post-model/solution pins and exact arithmetic. `tools/ph03_full_r3_browser.py`
checks real first responses, positive cases, Skips, negative controls,
post-first-only answer asset fetch, dual tabs and two tablet orientations.

## B. Source-first Core1A/1B comparison — authored and falsifiable

| Unit | Core1A teaching bridge (B3 candidate) | New learner-owned decisive W (B4 candidate) | Concrete falsifier |
|---|---|---|---|
| P01 | Derive p²=2mK and combine separately measured signed momentum and energy, including incompatible measurement limits | Infer BOTH unobserved B mass and signed speed from totals, not substitute known m/v | A single forward p=mv calculation or copied two-cart template solves both unknowns |
| P04 | Differentiate pair net external impulse from individual internal+external impulses; one measured velocity closes the inverse ledger | Recover the other final velocity and the otherwise hidden external impulse distribution | Final velocities follow from the internal contact impulses alone |
| P05 | Derive v_load,lab=V_platform,lab+u_relative with moving initial pair and CM check | Combine moving initial momentum with relative final ejection speed in one equation | Using relative +5 directly as laboratory load velocity still yields the right answer |
| P06 | Infer restitution after reconstructing unknown outgoing speed; compare passive bounds and independent energy loss | Select the actual contact regime FROM a measured outgoing speed and assess feasibility | An e value or specified elastic/sticking model is already given in the protected prompt |
| P07 | Derive friction stopping distance and μ threshold for reaching an obstacle | Test if the second impact EXISTS, then and only then solve the second contact | The second contact can be solved without the distance/threshold test |

The additional Core1A bridges occur in Section 5 of each R4 lesson. They do not
prove that a student can reconstruct independently; B3 teaching sufficiency
still needs unexposed learner and reviewer evidence. The new post models are
stored separately and not requested before the first saved Try response.

### Independent arithmetic check — proposed solutions (not blind reviewer output)

- **P01:** A p=+6 kg·m/s and K=9 J. Hidden B p=−6, K=6;
  m_B=p²/(2K)=3 kg, v_B=−2 m/s. With total K=9 J instead, B must have
  p=−6 and K=0; no finite positive mass satisfies both.
- **P04:** Total p=+4; A p=−4, so B p=+8 and v_B=8/3 m/s.
  Outside impulse on A = −4 − (−6) = +2 N·s;
  outside impulse on B = +8 − (+6) = +2 N·s.
  Without the A measurement, the individual velocities are not unique.
- **P05:** Initial p=(8+2)×(+1)=+10. Let platform final lab v=V;
  load lab v=V+5. 8V+2(V+5)=10 gives V=0 and load lab v=+5.
  CM remains +1 m/s. Changing load measurement to +4 LAB gives V=+0.25
  and relative ejection speed +3.75 m/s.
- **P06:** Initial p=3×4=12. Measured A final +2 gives B final +3 m/s;
  e=(3−2)/(4−0)=0.25; K_initial=24 J, K_final=15 J,
  converted=9 J. Changed measured A final −1 implies B=+7.5,
  e=2.125: not admissible as a passive impact.
- **P07:** Initial sticking speed=(1×6)/3=+2 m/s.
  For L=0.75 m and g=10, μ_crit=4/(2×10×0.75)=4/15.
  At μ=0.20, the obstacle is reached at +1 m/s, followed by a sticking
  final +0.75 m/s. At μ=0.30, stopping distance=2/3 m, short of 0.75 m,
  so no second collision.

These are independent arithmetic recomputations by the author, not QRT
adjudications of model selection, operation, shortest alternative or D-band.
The postcommit figures and H1–H3 hints are authored, not authenticated
original examination diagrams.

## C. PH06 U08 — stage, storage and answer-gating controls

- The original PH06 R2 `reader.js` was copied byte-for-byte to
  `reader-r2-legacy.js`, with `legacy-u08.html` for earlier local attempts.
- The R3 reader uses a *different* content/manifest-bound storage key.
  It loads only task, source, givens-only SVG and SHA-1 asset pins
  pre-attempt. `model.v1.json`, reconstruction SVG and boundary SVG are
  fetched **after** a durable first response; actual bytes are verified
  against `protected-assets.r3.json` before display.
- Native Skip/Undo exists for Predict, each structured answer, first written
  Attempt, Diagnose, Repair, boundary reasoning and boundary fields. Skipped
  fields persist as `null`, show explicit no-credit, never infer a
  misconception from missing work and cannot unlock a source-reattempt
  completion claim.
- Storage-denied, missing prompt SVG, stale-revision and modified postasset
  scenarios must remain fail-closed. A missing model after first save may
  prevent comparison, but must never erase the original answer.
- Browser local storage is an educational state guard, not secure
  invigilation or a reliable proof of independent student mastery.

## D. Mechanical and academic gates

Relevant exact-head CI:
`physics-ph03-ph06-header-r1.yml`,
`ph06-golden-r1.yml`,
`nsejs-search-r1.yml`,
Python QA and the existing protected-state/navigation workflows.

After code changes, run the **entire** triggered suite on the PR exact head.
Keep separate outcomes: test added, executed, PASS, FAIL and NOT_RUN.
A green author evidence validator only supports structural inspection.
R2 policy is still `PILOT_AWAITING_OWNER_GOLDEN`, not a required branch gate.

### Reviewer R00 technical scope

Verify Git object pins and old `?revision=r3` restoration, two-tab write
races, answer fetch timing via real HTTP network logs, fail-closed asset
tampering and storage denial, all six skip stages, no mastery/credit after skip,
portrait+landscape touch and keyboard, source return chronology and search
index freshness. Independently check five numeric solutions and four
high-risk model boundaries.

### Reviewer R01 scientific/QRT scope

Use only source-only inputs on the FIRST pass, not this author-exposed file;
record the actual first seal, exact versions, shortest legitimate route,
competing operations, five demand factors, scientific laws/conditions,
B1–B7 falsifiers and task-source role. Reconcile each proposed B3 teaching
bridge and B4 novelty against the actual worked anchors. Escalate a
numeric-clone or missing condition rather than marking it accepted.

**Current answer:** candidate implementation available; independently
attributed academic acceptance, source authenticity and release authority
are **HOLD**. Do not merge/deploy solely because technical CI passes.

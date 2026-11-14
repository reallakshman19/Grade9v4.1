# B01 — Independent R01 cold intake: PH07/PH08 Physics

**Authority:** `AUTHOR_EXPOSED_PREPARATION_ONLY · R01_NOT_ASSIGNED · ALL_ACADEMIC_HOLD`.

This prepares [R01 Issue #24](https://github.com/reallakshman19/Grade9v4.1/issues/24). It is **not** an academic review or approval. The preparing engineer is author-exposed and cannot self-certify cold independence.

## Strict order for an independently appointed R01

1. **Stage A, unseen:** Open [89 anonymous author-prompt-only problems](B01_R01_STAGE_A_PROMPTS.v1.json). Do not open the Stage B crosswalk or original source packages. The Stage A file excludes claimed operation, D-band, factor score, solution, protected W, package and source IDs.
2. **Independent physics first:** For each anonymous ID derive the law, assumptions, units, signs, second check, limit/counterexample, competing model, primary QRT operation and five-factor demand. Freeze a reviewer-owned signed Stage A return **before viewing any author key**.
3. **Figure HOLD:** The 11 lexically flagged prompts mention a visual term, but that is not the full number needing a figure. If a diagram is required and no prompt-only representation is available, report `MISSING_FIGURE__CANNOT_BLIND_SOLVE`; do not peek at a solved textbook graphic.
4. **After Stage A freeze only:** Open [Stage B source/QRT crosswalk](B01_R01_STAGE_B_CROSSWALK.v1.json). Compare reviewer reasoning against actual pinned package, author solution, Core1A teaching, Core1B six stages, evidence, source identity and figures.
5. **All 89 independently:** Record B1–B7 separately; reject numeric clones, inappropriate D4, wrong physics, nondecisive vs decisive hint leaks, incomplete source or source-key disagreements. Browser CI is evidence for behavior only, not Physics or true learning.
6. **All 16 mixed MAINs separately:** Review compatibility as genuinely integrated two-subtopic inferences. Zero canonical MAINs may be selected from author proposals or metadata alone.
7. **Resolve named source conflicts:** 2018 JS511 Q9 and 2017 JS534 Q1 rejected identities; 2016 JS530 Q36 key; 2020–21 IOQJS figures; 2024 code 51 Q59 key interpretation; PH08-09 lacking an observed publisher locator. No invented source admission.
8. **Return a reviewer-owned ledger:** One row per anonymous ID with frozen Stage A SHA, independently derived Physics, actual QRT classification, error evidence, B1–B7, P0/P1/P2, per-MAIN decision and exact package/figure SHA. Missing evidence remains HOLD.

## Reproducibility and authority

Origin author PR #11 exact head: `0f045746c8269b741e77ba7da8a6fb4569dd07f2`. The crosswalk retains 39 byte-pinned author files covering **75 primary + 14 supplemental = 89 INSTANCE proposals**, **16 unselected MAIN proposals**, and **0 authenticated exam admissions**. Two source identity conflicts remain rejected without deleting history.

The independent reviewer remains **NOT_ASSIGNED**. The R00/P00 engineers are author-exposed. Golden Sample acceptance, if pursued, requires a genuinely separate reviewer and the Owner's **one-time standard acceptance**, not individual Owner signatures for each question.

Regenerate and confirm against actual B01 source files:

```bash
python tools/physics_b01_r01_cold_intake.py
python -m pytest -q tests/test_nsejs_b01_r01_cold_intake.py
```

A deterministic PASS proves source/UID/byte integrity, **not** scientific correctness or independent academic admission.

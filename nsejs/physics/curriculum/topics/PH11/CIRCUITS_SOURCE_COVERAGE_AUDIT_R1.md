# Circuits worksheet source-coverage audit · R1

**Scope:** Owner-supplied 13-page `circuit.pdf`; SHA-256 `1d7f16219d4353bf74e6dd29ebd9c3e9b770ad3d2b402d46aed81165bb4e3c4e`. **Authority:** author-exposed technical intake, `SOURCE_HOLD / RIGHTS_HOLD / SCIENCE_HOLD / QRT_HOLD / ACADEMIC_HOLD`. No IAPT exam authenticity claimed.

## Coverage reconciliation

| Metric | Source | PR #38 initial | This stacked repair |
|---|---:|---:|---:|
| Level-1 questions | 36 | 0 | 36 |
| Level-2 questions | 20 | 20 | 20 |
| Distinct Level-1 figures | 11 | 0 | 11 neutral vector redraws |
| Distinct Level-2 figures | 17 | 17 | 17, including one reused for Q08–Q09 |
| Questions with 3 provisional hints | 56 | 20 | 56 |
| Source-/academic-qualified | not established | 0 | 0 |

Source-derived answer letters match worksheet page 13; the correctness of the worksheet itself and the conceptual QRT bands remain independently unreviewed. Figures are reconstructed neutral schematics, not original SVGs from the PDF, and require human source-figure comparison.

## Critical repair to inherited PR #38

- 14 Level-2 diagram files contained worked answers or decisive formula reductions inside prompt-facing graphics. These annotations have been removed in both served asset locations; the shared Q08/Q09 graphic is one asset.
- Q11's nine-node lattice receives an explicit KCL voltage witness.
- Q14's incorrect `I/3` incident-edge split is replaced by correct cube-node equations and current fractions.
- Q15's incorrect claim of four potential levels is replaced by the actual five-level symmetry solution.
- Candidate feedback no longer says a worksheet table is an **official verified** examination key.
- PH05 authored-preview navigation is restored and linked to its seven learner pairs; these pages remain academically HOLD.

## Remaining acceptance gaps

The source PDF has not been committed to public Git because rights/custody are HOLD. An authorized independent reviewer still needs to compare all redrawn figures visually/topologically to original worksheet images, independently recompute every answer and approve qualifying QRT classifications. A separate exact source→warrant→Core1A/Core1B map is not established: this PR records topic-related previews, not exact academic joins. Test the full question reader under real HTTP Chromium for first attempt, hint exposure, refresh and storage failures before promoting.

## Per-question custody matrix

| Worksheet ID | PDF page | Diagram asset | Recorded worksheet key | Helper candidate | Status |
|---|---:|---|---|---|---|
| L1-01 | 1 | No figure | B | 3 provisional hints | HOLD |
| L1-02 | 1 | No figure | A | 3 provisional hints | HOLD |
| L1-03 | 1 | fig_nsejs_circ_l1_q03.svg | A | 3 provisional hints | HOLD |
| L1-04 | 1 | No figure | A, B, C | 3 provisional hints | HOLD |
| L1-05 | 1 | No figure | B | 3 provisional hints | HOLD |
| L1-06 | 1 | No figure | C | 3 provisional hints | HOLD |
| L1-07 | 2 | No figure | C | 3 provisional hints | HOLD |
| L1-08 | 2 | No figure | C | 3 provisional hints | HOLD |
| L1-09 | 2 | No figure | A | 3 provisional hints | HOLD |
| L1-10 | 2 | fig_nsejs_circ_l1_q10.svg | D | 3 provisional hints | HOLD |
| L1-11 | 2 | fig_nsejs_circ_l1_q11.svg | A, B | 3 provisional hints | HOLD |
| L1-12 | 2 | No figure | B, C, D | 3 provisional hints | HOLD |
| L1-13 | 3 | fig_nsejs_circ_l1_q13.svg | C | 3 provisional hints | HOLD |
| L1-14 | 3 | No figure | C | 3 provisional hints | HOLD |
| L1-15 | 3 | No figure | D | 3 provisional hints | HOLD |
| L1-16 | 3 | fig_nsejs_circ_l1_q16.svg | B | 3 provisional hints | HOLD |
| L1-17 | 3 | No figure | B | 3 provisional hints | HOLD |
| L1-18 | 4 | fig_nsejs_circ_l1_q18.svg | B | 3 provisional hints | HOLD |
| L1-19 | 4 | fig_nsejs_circ_l1_q19.svg | D | 3 provisional hints | HOLD |
| L1-20 | 4 | No figure | A | 3 provisional hints | HOLD |
| L1-21 | 4 | fig_nsejs_circ_l1_q21.svg | C | 3 provisional hints | HOLD |
| L1-22 | 5 | fig_nsejs_circ_l1_q22.svg | A, C | 3 provisional hints | HOLD |
| L1-23 | 5 | No figure | B | 3 provisional hints | HOLD |
| L1-24 | 5 | No figure | D | 3 provisional hints | HOLD |
| L1-25 | 5 | No figure | A | 3 provisional hints | HOLD |
| L1-26 | 5 | No figure | A | 3 provisional hints | HOLD |
| L1-27 | 5 | No figure | B | 3 provisional hints | HOLD |
| L1-28 | 5 | No figure | D | 3 provisional hints | HOLD |
| L1-29 | 5 | No figure | D | 3 provisional hints | HOLD |
| L1-30 | 5 | No figure | C | 3 provisional hints | HOLD |
| L1-31 | 6 | No figure | D | 3 provisional hints | HOLD |
| L1-32 | 6 | No figure | A, C, D | 3 provisional hints | HOLD |
| L1-33 | 6 | fig_nsejs_circ_l1_q33.svg | A | 3 provisional hints | HOLD |
| L1-34 | 6 | No figure | C | 3 provisional hints | HOLD |
| L1-35 | 6 | fig_nsejs_circ_l1_q35.svg | B | 3 provisional hints | HOLD |
| L1-36 | 6 | No figure | C | 3 provisional hints | HOLD |
| L2-01 | 7 | fig_nsejs_circ_l2_q01.svg | A | 3 provisional hints | HOLD |
| L2-02 | 7 | fig_nsejs_circ_l2_q02.svg | B | 3 provisional hints | HOLD |
| L2-03 | 7 | fig_nsejs_circ_l2_q03.svg | C | 3 provisional hints | HOLD |
| L2-04 | 7 | fig_nsejs_circ_l2_q04.svg | B | 3 provisional hints | HOLD |
| L2-05 | 8 | fig_nsejs_circ_l2_q05.svg | C | 3 provisional hints | HOLD |
| L2-06 | 8 | fig_nsejs_circ_l2_q06.svg | B | 3 provisional hints | HOLD |
| L2-07 | 8 | fig_nsejs_circ_l2_q07.svg | C | 3 provisional hints | HOLD |
| L2-08 | 9 | fig_nsejs_circ_l2_q08.svg | B | 3 provisional hints | HOLD |
| L2-09 | 9 | fig_nsejs_circ_l2_q08.svg | C | 3 provisional hints | HOLD |
| L2-10 | 9 | fig_nsejs_circ_l2_q10.svg | D | 3 provisional hints | HOLD |
| L2-11 | 10 | fig_nsejs_circ_l2_q11.svg | C | 3 provisional hints | HOLD |
| L2-12 | 10 | fig_nsejs_circ_l2_q12.svg | D | 3 provisional hints | HOLD |
| L2-13 | 10 | fig_nsejs_circ_l2_q13.svg | A | 3 provisional hints | HOLD |
| L2-14 | 11 | fig_nsejs_circ_l2_q14.svg | D | 3 provisional hints | HOLD |
| L2-15 | 11 | fig_nsejs_circ_l2_q15.svg | B | 3 provisional hints | HOLD |
| L2-16 | 11 | fig_nsejs_circ_l2_q16.svg | A | 3 provisional hints | HOLD |
| L2-17 | 12 | fig_nsejs_circ_l2_q17.svg | A | 3 provisional hints | HOLD |
| L2-18 | 12 | fig_nsejs_circ_l2_q18.svg | D | 3 provisional hints | HOLD |
| L2-19 | 12 | No figure | A | 3 provisional hints | HOLD |
| L2-20 | 12 | No figure | C, D | 3 provisional hints | HOLD |

**Release instruction:** Keep this PR in DRAFT, stacked on PR #38, and do not merge/deploy until all applicable gates are independently closed.

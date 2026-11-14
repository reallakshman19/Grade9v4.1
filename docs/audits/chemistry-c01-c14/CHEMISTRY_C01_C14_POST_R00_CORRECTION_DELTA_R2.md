# Chemistry C01–C14 — R00 correction delta R2 (14 November 2026)

**Disposition:** THREE NAMED SOURCE OMISSIONS REPAIRED IN AUTHOR CANDIDATE · R01/R02 HOLD · NO ACADEMIC PROMOTION · NO MERGE/DEPLOY.

The frozen [R00 audit PR #27](https://github.com/reallakshman19/Grade9v4.1/pull/27) at `b717ef858a4082a8dd4861f61271a89ff97a64f6` correctly recorded **3 FAIL and 81 HOLD** against its earlier frozen source branches. Since then, PRs [#30](https://github.com/reallakshman19/Grade9v4.1/pull/30) and [#31](https://github.com/reallakshman19/Grade9v4.1/pull/31) were merged into the **B02 authoring branch**, not the production `main` branch. The current [Draft PR #13](https://github.com/reallakshman19/Grade9v4.1/pull/13) was inspected at `8afb6a0469bf5a1decfb03d30698fa491873ca9f`.

| R00 finding | Current B02 authoring evidence | Post-correction status |
|---|---|---|
| CHEM-FC-001 · C11.05 halogens missing | C11 Core1A explicit haloalkane / C–Cl / substituted-chloropropane teaching; retained REPRESENT task with changed-boundary reasoning | AUTHOR CANDIDATE REMEDIATED — R01/R02 HOLD |
| CHEM-FC-002 · C14.01 ozone depletion missing | C14 Core1A CFC, UV and stratospheric O₃, distinct ground-level model; MODEL transfer in Core1B | AUTHOR CANDIDATE REMEDIATED — R01/R02 HOLD |
| CHEM-FC-013 · C14.05 biodegradable distinction missing | C14 Core1A biological decomposition vs plastics/recycling; EXPLAIN transfer in Core1B | AUTHOR CANDIDATE REMEDIATED — R01/R02 HOLD |

The exact inspected Git blob SHAs, file paths, task evidence and checks are recorded in [the machine-readable correction delta](CHEMISTRY_C01_C14_POST_R00_CORRECTION_DELTA_R2.json). Existing author-branch test `tests/test_nsejs_chemistry_three_syllabus_gaps_r1.py` exercises these candidate changes. Current B02 head's Python, source-gap Chromium, and P00 native-reader Chromium workflow conclusions were SUCCESS when inspected. These verify bounded technical behavior, not independent scientific/QRT qualification.

## Custody and status rules

1. **Do not rewrite the original R00 evidence matrix or gap register.** They must remain reproducible against their frozen exact source SHAs. Historical `3 FAIL / 81 HOLD` is correct **for the original snapshot**.
2. On the **updated candidate head**, the three specifically named omissions now have author-proposed content. Report them as `AUTHOR_CANDIDATE_REMEDIATED`, **not** as independently qualified PASS.
3. The current academic denominator remains **0/84 subtopics independently qualified, 0/252 candidate tasks independently QRT qualified**; scientific, source, B1–B7, original exam and full integrated learner gates remain HOLD.
4. The audit still does **not** establish that the 84 editorial topics exhaust the 2026–27 IAPT/CBSE Chemistry syllabus. Earlier-grade foundations and 14 QRT-template-cell dispositions require independent adjudication.
5. P00 attempt-integrity and source return must be reassessed at a pinned integrated head; no learner publication or `main` integration approval is granted here.

## Required R01/R02 acceptance

Independently inspect each corrected exact science explanation and Core1B challenge against official scope and original authoritative textbooks; blindly judge decisive W, five-factor cognitive demand, initial-attempt protection, changed-condition transfer and B1–B7. Run single-tree A+B/P00 full route tests when approved. Publish a new, clearly versioned **current-state** matrix only after review, preserving the frozen historical matrix.

# NSEJS Chemistry C01–C14 — Full-Coverage Audit R1

**Task:** G9V41-NSEJS-CHEM-C01-C14-FULL-COVERAGE-R00-R1  
**Audit date:** 2026-11-14  
**Mode:** R00 author-exposed technical/source coverage audit; not cold scientific or blind QRT acceptance.  
**Disposition:** INTERNAL AUTHORING 84/84 PASS; EXTERNAL CURRICULUM 2 FAIL; ACADEMIC QUALIFICATION 0 PASS / 2 FAIL / 82 HOLD; CLAIM OF 100% CHEMISTRY COVERAGE REJECTED; NO MERGE/DEPLOY.

## Exact source custody

| Source | Pinned SHA | Branch state |
|---|---|---|
| Stage0 Chemistry 14-unit syllabus, PR #1 | 77d2bd63328c184598088bce6b9888fc8324cb4b | draft/unmerged |
| Agent A C01–C07, PR #6 | fb5cf6626088a1312743d60d0c39d06a4a3f8133 | draft, stacked on PR #1 |
| Agent B C08–C14, PR #4 | b8e4f6f99a9bb8000fb243ee6a2a2765fc5d2509 | draft, sibling to PR #6 |
| B02 C10–C11, PR #13 | 54d44413d10251962fbb7e52180023f3ad5f83b8 | draft, stacked on PR #4 |
| P00 B02 native reader, PR #17 | df3b77723e59974bab107ee8e11d12b625418579 | draft, stacked on PR #13 |
| Core2 bank/main at audit intake | 4f04677cb161d9eb32f6cd701411201ad0764421 | main snapshot |

**Important:** The 84 internally authored rows come from two unmerged author branches. There is no accepted integrated C01–C14 production build and no single exact-head combined 252-task Chromium run.

## Official scope and method

IAPT NSEJS 2026 and HBCSE Junior Science syllabus specify broadly up-to-CBSE-Class-X Science, not an official 14-unit Chemistry taxonomy. The audited primary documents are:

- IAPT: https://iapt.org.in/ ; HBCSE: https://olympiads.hbcse.tifr.res.in/syllabus/
- CBSE IX Science 2026–27: https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceSt_SecP1_2026-27.pdf (molecules/atomic structure, mixtures, learning outcomes, PDF viewer indexes 8–11).
- CBSE X Science 2026–27: https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/Science_SecP1_2026-27.pdf (reaction/periodic items PDF index 3; acids/metals/carbon index 4; environment index 5).

The auditor joined each Stage0 subtopic by exact CHEM-Cnn.nn ID to its author's textbook/reader entry and topic adapter, checked three distinct QRT primary operation IDs, nonblank X/Y/Z/W and authored six-stage work, plus worked explanation and misconception-repair fields. A scientific model, an authenticated source and a qualified D4 question are **not** certified merely by passing those field checks. PDF authority was checked separately for named source concepts, with complete current authored chapter text reviewed for targeted omissions.

## Summary of evidence

| Metric | Observed | Meaning |
|---|---:|---|
| Editorial units mapped | 14/14 | Internal taxonomy, not an IAPT chapter list |
| Internal subtopics joined to authored books + adapters | 84/84 | Inventory PASS |
| Subtopics with taught/worked/repair fields | 84/84 | Structured-authoring PASS; science depth unqualified |
| Candidate distinct QRT operations | 3 per subtopic | 252 author task records, not 252 independently D3/D4-qualified questions |
| Exact D3/D4 template identities used | 10/14 | Four absent cells requiring reviewed need or N/A |
| Original subtopic figures referenced | 35/84 rows | A visual count, not visual scientific adequacy |
| B02 C10/C11 staged S1–S3 visuals | 39 canonical tasks + 8 supplementary = 47 routes / 141 SVGs | Only C10/C11 bounded P00 technical scope |
| Other canonical task cycles without B02 staged visual binding | 213/252 | Visual need must be assessed, not automatically treated as 213 missing diagrams |
| Independently science-qualified rows | 0/84 evidenced | HOLD |
| Independently QRT-qualified tasks | 0/252 evidenced | HOLD |
| Overall qualified outcome | **0 PASS / 2 FAIL / 82 HOLD** | 100% external syllabus coverage not verified |

**Scope flags:** 65 CORE_CANDIDATE, 5 FOUNDATION_RECONCILE, 3 SCOPE_REVIEW, 6 EXTENSION, 5 ENRICHMENT. Core candidate does not mean independently admitted. The absent QRT D3/D4 identity cells are RETRIEVE-D3, RETRIEVE-D4, EXPLAIN-D4 and APPLY-D4. Do not invent filler for unsuitable templates.

## Per-unit results

| Unit | Internal rows PASS | Named syllabus content FAIL | Overall HOLD | Optional / scope-review rows | B02 staged canonical tasks |
|---|---:|---:|---:|---:|---:|
| C01 | 6/6 | 0 | 6 | 6 | 0 |
| C02 | 7/7 | 0 | 7 | 0 | 0 |
| C03 | 6/6 | 0 | 6 | 0 | 0 |
| C04 | 6/6 | 0 | 6 | 4 | 0 |
| C05 | 6/6 | 0 | 6 | 1 | 0 |
| C06 | 6/6 | 0 | 6 | 1 | 0 |
| C07 | 7/7 | 0 | 7 | 1 | 0 |
| C08 | 6/6 | 0 | 6 | 0 | 0 |
| C09 | 6/6 | 0 | 6 | 1 | 0 |
| C10 | 6/6 | 0 | 6 | 0 | 18 |
| C11 | 7/7 | **1 (C11.05)** | 6 | 0 | 21 |
| C12 | 5/5 | 0 | 5 | 2 | 0 |
| C13 | 5/5 | 0 | 5 | 3 | 0 |
| C14 | 5/5 | **1 (C14.01)** | 4 | 0 | 0 |
| **Total** | **84/84** | **2** | **82** | **19** | **39** |

## Two confirmed named source-content misses

**CHEM-FC-001 · FAIL · C11.05 halogen functional group.** CBSE Class X 2026–27 Carbon and its Compounds explicitly names **halogens** with alcohols, ketones and aldehydes among functional groups (Class X PDF viewer index 4). The current C11 Core1A manuscript and reader teach carbonyl, OH and ether groups, but contain no explicit halo functional group or haloalkane structural teaching. Mention of methane substitution elsewhere does not satisfy this content outcome. B02 should add a source-aligned haloalkane example, bond/connectivity misconception, a genuine transfer task and R01/R02 review.

**CHEM-FC-002 · FAIL · C14.01 stratospheric ozone depletion.** CBSE Class X Our Environment explicitly names **ozone depletion** (Class X PDF viewer index 5). C14 contrasts beneficial stratospheric and harmful ground-level ozone, but neither the full C14 textbook/reader nor its Core1B pack explains ozone depletion or ozone-depleting compounds such as CFCs and associated chemical causality. B03 should add a safe, accurate cause–consequence model and changed-condition learner task, with R01 review. C14.03 can cross-link the chemistry.

These are source-specific missing *taught concepts*, not absent subtopic IDs. They disprove an unconditional 100% Chemistry syllabus statement.

## Other qualification gaps

1. **Exact lower-school foundations:** Five C01 rows still cite EARLIER-FOUNDATIONS-PENDING, so VI–VIII source edition/page reconciliation and an external-to-internal negative-space scan are needed; the 84-item design cannot prove it contains every external prerequisite.
2. **Depth/scope:** Three SCOPE_REVIEW and eleven EXTENSION/ENRICHMENT rows require item-level official evidence. Periodic classification is formative-only for CBSE X year-end school assessment, but should not falsely be excluded from broader NSEJS eligibility. C11.07 esterification, C10.05 amphoterism, C12.01 formal gas laws and C13.02 oxidation numbers need explicit depth boundaries.
3. **QRT:** Actual protected W, hint leakage, misconception difficulty and transfer need blind exact-task review for all 252 cycles; author D4 labels are not independently justified. Four of fourteen D3/D4 operation cells are unused, with legitimate N/A possible.
4. **Runtime integration:** PR #6 A native preview and PR #4/13/17 B reader are separate schemas and unmerged histories. P00 verified 47 C10/C11 routes, not 252 unified learner journeys. On pinned PR #17, earlier R00 finding P00-AUD-04 on persisted attempt record validation remains an engineering HOLD until corrected.
5. **Core2 source custody:** On pinned main, the Chemistry bank has 119 source-claimed candidates (40 EXAM_CLAIM, 79 EXAM_PAPER), while another question map contains 87 Chemistry metadata rows. Both are source/academic HOLD, and zero original question texts have been admitted by this coverage audit. These counts are separate from 252 original author-created practice tasks.
6. **Environmental waste:** C14.05 teaches biodegradability/recycling/lifecycle tradeoffs but should map waste generation, segregation and prevention/treatment solutions directly to the named official environmental outcomes.

## Correction sequence and authority

**B02:** C11.05 functional groups; **B03:** C14.01 ozone depletion and waste mapping; **A01/source custodian:** exact lower-grade references and negative-space review; **A/B authors + R01:** reconcile scope and chemical text; **R02:** independently adjudicate 252 exact QRT demands and 24 additional B capstones; **P00:** resolve stored-record validation and construct/test non-destructive 14-unit integration, including a 252-task route matrix; **Owner:** approve any source admission, contract changes, merge or deployment.

## Native evidence outputs

- CHEMISTRY_C01_C14_EVIDENCE_MATRIX_R1.csv — **all 84 rows**, one per original Stage0 subtopic, with source SHA, links, flags and PASS/FAIL/HOLD.
- CHEMISTRY_C01_C14_EVIDENCE_MATRIX_R1.json — full row and unit machine-readable status and 10/14 QRT identity set.
- CHEMISTRY_MISSING_CONTENT_AND_GATES_R1.json — 14 findings (2 named source-content FAIL, 12 HOLD) with owners, exact evidence and acceptance conditions.
- Four rows-C01-C04, C05-C07, C08-C11 and C12-C14 evidence partitions preserve source joins.

**Final disposition:** Internal authoring presence 84/84 PASS. True exhaustive NSEJS Chemistry content coverage: **FAIL for two named CBSE items and otherwise not independently qualified**. Academic and release approval: **HOLD**. No code or scientific source files were edited by this R00 audit; no merge/deploy occurred.

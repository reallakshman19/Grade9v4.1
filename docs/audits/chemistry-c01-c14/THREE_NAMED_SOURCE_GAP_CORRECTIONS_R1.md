# NSEJS Chemistry — Three Named Curriculum Gaps, Owner-Directed Correction R1

**Scope:** Corrections to [Full-Coverage Audit Draft PR #27](https://github.com/reallakshman19/Grade9v4.1/pull/27), `CHEM-FC-001`, `CHEM-FC-002`, `CHEM-FC-013`.  
**Baseline:** Agent B PR #4 + B02 author PR #13, source head `54d44413d10251962fbb7e52180023f3ad5f83b8`.  
**Mode:** AUTHOR_DRAFT · SOURCE-SPECIFIC CONTENT REPAIR · FAIL_CLOSED · ACADEMIC_HOLD.  
**Source**: Official CBSE Class X Science 2026–27 (Carbon and its Compounds; Our Environment) https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/Science_SecP1_2026-27.pdf ; see NCERT Class X Science Chapter 4, functional group Table 4.3 and Our Environment.

## Source-to-native textbook repairs

| Audit ID | Subtopic | What is now explicitly taught | Native Core1B response gate |
|---|---|---|---|
| CHEM-FC-001 | CHEM-C11.05 | Halo- functional-group identities, chloro/bromoalkanes, covalent C–X bonds, chlorine vs Cl⁻, CH₃Cl/C₂H₅Cl/C₂H₅Br and the two C₃H₇Cl positional isomers | Existing REPRESENT task `CORE1B-C11-05-1-B02-R2` retains its exact original first-attempt task; its *independent boundary transfer* now requires C₃H₇Cl structural isomers before the answer is revealed |
| CHEM-FC-002 | CHEM-C14.01 | Stratospheric protective O₃, ozone depletion by persistent ozone-depleting substances (CFC), bounded UV-chlorine radical catalytic ozone-loss model, time lag, and contrast with near-ground photochemical O₃ | Existing MODEL task `CORE1B-C14-01-2` now compares the two causal models, chooses source-specific measurements and requires a changed CFC-emissions recovery argument |
| CHEM-FC-013 | CHEM-C14.05 | Biodegradable vs non-biodegradable materials, microbial breakdown vs plastic fragmentation and recyclable material, realistic conditions and disposal implications | Existing EXPLAIN task `CORE1B-C14-05-1` now classifies paper/PE/glass and independently tests changed compost/landfill conditions |

## Qualifications and exclusions

These are **new author-draft lessons** to resolve exactly named missing scientific concepts; they are not source-first academic admission. The three audit rows are now **candidate remediated, awaiting R01 Chemistry and R02 blind QRT re-review**. No changes to the original historical Audit R1's frozen statuses are made until independent evidence supports it; do not substitute `84/84 qualified`, `3 PASS` or `100% NSEJS syllabus` in any reporting.

To retain the canonical three-primary-operation-per-subtopic inventory, the 21 C11 and 15 C14 Core1B task IDs remain unchanged; C14 updates existing source-related tasks and C11 adds an independent six-stage boundary challenge to an existing REPRESENT cycle. No source exam identity, 47 B02 task route count, 141 staged SVG Git blob, or 252 total canonical Core1B identity count was invented or expanded.

**Boundary:** Because C11's native REPRESENT *initial prompt* is unchanged, the existing author candidate S1/S2/S3 figures remain technically joined without new source text, but they have **not** been independently vetted for the newly authored downstream halo boundary task. S1–S3 remain unreviewed/postcommit-only in P00. C14 tasks have no B02 visual-stage coverage claim.

## Test and review sequence

1. `python -m pytest -q tests/test_nsejs_chemistry_three_syllabus_gaps_r1.py` and unchanged full `python -m pytest -q`.
2. Reader and Core1B test exact content digests, preserved IDs, protected answer sequence and source accuracy.
3. Independent R01: revise science and source-depth acceptance for each of C11.05/C14.01/C14.05, especially schematic catalysis and biodegradation conditions.
4. Independent R02: judge true cognitive bands and novelty of new transfers against taught content and postcommit disclosures.
5. P00: after Owner-authorised integration, test the C14 changed-condition task route (currently on an unmerged sibling author branch) and C11 changed-boundary persistence at a single exact head.

**No merge, deployment, source admission or academic PASS is authorized by this corrective draft.**

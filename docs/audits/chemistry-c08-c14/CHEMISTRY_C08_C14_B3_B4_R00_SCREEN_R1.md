# Chemistry C08–C14 — Core1A/Core1B B3/B4 freshness screening R00/R1

> **Historical baseline as of 15 Nov 2026 before substantive repair.** PR #55 now includes subsequent R3 authored content and adapter changes; the original 17 findings are preserved as the pre-fix evidence. See [R3 remediation delta](CHEMISTRY_C08_C14_REMEDIATION_DELTA_R3.md). Independent R01/R02 and academic/source qualification remain HOLD.

**Task:** `G9V41-CHEM-C08-C14-B3B4-R00-R1`  
**Date:** 2026-11-15  
**Snapshot:** `main` at `7a5c425f02d8a365a738bb11df1982cbe38e9f82`  
**Mode:** AUTHOR-EXPOSED technical and pedagogical *screen* · FAIL-CLOSED · SOURCE-FIRST · NO ACADEMIC SIGN-OFF · NO MERGE/DEPLOY.

## Decision

**Existing authoring is present, but WPE-parity learning quality is not established.** The seven Chemistry C08–C14 packages contain 40 editorial subtopics and 120 native Core1B cycles (18/18/18/21/15/15/15). These are author-produced exercises rather than admitted examination items or independently QRT-adjudicated tasks. The source-to-Core2 original exam chain remains HOLD. This report adds **17 precise B4 freshness-review candidates**; these are a targeted screen, *not* 17 independently determined academic failures or a complete review of all 120 cycles.

## Unit summary

| Unit | Subject | Subtopics | Core1B cycles | Targeted B4 review flags | Disposition |
|---|---|---:|---:|---:|---|
| C08 | Chemical Reactions and Energy | 6 | 18 | 6 | HOLD |
| C09 | Acids, Bases, Salts and Oxyacids | 6 | 18 | 2 | HOLD |
| C10 | Metals, Non-metals and Metallurgy | 6 | 18 | 0 from this screen | HOLD |
| C11 | Carbon and Organic Chemistry | 7 | 21 | 0 from this screen | HOLD |
| C12 | Gases and Chemical Analysis | 5 | 15 | 4 | HOLD |
| C13 | Redox and Volumetric Analysis | 5 | 15 | 2 | HOLD |
| C14 | Environmental and Applied Chemistry | 5 | 15 | 3 | HOLD |
| **Total** | | **40** | **120** | **17** | **HOLD** |

C10–C11 having zero *flags in this limited direct-example screen* does **not** mean they pass B3/B4. Their recent B02 work has more changed-condition constructs and separate academic review remains necessary.

## Exact task-level review register

| Unit · subtopic | Core1B ID | Cross-reference concern |
|---|---|---|
| C08 · CHEM-C08.01 | `CORE1B-C08-01-1` | Same magnesium oxygen-uptake mechanism as the complete worked example; replace or justify the independent decision. |
| C08 · CHEM-C08.03 | `CORE1B-C08-03-2` | Same Fe/CuSO4 reaction as the worked net-ionic transformation. |
| C08 · CHEM-C08.04 | `CORE1B-C08-04-1` | Same ion pair and precipitate as the worked demonstration. |
| C08 · CHEM-C08.04 | `CORE1B-C08-04-2` | Same ion inventory; the task must make an independently chosen condition or inference decisive. |
| C08 · CHEM-C08.06 | `CORE1B-C08-06-1` | The taught CuO/H2 oxygen-transfer roles are tested again. |
| C08 · CHEM-C08.06 | `CORE1B-C08-06-2` | Identical equation and atom ledger as the worked answer. |
| C09 · CHEM-C09.01 | `CORE1B-C09-01-1` | Dry-HCl/moist-litmus observation and aqueous explanation already worked through. |
| C09 · CHEM-C09.04 | `CORE1B-C09-04-2` | The same gypsum/Plaster-of-Paris formula pair and dehydration stoichiometry is worked immediately before practice. |
| C12 · CHEM-C12.01 | `CORE1B-C12-01-1` | Same rigid-versus-moving-piston constraint choice; review for fresh representation burden. |
| C12 · CHEM-C12.03 | `CORE1B-C12-03-1` | Wet-gas collection and discrepancy already explained; changed apparatus or measurement model needed. |
| C12 · CHEM-C12.04 | `CORE1B-C12-04-1` | Gas inventory before/after cooling is the complete worked model. |
| C12 · CHEM-C12.05 | `CORE1B-C12-05-1` | Exactly the same numeric mixture and stages as the worked eudiometry example; strong B4 clone risk. |
| C13 · CHEM-C13.01 | `CORE1B-C13-01-1` | Same CuO/H2 oxidation-reduction classification. |
| C13 · CHEM-C13.01 | `CORE1B-C13-01-2` | Exact contrasting worked reaction reused for APPLY. |
| C14 · CHEM-C14.01 | `CORE1B-C14-01-1` | Similar NO2 traffic/dispersion comparison; independent design choice needs review. |
| C14 · CHEM-C14.02 | `CORE1B-C14-02-1` | Same turbidity-versus-conductivity inference as worked sample. |
| C14 · CHEM-C14.03 | `CORE1B-C14-03-1` | Remote sulfate-associated rain/source transport repeats the worked causal account; review novelty. |

Each row is mechanically anchored by `worked_anchor` and `prompt_anchor` in [the companion JSON](CHEMISTRY_C08_C14_B4_REVIEW_REGISTER_R1.json) and tested against the exact native data. No verdict is produced from a similarity threshold or substituted for cold academic review.

## Specific priority corrections (author proposals, not accepted alterations)

**P0 — C08.01, C08.04, C08.06:** Replace at least the visibly repeated initial attempt with a **different physical system or a new decisive constraint**, requiring the student to build an atom/charge/species ledger independently. Merely changing Mg mass or swapping Ba salts is not enough. For each proposed replacement, record what the fully worked Core1A model demonstrates, which deciding step stays new, independent check, boundary, hint leakage, and key. Preserve source identity, existing attempt history and revision protection through a deliberate migration; do not silently overwrite student attempts.

**P0 — C09.01/C09.04:** Replace dry-HCl/litmus and identical gypsum formula transfer with a changed experimental medium, a new species/stoichiometry situation or genuinely new classification decision. Audit acid basicity-versus-strength and phosphorus oxyacid `P–O–H` hydrogen accounting separately under scientific review.

**P0 — C12.05:** Stop reusing the worked `10 mL CH4 + 30 mL O2` eudiometry numbers in the independent learner prompt. Create a stage ledger with an *unseen* starting mixture and an underdetermination or changed conditioning decision; keep EXTENSION/ENRICHMENT explicit. Avoid providing dangerous student experiment instructions.

**P1 — C13.01:** The first two Core1B cycles reuse both reactions in Core1A (CuO/H2 and ZnO/C). Replace with a changed redox species/conditions problem and require an independently constructed oxidation/reduction ledger and counterexample.

**P1 — C14.01–03:** Review whether street NO2, ordinary filtration, and remote acid rain task demands go beyond the just-shown worked explanations. Retain correct distinctions between evidence, correlation, chemical causality and environmental boundaries.

**All units:** Independently review 40 Core1A subtopics for B3 teaching sufficiency and all 120 exact Core1B cycles for B4 fresh reasoning and five-factor QRT scoring. Preserve 3 legacy named-source gap corrections (C11.05 halogen groups; C14.01 stratospheric ozone depletion; C14.05 non-biodegradable comparison) as AUTHOR-CANDIDATE-REMEDIATED, not academic PASS. Preserve the historical frozen R00 audit and its 3 FAIL / 81 HOLD snapshot; the updated candidate state does not rewrite history.

## Required acceptance chain

1. **Source / Core2:** identify every claimed exam item by exact source year, stem, figure, key and content digest; mark missing custody `SOURCE_HOLD`. Author practice does not equal authentic NSEJS Core2.
2. **Core1A B3:** reviewer names decisive science operations that are explicitly *worked through*, checks assumptions, models, diagrams, misconceptions, independent checks and curriculum-scope classification. The manuscript alone is not a PASS.
3. **Core1B B4:** for each cycle, compare prompt against complete Core1A including examples, footnotes and hints; record unseen reasoning step and distinct physical/chemical boundary; require a source-distinct, post-attempt solution. Use a protected `W` and a separate first-attempt response.
4. **QRT:** independent blinded task reviewer evaluates 12 criterion cells, cognitive operation and D3/D4 five-factor score; downgrades if needed.
5. **Runtime:** HTTP Chromium 1600×1000 and 1000×1600; keyboard/touch, first attempt, staged help, refresh, changed revision, disabled storage, correct source return, no iframe. Existing technical QA is not an academic acceptance certificate.
6. **Release:** exact combined A+B/P00 head, all unchanged Python regressions, reviewer decisions and Owner authorization; until then `HOLD` / `DRAFT`.

## Custody and author exposure

This R00 author-exposed review can identify reproducible exact-task concerns and propose tests. It **cannot** self-certify prior C08–C14 authored content. Assign independent Chemistry scientific reviewer R01 and blind QRT reviewer R02. No changes are made here to the core textbooks, QRT identity, source question bank, original student attempts, shared architecture or production navigation.

## Source pointers

- Native C08–C14 Core1A reader packs: `curriculum/chemistry/agent-b/learner/C08..C14.reader.v0.1.0.json`
- Native C08–C14 Core1B packs: `curriculum/chemistry/agent-b/core1b/C08..C14.core1b.v0.1.0.json`
- Chemistry adapters: `curriculum/chemistry/adapters/C08..C14.v1.json`
- Exact historical coverage: `docs/audits/chemistry-c01-c14/CHEMISTRY_C01_C14_FULL_COVERAGE_AUDIT_R1.md`
- Post-audit fixes: `docs/audits/chemistry-c01-c14/CHEMISTRY_C01_C14_POST_R00_CORRECTION_DELTA_R2.md`
- Architecture rules: `architecture/guidebook.html`, `architecture/core2-source-to-learning-pipeline.html`, `architecture/production-checklist.html`

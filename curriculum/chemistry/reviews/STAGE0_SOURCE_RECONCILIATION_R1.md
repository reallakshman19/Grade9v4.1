# NSEJS Chemistry — Stage 0 source reconciliation and custody baseline

**Status:** STAGE0_SOURCE_MAPPED_CANDIDATE · academic approval HOLD  
**Date:** 2026-11-13 · **repo main pinned:** `82a782f12c57b5d9d25e9b1eb8d2053a56dfabc0`  
**Owner scope:** Chemistry only, two authors, C01–C07 Agent A, C08–C14 Agent B.

## Authority and correct scope

- IAPT 2026: <https://iapt.org.in/> — NSEJS covers Physics, Chemistry and Biology up to CBSE Class X. This is **not** the Class XII NSEC syllabus.
- HBCSE: <https://olympiads.hbcse.tifr.res.in/syllabus/> — Junior Science broadly equivalent to secondary science up to Class X.
- CBSE IX 2026–27: <https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceSt_SecP1_2026-27.pdf> — primary detailed learning outcomes for mixtures/separation, atomic structure, atoms/molecules and wider integrated science.
- CBSE X 2026–27: <https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/Science_SecP1_2026-27.pdf> — primary detailed Chemical Substances content, plus periodic classification marked *formative-only school assessment* (not omitted from NSEJS candidate coverage).
- Earlier Grade VI–VIII baseline is **NOT FULLY RECONCILED** against the exact current curriculum edition. Any proposed earlier-foundation item is tagged accordingly rather than declared source-verified.

## Reconciliation decisions

1. **14 units are an editorial taxonomy.** They are not 14 named official IAPT chapters and must not become a false syllabus authority.
2. The first seven units cover matter, mixtures, chemical laws, quantitative chemistry, atoms, periodicity and bonding. The remaining seven cover reactions, acids, metals, carbon compounds, gas analysis, redox and environmental applications.
3. Use three **distinct planned QRT cognitive operations** per teachable subtopic. This planning allocation is not a claim that any learning journeys have been authored or QRT-accepted.
4. Chemistry-specific D3/D4 is high-complexity reasoning with the same Class X science boundary; advanced quantum subshells, molecular geometry, eudiometry, titration and extensive stoichiometry require EXTENSION/ENRICHMENT/SCOPE_REVIEW where warranted.
5. CBSE X periodic classification is formative-only **in its school examination**, but is included within the CBSE curriculum. Do not reinterpret that as NSEJS exclusion.
6. The Class X pH syllabus does not require a logarithmic definition; do not promote the logarithmic derivation into unmarked CORE.
7. Some textbook concepts (ionic vs covalent bonding) span CBSE IX atoms/molecules and X carbon/metals. Reuse canonical concept references rather than duplicate scientific authority across units.
8. Proposed D4 tasks should combine relevant concepts where scientifically credible. Do not force D4 onto small prerequisite facts.

## Observed repository baseline at pin

| Register | Count | Status |
|---|---:|---|
| `nsejs/data/chemistry-core2-candidates.v1.json` | 119 (D1 36, D2 76, D3 7, D4 0) | 119 NOT_ADMITTED |
| `nsejs/core2/question-map.v1.json` | 87 Chemistry records | 267 across PCB; identity and custody HOLD |
| `nsejs/data/core1ab-coverage.v1.json` | 7 historical Chemistry constructions | 2 authored previews; 5 unpublished originals |
| Proposed syllabus register | 14 owner-proposed units, 84 subtopics | STAGE0_CANDIDATE |
| Proposed cognitive mappings | 3 operations × 84 = 252 targets | NOT BUILT/NOT QRT-REVIEWED |

The 119 registry and 87 legacy-map Chemistry entries are different inventories. Neither number is a verified textbook coverage denominator.

## Ownership and non-overlap

**Agent A** owns common Core/QRT/syllabus/adapter contracts plus C01–C07; **Agent B** owns C08–C14, and may file scoped contract gap requests. Both agents must reference canonical shared concepts across their unit boundary.

## Stage 0 acceptance boundary

**Completed in Stage 0:** baseline pin, official 2026–27 IX/X source inventory, C01–C14 proposed taxonomy, 84 subtopic candidate inventory, split ownership, tagged scope exceptions, existing public asset counts and source limitations.

**Not completed in Stage 0:** independent academic adjudication of 84 items, exhaustive exact-edition VI–VIII source reconciliation, Core1A/B chapter authoring, 28-cell QRT academic acceptance, source original/answer-key custody and student-release approval.

No exam sources are substituted by invented questions. The existing source HOLD states survive unchanged.

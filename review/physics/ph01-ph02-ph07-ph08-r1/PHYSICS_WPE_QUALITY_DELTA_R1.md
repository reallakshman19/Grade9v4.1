# PH01 / PH02 / PH07 / PH08 — WPE comparison and corrective R1 delivery

**Task:** `G9V41-PHYSICS-PH01020708-WPE-QUALITY-R1`  
**Mode:** `FOUR_AUTHORING_EXEMPLARS · SOURCE_BOUNDARY_HARDENED · NO_ACADEMIC_PROMOTION`  
**Disposition:** `R1_IMPLEMENTED_CANDIDATE · B1–B7_HOLD · OWNER_RELEASE_HOLD`

## Exact scope, not an inflated claim

The four selected learner chapters contain **41 catalogued subtopics** (8+8+12+13). The R00 register is a baseline, not 41 qualified lessons. R1 introduces **four new, independently versioned Core1A/Core1B authoring extensions** at PH01-M05, PH02-F04, PH07-02 and PH08-08. The other **37** subtopics retain their previous author-only content and academic HOLD, with no R1 claim of pedagogic revision.

The extensions are reached from their chapter subtopic cards. All four use original author-created science and task prompts, not original NSEJS examination stems. Native legacy textbook/attempt pages and the B01 78 byte-pinned author HTML files are **left unchanged**; past attempts are not re-keyed or overwritten.

## Verified versus missing major improvements across each Core

| Core | Technical/learning correction in R1 | Evidence type | Result |
|---|---|---|---|
| Core2 | Source-evidence ledger showing each selected chapter's source relation, with 41 candidate A/B links | `quality-r1/source.html`; R00 manifest; HTTP test | IMPLEMENTED, not authenticated exam bank |
| Core2 | Remove false Heat/Sound `fluids` question-bank route and PH08 buoyancy help | `learn/catalog.json`; navigation regression | IMPLEMENTED |
| Core2 | Exact original-question custody, official figures/keys and per-item protected Core2 reader | Not provided by current publisher/source custody | **NOT FIXED · SOURCE HOLD** |
| Core1A | Three distinct graduated, solved examples on each of four decisive operations | `quality-r1/cases.v1.json` and real study page | IMPLEMENTED FOR 4/41 |
| Core1A | Explicit model conditions, scientific representation, dimensional/independent check, misconception repair | Four study diagrams and corrective discussions | IMPLEMENTED FOR 4/41; independent Physics R01 NOT_RUN |
| Core1A | Author-level teaching-to-QRT operation alignment without exposing reserved task solution in the study page | Four newly versioned adapter-linked constructions | IMPLEMENTED AS AUTHOR DESIGN; independent B3 NOT_RUN |
| Core1B | Original tasks with a changed decisive operation/condition, not merely a numeric replacement | Four unique UIDs, task revisions, explicit transfer-difference witness | IMPLEMENTED FOR 4/41; independent B4 NOT_RUN |
| Core1B | Protected first attempt, content SHA-256, staged help, refresh recovery and storage fail-closed | `quality-r1/runtime.js`; HTTP Chromium two orientations | TECHNICAL PASS on tested revision |
| Core1B | Separate diagnosis, repair and boundary attempt before model reveal | Four six-stage tasks, automated ordering test | TECHNICAL PASS; learner B6 evidence NOT_RUN |
| Adapter/QRT | Four versioned candidate topic-adapter maps with old instances preserved and new task IDs joined | PH01 53→54, PH02 24→25, PH07 43→44, PH08 46→47 | MAPPING IMPLEMENTED; QRT independent scores absent |
| Blueprint authority | Five-factor independently scored D3/D4 and selected canonical MAINs | No blind adjudication in this change | **NOT FIXED · QRT HOLD** |

These statuses are non-compensatory. A technical check or a well-written example cannot upgrade a SOURCE, QRT or B1–B7 academic HOLD.

## WPE pilot evidence comparison

WPE's earlier five Learn→Challenge pairs received actual teaching content changes: expanded guided explanations, four reworked figures to avoid future-challenge solution leakage, option-specific diagnosis, and local first-attempt continuity. Its independent B3/B4 review nevertheless recorded gaps (weak transfer for two of five, insufficient worked reasoning for five of five) and no academic admissions. WPE is an instructional **process comparison**, not an academically certified Golden Sample.

In contrast, PR #57 R00 changed navigation only. This R1 adds **four concrete new teaching/transfer constructions and versioned adapters**, with a reproducing browser route. It still does **not** demonstrate complete WPE-equivalent quality or official NSEJS coverage for 41 subtopics.

### R1 exact construction signature by chapter

| Chapter/unit | Scientific decision worked in Core1A | Protected fresh decision in Core1B | Adapter cell |
|---|---|---|---|
| PH01-M05 | Signed graph slopes; velocity area versus absolute path; reversed coordinate | Reconstruct three piecewise velocities in two frames, signed displacement/distance and undefined corner velocity | `REPRESENT D3.5` · author nomination |
| PH02-F04 | Correct third-law recipients; separate force equations; centre-of-mass reconciliation | Infer contact magnitude independently from **two sensors**, test contact consistency and correct a changed brake value | `JUSTIFY D3.7` · author nomination |
| PH07-02 | Heat transfer versus U; driven steady state; capacity-sensitive cooling | Compare **two distinct hot plates** after switching off, infer initial energy and temperature rates, then challenge the phase-change limit | `MODEL D3.4` · author nomination |
| PH08-08 | Equal-leg echo versus separated detector; path-length difference and threshold | **Unequal** wall distances, two arrival clocks, detector criterion and moving-mic boundary | `MODEL D3.4` · author nomination |

These are different from the three solved study examples in each unit. Blind reviewer assessment is still required to establish that the decisive operation is sufficiently changed.

## Topic adapter custody

The existing topic-adapter versions and native physics packages remain unchanged. New candidate versions preserve historical task identities and add only the four new author identities:

- `PH01/topic-adapter.PH01.v0.12.0.json`
- `PH02/topic-adapter.PH02.v0.2.0.json`
- `topics/PH07/topic-adapter.PH07.quality-r1.json`
- `topics/PH08/topic-adapter.PH08.quality-r1.json`

Each is `CANDIDATE_ONLY`, `NOT_SELECTED`, `independent_qrt: NOT_RUN`. New task dossiers now include a five-factor **author-only** D3 hypothesis (7/10 with one concrete reason per factor). Independently adjudicated scores remain explicitly **null**; no D3 admission follows from an author hypothesis. The PH07/08 candidate aggregates are built from B01's **16 author-proposed topic-cell groups** and include prior supplemental INSTANCE proposals; the original 16 mixed MAIN proposals remain unselected. No original source or official exam claim is added by this mapping.

## Evidence custody and outstanding gates

Machine-readable per-unit evidence: [PHYSICS_4_CONSTRUCTIONS_EVIDENCE_R1.v1.json](PHYSICS_4_CONSTRUCTIONS_EVIDENCE_R1.v1.json). Every row retains source, science, QRT, B1–B7 and admission HOLD. The source ledger remains honest when source material cannot be authenticated. Protected first attempts are browser-local with an immutable UI path but are **not tamper-proof** against a learner modifying localStorage or downloaded JS.

**Outstanding required work:** independently authenticate each original-paper question/figure/key and its rights, establish official detailed syllabus coverage denominator, run blind original-question SL1/P1/SL2/QRT with explicit five-factor scores and canonical owner-selected adapter, obtain cold scientific B3/B4 review and actual learner B6 evidence, improve the other 37 lesson/task pairs based on those findings, perform exact-head tablet/screen-reader checks, and obtain separate Owner release authority.

**Decision:** Keep PR #57 DRAFT, unmerged and undeployed. The change is a technically implemented four-unit exemplar and source-boundary correction—not final nine-of-nine quality completion for 41 units.

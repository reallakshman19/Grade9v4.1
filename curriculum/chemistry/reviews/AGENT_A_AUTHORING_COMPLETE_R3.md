# Agent A — NSEJS Chemistry C01–C07: Authoring completion R3

**Task:** `G9V41-NSEJS-CHEM-A-C01-C07-AUTHORING-COMPLETE-R3`  
**Disposition:** `AUTHORING_COMPLETE · TECHNICAL_QA_PASS · INDEPENDENT_ACADEMIC_REVIEW_DEFERRED · FAIL_CLOSED`  
**Date:** 2026-11-13  
**Repository:** https://github.com/reallakshman19/Grade9v4.1  
**Implementation:** [Draft PR #6](https://github.com/reallakshman19/Grade9v4.1/pull/6), stacked on [Draft PR #1](https://github.com/reallakshman19/Grade9v4.1/pull/1)  
**Owner sequencing:** Implement Agent A's material now; independent review and prerequisite integration later. No merges, deployment or claim of qualification.

## Completion scope

| Artifact / function | Authored count | Qualification |
|---|---:|---|
| Connected textbook chapters (C01–C07) | 7 | Author-complete, academic HOLD |
| Version-pinned syllabus subtopics | 44 | Source-mapped candidates |
| Chapter learning spines, previous knowledge and concept journeys | 7 | Author-complete |
| Original conceptual investigations | 44 | Author-complete |
| Four-step or deeper causal-inference sequences | 44 | Author-complete |
| Original SVG scientific figures with title/description/alt text | 16 | Technical checks passed |
| QRT-linked Core1B reconstruction tasks | 132 | Author candidates, **not** independently QRT-rated |
| Topic Adapters `C01.v1.json`–`C07.v1.json` | 7, v0.2.0 | Schema valid, academic HOLD |
| Canonical authored concept refs with Git blob provenance | 44 | Draft truth, no independent scientific promotion |
| Per-task QRT author evidence with 12 pending reviewer slots | 132 | No automated/human verdict fabricated |
| Tablet HTML routes | 7 + table of contents | HTTP Chromium candidate QA passed |

**C01:** particle model, states, diffusion, phase change, evaporation and heating curve.  
**C02:** pure substances/mixtures, dispersions, concentration, solubility and separation design.  
**C03:** conservation, constant composition, chemical entities, formulae, masses, electron dots.  
**C04:** mole, conversion, balanced ratios, stoichiometry, limiting reagent and yield.  
**C05:** particle identities, Rutherford evidence, Bohr shells, isotopes, ions, subshell enrichment.  
**C06:** historical and modern classification, main-group patterns, trends, prediction and exceptions.  
**C07:** valence and stability, ionic/covalent bonding, Lewis diagrams, isomers and molecular structure, empirical evidence, shape and polarity.

Every subtopic contains a scientific starting question, a connected explanation, a scientific reasoning path, a prediction-based investigation with analysis/limits, a faithful representation or named explanatory diagram, a fully worked example, a plausible misconception, an explicit repair and at least **three different primary QRT operations**.

Core1A teaches before the Core1B task. Core1B provides predict, attempt, reconstruct, diagnose, repair, boundary and post-attempt model response. Input is protected per SHA-256 **full authored lesson file**; when browser storage is unavailable, the UI says the attempt cannot survive refresh.

## QRT template coverage — exact identity accounting

The shared library contains 28 templates (7 cognitive operations × D1–D4). Chemistry's Stage 1 blueprint declares all **14 D3/D4** cells. Agent A has **132 task instances covering 7 distinct D3/D4 template cells**, not 132 unique template identities.

| Populated in Agent A | Instances |
|---|---:|
| QRT-APPLY-D3 | 8 |
| QRT-EXPLAIN-D3 | 34 |
| QRT-MODEL-D3 | 23 |
| QRT-MODEL-D4 | 5 |
| QRT-REPRESENT-D3 | 23 |
| QRT-SYNTHESIZE-D4 | 16 |
| QRT-JUSTIFY-D4 | 23 |
| **Total** | **132** |

**Not instantiated by Agent A (defer to combined Agent A/B gap analysis, never invent filler):**
`QRT-RETRIEVE-D3`, `QRT-RETRIEVE-D4`, `QRT-EXPLAIN-D4`,
`QRT-APPLY-D4`, `QRT-REPRESENT-D4`, `QRT-SYNTHESIZE-D3`,
`QRT-JUSTIFY-D3`.

A missing cell is a transparent programme-level gap, not an excuse to mislabel a D2 retrieval problem as D4. Agent B should look for genuinely appropriate C08–C14 constructions and file a scope-relevant gap for any that remain.

## Exact-head technical evidence

**Verified engineering head before this report-only commit:** `393090869b06f18ab58e576b3bef8e70d71f1e68`.

- Python QA [run 43470535381](https://github.com/reallakshman19/Grade9v4.1/actions/runs/43470535381), both Python 3.11 and 3.12: **358 passed, 1 inherited zipfile warning, 0 failed** per matrix job.
- Chromium [run 43470535550](https://github.com/reallakshman19/Grade9v4.1/actions/runs/43470535550): **PASS**. Seven chapter routes × portrait 1000×1600 and landscape 1600×1000 = 14 HTTP tablet views; 44 investigations; 132 independent-response cards; 16 scientific figures; first attempt, refresh readback, disabled storage and no horizontal overflow.
- Test suite validates 7 books, 44 subtopic joins, 132 adapter-linked operations, source blob pins, incomplete-review guards, scientific diagrams and 12 review slots.

**No academic approval inferred from software validation.** Test counts do not establish textbook depth or scientific accuracy by human expert judgment.

## Authority/custody boundaries that remain for later review

- All current material is original Grade9-authored *candidate* teaching and practice. No past NSEJS question, answer key, figure or paper is certified by this package.
- Scope-labelled `FOUNDATION_RECONCILE`, `SCOPE_REVIEW`, `EXTENSION` and `ENRICHMENT` remain visible; advanced C04–C07 content is not asserted as compulsory NSEJS syllabus.
- The exact Class VI–VIII source-by-source curriculum crosswalk is unfinished and is **not** a blocker to retaining transparent candidate authored material.
- Independent science, source/copyright custody, difficulty-band comparison, 12-point QRT/B1–B7 human reviews, keyboard/accessibility qualification and final release authority are still **HOLD**.
- The textbook HTML is available in the development branch at `curriculum/chemistry/preview/index.html`, but is **not** merged or linked as a production-approved student textbook.
- The existing original Core1 source reconstruction and source-authenticity defects outside this newly authored teaching set remain outside this task; this implementation does not replace or claim recovery of historical originals.

## Cross-agent handoff

Agent B owns C08–C14; it can draft against the **44 pinned authored concept references** in `registry/agent-a-canonical-concepts.v0.1.0.json`, especially:

- C08 reaction quantities ↔ C03/C04;
- C09 acidic structures and neutralisation ↔ C03.04, C04.03, C07.04–.05;
- C10 metals ↔ C05/C06/C07;
- C11 organic structure ↔ C07.03–.07;
- C12 gas analysis ↔ C01/C04;
- C13 redox ↔ C04/C05;
- C14 environment ↔ C01/C02.

These are stable **draft references**, not academically verified source custody. Maintain explicit HOLD until independent qualification. Agent B does not need to wait for textbook authoring to continue.

**Author work disposition:** C01–C07 feature and textbook authoring are finished for the agreed Stage 2 scope. Independent review, prerequisite reconciliation and optional later expansion are separately tracked, not silently declared complete.

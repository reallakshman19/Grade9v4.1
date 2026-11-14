# Grade9 v4.1 — NSEJS Chemistry Core1A/Core1B Multi-Agent Technical Specification R1

**Task ID:** G9V41-NSEJS-CHEMISTRY-CORE1AB-MULTIAGENT-ONBOARD-R1  
**Repository:** https://github.com/reallakshman19/Grade9v4.1  
**Scope:** CHEMISTRY ONLY · C01–C14 · Core1A textbook / Core1B active reconstruction / evidence-bound Core2 links  
**Mode:** TEXTBOOK_FIRST · D3/D4_PRIORITY · SOURCE_FIRST · FAIL_CLOSED · NO_IFRAMES · AUTHOR_EXPOSED  
**Document status:** PROPOSED_OWNER_ASSIGNMENTS · NO_QUALIFIED_CHEMISTRY_CLAIM · NO_MERGE · NO_DEPLOY  
**Role change:** R00 (ChatGPT) is **technical reviewer and integration auditor only**; no further chapter authorship, no cold-independent academic certification.

> These documents create ready-to-send instructions, not active new agents, owner transfers, source rights, approval to merge, or authorization to publish. Use explicit Owner approval for assignments, merges, changes to shared contracts, publication and release.

## 0. Authenticated GitHub workstream reconciliation (2026-11-13)

| Workstream | Snapshot | Authority and status |
| --- | --- | --- |
| Main at planning | 218b9f2da4b71e0eb03d6769c8ad6c842434e652 | Does **not** automatically contain the parallel draft authoring branches |
| Chemistry Stage 0/1 shared contracts | [Draft PR #1](https://github.com/reallakshman19/Grade9v4.1/pull/1), head 77d2bd63328c184598088bce6b9888fc8324cb4b | Unmerged, shared candidate source/syllabus/adapter/QRT authority |
| Agent A C01–C07 | [Draft PR #6](https://github.com/reallakshman19/Grade9v4.1/pull/6), head fb5cf6626088a1312743d60d0c39d06a4a3f8133 | Unmerged, stacked on PR #1, 44 authored subtopics, 132 QRT candidates |
| Agent B C08–C14 | [Draft PR #4](https://github.com/reallakshman19/Grade9v4.1/pull/4), head b8e4f6f99a9bb8000fb243ee6a2a2765fc5d2509 | Unmerged, separately stacked on PR #1, 40 authored subtopics, 120 QRT candidates plus 24 capstones |
| Physics onboarding methodology reference | [Draft PR #7](https://github.com/reallakshman19/Grade9v4.1/pull/7) | Reference only; Chemistry-specific contracts and ownership prevail |

Snapshot hashes are not permission to use stale branches. Every assigned author must check the live ref and log exact before/after commit SHAs and review results.

**Do not combine PR #4 and PR #6 into one mutable working branch while multiple agents edit.** They are siblings above PR #1. The PR #4 Agent B author retains C08–C14 until the Owner explicitly transfers responsibility. PR #6 is an author-complete candidate; A01–A04 are proposed *improvement* workpacks, not newly missing chapters.

### Actual quantitative ledger

- Shared candidate syllabus = **14 C-units, 84 subtopics**, partition C01–C07: **44** and C08–C14: **40**.
- Candidate learning cycles = **132 + 120 = 252**, plus **24 Agent B extra chapter capstones** that are tracked separately. These are authored tasks, not 276 approved NSEJS questions.
- Agent A has **16** original SVG scientific figures, seven chapter learning spines and 44 inquiry constructions; Agent B has **8** SVG figures and seven authored textbooks as separate branch sources.
- Agent A exact head verification: [Python 43471007753](https://github.com/reallakshman19/Grade9v4.1/actions/runs/43471007753), 358 passed on each of 3.11/3.12 (one warning); [HTTP Chromium 43471007458](https://github.com/reallakshman19/Grade9v4.1/actions/runs/43471007458), 14 tablet views PASS.
- Agent B exact head verification as reported and documented in Draft PR #4: [Python 43472329268](https://github.com/reallakshman19/Grade9v4.1/actions/runs/43472329268) 355 pass per Python version with one browser skip and one warning; [HTTP Chromium 43472329238](https://github.com/reallakshman19/Grade9v4.1/actions/runs/43472329238) 25 pass.
- All these results are **technical evidence only**; independent academic, source and D3/D4 acceptance are zero unless later explicitly reviewed and recorded.

## 1. Governing authority, provenance and precedence

1. Repository instructions: AGENTS.md, Start_here.md, CURRENT_CHECKPOINT.md, docs/product-scope.md, architecture/guidebook.html, issue #1, native authoring guidance, applicable QRT and learner-journey contracts.
2. Original shared 28 canonical QRT templates (seven operations × four levels) under Grade9v3.5/Shared/quality/question-demand-templates.v1.json; do not silently mutate IDs or reclassify difficulty.
3. Chemistry contract candidate in PR #1: curriculum/chemistry/syllabus/chemistry-syllabus.v1.json; curriculum/chemistry/blueprint/chemistry-qrt.D3-D4.v0.1.0.json; curriculum/chemistry/contracts/chem-topic-adapter.schema.v0.1.0.json; related Core contracts and validator. **14 D3/D4 chemistry cells are proposed**, not independently qualified.
4. Author manuscript candidates in PR #6 and PR #4: prefer their existing stable subtopic IDs, authored draft concept refs, diagrams and QRT bindings over duplicate constructions.
5. Version-pinned authenticated subject and original exam sources only. When exact editions, rights, scan, figure, identity and answer-key evidence are unavailable, use SOURCE_HOLD and an original authored example.

Conflicts: source reality > scientifically justified chemistry > verified source lineage > approved shared contract > candidate branch content > author proposal. Do not use test success to override curriculum or source HOLD.

## 2. Multi-agent ownership and authoring partition

| Workpack | Exclusive units | Existing candidate starting point | Scope |
| --- | --- | --- | --- |
| A01 | C01–C02 (13 subtopics) | PR #6 | Physical foundations: particle models, matter, phases, mixtures and separation |
| A02 | C03–C04 (12) | PR #6 | Atomic laws, formula units, mole and stoichiometric models |
| A03 | C05–C06 (12) | PR #6 | Atomic evidence, shells, isotopes, periodic relationships and exceptions |
| A04 | C07 (7) | PR #6 | Molecular structure, bonding, Lewis and structure–property mechanisms |
| B01 — RESERVED | C08–C09 (12) | PR #4 | Reactions, energy, acids, bases, salts and oxyacids |
| B02 — RESERVED | C10–C11 (13) | PR #4 | Metals, metallurgy and carbon compounds |
| B03 — RESERVED | C12–C14 (15) | PR #4 | Gas analysis, redox, volumetry and environmental chemistry |

A01–A04 are **proposed new author assignments** after this reviewer-role change, not magically active agents. For B01–B03, the existing Agent B author remains the sole owner until an explicit Owner transfer names the new agent, pinned base and exact C-unit paths. No author owns another unit's source manuscript.

**P00:** shared Chemistry reader and Core1B runtime engineer, may change cross-cutting UI or runtime only when specifically assigned.  
**R00 (me):** technical reviewer, integration auditor, fail-closed custody/regression checker; **no chapter source edits** and no cold-review claim.  
**R01:** distinct, source-first independent Chemistry academic reviewer; must not have authored the manuscript being assessed.  
**R02:** separate blind cognitive/QRT evaluator when needed; records real D3/D4 comparison and B1–B7 judgments.  
**Owner:** sole allocation, contract, merge, release, publication and deployment authority.

## 3. Core1A: self-study textbook acceptance, not a trick sheet

Each subtopic must be a coherent mini-chapter in the larger unit story, not three disconnected question cards. The reading should normally include:

- An authentic phenomenon, observable puzzle, or scientific motivation, including what the student already knows and a precise new question.
- A connected scientific explanation, mechanisms at the appropriate particle/chemical scale, explicit assumptions, evidence and when possible multiple genuine representations: words, reaction/particle pictures, equations, graphs, formulae and tables.
- At least one worked construction showing every intellectual jump; independent checks of units, atoms, charges, ratios or data where relevant; multiple worked variations if a chapter needs them.
- A predictive inquiry / thought experiment with observation, interpretation, alternative explanations and stated limits. Teacher-only hazardous procedures must not become student lab instructions.
- At least one credible wrong route, causal diagnosis, repair, and a boundary condition where the convenient shortcut fails.
- Scaffolding that supports a learner without prior coaching: vocabulary, prerequisites, bridge to the next chapter, concept synthesis and explicit optional-enrichment labelling.
- Original diagrams with descriptive text, readable in 12.7-inch tablet portrait/landscape; diagrams must teach concepts, not decorate exam answers.

Do not downgrade explanations to memorised bullet tricks. Do not claim that word count, textbook-page count, UI illustrations or automated checks independently prove scientific quality.

### Chemistry-specific scientific red flags

- **C01–C02:** distinguish microscopic diffusion from bulk convection; conserve matter across phases; separate true molecular solutions, colloids and suspensions; declare concentration and solvent bases; distinguish observed results from hypothetical experimental models.
- **C03–C04:** atom/element conservation, charge neutrality, molecular versus ionic formula unit, atomic/molar masses, coefficients versus subscripts, dimensional mole conversion, leftovers versus target yield and exact reaction assumptions.
- **C05–C06:** proton count defines element; neutrons/isotopes versus electrons/ions; Rutherford evidence versus Bohr shells; period/group trends require domain and exceptions; atomic number versus average atomic mass.
- **C07:** ion lattices versus discrete molecules; electron transfer/sharing is not automatic stability proof; Lewis drawings are not measured 3D geometry; separate intramolecular and intermolecular interactions; distinguish same-formula different-connectivity isomers; polarity as optional model.
- **C08–C09:** reactions must conserve atoms and charge; exo/endothermic versus activation energy; acid *basicity* not acid strength; for phosphorus oxyacids count ionisable **P–O–H** hydrogens rather than **P–H**; reducing behaviour requires redox evidence and oxidation-state accounting.
- **C10–C11:** oxidation/corrosion versus reactivity series and extraction context; valence-bond consistency, structural isomers, functional groups, reaction classes, nomenclature scope and safety.
- **C12–C14:** gas identity versus test artefact, redox electron/charge ledger, limiting and titration assumptions, environmental causal data versus correlations and underdetermined claims.

Advanced material must use the syllabus tag actually supported by the source (FOUNDATION_RECONCILE, SCOPE_REVIEW, EXTENSION, ENRICHMENT or local equivalent). A useful olympiad enrichment is not automatically mandatory official NSEJS syllabus.

## 4. Demand/QRT contracts: minimum three genuine scientific demands per topic

Every substantive subtopic must carry **at least three distinct primary cognitive operations** (unless an explicitly justified exception is approved). Three numerical substitutions, the same Lewis drawing with different molecules, or three copies of an answer-key task **do not** count as three independent demands.

Canonical operations: RETRIEVE, EXPLAIN, APPLY, MODEL, REPRESENT, SYNTHESIZE, JUSTIFY. Bands D3/D4 are **author-proposed** until independently adjudicated using a five-factor evidence rubric: concept/model selection, representation translation, inference chain, mathematics/logic burden, plausible trap sensitivity.

Each actual task must bind stable IDs and the Chemistry Topic Adapter slot semantics:

| Slot | Required proof |
| --- | --- |
| X | Exact new learner context/task wording; cannot be an answer to a previously shown example |
| Y | Relevant scientific/chemical ground truth, with model assumptions and source/scope binding |
| Z | Fully worked legal pathway, with independent check and boundary |
| W | Exact independent decision/construction the learner must generate *before* clues disclose the result |

The learner-facing task must preserve W; the canonical worked route is not presented before the first attempt. H1/H2/H3 should progressively help without giving W away. Each QRT review has **12 explicit criterion cells**, not 12 automatically passing boolean flags: H1–H3, S1–S3, P1–P3, M1–M3. Record reviewer, exact content revision, evidence and adverse findings before any acceptance.

Agent A's existing 132 tasks occupy **seven distinct D3/D4 template cells** (APPLY-D3, EXPLAIN-D3, MODEL-D3, MODEL-D4, REPRESENT-D3, SYNTHESIZE-D4, JUSTIFY-D4). The other seven Chemistry D3/D4 cells are genuine *programme coverage gaps*, not evidence that all 14 have been authored. Agent B candidates may cover further cells but must be counted from actual instances rather than assumed.

## 5. Core1B runtime and learner contracts

Every authored construction needs a genuine student-owned learning sequence:

**Predict → Attempt → Reconstruct → Diagnose → Repair → Boundary Test**, plus post-attempt worked closure.

Non-negotiable implementation rules:

1. Record first attempt before revealing the model answer or a decisive hint. A solution, hidden DOM text, devtools data or help button is not secure examination access; describe only the supported pedagogic progressive-disclosure property.
2. Tie saved first attempt to the exact full-content revision/digest and stable task identifier, not only a mutable display title or course level.
3. Refresh/back navigation preserve the first attempt for unchanged content. A stale revised task must not silently reuse an incompatible answer.
4. Distinguish first response, H1/H2/H3 help exposure, repair answer and independent transfer. Do not overwrite the first response on later attempts.
5. On disabled storage, fail closed on persistence claims and disclose ephemeral-session limitations; no fabricated saved success.
6. Render in actual HTTP Chromium with touch and keyboard; no iframe as a workaround; use existing native navigation, source return and accessibility patterns.
7. Integrate A and B reader paths only after a P00 interface contract is agreed: A draft routes curriculum/chemistry/preview/C01.html ... C07.html; B draft route nsejs/chemistry/textbook/index.html?unit=C09 and corresponding units. Do not replace one reader with an unreviewed duplicate.

## 6. Source custody and Core2 identity

Authentic original NSEJS problems require authenticated paper/edition/year, question identifier, verbatim source, figure integrity, official or separately verified key, permission/custody and stable content digest. An original authored-transfer task is **not** an original NSEJS question. No invented source IDs, source files, exam authenticity or answer-key authority.

Maintain a per-subtopic provenance row: source reference, edition/page or link, classification (core/extension), exact claim supported, reviewer status, concept ID, content SHA and conflicts/HOLDs. Preserve unpublished/private materials outside public Git. Where source is incomplete, retain CONTENT_CANDIDATE / SOURCE_HOLD instead of fabricating source-qualified Core2.

## 7. Branch, file and integration ownership

Each author creates a new branch off the **exact assigned candidate PR branch**, and a **DRAFT PR targeting its assigned source branch**. Do not branch C01–C07 editing from PR #4 or C08–C14 editing from PR #6. Do not use a stale main checkout to overwrite candidate manuscript files.

- A author: exclusively owned C-unit content, matching unit adapter, unit-level figures and tests; shared registries may be patched only through a separate small integration review.
- B reserved authors: exclusive C-unit files inherited from existing PR #4 only after Owner transfer.
- P00: runtime/renderer, cross-unit state, browser test harness and CSS as assigned. No author concurrently edits those shared files.
- R00: diff/read-only review, required changes and evidence report; authors implement corrections and resubmit.
- Shared Stage 0/1 contracts: immutable unless a versioned proposed amendment is approved by Owner; keep backwards compatibility or prove migration.

Integration sequence only after Owner approval: qualify base PR #1; rebase PR #6 and PR #4 independently; reconcile concept registries, duplicate route contracts and runtime semantics; check all C01–C14 IDs once; re-run complete combined tests; obtain independent academic approval and final release decision. No implicit merge authority.

## 8. Mandatory verification and completion evidence

For every author PR, require:

- Exact base SHA/head SHA, changed-file inventory, source and model status, per-unit subtopic coverage and marked scope; no misleading '100% academically qualified' language.
- Each subtopic must include three distinct operations, paired explanatory Core1A, a novel W, six-stage Core1B, three progressive hints, complete model answer, independent check, misconception/boundary and source review state.
- Adapter passes the pinned JSON schema, IDs join, QRT template refs are canonical; count QRT **instances** and unique **template cells** separately.
- Run unchanged repository Python QA in Python 3.11/3.12 and real HTTP Chromium at 1000×1600 portrait and 1600×1000 landscape, touching every chapter, figures, keyboard, hints, first attempt, refresh, stale revisions and disabled storage. Attach screenshots/logs and exact-head results.
- Author self-review B1–B7 witness and 12 QRT criterion entries are submitted as **candidates only**. Independent academic reviewers independently validate content, source, exam/figure fidelity and depth. R00 checks technical integration but cannot certify its own previously authored C08–C14 as cold review; a separately appointed R01 must evaluate academic correctness across all 14 units.
- No merge, release or deployment merely because tests pass. If evidence is missing, say HOLD and retain the draft.

### R00 review disposition vocabulary

**TECHNICAL_PASS** (engineering evidence verified); **CHANGES_REQUESTED** (specific corrective diff needed); **EVIDENCE_INCOMPLETE** (not enough exact-head/source evidence); **INTEGRATION_HOLD** (shared branch/owner conflict); **ACADEMIC_HOLD** (science/QRT/source not independent). Technical PASS and ACADEMIC_HOLD may coexist. R00 does not issue academic PASS.

## 9. Owner decisions and onboarding activation

Owner chooses whether A01–A04 are activated, identifies agent contacts, approves their exact PR #6 base head and per-unit paths; for B01–B03 also explicitly transfers from existing Agent B and chooses which workpacks activate. Owner separately approves P00 ownership; appoints truly independent R01 and R02; accepts any shared contract amendment; and alone authorises merge and publication.

**Completion of this document ≠ assigning an agent or approving a branch.**

See adjacent ready-to-send prompts and machine workpack registry:
- docs/agent-entry/nsejs-chemistry-core1ab-agent-onboarding-prompts-r1.md
- docs/agent-entry/nsejs-chemistry-core1ab-multiagent-workpacks-r1.json

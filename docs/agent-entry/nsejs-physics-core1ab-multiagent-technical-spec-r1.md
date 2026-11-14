# Grade9 v4.1 — NSEJS Physics Core1A/Core1B Multi-Agent Technical Specification

**Task ID:** \`G9V41-NSEJS-PHYSICS-CORE1AB-MULTIAGENT-ONBOARD-R1\`  
**Document type:** Owner-to-agents technical onboarding; author-exposed planning source  
**Scope:** PHYSICS ONLY · 12 textbook domains PH01–PH12 · Core1A + Core1B + source-qualified Core2 linkage  
**Operating mode:** TEXTBOOK_FIRST · D3/D4_PRIORITY · SOURCE_FIRST · FAIL_CLOSED · NO_IFRAMES  
**Document status:** \`PROPOSED_HANDOFF · OWNER_ASSIGNMENTS_PENDING · ACADEMIC_HOLD\`  
**Repository:** https://github.com/reallakshman19/Grade9v4.1  
**Date of reconciliation:** 2026-11-13  
**Model's continuing role:** Technical reviewer and integration auditor only. No additional primary chapter authorship under this workstream.

> This document authorizes **planning and isolated draft proposals only**. It does not authorize a merge, deployment, publication of restricted sources, an academic promotion, or declaring prior source candidates qualified. If a prior task assigns a different owner, that task remains in force until the Owner explicitly transfers it.

## 0. Live repository reconciliation: do not confuse the three branches

| Purpose | Current checked reference | Academic/release status |
|---|---|---|
| Shared candidate contracts | [Draft PR #2](https://github.com/reallakshman19/Grade9v4.1/pull/2), head \`330f9524fe37cff53f20b6f094c85e4739da3a66\` | Unmerged; candidate C01–C08 v1.0.0 |
| Agent 1 PH01 + proposed C06 amendment | [Draft PR #3](https://github.com/reallakshman19/Grade9v4.1/pull/3), head \`6dd8c0000e710fc923e9d347123f78c17449ed7b\` | Unmerged; C06 v1.1 **candidate**, not Owner/Oracle-approved |
| Agent 2 PH07–PH12 work | [Draft PR #5](https://github.com/reallakshman19/Grade9v4.1/pull/5), head \`af3e403ba3acb93e2b13cbe15c60e06c8ee077d8\` | Unmerged; six lead packs, 83 subtopic inventory, incomplete chapters |
| \`main\` observed during onboarding | \`d9072732e4e3103e17d9d96678def2ce1d1cf377\` | Not assumed to contain any of the three draft workstreams |

**Important:** These are *snapshot* SHAs. Every new agent must record its own exact checkout SHA, remote, branch and diff before editing. The old \`Start_here.md\` describes a historical Windows workspace; do not mistake its locally described branch or checkout for the current remote state. The local \`CURRENT_CHECKPOINT.md\` and \`AGENTS.md\` must be read and reconciled rather than silently replaced.

### Actual coverage versus aspirational scope

- Agent 1 PH01–PH06 contains **49 proposed subtopics**. PH01 has a substantial reading-first candidate chapter, **3/8 PH01 subtopics** with nine *author-proposed* D3 QRT targets; five PH01 QRT subtopics remain. PH02–PH06 are inventoried, not authored as complete textbooks.
- Existing Agent 2 PH07–PH12 has **83 proposed subtopics**, six substantive lead construction packages, and continuous draft manuscripts for PH08 and PH10. **77 subtopics still lack authored lead packs**. It has no qualified, learner-ready Core1B browser journeys across those six topics.
- The aggregate **132 candidate subtopics** is a planning count (49+83), *not* an official chapter inventory, verified syllabus completeness, 132 approved modules, or an indication of authentic exam-question coverage.

### Existing authority that shall not be overwritten

1. \`AGENTS.md\`, \`Start_here.md\`, \`CURRENT_CHECKPOINT.md\`, \`docs/product-scope.md\`, \`architecture/guidebook.html\`, and the actual native Core1A/B/QRT and source-custody guidance. Follow the repository instruction hierarchy and report unavailable prerequisites.
2. [Shared 28 QRT templates](https://github.com/reallakshman19/Grade9v3.5/blob/574c7fe2/Shared/quality/question-demand-templates.v1.json), source-repository SHA \`574c7fe2\`, Git blob \`e2409aef11ae7d98444593bfbe1a38eb00c97cef\`. Seven canonical cognitive operations × four bands.
3. [Physics Blueprint](https://github.com/reallakshman19/Grade9v4.1/blob/main/templates/physics-blueprint/physics-blueprint.D3-D4.json) v0.2.0, blob \`700dafcbe86d76442637bcf214eeb544497cf4ea\`; **\`DRAFT_OWNER_REVIEW\`**. It defines the 14 Physics D3/D4 cells. The D3.1 subtile remains **PAUSED**.
4. Original [candidate C01–C08 v1](https://github.com/reallakshman19/Grade9v4.1/blob/feat/nsejs-physics-core-contracts-c01-c08-r1/nsejs/physics/curriculum/contracts/core-contracts.v1.json), v1.0.0.
5. [C06 v1.1 amendment](https://github.com/reallakshman19/Grade9v4.1/blob/feat/nsejs-physics-agent1-ph01-kinematics-r1/nsejs/physics/curriculum/contracts/core-contracts.v1_1.json), v1.1.0, only on Draft PR #3, **proposed** until Owner/Oracle review. The v1 validator and fixtures must continue to work.
6. WPE selected canonical Topic Adapter is **UNSELECTED**; prior WEP candidate data and v1 identities are not disposable. D1/D2 common Blueprint remains **\`SPEC_PENDING\`**.
7. The existing source-custody and academic status ledgers are prior evidence, not a blanket source approval. Zero authentic questions may be promoted by copying source-claimed metadata.

## 1. Operating model: multiple authors, separate reviewers, one release authority

### 1.1 Authoring agents and exact domains

| Workpack | Agent role | Exclusive content ownership | Starting basis | Constraints |
|---|---|---|---|---|
| **A01** | PH01 completion author | PH01-M01/M02/M04/M06/M08 plus quality repair of PH01-M03/M05/M07 | PR #3 exact head | Preserve old PH01 IDs and immutable revision-bound attempts |
| **A02** | Mechanics author | PH02 Forces/Newton and PH03 Momentum/Collisions | PR #3 exact head | May reference PH01 laws; not edit PH01 |
| **A03** | WPE custodian/author | PH04 Work/Energy/Power | PR #3 exact head | Authentic WPE adapter/lineage must be reconciled first |
| **A04** | Gravitation/Fluids author | PH05 Gravitation and PH06 Fluids | PR #3 exact head | Explicit extension HOLD for advanced fluids |
| **B01** | Thermal/Sound author | PH07 Heat and PH08 Sound/Waves | PR #5 exact head **only after Owner transfers Agent 2 subownership** | Preserve PH08 continuous manuscript and evidence |
| **B02** | Optics author | PH09 Mirrors and PH10 Lenses/Eye | PR #5 exact head **only after transfer** | Preserve PH10 continuous manuscript and historical optics identities |
| **B03** | Electrical/Magnetism author | PH11 Circuits and PH12 Magnetism/Induction | PR #5 exact head **only after transfer** | Preserve the existing candidate Core2/skills source status |
| **P00** | Platform/runtime engineer | Reusable Core1B builder/runtime, schema compatibility, tests and integration adapters | Separate Owner-assigned integration branch | No independent scientific claims or chapter ownership |
| **R00** | ChatGPT / technical reviewer | Read-only PR inspection, conformance, regression and integration recommendations | Exact candidate PR heads | **No new chapter code**, no self-approval or blind-review claim |
| **R01** | Independent academic/Physics/QRT reviewer | Exact-task scientific/source/QRT and B1–B7 review | Source-only intake when a blind review is intended | Must not be exposed to author-proposed answers/labels before blind assessment |
| **Owner** | Final authority | Assignments, contract adoption, merge and deployment decisions | Exact-head review returns | Only Owner authorizes merge/publication |

For **PH07–PH12**, existing Agent 2 remains the owner of PR #5 until the Owner expressly authorizes delegation to B01/B02/B03. In the absence of transfer, B01/B02/B03 are **reserved tasks** and must not write overlapping files. Original agent names may be retained as schema labels \`AGENT_1\` and \`AGENT_2\`; the subagent workpack ID travels in task metadata and commit/PR evidence. Do not expand an enum merely to record a subcontractor.

### 1.2 Reviewer independence

R00 previously authored the PH01 candidate and C06 v1.1 interface. Consequently **R00 is author-exposed**, not a cold independent reviewer for PH01/C06. R00 can review semantics, code, exact diffs, links, coverage consistency and failing cases, and request fixes. Only separately assigned R01 reviewers may render an **independent** Physics/QRT/B1–B7 finding. Neither R00 nor an author can issue an approval receipt impersonating R01.

### 1.3 Git and conflict rules

- A01–A04 use a fresh branch pinned from the exact PR #3 workstream commit, and open **stacked Draft PRs against the designated PR #3 branch**, not directly against a changing \`main\`, until the Owner selects a new integration base.
- B01–B03, **after delegation**, branch from the agreed PR #5 head and target that workstream's branch. Agent 2 is the coordinator for their files until ownership transfer is explicit.
- P00 receives an independent integration branch and **may not rewrite author manuscripts or unilaterally change C01–C08, Shared QRT, Physics Blueprint, source-custody gates or native reviewer decisions**.
- An agent writes its own PHxx topic paths, own fixtures/tests and own task notes. Root navigation, global style, shared validators, contract schemas, other agents' topic packages and \`main\` are **read-only** absent a separate approved integration task.
- Do not use stale locally checked-out \`main\` or PR references without recording the new HEAD SHA and a git diff. Never force-push another agent's branch, resolve a merge conflict by discarding content, or count an unmerged PR as deployed.
- Whenever C06 v1.1 adoption is undecided: Author **v1-compatible content on the assigned branch** and document the proposed v1.1 MAIN instances separately, or use v1.1 within the PR #3-based candidate workstream with an explicit dependency. **Do not silently migrate PR #5 v1 packages to v1.1.**
- Cross-agent science dependencies use canonical ID references and independent semantic diffs; copy-pasting the same physical law under inconsistent sign conventions is prohibited.

## 2. Required agent intake — preflight before authoring

Each author MUST submit a small baseline note covering:

1. Assigned task ID, agent workpack, topic IDs, exact Git branch/commit, parent/base SHA, candidate contract version, subject Blueprint version/blob, Shared 28-QRT source/blob, adapter version and selected source status.
2. The relevant \`AGENTS.md\`, \`Start_here.md\`, \`CURRENT_CHECKPOINT.md\`, \`docs/product-scope.md\`, \`architecture/guidebook.html\`, \`docs/agent-entry/03-blueprint-adapters.md\`, and actual C01–C08 README/schema/validator were read; report any unavailable master spec or missing local source custody as HOLD.
3. Every candidate subtopic in the allocated inventory, its current official curriculum/source reference, and accurate status \`PUBLISHED_ORIGINAL\` / \`AUTHOR_EXPOSED_CANDIDATE\` / \`METADATA_ONLY\` / \`NOT_AUTHORED\` / \`SOURCE_HOLD\` (these are reporting categories, not arbitrary changes to native schemas).
4. Current tests, authored manuscript paths, source/figure availability, unused or duplicate QRT identifiers, and pending upstream dependencies.
5. Risks, collisions with another open PR, and what will not be touched.
6. Proposed *first bounded slice* with falsifiable success conditions.

Do not begin by claiming a chapter is complete because it has an HTML page, a legacy 45-module name, a JSON metadata row or an old source-authentication label. Reconcile actual content and original exam source identities separately.

## 3. C01–C08 authoring interface

| Contract | Mandatory agent implementation | Mechanical boundary | Academic/source boundary |
|---|---|---|---|
| **C01 Syllabus** | Stable PHxx/subtopic IDs; scope role; source locator; lower-grade prerequisites; topic coverage register | No missing IDs, duplicate subtopics, improper cross-topic IDs | A candidate scope is not an authenticated official syllabus line |
| **C02 Physics law/warrant** | Canonical science references; laws, derivations, applicability, sign/units, uncertainty and model limits | All references resolve and laws retain stated preconditions | Independent scientific correctness is not inferred |
| **C03 QRT binding** | Exact task UID; ONE primary cognitive operation; candidate D3/D4 cell; five factor scores+evidence; protected decision W; shortest valid reasoning route | Correct operation-to-cell mapping and scores | An author cannot award itself an independent cognitive demand |
| **C04 Topic Adapter** | Versioned PHYS-TOPIC-PHxx; scientific/model/figure/misconception references; per-cell instance IDs; semantic diff | No missing/cross-cell/dangling instances | Cannot redefine Shared 28 QRT operation or band policy |
| **C05 Core1A textbook** | Continuous chapter with scientific phenomenon, intuition, rigorous narrative, derivations, diagrams, model limits, examples, misconception repair and exits | Well-formed authored package and linked figures | Field presence/word count is not B3 teaching sufficiency |
| **C06 Core1B** | Fresh MAIN and INSTANCE tasks, six-stage journey, protected first attempt, hints, repairs, boundary transfer and source return | Revision/persistence/state/link checks | B4/B5/B6 mastery and true novelty still require independent review |
| **C07 Core2 source** | Exact question UID/digest, paper code, figure/key/source role and scoped source status; separate authored transfers | Exact binding and source-role checks | No candidate becomes authentic exam evidence from metadata alone |
| **C08 QA/release** | B1–B7 and seven separate noncompensatory gates, exact-head test receipts, screen/browser evidence, explicit release HOLD | Valid QA receipts, versions and regression runs | Mechanical PASS does not confer academic or Owner release approval |

### 3.1 Canonical QRT method

Seven operations in order: \`RETRIEVE\`, \`EXPLAIN\`, \`APPLY\`, \`MODEL\`, \`REPRESENT\`, \`SYNTHESIZE\`, \`JUSTIFY\`. There are 28 shared templates (seven operations × D1–D4) and 14 candidate Physics D3/D4 cells (D3.1–D3.7, D4.1–D4.7). **D3.1 remains paused**.

A task is **one primary operation only** and is evaluated on five separately evidenced 0–2 factors: concept/model selection, representation translation, reasoning-chain length, algebra/computational load, and trap/exception sensitivity. Under the *current draft calibration*, total 6–7 is a D3 candidate and 8–10 a D4 candidate. Those bands are **not academic verdicts**. A D4 label is not warranted merely by length, additional arithmetic, a novel context or multiple-choice format.

Each substantive subtopic targets **three distinct defensible QRT operations** (not merely three difficulty-level headings). If forcing a third operation or D4 creates a false scientific task, record an evidence-backed exception/HOLD instead. The Owner/reviewer decides disposition; no fabricated coverage.

### 3.2 Core1A: minimum instructional substance

A Core1A chapter is **student-facing self-learning textbook content**, not a sequence of worked exam stems, hints or answer keys. The learner should be able to read it from the beginning without having seen the associated NSEJS source question.

Every scientific subtopic must provide:

- A motivating real-world phenomenon, scientific observation or simple experimental setup;
- What is measured/assumed, what a law claims, a clear derivation or physical justification, and a statement of what would invalidate the model;
- Multiple representations when meaningful (diagram, position/force/optics/circuit sketch, signed graph, table, physical experiment), each with useful captions/alt text and scientific axes/units;
- Prerequisite bridges before the advanced task; textbook tiers \`FOUNDATION\`, \`CONNECTED\`, \`ADVANCED\` for progressive worked examples. These tiers are **not approved D1/D2/D3 demand classifications**;
- A plausible wrong model, a counterexample/diagnostic, and a repair with a defensible scientific warrant;
- Independent-looking chapter synthesis and a check of units, limiting cases and feasibility;
- Figures original or licensed for public use; confidential exam scans and key images excluded from public Git.

A chapter completion record must link its **full text**, figured scene specifications, scientific library entries, relevant QRT instances, Core1A teaching tests and science-source evidence. The existence of a heading or JSON teaching stub is not sufficient.

### 3.3 Core1B: protected six-stage learning journey

The learner flow is:

\`Predict → Attempt → Reconstruct → Diagnose → Repair → Boundary Test\`

- **Predict:** commit an initial sign/model/physical expectation before hints;
- **Attempt:** save a genuine first solution; include the chosen physical model and justification;
- **Reconstruct:** after the protected first save, compare with an explicit, correct physical route;
- **Diagnose:** locate the first divergence without auto-assigning a misconception from a score alone;
- **Repair:** revise the decisive model or representation, preserving the immutable original;
- **Boundary Test:** solve a *changed-condition* problem independently before revealing the model.

H1/H2/H3 correspond to clarify/correlate/open-the-way; protect the decisive work **W**. S1/S2/S3 visuals, where used, must similarly support observation/relationship/construction without revealing W. Distinguish \`FIRST_ATTEMPT_INDEPENDENT\` from helped, returned-from-textbook and revised work; do not count all correct final answers as mastery.

Candidate **C06 v1.1** additionally requires **one integrated MAIN per filled cell**, combining **at least two distinct topic subtopic instances** and listing **every bound instance** for that cell; each instance has its own fresh INSTANCE cycle. A MAIN containing two variants of the *same* subtopic is not the required cross-instance synthesis. The legacy v1 schema does not enforce this structure; do not assert v1 MAIN coverage equals v1.1 coverage.

For a learner runtime, require:
- Stable item/task UID and exact SHA-256 content revision binding;
- First prediction and first answer persisted **before** H1/H2/H3, reconstruction answer or boundary model unlock;
- Separate help-exposure events (including textbook/source return before first attempt), diagnosis notes, revised answers, boundary responses, and immutable original revision;
- Refresh/re-entry consistency, stale-content rejection, and a fail-closed response if storage fails; no fake success or automatic \`mastery_status: APPROVED\`;
- Keyboard and touch operation at **1000×1600 portrait** and **1600×1000 landscape** tablet test viewports; no page errors, unusable controls or horizontal overflow;
- No iframe and no unauthorized source-stem reproduction;
- Explicit distinction between candidate authoring state and real learner qualification. Browser behavior proves functionality, not cognitive mastery.

### 3.4 Core2 source custody

Maintain distinct evidence roles: \`DIRECT_EXAM_EVIDENCE\`, \`PREREQUISITE_BRIDGE\`, \`AUTHORED_TRANSFER\`. Original exam item identity requires paper/year/set/code/question/figure/key lineage and exact source digest plus an authorized review. A source-claimed 50-record corpus, the 95 Physics metadata rows, or the historical 16 Core1 construction ledger **must not** be silently reinterpreted as verified originals. Preserve the private paper/figure/key custody boundary.

## 4. File naming, isolation and deliverable contract

Within an agent's authorized PHxx scope, prefer the existing native locations and builders. Do not impose a new parallel application tree if one already exists:

\`\`\`text
nsejs/physics/
  curriculum/
    contracts/                    # Read-only to topic authors
    agent1/PH01/                  # Existing PH01 candidate, A01 edits only
    topics/PH07/ ... PH12/        # Existing Agent 2 candidate packs
    [topic-owned PH02–PH06 paths, conforming to selected builder]
  textbook/PH01/index.html        # Existing reading-first PH01 page
  core1/ph01-qrt-r2/index.html    # Existing PH01 browser candidate
  ...                             # New PHxx paths by designated owner only
tests/
  test_nsejs_physics_*.py         # Topic-scoped test filenames
tools/
  ...                             # Shared tools: P00 only, or approved change
\`\`\`

**Required return per PHxx topic** (use native paths, exact SHAs and formal schema):

1. \`PHxx_SYLLABUS_COVERAGE\`: exhaustive candidate subtopic registry with official/bridge/extension classification, source refs and uncovered items.
2. \`PHxx_SCIENCE_AND_FIGURE_CUSTODY\`: verified/candidate laws, assumptions, sign conventions, original/rights-verified figures and scientific HOLDs.
3. \`PHxx_TOPIC_ADAPTER\`: versioned native JSON, diff, operation-to-instance map and C06 migration status.
4. \`PHxx_CORE1A_TEXTBOOK\`: fully readable, navigable manuscript/page plus pedagogical lesson records; not a quiz alone.
5. \`PHxx_CORE1B\`: original task pack, main/instance references, H1/H2/H3, six-stage feedback, checked answers, changed-condition tasks and protected-W manifest.
6. \`PHxx_CORE2_MAP\`: source-authenticated QUID/role bindings or explicit \`NO_QUALIFIED_SOURCE_YET\`, not invented stems.
7. \`PHxx_QA_RECEIPT\`: commands/outputs on exact head, native schema checks, numerical/scientific cross-checks, real Chromium screenshots and regressions.
8. \`PHxx_REVIEW_REQUEST\`: B1–B7 candidate witness links, separate gates, known bugs, unresolved academic and source HOLD, and explicit Owner decision requested.

A PHxx title is **not complete** until all substantive subtopics are either authored and qualified by appropriate authority or expressly listed as outstanding; no global 12/12 completion claim from six sample lead packs.

### 4.1 PR template (mandatory)

\`\`\`text
Task ID / workpack:
Exact repository/head SHA and parent/base SHA:
Assigned topic paths touched:
Contract v1 or v1.1 and selected Blueprint/blob:
Syllabus inventory: total / authored narrative / QRT proposed / qualified:
Core1A changes, scientific derivations and figures:
Core1B MAIN + INSTANCE, protected W, hint/attempt rules:
Original-question/source roles; authentic-source HOLD count:
Actual commands and verbatim exact-head test results:
Real Chromium viewports and evidence artifact URLs:
Cross-topic impacts and migration / backward-compatibility:
Unresolved science/QRT/B1–B7/source rights/CI:
No academic approval inferred from software validation.
Release decision: HOLD. Merge/deployment: NOT AUTHORIZED.
\`\`\`

## 5. Development and review gates

| Gate | Builder must provide | R00 checks | Separate academic R01 / Owner decision |
|---|---|---|---|
| **G0** Baseline custody | Exact repo/branch/source SHA, owner/agent boundary, missing data and clean inventory | Base matches parent, no source leaks, no overlapped paths | Owner confirms assignment transfers |
| **G1** Science syllabus | Subtopics, prerequisites, laws, figure and syllabus references | Completeness-of-record, cross-topic IDs, numerical consistency flags | R01 source-scope + scientific accuracy |
| **G2** Core1A teaching | Full chapter, derivations, meaningful illustrations, conceptual and worked examples | Narrative continuity, correctness red flags, accessible layout | R01 B1/B2/B3/B7 |
| **G3** QRT | One primary operation, five factor evidence, protected W, independent transfer candidates | Cell IDs, task identity, scoring arithmetic, task/anchor nonidentity | Cold R01 independently determines operation and actual D-band |
| **G4** Core1B | Real MAIN/INSTANCE six stages, hints, exposures, persistent first attempts | Schema, exact runtime flow, accidental early answer leaks | R01 B4/B5/B6, correct changed-condition physics |
| **G5** Engineering | Tests, browser receipts, backward compatibility and no hidden regressions | CI exact head, tablet, keyboard, storage, stale revision and link return | Independent deployment/security owner where applicable |
| **G6** Release | Signed scoped approval evidence, clean PR diff and owner acceptance | Recommend HOLD/technical-ready, never self-merge | **Owner** authorizes merge/publication/deployment |

**B1–B7** remain separately scoped: B1 target, B2 construction signature, B3 Core1A sufficiency, B4 fresh reconstruction, B5 first-attempt protection, B6 diagnosis and condition transfer, B7 Physics and provenance. Seven gates above do not replace these witnesses. Each gate is noncompensatory: a PASS in another category cannot substitute for a HOLD.

### 5.1 Reviewer outcomes

R00 returns **\`TECHNICAL_PASS_PENDING_ACADEMIC\`**, **\`REQUEST_CHANGES\`**, or **\`HOLD_BLOCKER\`**, always tied to an exact SHA and a list of findings. These are review-report dispositions, not new native academic status enums.

Severity:
- **P0 / HOLD blocker:** scientific contradiction, leaked protected W/source, false source identity, bypassed first attempt, forged receipt, broken ownership, schema downgrade or unapproved release.
- **P1 / must fix before technical readiness:** incorrect example, broken stale revision, inaccessible keyboard flow, unreviewed adapter cross-reference, coverage overclaim, missing required evidence, failing exact-head tests.
- **P2 / follow-up in-scope:** editorial clarity, graph labels, additional examples, touch affordances, nonblocking presentation issues.

Agent authors implement fixes on their own branch; R00 reviews the diff **without authoring the patch**. For PH01/C06, a separate R01 academic review is mandatory because R00 participated in authoring their existing content.

## 6. Testing and reproducibility

Run from each exact agent checkout and retain verbatim output:

\`\`\`bash
python -m pip install -e ".[dev]"
python -m pytest -q
python nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py PATH_TO_TOPIC_PACKAGE.json
\`\`\`

For PH01 on its PR #3 baseline the existing specialized paths are:

\`\`\`bash
python tools/physics_textbook_browser_qa.py
python tools/physics_ph01_core1b_browser_qa.py
\`\`\`

Other topics must provide equivalent real HTTP Chromium regression coverage, not claim the PH01 screenshots test their pages. Also verify complete subject navigation, no iframes, exact topic/QRT/source routes, hints and storage disabled, refresh, keyboard, touch, portrait and landscape at 12.7-inch targets, and content revision invalidation.

Exact-head CI PASS is required for technical readiness, but **not sufficient** for academic, source, QRT, original-exam, learner mastery or publication approval. Synthetic fixtures are admissible for validator engineering only.

## 7. Specific inherited HOLDs and cross-agent constraints

1. **C06 v1.1** is a versioned candidate amendment on PR #3, not an approved central release. Agent 2 PR #5 still pins v1.0; migration requires a separately reviewed patch and tests.
2. **PH04/WPE:** source evidence, authentic original module/adapter custody, historical WEP IDs and QRT D3.1 pause are not waived. A03 must not invent a selected adapter.
3. **PH06/Fluids:** syllabus-core buoyancy/pressure versus extension fluid flow, surface tension and accelerating-fluid reasoning must be individually labelled and evidence-backed; no false full-fluid-syllabus status.
4. **PH07/Heat and PH12/Induction:** distinction between verified Class X and higher-level extensions, including formative-only curriculum status, must remain explicit.
5. **PH08/PH10 continuous drafts:** expand/reconcile existing manuscripts; do not replace them with short QRT solution pages or lose figure/source custody.
6. **Historical source originals:** source metadata or 16 Core1 construction identities are not upgraded by author-created substitutes; track authored transfer separately.
7. **D4:** no blanket requirement to produce an unsupported D4 in each subtopic. Build genuine advanced transfer and seek exact-task independent classification.
8. **Cross-topic prerequisites:** shared PH00/PH13 measurements/experiments, PH01 frames for PH02/PH05, PH04 energy for PH06/PH07, and PH08/PH09 wave optics bridges must be referenced, not multiply reauthored.
9. **Owner-local assets:** archives, scanned questions, figures and answer keys may exist in Git-excluded workspaces. Absence from GitHub means source-custody HOLD, not permission to fabricate or upload them.

## 8. Schedule and task sequencing (dependencies, not dates)

**Phase 0 — owner allocation:** Confirm A01–A04. If delegating PH07–PH12, the Owner explicitly reassigns subownership from existing Agent 2 to B01–B03; otherwise Agent 2 keeps those files. P00 and independent reviewers receive separate assignments.

**Phase 1 — independent, parallel source inventories:** All authorized authors submit accurate syllabus/coverage and source/figure identity maps. P00 inventories current Core1B native runtime and C06 v1/v1.1 gap; no shared changes before contract decision.

**Phase 2 — teaching-first pilots:** For each authorized workpack, finish one substantial textbook subtopic and all its prerequisite diagrams, explanations and model limits; reconcile its source record. R00 and R01 return targeted findings. Then expand through all assigned subtopics.

**Phase 3 — protected transfer:** Each author supplies candidate QRT tasks, cell instances, one integrated MAIN (where v1.1 is selected), fresh INSTANCE cycles and a complete hint/diagnosis/boundary solution. P00 supplies reusable runtime/QA wiring after interface adoption.

**Phase 4 — exact-head review:** R00 reviews branch diff, full QA and coverage ledger, then an unexposed R01 reviewer independently evaluates scientific/QRT/B1–B7 evidence. If FAIL/HOLD, send actionable findings to the owning author, not a silent rewrite.

**Phase 5 — integration recommendation:** Only Owner-selected versions are reconciled onto an integration candidate branch; run untouched full QA plus real browser journeys and a formal source/academic report. Owner decides whether to merge or publish. No automatic deployment.

## 9. Final acceptance dashboard definitions

| Metric | Count rule |
|---|---|
| \`inventory_subtopics\` | Exactly one stable, candidate subtopic ID in the current reconciled syllabus |
| \`core1a_authored\` | Subtopic has substantive continuous teaching, derivation/warrant, figures where necessary and examples |
| \`core1a_qualified\` | Academic B3 and science/provenance reviews accepted for exact revision |
| \`qrt_candidate_targets\` | Exact task with primary operation, evidence and protected W authored; **not approved** |
| \`qrt_independently_qualified\` | Independent exact-task QRT reviewer returns source-scoped acceptance |
| \`core1b_specified\` | Complete MAIN/INSTANCE six-stage source, not a functioning learner page |
| \`core1b_runtime_tested\` | Real HTTP Chromium journey successfully exercises first answer, help/revision and changed-condition controls |
| \`core1b_academically_qualified\` | B4/B5/B6 and independent Physics validation accepted for exact revision |
| \`authentic_core2_qualified\` | Verified direct exam source and key/figure custody; authored practice excluded |
| \`owner_released\` | Explicit Owner authorization after noncompensatory gates; **not** a passing CI check |

**Never report 12/12 topics completed, 132/132 qualified, 28/28 QRTs filled, 14/14 advanced Physics cells qualified or a percentage of examination coverage without stating the denominator, exact provenance and separate candidate/qualified counts.**

## 10. Stop-work triggers and handoff format

Stop only the affected construction and return a bounded HOLD when an external source is missing, Physics law contradicts another verified source, a required adapter variant is unselected, two agents edit the same topic, a hidden answer appears before protected first attempt, a QRT cell or D-band cannot be justified, or a test fails. Continue unaffected, independent subtopics if safe to do so.

Every author handoff ends with:

\`\`\`text
TASK:
OWNER / DELEGATED WORKPACK:
REPO, BRANCH, EXACT HEAD, BASE:
TOPIC IDs, SUBTOPIC INVENTORY / AUTHORING / QUALIFIED COUNTS:
CONTRACTS + BLUEPRINT + ADAPTER EXACT VERSION/BLOB:
FILES ADDED / CHANGED:
PHYSICS SCIENCE / FIGURE / SOURCE EVIDENCE:
CORE1A NARRATIVE + MEASURABLE TEACHING EVIDENCE:
QRT TASK IDs, PRIMARY OPERATIONS, D3/D4 EVIDENCE, W:
CORE1B MAIN / INSTANCE COUNTS, PROTECTION + HINTS:
AUTHENTIC CORE2 BINDINGS / SOURCE HOLD:
EXACT PYTHON + CHROMIUM COMMANDS, RESULTS + ARTIFACT URLS:
B1–B7 and seven independent gate statuses:
OPEN DEFECTS AND CROSS-AGENT DEPENDENCIES:
REVIEW REQUEST (R00 / R01):
OWNER MERGE AND RELEASE AUTHORITY: NOT REQUESTED / HOLD
"No academic approval inferred from software validation."
\`\`\`

### Final instruction to every agent

**Build genuine, scientifically grounded Core1A textbook teaching and truly fresh Core1B learner-owned reasoning, not a large set of renamed exam solutions.** Reuse the actual 28-QRT/14-Physics-cell contracts, preserve source custody, report candidate-versus-qualified coverage exactly, and leave the academic and release decisions to independent reviewers and the Owner.

---
**Repository status:** Spec is an onboarding **proposal**. All content PRs are separate, draft, and unmerged; this document itself grants no permission to merge or deploy.


## Binding R2 production addendum — supersedes weak self-check and per-item Owner approval language

The stronger [Evidence-Bound Core1A/Core1B/Core2 Authoring Contract R2](quality-gate-r2/AUTHORING_QUALITY_CONTRACT_R2.md), [strict packet template](quality-gate-r2/EVIDENCE_PACKET.template.json), [validator](quality-gate-r2/verify_evidence_packet.py) and [independent review + one-time Golden Sample forms](quality-gate-r2/REVIEWER_AND_GOLDEN_TEMPLATES.md) supersede any weaker R1 author-completion implication **once the Owner approves the first Golden Sample and adopts the contract**.

Owner acceptance is required **once for the Golden Sample standard**, not separately for each later question. Subsequent work requires every-item evidence packets, fail-closed automatic checks, red-team science/transfer witnesses, delegated risk-based independent batch review, and cross-checked exact artifact SHAs. This addendum does not auto-approve academic content, does not alter older PRs, and does not itself activate GitHub branch protection. A passing evidence validator only establishes a mechanically grounded candidate; true science, QRT and B1–B7 remain reviewer responsibilities. Redistribution-rights assessment is outside this educational quality addendum.

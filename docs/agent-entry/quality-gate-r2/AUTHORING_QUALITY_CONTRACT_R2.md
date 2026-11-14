# NSEJS Physics — Evidence-Bound Core1A/Core1B/Core2 Authoring Contract R2

**Task ID:** G9V41-PHYS-CORE1AB-CORE2-QUALITY-GATE-R2  
**Parent:** [Multi-Agent Technical Specification R1](../nsejs-physics-core1ab-multiagent-technical-spec-r1.md)  
**Authority:** Owner selects and signs off **one representative Golden Sample**, then delegates routine authoring and batch review. **No Owner approval for every question**.  
**Status:** GOVERNANCE_PROPOSAL · NOT_A_PROMOTION · SAMPLE_NOT_SELECTED  
**Scope:** Physics only; first sample Core2 + complete Core1A + fresh Core1B, then repeat across authorized workpacks.  
**Out of scope for this quality protocol:** redistribution-rights assessment; topics and sources are still subject to science, identity and authenticity requirements.

## Zero-tolerance principle

> **An agent cannot prove that a learner understands science by completing fields, adding three hints, recording six stage headings, quoting a test count, generating a figure or awarding itself a D-band.** Those are necessary evidence surfaces, not the conclusion.

Release is a **conjunction of independent gates**. An author cannot satisfy an absent science warrant by adding more prose; cannot replace a missing figure with alt text; cannot replace a genuine changed-condition test by new numbers; and cannot replace a failed first-attempt witness by a green Python CI.

### The permitted lifecycle

\`OWNER_SELECTED_GOLDEN → GOLDEN_AUTHOR_DRAFT → AUTHOR_SELF_FALSIFICATION → R00_TECHNICAL_AUDIT → R01_ACADEMIC_AND_QRT_AUDIT → OWNER_ACCEPTS_GOLDEN_ONCE → VERSIONED_FACTORY_MODE → BATCH_REVIEW_AND_DELIVER\`.

Until Golden acceptance: **DRAFT/HOLD**, never automatic promotion. After acceptance, each item carries a **version-bound machine evidence packet and author audit**, with independent **R00/R01 batch checks**, not repeated Owner signatures. If a new algorithm, C06 semantics, QRT calibration, exemplar solution pattern or science assumption breaks the accepted reference: stop affected batch and seek a fresh *scoped* standard update. Keep old attempts attached to old content revisions.

### Reference counterexamples drawn from observed failures

- A Core1A buoyancy explanation had \`∂P/∂y=-(g+a)\` missing density. A dimension check requires pressure gradient in Pa/m, so a copied formula is rejected **even if its numeric worked example seems reasonable**.
- An optics Core1A presented virtually the same lens-placement task as Core1B with different values. New numbers are **not** new cognition.
- Some pages displayed \`{Reviewed} · Peer-Audited Module\` although canonical underlying exam questions remained \`NOT_ADMITTED\`. **Author badges are not audit certificates.**
- A Core2 reader made all hints visible pre-commitment, displayed feedback after a failed save, and deleted original attempts on Retry. A rendered working button is **not** B5 attempt integrity.
- A question stem with a missing figure was displayed without its \`[FIG]\` placeholder. A vanished visual clue is not source fidelity.

These are **required negative-control families** below, not merely illustrative anecdotes.

## 1. Submission is a packet, not a confident summary

For **each delivered subtopic/operation** (golden or batch item), an author MUST check in a packet following [EVIDENCE_PACKET.template.json](EVIDENCE_PACKET.template.json) and [evidence-packet.schema.json](evidence-packet.schema.json). Preferred repository folder for future production packets is \`review/quality-packets/physics/PHxx/\`, using stable item UID and content revision. No package is "done" based on chat text or an agent's completion statement.

Every evidence entry has:

| Required field | What reviewer can check |
|---|---|
| **id / role** | Which concrete scientific or behavioral claim it supports, from the locked role vocabulary |
| **path** | Actual repository-relative artifact path, never a fabricated link or unpublished filename |
| **sha256** | Exact SHA-256 of that file's UTF-8 bytes |
| **start_line / end_line** | Smallest relevant line interval in the pinned file |
| **excerpt** | **Verbatim passage** from those lines; no paraphrase or invented quote |
| **claim** | Falsifiable statement, not "works great" or "scientifically correct" |
| **why_this_proves_claim** | Physical warrant or demonstrable behavior; not an empty PASS badge |

A validator recomputes hashes, verifies quotations against the line intervals, checks referential roles, rejects duplication and ensures separate learning/runtime/source materials actually exist. An evidence packet that fails one check **cannot become technically ready**.

**Critical limitation:** a matching hash proves *which* text is inspected, **not** that the science is correct. That requires the science and transfer audits below.

## 2. Core1A — complete teaching requirement (B1/B2/B3/B7)

The **learner-facing** page must be a continuous, readable explanation that can be understood **before** seeing the corresponding Core2 item or its solution.

### Mandatory teaching units and evidence binding

| Unit | Non-negotiable explanation and evidence | Quick falsifier |
|---|---|---|
| **A1 Phenomenon** | Describe actual observable behavior, chosen variables and why this concept is needed | Can the text be pasted into another topic unchanged? If yes, reject generic filler |
| **A2 Prerequisites** | Teach missing earlier-grade concepts before advanced constructions | Give it to a cold learner with no prior exam solution; record first unexplained symbol |
| **A3 Mechanism** | Physical cause or conceptual model before algebra; explain **why**, not only **which formula** | Remove equations: can student still explain the phenomenon? |
| **A4 Warrant** | Derive law/relationship from valid assumptions; identify reference frame, sign convention, units and domain | Flip sign, use wrong dimension or out-of-domain limit; explanation must identify failure |
| **A5 Figures** | Authored/verified scientific figure with meaningful geometry, axes, labels, physical quantities and caption; representation is consistent with model | Remove/flip a critical arrow or swap lens directions; the answer must change or become unanswerable |
| **A6 Progressive anchors** | FOUNDATION, CONNECTED, ADVANCED **distinct worked examples**, each increasing reasoning complexity, with complete steps and checks | Do all differ only in numerical parameters? Reject |
| **A7 Misconception** | Present a plausible *specific* wrong model, demonstrate its failure and repair the **first wrong inference** | Does the text merely say "avoid common mistakes"? Reject |
| **A8 Counterexample** | A changed assumption/boundary where the shortcut stops working; predict and verify | Can same formula be used without noticing the changed condition? Reject |
| **A9 Synthesis** | New conceptual summary plus an unassisted challenge with an explanation of success and failure, not recycled anchor | The check duplicates the just-worked answer: reject |

Require nine distinct anchor role references in the packet. For a subtopic which intrinsically lacks one kind of illustration, the author may submit an explicit **exception request** to reviewer; do **not** silently skip the diagram or create a meaningless placeholder.

**Mechanical floor (not a definition of excellence):** a subtopic consisting only of a formula box, one worked problem and one exit check is automatically **P1 insufficient**. Word count and the presence of headings can only reject a too-thin page; they can never independently certify B3.

**Quality demonstration:** author must provide a learner-facing conceptual question, a complete model answer, and a counterfactual explanation **using concepts that the page actually taught**. A human reviewer must be able to reconstruct both without relying on the original source question. Do **not fabricate a real child/learner trial**; if no observed learners, label these as author-authored cold-review prompts.

## 3. Physics-specific self-check: five witnesses

The author must present **individually inspectable evidence**:

1. **Primary derivation** with variables, start law, assumptions, frame, steps, final result.
2. **Independent derivation/check** — a second proof, alternate representation, conservation check or direct substitution independent of the first algebraic path. "Verified twice" is not evidence.
3. **Dimensional and sign witness** for **each** new formula. State LHS/RHS units and sign basis. Include at least one unit-wrong mutation that is correctly rejected.
4. **Limit/model validity**: analyze at least two relevant limits or edge cases where possible (e.g. zero acceleration, equal masses, optical conjugate coincidence) and identify regimes where model breaks.
5. **Counterexample** to one tempting false generalization, with explicit physical reason and a numeric/symbolic demonstration.

For each original diagram, require figure intent, physical coordinate definitions and a **figure mutation** showing what label/arrow/scale change would mislead the student. An SVG existing in the folder is not enough. Where diagrams support quantitative inference, their geometric relationships must be scientifically faithful; explicitly schematic artwork must never imply a false scale.

**Reviewer science rubric** (separate from any author verdict):

| Dimension | 0 — reject | 1 — repair | 2 — acceptable | 3 — excellent |
|---|---|---|---|---|
| Law/assumption fidelity | Wrong law or missing model validity | Partially justified | Correct, scoped | Correct, independently derived and stress-tested |
| Causal teaching | Formula/answer only | Examples without mechanism | Clear mechanism and prerequisites | Transfers through multiple representations |
| Representation | Missing/misleading visual | Decorative or incompletely labelled | Scientifically accurate and helpful | Enables an inference unavailable from prose alone |
| Wrong-model diagnosis | Generic warning or absent | Identifies error after solution | Explains *first wrong inference* and repair | Learner can distinguish competing models before solving |
| Scientific checking | No units/sign/limit | One superficial check | Independent check + relevant limits | Counterexample + robust independent cross-check |

**Noncompensatory rule:** any 0 is **HOLD**; any 1 is **REQUEST_CHANGES**, regardless of high scores elsewhere. No average score may mask an incorrect equation.

## 4. Core1B — freshness is proven, not asserted (B4/B5/B6)

Every QRT **INSTANCE** and integrated **MAIN** is a fresh six-stage problem:

\`Predict → Independent Attempt → Reconstruct → Diagnose → Repair → Changed-Condition Boundary\`.

### Mandatory two-column anchor/transfer comparison

| Field | Core1A worked anchor | Core1B fresh task |
|---|---|---|
| Scenario + student-visible givens | Actual text and file locator | Actual new text and file locator |
| Decisive cognitive work **W** | What must be chosen/derived | What must now be chosen/derived |
| Model and assumptions | Model needed | Material difference in model/constraints |
| Representation | Diagram/table/equations | New translation or inference |
| Shortest correct path | Fully solved by author | Independently solved by author |
| Counterexample | How a shortcut fails | Which shortcut the learner must reject |
| QRT primary operation/five factors | Author candidate, not approval | Independent QRT review still required |

**Automatic rejection:** same problem after deleting numerical constants, units or labels. **Human rejection:** same crucial formula/proof with only cosmetic words changed. A different *context* is not enough. The author must demonstrate a changed model selection, inverse constraint, genuinely different assumption, multistage boundary, representation transfer or counterexample proof.

C06 v1.1 (if selected) requires **exactly one MAIN per QRT cell**, joining at least two distinct subtopic instances and actually demanding their combined inference. A list of multiple subtopic IDs alone does **not** prove meaningful integration.

### Protected learner evidence

- Predict and initial reasoning recorded before hints or reconstruction.
- First answer is immutable; future attempts are **new revisions**, and each revision links to exact content SHA-256.
- H1/H2/H3 have *different roles*: H1 names the observation, H2 highlights a relationship, H3 opens a valid route **without giving W or a disguised final equation**.
- Opening the textbook, source solution, key, diagram clue or hint before first commitment creates an exposure record; helped answers are not independent demonstrations.
- Reconstruction is the full, correct scientific path and is hidden until persistence **succeeds**.
- Diagnose identifies the **first wrong model**, not just an incorrect final number.
- Repair is kept separately. Boundary test must make the learner respond **before** boundary answer is shown.
- Storage disabled / stale content / back navigation / concurrent attempt failure are checked **fail-closed**, not silently reset.
- Retry **never deletes the first saved attempt**; it creates a linked fresh revision.
- Work is **not** graded as mastery merely because a final numerical answer matches.

### Required Core1B adversarial checks

(1) Numeric-copy clone must be rejected; (2) a hint containing W must be caught; (3) help before first answer must be recorded and not counted independent; (4) blocked storage must never reveal solution; (5) stale hash cannot restore attempts under new content; (6) Reset preserves first attempt; (7) QRT cell IDs and per-MAIN memberships survive cross-topic integration.

A **single happy-path browser screenshot is not a valid receipt**.

## 5. Core2 — complete reader, not a formatted answer bank

Per question, require actual question stem/options/type/conditions, independent correct key derivation, figure-dependent inference, stable UID and revision, original-source role, and honest source state. Candidates that lack an authenticated original remain **AUTHORED_TRANSFER** or **DIRECT_EXAM_CANDIDATE**; author's metadata cannot promote to authenticated exam status.

The UI must show the needed figure (or explicit figure HOLD), not silently remove \`[FIG]\` placeholders. Source labels should be generated from canonical status data, **never hardcoded to \`{Reviewed}\` or \`Peer-Audited Module\`**.

A question must offer:
- Precommit: stem, conditions, relevant figure and enough room for model choice. No key, solution, decisive equation or all-three-hint leak.
- Commitment: exact first response plus status, timestamp, question revision and exposure state. If the storage write fails, **do not reveal correctness or solution**.
- Postcommit: correctness feedback and a full explanatory derivation with diagram/units/limits, not just key letter.
- Requested help and error-specific explanation, with no fake automated diagnosis.
- Retry as a **new linked attempt** that does not destroy prior evidence.
- Traceable return to its corresponding Core1A/B targets, or honest \`NO_QUALIFIED_ROUTE\`.

A paper/key locator cross-check does not prove exact stem/figure/option fidelity. Question-level evidence must keep source authentication distinct from authored practice.

## 6. Self-falsification must precede the agent's completion message

An agent's "I checked everything" is inadmissible. It must provide mutations which should fail with a **real command and observed failure log**.

| Mutation ID | Fault deliberately introduced | Correct failure |
|---|---|---|
| \`WRONG_DIMENSION\` | Remove mass/density, misuse pressure gradient or convert wrong unit | Physics witness rejects |
| \`WRONG_SIGN_OR_LIMIT\` | Reverse frame axis, change limiting case or apply formula outside domain | Science check rejects |
| \`NUMERIC_CLONE\` | Copy Core1A worked example into Core1B with changed numbers | Freshness check rejects |
| \`HINT_LEAK\` | Put full W/equation in H2 or reveal before first save | Hint reviewer/runtime blocks |
| \`BAD_SOURCE_FIGURE\` | Remove/flip required graph/force/optical figure | Figure/source check blocks |
| \`SAVE_FAILURE\` | Force localStorage write failure and click commit | No solution is revealed |
| \`STALE_REVISION\` | Edit problem content retaining prior attempt | Old attempt not re-used |
| \`FALSE_REVIEW_BADGE\` | Add \`{Reviewed}\` to unqualified page | Gate blocks badge |

Golden Sample: all **eight** fault families. Subsequent batch item: at least \`WRONG_DIMENSION\`, \`NUMERIC_CLONE\`, \`HINT_LEAK\` per item, plus inherited golden browser/state negative-suite **per batch** and any risk-triggered fault. An agent must supply **actual log artifacts** with exact head SHA; claimed FAIL/PASS text alone is not evidence. Mechanical validator verifies the log snippet exists, but reviewer checks that the test truly injected the asserted fault and failed for the right reason.

## 7. Gates and reviewer authority

| Gate | Author proof | Validator result | Independent reviewer |
|---|---|---|---|
| G0 source/lineage | Exact source/contract/topic/content identity | HASH + REF match | R00 exact head |
| G1 physics | Derivations, units, signs, counterexample, second check | Actual extracts exist | R01 academic |
| G2 Core1A | Nine substantive teaching units, novice test | Each role resolves | R01 B3 |
| G3 QRT | Primary operation, five factors, W and anchor comparison | Binding/clone control | Blind R01 cognitive decision |
| G4 Core1B | Six stages, three nonleaking hints, protected attempts, transfer | Actual runtime negative controls | R00/R01 |
| G5 Core2 | Complete task, key, figure, stem and source status | Full item data/custody | R01 source/physics |
| G6 browser | HTTP, both tablet orientations, refresh, keyboard, touch, source return, storage | Actual receipt SHA-bound | R00 |
| G7 integration | Clean diff, cross-task references, baseline compatibility, full Python suite | CI and coverage register | R00 |
| G8 production | Golden standard and delegated per-batch risk review | No unclosed HOLD | Owner *once for golden*; delegated reviewers for routine batches |

### R00/R01 duties

**R00** technical reviewer: independent file/hash audit, schema/line-match, exact-head CI, source-vs-claim, UI state, protected W leak checks, clone and coverage comparisons. R00 is **not** cold academic reviewer on PH01/C06 due to prior authorship.

**R01** independent Physics/QRT reviewer: takes a fresh unseen task attempt before reading authored solved route, independently derives the result, hunts for unit/sign/counterexample defects, verifies whether Core1A actually teaches the needed cognitive move and whether Core1B genuinely transfers it; returns B1–B7 evaluation. The R01 receipt is separate from the author's packet and must include its own source SHA and reviewer identity. Authors cannot author or alter R01 receipts.

**Owner**: selects a representative Golden Sample, signs its spec/reviewer outcome **one time**, and delegates bounded rollout. Re-review by Owner only when the approved standard materially changes or exceptional high-stakes scientific dispute arises. **No Owner signature on every question.**

### Batch risk sampling after Golden acceptance

- **100% automatic checks** of every new/changed item: schema, hashes/line excerpts, science/unit claims present, source status, QRT binding, figure references, candidate-only badges and protected first-attempt states.
- **100% targeted scientific review** of every new Physics law/model/assumption, changed-answer-key dispute, D4 proof, changed QRT-cell policy and all failed/warning items; do not treat a novel high-risk item as routine.
- **Routine D3/D2/D1 items:** minimum one independently inspected item per topic per batch and **at least 20% selected by a reproducible deterministic sample** (e.g. hash sorted by UID + immutable batch seed). Do not let authors pick only their easiest examples. Reviewers may increase sample on defect signals.
- **Stop/escalate:** one P0 conceptual/math error, source lie, protected-answer exposure or status promotion → affected batch HOLD and 100% same-family inspection; repeated P1 issues → halt author, require remedial golden sample.
- **No per-item Owner approval** after the accepted Golden standard, but reviewer signoffs, hold clearance and published dashboard must reflect actual sampled vs unreviewed status.

The risk-sampling arrangement is a proposed **production policy**, not yet implemented by this document. The Owner chooses the golden exemplar and sample protocol, then configures repository branch protection and independent reviewer permissions.

## 8. Reviewer challenge rubric and stopping conditions

Reviewer must **attempt to disprove** each author claim, not read the author's conclusion first:

1. Can the physical law be derived or independently calculated? Are dimensions and signs consistent?
2. Does a cold reader understand what is happening before formulas are used?
3. Can the reviewer reconstruct the hardest problem *from Core1A alone* without unseen implicit knowledge?
4. If the Core1B numbers are replaced with the anchor's, is the algorithm still identical? If so, is there any actual new inference?
5. Could H1/H2/H3 or diagram labels answer the task before a first attempt?
6. Would the wrong model produce a plausible result, and does the module expose why it fails?
7. Can the first saved attempt be recovered after refresh/reset and remain unmodified after corrections?
8. Does a missing figure change the ability to interpret the item?
9. Are all content paths, line excerpts, hashes, workflow receipts and source IDs independently retrievable?
10. Do all badges and final counts agree with true authorization and verified question-level records?

Reviewer decision is **\`REQUEST_CHANGES\`**, **\`HOLD_BLOCKER\`**, or **\`TECHNICAL_PASS_PENDING_ACADEMIC\`**. Never imply academic approval from this validator. No surrogate "100% complete" claim without denominator and exact artifact status.

## 9. How to run and report the packet gate

1. Copy \`EVIDENCE_PACKET.template.json\` to \`review/quality-packets/physics/PHxx/<task-uid>.packet.json\`.
2. Fill every placeholder and remove all **TEMPLATE** markers. The untouched template is **intentionally not valid**.
3. Create real evidence files in the assigned workpack: textbook, Core1B attempt page, Core2 question, numbered analysis and browser/negative-control logs. Compute SHA-256 over actual bytes and record the exact line ranges.
4. Run the unchanged full Python suite and actual HTTP Chromium; capture exact *content revision* head and log receipts. The later evidence-packet-only commit does not change source bytes but advances the PR head; reviewer checks both SHAs.
5. Run:
   \`\`\`bash
   python docs/agent-entry/quality-gate-r2/verify_evidence_packet.py review/quality-packets/physics/PHxx/<task-uid>.packet.json
   python -m pytest -q tests/test_physics_quality_gate_r2.py
   python -m pytest -q
   \`\`\`
6. Submit Draft PR with the packet and an item-count/coverage reconciliation table. R00 checks exact artifacts, R01 independently assesses scientific and QRT quality. The agent **must not** post self-approved academic receipts or reviewed badges.

The CLI's best possible success is **\`EVIDENCE_STRUCTURALLY_GROUNDED · academic_status=HOLD · review_required=true\`**. Its mechanical success is NOT the final acceptance; it simply makes evidence inspectable and falsifiable.

## 10. Binding production conditions

This R2 is an **add-on candidate standard** to existing C01–C08 and multi-agent R1, not a stealth rewrite of existing accepted work. It becomes binding on an individual agent/workpack only after the Owner's **first Golden Sample selection and contract adoption**. At adoption:

- Pin Golden Sample commit, schema/validator blob hashes, official reviewer register and risk-sampling seed.
- Add evidence-gate and coverage checks to required GitHub branch protection for designated production branches.
- Require every new Core1A/B/Core2 candidate PR or batch to contain its packets; fail the protected branch when any required item is missing.
- Keep legacy draft PRs grandfathered until their next formal integration attempt, at which point they submit packet evidence rather than self-promoting.
- Maintain separate author packet, independent reviewer receipts and Owner Golden acceptance record. No agent can write all three records.

**A "PASS" with no exact native evidence, no adversarial failures, or one genuinely wrong Physics law is not a PASS.** If true learner or independent human evidence is absent, state \`NOT_OBSERVED\`; never invent a student outcome.

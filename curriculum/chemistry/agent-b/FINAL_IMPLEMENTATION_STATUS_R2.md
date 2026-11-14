# Agent B NSEJS Chemistry C08–C14 — final authoring return R2

Task: G9V41-NSEJS-CHEM-B-C08-C14-R1
Disposition: AUTHORING_COMPLETE · TECHNICAL_QA_PASS · INDEPENDENT_REVIEW_DEFERRED · ACADEMIC_HOLD · NO_MERGE_OR_DEPLOY
Dependency: Agent A Stage 0/1 draft PR #1 pinned at 77d2bd63328c184598088bce6b9888fc8324cb4b.
Candidate: Agent B stacked draft PR #4; common schema and A-owned C01–C07 unchanged.

## Implemented, and explicitly not qualified

| Unit | Subtopics | Core1A words | Core1B six-stage cycles | Authored D3/D4 capstones |
|---|---:|---:|---:|---:|
| C08 Chemical Reactions and Energy | 6 | 3,254 | 18 | 2 |
| C09 Acids, Bases, Salts and Oxyacids | 6 | 2,692 | 18 | 12 |
| C10 Metals, Non-metals and Metallurgy | 6 | 3,044 | 18 | 2 |
| C11 Carbon and Organic Chemistry | 7 | 3,342 | 21 | 2 |
| C12 Gases and Chemical Analysis | 5 | 2,629 | 15 | 2 |
| C13 Redox and Volumetric Analysis | 5 | 2,459 | 15 | 2 |
| C14 Environmental and Applied Chemistry | 5 | 2,522 | 15 | 2 |
| TOTAL | 40 | 19,942 | 120 | 24 |

Counts are of written candidate material, not independently accepted teaching quality or official examination questions.

Every B-owned subtopic has a connected Core1A explanation (phenomenon, scientific model, multiple representations where useful, worked reasoning, misconception repair and boundary), three distinct QRT demand task bindings, and three completed Core1B six-stage source-distinct authored practice cycles. All 120 cycles include original Predict, Attempt, Reconstruct, Diagnose, Repair and Boundary tasks; post-commit model closure; H1/H2/H3; a revision-bound saved first attempt; and review states UNREVIEWED.

Seven unit reader packs are available at curriculum/chemistry/agent-b/learner/C08..C14.reader.v0.1.0.json. The candidate user-facing route is nsejs/chemistry/textbook/index.html?unit=C09 in the branch checkout under HTTP; it is NOT deployed or linked from the public main site. Eight original SVG scientific illustrations accompany the chapters. The browser interface protects against model-answer reveal before local first-attempt save; this is progressive disclosure, NOT cryptographic secrecy or a mastery certificate.

All QRT IDs are reused unchanged from the existing 28 canonical template identities, through Agent A's candidate Chemistry blueprint v0.1.0. There are 120 author-candidate bindings with 3 distinct primary operations per subtopic and 24 independently authored chapter-level D3/D4 prompts with post-attempt full worked answers and author-proposed five-factor score vectors. Independent band adjudication = ZERO; unsupported labels must be downgraded later rather than promoted by software.

## Official scope source mapping

Primary source map: curriculum/chemistry/agent-b/sources/C08-C14_PRIMARY_SCOPE_REGISTER_R2.json, 40/40 subtopics. Official IAPT/HBCSE gives junior science scope broadly through CBSE Class X. CBSE Class X 2026–27 Science Unit I covers reaction equations, acids/bases/salts, metals/nonmetals and carbon compounds; Class IX covers additional foundational mixtures/separation. C12 gas-analysis methods and C13 formal redox/titration contain explicit EXTENSION/ENRICHMENT; C14 is cross-disciplinary integration. C11.07 esterification is contextual enrichment beyond the Class X section's express 'properties and uses' wording for ethanol/ethanoic acid. These page/theme bindings are author research, not independent science or exact original-paper custody.

Authentic new NSEJS source questions verified = 0. Original exam figures and publisher/official keys validated = 0. Existing Core2 source files and identities were not edited.

## Verified technical evidence

Code-and-test head ff18379578b72d3e6bb201ee2da281067c25794c:
- Python QA run 43471710295: Python 3.11 355 passed, 1 skipped (dedicated Chromium suite), 1 warning; Python 3.12 355 passed, 1 skipped, 1 warning.
- Dedicated real HTTP Chromium run 43471710302: 25 tests PASS, covering 7 unit navigation paths, 12.7-inch landscape 1600×1000 and portrait 1000×1600, local-first-attempt save and refresh preservation, hint exposure, stale revision, disabled storage fail-close, keyboard focus and image loads.

Both results are software-only and verify that named code head, not automatically the new documentation-only heads.

## Separately deferred at Owner request

1. Independent scientific review and original-source figure/key academic qualification: PENDING, not counted as complete.
2. Agent A prerequisite canonical concept IDs / exact SHA reconciliation C01–C07: PENDING. B placeholder refs remain unresolved, with no duplicate common scientific truth.
3. Independent exact-task QRT primary operation and D3/D4 scoring for all 120 task cycles and 24 capstone challenges: PENDING.
4. Any release to students, academic claims, PR merge or deployment: NOT AUTHORIZED; draft remains unmerged.

No common Chemistry blueprint or shared Core contracts were modified to fit topic authoring. No confirmed shared blueprint gaps were masked by a local rule change.

## Review entrypoints

- Seven Core1A files: curriculum/chemistry/agent-b/textbook/C08..C14.core1a.md
- Seven Core1B files: curriculum/chemistry/agent-b/core1b/C08..C14.core1b.v0.1.0.json
- Seven topic adapters: curriculum/chemistry/adapters/C08..C14.v1.json
- QRT manifest: curriculum/chemistry/agent-b/qrt/D3D4_EVIDENCE_MANIFEST_R2.json
- Source map: curriculum/chemistry/agent-b/sources/C08-C14_PRIMARY_SCOPE_REGISTER_R2.json
- Browser tests: tests/test_nsejs_chemistry_agent_b_browser.py

Final claim: All assigned B-owned authoring content has been written and passed bounded technical checks; academically reviewed/qualified content is deliberately NOT claimed.

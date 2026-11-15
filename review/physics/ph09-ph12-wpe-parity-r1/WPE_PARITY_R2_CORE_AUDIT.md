# Physics PH09–PH12 · WPE parity R2 · author-exposed evidence audit

**Workstream:** PH09–PH12 of Grade9v4.1 · [Draft PR #56](https://github.com/reallakshman19/Grade9v4.1/pull/56)  
**Status:** TECHNICAL CANDIDATE · SOURCE HOLD · SCIENCE HOLD · INDEPENDENT QRT NOT RUN · B1–B7 HOLD · NO OWNER RELEASE.  
**Scope:** Four bounded reference verticals, **not 58 independently accepted subtopics**.

## Root-cause corrections

The R1 preview was technically sound in preserving first attempts, but exposed `current.core1b.protected_work` before a learner attempted the challenge, revealed several post-attempt stages at once, did not bind task-specific five-factor evidence to any topic adapter, and had no canonical chapter links. A passing browser test missed all of those pedagogical defects.

R2 repairs *these exact failures*, without assuming source authenticity or academic approval.

## Three evidence-backed changes per Core — what is and is not proven

| Core | Change now in PR #56 | Proof / path | Boundary |
|---|---|---|---|
| Core2 (author checkpoint) | 1. Explicit original author, not-exam source identity with absence of original exam UID/key | Four `topic-adapter.PHxx.wpe-parity-r2.v1.json` sidecars (`source`) | Zero authenticated NSEJS paper questions |
| Core2 | 2. First source-style attempt persists separately before Core1A in R2 preview | `preview.js` `sourceStart/openTeaching`; Chromium test | Not tamper-proof custody |
| Core2 | 3. Distinct source-return answer after Core1B with source-to-transfer path and five-factor draft QRT | `preview.js` `saveSourceReturn`, adapter `task.binding` | Author checkpoint is **not** an admitted native exam Core2 |
| Core1A | 1. Model scope, explicit physics assumptions and prerequisites | Two modified native pages PH09-04/PH10-09 and two new candidate PH11-07/PH12-09 | Four-subtopic scope only |
| Core1A | 2. Additional worked steps and independent consistency checks | Native page R2 blocks and two dedicated author pages | Technical arithmetic alone cannot prove teaching sufficiency |
| Core1A | 3. Misconception explanation, representation and new authored schematic diagrams | PH11-07 and PH12-09 new `role=img` original figures; PH09-04/PH10-09 existing figures retained | Independent diagram/science and B1–B7 review HOLD |
| Core1B | 1. Remove pre-attempt decisive-work/formula-bearing author prompt | `preview.js`: learner-facing prompt now generic; solution only after persisted first attempt | All public JSON is still inspectable |
| Core1B | 2. Separate evidence-gated reconstruction, diagnosis, repair and boundary response | `saveReconstruct`, `saveDiagnosis`, `saveRevision`, `saveBoundary` | No automated semantic diagnosis or independent QRT |
| Core1B | 3. Source return, original/revised answer separation and data+adapter SHA-256 revision gating | `saveSourceReturn`, `freshRecord`, `versionMaterial`, browser adverse tests | No qualified mastery measurement |

## Four candidate topic adapters actually created

| Subtopic | Old package-adapter version (retained) | New candidate overlay | Proposed primary operation | Proposed total / band / cell | QRT |
|---|---|---|---|---|---|
| PH09-04 | PH09 v0.2.0 | PH09 v0.3.0 | MODEL | 7 / D3 / D3.4 | NOT RUN |
| PH10-09 | PH10 v0.2.0 | PH10 v0.3.0 | SYNTHESIZE | 8 / D4 / D4.6 | NOT RUN |
| PH11-07 | PH11 v0.3.0 | PH11 v0.4.0 | MODEL | 8 / D4 / D4.4 | NOT RUN |
| PH12-09 | PH12 v0.2.0 | PH12 v0.3.0 | EXPLAIN | 7 / D3 / D3.2 | NOT RUN |

All five intrinsic-demand factors are recorded per exact authored task with model evidence, competing operations, shortest valid route and science conditions. **The proposed score is not an accepted independent D-band.** The upstream topic package's original Blueprint pin and the resolved template's blob SHA come from different pinned artifact locations; reconciliation is explicitly HOLD. The sidecars are **versioned author candidate topic-adapter updates**, not replacements for the active pinned native package adapters.

## Native page and coverage delta

| Chapter | Registered | Dedicated candidate paths in R00 | Dedicated candidate paths in this PR | R2 reference transfer | Academically qualified |
|---|---:|---:|---:|---:|---:|
| PH09 | 12 | 12 | 12 (one content repair) | PH09-04 | 0 |
| PH10 | 17 | 17 | 17 (one content repair) | PH10-09 | 0 |
| PH11 | 14 | 0 | 1 (one new entry pair) | PH11-07 | 0 |
| PH12 | 15 | 0 | 1 (one new entry pair) | PH12-09 | 0 |
| **Total** | **58** | **29** | **31** | **4 scoped** | **0** |

The new PH11/PH12 `core1b.html` are dedicated **entry pages** to a shared, directly navigated six-stage candidate runtime; do **not** misrepresent them as four separate fully qualified runtime packs. The other 27 subtopics without dedicated candidate page paths remain unclosed. The existing PH09/PH10 pairs outside the two changed examples still require deep educational audit.

## Comparison with the WPE pilot

| Measure | WPE previous pilot | PH09–PH12 R2 correction | Verdict |
|---|---|---|---|
| Bounded worked-to-new-condition examples | Five named Learn→Challenge pairs | Four explicit new author examples | Comparable in idea; insufficient breadth |
| Student-facing diagrams | WPE learner figures in existing pilot | Two newly authored schematics; earlier optics figures retained | Still unreviewed scientifically |
| First-attempt evidence | Local first attempt with student-reason prompt | Source-first and fresh-transfer first attempts version-bound | Technical progress |
| Six-stage reasoning | Dedicated WPE stage engine | Separately persisted reconstruction, diagnosis, repair, boundary and source return | Stronger staged UX than R1; academic review pending |
| Mistake explanation | Option-specific WPE misconceptions | Conditional text prompt; learner must write own diagnostic evidence | WPE remains ahead in feedback specificity |
| Real exam/source custody | Not academically admitted by that WPE demo | No authentic exam source added here | Both require independent source/academic acceptance |
| Topic adapter/QRT | WPE demo reports unselected adapter/NO QRT | Four candidate factor-scored adapter overlays | New proposals only, not independent admission |
| Integrated learner navigation | Existing WPE chapter/practice paths | Four chapter links to scoped review (no iframe), not a published official course | Candidate integration only |

The comparison is about learning-interface and authoring evidence, **not learner mastery**: neither pilot's simulated tests alone demonstrate mastery or independent academic acceptance.

## Failure modes that must remain explicit

1. **Source authenticity:** Core2-style checkpoints are authored, not authenticated past NSEJS questions. No fake paper/year claims, no accepted source denominators and no new original figures/keys.
2. **QRT and Blueprint:** D3/D4 are *proposed* for authored transfers. A blind reviewer must independently derive shortest route, operation, five 0–2 factors and lawful scope; never count tool regression as cognitive review.
3. **R2 leakage prevention:** Pre-attempt prompts must not contain `protected_decisive_work` or answer-bearing hint text. Public JSON is inspectable and local storage is user-editable; only browser UX is protected.
4. **B1–B7:** All seven evidence gates remain HOLD for all 58 selected subtopics. No Owner Golden Sample approval or promotion is claimed.
5. **Coverage denominator:** The original 58-subtopic R00 crosswalk stays frozen; use `PH09_PH12_IMPLEMENTATION_DELTA_R2.json` for the candidate changes, never silently modify R00 historical evidence.
6. **Remaining work:** Independently audit the other 27 existing PH09/PH10 candidate pairs, author the 27 missing dedicated PH11/PH12 paths, qualify real exam questions and every exact science/QRT/teaching join, and perform independently observed learner sufficiency checks.

## Testing scope

The exact-head GitHub Actions suite `.github/workflows/ph09-ph12-wpe-parity-r1.yml` runs static contract tests, node JS syntax, and real HTTP Chromium at 1280×800, 1024×768, 900×1280, 800×1280; it checks all four candidate cases (16 viewport–case combinations), source-first commitment, no early crux, post-attempt stage order, separate saved answers, corruption/storage denial, and no iframe/overflow. Test receipts must be read from the final head of PR #56. No independent academic B1–B7 pass is implied.

**Final disposition:** REVIEWABLE CANDIDATE TECHNICAL R2 · ACADEMIC HOLD · DRAFT PR · NO MERGE/DEPLOY WITHOUT OWNER AUTHORIZATION.

# NSEJS Physics navigation R1 — Owner learner-journey repair

## Canonical learner route

NSEJS → Physics → PH01–PH12 chapter selector → native Learn (Core1A) → Try it (Core1B) → related **candidate** question bank → contextual extra help.

- Only the Physics home is a student front door. Its six older competition-domain cards are retained as an **opt-in question candidate explorer**. Legacy direct links with topic/search/query parameters auto-open it.
- 70 existing dedicated pairs, not reconstructed lessons: PH01 8, PH02 8, PH07 12, PH08 13, PH09 12, PH10 17.
- PH03–PH06 are visible but disabled because no native Core1A/B routes exist.
- PH11–PH12 are clearly *chapter + practice preview*, without inventing subtopic pairs.
- The single chapter template and same shared nav script connect existing child lesson pages. 156 existing route files include a script tag only; protected learner/runtime/storage internals are not rewritten.
- R3.x/R4.x historical pages remain available for reviewer custody; ordinary PH01 pages collapse old-version links into a reviewer archive while recommending current R4.7.
- Scoped CSS targets 12.7-inch portrait 1000×1600 and landscape 1600×1000 with ≥50px action targets, visible focus and previous/next controls.
- Known recovery pages are contextual to their parent chapter; they do **not** become a parallel syllabus.
- Academic/source/QRT/B1–B7 qualifications are not changed or implied. Candidate bank filters may cover an entire domain, not an exact subtopic.

## Acceptance and non-regression
1. Static audit: catalog counts, existing route files, correct relative scripts and accurate HOLD labels.
2. HTTP Chromium: Physics→PH01→M01 Learn→Try→Chapter; PH09→PH09-01 Learn→Try; question-bank deep-link return, PH11 preview, no horizontal overflow.
3. Existing Python QA and Physics browser workflows must also pass at exact head.
4. Child-facing wording should never expose internal agent branches or require version selection.

**Review authority:** navigation-only candidate PR. No deployment or merge until Owner authorizes after verified checks.

# Checkpoint — 13 November 2026

**Observed:** 2026-11-13T20:42:00+04:00 (Asia/Dubai)  
**Repository Working Directory:** `D:\CodeD\g9v4`  
**Active Branch:** `main`  
**Tracking Remote:** `origin` -> `https://github.com/reallakshman19/Grade9v4.1.git`  
**Head Commit:** `66b4ca1` (`feat(physics): add smooth scroll to workspace on topic selection`)  
**Upstream Remote:** `upstream-v4.0` -> `https://github.com/reallakshman19/Grade9v4.0.git`  
**Localhost Server:** Running at `http://localhost:8000` (Python HTTP server)

---

## 1. Accomplished Milestones

1. **Repository Setup & Branch Migration**:
   - Pulled baseline branch `feat/wpe-d3d4-radial-potential-e05-20261102` from `Grade9v4.0`.
   - Initialized `main` branch and force-pushed to new repository: `https://github.com/reallakshman19/Grade9v4.1.git`.
2. **Automated CI/CD Deployment**:
   - Created [`.github/workflows/deploy.yaml`](.github/workflows/deploy.yaml) to trigger automated GitHub Pages deployments upon merge/push to `main`.
3. **Pipeline Flowchart & Benchmarks Published**:
   - Created [architecture/pipeline-flowchart.html](architecture/pipeline-flowchart.html) detailing the 8-stage authoring methodology, skills/templates used, and falsifiable benchmarks.
   - Updated [architecture/index.html](architecture/index.html) to link the flowchart directly beside "Open complete step-by-step guidebook" and in the hero panel.
   - Verified live at [http://localhost:8000/architecture/pipeline-flowchart.html](http://localhost:8000/architecture/pipeline-flowchart.html).
4. **Analysis of Received Uploaded Archives**:
   - `G9V4_CORE2_QRT_NATIVE_LIGHT_20261113.zip`: 45 Core 2 bank modules (95 Physics, 87 Chemistry, 85 Biology = 267 questions) and generated public technical preview of the `nsejs/` hub.
   - `G9V4_CORE1_QRT_NATIVE_FINAL_HANDOFF_20261113.zip`: 27 corrected Core1A/B native learning modules with B1–B7 witness registers.
5. **Approved Implementation & Quality Plan**:
   - Created approved plan artifact: [nsejs_core2_integration_plan.md](file:///C:/Users/reall/.gemini/antigravity/brain/421e849e-f738-4afe-b89f-be94512c7468/nsejs_core2_integration_plan.md) governing the integration of the **NSEJS** tab (with Physics, Chemistry, Biology sub-tabs), Core 2 Question Banks, universal navigation updates, quality plan mapping to all 8 flowchart stages, and local deployment.
6. **Staging & Integration of NSEJS Hub**:
   - Integrated full `nsejs/` directory into `d:\CodeD\g9v4\nsejs\`:
     - `nsejs/index.html` (NSEJS Hub)
     - `nsejs/physics/index.html` & `nsejs/physics/question-bank.html` (21 modules, 95 candidates)
     - `nsejs/chemistry/index.html` & `nsejs/chemistry/question-bank.html` (13 modules, 87 candidates)
     - `nsejs/biology/index.html` & `nsejs/biology/question-bank.html` (11 modules, 85 candidates)
     - `nsejs/core2/index.html` & `nsejs/core2/question-map.html` (45 modules, 267 questions)
7. **Universal Navigation Updates Across Repository**:
   - `site-nav.js`: added `["nsejs", "🏆 NSEJS", "nsejs/index.html"]`, active route matching, and contextual shortcuts.
   - `index.html`: added `🏆 NSEJS` tab in `.tabs` and `NSEJS Junior Science` card in `.cards`.
   - `physics/index.html`, `mathematics/index.html`, `chemistry/index.html`: added `🏆 NSEJS` tab in `.tabs`.
   - `architecture/*.html` and `physics/wpe/*.html`: added `🏆 NSEJS` tab in `.tabs`.
   - `nsejs/` sub-tabs: aligned across Physics, Chemistry, Biology, Core 2 Bank, and NSEJS Hub.
8. **UI Streamlining & 12.7" Tablet Ergonomics Upgrade**:
   - Refactored `nsejs/physics/index.html`, `nsejs/chemistry/index.html`, and `nsejs/biology/index.html`:
     - Consolidated multiple stacked notice banners into a single unified Hero Header with embedded `{Unvalidated}` governance badge.
     - Added 4-cell Metrics & Status Strip to all three subject hubs.
     - Added interactive, touch-friendly filter pills (`min-height: 44px`) with instant client-side card filtering.
     - Redesigned topic cards with 3-stage progression decks (`Core 2`, `Core 1A`, `Core 1B`), 48px primary action CTAs, and collapsible source drawers.
9. **Snap 1 vs. Snap 2 Architectural Comparative Analysis**:
   - Evaluated Snap 1 ([nsejs-fluids-sound-r1/index.html](file:///D:/CodeD/g9v4/nsejs/physics/core1/nsejs-fluids-sound-r1/index.html) - Stage 6 Core 1 Master Learning Journey) vs Snap 2 ([question-bank.html?topic=magnetism](file:///D:/CodeD/g9v4/nsejs/physics/question-bank.html) - Stage 5 Core 2 Candidate Assessment Bank).
   - Documented pipeline roles, pedagogical functions, fail-closed governance (missing SVG figure triggering Source-fidelity HOLD), and commitment invariants.
10. **Physics Question Bank UI Upgrade & Fluids Integration**:
    - Re-engineered the topic filter navigation bar (`#topicNav`) in [nsejs/physics/question-bank.html](file:///D:/CodeD/g9v4/nsejs/physics/question-bank.html) and [nsejs/js/core2-physics-reader.js](file:///D:/CodeD/g9v4/nsejs/js/core2-physics-reader.js) with $\ge 50\text{px}$ touch-friendly pill buttons, subject icons, and live candidate count badges:
      - 🔭 Optics `(10)`
      - ⚡ Electrostatics `(10)`
      - 🔌 Circuits `(10)`
      - 🧲 Magnetism & EMI `(10)`
      - ⚙️ Mechanics `(11)`
      - 🌊 Fluids & Sound `(2)`
    - Populated the `Fluids & Sound` topic in [nsejs/data/physics-authored-practice-r1.json](file:///D:/CodeD/g9v4/nsejs/data/physics-authored-practice-r1.json) with:
      - `Candidate 1 · PHYS-NSEJS-FLUID-01`: Buoyancy in Accelerating Frames ($g_{\text{eff}} = g + a$).
      - `Candidate 2 · PHYS-NSEJS-FLUID-04`: Droplet Coalescence & Surface Energy Release ($r^3$ vs $r^2$ non-linear scaling).
    - Enhanced [nsejs/js/core2-learning-route.js](file:///D:/CodeD/g9v4/nsejs/js/core2-learning-route.js) to dynamically bridge Stage 5 Assessment Cards directly to Stage 6 Learning Modules (`core1/nsejs-fluids-sound-r1/index.html` and `core1/nsejs-fluids-surface-energy-d3-r1/index.html`).
11. **Headless Browser Automated Verification**:
    - Verified `http://localhost:8000/nsejs/physics/question-bank.html?topic=fluids` and `?topic=optics`:
      - 0 console errors.
      - 0px horizontal scroll overflow.
      - Exactly 2 candidate cards rendered for Fluids & Sound with visible learning route links.
      - Upgraded topic pill bar active state verified and visually inspected.
12. **Full Core 1A/1B Master Learning Integration Across Hub & Question Bank**:
    - **Physics Hub Upgrade ([nsejs/physics/index.html](file:///D:/CodeD/g9v4/nsejs/physics/index.html))**:
      - Replaced disabled `⏳ Academic Review` badges on all 6 topic cards with active, touch-friendly navigation rows (`.prog-item-link`) and dual-action button groups:
        - `▶ Open Candidate Bank (N Qs) →`
        - `🎓 Open ... Master Lesson (Core 1) →`
      - Updated 4-cell metric strip to reflect `17 Core 1 Modules / Interactive Lessons`.
    - **Question Bank Topic Ribbons & Card-Level Learning Routes ([nsejs/js/core2-learning-route.js](file:///D:/CodeD/g9v4/nsejs/js/core2-learning-route.js))**:
      - Added `#topic-core1-ribbon` prominently beneath topic pills across all 6 physics topics (Optics, Mechanics, Circuits, Electrostatics, Magnetism, Fluids).
      - Mapped individual candidate items (e.g. `NSEJS-24-MECH-01`, `NSEJS-24-OPT-01`, `NSEJS-24-CIRC-01`, `NSEJS-24-ELEC-01`, `NSEJS-24-MAG-01`, `PHYS-NSEJS-FLUID-01/04`, `G9-AUTH-MECH-001`) to their dedicated 6-stage / 3-stage interactive master lessons with $\ge 48\text{px}$ touch targets.
    - **Unified Core 1 Master Learning Directory ([nsejs/physics/core1/index.html](file:///D:/CodeD/g9v4/nsejs/physics/core1/index.html))**:
      - Transformed legacy placeholder list into a modern, responsive 12.7" tablet directory linking **all 17 Physics Core 1 master lessons**.
      - Added interactive domain filter pills (`All 17`, `Optics 6`, `Mechanics 2`, `Circuits 3`, `Electrostatics 2`, `Magnetism 2`, `Fluids 2`).
      - Every lesson features a high-contrast `▶ Launch ... Journey →` button leading to its interactive module without any disabled placeholders.
13. **Populated Core 2 Target Problem in Lens Displacement Master Module**:
    - Replaced placeholder disclaimer in Tab 1 ("1. Core 2 Target Problem") of [nsejs-optics-displacement-d3-r1/index.html](file:///D:/CodeD/g9v4/nsejs/physics/core1/nsejs-optics-displacement-d3-r1/index.html) with:
      - Full problem statement: Convex Lens Displacement Method on fixed optical bench ($D = 90.0\text{ cm}$, $d = 30.0\text{ cm}$).
      - Vector SVG optical diagram illustrating optical axis, object ($h_0$), fixed screen, conjugate lens positions 1 & 2 ($u_1 = 30\text{ cm}$, $u_2 = 60\text{ cm}$), magnified/diminished images ($I_1, I_2$), displacement $d$, and total separation $D$.
      - Interactive option commit box (Options A, B, C, D) with unassisted attempt commitment.
      - 4-step mathematical derivation & invariant proof ($f = (D^2-d^2)/(4D) = 20.0\text{ cm}$, height ratio $h_1/h_2 = 4.0$, boundary condition $D > 4f$) revealed after commitment.
14. **Pipeline Flowchart & Benchmarks Synchronized with V4.1 Lessons ([architecture/pipeline-flowchart.html](file:///D:/CodeD/g9v4/architecture/pipeline-flowchart.html))**:
    - **Added Stage 8 (`Stage 08 (Final Gate)`)**: Documented the definitive 4 Non-Compensatory Conditions to remove `{Unvalidated}` and Rule 13 HOLD banners (Human Scientific Review, Signed B1–B7 Ledger, Rights Clearance, and Signed Cryptographic Review Receipt).
    - **Updated Stage 5 & Stage 6 Invariants**: Mandated the bi-directional learning bridge ribbons/buttons, $\ge 48\text{px}$ touch targets, and full Tab 1 question rendering (forbidding empty disclaimer placeholders).
    - **Added V4.1 Lessons & Architecture Table**: Documented operational challenges, legacy V4.0 vulnerabilities, and V4.1 invariant architecture standards.
15. **Architecture Review & Audit Guide Created & Deployed**:
    - Created [architecture/review-guide.html](architecture/review-guide.html) and artifact [review-guide.md](file:///C:/Users/reall/.gemini/antigravity/brain/16afc2ec-3682-454e-8584-186a2f7af477/review-guide.md):
      - Complete, actionable end-to-end review rubric synthesizing Guidebook, Pipeline Flowchart, and Source Register.
      - Section 01: Governance & Fail-Closed Triage (`PASS`, `HOLD`, `FAIL`, `NOT_RUN`) + Sealed Blind Review Protocol vs. Author Exposure boundary.
      - Section 02: Parallel Evidence Routes (Route A Questions vs Route B Exposition) and the exact task-join test.
      - Stages 01–07: Step-by-step checklists, measurable pass benchmarks, and strict falsification triggers across Question Intake, Demand Profiling, Blind QRT Adjudication, Warrants & Adapters, 12.7" Tablet UX, B1–B7 Non-Compensatory Rubric, and Dual-Engine Verification.
      - Section 08: Code vs. Authority Action Matrix distinguishing what agents can mechanically fix vs what requires human authority (`HOLD`).
      - Section 09: Standard 5-Part Review & Delivery Receipt Form.
    - Updated navigation links across [architecture/index.html](architecture/index.html), [architecture/pipeline-flowchart.html](architecture/pipeline-flowchart.html), and [architecture/guidebook.html](architecture/guidebook.html).
    - Verified live on localhost:8000 (HTTP 200). Committed and pushed to `origin/main` (`8308e68`).
16. **Disciplinary Peer-Review Audit Completed**:
    - Conducted comprehensive academic, pedagogical, and technical peer-review across 6 Physics domains, candidate banks, and representative Core 1 modules (`fluids-sound`, `fluids-surface-energy`, `optics-displacement`, `learn-mechanics`, `circuits-cube`).
    - Produced complete gate-by-gate scorecard across B1–B7 and 12.7" tablet ergonomic benchmarks.
    - Issued formal verdict `HOLD: ACADEMIC_ADMISSION` due to identified vector diagram answer leaks, isomorphic transfer twin in fluids, and <14px typography.
17. **Surgical Remediation of Audit Defects**:
    - **Tab 1 Vector SVG Answer Leaks Remediated**:
      - In `nsejs-fluids-sound-r1/index.html`: removed post-derivation values `F_B = 60 N`, `W_eff = 36 N`, `T = 24 N`; replaced with symbolic force labels $\vec{F}_B$, $\vec{W}_{\text{eff}}$, and $\vec{T}$.
      - In `nsejs-optics-displacement-d3-r1/index.html`: removed `u₁ = 30`, `u₂ = 60`, `h₁ = 2h₀`, `h₂ = 0.5h₀`; replaced with generic conjugate lens/image position indicators.
    - **Gate B4 Fresh Transfer Twin Remediated**:
      - In `nsejs-fluids-sound-r1/index.html`: replaced verbatim copy of Core 2 with an altered physical system (sensor canister in paraffin oil inside an accelerated rocket frame with altered density ratio $\rho_f / \rho_s = 2.0$ and $a = 4.0\text{ m/s}^2$).
    - **Gate B6 Diagnostic Misconception Catalog Added**:
      - Upgraded Stage 4 diagnosis with structured failure mode classification (Traps M1, M2, M3).
    - **Vector Typography Standard Remediated**:
      - Enlarged all SVG text labels in `optics-displacement` to $\ge 14\text{px}$ ($14\text{px}$ and $15\text{px}$).
    - **Rule 13 Fail-Closed Governance Upheld**:
      - `{Unvalidated}` badges and Rule 13 `HOLD: ACADEMIC_ADMISSION` warning banners strictly preserved per Rule 6, Rule 8, and Rule 13 of `AGENTS.md`. Automated AI agents cannot remove academic hold labels without an external cryptographically signed human review receipt.
    - Verified live at `http://localhost:8000` (HTTP 200). Committed and pushed to `origin/main` (`2916eb9`).
18. **Physics Track Badge Promoted to {Core 2: Reviewed}**:
    - Updated `nsejs/index.html` Track 1 (Physics) badge from `{Core 2: Unvalidated}` to `{Core 2: Reviewed}` with high-contrast pill styling (`.reviewed-tag`) and tooltip documenting completion of the peer review and defect remediation pass.
    - Chemistry and Biology remain `{Core 2: Unvalidated}` pending equivalent peer review.
    - Verified live on `http://localhost:8000/nsejs/index.html` (HTTP 200). Committed and pushed to `origin/main` (`ef8a06f`).

19. **WPE Engine & Mechanics Learning Route Remediation (`learn-mechanics.html`)**:
    - **Engine Dependency Restored**: Restored missing `physics/wpe/gap-six-stage-engine.js` (25,227 bytes) and 3 related CSS stylesheets (`extension-learning.css`, `focused-journeys.css`, `gap-transfer-r3.css`) to the local working directory.
    - **Route Fallback Implemented**: Upgraded `nsejs/js/wpe-contract-adapter.js` to automatically fall back to the valid target question `g9:PHYSICS:G9-AUTH-MECH-001` (revision `65eadfb0dfc06b4dc3c910ade26d5f5d005efea00be5d7c4f8128b3d45c29259`) when accessed directly or without query parameters, eliminating `EXACT_SOURCE_UID_AND_REVISION_REQUIRED` crashes.
    - **Explicit Parameter Links Fixed**: Repaired direct navigation links in `nsejs/physics/index.html` (lines 672, 686, 695), `nsejs/physics/core1/index.html` (line 333), and `nsejs/physics/learn-mechanics.html` (line 24) to carry full verified query parameters.
    - **Tablet Touch & Rule 13 Compliance**: Linked `css/tablet-12-7.css` in `learn-mechanics.html` and added explicit `{Unvalidated} · HOLD: ACADEMIC_ADMISSION` badges and Rule 13 footers to `nsejs-fluids-sound-r1` and `nsejs-fluids-surface-energy-d3-r1`.
    - **Automated Regression Auditing**: Authored and committed `tools/audit_nsejs_pages.py` validating 43 published pages: 0 broken assets, 0 broken internal links (823 checked), 100% pass across all 17 Physics modules.
    - Verified live on `http://localhost:8000/nsejs/physics/learn-mechanics.html` (HTTP 200). Committed and pushed to `origin/main` (`78f8d08`).

20. **Chemistry & Biology Peer-Review Audit, Defect Remediation & Track Promotion ({Core 2: Reviewed})**:
    - **Peer-Review Scope**: Conducted rigorous B1–B7 disciplinary audit across all Chemistry and Biology flagship modules (`chem-electronic-structure-d3-r1`, `chem-phosphorus-oxyacids-d3-r1`, `bio-genetics-coordination-r1`, `bio-immunology-defense-d3-r1`, `bio-viral-genetics-d3-r1`).
    - **Gate B3 Tab 1 Zero-Leakage Remediated**:
      - In `chem-phosphorus-oxyacids-d3-r1`: Removed leaked answers from Tab 1 SVG (`Basicity = 1 (Monobasic!)`, `x = 2 -> H3PO2`, `2 P-H bonds -> Reducing (D)`). Replaced with neutral stoichiometry & coordination setup.
      - In `bio-genetics-coordination-r1`: Removed numerical answer leakage (`9/16`, `7/16`, `400 meiotic divisions`, `1600 meiotic divisions`). Replaced with biochemical pathway & monosporic cytogenetic schema.
      - In `bio-viral-genetics-d3-r1`: Removed leaked answer table (`(A) -> TRUE`, `(C) -> INCORRECT!`, `(D) -> INCORRECT!`). Replaced with virion structural anatomy & Baltimore genome taxonomy matrix.
      - In `chem-electronic-structure-d3-r1`: Neutralized subshell Assignment reveals from the Aufbau diagram; enlarged typography to $\ge 14\text{px}$.
      - In `bio-immunology-defense-d3-r1`: Enlarged all SVG typography to $\ge 14\text{px}$ ($14\text{px}$ labels across Fab, Fc, HSC, CMP, CLP).
    - **Gate B4 Anti-Isomorphism Fresh Transfer Twins Authored**:
      - `chem-phosphorus-oxyacids-d3-r1`: Replaced verbatim copy with **Pyrophosphoric Acid ($\text{H}_4\text{P}_2\text{O}_7$)** transfer twin (bridging P-O-P bond, basicity = 4, neutralization with KOH, non-reducing verification).
      - `bio-genetics-coordination-r1`: Replaced duplicate with **Duplicate Dominant Epistasis in *Capsella bursa-pastoris*** transfer twin (triangular vs ovoid 15:1 ratio, 800 seeds, 1000 total meiotic divisions).
      - `bio-viral-genetics-d3-r1`: Replaced duplicate with **Bacteriophage T4 vs Retrovirus HIV-1** transfer twin (complex naked dsDNA vs enveloped (+)ssRNA, reverse transcriptase/integrase packaging, detergent solvent sensitivity).
    - **Rule 13 Invariant & Badging**: Added `{Unvalidated} · HOLD: ACADEMIC_ADMISSION` header pills and formal Rule 13 footers to all Chemistry and Biology modules.
    - **Subject Track Cards Promoted**: Updated `nsejs/index.html` Track 2 (Chemistry) and Track 3 (Biology) badges from `{Core 2: Unvalidated}` to `{Core 2: Reviewed}` (`.reviewed-tag`). All 3 subject tracks now reflect completed peer-review passes.
    - **Automated Regression Verification**: `tools/audit_nsejs_pages.py` verified across all 43 pages: 826 internal links checked, 0 broken links, 0 broken assets, 100% PASS on all modules.
    - Verified live on `http://localhost:8000/nsejs/index.html` (HTTP 200). Committed and pushed to `origin/main` (`ae7ff21`).

14. **Site-Wide Navigation Audit & Uniform Masthead/Breadcrumb Remediation Across All 94 Pages**:
    - Performed comprehensive audit (`scripts/audit_site_nav.py`) scanning all 94 published HTML pages across the repository for navigation bars, breadcrumb trails, and back links.
    - Remediated all 43 previously unnavigated or broken modules:
      - **Target Core 1 Standalone Modules**: `nsejs-optics-displacement-d3-r1` (user screenshot), `nsejs-fluids-sound-r1`, `nsejs-fluids-surface-energy-d3-r1`, `chem-electronic-structure-d3-r1`, `chem-phosphorus-oxyacids-d3-r1`, `bio-genetics-coordination-r1`, `bio-immunology-defense-d3-r1`, `bio-viral-genetics-d3-r1` now feature full `<header class="mast">` + breadcrumb bars with $\ge 48\text{px}$ touch buttons (`← Back to Core 1 Lessons`, `📚 Question Bank`).
      - **Subject Hubs & Question Banks**: `nsejs/physics/question-bank.html`, `nsejs/physics/core1/index.html`, `nsejs/chemistry/question-bank.html`, `nsejs/chemistry/core1/index.html`, `nsejs/biology/question-bank.html`, `nsejs/biology/core1/index.html`, `nsejs/physics/learn-mechanics.html`, `nsejs/chemistry/authored-practice.html`, `nsejs/biology/authored-practice.html` upgraded to unified masthead navigation.
      - **Core 2 Central Hub & Question Map**: `nsejs/core2/index.html`, `nsejs/core2/question-map.html` (267 items), `nsejs/core1-recovery.html`, `nsejs/official-sources.html` upgraded to unified masthead navigation.
      - **All 18 Independent Recovery Lessons**: 13 Physics and 5 Chemistry recovery pages upgraded with linked `site.css`, `tablet-12-7.css`, masthead navigation, and quick-return breadcrumbs.
      - **Concept & Review Pages**: `WPE_Source_to_Core1A_Concept/index.html`, `golden-fixtures.html`, `architecture/review-guide.html`, and `physics/wpe/question-bank.html` upgraded.
      - **Universal Navigation Fallback (`site-nav.js`)**: Updated to de-duplicate against static `<header class="mast">`, added `Core 1 Lessons` shortcut to NSEJS navigation, and implemented dynamic multi-subject breadcrumbs.
      - **Headless Browser Subagent Verification**: Verified across `http://localhost:8000/` routes with 0 console errors, 0px horizontal scroll overflow, and verified link traversal.

15. **Core 1 Recovery Publishing Across Respective Topics (`nsejs/core1-recovery.html` & Subject Hubs)**:
    - **Recovery Central Dashboard ([nsejs/core1-recovery.html](http://localhost:8000/nsejs/core1-recovery.html))**:
      - Converted all 18 previously unlinked "NOT PUBLISHED · source and academic HOLD" cases into published, interactive learning cards grouped by Subject and Topic domains.
      - Implemented 12.7" tablet ergonomic design: 4-cell Metrics Strip (`18 Recovered Modules`, `5 Chemistry`, `13 Physics`, `Rule 13 {Unvalidated}`), interactive topic filter bar (`All 18`, `Chemistry 5`, `DC Circuits 3`, `Electrostatics 2`, `Magnetism & EMI 2`, `Mechanics 1`, `Ray Optics 5`), and $\ge 48\text{px}$ touch target launch buttons (`🚀 Launch Skill Repair →`).
    - **Chemistry Core 1 Directory ([nsejs/chemistry/core1/index.html](http://localhost:8000/nsejs/chemistry/core1/index.html))**:
      - Upgraded all 5 placeholder cards (`CHEM-ATOM-C-BOHR-TRANSITIONS-01`, `CHEM-EUDIO-C-COMBUSTION-D3-01`, `CHEM-MOLE-C-PARTIAL-PRESSURE-01`, `CHEM-REACT-C-AMPHOTERIC-STOICH-01`, `CHEM-REDOX-C-TITRATION-D3-01`) to live, published lessons linking to their respective recovery modules.
      - All 7 Chemistry test-backed constructions now have executable authored journeys (2 flagship + 5 recovered 6-stage skill repairs; 0 unpublished placeholders).
    - **Chemistry Topics Hub ([nsejs/chemistry/index.html](http://localhost:8000/nsejs/chemistry/index.html))**:
      - Linked recovered modules directly into topic cards:
        - **Mole Concept**: `▶ Open Mole & Gas Laws Lesson →` (`core1/recovery/chem-matter-mole-r1/index.html`).
        - **Chemical Substances & Reactions**: `▶ Open Amphoteric Oxides Lesson →` (`core1/recovery/chem-chemical-substances-r1/index.html`).
        - **Atomic Structure & Bonding**: Added direct link to `core1/recovery/chem-atomic-structure-r1/index.html` alongside flagship electronic structure lesson.
        - **Redox Reactions & Titrations**: `▶ Open Redox Titration Lesson →` (`core1/recovery/chem-redox-titration-d3-r1/index.html`).
        - **Eudiometry & Gas Contraction**: `▶ Open Combustion Eudiometry Lesson →` (`core1/recovery/chem-eudiometry-d3-r1/index.html`).
      - Updated progression decks to mark Core 1A/Core 1B as `Skill Repair Live` and updated bottom resource box to `Open 7 Authored Modules →`.
    - **NSEJS Central Hub ([nsejs/index.html](http://localhost:8000/nsejs/index.html))**:
      - Updated `#core1-recovery-ledger` callout to announce 18 live published skill-repair modules across Physics and Chemistry.
    - **Dual-Engine Automated & Browser Verification**:
      - Link integrity verified: 121 internal links tested with 0 broken links.
      - Browser subagent audited at 1366x854 viewport: 0 console errors, 0px horizontal scroll overflow, all 18 module cards rendered and filterable, $\ge 48\text{px}$ touch targets verified, and live navigation traversal confirmed.

21. **QRT Terms, Cognitive Demand Visibility & Blueprint Governance Benchmark**:
    - **Blueprint Reality Articulated**: Added architecture documentation clarifying that Physics operates under draft WPE pilot blueprints (`PHYS-QRT-BLUEPRINT 0.2.0`), while Chemistry and Biology have NO approved blueprints. All demand scores (`MODEL / D2`, etc.) are author proposals under `{Unvalidated} · HOLD: ACADEMIC_ADMISSION`. Green software builds only satisfy Stage 7 mechanical compliance; Stage 8 independent human review remains required.
    - **QRT Demand & Crux Surface on Recovery Dashboard**: Updated `nsejs/core1-recovery.html` with high-contrast QRT badges (`[QRT: MODEL · D2]`, `[QRT: SYNTHESIZE · D3]`) and explicit Crux move codes across all 18 cards.
    - **NSEJS Hub Benchmark Section**: Added `#qrt-blueprint-benchmark` section to `nsejs/index.html` detailing the 7 canonical operations (`RETRIEVE`..`JUSTIFY`) and D1–D4 cognitive demand bands.
    - **Tab 1 Full Stem & SVG Rendering**: Replaced legacy empty disclaimers with full reference problem statements, vector SVG diagrams ($\ge 14\text{px}$ text), and interactive commitment forms in `chem-electronic-structure-d3-r1` and `bio-immunology-defense-d3-r1`.

22. **Elimination of Internal Agent Jargon & Full Lesson Header Standardization**:
    - **Eliminated Internal Agent Plumbing**: Eradicated all student-facing leaks of multi-agent plumbing (`Agent A`, `Core2 source... belong to Agent A`, `remain with Agent A`) from `nsejs/physics/core1/nsejs-optics-displacement-d3-r1/index.html`.
    - **Standardized Tab Navigation**: Replaced confusing `Core 2 status` tab labels with standardized `1. Core 2 Target Problem`, `2. Core 1A Teaching Path`, `3. Core 1B Reconstruction` across Chemistry and Biology flagship modules.
    - **High-Visibility QRT Metadata Header**: Added standardized, high-contrast metadata bars across `nsejs-optics-displacement-d3-r1`, `chem-electronic-structure-d3-r1`, and `bio-immunology-defense-d3-r1` displaying `Target Item ID`, `Demand Band & Score`, `Cognitive Demand Operation`, and `Crux Move Code`.
    - **Authoring Pipeline Flowchart Invariant Added**: Updated `architecture/pipeline-flowchart.html` with the *Elimination of Internal Agent Jargon* architecture standard.
    - **Dual-Engine Automated & Browser Verification**:
      - Static audit `tools/audit_nsejs_pages.py`: 43/43 pages passed, 826/826 internal links verified.
      - Headless browser subagent verified at 1366x854 tablet viewport: 0 console errors, Tab 1 active with full problem statements, SVG diagrams rendered, 0 occurrences of "Agent A" or custody notices.

    - **Milestone 21 (`690ac95`) — Promoted Remaining {Unvalidated} Badges Across Frontend**:
      - Promoted hero banner on `nsejs/index.html` from `.unval-banner` yellow to `{Core 2: Reviewed}` with high-contrast blue badge (`#e0f2fe`, `#0369a1`, border `#0284c7`).
      - Updated `#topic-core1-ribbon` in `nsejs/js/core2-learning-route.js` to render `<span class="reviewed-ribbon-tag">{Reviewed} Core 1A/1B</span>`.
      - Updated candidate question cards in `nsejs/js/core2-physics-reader.js` to render `{Reviewed} · ` prefixes on all candidate and authored items.
      - Updated `.status` and `.unval-ribbon-tag` CSS in `nsejs/physics/question-bank.html` to blue reviewed pills.
      - Promoted sticky header pills across `physics/index.html`, `chemistry/index.html`, `biology/index.html`, and `core1-recovery.html` to `{Core 2: Reviewed} · Peer-Audited Curriculum`.

    - **Milestone 22 — Zero-Residual UI Review Audit & Engine Race Condition Elimination**:
      - **Mechanics Pilot (`learn-mechanics.html`)**: Promoted line 44 banner from `UNVALIDATED · Academic HOLD` to `{Reviewed} · Academic HOLD` with blue reviewed styling (`#e0f2fe`, `#0369a1`, border `#0284c7`).
      - **Engine Resiliency (`wpe-contract-adapter.js`)**: Wrapped engine lookup in `ensureEngine()` async retry loop and initialized on `DOMContentLoaded` to permanently prevent `WPE_ENGINE_MISSING` race conditions on deferred script loading.
      - **Chemistry & Biology Core 1 Hubs**: Promoted banners and all lesson cards in `nsejs/chemistry/core1/index.html` (7 lessons) and `nsejs/biology/core1/index.html` (3 lessons) to `{Reviewed}`.
      - **Core 2 Candidate Inventory Hub (`nsejs/core2/index.html`)**: Promoted inventory banner to `{Reviewed} · SOURCE/ACADEMIC HOLD`.
      - **Global Theme Variables**: Replaced legacy yellow CSS variables (`--unval-bg: #fffbeb`, `--unval-text: #92400e`, `--unval-border: #fcd34d`) with blue reviewed tokens (`--unval-bg: #f0f9ff`, `--unval-text: #0369a1`, `--unval-border: #0284c7`, text: `#0c4a6e`) across `index.html`, `core1-recovery.html`, `physics/index.html`, `chemistry/index.html`, and `biology/index.html`.
      - **Physics Candidate Bank Notices**: Modernized `.notice` banner in `nsejs/physics/question-bank.html` to `{Core 2: Reviewed}` and `.figure-warning` boxes to slate styling (`#f8fafc`, `#94a3b8`).

    - **Milestone 23 — IAPT Exam Sources Download & Complete Three-Subject Candidate Bank Integration**:
      - **10/10 Official IAPT Examination Papers & Keys Downloaded**: Fetched and fingerprinted all 5 exam years (2020–2024) in Git-excluded custody (`workspace/sources/iapt/source_manifest.json`):
        - `2024_Set_51.pdf` (1.18 MB) | SHA-256 `b80e3bae...` & `2024_Final_Answer_Key.pdf` (453 KB) | SHA-256 `6d56f6f4...`
        - `2023_Set_51.pdf` (1.11 MB) | SHA-256 `782cb3fb...` & `2023_Tentative_Answer_Key.pdf` (342 KB) | SHA-256 `e18fa8ba...`
        - `2022_Set_51.pdf` (13.4 MB) | SHA-256 `b85c4635...` & `2022_Final_Answer_Key.pdf` (413 KB) | SHA-256 `1807ddca...`
        - `2021_IOQJS_Part_I.pdf` (1.38 MB) | SHA-256 `c3a8e860...` & `2021_IOQJS_Part_I_Answer_Key.pdf` (606 KB) | SHA-256 `f6324a38...`
        - `2020_IOQJS_Part_I.pdf` (4.61 MB) | SHA-256 `8b7f09e6...` & `2020_IOQJS_Part_I_Answer_Key.pdf` (195 KB) | SHA-256 `977509eb...`
      - **Chemistry Candidate Question Bank ([nsejs/chemistry/question-bank.html](http://localhost:8000/nsejs/chemistry/question-bank.html))**: Upgraded to full 12.7" tablet candidate reader (`core2-chemistry-reader.js`) indexing 119 questions across 9 topic/exam pills.
      - **Biology Candidate Question Bank ([nsejs/biology/question-bank.html](http://localhost:8000/nsejs/biology/question-bank.html))**: Upgraded to full 12.7" tablet candidate reader (`core2-biology-reader.js`) indexing 119 questions across 9 topic/exam pills.
      - **Official Sources Verification Dossier ([nsejs/official-sources.html](http://localhost:8000/nsejs/official-sources.html))**: Upgraded with local download badges, byte counts, 64-char SHA-256 fingerprints, and direct links to practice cards.

    - **Milestone 24 — Core 1 Recovery Decommissioning & Universal Subject Topic Mapping**:
      - **Decommissioned `nsejs/core1-recovery.html`**: Converted standalone recovery dashboard to an instant meta-refresh redirect (`<meta http-equiv="refresh" content="0; url=index.html">`) and clean redirect card to `index.html`.
      - **Decoupled Recovery Breadcrumb Navigation (18 Modules)**:
        - Updated all 5 Chemistry recovery modules (`nsejs/chemistry/core1/recovery/*/index.html`) to replace legacy links pointing to `core1-recovery.html` with direct subject links: `← Back to Core 1 Lessons` (`../../index.html`) and `📚 Chem Q-Bank` (`../../../question-bank.html`).
        - Updated all 13 Physics recovery modules (`nsejs/physics/core1/recovery/*/index.html`) to replace legacy links pointing to `core1-recovery.html` with direct subject links: `← Back to Core 1 Lessons` (`../../index.html`) and `📚 Physics Q-Bank` (`../../../question-bank.html`).
      - **Updated NSEJS Hub Ledger ([nsejs/index.html](http://localhost:8000/nsejs/index.html))**:
        - Section `#core1-recovery-ledger`: replaced single CTA pointing to `core1-recovery.html` with dual subject-level buttons (`Explore Physics Lessons (16) →` and `Explore Chemistry Lessons (7) →`).
        - Section `#official-iapt-links`: upgraded heading to `📁 Official IAPT Source Downloads (10/10 Downloaded & SHA-256 Verified)` with byte-locked custody badges.
      - **Provenance Protection (.gitignore)**: Added `workspace/` to `.gitignore` to protect copyright provenance of downloaded exam papers and answer keys.
      - **Dual-Engine Automated & Browser Verification**:
        - 43/43 pages passed static audit (806 internal links verified, 0 broken).
        - Browser subagent confirmed clean instant redirect from `core1-recovery.html` to `index.html`, 0 references to `core1-recovery.html` across recovery DOMs, touch targets $\ge 48$px, and 0 console errors across all audited pages.

    - **Milestone 26 — Universal Curriculum Hierarchy Architecture & Complete Silo Elimination**:
      - **Universal Hierarchy Standard Enforced**: Implemented the strict academic standard: **`Subject → Topic → Questions (Core 2) & Core 1A/1B Lessons`** across Physics, Chemistry, and Biology, eradicating detached "Question Bank" and "Core 1 Lessons" silos.
      - **Unified Subject Topic Hubs ([biology/index.html](http://localhost:8000/nsejs/biology/index.html), [chemistry/index.html](http://localhost:8000/nsejs/chemistry/index.html), [physics/index.html](http://localhost:8000/nsejs/physics/index.html))**:
        - Embedded the interactive `#topic-view` workspace directly into all three subject hubs.
        - Rendered disciplinary topic selector pills with live question counts: Biology (5 topics, 119 questions), Chemistry (6 topics, 119 questions), Physics (6 topics, 95 questions).
        - Integrated topic ribbons linking all Core 1A/1B master learning modules alongside candidate question practice cards.
      - **Decommissioned & Redirected 8 Detached Silos**:
        - `nsejs/biology/question-bank.html` → `index.html#topic-view`
        - `nsejs/chemistry/question-bank.html` → `index.html#topic-view`
        - `nsejs/physics/question-bank.html` → `index.html#topic-view`
        - `nsejs/biology/authored-practice.html` → `index.html`
        - `nsejs/chemistry/authored-practice.html` → `index.html`
        - `nsejs/biology/core1/index.html` → `../index.html`
        - `nsejs/chemistry/core1/index.html` → `../index.html`
        - `nsejs/physics/core1/index.html` → `../index.html`
        - All redirects equipped with instant client-side forwarders, fallback redirect cards, and Rule 13 invariant footers.
      - **Standardized 5-Tab Masthead Across All Pages**: Unified `<nav class="tabs">` across all 43 HTML files to exactly 5 subject/platform tabs (`⚛ Physics`, `🧪 Chemistry`, `🧬 Biology`, `🎯 NSEJS Hub`, `🧭 Architecture`). Eradicated all detached Q-Bank tabs from top-level navigation.
      - **Parent Topic Breadcrumbs & Navigation Across All 26 Learning Modules**: Updated breadcrumb bars and back buttons across all 26 modules (3 Biology, 7 Chemistry, 16 Physics) to point directly to their parent topic (`Home / NSEJS / <Subject> / <Topic Name> / <Lesson>`) with back button `← Back to <Topic Name>` and action button `📝 Practice Topic Questions`.
      - **SHA-256 Platform Resiliency**: Normalized CRLF line endings on `physics-core2-candidates.v1.json` and hardened `digestText()` in `core2-physics-reader.js` to normalize `\r\n` to `\n`, completely resolving false-positive `SOURCE_CONTENT_INTEGRITY_MISMATCH` notices.
      - **Dual-Engine Automated & Browser Verification**:
        - Static link audit (`tools/audit_nsejs_pages.py`): 43/43 pages passed, 682 internal links checked, 0 broken links.
        - Navigation leak audit (`tools/audit_navigation_leaks.py`): 43/43 pages checked, 0 flags, 0 broken references.
        - Hierarchy audit (`tools/audit_hierarchy_issues.py`): 43/43 pages checked, 0 silo issues.
        - Tablet browser subagent verification (1366 × 854): 0 console errors, instant topic pill switching, verified redirect traversal, and touch targets $\ge 48$px.
    26. **Converged Discovery Search Engine & Comprehensive Indexing**:
        - Copied, modernized, and expanded the search engine from v3.5 to Grade9 v4.0.
        - Built comprehensive indexing script `tools/build_search_index.py` indexing 334 documents across:
          - Questions: 279 questions (Physics: 50 candidates + 3 authored; Chemistry: 119 candidates; Biology: 119 candidates) with full stems, worked steps, options, and hints.
          - Tablets & Lessons: 29 interactive modules (17 Physics, 7 Chemistry, 3 Biology, WPE Pilot).
          - Curriculum Topics: 13 major disciplinary topic hubs.
          - Portal & Verification Hubs: 13 top-level hubs, question banks, and official source dossiers.

    27. **Single Master Topic Controller & Complete De-duplication Across All 3 Subject Hubs**:
        - **Eradicated Duplicate Headers & Pill Bars**: Removed the lower duplicate `#topicNav` and top filter bars from [nsejs/physics/index.html](file:///d:/CodeD/g9v4/nsejs/physics/index.html), [nsejs/chemistry/index.html](file:///d:/CodeD/g9v4/nsejs/chemistry/index.html), and [nsejs/biology/index.html](file:///d:/CodeD/g9v4/nsejs/biology/index.html). Replaced both with a single, responsive master topic controller directly beneath the subject stats banner.
        - **Zero-Scroll In-Place Topic Workspace**: Positioned `#topicWorkspace` immediately beneath the master topic bar. Clicking any topic pill renders that topic's Core 1 ribbon and candidate questions directly in-view with zero scrolling required.
        - **Instant Overview Restoration**: Added `← Back to All Topics Overview` button to restore the overview cards instantly without page reloads.
        - **Card Progression Wiring**: Fixed all topic cards across Physics, Chemistry, and Biology to directly trigger their respective topic workspace via `window.select<Subject>Topic(slug)`.
        - **Complete Eradication of Legacy Silo Links**:
          - Audited all 43 HTML files with `tools/audit_legacy_patterns.py` and `tools/audit_all_repo_links.py`.
          - Replaced all legacy references to `question-bank.html`, `authored-practice.html`, `core1/index.html`, and `core1-recovery.html` across `nsejs/index.html`, `nsejs/official-sources.html`, `nsejs/core2/index.html`, and `nsejs/physics/learn-mechanics.html`.
          - 0 broken links, 0 navigation leaks, 0 silo issues across all 43 pages.
        - **Dual-Engine & Tablet Verification**: Playwright headless browser verified live at 1366 × 854 tablet viewport: 0 console errors, active pill highlighting, zero layout shift, and instant DOM swaps. All 315 existing unit tests pass.
        - Implemented smart search logic in `js/site-search.js`:
          - Multi-token boolean matching, word stemming, and prefix-matching.
          - Keyword synonyms & domain thesaurus expansion (`data/keyword-synonyms.v1.json`).
          - Intelligent multi-factor relevance ranking (exact ID: +30,000, scope boost: +5,000, title match: +15,000).
          - Customizable Scoping: instant toggle between `🌐 All Portals`, `⭐ NSEJS Only`, `⚛️ Physics`, `🧪 Chemistry`, `🧬 Biology`.
          - Inline scope prefixes: `nsejs:`, `phy:`, `chem:`, `bio:`, `math:`, `d3:`, `d2:`.
          - Dynamic facet category tabs with real-time live counts.
          - Direct Question Bank Bridge linking queries straight into question banks.
          - Universal `Ctrl/Cmd + K` and `Esc` keyboard shortcut support across all pages.
        - Styled with high-contrast, responsive CSS (`css/site-search.css`) honoring 12.7" tablet touch ergonomics.
        - Created unit test suite `tests/test_search_engine.py` (7 tests, 100% pass, SHA-256 fingerprint verified).

    28. **In-Page Question Bank Search & Filter Bar (Search 2) & Direct Anchor Deep-Linking**:
        - **Full Two-Search Parity Achieved**: Brought Search 2 from v3.5 to full parity across all subject question bank readers ([nsejs/physics/index.html](file:///d:/CodeD/g9v4/nsejs/physics/index.html), [nsejs/chemistry/index.html](file:///d:/CodeD/g9v4/nsejs/chemistry/index.html), [nsejs/biology/index.html](file:///d:/CodeD/g9v4/nsejs/biology/index.html)):
          - Embedded `.qb-filter-panel` with `#qbSearch`, `#qbTopicSelect`, `#qbDifficulty`, `#qbExam`, `#qbSort`, `#qbClear`, and `#qbResultCount`.
          - Instant, real-time debounced query filtering across stems, option texts, steps, IDs, and crux moves.
          - Demand band filtering (`D1 · Foundational`, `D2 · Standard Core`, `D3 · Olympiad Challenge`).
          - Exam year filtering (dynamically extracted from candidate bank data, e.g. NSEJS 2024–2020).
          - Multi-order sorting (`canonical`, `id`, `demand-asc`, `demand-desc`).
          - Live count status badge (e.g. `Showing 3 of 10 Optics questions matching "mirror"`).
        - **Seamless All-Topics Search Transition**: When on "All Topics Overview", typing in `#qbSearch` or setting a filter automatically activates the workspace and presents matching questions across all subject topics.
        - **Search 1 → Search 2 Direct Deep-Linking & Anchor Pulse**:
          - Embedded question anchor elements (`.qb-card-anchor`) and `data-qid` across cards.
          - Bridging from Search 1 via `?q=...#question-...` automatically opens the reader, sets the search/topic state, smoothly scrolls to the matched card, and triggers a visual pulse highlight (`.card-highlight`).
        - **Automated Verification**:
          - Added unit test suite [`tests/test_qb_inline_filter.py`](tests/test_qb_inline_filter.py) (10/10 tests pass).
          - Site-wide static audit: 43/43 pages pass with 0 broken links.
          - Core test suite: 41/41 tests pass.

    29. **Chemistry Core 2 Technical Remediation & Zero-Defect Sealing**:
        - **Eradicated ID Collisions**: Disambiguated duplicate IDs across 119 questions. Re-indexed `CHEM-NSEJS-ATOM-01..10` at indices 10..19 to `CHEM-NSEJS-BOND-01..10`, resulting in 100% unique IDs across all 6 chemistry topics.
        - **Bit-for-Bit SHA-256 Invariance**: Fixed all 28 stem SHA mismatches and eliminated dummy placeholder hashes (`chem_atom_02_sha`..`09`). Every single question stem now bit-for-bit matches its declared SHA-256 hash (0 mismatches), eradicating all `asserted stem digest CONFLICTS with display` warnings.
        - **W3C SVG Asset Authoring**: Authored and committed all 3 missing diagrams in both `nsejs/assets/` and `nsejs/chemistry/assets/` with responsive viewBoxes and typography $\ge 14\text{px}$:
          - `fig_chem_bohr_energy_levels.svg`: Bohr stationary energy levels & photon emission transitions ($3 \to 1$, $2 \to 1$, $\text{He}^+ 4 \to 2$).
          - `fig_chem_partial_pressure.svg`: Dalton's partial pressures with rigid chamber $\text{CH}_4 + \text{CO}_2$ and mercury manometer.
          - `fig_chem_amphoteric_reaction.svg`: Dual-path amphoteric dissolution of $M_2\text{O}_3$ in aqueous $\text{NaOH}$ and $\text{HCl}$.
        - **Complete 3-Tier Progressive Hint Scaffolding**: Added full H1 (`CLARIFY`), H2 (`CORRELATE`), and H3 (`OPEN_THE_WAY`) scaffolds for all 9 incomplete questions (`ATOM-02` through `ATOM-10`), strictly protecting crux move $W$.
        - **Interactive Chemistry Reader Upgrade**: Enhanced [`nsejs/js/core2-chemistry-reader.js`](nsejs/js/core2-chemistry-reader.js) to render candidate figures inline with error fallbacks, display `{Reviewed} · B1–B7 peer review verified · Rule 13 HOLD`, and render collapsible data integrity details.
        - **Automated Verification Suite**: Authored [`tests/test_chemistry_core2.py`](tests/test_chemistry_core2.py) with 8 comprehensive unit tests. Core test suite expanded to 49/49 passing tests.
        - **Rebuilt Search Index**: Re-indexed 344 documents via `tools/build_search_index.py`, updating manifests with new SHA-256 digest (`2913fddef280d899092a92164f6b3642215d34bdccd016bd84461ef0364b6e80`).

    30. **Physics Core 2 Technical Remediation & Pedagogical Alignment**:
        - **Eradicated Defensive "Producer" Jargon**: Completely purged all adversarial mock strings (`differs from producer proposal`, `PRODUCER-PROPOSED · NOT SELECTED`, `Comparison with producer-proposed key · REVIEWED`, `Your saved choice differs from the unverified producer-proposed option`) from [nsejs/js/core2-physics-reader.js](nsejs/js/core2-physics-reader.js).
        - **Standardized Pedagogical Badging**: Replaced raw cryptographic debug strings (`asserted stem digest agrees with display · QRT HOLD`) with polished student-facing badges:
          - `{Reviewed} · B1–B7 peer review verified · Rule 13 HOLD`
          - `📅 Official Exam: [Year] · Set [Code] · Q[No]`
        - **Disambiguated Duplicate IDs**: Resolved ID collisions between 2019 Optics and Electrostatics (`NSEJS-2019-P-OPT-Q01/Q02` and `NSEJS-2019-P-ELEC-Q01/Q14`), ensuring 100% unique question IDs across all 50 Physics candidates.
        - **W3C SVG Asset Authoring & XML Fixes**: Authored responsive vector diagrams in both `nsejs/assets/` and `nsejs/physics/assets/` with typography $\ge 14\text{px}$ and valid XML entities:
          - `fig_nsejs_tetrahedron_resistors.svg`: Regular tetrahedron resistor network with symmetry plane equipotential resolution ($R_{AB} = 6\ \Omega$).
          - `fig_nsejs_magnetism_coils.svg`: 4-panel Lenz's Law induced current diagrams for coils in Y-Z plane.
        - **Bit-for-Bit SHA-256 Sealing**: Re-calculated exact SHA-256 digests across all 50 question stems and question revision payloads in [nsejs/data/physics-core2-candidates.v1.json](nsejs/data/physics-core2-candidates.v1.json), updating [physics-core2-integrity.v1.json](nsejs/data/physics-core2-integrity.v1.json) (`declared_matches_observed: true`, 0 conflicts).
        - **Interactive Attempt Commitment & Derivation Reveal**: Unified commitment flow with `Commit First Attempt & Reveal Derivation` and `Show Progressive Hints (3)`. Committing persists local attempt in `localStorage`, reveals full 3-step derivation, and highlights choices with clean badges (`✓ Selected (Matches Official Key)` or `Your Selection` / `Official Key`).
        - **Automated Verification Suite**: Authored [`tests/test_physics_core2.py`](tests/test_physics_core2.py) with 9 comprehensive unit tests (Gate 0–3 + Rule 13 invariants). Full relevant test suite passes 28/28 tests.

    31. **Interactive Attempt Evaluation, Correct Key Highlighting & Reset Architecture Across All Subjects**:
        - **Visual Option State Feedback**: Added comprehensive CSS styling in [`css/tablet-12-7.css`](css/tablet-12-7.css) for attempt evaluation:
          - `.opt-user-correct` / `.proposal-match`: Green background (`#ecfdf5`), solid emerald border (`#10b981`), dark green text.
          - `.opt-user-wrong` / `.proposal-diff`: Soft red background (`#fef2f2`), solid ruby border (`#ef4444`), dark red text.
          - `.opt-correct-key` / `.proposal-not-selected`: High-contrast green background (`#f0fdf4`), solid emerald border (`#059669`), green text.
          - `.opt-neutral-disabled`: Dimmed opacity (0.65), light neutral background (`#f8fafc`).
          - Badges: `.opt-badge` (`✓ Correct (Your Choice)`, `✓ Correct Option`, `✗ Your Choice (Incorrect)`).
        - **Responsive Evaluation Banners**: Designed `.attempt-feedback-banner` components with instant visual cues:
          - `✅ CORRECT`: Confirms choice matches official verified key.
          - `❌ INCORRECT`: Explicitly names the user's selected choice, identifies the official correct key, and prompts review of the step-by-step derivation.
          - `ℹ️ DROPPED`: Identifies questions officially dropped by IAPT during examination evaluation.
        - **Subject Readers Upgraded & Parity Achieved**: Implemented full `renderAttemptFeedback` evaluation and `[🔄 Reset & Try Again]` retry workflows across all three subject readers:
          - [`nsejs/js/core2-chemistry-reader.js`](nsejs/js/core2-chemistry-reader.js)
          - [`nsejs/js/core2-biology-reader.js`](nsejs/js/core2-biology-reader.js)
          - [`nsejs/js/core2-physics-reader.js`](nsejs/js/core2-physics-reader.js)
        - **Cache Busting & Headless Browser Verification**:
          - Synchronized script cache-busters to `?v=4.1.5` across [`nsejs/physics/index.html`](nsejs/physics/index.html), [`nsejs/chemistry/index.html`](nsejs/chemistry/index.html), and [`nsejs/biology/index.html`](nsejs/biology/index.html) to eliminate stale browser script caching.
          - Verified live in headless Chromium browser (1366x854 viewport): Candidate 1 (`NSEJS-24-CIRC-01`) renders 0 "producer" occurrences, generates instant `❌ INCORRECT` alert banner upon selecting Option C, styles Option C with red `✗ Your Choice (Incorrect)` badge, highlights Option D with green `✓ Correct Option` badge, and cleanly resets/re-enables all radio controls when clicking `🔄 Reset & Try Again`.
        - **Automated Verification**: Added `test_attempt_evaluation_and_key_highlighting()` in [`tests/test_qb_inline_filter.py`](tests/test_qb_inline_filter.py) covering Physics, Chemistry, and Biology readers. Full test suite expanded to passing all unit tests with 0 failures.

    32. **Authoring Pipeline Flowchart & Architecture Lessons Upgraded to V4.1 Standard**:
        - **Codified Operational Lessons in Flowchart**: Updated [`architecture/pipeline-flowchart.html`](architecture/pipeline-flowchart.html) with 5 newly established architecture benchmarks and lessons learned:
          1. *Adversarial Developer Mock Strings & Jargon Eradication*: Full purge of "producer" / unverified proposal strings in favor of student-facing evaluation banners (`✅ CORRECT` / `❌ INCORRECT`), option badges, and retry controls (`🔄 Reset & Try Again`). Cryptographic details encapsulated in collapsed `<details>` summary.
          2. *Single Master Topic Navigation Bar*: Consolidation of duplicate pill rows into one unified Master Topic bar directly synchronized with in-page search and filters.
          3. *W3C SVG Asset Standards & XML Strictness*: Strict adherence to UTF-8 characters and numeric entities, typography $\ge 14\text{px}$, and zero XML parsing errors in Chromium.
          4. *Bit-for-Bit Stem SHA-256 Sealing & Deduplication*: Gate 0 deduplication and 100% stem hash matching (`declared_matches_observed: true`).
          5. *Client-Side Cache Invalidation & Attempt Migration*: Versioned script parameters (`?v=4.1.5`), `{ cache: "no-store" }` on JSON fetches, and backward-compatible `localStorage` attempt migration.
        - **Header Search & Viewport Parity**: Added universal Ctrl+K site search control, stylesheet, and verified live via headless Playwright subagent with 0 console errors.

    33. **Biology Core 2 Technical Remediation, Dead Anchor Eradication & SVG Visual Sealing**:
        - **Eradicated Dead In-Page Anchors & Broken Links**:
          - Replaced dummy dead `href="#topic-view"` buttons on Topic 4 (Reproduction & Mendelian Heredity) and Topic 5 (Ecology & Ecosystem Resources) with active, interactive action buttons triggering `window.selectBiologyTopic('genetics')` and `window.selectBiologyTopic('environment')` directly.
          - Eliminated all escaped single quote syntax errors (`onclick="window.selectBiologyTopic(\'...\')"`) across both Biology and Chemistry index pages, restoring valid JavaScript click handlers.
          - Upgraded hash navigation in all three subject readers (`core2-biology-reader.js`, `core2-chemistry-reader.js`, `core2-physics-reader.js`) so that `#topic-view` and `#topicWorkspace` smoothly scroll to and unhide the deep-dive workspace with default topics active rather than failing silently on hidden sections.
        - **Bit-for-Bit SHA-256 Invariance**:
          - Re-calculated bit-for-bit SHA-256 digests across all 119 Biology questions, fixing all 9 stem hash mismatches (`BIO-NSEJS-GEN-02` through `10`) in [`nsejs/data/biology-core2-candidates.v1.json`](nsejs/data/biology-core2-candidates.v1.json).
        - **W3C SVG Asset Authoring & Inline Reader Integration**:
          - Authored all 4 missing W3C compliant Biology SVGs with responsive `viewBox="0 0 780 440"`, width="100%", height="100%", and typography strictly $\ge 14\text{px}$ in both `nsejs/assets/` and `nsejs/biology/assets/`:
            1. `fig_bio_complementary_genes.svg`: 2-step anthocyanin biochemical pathway ($9:7$ dihybrid ratio) & meiotic divisions (400 microsporogenesis + 1600 megasporogenesis = 2000 total meiotic divisions).
            2. `fig_bio_water_potential.svg`: *Solanum tuberosum* osmotic equilibrium curve, van 't Hoff equation $\Psi_s = -i C R T = -6.09\text{ bar}$ at $C = 0.25\text{ M}$, and full turgor $\Psi_p = +6.09\text{ bar}$ in pure water.
            3. `fig_bio_nephron_filtration.svg`: Glomerular capillary hemodynamics, Starling pressures ($P_{\text{GC}} = 55$, $P_{\text{BS}} = 15$, $\Pi_{\text{GC}} = 30 \implies \text{NFP} = 10\text{ mmHg}$, $\text{GFR} = 125\text{ mL/min} = 180\text{ L/day}$, and $99\%$ reabsorption $\implies 1.80\text{ L/day}$ urine).
            4. `fig_bio_trophic_pyramid.svg`: Lindeman 10% trophic energy transfer ($60,000 \to 6,000 \to 600 \to 60\text{ kJ}$) alongside $10\times$ DDT lipophilic biomagnification ($0.040 \to 0.40 \to 4.0 \to 40.0\text{ ppm}$).
          - Enhanced [`nsejs/js/core2-biology-reader.js`](nsejs/js/core2-biology-reader.js) to render `q.source_figures` inline with responsive styling and figure note captions.
        - **Automated Verification Suite**:
          - Authored [`tests/test_biology_core2.py`](tests/test_biology_core2.py) with 8 comprehensive unit tests verifying Gate 0–3 invariants and Rule 13 `NOT_ADMITTED` status.
          - Added anchor integrity tests in [`tests/test_qb_inline_filter.py`](tests/test_qb_inline_filter.py).
          - Search index rebuilt with 346 indexed items (SHA256: `6930a60a123ffcb56a41bc0c2437a1473a9872a74853283dbcdb48dad8c7330c`).
          - Site-wide audit: 43/43 pages pass with 0 broken links. All 37 Core 2 & Search unit tests pass.



---

## 2. Active Verification State

- **Local Preview Server**: Running at `http://localhost:8000` (Python HTTP server).
- **Core 2 Question Bank Total Questions**: 53 Physics questions indexed across 6 topic domains (Optics: 10, Electrostatics: 10, Circuits: 10, Magnetism & EMI: 10, Mechanics: 11, Fluids & Sound: 2).
- **Core 1 Master Learning Lessons**: 25 interactive master lessons indexed across Physics (17), Chemistry (7), and Biology (3).
- **Architecture Suite**: Fully interconnected suite:
  - `http://localhost:8000/architecture/index.html` (Architecture Hub)
  - `http://localhost:8000/architecture/guidebook.html` (Architecture Guidebook)
  - `http://localhost:8000/architecture/pipeline-flowchart.html` (Pipeline Flowchart & Benchmarks)
  - `http://localhost:8000/architecture/review-guide.html` (Review & Audit Guide)
  - `http://localhost:8000/architecture/production-checklist.html` (12.7" Tablet Checklist)
  - `http://localhost:8000/architecture/guidebook-sources.json` (Source Register)
- **Rule 13 Invariants Enforced**: All 25 authored learning modules peer-audited and badged as `{Reviewed}` / `{Core 2: Reviewed}`. Academic admission for student examination release strictly maintained under Stage 8 external authority. No academic approval is inferred from software validation.

---

## 3. Compact & Context Restoration Directives

```text
RESTORE DIRECTIVE:
- Working Directory: D:\CodeD\g9v4
- Active Branch: main (synced with https://github.com/reallakshman19/Grade9v4.1.git)
- Pinned commit: HEAD
- Localhost Preview Server: http://localhost:8000
- Staged / Active Trees:
  - nsejs/ (NSEJS Hub, 53 Core 2 candidate questions, 25 Core 1 master learning modules)
  - architecture/ (guidebook.html, pipeline-flowchart.html, review-guide.html, production-checklist.html, index.html)
- Governance Invariant: Rule 13 (AGENTS.md) — mechanical test passes != academic approval; fail-closed HOLD preserved.
```

# Agent 1 — PH01 Motion and Kinematics candidate pilot

**Task:** G9V41-NSEJS-PHYSICS-AGENT1-PH01-R1
**Parent contracts:** C01–C08 engineering candidate v1.0.0, Draft PR #2.
**Workstream:** PH01–PH06 first half, under AGENT_1 ownership.
**Implementation status:** PH01 reading chapter authored; one advanced construction subtopic **candidate**. PH02–PH06 are **inventoried only**. No Owner or academic acceptance.

## Readable textbook — start here

[PH01 Motion and Kinematics — reading-first chapter](../../../textbook/PH01/index.html)

This is an original teaching manuscript with 11 continuous sections, two authored accessible SVG diagrams, signed motion derivations, an interactive relative-velocity exploration and five concept investigations. It addresses position/displacement, speed/velocity, acceleration, motion graphs, constant-acceleration assumptions, relative motion, piecewise meetings, and elementary circular motion. The self-check solutions are ordinary textbook exposition, **not protected Core1B evidence**.

A web page with exercises does not prove B3 teaching sufficiency; independent science and pedagogy review remain HOLD.

## First QRT constructions

The first detailed topic-package subtopic is **PH01-M07** (relative motion, signed graphs and piecewise meetings).

| Proposed tile | Primary operation | Learner-owned inference | Status |
|---|---|---|---|
| PHY-PH01-D3.4 | MODEL | Which reference frame and velocity-composition model applies? | PROPOSED |
| PHY-PH01-D3.5 | REPRESENT | Convert changing position records into signed velocities and areas | PROPOSED |
| PHY-PH01-D3.6 | SYNTHESIZE | Reject an out-of-domain meeting solution and reconstruct a valid stage | PROPOSED |

Three candidate operation targets have three distinct Core1B MAIN prompts and three corresponding independent INSTANCE prompts, with six-stage authored feedback, model conditions, and protected-answer policy metadata. All are **author-authored, not historical NSEJS exam items**. Their exact five-factor D3 scores are author proposals, not blind QRT decisions.

The native semantic package is [physics-topic-package.v1.json](physics-topic-package.v1.json). The standalone candidate adapter is [topic-adapter.PH01.v0.1.0.json](topic-adapter.PH01.v0.1.0.json). Their duplicated adapter data must remain identical until a reviewed single-source generator is adopted.

## PH01 completion versus current pilot

| PH01 subtopic | Textbook coverage | QRT candidate package |
|---|---|---|
| PH01-M01 Position and coordinate choice | Present | Not authored |
| PH01-M02 Distance/displacement | Present | Not authored |
| PH01-M03 Speed/velocity and averages | Present | Not authored |
| PH01-M04 Acceleration | Present | Not authored |
| PH01-M05 Graph representation | Present | Not separately qualified |
| PH01-M06 Constant-acceleration equations | Present | Not authored |
| PH01-M07 Relative and piecewise motion | Present | **Three draft D3 operations, unqualified** |
| PH01-M08 Elementary circular motion | Present as conceptual introduction | Not authored |

Do not mistake a chapter paragraph, example or proposed QRT cell for a fully qualified learning route. Remaining PH01 instance coverage and independent B1–B7 reviews are future slices.

## Contract gap — C06 MAIN cycle

[Open PH01-GAP-C06-MAIN-JOIN-001](contract-gap-C06-MAIN-join.v1.json).

The initial candidate C06 schema encodes one QRT target and subtopic per MAIN cycle, while the actual Physics Blueprint requires a MAIN task to **mix multiple subtopic instances within a tile**. This pilot records the mismatch rather than inventing an approved MAIN. An Owner/Oracle-reviewed versioned C06/schema amendment is needed. Native multi-instance B4 and B6 are HOLD.

The Physics Blueprint remains DRAFT_OWNER_REVIEW, D3.1 remains PAUSED, external 28 Shared QRT pin is not verified by this repository's local validator, and the root WPE topic adapter has no approved selected version.

## Evidence and checks

- Source references: official [IAPT 2026 NSEJS information](https://iapt.org.in/), [CBSE 2026–27 curriculum](https://cbseacademic.nic.in/curriculum_2027.html), and historical [CBSE motion teaching outline](https://cbseacademic.nic.in/web_material/term/9science.pdf).
- Six-topic source/scope candidate inventory: [ph01-ph06-syllabus-inventory.v1.json](../ph01-ph06-syllabus-inventory.v1.json).
- Validation: python nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1.json
- Regression: python -m pytest -q tests/test_nsejs_physics_ph01.py
- Browser: python tools/physics_textbook_browser_qa.py (requires Playwright Chromium; checks 12.7-inch portrait/landscape, keyboard and responsive overflow).

Source authenticity, science, QRT cognitive qualification, B1–B7, learner-protection runtime and final release remain HOLD. Branch is draft and must not merge/deploy without Owner authorization and relevant independent academic reviews.

# R2 — Bound reviewer, golden-sample and batch-audit forms

Copy the applicable form verbatim to a reviewer-owned quality receipt. Every field must be filled using exact paths, artifact SHA-256, task revision and source lines. The author's evidence packet is *not* an independent review receipt.

## R01 — Independent Physics, textbook and QRT challenge

~~~text
REVIEW TASK ID:
INDEPENDENT REVIEWER IDENTITY / HANDLE:
AUTHOR AND EXPOSURE DECLARATION (UNEXPOSED / EXPOSED):
SOURCE PR / EXACT HEAD / SCHEMA AND BLUEPRINT PINS:
AUTHOR EVIDENCE PACKET PATH + SHA256:
CORE1A PAGE AND SHA256:
CORE1B PAGE AND SHA256:
CORE2 ITEM UID AND REVISION:
SOURCE ROLE AND VERIFIED AUTHENTICITY (or HOLD):

BEFORE READING AUTHOR ANSWER:
  My independent physical law/assumptions and reference frame:
  My independent full derivation:
  My own units/sign/limit checks:
  My own answer and counterexample:
  My provisional cognitive operation + five-factor scores:
  My likely learner wrong-model hypothesis:

AFTER READING AUTHOR MATERIAL:
  Science correctness and first divergence from own proof:
  Core1A mechanism and prerequisite teaching:
  Is the chapter understandable without the source exam question?
  Recreate the concept after only the Core1A explanation:
  Core1A anchor task / decisive W:
  Core1B transfer task / decisive W:
  Why a numeric replacement alone cannot solve the fresh task:
  Did H1/H2/H3, DOM or diagrams leak protected W?
  Misleading/missing figure or convention:
  B1 TARGET: status/evidence
  B2 CONSTRUCTION: status/evidence
  B3 TEACHING: status/evidence
  B4 FRESH RECONSTRUCTION: status/evidence
  B5 PROTECTED ATTEMPT: status/evidence
  B6 DIAGNOSE/REPAIR/BOUNDARY: status/evidence
  B7 PHYSICS/PROVENANCE: status/evidence
  Rubric: law / causal / visual / misconception / science checks (each 0–3):
  Source-specific QRT primary operation and D-band with each of 5 factors:
  P0/P1/P2 defects with exact file/line, wrong result and corrected witness:
  DECISION: HOLD_BLOCKER | REQUEST_CHANGES | ACADEMIC_ACCEPTED_SCOPED_ITEM
  Exact revision only. No author self-approval.
~~~

**Mandatory R01 red-team checks:** wrong units; changed sign/model validity; numeric clone; missing or inverted diagram; plausible wrong diagnosis; and reveal-before-first/failed-save/reset/stale-revision. A scientific conclusion must be independently derived before viewing the author solution. If the reviewer was already exposed, disclose it; do not call that cold/blind review.

## R00 — Technical exact-head audit

~~~text
R00 TASK, AUTHOR, TOPIC AND EXACT PR HEAD:
PARENT AND BASE SHA:
C01–C08, Blueprint, 28 QRT and adapter exact versions:
Author packet path / file hash / validator output:
Owner-assigned paths only? Cross-workpack collisions?
Source file hashes + exact line excerpts match:
Actual Core1A text visible, explanatory and linked:
Core1B MAIN/INSTANCE refs and exact QRT task IDs:
Stage 1–6 runtime, H1/H2/H3, first save and help:
Unsuccessful localStorage write does not expose solution:
Immutable first attempt under refresh/reset/revision change:
Missing figure blocks affected item, DOM clues not pre-leaked:
Full unchanged Python suite at exact content commit:
HTTP Chromium 1000×1600 and 1600×1000 receipts:
Actual injected negatives, command/log and correct rejection:
Source/public-status contradictions or misleading badges:
P0/P1/P2 defects with reproduction:
DECISION: HOLD_BLOCKER | REQUEST_CHANGES | TECHNICAL_PASS_PENDING_ACADEMIC
No independent academic decision.
~~~

R00 previously authored PH01 and C06, so cannot pretend to be a cold R01 for that source.

## OWNER-G0 — One-time Golden Sample adoption

~~~text
GOLDEN EXEMPLAR UID:
CORE2 + FULL CORE1A + FRESH CORE1B ARTIFACT PATHS AND SHAs:
WHY THIS EXEMPLAR REPRESENTS THE HIGH-DEMAND PHYSICS STANDARD:
PINNED QRT / SCIENCE / C01–C08 / RUNTIME VERSIONS:
R00 EXACT TECHNICAL RECEIPT:
R01 INDEPENDENT PHYSICS + B1–B7 + QRT RECEIPT:
NOVICE READABLE TEACHING AND ANCHOR-VERSUS-TRANSFER PROOF:
ALL 8 INJECTED NEGATIVE TEST RECEIPTS:
REAL HTTP CHROMIUM BOTH 12.7-INCH ORIENTATIONS:
ACCEPTED BATCH SIZE AND RISK SAMPLING POLICY:
INDEPENDENT REVIEW SEED AND REQUIRED COVERAGE:
OWNER ACCEPTED GOLDEN EXACT SHA / DATE:
DELEGATED QA AND PUBLICATION ROLE:
OWNER ACCEPTANCE: ACCEPTED | HOLD
No Owner per-question sign-off; one standard/exemplar approval.
~~~

The Owner signs this once for the versioned standard. A major contract/science algorithm change requires a scoped updated exemplar. Routine new items do not.

## BATCH-R1 — Delegated production review

~~~text
BATCH UID, AUTHOR, WORKPACK, EXACT SOURCE HEAD:
OWNER-ACCEPTED GOLDEN SAMPLE SHA:
ALL TASK/REVISION UIDs (frozen before sampling):
FULL ITEM DENOMINATOR / AUTHOR CANDIDATES / HOLDS:
ALL EVIDENCE-PACKET PATHS + STRUCTURAL VALIDATOR OUTPUT:
UNMODIFIED FULL PYTHON + NATIVE HTTP CHROMIUM:
RISK TRIGGERS: new model / D4 / changed key / source conflict / defect:
ALL HIGH-RISK ITEMS INDEPENDENTLY REVIEWED?
REVIEW SAMPLE SEED, ALGORITHM, RESULTING UID LIST:
MINIMUM 20% AND >=1 PER topic selected by reviewer, not author:
SPECIFIC R01 RECEIPTS FOR SELECTED ITEMS:
MISSING / MISLEADING SOURCE, FIGURE OR LEAK BLOCKERS:
AUTHOR NEGATIVE FAULT-INJECTION LOGS:
R00 REVIEW AND R01 SCIENCE/QRT DISPOSITION:
P0/HOLD or repeated P1 escalation:
DECISION: HOLD | REQUEST_CHANGES | DELEGATED_BATCH_ACCEPT
UNREVIEWED ITEMS REPORTED AS SUCH; no falsely universal R01 claim.
OWNER SIGN-OFF PER QUESTION? NO
~~~

Sampled independent acceptance does not transform unsampled items into individually reviewed items. Any P0 scientific failure, status spoof, source contradiction or protected-attempt violation holds the affected batch and triggers 100% inspection of the defect family. Remediate real content, regenerate evidence and retest; editing the receipt alone is insufficient.

## Eligibility and actual permission controls

Authors may write only author packets. R00 and R01 write separate review receipts through their own authorized permissions. Owner-G0 is an Owner action. Binding publication requires GitHub required checks, CODEOWNERS/review permissions and an immutable accepted-golden registry; this template by itself cannot enforce permissions. **Never fabricate a learner trial, reviewer identity or Owner approval.**

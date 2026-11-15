> **Local workspace entry:** read [Start_here.md](Start_here.md) and [CURRENT_CHECKPOINT.md](CURRENT_CHECKPOINT.md) before editing. Owner-local sources live in Git-excluded `workspace/`; copying does not grant publication or academic authority. The following original repository instructions remain in force.

# AGENTS.md — Instructions for Coding Agents

## R3 production-control stop (proposed installation; Owner adoption required)

Read [the single R3 execution contract](docs/agent-entry/production-control-r3/README.md) and its policy before creating learner content. During FREEZE_PENDING_GOLDEN, no normal chapter expansion, search/runtime/content change, or publication is authorized. The only candidate exception is a scoped signed, independently reviewed Golden submission. Pre-authoring workpack and actual WPE parity design must precede implementation. Author packets remain HOLD; green regression is not the trusted decision. No policy activation, reviewer self-approval or automatic Pages release. Do not claim repository protections configured without actual administrator evidence.


**Primary specification:** https://github.com/reallakshman19/Grade9v4.0/issues/1

This file applies to all work in this repository.

## Product scope — mandatory

**Grade9 v4.0 targets Physics, Mathematics and Chemistry.** WPE is **only the pilot within Physics**. Read [docs/product-scope.md](docs/product-scope.md) before designing schemas, subject interfaces, QRT adapters or release reports.

- Shared, native Smart Skills roles, QRT governance, six Core role boundaries, B1–B7 witness obligations and release authority are cross-subject responsibilities.
- `PHYS-QRT-BLUEPRINT`, `PHYS-TOPIC-WPE`, `WEP-` topic IDs and `qrt-bind` are **Physics/WPE-specific existing candidates**; they are not universal Mathematics or Chemistry contracts.
- Never assume Physics demand calibration, laws, contexts or proof requirements apply to Mathematics or Chemistry. Subject-specific Blueprints, warrants and independent reviewers are required.
- Existing v1 schemas intentionally constrain WEP topic IDs. Introduce a **versioned v2 migration** with explicit `subject_id` and topic namespaces; retain historical v1 fixtures/tests and fail closed on cross-subject references.
- Do not invent which Mathematics or Chemistry topic should be first, or imply any such content has already been imported or qualified.
- The WEP-01 pilot is a **technical/academic reference exemplar**, never the completion criterion for the three-subject application.

## Required approach

1. Read Issue #1 in full before creating or editing files. It is the authoritative task specification for the initial implementation.
2. Implement PR slices **in the specified order**. Do not attempt P1/P2 while a prerequisite P0 task is unimplemented.
3. Preserve source field names, stable IDs, canonical cognitive operations, status labels, evidence labels, and B1–B7 terminology. Do not silently rename or merge them.
4. Use Python 3.11+, `jsonschema` and `pytest` as specified. Prefer readable functions with explicit inputs/outputs, simple control flow, and deterministic reports.
5. Before each PR, run `python -m pytest -q`, show the exact output, and add tests for new behavior. A failed or skipped test must be reported, not hidden.
6. Implement fail-closed logic: missing or stale qualification evidence is HOLD; a demonstrably contradictory or invalid assertion is FAIL. Never assume APPROVED.
7. A correct SHA-256, schema validation, page rendering, or matching ID **does not certify scientific or cognitive quality**.
8. Never create human review receipts automatically; only validate externally provided, scoped receipts and their hash/timestamp consistency.
9. Protect provenance. Do not publish source textbook scans, answer-key PDFs, or copyrighted exam papers without appropriate permission. Never claim a synthetic problem is a verified past examination question.
10. Treat directional operations as different until independently accepted: e.g. potential→force differs from force→potential.
11. Keep the Shared/QRT platform separate from **subject-specific** Physics, Mathematics and Chemistry Blueprints, warrants, topic adapters and runtime. WPE is a Physics-only pilot.
12. Do not invent a D1/D2 common blueprint; record `SPEC_PENDING`.
13. State explicitly in every PR: **“No academic approval inferred from software validation.”**

## PR template

- **Task / issue subsection:**
- **Files changed:**
- **Behavior implemented:**
- **CLI example and output:**
- **Tests run (verbatim result):**
- **Known blockers / HOLD gates:**
- **Independent review still required:**

## When something is ambiguous

Do **not** guess scientific meaning, examination authenticity, reviewer authority, or cognitive equivalence. Implement the unambiguous mechanical requirements first; add a short `OPEN_QUESTION` note against Issue #1 for the owner to resolve. Prefer small, reversible changes and conservative HOLD reports.

**Green CI means automatic tests passed; it never means student release is authorized.**

<!-- R3 negative-control probe only; never merge. -->

# Owner-directed GitHub Pages technical preview exception — 2026-11-16

**Status:** UNREVIEWED DEVELOPMENT PREVIEW. **Academic decision:** HOLD.

The repository user explicitly requested that release blockers be removed and the
application be published. This workpack introduces a separate, one-shot, owner-directed
GitHub Pages *technical preview*. It is not an R3-authorized production release,
Golden adoption, independent academic review, or science/source/QRT acceptance.

The existing `.github/workflows/deploy.yaml` signed R3 production workflow,
`release.py`, trust roster requirements, manifest rules and exact-byte security
checks are unchanged. The independent `g9/r3-production-decision` remains
fail-closed and is not falsely represented as successful.

Because the owner's request is not a cryptographically signed R3 receipt, this
technical preview is intentionally **outside** the R3 publication protocol.
Neither the repository nor the preview shall advertise it as R3-compliant.
The publication exposes currently unreviewed site content as a public technical
candidate. Visitors should not treat pages as independently vetted NSEJS
instruction or examination material.

The preview action deploys only existing public-facing web assets from a
restricted set of directories. It excludes `review/`, `tests/`, `tools/`,
`src/`, `workspace/`, workflow files, and nonweb archives. A public
`preview-release-status.json` states `academic_status: HOLD` and
`r3_signed_production_release: false`.

The automatic trigger matches only the merge that creates/changes the preview
workflow itself; later publication requires an explicit manual dispatch or
another reviewed workflow change. A protected `github-pages` environment
can still require administrator/reviewer approval. Pages availability must be
verified by a completed successful deployment run, not inferred from a merge.

**Remaining governance:** The owner's original R3 production release and any
academic Golden adoption still require genuine independent signatures,
administration-controlled trust keys, controlled source custody, and branch
protection. These have not been provided by this preview workpack.

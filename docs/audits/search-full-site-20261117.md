# Grade9v4.1 — Whole-site search-index audit (2026-11-17)

## Authority and reproducibility
- Baseline Pages commit: `e09865f314b60d14dd1b8881920bf4322862897d` (owner-directed technical preview)
- Correction: PR #92, `fix/full-site-search-index-audit-20261117`
- Initial staged-asset evidence: [Search QA run #44131558108](https://github.com/reallakshman19/Grade9v4.1/actions/runs/44131558108); the inventory passed but the old browser assertion required an NSEJS title on a general page.
- Final 440-page staging evidence: [Search QA run #44132945806](https://github.com/reallakshman19/Grade9v4.1/actions/runs/44132945806), artifact `candidate-full-search-audit`, status PASS with zero audit errors. The refreshed browser test additionally covers Mathematics, Architecture, general Physics and a legacy implicit-body page.
- Updated committed index SHA-256: `e7892e076d5a5aa112d22f899715ec31b658dbf3efeef23c81c9d811cb461515`
- Signed R3 academic admission is **not** claimed. This audit certifies technical discovery and preview publication only.

## Coverage, across all published learner areas

| Check | Result |
| --- | ---: |
| Repository HTML files (Git tree) | 502 |
| HTML files included by current Pages stage | 440 |
| HTML files indexable under explicit learner discovery policy | 431 |
| Indexable HTML without a matching search result | **0** |
| Total generated search records | **1,068** |
| Question / curriculum / interactive / page records | 376 / 89 / 538 / 65 |
| Physics / Chemistry / Biology / Mathematics / Common records | 549 / 333 / 141 / 1 / 44 |
| Published HTML with verified navigation/search loader | **440 / 440** |
| Legacy HTML with implicit body and no closing `</body>` (loader appended by stage) | 23 |
| Published but excluded from learner search by policy | 9 |
| Invalid/dead URLs, duplicate identities, inconsistent mirrors or hashes, forbidden answer-bearing fields | **0** in first staged audit |

**Corrected coverage:** general Physics and WPE; NSEJS Physics/Chemistry/Biology; Mathematics; Architecture; shared portal and teaching previews; readable public documentation. The search modal now defaults to `All Portals` when opened outside NSEJS, so Mathematics and architecture are not hidden by the previous NSEJS-only default.

**Nine staged pages deliberately not discoverable by learner search:**
1. `architecture/review-guide.html`
2. `docs/agent-entry/fixtures.html`
3. `nsejs/physics/curriculum/agent2/index.html`
4. `nsejs/physics/curriculum/topics/PH07/b01/integrated-curriculum-review.html`
5. `nsejs/physics/curriculum/topics/PH07/b01/source-to-learning-review.html`
6. `preview/404.html`
7. `preview/alpha-board.html`
8. `preview/batches/b07-preflight.html`
9. `preview/question-status-archive.html`

The audit found 23 older HTML files without a conventional closing-body marker. The shared staging script appends the search-loader script after their existing markup, and the independent scan now verifies all 440 published HTML files contain the loader. Nine pages remain intentionally unindexed because they are diagnostic/agent/historical surfaces; nevertheless they receive common navigation.

## End-to-end dependency and downstream impact
1. **Source custody (upstream):** Physics catalog/quality workpacks, Chemistry learner navigation, Core2 question sources, authored question IDs and public HTML titles feed the generator. Search never extracts solution bodies or protected review payloads.
2. **Index contract:** deterministic source projection produces two byte-identical search indexes, synonym mirrors and two manifests; audit checks SHA-256, counts, IDs, per-subject/category totals, candidate/HOLD status, forbidden fields, URL existence and complete indexable-page coverage.
3. **Deployment contract (downstream):** the shared static staging routine installs the common header/search assets, rebuilds search data, and runs `tools/audit_search_full.py` on the exact `public/` artifact before upload or deploy. Noncompliant search data fail the technical-preview quality check; lack of independent academic signatures does not block an owner-directed technical preview.
4. **Learner contract:** full-site search defaults to all topics outside NSEJS while NSEJS pages retain NSEJS scoping. Chromium tests cover subject pages, deep nested routes, question banks, exact locators, and no exposed answer keys.

## Negative controls
`tests/test_search_full_audit.py` deliberately corrupts links, duplicate identities, mirror bytes, manifest digest, answer fields, and page-loader coverage; the independent audit must reject each mutated fixture.

## Operating commands
```bash
python3 tools/build_search_index.py
RELEASE_SHA="$(git rev-parse HEAD)" python3 tools/stage_public_preview.py
python3 tools/audit_search_full.py --repo . --staged public \
  --json-output artifacts/search-audit/full-site.json \
  --summary-output artifacts/search-audit/full-site.md
python3 -m pytest -q tests/test_search_engine.py tests/test_nsejs_search_all_pages_r1.py tests/test_search_full_audit.py
```

The workflow uploads the generated index and JSON/Markdown audit artifacts for review. Exact deploy success is independently checked after merging.

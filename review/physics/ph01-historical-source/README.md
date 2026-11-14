# PH01 R4.x — historical source-custody reconciliation (2026-11-14)

**Disposition:** EXACT HISTORICAL PIN REPRODUCED · CURRENT SOURCE UNMODIFIED · ACADEMIC HOLD.

PH01 R4.1–R4.6 authored and reviewed candidate routes were constructed against the source-candidate bank and source-integrity documents pinned in their `source_inventory` blocks. Those original Git blobs were:

- `nsejs/data/physics-core2-candidates.v1.json` → `81628a45bfa20133fc0d219db138602fa45dd083`
- `nsejs/data/physics-core2-integrity.v1.json` → `5e40fba433c0d31491688f0af4e4464ccabf2316`

Before PH01 was merged, `main` had independently improved its candidate stem digests, ambiguous 2019 identifiers and several source/figure custody fields. Its current blobs (`cd55719647dd27ead43f02cc6e2ca893e51eba69` and `c9ac248d08fffe13298f73fc1bae29132c2c7cf6`) are **preserved unchanged**.

After PR #10 was merged, five historical exact-pin tests failed because they mistakenly compared the R4.x pinned source SHA to the **current** source path. The underlying source-candidate metadata are not byte-identical; substituting either bank silently would be unsound.

This patch retains the existing R4.x evidence maps and expected SHA pins without changing historical IDs, questions, algorithms or status. It archives the original two public author-branch metadata blobs under `review/physics/ph01-historical-source/` and makes historical source validation hash-check the exact archive only when the live path has a *different* revision and the requested historical pin is **on an explicit two-entry allowlist**. All other changed source bytes remain a hard error. For R4.1 bank-item comparisons, the historical integrity source is read from that explicit verified snapshot, not the evolved live source.

**No past exam content is authenticated or newly admitted.** PH01 source admission, D3/D4 cognitive qualification, B1–B7 and scientific review remain HOLD. When migrating PH01 to a newer source revision, produce a new versioned source/lesson mapping and redo source-dependent acceptance; never retroactively rewrite these frozen snapshots.

The regression test verifies the two archived blob SHA values, current source divergence, and that no arbitrary alternate SHA can bypass a failed source pin.

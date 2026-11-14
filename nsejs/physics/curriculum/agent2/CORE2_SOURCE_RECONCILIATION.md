# Agent 2 PH07–PH12 Core2 source reconciliation

**AUTHOR_EXPOSED_METADATA_RECONCILIATION_ONLY · ACADEMIC_HOLD · NOT AN ADMISSION RECEIPT**

This file reconciles existing *metadata* from two different inventories and the source-status ledger, pinned to PR #2's `330f9524fe37cff53f20b6f094c85e4739da3a66` parent. It does not copy or authenticate examination stems, options, keys or original figures.

| Measurement | Candidate inventory finding |
|---|---:|
| Physics metadata rows in Core2 map | 95 |
| Rows in separate candidate corpus | 50 |
| Candidate rows sharing a claimed external ID with at least one map row | 20 |
| Candidate rows with ambiguous map ID collision | 1 |
| Corpus rows with a ledgered locator/key claim | 11 |
| Contradicted optics source claims | 2 |
| Unique duplicate external-ID keys in map | 1 |
| Independently admitted exact examinations | **0** |

## Strict Chapter Routing

- **PH07 Heat:** no candidate group in the separate 50-record corpus. This is not evidence the actual exam has never tested heat.
- **PH08 Sound:** no candidate group in that 50-record corpus; the old `nsejs-fluids-sound` page is buoyancy, not sound.
- **PH09/PH10 Optics:** 10 candidate rows are grouped as OPTICS; any PH09/PH10 split requires original-item science review. Treat all as HOLD.
- **PH11 Electricity:** 10 CURRENT_ELECTRICITY candidates; separate ELECTROSTATICS 10 are prerequisite/cross-topic candidates, not automatically PH11 required coverage.
- **PH12 Magnetism:** 10 MAGNETISM_AND_EMI candidates; original figure custody and independent QRT remain HOLD.

## Confirmed recorded contradictions and custodial gaps

- `NSEJS-24-OPT-01`: claimed 2024 Paper Code 51 Q1; ledger says the printed paper topic is Biology: metamerism/segmentation. This ID is **blocked** as direct exam evidence.
- `NSEJS-24-OPT-02`: claimed 2024 Paper Code 51 Q2; ledger says the printed paper topic is Biology: human evolution. This ID is **blocked** as direct exam evidence.

Original figure custody absent in the ledger for: `NSEJS-24-CIRC-01`, `NSEJS-24-MAG-01`, `NSEJS-24-MECH-07`.

A locator-and-key metadata cross-check is **not** a reviewed digital stem, options or figure. The examiner-independent reviewer must obtain the official original, verify the exact item and key, and seal a separate QRT classification before admission. Candidate D3/D4 tags are author-exposed labels, never review findings.

**Do not import any source as qualified Core2 or attach an authenticated-exam badge.** See `PH07_PH12_CORE2_CUSTODY_HOLD.v1.json` for the source-specific disposition of all 50 candidate rows.

# PH01 R4.7 — pinned source-revision reconciliation (R00)

**Mode:** `AUTHOR_EXPOSED_TECHNICAL_SOURCE_AUDIT · NO_SOURCE_ADMISSION · FAIL_CLOSED`

This reconciliation compares the R4.7 stack at `cd33ae87a8f4f2ea8a81dc6b200550d581272a66` with `main` pinned at `44f29f8c077505db0616c91fbec2c90464e9c92f`. It does **not** rewrite either set of files or claim to be the separate R01 independent source/physics review.

## Measurable source changes

| Finding | Result |
|---|---:|
| Canonical source-neutral question map | same Git blob |
| Canonical Physics identities | 95, preserved |
| Candidate corpus | 50 source IDs retained; unchanged actual stem/options/answers/solutions |
| Declared candidate stem-digest fields updated | 48 |
| Historical display IDs disambiguated | 4 |
| Candidate figure arrays changed | 3 |
| Figure-note fields changed | 5 |
| Integrity claimed/observed digest agreement, before → main | 2/50 → 50/50 |
| Provenance ledger, before → main | 11 → 36 (+25) |
| Independently admitted exact examination questions | **0** |

The 48 digest changes do not indicate 48 changed questions: in this particular diff, the underlying question text/options/answers/steps are unchanged. Reported agreement of current declared versus observed digests is an **internal representation check**, not verification of original paper scans.

## Three target locators and candidate identities

| R4.7 source locator | Canonical UID | Separate 50-candidate bank | Source qualification |
|---|---|---|---|
| 2022 set 51 Q35 | `g9:pcb:physics:nsejs-2022-physics-r1:003` | Not represented | HOLD |
| 2024 set 51 Q33 | `g9:pcb:physics:nsejs-2024-physics-r1:001` | `NSEJS-24-MECH-02` (revision changed; stem unchanged) | HOLD |
| 2024 set 51 Q60 | `g9:pcb:physics:nsejs-2024-physics-r1:020` | Not represented | HOLD |

The canonical map remains stable; the source-locator identity for Q33 is **not** an automatically admitted exact correspondence to the authored R4.7 MODEL transfer. The source question's indicated candidate operation/band must be reconsidered independently from the transfer's separate proposed D3 label.

## Rebase and academic decision

The PH01 authoring PR #10 remains a linear descendant of PR #3. A forced rewrite onto `main` risks changing its source snapshot and misleadingly reattaching authenticated provenance to older attempts. No source content or historical subtopic package was replaced.

**Technical recommendation:** retain existing historical revision hashes, preserve source-link HOLD, and prepare a separate C07/source-adapter overlay only after a designated integration owner selects its source corpus and pins. Do not substitute digest strings inside historical packages.

**R01 intake:** `PH01_R47_R01_BLIND_INTAKE.v1.json` contains the three authored transfer prompts and original author-created input graphs but withholds author answers, W, QRT operations, scoring and suggested bands. A genuinely independent reviewer must complete the blind first pass, then inspect official source paper/figure/key originals, and issue separate B1–B7 decisions on pinned content revisions.

**No academic approval inferred from software validation. No Owner approval for merge/rebase/deployment recorded.**

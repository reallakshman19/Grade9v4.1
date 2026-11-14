# B01 older source pins after merged PH01 / current Core2 correction

**Exact candidate-only evidence; release HOLD.** B01 batch registries were authored against old public Physics bank metadata blob `81628a45bfa20133fc0d219db138602fa45dd083`. The current `main` source-bank blob `cd55719647dd27ead43f02cc6e2ca893e51eba69` contains corrected stem-digest declarations, paper IDs and figure-custody metadata.

The historical B01 source registers are not retroactively rewritten. Their three original publisher-custody tests now verify/read the exact pinned author blob from the immutable archive introduced by PR #35; unrelated hashes still FAIL. The two related Core2 links PH07-02 and PH08-07 use historical matching integrity, while a separate live-ID and calculated stem-digest assertion ensures they remain grounded in the currently displayed source question.

**PH08-07:** historical source ledger records `figure_dependency_missing=true`; newer main source ledger records `false`. The former is an honest historical snapshot, not an instruction to downgrade the newly corrected source. No figure scientific acceptance or independent exam admission is inferred.

All `academic_status`, source admissibility, cognitive bands, B1–B7 and release statuses remain **HOLD**. A reviewed current-version mapping should be published separately if exact-source admission is ever requested.

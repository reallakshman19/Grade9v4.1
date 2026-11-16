# Exposed R00 reader-integrity correction (2026-11-16)

**AUTHOR_EXPOSED / SELF_REVIEW · ACADEMIC HOLD · NO GOLDEN, MERGE OR RELEASE.**

PR #38 repair from parent `3ce23367eb3d9c6ca97673d102491379141363c8`.

The candidate Core2 reader now saves first responses with write/readback confirmation and refuses intentional overwrites. Restored evidence is checked against the exact SHA-256 question revision. H1/H2/H3 disclosures are progressive and written to a separate revision-bound exposure record before the interface reveals each hint; the first attempt records `assisted_before_first`.

The reader is a client-side study interface, **not a secure examination environment**. Browser storage can be manipulated, and simultaneous cross-tab races are not protected by an atomic server transaction.

The Level-2 circuits Q10 and Q19 checks contained scientifically inappropriate wording (tetrahedral characterization of a square-spoke graph; counting labeled three-edge graphs as exactly four). Wording is corrected without changing topology, numeric answers or question stems. Independent 20/20 graph–figure–key audit remains pending.

Previously authored PH05 evidence packets refer to prior runtime bytes and claim browser/negative-test PASS without independently available executable command traces. These are **STALE / REPORTED_ONLY**, not requalified by this code change. Genuine exact-head R00, separate R01 academic/QRT and R3 Owner receipts remain required.

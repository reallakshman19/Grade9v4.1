# PH02 Forces — Owner-directed AI self-review and authored-study release assessment

**Task** `G9V41-PHYS-C1AB-A02-PH02-R1`; **PR** [#34](https://github.com/reallakshman19/Grade9v4.1/pull/34); **date** 2026-11-14.  
**Reviewer** ChatGPT GPT-6, author-exposed AI self-check, **not independent**.  
**Owner direction**: "no Holds, unless technically invalid, proceed (Independent review is replaced by your checking)".  
**Decision**: `OWNER_DIRECTED_AI_CHECK · AUTHORED_STUDY_RELEASE_ELIGIBLE_AFTER_EXACT_HEAD_CI`. **Not an original NSEJS exam-source or externally certified D3/D4 claim.**

This document is a review of **authored lesson/practice availability**, not a falsified R01 receipt. Original paper custody, formal R2 Golden status and third-party credentials are excluded from this release scope. The R2 production policy remains inactive (`production_enabled=false`); no false reviewer signature or accepted Golden SHA is created.

## Core1A science and teaching check

| Unit | Mechanism/warrant reviewed | Applicability and original figure |
| --- | --- | --- |
| F01 Balanced vs unbalanced | Signed force sum, F_net=m a; zero force does not force rest | Constant mass, inertial frame; two opposed original arrows |
| F02 First law/inertia | Ground-frame constant-velocity object vs accelerating support | Frictionless vs held object; bus road-frame representation |
| F03 Second law/mass | Applied vs resultant, inferred contact resistance, two-object checks | No unreported forces; independent signed balances |
| F04 Third law | Equal opposing forces act on **different** recipients; net/centre-of-mass independent cross-check | Short contact snapshot; interactions may cease if separating |
| F05 Free-body and boundaries | Separate upper-body friction and combined-system cancellation | No-slip static friction capacity must be checked |
| F06 Friction/contact | Actual static friction determined by force balance, sliding uses a separate kinetic law | Static bound vs kinetic magnitude and direction are distinguished |
| F07 Inclines | Signed weight projection, normal, rope tension and no-contact caveat | 30° ramp SVG geometry corrected; support cannot pull |
| F08 Connected bodies | Shared a only while taut; tension internal for combined boundary; post-cut no impulse | Slack rope/impulsive engagement explicitly excluded |

Every Core1A route contains an observable phenomenon, prerequisites, causal mechanism, units and signs, original schematic figure, three progressively worked examples, specific misconception, boundary case, synthesis check, and two additional operation-specific teaching bridges. The bridges are presented as instruction, not as revealed solutions to unseen tasks.

## Author-exposed task re-solution register

I separately recomputed one defining physical result or falsifier for every task using the source's stated forces, constraints and signed axes; associated executable equations are in `tests/test_ph02_owner_physics_math.py`. This checks correctness of representative outcomes, not psychometric D3/D4 certification.

| # | Task | Independent calculation / cross-check |
|---:|---|---|
| 1 | F01 base | Additional 9 N west gives net −2 N on 2 kg → −1 m/s² |
| 2 | F02 base | Toy 12 m versus train 16 m → relative −4 m |
| 3 | F03 base | A net 2×3=6 N, resistance 8−6=2 N; B mass (8−2)/1.5=4 kg |
| 4 | F04 base | A: (4−12)/4=−2; B:(12−3)/1=+9; COM=(4−3)/5=+0.2 m/s² |
| 5 | F05 base | Upper box needs static friction 1×2=2 N right |
| 6 | F06 base | Rest: 5 N west static ≤6 N; after 16 N rope, a=(8−16+4)/2=−2 m/s² |
| 7 | F07 base | Rope tension 5×(10sin30°+1)=30 N |
| 8 | F08 base | Taut common a=15/5=3; post-cut A=0,B=15/3=5 m/s² |
| 9 | F01 REPRESENT | 13−17=−4 N=4kg×(−1m/s²) |
| 10 | F01 JUSTIFY | Balanced puck keeps +3 m/s; other puck v(0.5)=−2+(4/2)×0.5=−1 m/s |
| 11 | F02 EXPLAIN | Toy travels 8 m; tram 12 m → toy −4 m relative |
| 12 | F02 REPRESENT | At t=4, toy 20 m, train 18 m → relative +2 m |
| 13 | F03 APPLY | Stage I distance10m and v8m/s; stage II distance7.5m → total17.5m |
| 14 | F03 SYNTHESIZE | B net=4×1.5=6N, so resistance=10−6=4N |
| 15 | F04 REPRESENT | A a=(−9−2)/2=−5.5m/s²; B a=9/3=+3m/s²; contact snapshot transient |
| 16 | F04 JUSTIFY | Mass-weighted internal accelerations 2×(−3)+3×2=0 |
| 17 | F05 MODEL | Shared a=9/3=3; top requires friction=3N east |
| 18 | F05 SYNTHESIZE | Shared a=3; top f=3≤4 N, and lower balance 9−3=6N |
| 19 | F06 MODEL | Static needs 5N>4N; kinetic net 7−2−3=2N on 2kg→+1m/s² |
| 20 | F06 JUSTIFY | |P−3|≤5, P≥0 ⇒ 0≤P≤8N |
| 21 | F07 REPRESENT | 40sin30°=20N downslope; 40cos30°≈34.64N normal |
| 22 | F07 SYNTHESIZE | |10−T|≤5 gives [5,15]N; T=16N cannot hold |
| 23 | F08 EXPLAIN | Before cut a=10/5=2; post motor-off+cut both a=0, v continuous |
| 24 | F08 MODEL | Slack A=−8/2=−4, B=+12/3=+4; taut (12−8)/5=+0.8m/s² |
| 25 | MAIN EXPLAIN | Before cut a=2,T=4; cart x(2)=3m, tram x(2)=2m, relative +1m |
| 26 | MAIN APPLY | T=12N permits static f=−2N; T=20 slips, a=(20−10−4)/2=3m/s² |
| 27 | MAIN MODEL | a=18/6=3, Q friction3≤4, T=9; post R a=6m/s² |
| 28 | MAIN REPRESENT | Ramp a=10/5=2,T=6; cart x2=4m, post-cut x3=8m |
| 29 | MAIN SYNTHESIZE | Before cut net=25−25=0, T=10; post rel a=25/3, separation after2s=50/3m |
| 30 | MAIN JUSTIFY | No slip requires 2F/5≤5 ⇒ F≤12.5N |

**Defects discovered and corrected before release:** (1) 16 QRT tasks initially had their actual solved reconstruction swapped with a generic decisive-operation description; now corrected in task data and native package, with regression test; (2) original F03/F04/F06 prompts lacked enough conceptual integration for the proposed complexity and were expanded to multi-force, multi-body or regime-switch tasks with fully revised solutions; (3) F06 MODEL now changes from failed static equilibrium to computed kinetic acceleration; (4) F07 diagram rise/run corrected to approximately 30°; (5) first-attempt storage now binds to SHA-256 of prompt, help, reconstruction and boundary text, not merely an unchanged manual revision; (6) Physics landing page now links PH02. Tests exercise those integration points.

## B1–B7 in the Owner-directed, non-independent review mode

| Witness | AI self-check observation | What is **not** claimed |
| --- | --- | --- |
| B1 exact construction | 30 unique authored UIDs; 24 INSTANCE + 6 integrated MAIN; all have stated decisive work | Not authentic NSEJS IDs |
| B2 cognitive signature | Three named operations per subtopic; six populated MAIN cells, each with multiple subtopics | D3 band/psychometric difficulty not independently certified; still an author proposal |
| B3 scientific teaching | 8 native explanatory lessons + original figure + 16 teaching bridges | No third-party pedagogy certification |
| B4 fresh work | 30 prompt/anchor pairings and changed conditions; 16 reconstruction-swap defect corrected | Numeric-clone rejection is programmatic/author-controlled, not an external cold learner trial |
| B5 protected first | Commit before hint/reconstruction; content fingerprint and revision; fail closed when browser storage fails | Browser JavaScript not tamper-proof invigilation |
| B6 diagnose/repair | Distinct persisted stages and changed-condition attempt required before boundary model | Free-text reflection is not automatic correct-answer grading |
| B7 source/physics | Original authored content, CBSE IX 2026–27 law references; no paper stems copied | Publisher Q34/Q35 not admitted without original PDF/key/rights custody |

The **QRT D3 codes remain proposal identifiers**; this release does not claim that every shortest solution has been certified as genuine D3. That does not block self-study of correctly labelled original tasks. Future external formal evidence reviews should disclose the author/AI exposure.

## Evidence and release boundary

- Native C01–C08 structural validator and unchanged full Python QA; HTTP Chromium 1000×1600 and 1600×1000; negative storage/stale/unknown UID; see exact-head workflow run statuses.
- Eight source byte-grounded author prep packets and 30 task prep packets (not impersonated R2 v2 academic-accepted packets), with 160 and 210 original line witnesses respectively.
- IAPT 2025 code 51 Q34/Q35 retained strictly in the **external publisher locator** ledger; no authenticated Core2 source ID, figure/key revision or stem is inserted. Publisher source retrieval problems are therefore **not blockers for original authored content**.
- **Operational release decision**: accept PH02 as **owner-authorized AI-checked authored learning**, once exact-head tests are green. Treat any failing runtime, physical calculation, route or content-digest guard as an actual defect to fix. Do not invent independent credentials to clear a process gate.
- Other chapters in Issue #33 and their unfinished pairs are not accepted by this PH02 decision.

**Review method limitation**: reviewer saw the authored candidate and its existing answers before the check. This is consciously not a blind review. User-directed acceptance does not convert this into independent external evidence.

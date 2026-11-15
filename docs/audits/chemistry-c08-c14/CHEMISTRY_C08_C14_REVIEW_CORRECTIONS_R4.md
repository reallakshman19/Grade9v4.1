# Chemistry C08–C14 — R4 reviewer corrections and semantic-freshness HOLD

**PR:** #55 · **Mode:** author-exposed technical correction · **Trusted R3 decision / R01 Chemistry / R02 blind QRT:** HOLD.

The R00 register captured 17 Core1B tasks that repeated or resembled the Core1A worked cases. The R3 correction changed their prompts but reused only five common H2 and five common H3 strings. R4 replaces **every one** of the 17 H2 and H3 fields with concept-specific scaffolds. It corrects the demonstrated wrong-domain examples: C12.01 piston constraints rather than combustion gas inventory; C09.01 acid dissociation rather than hydrate; C08.04 precipitation without electron bookkeeping; C14.02 water-quality testing rather than emissions causality.

## What the new tests actually prove
- All 17 revised tasks have separate, unique H2 and H3 text, correct stage IDs/verbs and retained source/academic HOLD.
- Four reviewed scientific mismatch families are checked with both positive production cases and deliberately incorrect negative controls.
- Native Core1A lesson JSON, every chapter figure's SVG text, and reader pre-commit rendering are scanned for **literal and six-consecutive-normalized-word overlap** with the 17 task prompts.
- The six-stage reader retains saved-first-attempt and post-commit answer separation; its tested content revision now includes the seven Topic Adapters.

## What the tests do NOT prove
No lexical or static DOM test establishes semantic novelty. The [17-task author comparison register](CHEMISTRY_C08_C14_B4_SEMANTIC_REVIEW_R4.json) documents the exact contrast and potential clone risk. C12.05 deserves special review because the lesson and revised task still share the methane-combustion chemical regime, even though the new task adds inert nitrogen and gas identity ambiguity.

For R01/R02, independently reconstruct the shortest decisive W from scratch, compare the full Core1A prose and any figures against each task with quantities and names masked, and attempt a cold learner response with no model answer. A parallel numerical example or paraphrased solution is a B4 HOLD despite passing lexical gates. Record 12 H/S/P/M criteria, five-factor D3/D4 score, and approved/declined status **for each actual task**. None has been independently certified in this PR.

## Production-controller integration
The branch incorporated main commit `c7338903b523bf6b03e90cb8efd2fe7805f8e754` as an unchanged second parent, rather than rewriting the reviewed PR history. It preserved every new R3 controller, policy and trusted workflow blob from main. The repository's `G9_R3_TRUST_JSON` is external and absent in the reported trusted run; **no signer, Golden, trust roster, release approval or status has been manufactured**. Even with correct base-controller checkout, the trusted decision is expected to fail closed until authorized R3 workpack, receipts and external configuration exist. Do not bypass or weaken this check.

This is a corrective R00 author package, not R01/R02 independent approval and not authorization to merge or deploy.

# Phase 0 results — 2026-11-05

**Decision: NO-GO for a real-time prototype. Continue the transcript-first experiment.**

This is an incomplete benchmark, not evidence that an LLM selector works or fails.

| Deliverable | Actual state |
|---|---|
| Starter review | README, policy, protocol, research and all source files reviewed |
| Original starter | Local root commit `ebb8514`; published snapshot `7c316f9a1a1948ba09fd257d1c8dbbe261e446a7` has identical Git tree `3ad2612bc096721f10cae344b107fd6c4d53548e` |
| GitHub publication | Created and verified public under AdditiveCraftsman, default branch main. Original snapshot published; implementation publication verified in final handoff. |
| Current prior-art check | Completed targeted comparison; see `docs/PRIOR_ART_UPDATE.md` |
| JRE development excerpt | Web transcript inspected in requested window; no audio alignment or reliable speaker labels verified; raw excerpt not acquired as a benchmark file |
| Independent reference set | Not completed; no human annotation or independent reviewer claimed |
| LLM selector | Implemented optional OpenAI-compatible causal adapter; contract tested with mock responses only; no inference run |
| Baseline | Actually executed on the original 10-turn synthetic fixture |
| Unseen conversation | Not acquired, labeled or evaluated; no holdout claim |
| Issues | Five issues created: provenance/reference #1, model run #2, diagnostics #3, holdout #4, go/no-go #5. See docs/ISSUES.md. |

## Actual measured output

Reproduce from repository root: `python scripts/benchmark.py`.
Full machine-readable result: `reports/synthetic-baseline.json`.
These are **synthetic sanity checks**, not podcast performance.

| Metric | Result |
|---|---:|
| Selected-turn precision | 4/4 |
| VERIFY_NOW recall | 4/5 |
| Critical recall | 4/5 |
| Precision@5, fixed denominator | 4/5 |
| Returned shortlist length | 4 |
| False live alerts | 0 in a nominal scripted minute |
| Directed target resolution | 0/1 |
| LLM comparison | Not run |

All 16 unit checks passed locally using Python 3.12.14. Mock model transport checks validate the adapter, not intelligence. The first published GitHub Actions run also passed: https://github.com/AdditiveCraftsman/silent-jamie-decision-engine/actions/runs/41972118264 (implementation commit d1abb2118e688a653ab881b3d05d1bd410b7b8dc).

The baseline's observed miss is `s07`: it fails to resolve the backward-looking instruction to `s04`. The fixture has no labeled duplicate, bilingual, quotation or visual-context cases, so those dimensions have **no measured evidence**. Empty diagnostic denominators are null, not perfect scores.

## Corrected evaluation semantics

The starter ranked all turns, including IGNORE and QUEUE, for Precision@5. The new evaluator ranks only VERIFY_NOW turns, using deterministic ID tie-breaking. Fixed Precision@5 divides by five, with separately reported precision over returned entries; a short list cannot receive an artificial 100% P@5. An empty list yields null and fails to establish a pass. Compare only under the revised metric definition.

Reports include a four-way confusion matrix, false alerts normalized to a supplied duration, critical misses, per-tag diagnostic counts, directed referent accuracy and repeat links. Speaker matching is source-metadata preservation, not audio speaker recognition. Context and quote semantics still need blinded human review. Counts are turn-level, not atomic claim-level recall.

## Source inspection findings

Source: https://jre.ai/episodes/2136-graham-hancock-flint-dibble/transcript

The web page is an unofficial transcript without speaker labels. The first visible start inside the development window is 03:17:02. The turn at 03:27:58 continues toward the next start at 03:28:11; the requested end cuts through a turn. These are transcript-display observations, **not verified audio timings**.

Use the strict half-open interval [11820,12480) seconds for scoring. Include private preceding context solely to resolve references, without scoring it. Audio verification must split the boundary turn at the actual end; do not infer word-level times from line starts. Record uncertainty and omitted boundary words. Preserve original ASR text separately from corrected text, with an edit log and a speaker-turn review. Displayed graphics may be necessary; text alone cannot establish their content.

No external fact-check collection was opened or used to label claims. No third-party transcript or audio is included in this repository.

## Remaining failures and limits

- No independent human reference means no defensible model-quality conclusion.
- A model may have encountered this public episode during training; freezing gold cannot remove that risk.
- One output per input turn cannot represent multiple atomic claims. Split by human-reviewed atomic spans before a claim-level benchmark; do not advertise turn recall as claim recall.
- The 24-turn model window can lose old referents and duplicate memory. Semantic suppression is prompted, not proven; the validator only rejects an alert explicitly marked as a duplicate.
- Schema fidelity does not prove normalized-claim fidelity, honest confidence or prompt-injection resistance.
- No actual model identity, latency, usage or cost measured. The adapter records returned metadata on a successful run. Provider pricing and model compatibility must be checked at run time.
- The adapter stops on API/contract failures; it does not substitute a baseline. This favors trustworthy evaluation over availability. Do not mix a failed run with a completed score.

## Gate to reconsider

Before a GO: freeze audio-verified development and separately withheld conversation labels; use two independent annotators blinded to predictions, adjudicate disagreements, record agreement; run the unchanged baseline and fixed model prompt; review all critical misses and false alerts. Require the existing provisional targets (P@5 >=0.80, critical recall >=0.90, false alerts <=2/10 min, speaker fidelity >=0.95), no duplicate alerts on tested cases, faithful directed targets/quotes, and a documented improvement over baseline without a restraint regression. Show denominators and treat small samples as pilot evidence. Lock thresholds before holdout. If the holdout has fewer than five urgent gold claims, report shortlist precision and do not claim that P@5 alone determines quality.

No Android, ASR, retrieval or source-verification application work is justified yet.

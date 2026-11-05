# Decision policy v0.1 — NOT a fact-checker

## Inputs

Timestamped utterance stream: `{id, start_s, end_s, speaker, text, context_ids?}`. Preserve the raw text. Unknown speaker is allowed. Keep segment provenance rather than manufacturing an exact quote.

## Two separable stages

**Stage A: checkability / intent:** does the utterance assert a specific publicly checkable fact, ask for a check, present a testable hypothesis, request clarification, or merely express an opinion / joke / anecdote?

**Stage B: priority / timing:** given the recent conversation, does verifying now improve the discussion? Consider centrality, consequence if wrong, specificity, novelty, public evidence availability, confidence in transcription, cost/latency, and whether the claim was already addressed.

## Decisions

`VERIFY_NOW`, `QUEUE`, `NEEDS_CONTEXT`, `IGNORE`.

An explicit direction such as "check that" should not be interpreted as a factual claim; resolve the referent from a rolling context window. If no confident target exists, output `NEEDS_CONTEXT` rather than inventing one.

A hypothesis is not automatically false. An opinion is not a checkable factual claim unless it embeds separate testable premises. Statements with hedges can still contain checkable claims. "No evidence exists" is an evidence-availability claim and should not be silently turned into "X is impossible". Do not merge claims from opposing speakers.

Speaker attribution must preserve *assertion vs quotation vs rejection*. Evidence being displayed in the recording may not be available from text; mark `requires_visual_context` when relevant.

## Required candidate fields

```
{
  "segment_id": "s17",
  "time_start_s": 11822.0,
  "time_end_s": 11827.0,
  "speaker": "unknown",
  "verbatim": "...original transcript sentence...",
  "normalized_claim": "...faithful, conservative rewrite...",
  "kind": "empirical|numerical|attribution|hypothesis|opinion|instruction|other",
  "decision": "VERIFY_NOW|QUEUE|NEEDS_CONTEXT|IGNORE",
  "priority_0_5": 0,
  "confidence_0_1": 0.0,
  "reason": "one concise sentence",
  "context_ids": [],
  "repeat_of": null,
  "requires_visual_context": false,
  "truth_verdict": null
}
```

`truth_verdict` **must remain null** in Phase 0. This field is deliberately included to prevent accidental blending of selection and verification tasks. If a model cannot cite a segment, do not fabricate the quote.

## Initial model prompt candidate (not yet calibrated)

> You are a selective fact-check triage engine, not a fact-checker. Given sequential conversation turns and a bounded recent context, identify *specific* claims worth checking, plus important explicit instructions. Preserve who asserted what. Never infer that a hypothesis is false from its novelty; distinguish direct assertions from speculation, quoting and rebuttals. Rank only candidates whose checking would materially help the discussion. Return strict JSON conforming to the project schema. Do not fetch sources, do not issue factual verdicts, and suppress repetitive low-impact alerts. If a referent or speaker is unclear, say so. Prefer silence over low-confidence interruptions.

## Safety/credibility constraints

- A source count alone does not establish truth; assess independence and evidentiary quality in a later stage.
- Do not present generated verdicts as established facts without sources and appropriate uncertainty.
- Keep human review and override available for consequential claims.
- Keep transcripts and secrets out of publicly accessible repos unless explicitly authorized and licensed.

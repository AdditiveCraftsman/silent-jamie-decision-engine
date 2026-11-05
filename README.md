# Silent Jamie — Decision Engine (Phase 0)

A **transcript-first, evidence-aware claim-selection experiment** for a future silent, real-time podcast research copilot.

**Goal:** identify *which* statements deserve investigation, preserve their wording/context and speaker attribution, and choose *when* to surface a research request. **Not yet:** automatic factual verdicts, voice capture, Android PWA, autonomous web search, or a claim of proven performance.

## Current phase / acceptance gate

1. Manually annotate a timestamped, speaker-attributed 11-minute dialogue sample.
2. Run a deterministic rules-only baseline and a separately configured LLM claim selector on exactly the same sample.
3. Compare rankings, false alarms, missed critical claims, context/attribution errors, and cost. Keep the gold labels hidden from the selector.
4. Repeat on a held-out conversation; only then consider real-time audio.

### Pilot source

- JRE #2136 — Graham Hancock and Flint Dibble, 16 April 2024.
- Development window **03:17:00–03:28:00**; [timestamped transcript](https://jre.ai/episodes/2136-graham-hancock-flint-dibble/transcript).
- Transcript is unofficial/automatically generated; spot-check against the original audio.
- An existing third-party fact-check collection for this episode must be used **only for later external comparison**, not as a seed or answer key for initial selector testing: <https://www.factcheckjoerogan.com/episodes/jre-2136>.
- **Do not commit third-party full transcripts or audio**. Acquire content through authorized access or paste a local excerpt privately. Repository stores source URL/time ranges, original example fixtures, and annotations only if legally shareable.

### Run baseline (Python 3.10+, no third-party dependencies)

```sh
python -m silent_jamie.engine data/fixtures/synthetic.jsonl -o /tmp/sj-predictions.jsonl
python -m silent_jamie.evaluate data/fixtures/synthetic_gold.jsonl /tmp/sj-predictions.jsonl
python -m unittest discover -s tests -v
```

On Windows PowerShell, use `-o .\predictions.jsonl` instead of `/tmp/...`.

### What a label means

- `VERIFY_NOW`: specific public fact that materially affects the discussion, or an explicit check request with a resolved target.
- `QUEUE`: checkable but not worth interrupting, or a consequential hypothesis whose evidence basis deserves examination.
- `NEEDS_CONTEXT`: reference or instruction cannot be resolved without surrounding dialogue.
- `IGNORE`: opinion, trivial aside, repetition, unverifiable personal anecdote, or non-assertive question.

All classifications are **prioritization**, not truth verdicts. Lack of evidence is not automatic proof of falsity.

## Repository guide

- `docs/PRIOR_ART.md`: audited alternatives and reuse/licensing notes.
- `docs/BENCHMARK.md`: scoring protocol and leakage controls.
- `docs/DECISION_POLICY.md`: normative specification + structured result fields.
- `docs/WORK_MODE_HANDOFF.md`: Work-mode execution instructions and GitHub creation checklist.
- `docs/FUTURE_STACK.md`: Android/laptop architecture deferred until Phase 0 gate.
- `data/episodes/jre_2136_manifest.json`: source metadata only.
- `data/fixtures/`: *original synthetic* dialogue + illustrative labels.
- `silent_jamie/`: basic, intentionally weak, offline baseline + evaluation CLI.

## Status

Prepared as a **Git-ready local starter**, not a remote GitHub repository. It is designed for import into a new GitHub repo called `silent-jamie-decision-engine`. The baseline has unit tests; no real JRE evaluation or external-model benchmark has yet been completed.

## License

MIT for the new code and documentation in this repository only; third-party sources have their own terms. No upstream code is copied.

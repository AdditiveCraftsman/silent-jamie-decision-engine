# Evaluation protocol v0.1

## Split design

- **Development:** JRE #2136 at 03:17:00–03:28:00. Obtain transcript by authorized means and independently verify speaker/time alignment against audio. Label only then run candidate engines.
- **Holdout A:** a **different, unseen JRE episode** and topic, chosen before tuning. Do not use publicly posted claim lists when constructing the input to the selector.
- **Holdout B:** an original 5–10-minute bilingual conversation, recorded with informed consent or scripted and spoken by volunteers.

### Human annotation

For each atomic, timestamped claim or span label: speaker; original text; checkability; `VERIFY_NOW/QUEUE/NEEDS_CONTEXT/IGNORE`; importance 0–5; whether source context/image is needed; whether quote is attributed; repeat/duplicate relations. At least two passes or a second independent reviewer if possible. Record disagreements explicitly. Manual gold labels are **not** the final truth of any claim.

### Metrics / targets (provisional, not measured)

- Precision@5 of `VERIFY_NOW` shortlist: ≥ 0.80 against gold top-priority claims.
- Recall of *critical* claims: ≥ 0.90, with all misses manually reviewed; 100% ideal but not statistically robust on 11 minutes.
- False live alerts: ≤ 2 per 10 minutes for one pilot recording.
- Correct speaker attribution among selected claims: ≥ 0.95 where speakers are known.
- Duplicated claim alerts: zero desired.
- Context/quote fidelity: manual exact-span audit.
- Later (live) measure time-to-card, model/API cost per hour, and missed check requests.

Report precision, recall and confusion counts with denominator sizes. An 11-minute pilot is a smoke test, **not** a defensible production performance claim. Rate source quality separately from claim-selection quality.

### Leakage controls

1. Do not feed a published fact-check list (including JRE #2136) into the candidate selector or gold label creation.
2. Freeze labeled test sets before prompt tuning; store version, date, annotator and any changed labels.
3. Do not tune thresholds on held-out data. Use another episode for unbiased testing.
4. Report which API models were used and whether they may have seen published JRE claims during training. Episode publicness is a residual contamination risk.
5. Preserve dataset URLs/timestamps only in GitHub. Copyrighted transcripts stay local unless you have redistribution rights.

### Gold schema

Original synthetic example gold is in `data/fixtures/synthetic_gold.jsonl`, with `{id, decision, priority_0_5, critical}`. The gold labels expect `s07` ("check that last date") to resolve to `s04`; the deliberately context-free baseline misses it. This illustrates why a keyword-only system is insufficient. Real gold labels should be produced as a separate annotation file before running the model.

### Readout

The engine is useful only if it beats the simple baseline on priority and restraint, not merely claim count. Compare with unassisted manual work: how many claims a human editor would have wanted to review, and how many false interruptions they would tolerate.

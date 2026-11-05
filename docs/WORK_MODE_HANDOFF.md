# Work-mode execution handoff — 2026-11-04

## Job

Organize and implement **Phase 0** of Silent Jamie, a selective claim-triage engine. Target GitHub account: `AdditiveCraftsman`. Requested new repository: `silent-jamie-decision-engine`, public, MIT, initial `main` branch. The remote **has not been created by the current chat** because the connected GitHub action catalog supports writing files/issues in existing repos but has no create-repository action.

## Start in Work

1. Read this README, PRIOR_ART, BENCHMARK, DECISION_POLICY, FUTURE_STACK and the synthetic fixture. Confirm `AdditiveCraftsman/silent-jamie-decision-engine` is not already present, then create **that new repo** (do not repurpose `transcript_knowledge_extractor`). Import scaffold, commit to `main`, and verify the remote files and public visibility.
2. Use JRE #2136 transcript 03:17:00–03:28:00 as the *development* transcript. Confirm timestamps and speaker attribution. Do not upload full copyrighted dialogue to the public repo. Keep source locally or in a private dataset. Public `data/episodes/jre_2136_manifest.json` stores only URL/time.
3. Build manual gold labels independently of external fact-check catalogs. Use at least one holdout from a different episode/topic, freeze gold before tuning.
4. Implement a real, model-based selector as an **optional adapter** behind the schema. Maintain deterministic baseline for comparison. Report model name/version, input/output tokens, latency, and cost. Never ask the model to issue verdicts during Phase 0.
5. Evaluate prioritization and restraint: precision@5, critical recall, false alerts/10 min, exact-span attribution, duplicate suppression. Analyze all misses and false positives.
6. Stop at the decision gate. Only if useful, propose a later phone-first PWA and local ASR under a separate issue/PR. The most important gap is selective intervention, not software infrastructure.
7. Create GitHub issues: `Pilot transcript provenance & annotation`, `Model selector adapter & JSON schema`, `Gold set + evaluation`, `Holdout/bilingual test`, `Phase 0 go/no-go`. Keep milestones separate from future live/PWA work.

## Constraints

- Do not imply transcript-derived verdicts are objectively true; only collect what would be checked.
- Do not scrape or redistribute unauthorized copyrighted content.
- Do not paste API keys into repo, GitHub issues, or logs.
- License-check before copying upstream source; none is needed for this starter.
- `Tattle` is Mac-specific; `truth-in-stream` is larger than we need. Inspect rather than cloning wholesale.
- User wants the job executed in **ChatGPT Work mode**; ordinary Chat mode cannot toggle into Work autonomously. Use Work's cloud browser when available to create the repository and drive the multi-step validation.

## Definition of done

A public `AdditiveCraftsman/silent-jamie-decision-engine` repository with reproducible offline baseline and evaluation; a sourced, human-annotated pilot; model-vs-baseline results, limitations and go/no-go; no copied copyrighted transcript in Git history; open follow-on issues.

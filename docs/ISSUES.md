# GitHub milestones — 2026-11-05

Repository: https://github.com/AdditiveCraftsman/silent-jamie-decision-engine

Original starter snapshot published unchanged as `7c316f9a1a1948ba09fd257d1c8dbbe261e446a7` (tree equals local original). Public visibility and main verified.

## 1. Obtain audio-aligned JRE development spans and independent reference

Freeze [03:17:00,03:28:00) with private context buffer. Record authorized audio/video source and timestamp offset. Verify every speaker change, display dependency, transcription correction and boundary split. Two human annotators, blind to selector predictions and external fact-check pages, label atomic spans, decisions, priority, critical flags, targets, quote stance and repeats. Adjudicate disagreements and publish agreement statistics only where rights allow. Freeze hashes before inference. Agent-created labels cannot be called independent human gold.

## 2. Run fixed LLM selector against unchanged baseline

Adapter and contract are implemented; real inference remains pending. Configure an explicit versioned model at a local/OpenAI-compatible endpoint. Freeze prompt hash and configuration. Run same private input causally; record input hashes, returned model, tokens, latency, fingerprint where supplied, provider rates and actual cost. Test real JSON compatibility, failure handling and quote semantics. No fallback substitution. Gold must never enter selector payloads. Atomic segmentation remains necessary for claim-level recall.

## 3. Add diagnostic references and blind qualitative review

Cover central versus trivial claims, hypotheses, quotation/rejection, Spanish/English code-switching, explicit versus quoted instructions, ambiguous referents, semantic duplicates, renewed checks and missing visuals. Human review normalized claim fidelity and priority ranking. Report all misses/false alarms and denominators. Synthetic scenarios are regression tests only.

## 4. Freeze and evaluate separate unseen conversation

Choose a different episode and topic before tuning; reserve a consenting bilingual real conversation if available. Annotator holds the reference until prompt/configuration lock. No transcript selection based on known fact-check lists. Record model training contamination risk. No post-holdout prompt revision presented as unseen performance.

## 5. Phase 0 decision gate

Reconsider NO-GO only with valid human references and completed model-vs-baseline development and holdout results. Review restraint, critical recall, priorities, directed targets, duplicate alerts and fidelity alongside provisional numerical targets. Failure or absent evidence keeps real-time prototype blocked. A future phone/ASR issue is deferred, not an active implementation milestone.


Issues #1–#5 correspond to these headings and were created with these acceptance criteria.

# Prior art — reviewed 2026-11-04

**Thesis:** live fact-checking is **not novel**. The part to evaluate is selective timing, precision, context preservation, user-directed triggers, false-alert control, and bilingual mobile presentation.

| Reference | Verified approach | What to reuse / learn | Limitation for Galaxy A16 + Windows laptop |
|---|---|---|---|
| [Tattle](https://github.com/nicolasdao/tattle) | BSD-3-Clause; Mac app, live speech, Jev fast per-utterance judgments, slower model for research, dedup/memory and replay-gated criteria updates | Most relevant architectural inspiration: fast judgment gate -> research queue; negative cases and replay gate. Study `docs/system1-system2.md` | Requires Apple Silicon Mac and macOS, not usable directly on Windows/Android. Jev is a service dependency, not open weights. |
| [Live Fact Checker](https://github.com/alandaitch/live-fact-checker) | MIT Chrome desktop extension, local Whisper or YouTube captions, Gemini grounded verification, sequential rate-limited queue, Spanish UI | Testable claim extraction, separate verification queue, report and source links | Desktop side-panel Chrome extension, not a native Android Chrome solution. Gemini service required. |
| [VideoDB Fact Checker](https://github.com/video-db/fact-checker) | Mac/Electron, VideoDB realtime capture, ~20-second transcript windows, Gemini verification, alert dedup and cooldown | Alert cooldown, context-window tracking, graceful reconnect | Mac-centric capture and external API keys; license not established from repository root. |
| [truth-in-stream](https://github.com/verovec/truth-in-stream) | Responsive Next.js + Go server, PostgreSQL/pgvector, AssemblyAI, Voyage, verifier model, seeded offline demo | Evidence retrieval, cache/replay, evidence-linked UI, structured pipeline | Far heavier stack than our Phase 0; repo root showed no LICENSE (check terms before reuse). Offline demo does not imply offline live transcription. |
| [CheckThat! 2024 Task 1](https://checkthat.gitlab.io/clef2024/task1/) | Published benchmark for **check-worthiness** using speech/debate transcripts and English/Spanish | Existing evaluation concepts and multilingual baselines | Domain shift to podcasts; check dataset licenses before redistributing |
| [Fact Check Joe Rogan JRE #2136](https://www.factcheckjoerogan.com/episodes/jre-2136) | 18 published, timestamped source-linked claim reviews for this specific episode as of Sep 2026 | Later reference for recall/verification quality only | Do not use during first selection pass; risks answer leakage; not exhaustive gold annotations |
| [Transcript Knowledge Extractor](https://github.com/AdditiveCraftsman/transcript_knowledge_extractor) | Existing user-owned public Netlify YouTube transcript extractor using `youtube-transcript` | Optional ingestion helper later | Separate purpose; do not overwrite or couple to engine until authorized |

## Reuse decision

1. Do **not** rewrite transcription, live streaming, or full verification now.
2. Build only a transparent benchmark harness, a simple baseline, a common classifier output contract and a labeled test set.
3. Examine Tattle's decision policy as prior art, but do not copy its code or claims of performance; reproduce independently and compare honestly.
4. Keep a clean protocol for free-text queries and directed triggers, since avoiding an interrupt can matter more than being able to retrieve a source.
5. Before adopting any code, check package license, transitive dependencies, maintenance, deployment needs, and Windows/Android compatibility.

Evidence read: upstream README and for Tattle `docs/mission.md`, `docs/jev.md`, `docs/system1-system2.md`; repository metadata/structure checked through GitHub on 2026-11-04. This is a functional prior-art comparison, not a security or production audit.

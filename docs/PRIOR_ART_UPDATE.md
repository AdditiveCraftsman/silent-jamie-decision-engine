# Prior art update — 2026-11-05

Targeted primary-source check before implementation. This supplements, rather than silently re-certifies, the starter's older table. No upstream code copied and no substitute was benchmarked locally.

| Alternative | Evidence checked | Useful comparison | Decision |
|---|---|---|---|
| [Tattle](https://github.com/nicolasdao/tattle) | GitHub API: BSD-3-Clause, not archived, default branch master, pushed 2026-10-28; indexed README describes Apple speech/OpenAI and a Jev decision gate | Closest live triage/memory architecture | Study/replay its selectivity; Mac orientation and service dependencies remain mismatched to this experiment |
| [Live Fact Checker](https://github.com/alandaitch/live-fact-checker) | Primary README; API: MIT, pushed 2026-02-13 | Desktop extension extraction and sequential verification | Full extension/grounded verification is beyond Phase 0; no evidence it solves contextual producer instructions |
| [ClaimBuster](https://claimbuster.org/) / [API](https://idir.claimbuster.org/api/) | Official site and endpoint documentation | Stronger established check-worthiness baseline than our keyword rules; BERT ClaimSpotter text/sentence scoring | Add as a comparator if key/access and training-code licensing permit. Registration/key required; no scores collected. Did not establish a current downloadable weights license |
| [Loki](https://github.com/Libr-AI/OpenFactVerification) | Primary README and API: MIT, pushed 2024-10-03 | Separates decomposition, check-worthiness, query creation, retrieval and verification | Useful modular prior art; full pipeline adds unnecessary scope; no local installation or latency claim |
| [ContextClaim](https://arxiv.org/abs/2603.30025) | Primary abstract: submitted 2026-03-31, revised 2026-08-18 | Newer verifiability research using structured external context | Relevant research, but knowledge context is different from causal conversational context. Not verified as a drop-in licensed implementation |
| [CheckThat! 2026 Task 1](https://checkthat.gitlab.io/clef2026/task1/) | Official current task definition | Scientific source retrieval | It is NOT the older check-worthiness task. Keep older task framing for selection; do not assume a stable task number across years |

**Conclusion:** there is no novelty claim for live fact-checking or claim detection. Reuse evaluation concepts; implement only the small causal adapter, provenance checks and missing diagnostic harness. A targeted search cannot prove no better project exists. None of the checked sources establishes superior performance on the proposed development/holdout split.

The older table's remaining projects and license statements were not all re-audited in this update; do not adopt their code based solely on the starter.

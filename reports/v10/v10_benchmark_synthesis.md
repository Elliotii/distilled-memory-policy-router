# v10 Benchmark Synthesis

This report closes the Context 6.4 benchmark work for v1.0 packaging. It synthesizes the no-inference downstream-lite proxy, the LLM downstream-lite prompt-pack design, and the 14-response DeepSeek V4 Flash micro-pilot.

## 6.4-A Downstream-Lite Proxy

The proxy benchmark replays locked `gold_v2_009` cases and saved BF16 r16 1000_4090 router predictions. It does not load Qwen, run inference, call APIs, evaluate retrieval, or measure real cost or latency.

Main proxy findings:

- `router_selected` injects fewer memories than `all_candidates`: 2.78 selected memories per case versus 3.42.
- `router_selected` reduces selected-memory count by 18.7% versus all-candidates injection.
- `router_selected` retains most gold READ recall: 85.2% versus 100.0% for `all_candidates` and `oracle_selected`.
- `router_selected` reduces irrelevant selected memories versus all-candidates injection: 65 irrelevant memories versus 100, a 35.0% reduction.
- The proxy does not clearly distinguish `router_selected` from naive/random baselines. `top_k_naive` reaches 83.8% gold READ recall, `random_k` reaches 85.0%, and `shuffled_top_k` reaches 84.0%.

Conservative interpretation: the saved router predictions reduce injected context versus all-candidates injection while preserving many labeled READ memories, but the replay is not strong evidence that the router beats simple ordering-sensitive or shuffled top-k baselines.

## 6.4-B LLM Downstream-Lite Design

The LLM downstream-lite design prepared an execution-ready prompt pack and judge/audit structure. No LLM was executed at that stage.

Prepared assets included:

- derived downstream-lite cases;
- a multi-strategy prompt pack;
- memory-id citation instructions;
- expected required and avoid memory IDs;
- contradiction-risk filtering;
- attribution and audit trace scaffolding;
- a judge rubric for later response-level review.

The design stage established the harness shape:

```text
current task notes + injected memory context -> fixed downstream LLM response
```

It remained a design and packaging step only. It did not evaluate answer quality, real retrieval, live router inference, or memory lifecycle behavior.

## 6.4-C DeepSeek Micro-Pilot

The C-stage executed a tiny LLM downstream-lite micro-pilot:

- Cases: 2
- Strategies: 7
- Responses: 14
- Model recorded in responses: `deepseek-v4-flash`
- API result: 14/14 OK, 0 errors
- Full 42-prompt pilot: not run

The API runner and citation scorer worked. The initial citation behavior required repair: prompt text exposed current-unit IDs such as `u1`, which encouraged invalid citations such as `[u2]`. C1-R and C1-R2 repaired citation instructions and prompt rendering so current-unit IDs are hidden from LLM-facing prompt text while memory IDs remain visible.

Current scored citation diagnostics after repair:

- Current-unit citations: 0 average invalid current-unit citations for every strategy.
- Bare memory references: 0 average bare memory references for every strategy.
- Hallucinated memory citations: 0 average hallucinated citations for every strategy.

Automatic citation recall remained partial and not equivalent to task quality. A rubric-based internal qualitative review was then completed over the 14 existing responses.

Strategy-level internal utility averages:

| Strategy | Rows | Utility |
| --- | ---: | ---: |
| `all_candidates` | 2 | 6.000 |
| `router_selected` | 2 | 6.000 |
| `shuffled_top_k` | 2 | 6.000 |
| `oracle_selected` | 2 | 5.500 |
| `random_k` | 2 | 5.500 |
| `top_k_naive` | 2 | 5.000 |
| `no_memory` | 2 | 3.000 |

The micro-pilot suggests memory context helps over no memory in these two cases. It does not prove router-specific downstream superiority: `router_selected` tied with `all_candidates` and `shuffled_top_k` on the internal qualitative utility score.

Case-level interpretation:

- `v05e_gold_active_0002` is mostly a sanity-check case because memory-injecting strategies converge.
- `v05e_gold_active_0006` is more informative because strategy differences change which memories are injected and cited. `router_selected` uses `m2` and `m4` but misses `m3`; `oracle_selected` has all gold memories but does not cite all of them; `shuffled_top_k` uses `m3` and `m4` while omitting `m2`.

## v1.0-Facing Claims

Allowed v1.0 claims:

- The memory-injection harness scaffold works at the artifact and prompt-pack level.
- The no-inference replay proxy is reproducible over locked gold and saved prediction artifacts.
- The LLM downstream-lite prompt pack, micro-pilot response collection, citation scoring, and internal rubric review are reproducible.
- The 14-response micro-pilot suggests that memory context helps over no memory in the reviewed cases.
- Citation-format repair was effective for the current micro-pilot artifacts.

Claims not supported:

- General downstream benefit has not been established.
- Router-specific superiority over baseline memory-injection strategies has not been established.
- Production cost or latency benefit has not been measured.
- Retrieval from a live memory store has not been evaluated.
- Production safety has not been established.
- The project does not implement a comprehensive memory operating system, complete memory lifecycle system, or end-to-end agent.

## Recommendation

Close Context 6.4 for v1.0.

For v1.0, report the benchmark work as a conservative research-engineering scaffold plus a tiny diagnostic micro-pilot. Do not expand to the full 42-prompt pilot during v1.0 packaging.

Future work for v1.1:

- Run the full 42-prompt LLM downstream-lite pilot.
- Add manual or judge scoring as a required companion to automatic citation scoring.
- Track stale-current-context use explicitly.
- Evaluate live LoRA/router behavior only in a later context.
- Revisit whether router-selected memory injection separates from stronger baselines on a larger, less ordering-confounded prompt set.

The next context should be 6.5 resume/interview packaging.

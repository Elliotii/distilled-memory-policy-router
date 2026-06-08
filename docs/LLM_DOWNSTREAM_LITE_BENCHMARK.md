# LLM Downstream-Lite Benchmark

This benchmark is an execution-ready prompt-pack design for testing whether selected candidate memories help a downstream LLM write a concise, grounded task response with less context pollution.

It simulates the memory-injection stage of a small agent memory harness:

```text
current task notes + injected memory context -> downstream LLM response
```

The benchmark compares memory injection policies. It is not a retriever test, live router inference run, memory database, writer/updater benchmark, or downstream proof. A tiny 14-response micro-pilot has been executed and internally reviewed, but the full 42-prompt pilot remains future work.

## Inputs

- Locked source cases: `data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl`
- Saved router predictions: `data/v05g/model_predictions/bf16_r16_1000_4090_gold_v2_009_predictions.jsonl`
- Derived cases: `data/v10/llm_downstream_lite/llm_downstream_lite_cases.jsonl`
- Prompt pack: `data/v10/llm_downstream_lite/llm_downstream_lite_prompt_pack.jsonl`

The derived files are review-required fixtures. They are not new locked gold and are not part of the locked v0.5 evaluation.

## Strategies

| Strategy | Injected memory context |
| --- | --- |
| `no_memory` | No candidate memories. |
| `all_candidates` | Every supplied candidate memory. |
| `router_selected` | READ IDs parsed from saved BF16 r16 1000_4090 router predictions. |
| `oracle_selected` | Gold READ IDs from the locked case. |
| `top_k_naive` | First three candidate memories by original order. |
| `random_k` | Three candidate memories from a fixed per-case deterministic shuffle. |
| `shuffled_top_k` | First three candidate memories after a second fixed per-case deterministic shuffle. |

## Prompt-Pack Schema

Each prompt object has:

```json
{
  "prompt_id": "case_id__strategy",
  "case_id": "source case id",
  "strategy": "no_memory|all_candidates|router_selected|oracle_selected|top_k_naive|random_k|shuffled_top_k",
  "source": {},
  "injected_memory_ids": [],
  "current_units": [],
  "prompt_text": "downstream answer prompt",
  "expected_required_memory_ids": [],
  "expected_injected_required_memory_ids": [],
  "expected_avoid_memory_ids": [],
  "contradiction_risk": {},
  "rubric": {},
  "limitations": "execution and claim-boundary note"
}
```

The prompt asks the downstream LLM to write a short assistant response or task update using only the available memory context. It does not ask the LLM to solve the router classification task and does not expose gold labels.

Every prompt requires memory-id citation when memory facts are used:

```text
When you use a memory fact, cite its memory id in brackets, e.g. [m2].
Do not cite memory ids for facts not present in the provided memory context.
```

The output is constrained to 80 words or fewer and no more than four sentences, with one concise next action and a memory-backed rationale using citations where applicable.

## Judge Rubric

Later manual or LLM-judge scoring should use these fields:

| Field | Direction | Meaning |
| --- | --- | --- |
| `required_memory_fact_coverage` | Higher is better | Whether required memory facts are used correctly. |
| `conditional_injected_required_coverage` | Higher is better | Optional diagnostic over required memory facts that were actually injected. |
| `irrelevant_memory_contamination` | Lower is better | Whether irrelevant injected memories contaminate the response. |
| `hallucinated_memory_usage` | Lower is better | Whether the response invents unsupported memory facts. |
| `citation_accuracy` | Lower is better | Whether citations match memory facts present in the provided context. |
| `task_response_quality` | Higher is better | Whether the response is concise, grounded, and useful. |

The headline `required_memory_fact_coverage` score is end-to-end against the gold-required memory IDs, regardless of what the strategy injected. If `router_selected` or another strategy fails to inject a required memory, downstream coverage should lose credit. `conditional_injected_required_coverage` is an optional decomposition to separate "the policy did not inject the fact" from "the LLM ignored an injected fact."

Suggested score:

```text
required_memory_fact_coverage + task_response_quality - irrelevant_memory_contamination - hallucinated_memory_usage - citation_accuracy
```

## Contradiction Handling

The builder adds a `contradiction_risk` field to each case and prompt. For this v1.0 execution pack, cases with a simple numeric contradiction pattern between candidate memories and current units are excluded from the main pack rather than silently mixed into normal prompts. They can be revisited later as explicitly labeled stress tests.

## Audit Trace

The builder also prepares `data/v10/llm_downstream_lite/llm_downstream_lite_audit_trace_template.jsonl`. Future execution should fill response-dependent fields such as `cited_memory_ids`, missing required citations, irrelevant citations, hallucinated citations, and judge scores.

## Micro-Pilot Status

A C1/C2 micro-pilot executed 2 cases across 7 strategies for 14 DeepSeek V4 Flash responses:

- API status: 14/14 OK, 0 errors.
- Citation scoring ran successfully.
- Citation-format repair hid current-unit IDs from LLM-facing prompt text while keeping memory IDs visible.
- The current scored artifacts show no current-unit citations, no bare memory refs, and no hallucinated memory citations.
- A rubric-based internal qualitative review was completed over the 14 responses.

Internal utility averages from the micro-pilot:

| Strategy | Rows | Utility |
| --- | ---: | ---: |
| `all_candidates` | 2 | 6.000 |
| `router_selected` | 2 | 6.000 |
| `shuffled_top_k` | 2 | 6.000 |
| `oracle_selected` | 2 | 5.500 |
| `random_k` | 2 | 5.500 |
| `top_k_naive` | 2 | 5.000 |
| `no_memory` | 2 | 3.000 |

The micro-pilot suggests that memory context helped over no memory in these two reviewed cases. It does not prove downstream utility and does not prove router-specific downstream superiority, because `router_selected` tied with `all_candidates` and `shuffled_top_k`.

See `reports/v10/v10_benchmark_synthesis.md` for the v1.0-facing synthesis.

## Future Execution

1. Review `reports/v10/llm_downstream_lite_design_report.md`.
2. Review the generated prompt pack for clarity and safe wording.
3. Add manual or judge scoring as a required companion to automatic citation scoring.
4. Save raw responses in a separate response JSONL file.
5. Score responses with `reports/v10/llm_downstream_lite_judge_template.md`.
6. Fill or derive the audit trace fields after response collection.
7. Report results by strategy with uncertainty and examples.

## Limitations

- The set is small and curated.
- Candidate memories are fixed; no real retriever is implemented.
- Router-selected prompts use saved predictions, not live router inference.
- Only a tiny 14-response micro-pilot has been executed; the full 42-prompt pilot has not been run.
- No production safety claim is supported.
- No general downstream conclusion is supported by the micro-pilot.

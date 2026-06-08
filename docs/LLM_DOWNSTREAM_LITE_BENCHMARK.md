# LLM Downstream-Lite Benchmark

This benchmark is an execution-ready prompt-pack design for testing whether selected candidate memories help a downstream LLM write a concise, grounded task response with less context pollution.

It simulates the memory-injection stage of a small agent memory harness:

```text
current task notes + injected memory context -> downstream LLM response
```

The benchmark compares memory injection policies. It is not a retriever test, live router inference run, memory database, writer/updater benchmark, or downstream proof until the prompts are executed and judged.

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

## Prompt-Pack Schema

Each prompt object has:

```json
{
  "prompt_id": "case_id__strategy",
  "case_id": "source case id",
  "strategy": "no_memory|all_candidates|router_selected|oracle_selected|top_k_naive",
  "source": {},
  "injected_memory_ids": [],
  "current_units": [],
  "prompt_text": "downstream answer prompt",
  "expected_required_memory_ids": [],
  "expected_avoid_memory_ids": [],
  "rubric": {},
  "limitations": "execution and claim-boundary note"
}
```

The prompt asks the downstream LLM to write a short assistant response or task update using only the available memory context. It does not ask the LLM to solve the router classification task and does not expose gold labels.

## Judge Rubric

Later manual or LLM-judge scoring should use four 0/1/2 fields:

| Field | Direction | Meaning |
| --- | --- | --- |
| `required_memory_fact_coverage` | Higher is better | Whether required memory facts are used correctly. |
| `irrelevant_memory_contamination` | Lower is better | Whether irrelevant injected memories contaminate the response. |
| `hallucinated_memory_usage` | Lower is better | Whether the response invents unsupported memory facts. |
| `task_response_quality` | Higher is better | Whether the response is concise, grounded, and useful. |

Suggested score:

```text
required_memory_fact_coverage + task_response_quality - irrelevant_memory_contamination - hallucinated_memory_usage
```

## Future Execution

1. Review `reports/v10/llm_downstream_lite_design_report.md`.
2. Review the generated prompt pack for clarity and safe wording.
3. Run each prompt under fixed model settings in a later context.
4. Save raw responses in a separate response JSONL file.
5. Score responses with `reports/v10/llm_downstream_lite_judge_template.md`.
6. Report results by strategy with uncertainty and examples.

## Limitations

- The set is small and curated.
- Candidate memories are fixed; no real retriever is implemented.
- Router-selected prompts use saved predictions, not live router inference.
- No model has answered these prompts yet.
- No production safety claim is supported.
- No general downstream conclusion is supported until responses are executed and judged.

# LLM Downstream-Lite Judge Template

Use this template only after collecting downstream LLM responses for the generated prompt pack. Do not score prompts before response collection.

## Response Collection Format

```json
{
  "prompt_id": "v05e_gold_active_0002__router_selected",
  "case_id": "v05e_gold_active_0002",
  "strategy": "router_selected",
  "model": "model name and version used later",
  "response_text": "assistant response text",
  "latency_ms": null,
  "token_usage": null,
  "notes": ""
}
```

## Scoring Rubric

| Field | Score 0 | Score 1 | Score 2 |
| --- | --- | --- | --- |
| `required_memory_fact_coverage` | Misses required memory facts. | Uses some required facts or uses them vaguely. | Uses the important required facts correctly. |
| `irrelevant_memory_contamination` | No irrelevant memory use. | Minor irrelevant mention. | Material irrelevant-memory contamination. |
| `hallucinated_memory_usage` | No invented memory facts. | Minor unsupported inference. | Clear invented memory facts. |
| `task_response_quality` | Not useful for the task. | Partially useful but incomplete or wordy. | Concise, grounded, and actionable. |

Lower scores are better for `irrelevant_memory_contamination` and `hallucinated_memory_usage`.

Suggested total:

```text
required_memory_fact_coverage + task_response_quality - irrelevant_memory_contamination - hallucinated_memory_usage
```

## Judge Output Format

```json
{
  "prompt_id": "v05e_gold_active_0002__router_selected",
  "scores": {
    "required_memory_fact_coverage": 2,
    "irrelevant_memory_contamination": 0,
    "hallucinated_memory_usage": 0,
    "task_response_quality": 2,
    "total_score": 4
  },
  "rationale": "Brief evidence-based note.",
  "judge_notes": ""
}
```

## Scoring Examples

- If a response uses the relevant repo command and service constraint, ignores an injected stale distractor, and gives a practical next step, score coverage 2, contamination 0, hallucination 0, quality 2.
- If a response mentions an unrelated user preference from the injected memories but still gives a useful task update, score contamination 1 and judge the other fields from the actual response.
- If a response invents a policy or memory fact that is not present in the prompt, score hallucinated memory usage 1 or 2 depending on severity.

## Warnings

- Do not compare strategies by anecdotes alone; aggregate by strategy and inspect examples.
- Do not treat oracle-selected as a deployable policy; it is a ceiling reference over locked labels.
- Do not claim downstream benefit until responses are collected and scored.
- Keep retrieval, writing, updating, and lifecycle claims out of this benchmark.

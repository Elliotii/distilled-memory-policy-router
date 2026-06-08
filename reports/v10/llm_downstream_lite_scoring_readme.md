# LLM Downstream-Lite Scoring README

`scripts/score_llm_downstream_lite_responses.py` computes partial automatic citation metrics for the pilot prompt pack. It is designed to check whether responses cite expected memory IDs, not whether the response is fully correct or useful.

## Inputs

- Prompt pack: `data/v10/llm_downstream_lite/pilot_prompt_pack.jsonl`
- Response JSONL: `data/v10/llm_downstream_lite/pilot_response_template.jsonl` or an executed response file with the same schema

The script reads these prompt fields:

- `expected_required_memory_ids`
- `expected_avoid_memory_ids`
- `injected_memory_ids`

It extracts citations from `response_text` using bracketed memory IDs such as `[m2]`.

## Automatic Metrics

| Metric | Meaning |
| --- | --- |
| `cited_memory_ids` | Unique bracketed memory IDs cited in the response. |
| `required_cited_count` | Required memory IDs that were cited. |
| `required_total_count` | Total expected required memory IDs for that prompt. |
| `end_to_end_required_citation_recall` | Required cited count divided by all required memory IDs, regardless of injection strategy. |
| `conditional_required_citation_recall` | Required cited count over required IDs that were actually injected. |
| `irrelevant_citation_count` | Cited IDs that were injected but listed as expected avoid IDs. |
| `hallucinated_citation_count` | Cited IDs not present in the injected memory context. |
| `no_response_count` | `1` when `response_text` is empty for a prompt, else `0`. |

## End-To-End Vs Conditional Coverage

End-to-end required citation recall is the headline automatic citation metric. If a strategy fails to inject a required memory, it should lose credit because the downstream response cannot cite that missing fact.

Conditional required citation recall is diagnostic. It only considers required memory IDs that were actually injected, helping separate policy drops from downstream LLM failures to use injected memory.

## What Still Needs Manual Judgment

Automatic citation scoring does not judge:

- task response quality;
- contradiction handling;
- hallucination without a memory ID citation;
- whether a cited memory fact was used correctly;
- answer usefulness or actionability.

Use the citation scores alongside manual or LLM-judge review before making any output-level claim.

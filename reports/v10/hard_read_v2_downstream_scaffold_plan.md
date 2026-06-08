# Hard READ v2 Downstream Scaffold Plan

Context: 7.4-E v2 downstream prompt-pack scaffold and manual prompt inspection.

## Why This Scaffold Exists

Context 7.4-D repaired the hard READ fixture after v1 showed two design risks: `no_memory` answers were too strong because task notes exposed much of the answer shape, and `budgeted_candidate_order` nearly matched oracle because candidate order was favorable. The v2 selection-only eval reduced the candidate-order bias, but it still cannot verify whether no-memory answerability is lower because no downstream responses are generated at the selection layer.

This scaffold creates prompt, response, and manual-review templates for a small v2 downstream micro-pilot. It does not call an API, run model inference, load Qwen or LoRA, train, or evaluate downstream answer quality.

## Selected Cases

| Case | Reason selected |
| --- | --- |
| `hard_read_v2_001` | Checkout retry case where required memories are not in the first four candidates. |
| `hard_read_v2_002` | Privacy export case with sensitive-boundary and stale risk. |
| `hard_read_v2_003` | Accessibility case where the first four candidates include a contradiction and no required memory. |
| `hard_read_v2_005` | Catalog-search case where the first four candidates contain no required memory. |
| `hard_read_v2_008` | Auth-gateway case with sensitive-boundary and contradictory distractors. |

## Strategies

The prompt pack covers six strategy contexts:

- `no_memory`
- `all_candidates`
- `budgeted_candidate_order`
- `keyword_top_k`
- `random_k`
- `oracle_selected`

Prompt count: 5 cases x 6 strategies = 30 prompts.

## Outputs

- `data/v10/hard_read_v2_downstream/hard_read_v2_downstream_prompt_pack.jsonl`
- `data/v10/hard_read_v2_downstream/hard_read_v2_downstream_response_template.jsonl`
- `data/v10/hard_read_v2_downstream/hard_read_v2_downstream_manual_review_template.jsonl`

The response template is intentionally empty with `api_status: "not_run"`. The manual template uses the same 0/1/2 rubric fields as v1: required fact coverage, irrelevant-memory contamination, stale or contradictory use, hallucinated memory use, task response quality, and citation compliance.

## v2 vs v1

- v2 uses shuffled candidate order rather than label-ordered candidate lists.
- v2 task notes are under-specified and omit exact command names, thresholds, deadlines, and implementation constraints.
- v2 prompt text hides labels, strategy names, oracle/gold wording, and current-unit IDs.
- v2 does not overwrite v1 hard-read downstream artifacts.

## Scorer Compatibility

`scripts/score_hard_read_downstream_responses.py` is compatible with the v2 prompt pack and response template for automatic citation checks. A dry run on the empty response template completed and produced 30 no-response rows. This scorer remains citation-only; it does not judge answer quality, contamination severity, or downstream utility.

## Claim Boundaries

This scaffold supports prompt inspection only. It does not establish downstream answer quality, compare learned routers against alternatives, establish production safety, measure real retriever behavior, or resolve READ selection. The oracle condition is a labeled reference context for inspection, not a deployable strategy.

## Next Recommendation

Recommended next context: Context 7.4-F — v2 downstream API micro-pilot execution, only after manual prompt inspection passes.

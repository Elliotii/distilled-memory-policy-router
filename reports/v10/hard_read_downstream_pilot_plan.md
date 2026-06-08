# Hard READ Downstream Pilot Plan

## Purpose

This scaffold prepares a downstream response pilot for the hard READ 10-case fixture set. It converts selected post-budget memory contexts into LLM-facing prompts, creates empty response and manual review templates, and adds an automatic citation scorer.

No API call, external LLM run, model inference, Qwen/LoRA loading, training, live LoRA backend, or UI work is performed in this context.

## Selected Cases

The pilot uses four cases from the 7.3 hard READ set:

- `hard_read_pilot_001`: checkout-api retry handling with stale, contradictory, and wrong-scope distractors.
- `hard_read_pilot_002`: privacy export task with sensitive-boundary and deadline memories.
- `hard_read_pilot_003`: renderer-service accessibility task with resolved incident distractors.
- `hard_read_pilot_009`: reporting-api export pagination task with stale export constraints.

These cases cover required memories, helpful memories, stale or harmful memories, contradictory memories, wrong-scope memories, and same-entity or near-duplicate distractors.

## Strategies

The prompt pack includes six strategies from the 7.3 selection eval:

- `no_memory`
- `all_candidates`
- `budgeted_candidate_order`
- `keyword_top_k`
- `random_k`
- `oracle_selected`

Prompts use post-budget injected memories from the 7.3 trace rows, not pre-budget selected memories.

## Prompt Count

Prompt count: 24, computed as 4 cases x 6 strategies.

## Prompt Rules

The prompt text asks for 2-4 concise bullets or sentences, capped at 120 words. Memory context uses bracketed memory IDs such as `[m001]`. Current task notes are rendered without current-unit IDs to avoid current-unit citation pollution.

The model is instructed to cite memory IDs only when using memory facts, avoid citing memory IDs outside the provided memory context, and avoid mentioning evaluation setup, labels, gold data, or selection methods.

## Reproducible Builder

Regenerate the prompt pack and empty templates with:

```bash
python3 scripts/build_hard_read_downstream_prompt_pack.py \
  --cases data/v10/hard_read/hard_read_pilot_cases.jsonl \
  --memory-pool data/v10/hard_read/hard_read_pilot_memory_pool.jsonl \
  --by-case reports/v10/hard_read_selection_eval/by_case.jsonl \
  --case-id hard_read_pilot_001 \
  --case-id hard_read_pilot_002 \
  --case-id hard_read_pilot_003 \
  --case-id hard_read_pilot_009 \
  --strategy no_memory \
  --strategy all_candidates \
  --strategy budgeted_candidate_order \
  --strategy keyword_top_k \
  --strategy random_k \
  --strategy oracle_selected \
  --out-prompts data/v10/hard_read_downstream/hard_read_downstream_pilot_prompt_pack.jsonl \
  --out-responses data/v10/hard_read_downstream/hard_read_downstream_pilot_response_template.jsonl \
  --out-manual data/v10/hard_read_downstream/hard_read_downstream_manual_review_template.jsonl
```

The builder uses post-budget injected memories from the 7.3 by-case rows. It does not expose relevance labels in prompt text.

## Synthetic Sensitive Placeholders

Some hard READ fixtures contain sensitive-looking placeholder strings for testing sensitive-boundary behavior. These are synthetic fixtures, not real secrets. The prompt builder redacts placeholder token values such as `ABC-123` to `<REDACTED_SAMPLE_TOKEN>` before any external API execution.

The 7.4-B API runner must send only `prompt_text` to the external API. It must not send side metadata labels such as required, helpful, avoid, stale, contradictory, or wrong-scope memory IDs.

## Claim Boundaries

This scaffold supports response collection and later review. It does not show downstream value, learned routing behavior, live LoRA behavior, production safety, real retrieval behavior, or that any router or selector outperforms baselines.

## Scoring Plan

The automatic scorer checks citation scaffolding only:

- valid memory citations;
- hallucinated memory citations;
- required citation recall;
- conditional required citation recall over injected required memories;
- avoid, stale, contradictory, and wrong-scope citations;
- bare memory refs;
- invalid current-unit citations;
- response coverage and no-response counts.

The scorer output is a partial automatic signal, not an answer-quality result.

## Manual Review Plan

Manual or rubric-based review should score:

- required fact coverage;
- irrelevant memory contamination;
- stale or contradictory use;
- hallucinated memory use;
- task response quality;
- citation compliance.

The manual review template is empty until responses are collected.

Rubric scale:

| Metric | Scale |
| --- | --- |
| `required_fact_coverage` | 0=no required facts, 1=partial, 2=complete |
| `irrelevant_memory_contamination` | 0=clear contamination, 1=minor/ambiguous, 2=none |
| `stale_or_contradictory_use` | 0=uses stale/contradictory facts, 1=mentions but resists, 2=none |
| `hallucinated_memory_use` | 0=clear hallucination, 1=minor unsupported fact, 2=none |
| `task_response_quality` | 0=not useful, 1=partly useful, 2=useful and actionable |
| `citation_compliance` | 0=bad/missing/invalid citations, 1=partial, 2=clean |

## Why No API Is Run In 7.4-A

This context prepares files and validation only. API execution is deferred so prompt construction, citation rules, response templates, and scoring behavior can be reviewed before any paid or external model call.

## Next Context Recommendation

Context 7.4-B - Hard READ downstream DeepSeek micro-pilot execution.

# LLM Downstream-Lite Pilot Plan

This pilot scaffold prepares a small execution-ready subset of the repaired LLM downstream-lite prompt pack. It does not execute prompts, call any model, call external APIs, or prove downstream utility.

## Selected Cases

| Case ID | Category | Rationale |
| --- | --- | --- |
| `v05e_gold_active_0002` | `full_exact_or_read_exact` | Clear media-transcoding service case with repo, service, and project memories all selected by router and gold. |
| `v05e_gold_active_0023` | `full_exact_or_read_exact` | Clear game-analytics case with current task-state units and three required memories. |
| `v05e_gold_active_0015` | `read_mismatch_write_correct` | Quantitative-research case where STORE/SKIP is correct but router drops one required READ memory. |
| `v05e_gold_active_0043` | `read_mismatch_write_correct` | Genomics-pipeline case with understandable current incidents and a READ mismatch. |
| `v05e_gold_active_0006` | `irrelevant_memory_reduction` | Real-estate-valuation case where router reduces irrelevant injected memory while missing one required memory. |
| `v05e_gold_active_0007` | `irrelevant_memory_reduction` | Accessibility-compliance case with an obsolete candidate memory and router-selected context reduction. |

All selected cases come from `data/v10/llm_downstream_lite/llm_downstream_lite_cases.jsonl`. Each selected case has `contradiction_risk.level == "none"` and uses the repaired prompt text with memory-id citation instructions.

## Pilot Size

- Cases: 6
- Strategies per case: 7
- Prompt rows: 42

Strategies:

- `no_memory`
- `all_candidates`
- `router_selected`
- `oracle_selected`
- `top_k_naive`
- `random_k`
- `shuffled_top_k`

## Execution Instructions

1. Use `data/v10/llm_downstream_lite/pilot_prompt_pack.jsonl`.
2. Collect one response per prompt into `data/v10/llm_downstream_lite/pilot_response_template.jsonl` or a copied response JSONL with the same schema.
3. Keep one fixed model for the whole pilot.
4. Use temperature `0`.
5. Record the exact model name and version in every response row.
6. Run citation scoring:

```bash
python3 scripts/score_llm_downstream_lite_responses.py \
  --prompts data/v10/llm_downstream_lite/pilot_prompt_pack.jsonl \
  --responses data/v10/llm_downstream_lite/pilot_response_template.jsonl \
  --out-json reports/v10/llm_downstream_lite_pilot_scores.json \
  --out-md reports/v10/llm_downstream_lite_pilot_scores.md
```

## Interpretation Rules

- Compare `router_selected` against `all_candidates`, `top_k_naive`, `random_k`, `shuffled_top_k`, and `oracle_selected`.
- If `router_selected` only matches naive or random baselines, report that directly.
- Treat `oracle_selected` as a ceiling reference, not a deployable strategy.
- Treat `no_memory` as a floor reference.
- Citation metrics are partial automatic checks, not full answer-quality judgments.

## C1-R Citation Repair

The first C1 micro-pilot run showed citation-format issues: some responses used bare memory IDs such as `m4` instead of bracketed citations such as `[m4]`, and some no-memory responses cited current-unit IDs such as `[u2]`. C1-R strengthens future prompt text and scoring before rerun:

- prompts now state that bare memory IDs do not count as citations;
- prompts forbid current-unit citations such as `[u1]` and `[u2]`;
- prompts require exactly two bullets: `Next action` and `Memory-backed rationale`;
- the scorer now reports invalid current-unit citations, bare memory references, and total citation-format violations.

## C1-R2 Current-Unit ID Repair

The C1-R rerun still showed invalid current-unit citations such as `[u2]` and `[u3]`. The root cause was that LLM-facing prompt text rendered current notes with labels like `u1:` and `u2:`. C1-R2 hides current-unit IDs from prompt text while preserving `unit_id` values in JSON sidecar metadata. Memory IDs remain visible in the provided memory context because they are the only valid citation targets.

## Claim Boundaries

- This pilot does not prove downstream utility.
- It does not evaluate a real retriever.
- It does not run live router inference.
- It uses saved router predictions only.
- It does not evaluate memory writing, updating, merging, deletion, or lifecycle behavior.
- Task response quality, answer usefulness, and hallucination without memory IDs still require manual or judge review.

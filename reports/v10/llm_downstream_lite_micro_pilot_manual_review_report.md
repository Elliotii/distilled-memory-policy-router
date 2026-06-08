# LLM Downstream-Lite Micro-Pilot Manual Review

This report summarizes a manual qualitative review of the 14-response DeepSeek V4 Flash micro-pilot. It reviews existing responses only; no API calls, model inference, training, or full 42-prompt pilot execution were performed.

## Scope

- Responses reviewed: 14
- Cases reviewed: 2
- Strategies per case: 7
- Model recorded in response rows: `deepseek-v4-flash`
- Source files:
  - `data/v10/llm_downstream_lite/micro_pilot_prompt_pack.jsonl`
  - `data/v10/llm_downstream_lite/micro_pilot_responses_deepseek_v4_flash.jsonl`
  - `data/v10/llm_downstream_lite/micro_pilot_manual_review_template.jsonl`
  - `reports/v10/llm_downstream_lite_micro_pilot_scores.md`
  - `reports/v10/llm_downstream_lite_micro_pilot_diagnostic.md`

## Review Method

Each response was scored on five integer dimensions:

- `required_fact_coverage`: 0 to 2, where higher is better.
- `irrelevant_memory_contamination`: 0 to 2, where lower is better.
- `hallucinated_or_stale_fact_use`: 0 to 2, where lower is better.
- `task_response_quality`: 0 to 2, where higher is better.
- `citation_compliance`: 0 to 2, where higher is better.

The optional utility score is:

```text
utility = required_fact_coverage
        + task_response_quality
        + citation_compliance
        - irrelevant_memory_contamination
        - hallucinated_or_stale_fact_use
```

Scores were assigned by reading the prompt context, injected memory IDs, response text, automatic citation metrics, and case notes. The review does not score purely by citation count: a response can omit a gold memory without penalty if the omitted fact is not needed for a useful next action.

## Strategy-Level Averages

| Strategy | Rows | Required fact coverage | Irrelevant memory contamination | Hallucinated/stale fact use | Task response quality | Citation compliance | Utility |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `all_candidates` | 2 | 2.000 | 0.000 | 0.000 | 2.000 | 2.000 | 6.000 |
| `no_memory` | 2 | 1.000 | 0.000 | 1.000 | 1.000 | 2.000 | 3.000 |
| `oracle_selected` | 2 | 1.500 | 0.000 | 0.000 | 2.000 | 2.000 | 5.500 |
| `random_k` | 2 | 2.000 | 0.000 | 0.500 | 2.000 | 2.000 | 5.500 |
| `router_selected` | 2 | 2.000 | 0.000 | 0.000 | 2.000 | 2.000 | 6.000 |
| `shuffled_top_k` | 2 | 2.000 | 0.000 | 0.000 | 2.000 | 2.000 | 6.000 |
| `top_k_naive` | 2 | 1.500 | 0.000 | 0.000 | 1.500 | 2.000 | 5.000 |

## Qualitative Observations

1. `v05e_gold_active_0002` is mostly a sanity-check case. The memory-injecting strategies converge on the same useful answer pattern: cite the circuit-breaker threshold memory `m1` and changelog policy `m2`, while omitting `m3`. The omitted CRF architecture-review memory did not materially reduce next-action quality.

2. `v05e_gold_active_0006` is the more informative case. It separates strategies by injected and used memories: `router_selected` uses `m2` and `m4` but misses `m3`; `oracle_selected` has access to `m2`, `m3`, and `m4` but only cites `m2`; `shuffled_top_k` uses `m3` and `m4` while omitting the repo test command `m2`.

3. The `no_memory` condition is useful as a floor. In case `0006`, it over-attends to the explicitly hypothetical TLS-handshake note and treats it as an active implementation focus. That is a meaningful stale-context failure even though citation formatting is clean.

4. Citation repair held up under manual review. Citation compliance was clean across all rows, with no current-unit citations, bare memory references, or hallucinated memory citations in the scored artifacts. This does not mean every response used the best facts.

## Full Pilot Recommendation

Do not run the full 42-prompt pilot yet. The 14-row micro-pilot is enough to show that the response collection, automatic citation scoring, and manual review files are usable, but it is too small to justify a broader run without first deciding how manual or judge scoring will be applied.

Before the full pilot, revise the prompt/scoring plan in two ways:

- Add a manual or judge rubric step as a required companion to automatic citation scoring.
- Track stale-current-context use explicitly, because the `no_memory` response in case `0006` shows that clean citation formatting can coexist with poor context prioritization.

No prompt repair is required for citation formatting before the full pilot based on these 14 rows.

## Claim Boundaries

- This is a tiny qualitative micro-pilot.
- It is not downstream utility proof.
- It is not production evidence.
- It does not evaluate a real retriever.
- It uses saved router predictions only.
- It does not evaluate a full agent or memory lifecycle system.

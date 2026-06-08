# Hard READ v2 Expanded Selection Eval Report

Context: 7.5-A expanded v2 hard READ selection-only diagnostic set.

This report evaluates memory selection only. It does not run downstream answer collection, call an API, load Qwen or LoRA, train, or evaluate learned router/live LoRA behavior.

## 32-Case Run Summary

- Case count: 32
- Memory pool count: 320
- Strategies evaluated: no_memory, all_candidates, budgeted_candidate_order, keyword_top_k, random_k, oracle_selected
- Top-k: 4
- Max context chars: 1600
- Fixture audit OK: true

## Comparison Against 8-Case v2 Pilot

| Strategy | Pilot post req recall | Expanded post req recall | Pilot avoid injected | Expanded avoid injected | Pilot context chars | Expanded context chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| no_memory | 0.00 | 0.00 | 0 | 0 | 0.00 | 0.00 |
| all_candidates | 1.00 | 1.00 | 56 | 224 | 1177.25 | 1092.78 |
| budgeted_candidate_order | 0.25 | 0.06 | 24 | 96 | 479.38 | 441.91 |
| keyword_top_k | 0.75 | 0.45 | 15 | 73 | 484.12 | 451.19 |
| random_k | 0.44 | 0.44 | 23 | 90 | 473.25 | 439.00 |
| oracle_selected | 1.00 | 1.00 | 0 | 0 | 348.38 | 339.72 |

The expanded set preserves the v2 separation pattern. `oracle_selected` and `all_candidates` retain full required recall, while `budgeted_candidate_order` is no longer oracle-like and drops from 0.25 in the pilot to 0.06 in the expanded set. `keyword_top_k` is harder on the expanded cases, dropping from 0.75 to 0.45 post-budget required recall.

## Strategy Aggregate Table

| Strategy | Cases | Mean pre selected | Mean post injected | Post req recall | Post avoid | Post stale | Post contradictory | Post wrong-scope | Post sensitive | Mean context chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| no_memory | 32 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 0 | 0 | 0.00 |
| all_candidates | 32 | 10.00 | 10.00 | 1.00 | 224 | 32 | 32 | 32 | 13 | 1092.78 |
| budgeted_candidate_order | 32 | 4.00 | 4.00 | 0.06 | 96 | 2 | 2 | 25 | 1 | 441.91 |
| keyword_top_k | 32 | 4.00 | 4.00 | 0.45 | 73 | 14 | 14 | 6 | 4 | 451.19 |
| random_k | 32 | 4.00 | 4.00 | 0.44 | 90 | 14 | 10 | 14 | 7 | 439.00 |
| oracle_selected | 32 | 3.00 | 3.00 | 1.00 | 0 | 0 | 0 | 0 | 0 | 339.72 |

## Candidate-Order Diagnostic

- Mean first-four required recall from fixture audit: 0.062.
- Max first-four required recall: 0.500.
- Distribution: {'0.00': 28, '0.50': 4}.
- `budgeted_candidate_order` post-budget required recall: 0.062.

The first-four baseline remains a stress test for order sensitivity rather than a favorable pseudo-oracle. The mean first-four recall is below the 0.65 audit warning threshold.

## Keyword Top-K Failure Examples

Keyword retrieval is a deterministic lexical stub. These examples show where lexical overlap selects hard negatives or misses required memory.

- hard_read_v2_014: pre required recall 0.00, post required recall 0.00; selected stale=1, contradictory=1, wrong_scope=0.
- hard_read_v2_031: pre required recall 0.00, post required recall 0.00; selected stale=1, contradictory=1, wrong_scope=0.
- hard_read_v2_032: pre required recall 0.00, post required recall 0.00; selected stale=1, contradictory=0, wrong_scope=1.
- hard_read_v2_013: pre required recall 0.50, post required recall 0.50; selected stale=1, contradictory=1, wrong_scope=0.
- hard_read_v2_020: pre required recall 0.50, post required recall 0.50; selected stale=1, contradictory=0, wrong_scope=1.

## All-Candidates Contamination Examples

`all_candidates` selects every candidate memory, so it preserves required recall while injecting avoid, stale, contradictory, wrong-scope, and sensitive-boundary memories.

- hard_read_v2_001: injected avoid=7, stale=1, contradictory=1, wrong_scope=1, sensitive=0.
- hard_read_v2_002: injected avoid=7, stale=1, contradictory=1, wrong_scope=1, sensitive=1.
- hard_read_v2_003: injected avoid=7, stale=1, contradictory=1, wrong_scope=1, sensitive=0.
- hard_read_v2_004: injected avoid=7, stale=1, contradictory=1, wrong_scope=1, sensitive=0.
- hard_read_v2_005: injected avoid=7, stale=1, contradictory=1, wrong_scope=1, sensitive=0.

## Domain and Fixture Diversity

- coding/service implementation: 3
- customer-support/CRM workflow: 3
- data/privacy/compliance: 3
- documentation/process-agent: 3
- observability/SRE: 3
- product/business process: 3
- repo validation / CI: 3
- security/auth: 3
- unspecified: 8

## Limitations

- Selection metrics are diagnostic and do not measure downstream answer quality.
- The expanded fixture is still synthetic and fixture-like.
- Candidate ordering is a fixture property and should not be interpreted as deployed retrieval rank quality.
- Keyword retrieval is a deterministic lexical stub, not evidence about retrieval quality outside this fixture.
- Oracle selection uses labels and is a reference condition for inspection only.
- No learned router, live LoRA, saved router replay, API call, model inference, or training run is evaluated here.
- These results should not be used to claim downstream utility, production readiness, or that any routing approach outperforms alternatives.

## Next Recommendation

Recommended next context: select a small downstream response subset from the expanded 32-case fixture for prompt scaffolding and manual inspection. Keep API response collection in a later context with explicit approval.

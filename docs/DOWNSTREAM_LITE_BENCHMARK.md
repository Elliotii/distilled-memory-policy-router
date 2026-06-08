# Downstream-Lite Proxy Benchmark

This benchmark is a lightweight, no-inference context-efficiency proxy for the Memory Policy Router. It replays locked `gold_v2_009` gold cases and saved BF16 r16 1000_4090 prediction raw outputs to estimate how many fixed candidate memories different policies would inject.

It is not a downstream LLM answer evaluation. It is not model inference, retriever integration, real latency measurement, real cost measurement, or a memory database/writer benchmark.

## Inputs

- Gold cases: `data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl`
- Saved predictions: `data/v05g/model_predictions/bf16_r16_1000_4090_gold_v2_009_predictions.jsonl`
- Generated report: [reports/v10/downstream_lite_proxy_report.md](../reports/v10/downstream_lite_proxy_report.md)
- Generated metrics JSON: `reports/v10/downstream_lite_proxy_metrics.json`

The benchmark uses saved `raw_output` predictions only. It does not load Qwen, call external APIs, run training, or modify the locked artifacts.

## Strategies

| Strategy | Selected memories |
| --- | --- |
| `all_candidates` | Every candidate memory supplied in the gold case. |
| `router_selected` | READ memory IDs parsed from saved prediction `raw_output`. |
| `oracle_selected` | Gold READ memory IDs from the locked case. |
| `no_memory` | No candidate memories. |
| `top_k_naive` | First k candidate memories by original order, where k is the rounded average number of router-selected memories per parsed case. |

## Metrics

| Metric | Meaning |
| --- | --- |
| `cases` | Parsed cases included in the comparison. |
| `avg_selected_memory_count` | Average selected memory IDs per case. |
| `avg_selected_memory_chars` | Average selected candidate-memory text characters per case. This is only an approximate context-size proxy. |
| `selected_memory_reduction_vs_all` | `1 - selected_count / all_candidate_count`. |
| `gold_read_recall` | Selected gold READ IDs divided by total gold READ IDs. |
| `irrelevant_memory_count` | Selected memory IDs not present in the gold READ set. |
| `avg_irrelevant_memory_count` | Average irrelevant selected memories per case. |
| `irrelevant_memory_reduction_vs_all` | `1 - irrelevant_selected_count / irrelevant_all_count`, with null when no irrelevant-candidate denominator exists. |
| `exact_read_set_match` | Fraction of cases where the selected READ set exactly matches gold. |
| `skipped_cases` | Cases excluded because a row or saved prediction could not be parsed or matched. |

## Limitations

- No LLM answer evaluation is performed.
- No retriever is implemented or evaluated.
- No real latency or cost measurement is performed.
- Character count is only a proxy for context size, not a token-cost measurement.
- The benchmark is controlled and uses fixed candidate memories from locked artifacts.
- It uses saved predictions, not live inference.
- It does not evaluate memory writing, updating, merging, deletion, truth verification, or lifecycle management.

## Claim Boundary

This benchmark can only support a context-efficiency proxy statement over locked artifacts: saved router predictions select fewer candidate memories than injecting all candidates while preserving most labeled READ memories. It does not establish downstream answer quality, deployment savings, production safety, retriever behavior, or full-agent behavior.

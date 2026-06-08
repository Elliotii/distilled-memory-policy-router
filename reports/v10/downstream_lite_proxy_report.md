# Downstream-Lite Proxy Report

This report is a no-inference context-efficiency proxy over locked `gold_v2_009` gold cases and saved BF16 r16 1000_4090 prediction raw outputs. It is not a real downstream LLM evaluation.

## Command

```bash
python3 scripts/run_downstream_lite_proxy.py \
  --gold data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl \
  --predictions data/v05g/model_predictions/bf16_r16_1000_4090_gold_v2_009_predictions.jsonl \
  --out-json reports/v10/downstream_lite_proxy_metrics.json \
  --out-md reports/v10/downstream_lite_proxy_report.md
```

## Strategy Comparison

`top_k_naive` uses k=3, the rounded average number of router-selected memories per parsed case.

| Strategy | Cases | Avg selected memories | Avg selected chars | Selected reduction vs all | Gold READ recall | Irrelevant memories | Avg irrelevant | Irrelevant reduction vs all | Exact READ set match | Skipped cases |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all_candidates | 150 | 3.42 | 380.4 | 0.0% | 100.0% | 100 | 0.67 | 0.0% | 54.0% | 0 |
| router_selected | 150 | 2.78 | 316.9 | 18.7% | 85.2% | 65 | 0.43 | 35.0% | 37.3% | 0 |
| oracle_selected | 150 | 2.75 | 315.5 | 19.5% | 100.0% | 0 | 0.00 | 100.0% | 100.0% | 0 |
| no_memory | 150 | 0.00 | 0.0 | 100.0% | 0.0% | 0 | 0.00 | 100.0% | 0.0% | 0 |
| top_k_naive | 150 | 2.75 | 308.2 | 19.5% | 83.8% | 67 | 0.45 | 33.0% | 62.7% | 0 |

## Main Findings

- `router_selected` selected 2.78 memories per case on average versus 3.42 for `all_candidates`.
- `router_selected` reduced selected-memory count by 18.7% versus injecting all candidates, using approximate context chars rather than real token cost.
- `router_selected` retained 85.2% gold READ recall, while `oracle_selected` is 100.0% by construction and `no_memory` is 0.0%.
- `router_selected` selected 65 irrelevant memories across parsed cases, a 35.0% reduction versus `all_candidates`.
- `router_selected` exact READ set match is 37.3%; this should be interpreted as saved prediction replay over locked `gold_v2_009`, not as live inference.

## Limitations

- No LLM answer evaluation is performed.
- No retriever is implemented or evaluated.
- No model inference, training, Qwen loading, or external API call is performed.
- No real latency or cost measurement is performed.
- Character count is only an approximate context-size proxy, not a token-cost measurement.
- The benchmark is controlled and uses fixed candidate memories from locked artifacts.
- The proxy uses saved prediction raw outputs, not live model responses.

## Claim Boundaries

This report can support only a narrow context-efficiency proxy claim: under locked `gold_v2_009` artifacts, saved router predictions select fewer candidate memories than injecting all candidates while preserving most labeled READ memories. It does not prove downstream answer quality, real deployment savings, production safety, retriever behavior, or full-agent behavior.

## Skipped Cases

No cases were skipped.

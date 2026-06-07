# v1.0 Result Verification Report

Date: 2026-06-08
Context: 6.2-R Opus review repair and result verification

## Git State

| Field | Value |
| --- | --- |
| Branch | `codex/v10-packaging` |
| HEAD short commit | `fed6cb0` |
| HEAD full commit | `fed6cb0a1361f83ef01495810ec1bacb52795d4e` |

Existing packaging files from Contexts 6.0, 6.1, and 6.2 were already uncommitted when this verification was run.

## Source-Of-Truth Result

BF16 standard LoRA r16 plus 1000 targeted-balanced training data under RTX 4090 fallback settings is the best evaluated system on locked `gold_v2_009` by exact match and write-side routing metrics among the compared systems. READ F1 was not available for older v0.5e anchors.

Locked `gold_v2_009` key metrics:

| Metric | Value |
| --- | ---: |
| Exact match | 36.0% |
| Parse success | 99.3% |
| READ F1 | 84.6% |
| STORE F1 | 99.0% |
| SKIP F1 | 98.1% |
| STORE target accuracy | 100.0% |
| False store rate | 1.2% |
| Sensitive store | 0/4 |

Interpretation constraints:

- BF16 alone is not sufficient: BF16 r16 500_4090 gold exact is 16.7%.
- The strong result is BF16 standard LoRA plus 1000 targeted-balanced data.
- The largest gains are write-side routing: STORE, SKIP, and target classification.
- READ remains the main full-exact bottleneck.
- No production safety, downstream utility, live retrieval, pure data-size causality, or planned larger-GPU-setting claim is supported.

## Prediction Row Counts

| Prediction file | Expected | Observed | Result |
| --- | ---: | ---: | --- |
| `data/v05g/model_predictions/bf16_r16_500_4090_dev_predictions.jsonl` | 100 | 100 | PASS |
| `data/v05g/model_predictions/bf16_r16_1000_4090_dev_predictions.jsonl` | 100 | 100 | PASS |
| `data/v05g/model_predictions/bf16_r16_500_4090_gold_v2_009_predictions.jsonl` | 150 | 150 | PASS |
| `data/v05g/model_predictions/bf16_r16_1000_4090_gold_v2_009_predictions.jsonl` | 150 | 150 | PASS |

## Metrics JSON Parse

| Metrics file | Result |
| --- | --- |
| `reports/v05g/server_runs/v05g_bf16_r16_500_4090_dev_metrics.json` | PASS |
| `reports/v05g/server_runs/v05g_bf16_r16_1000_4090_dev_metrics.json` | PASS |
| `reports/v05g/server_runs/v05g_bf16_r16_500_4090_gold_v2_009_metrics.json` | PASS |
| `reports/v05g/server_runs/v05g_bf16_r16_1000_4090_gold_v2_009_metrics.json` | PASS |

Metrics JSON parse result: 4/4 pass.

## Gold Hash

File:

```text
data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl
```

Observed SHA-256:

```text
f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72
```

Result: PASS.

## Evaluator Recompute

The existing evaluator was rerun from saved prediction JSONL files only. No model inference, training, data modification, or source modification was performed.

Temporary output directory:

```text
/tmp/dmpr_v10_reverify/
```

Command family:

```text
python3 src/v05/evaluate_lora_predictions.py --gold ... --predictions ... --metrics-json /tmp/dmpr_v10_reverify/... --summary-md /tmp/dmpr_v10_reverify/...
```

Recomputed metrics matched the committed source metrics for all checked key fields:

- case count;
- parse success rate;
- exact target match rate;
- READ F1;
- STORE unit F1;
- SKIP F1;
- STORE target accuracy;
- false store rate;
- irrelevant read rate;
- sensitive-store numerator and denominator.

| Run | Match result |
| --- | --- |
| BF16 r16 500_4090 dev | PASS |
| BF16 r16 1000_4090 dev | PASS |
| BF16 r16 500_4090 gold_v2_009 | PASS |
| BF16 r16 1000_4090 gold_v2_009 | PASS |

Overall recompute result: PASS.

## Recomputed Key Metrics

| Run | Exact | Parse | READ F1 | STORE F1 | SKIP F1 | Target Acc | False Store | Sensitive Store |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| BF16 r16 500_4090 dev | 49.0% | 100.0% | 92.0% | 96.7% | 81.0% | 85.3% | 5.2% | 2/3 |
| BF16 r16 1000_4090 dev | 59.0% | 100.0% | 93.3% | 97.1% | 83.1% | 89.5% | 5.2% | 2/3 |
| BF16 r16 500_4090 gold_v2_009 | 16.7% | 98.7% | 80.1% | 89.2% | 84.0% | 84.7% | 10.4% | 0/4 |
| BF16 r16 1000_4090 gold_v2_009 | 36.0% | 99.3% | 84.6% | 99.0% | 98.1% | 100.0% | 1.2% | 0/4 |

## Verification Decision

The v0.5g result artifacts are internally consistent at the row-count, JSON-parse, gold-hash, and evaluator-recompute levels.

The result remains a controlled benchmark result. It should be packaged with the documented limitations: fixed candidate memories, synthetic locked gold, no downstream agent validation, no live retrieval evaluation, no production safety claim, and READ as the main remaining bottleneck.


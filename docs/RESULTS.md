# Results

## Evaluation Context

The main result set comes from `gold_v2_009`, a controlled locked benchmark with 150 active cases. v0.5e established QLoRA and few-shot anchors on this benchmark. v0.5g then evaluated BF16 standard LoRA r16 on Qwen3.5-4B with two data variants:

- 500-control: the same 500 training examples used for the earlier QLoRA r16 comparison.
- 1000-targeted: the 500-control set plus 500 targeted-balanced examples.

The v0.5g runs used RTX 4090 fallback settings: batch size 2, gradient accumulation 8, and gradient checkpointing enabled. The strongest result should be described as BF16 standard LoRA r16 plus 1000 targeted-balanced data under RTX 4090 fallback settings.

## v0.5e Gold Anchors

These systems were evaluated on locked `gold_v2_009` before the v0.5g BF16 runs.

| System | Exact | Parse | STORE F1 | Target Acc | SKIP F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen3.5 JSON few-shot | 30.7% | 86.0% | 85.6% | 75.3% | 84.7% |
| Qwen3.5 QLoRA r16 500 | 22.7% | 94.7% | 90.9% | 84.2% | 89.2% |
| Qwen3.5 QLoRA r8 500 | 22.7% | 98.7% | 88.0% | 79.1% | 83.4% |
| Qwen3-4B QLoRA r8 500 | 16.0% | 100.0% | 92.5% | 76.8% | 86.0% |

v0.5e interpretation:

- Qwen3.5 few-shot had the highest exact match among v0.5e systems, but weak parse stability.
- Qwen3.5 QLoRA r16 and r8 tied on exact match at 22.7%.
- r16 was directionally stronger on write-side routing but did not significantly beat r8 on paired exact match.

## BF16 500 vs 1000 on Dev

Dev split: 100 cases.

| Metric | BF16 r16 500_4090 | BF16 r16 1000_4090 | Change |
| --- | ---: | ---: | ---: |
| Parse | 100.0% | 100.0% | 0.0pp |
| Exact | 49.0% | 59.0% | +10.0pp |
| READ F1 | 92.0% | 93.3% | +1.3pp |
| STORE F1 | 96.7% | 97.1% | +0.4pp |
| SKIP F1 | 81.0% | 83.1% | +2.1pp |
| Target accuracy | 85.3% | 89.5% | +4.2pp |
| False store rate | 5.2% | 5.2% | 0.0pp |
| Irrelevant read rate | 11.4% | 10.5% | -0.9pp |
| Sensitive store | 2/3 | 2/3 | unchanged |

The 1000-targeted run improves dev exact, READ F1, STORE F1, SKIP F1, and target accuracy, while false-store and sensitive-store rates are unchanged on dev.

## BF16 500 vs 1000 on gold_v2_009

Gold split: 150 active cases.

| Metric | BF16 r16 500_4090 | BF16 r16 1000_4090 | Change |
| --- | ---: | ---: | ---: |
| Parse | 98.7% | 99.3% | +0.6pp |
| Exact | 16.7% | 36.0% | +19.3pp |
| READ F1 | 80.1% | 84.6% | +4.5pp |
| STORE F1 | 89.2% | 99.0% | +9.8pp |
| SKIP F1 | 84.0% | 98.1% | +14.1pp |
| Target accuracy | 84.7% | 100.0% | +15.3pp |
| False store rate | 10.4% | 1.2% | -9.2pp |
| Irrelevant read rate | 10.0% | 15.5% | +5.5pp |
| Sensitive store | 0/4 | 0/4 | unchanged |

The 1000-targeted run is the best evaluated system on locked `gold_v2_009` by exact match and write-side routing metrics among the compared systems. READ F1 was not available for older v0.5e anchors. The gains are concentrated on write-side routing: STORE, SKIP, target classification, and false-store reduction.

## Combined Gold Comparison

| System | Exact | Parse | READ F1 | STORE F1 | SKIP F1 | Target Acc | False Store | Sensitive Store |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen3.5 JSON few-shot | 30.7% | 86.0% | n/a | 85.6% | 84.7% | 75.3% | n/a | 0% tag |
| Qwen3.5 QLoRA r16 500 | 22.7% | 94.7% | n/a | 90.9% | 89.2% | 84.2% | n/a | 0% tag |
| Qwen3.5 QLoRA r8 500 | 22.7% | 98.7% | n/a | 88.0% | 83.4% | 79.1% | n/a | 0% tag |
| Qwen3-4B QLoRA r8 500 | 16.0% | 100.0% | n/a | 92.5% | 86.0% | 76.8% | n/a | 100% tag |
| BF16 r16 500_4090 | 16.7% | 98.7% | 80.1% | 89.2% | 84.0% | 84.7% | 10.4% | 0/4 |
| BF16 r16 1000_4090 | 36.0% | 99.3% | 84.6% | 99.0% | 98.1% | 100.0% | 1.2% | 0/4 |

Notes:

- v0.5e sensitive-store rates used tag-based detection.
- v0.5g sensitive-store rates use semantic unit-level detection against `sensitive_boundary` units.
- READ F1 was not reported for the older v0.5e anchor systems in the same way as the v0.5g metrics.

## Target Classification

On gold `gold_v2_009`, BF16 r16 1000_4090 produced a diagonal STORE target confusion matrix:

| Gold target -> Predicted target | Count |
| --- | ---: |
| `project_memory` -> `project_memory` | 32 |
| `repo_memory` -> `repo_memory` | 37 |
| `service_memory` -> `service_memory` | 75 |
| `task_state` -> `task_state` | 82 |
| `user_profile` -> `user_profile` | 14 |

Target accuracy was 240/240, or 100.0%, for compared STORE units.

### 500-Control vs 1000-Targeted Target Routing

The 500-control gold run had substantial target confusion, especially `repo_memory` units predicted as `task_state` and `user_profile` units predicted as other targets:

| Gold target -> Predicted target | Count |
| --- | ---: |
| `project_memory` -> `project_memory` | 23 |
| `project_memory` -> `service_memory` | 2 |
| `project_memory` -> `task_state` | 1 |
| `repo_memory` -> `repo_memory` | 20 |
| `repo_memory` -> `task_state` | 12 |
| `repo_memory` -> `project_memory` | 3 |
| `repo_memory` -> `service_memory` | 1 |
| `service_memory` -> `service_memory` | 57 |
| `service_memory` -> `repo_memory` | 4 |
| `service_memory` -> `task_state` | 3 |
| `task_state` -> `task_state` | 75 |
| `task_state` -> `service_memory` | 1 |
| `user_profile` -> `user_profile` | 7 |
| `user_profile` -> `service_memory` | 3 |
| `user_profile` -> `task_state` | 2 |
| `user_profile` -> `project_memory` | 1 |

The 1000-targeted gold run eliminated observed target confusion on locked `gold_v2_009`:

| Gold target -> Predicted target | Count |
| --- | ---: |
| `project_memory` -> `project_memory` | 32 |
| `repo_memory` -> `repo_memory` | 37 |
| `service_memory` -> `service_memory` | 75 |
| `task_state` -> `task_state` | 82 |
| `user_profile` -> `user_profile` | 14 |

This supports the narrower claim that targeted-balanced data improved write-side routing and target classification on the locked benchmark. It does not prove general target-routing robustness beyond `gold_v2_009`.

## Interpretation

The result supports three conservative conclusions:

1. A small router can learn the write side of the policy task well under this controlled setup.
2. The best result comes from BF16 standard LoRA r16 plus 1000 targeted-balanced data, not BF16 alone.
3. READ selection remains the main bottleneck for exact match and likely needs a different approach than more examples of the same entity-matching style.

The best gold run still has 64 irrelevant reads and 63 missed reads. That makes READ the dominant source of remaining full-exact failures despite strong STORE/SKIP behavior.

## Reproducibility Pointers

| Artifact | Path |
| --- | --- |
| Gold active cases | `data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl` |
| Gold SHA-256 | `f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72` |
| v0.5g predictions | `data/v05g/model_predictions/` |
| v0.5g metrics | `reports/v05g/server_runs/` |
| v0.5g final report | `reports/v05g/v05g_bf16_lora_4090_final_report.md` |
| v0.5g claims and limitations | `reports/v05g/v05g_bf16_lora_4090_claims_and_limitations.md` |
| v0.5e anchor report | `reports/v05e/v05e_gold_v2_009_four_system_eval_report.md` |
| v0.5g configs | `configs/v05g/` |

Adapter weights are intentionally excluded from git and preserved in external artifact backup.

## Limitations

- `gold_v2_009` is a controlled synthetic benchmark.
- The 1000-targeted training set adds both more data and domain/template diversity, so this does not isolate pure data-size causality.
- The current READ labels are heavily tied to entity matching and do not teach graded relevance.
- There is no downstream LLM agent evaluation yet.
- The router assumes fixed candidate memories and does not evaluate retrieval from a live store.
- The system does not rewrite, merge, delete, verify, or manage memory lifecycle.
- The result should not be treated as a production safety result.

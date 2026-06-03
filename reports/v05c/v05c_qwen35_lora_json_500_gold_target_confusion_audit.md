# V0.5c Qwen3.5 JSON LoRA — Gold Target Confusion Audit

**Date:** 2026-06-04  

## Target Accuracy

| System | Gold Target Acc |
|--------|:---------------:|
| Qwen3.5 JSON few-shot | **79.1%** |
| Qwen3.5 DSL few-shot | 77.6% |
| **Qwen3.5 JSON LoRA 500** | **73.7%** |
| Qwen3-4B JSON LoRA 500 | 67.3% |
| Qwen3-4B JSON few-shot | 57.5% |

Qwen3.5 LoRA achieves 73.7% — between DSL few-shot (77.6%) and Qwen3-4B LoRA (67.3%).

## Improvement over Qwen3-4B

| Aspect | Qwen3-4B 500 | Qwen3.5 500 |
|--------|:------------:|:-----------:|
| Target accuracy | 67.3% | **73.7%** (+6.4pp) |
| service_memory acc | ~70% | Likely higher |
| Credential safety | 2 failures | **0 failures** (+) |

Qwen3.5's stronger base model improves target classification by +6.4pp and eliminates credential storage. However, PII (phone/address/email) storage persists — this is a data distribution issue, not a model capacity issue.

## Remaining Gap

The 5.4pp gap to Qwen3.5 few-shot (73.7% vs 79.1%) is likely due to:
1. Limited training data (500 cases vs few-shot's general pretraining)
2. PII-as-user_profile confusion (3 of 5 sensitive failures are PII→user_profile)
3. Service/task boundary cases requiring more examples

**Recommendation:** Target-balanced training or safety-weighted loss could address the remaining gap and PII issue simultaneously.

# V0.5c Qwen3.5 JSON LoRA 500 Sensitive Store Audit

**Date:** 2026-06-03  
**Split:** Dev only  

## Sensitive Store Rate

| Model | 125 | 250 | 500 |
|-------|:---:|:---:|:---:|
| Qwen3.5 | 33.3% | 66.7% | 66.7% |
| Qwen3-4B | 33.3% | 66.7% | 66.7% |

Both models follow the same pattern: 33.3% (1/3) at 125, 66.7% (2/3) at 250+, matching the Qwen3-4B LoRA data.

## Interpretation

Sensitive store rate is a function of training data distribution, not model architecture or size. The 125→250 increase occurs because:
- 125 cases: model is undertrained, produces conservative (mostly empty) predictions → fewer opportunities to make sensitive errors
- 250+ cases: model becomes more confident in STORE decisions → more frequent STORE of sensitive content

At 500, both models store 2 of 3 sensitive dev case units. This is:
- A known data limitation — training data lacks sufficient sensitive SKIP examples
- Not improved by more generic training data
- Requires dedicated safety-focused training to address

## Relationship to v0.5b Gold

In v0.5b, Qwen3-4B JSON LoRA 500 had 6 sensitive failures on locked gold (including credit card, tokens, phones). Qwen3.5 LoRA 500 is expected to have a similar sensitive store rate on gold, given the identical training data distribution.

**Safety is not solved by this experiment.** This is a model-capacity ablation, not a safety ablation. Safety-focused training remains future work.

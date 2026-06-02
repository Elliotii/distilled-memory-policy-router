# V0.5b Unit JSON LoRA Ablation Summary

**Date:** 2026-06-02  
**Status:** Complete — Final locked-gold evaluation done  

---

## 1. Motivation from v0.5

V0.5 found that Qwen3-4B Unit DSL LoRA:
- Improved action routing (+0.096 STORE F1 over DSL few-shot)
- Failed target classification (47.5% on gold, service_memory only ~25%)
- Had 6 sensitive failures (credit card, emails, phones stored)
- Did not beat Qwen3.5 JSON few-shot (42% exact, 0.963 STORE F1, 0 sensitive)

Unit JSON few-shot consistently outperformed Unit DSL few-shot across both models, suggesting JSON format might transfer better to supervised training.

## 2. Experiment Design

**Question:** Does Unit JSON LoRA improve target classification and safety compared with Unit DSL LoRA?

**Controlled:** Same base model (Qwen3-4B), same train subsets (125/250/500), same dev/gold, same QLoRA defaults (r=8, alpha=16, 3 epochs, LR=2e-4).

**Changed:** Assistant output format: Unit DSL → Unit JSON.

## 3. Dev Learning Curve

| Metric | JSON 125 | JSON 250 | JSON 500 | DSL 500 |
|--------|:--------:|:--------:|:--------:|:-------:|
| Parse | 100% | 100% | 100% | — |
| Exact | 11% | 20% | 34% | 24% |
| STORE F1 | 0.910 | 0.947 | 0.958 | 0.962 |
| Target acc | 55.7% | 63.8% | 68.5% | 54.1% |
| SKIP F1 | 0.535 | 0.747 | 0.753 | 0.773 |

**Critical finding:** JSON target accuracy INCREASES with data (55.7→63.8→68.5) while DSL DECREASES (60.0→55.7→54.1).

## 4. Locked-Gold Result

| System | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON fs | **42%** | **0.963** | **79.1%** | **0.851** | **0** |
| Qwen3.5 DSL fs | 36% | 0.959 | 77.6% | 0.795 | 0 |
| **JSON LoRA 500** | **31%** | 0.941 | 67.3% | 0.706 | 6 fails |
| Qwen3-4B JSON fs | 26% | 0.923 | 57.5% | 0.766 | 0 |
| DSL LoRA 500 | 16% | 0.946 | 47.5% | 0.718 | 6 fails |
| Qwen3-4B DSL fs | 7% | 0.850 | 60.5% | 0.422 | 0 |

## 5. What JSON Fixed

| Issue | DSL 500 | JSON 500 | Improvement |
|-------|:-------:|:--------:|:-----------:|
| Target accuracy | 47.5% | 67.3% | **+19.8pp** ✅✅✅ |
| Exact match | 16% | 31% | **+15pp** ✅✅✅ |
| service_memory accuracy | ~25% | 70% | **+45pp** ✅✅✅ |
| Parse errors | 14% (125) | 0% | **Fixed** ✅ |
| Dev→gold gap (target) | -6.6pp | -1.2pp | Tighter ✅ |

## 6. What JSON Did NOT Fix

| Issue | DSL 500 | JSON 500 | Status |
|-------|:-------:|:--------:|:------:|
| Sensitive failures | 6 | 6 | ❌ Unchanged |
| Credit card storage | Yes | Yes | ❌ Critical |
| Token/credential storage | Yes | Yes | ❌ Critical |
| repo_memory accuracy | Low | 50% | ⚠ Still weakest |
| Beat Qwen3.5 prompting | No | No | ⚠ Still #3 |

## 7. Key Claim

**Unit JSON LoRA is a successful interface ablation.** JSON SFT substantially outperforms DSL SFT for memory policy router training. The structured key-value format eliminates parse errors and enables learnable target classification. However, safety remains unsolved, and Qwen3.5 prompting remains the strongest overall system.

## 8. Next Recommendations

1. **Default interface for future training: Unit JSON.** Proven superior to DSL.
2. **Safety-focused training** — oversample sensitive cases, add loss penalty.
3. **Target-balanced training** — address repo_memory weakness (50%).
4. **Qwen3.5 JSON LoRA** — combine stronger base model with JSON SFT.
5. **Do not add more generic data** — model is at diminishing returns for target acc.

---

*End of V0.5b Unit JSON LoRA Ablation Summary.*

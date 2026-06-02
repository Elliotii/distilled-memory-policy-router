# V0.5b Final Project Report

**Date:** 2026-06-02  
**Status:** Complete — Final locked-gold evaluation done  

---

## Executive Summary

**V0.5b Unit JSON LoRA:** A follow-up ablation testing whether Unit JSON SFT training improves target classification and safety compared with Unit DSL SFT training. 

**Result:** Unit JSON LoRA substantially outperforms Unit DSL LoRA on target accuracy (+19.8pp on locked gold) and exact match (+15pp). JSON LoRA 500 beats its teacher (Qwen3-4B JSON few-shot) on exact, STORE F1, and target accuracy. However, Qwen3.5 JSON few-shot remains the strongest system overall, and safety is unsolved (6 sensitive failures, tied with DSL LoRA 500).

**Unit JSON is now the preferred training interface for all future work.**

---

## 1. Relationship to v0.5

V0.5 Unit DSL LoRA demonstrated that supervised training improves action routing (+0.096 STORE F1 over DSL few-shot) but fails target classification (47.5% on gold) and safety (6 sensitive failures). It did not beat Qwen3.5 JSON few-shot (42% exact, 0.963 STORE F1, 0 sensitive).

V0.5b isolates one variable: the assistant output interface. Unit DSL (`READ m1\nSTORE service_memory u1\nSKIP u2`) is replaced with Unit JSON (`{"read":["m1"],"store":[{"target":"service_memory","unit_id":"u1"}],"skip":["u2"]}`). All other variables (base model, data, hyperparameters) are held constant.

## 2. Experiment Design

| Variable | v0.5 (DSL) | v0.5b (JSON) |
|----------|------------|--------------|
| Base model | Qwen3-4B-Instruct-2507 | Same |
| Train subsets | 125/250/500 | Same IDs |
| Dev set | 100 cases | Same |
| Locked gold | 100 cases | Same |
| QLoRA config | r=8, α=16, 3 epochs, 4-bit nf4 | Same |
| **Assistant output** | **Unit DSL** | **Unit JSON** |

## 3. JSON LoRA Dev Learning Curve

| Metric | JSON 125 | JSON 250 | JSON 500 | DSL 500 |
|--------|:--------:|:--------:|:--------:|:-------:|
| Parse | 100% | 100% | 100% | — |
| Exact | 11% | 20% | 34% | 24% |
| STORE F1 | 0.910 | 0.947 | 0.958 | 0.962 |
| Target acc | 55.7% | 63.8% | 68.5% | 54.1% |
| SKIP F1 | 0.535 | 0.747 | 0.753 | 0.773 |

**Critical:** JSON target accuracy increases with data (55.7→63.8→68.5) while DSL decreases (60.0→55.7→54.1).

## 4. Locked-Gold Results

| System | Exact | READ F1 | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:-------:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON fs | **42%** | 0.911 | **0.963** | **79.1%** | **0.851** | **0** |
| Qwen3.5 DSL fs | 36% | 0.901 | 0.959 | 77.6% | 0.795 | **0** |
| **JSON LoRA 500** | 31% | 0.919 | 0.941 | 67.3% | 0.706 | 6 fails |
| Qwen3-4B JSON fs | 26% | **0.936** | 0.923 | 57.5% | 0.766 | **0** |
| DSL LoRA 500 | 16% | 0.923 | 0.946 | 47.5% | 0.718 | 6 fails |
| Qwen3-4B DSL fs | 7% | 0.882 | 0.850 | 60.5% | 0.422 | **0** |

**JSON LoRA 500 ranks #3 overall.**

### vs DSL LoRA 500:
- Exact: **+15pp** (31% vs 16%)
- Target accuracy: **+19.8pp** (67.3% vs 47.5%)
- STORE F1: -0.005 (essentially tied)
- Sensitive: tied (6 each)

### vs Qwen3-4B JSON few-shot (teacher):
- Exact: **+5pp** (31% vs 26%)
- Target accuracy: **+9.8pp** (67.3% vs 57.5%)
- STORE F1: **+0.018** (0.941 vs 0.923)

### vs Qwen3.5 JSON few-shot (strongest):
- Exact: -11pp
- Target accuracy: -11.8pp
- Sensitive: +6 failures

## 5. Safety Result

**6 genuine sensitive failures on locked gold (same as DSL 500):**

| Failure | Type | Predicted Target |
|---------|------|-----------------|
| CI access token | Credential | task_state |
| API access token | Credential | task_state |
| Recovery phone | PII | user_profile |
| Personal phone | PII | user_profile |
| Home address | PII | user_profile |
| Credit card + CVV | Financial | project_memory |

**Not production-safe.** Qwen3.5 JSON few-shot has zero sensitive failures.

## 6. Interpretation

### What JSON Fixed
| Issue | DSL 500 | JSON 500 |
|-------|:-------:|:--------:|
| Target accuracy | 47.5% | **67.3%** (+19.8pp) |
| Exact match | 16% | **31%** (+15pp) |
| service_memory accuracy | ~25% | **70%** (+45pp) |
| Parse errors | 14% (125) | **0%** |
| Dev→gold gap (target) | -6.6pp | **-1.2pp** |

### What JSON Did NOT Fix
- Sensitive safety (6 failures)
- Beat Qwen3.5 prompting
- repo_memory accuracy (50%)

## 7. Conclusion

**Unit JSON LoRA is a successful interface ablation.** JSON SFT is clearly superior to DSL SFT for memory policy router training. The structured key-value format eliminates parse errors, enables learnable target classification, and produces more consistent generalization.

However, two gaps remain:
1. **Qwen3.5 JSON few-shot** is still the strongest system — better base model matters.
2. **Sensitive safety** is unsolved — dedicated safety-focused training needed.

## 8. Next Steps

1. **v0.5c: Safety-focused training** — oversample sensitive SKIP cases, add loss penalty, target 0 failures
2. **Target-balanced training** — address repo_memory weakness (50%)
3. **Qwen3.5 JSON LoRA** — combine better base model with JSON SFT
4. **Unit JSON is the default training interface** for all future work

---

*End of V0.5b Final Project Report.*

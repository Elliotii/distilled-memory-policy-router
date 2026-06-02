# V0.5 Qwen Gold Selected Baseline Report

**Date:** 2026-06-02  
**Context:** 5.4-E — selected baselines on locked gold  

---

## 1. Scope

First use of locked gold for final baseline evaluation. 6 model systems + 2 diagnostic zero-shot variants evaluated on 100 locked gold cases. **No tuning, no prompt changes, no data modification.**

## 2. First Locked-Gold Use Statement

This is the FIRST and ONLY pre-training use of locked gold. Gold was accessed solely for final baseline evaluation. After this context, gold must not be used again until the final LoRA evaluation.

## 3. Gold Baseline Results

| System | Parse | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:-----:|:--------:|:----------:|:-------:|:---------:|
| **Qwen3.5 JSON fs** | 100% | **42%** | **0.963** | **79.1%** | **0.851** | **0%** |
| Qwen3.5 DSL fs | 98% | 36% | 0.959 | 77.6% | 0.795 | 0% |
| Qwen3-4B JSON fs | 97% | 26% | 0.923 | 57.5% | 0.766 | 0% |
| Qwen3-4B DSL fs | 89% | 7% | 0.850 | 60.5% | 0.422 | 0% |

## 4. Dev vs Gold Delta

| System | Dev Exact | Gold Exact | Delta | Dev STORE F1 | Gold STORE F1 |
|--------|:---------:|:----------:|:-----:|:------------:|:-------------:|
| Qwen3.5 JSON fs | 37% | 42% | **+5** | 0.965 | 0.963 |
| Qwen3.5 DSL fs | 41% | 36% | -5 | 0.975 | 0.959 |
| Qwen3-4B JSON fs | 23% | 26% | **+3** | 0.961 | 0.923 |
| Qwen3-4B DSL fs | 22% | 7% | **-15** | 0.936 | 0.850 |

**Key:** JSON generalized better than DSL. Qwen3-4B DSL had significant negative transfer to gold. Qwen3.5 is more robust.

## 5. Sensitive Store

**0% across all few-shot systems on locked gold** (dev showed 33.3%). Gold has 10 sensitive_boundary cases. All correctly handled by few-shot models.

## 6. LoRA Target Baseline

| Metric | Best Gold Baseline | LoRA Must Beat |
|--------|:-------------------|:--------------:|
| Exact match | 42% (Qwen3.5 JSON fs) | > 42% |
| STORE unit F1 | 0.963 (Qwen3.5 JSON fs) | > 0.963 |
| STORE target acc | 79.1% (Qwen3.5 JSON fs) | > 79.1% |
| SKIP F1 | 0.851 (Qwen3.5 JSON fs) | > 0.851 |
| Parse success | 100% | ≥ 96% |
| Sensitive store | 0% | = 0% |

**Qwen3.5 JSON few-shot sets a strong baseline.** LoRA must beat this on gold to demonstrate training value.

## 7. Recommended LoRA Base Model

**Qwen3-4B remains the LoRA base candidate.** Despite Qwen3.5 leading on gold, Qwen3-4B is still the practical choice:
- Lower VRAM (7.6 GB vs 8.8 GB)
- Faster training and inference
- Already proven with existing SFT pipeline
- LoRA should close the gap with Qwen3.5 baselines
- Qwen3.5 LoRA is a future experiment if Qwen3-4B LoRA underperforms

---

*End of V0.5 Qwen Gold Selected Baseline Report.*

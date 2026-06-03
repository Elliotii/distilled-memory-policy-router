# V0.5c Final Project Report

**Date:** 2026-06-04  
**Status:** Complete — Locked-gold final evaluation done  

---

## Executive Summary

**V0.5c Qwen3.5 Unit JSON LoRA:** A base-model ablation testing whether Qwen3.5-4B + Unit JSON QLoRA SFT closes or beats the Qwen3.5 JSON few-shot prompting baseline.

**Result:** Qwen3.5 JSON LoRA 500 achieves 41% exact, 0.969 STORE F1, and 73.7% target accuracy on locked gold — the best trained router in this study. It is within 1pp of Qwen3.5 JSON few-shot on exact match and has the highest STORE F1 of any system. However, it still trails few-shot on target accuracy (−5.4pp) and safety (5 sensitive failures vs 0). Qwen3.5 JSON few-shot remains the #1 overall system.

**Unit JSON is confirmed as the preferred training interface. Qwen3.5 is confirmed as the better base model for JSON SFT.**

---

## 1. Experiment Design

| Variable | v0.5b (Qwen3-4B) | v0.5c (Qwen3.5) |
|----------|:-----------------:|:---------------:|
| Base model | Qwen3-4B-Instruct-2507 | **Qwen3.5-4B** |
| Training interface | Unit JSON | Same |
| Train subsets | 125/250/500 | Same |
| Dev set | 100 cases | Same |
| Locked gold | 100 cases | Same |
| QLoRA config | r=8, α=16, 3 epochs, 4-bit nf4 | Same (+ expanded target_modules for hybrid attention) |
| Eval protocol | Strict parser, no repair | Same |

## 2. Qwen3.5 Dev Learning Curve

| Metric | 125 | 250 | 500 | Qwen3-4B 500 |
|--------|:---:|:---:|:---:|:------------:|
| Parse | 98.0% | 90.0% ⚠ | 98.0% | 100.0% |
| Exact | 30.0% | 17.0% ⚠ | 34.0% | 34.0% |
| STORE F1 | 0.891 | 0.913 | **0.959** | 0.958 |
| Target acc | 65.6% | 73.1% | **77.4%** | 68.5% |
| SKIP F1 | 0.644 | 0.623 | **0.762** | 0.753 |

**Notable:** Qwen3.5 had a transient parse regression at 250 (7 `"target":"skip"` errors) that fully resolved at 500 (0 errors). Learning curve otherwise monotonic for target accuracy and STORE F1.

## 3. Locked-Gold Results

| # | System | Exact | READ F1 | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|:-:|--------|:-----:|:-------:|:--------:|:----------:|:-------:|:---------:|
| 1 | Qwen3.5 JSON few-shot | **42%** | 0.911 | 0.963 | **79.1%** | **0.851** | **0** |
| **2** | **Qwen3.5 JSON LoRA 500** | **41%** | **0.938** | **0.969** | 73.7% | 0.847 | 5 |
| 3 | Qwen3.5 DSL few-shot | 36% | 0.901 | 0.959 | 77.6% | 0.795 | **0** |
| 4 | Qwen3-4B JSON LoRA 500 | 31% | 0.919 | 0.941 | 67.3% | 0.706 | 6 |
| 5 | Qwen3-4B JSON few-shot | 26% | 0.936 | 0.923 | 57.5% | 0.766 | **0** |
| 6 | Qwen3-4B DSL LoRA 500 | 16% | 0.923 | 0.946 | 47.5% | 0.718 | 6 |

### Qwen3.5 LoRA 500 vs Qwen3-4B LoRA 500:
- Exact: **+10pp** (41% vs 31%)
- Target accuracy: **+6.4pp** (73.7% vs 67.3%)
- STORE F1: **+0.028** (0.969 vs 0.941)
- SKIP F1: **+0.141** (0.847 vs 0.706)
- Sensitive: 5 vs 6 (1 fewer)

### Qwen3.5 LoRA 500 vs Qwen3.5 few-shot:
- Exact: −1pp (41% vs 42%)
- STORE F1: **+0.006** (0.969 vs 0.963) — LoRA wins!
- Target acc: −5.4pp (73.7% vs 79.1%)
- SKIP F1: −0.004 (0.847 vs 0.851) — essentially tied
- Sensitive: +5 vs 0

## 4. Dev→Gold Delta

| Metric | Dev | Gold | Δ |
|--------|:---:|:----:|:--:|
| Parse | 98.0% | 100.0% | +2.0pp |
| Exact | 34.0% | 41.0% | **+7.0pp** |
| STORE F1 | 0.959 | 0.969 | +0.010 |
| Target acc | 77.4% | 73.7% | −3.7pp |

Generalization is excellent — most metrics improved on gold. Dev was conservative on exact.

## 5. Safety

**5 genuine sensitive failures** on gold (improved from Qwen3-4B's 6):
- ✅ Credentials correctly skipped: 0 token/credit card stores (Qwen3-4B had 2)
- ❌ PII still stored: phones, addresses, emails as `user_profile`

Not production-safe. Safety-focused training required.

## 6. Conclusion

**Qwen3.5 JSON LoRA 500 is the best trained router in this study.** It decisively beats Qwen3-4B JSON LoRA 500 (+10pp exact) and is ultra-competitive with Qwen3.5 JSON few-shot (1pp exact gap, higher STORE F1). However, Qwen3.5 JSON few-shot remains the #1 overall system due to better target accuracy and zero sensitive failures.

**V0.5c confirms:**
1. ✅ Unit JSON is the best training interface (re-confirms v0.5b)
2. ✅ Qwen3.5 is a stronger base model than Qwen3-4B for JSON SFT (+10pp exact)
3. ✅ 500-case QLoRA r=8 is the best current QLoRA setup
4. ⚠ Safety remains the primary unsolved bottleneck
5. 🎯 1pp exact gap to few-shot — within reach of standard LoRA or r=16

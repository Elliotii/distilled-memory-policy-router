# V0.5c Qwen3.5 JSON LoRA 500 — Gold Baseline Comparison

**Date:** 2026-06-04  
**Split:** Locked gold only  

## Full Gold Ranking

| # | System | Exact | READ F1 | STORE F1 | Target Acc | SKIP F1 | Sensitive (genuine) |
|:-:|--------|:-----:|:-------:|:--------:|:----------:|:-------:|:-------------------:|
| 1 | Qwen3.5 JSON few-shot | **42%** | 0.911 | 0.963 | **79.1%** | **0.851** | **0** |
| **2** | **Qwen3.5 JSON LoRA 500** | **41%** | **0.938** | **0.969** | 73.7% | 0.847 | 5 |
| 3 | Qwen3.5 DSL few-shot | 36% | 0.901 | 0.959 | 77.6% | 0.795 | **0** |
| 4 | Qwen3-4B JSON LoRA 500 | 31% | 0.919 | 0.941 | 67.3% | 0.706 | 6 |
| 5 | Qwen3-4B JSON few-shot | 26% | 0.936 | 0.923 | 57.5% | 0.766 | **0** |
| 6 | Qwen3-4B DSL LoRA 500 | 16% | 0.923 | 0.946 | 47.5% | 0.718 | 6 |
| 7 | Qwen3-4B DSL few-shot | 7% | 0.882 | 0.850 | 60.5% | 0.422 | **0** |

## Key Questions

### Q1: Does Qwen3.5 JSON LoRA 500 beat Qwen3-4B JSON LoRA 500?
**Yes, decisively.** +10pp exact (41% vs 31%), +6.4pp target acc (73.7% vs 67.3%), +0.028 STORE F1, +0.141 SKIP F1, −1 fewer sensitive failure.

### Q2: Does Qwen3.5 JSON LoRA 500 beat Qwen3-4B JSON few-shot?
**Yes, on most metrics.** 41% vs 26% exact, 0.969 vs 0.923 STORE F1, 73.7% vs 57.5% target acc, 0.847 vs 0.766 SKIP F1. Qwen3-4B few-shot is safer (0 vs 5 sensitive).

### Q3: Does Qwen3.5 JSON LoRA 500 beat Qwen3.5 JSON few-shot?
**No, but ultra-competitive.** Few-shot leads by 1pp exact (42% vs 41%), 5.4pp target acc (79.1% vs 73.7%), and clean safety (0 vs 5). But LoRA wins STORE F1 (0.969 vs 0.963) and nearly ties SKIP F1 (0.847 vs 0.851).

### Q4: Is Qwen3.5 LoRA the best Qwen3.5 system?
**No, Qwen3.5 JSON few-shot remains #1 overall.** But the gap is the narrowest of any LoRA variant (1pp exact).

### Q5: Does Qwen3.5 LoRA preserve structural validity?
**Yes — 100% parse, 0 structural errors.** Better structural quality than any other trained system, matching few-shot quality.

### Q6: Safety?
**5 genuine failures** (vs 6 for Qwen3-4B LoRA, 0 for few-shot). Improved over Qwen3-4B: correctly skips credit cards and tokens but still stores PII (phones, addresses, emails) as user_profile.

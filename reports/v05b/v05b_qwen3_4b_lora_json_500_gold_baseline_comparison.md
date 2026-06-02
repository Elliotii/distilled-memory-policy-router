# V0.5b Qwen3-4B Unit JSON LoRA 500 Locked-Gold Baseline Comparison

**Date:** 2026-06-02  
**Context:** 5.7-E — locked-gold final evaluation  
**Split:** Locked gold (100 cases)  

---

## 1. Locked-Gold Results Table

| System | Parse | Exact | READ F1 | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:-----:|:-------:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON fs | 98% | **42%** | 0.911 | **0.963** | **79.1%** | **0.851** | **0 fails** |
| Qwen3.5 DSL fs | 99% | 36% | 0.901 | 0.959 | 77.6% | 0.795 | **0 fails** |
| **JSON LoRA 500** | **100%** | **31%** | 0.919 | 0.941 | 67.3% | 0.706 | 6 fails |
| Qwen3-4B JSON fs | 99% | 26% | **0.936** | 0.923 | 57.5% | 0.766 | **0 fails** |
| DSL LoRA 500 | — | 16% | 0.923 | 0.946 | 47.5% | 0.718 | 6 fails |
| Qwen3-4B DSL fs | 96% | 7% | 0.882 | 0.850 | 60.5% | 0.422 | **0 fails** |

**JSON LoRA 500 ranks #3 overall** behind Qwen3.5 JSON fs (#1) and Qwen3.5 DSL fs (#2).

## 2. Key Questions Answered

### Q1: Does JSON LoRA 500 beat DSL LoRA 500 on gold?
**Yes, decisively.**
- Exact: 31% vs 16% **(+15pp)**
- Target accuracy: 67.3% vs 47.5% **(+19.8pp)**
- STORE F1: 0.941 vs 0.946 (-0.005) — essentially tied
- SKIP F1: 0.706 vs 0.718 (-0.012) — essentially tied
- Sensitive: 6 fails vs 6 fails — tied

**The interface-ablation hypothesis is confirmed on gold: Unit JSON substantially outperforms Unit DSL for SFT training.**

### Q2: Does JSON LoRA 500 beat Qwen3-4B JSON few-shot on gold?
**Yes, on 3 of 5 primary metrics.**
- Exact: 31% vs 26% **(+5pp)** ✅
- STORE F1: 0.941 vs 0.923 **(+0.018)** ✅
- Target accuracy: 67.3% vs 57.5% **(+9.8pp)** ✅
- READ F1: 0.919 vs 0.936 (-0.017)
- SKIP F1: 0.706 vs 0.766 (-0.060)

**JSON 500 is the first LoRA variant to beat its teacher (same-model prompting baseline).** This demonstrates supervised training value beyond prompting.

### Q3: Does JSON LoRA 500 approach Qwen3.5 JSON few-shot?
**No. Qwen3.5 JSON fs remains #1.**
- Exact gap: -11pp (31% vs 42%)
- STORE F1 gap: -0.022 (0.941 vs 0.963)
- Target acc gap: -11.8pp (67.3% vs 79.1%)
- SKIP F1 gap: -0.145 (0.706 vs 0.851)
- Sensitive: 6 fails vs 0 — Qwen3.5 has zero sensitive failures

### Q4: Does JSON LoRA 500 improve target accuracy over DSL LoRA 500?
**Yes. +19.8pp (67.3% vs 47.5%).** This is the single largest improvement of v0.5b. JSON target accuracy on gold approaches prompting baselines; DSL was far behind.

### Q5: Does JSON LoRA 500 improve safety?
**No. Tied with DSL 500 (6 sensitive failures each).** Both formats store credentials, tokens, phones, and credit cards. Safety is not improved by interface format alone.

## 3. Historical Comparison

| System | Dev Target Acc | Gold Target Acc | Gap |
|--------|:-------------:|:--------------:|:---:|
| JSON LoRA 500 | 68.5% | 67.3% | -1.2pp |
| DSL LoRA 500 | 54.1% | 47.5% | -6.6pp |
| Qwen3-4B JSON fs | 67.1% | 57.5% | -9.6pp |

JSON 500 has the smallest dev→gold gap (-1.2pp) — the model generalizes very consistently.

---

## 4. Verdict

**Unit JSON LoRA is a successful v0.5b interface ablation.** JSON SFT substantially improves target classification over DSL SFT (+19.8pp on gold). JSON 500 beats its teacher (Qwen3-4B JSON few-shot) on exact, STORE F1, and target accuracy. However, Qwen3.5 JSON few-shot remains the strongest system overall, and safety remains unresolved (6 sensitive failures).

---

*End of V0.5b Gold Baseline Comparison.*

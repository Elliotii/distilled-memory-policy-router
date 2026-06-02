# V0.5b Qwen3-4B Unit JSON LoRA 125 vs DSL 125 Comparison

**Date:** 2026-06-02  
**Context:** 5.7-B — same-split dev comparison  
**Split:** Dev only (100 cases) — NOT locked gold  

---

## 1. JSON LoRA 125 vs DSL LoRA 125 (Dev)

| Metric | DSL LoRA 125 | JSON LoRA 125 | Delta |
|--------|:-----------:|:-------------:|:-----:|
| Parse success | 86.0% | **100.0%** | **+14.0pp** |
| Exact match | 12.0% | 11.0% | -1.0pp |
| READ F1 | 0.822 | **0.889** | +0.067 |
| STORE unit F1 | 0.867 | **0.910** | **+0.043** |
| STORE target acc | **60.0%** | 55.7% | -4.3pp |
| SKIP F1 | 0.492 | **0.535** | +0.043 |
| False store rate | 10.6% | **9.5%** | -1.1pp |
| Irrelevant read rate | 14.3% | 16.3% | +2.0pp |
| Sensitive store rate | 33.3% | 33.3% | 0 |
| Invalid memory IDs | 0.0% | 0.0% | — |
| Invalid unit IDs | 1.1% | **0.0%** | -1.1pp |
| Invalid targets | 1.7% | **0.0%** | -1.7pp |

### Key Findings

1. **Parse success: +14pp.** JSON eliminates all structural errors — no malformed lines, no ID confusion, no STORE NONE conflicts. This alone is a significant win.

2. **STORE F1: +0.043.** JSON LoRA improves action routing. The model learns WHAT to store/skip better in JSON format.

3. **READ F1: +0.067.** Memory selection improves with JSON.

4. **Target accuracy: -4.3pp.** JSON LoRA is slightly worse at classifying targets. This is consistent with v0.5 finding that target classification is the bottleneck regardless of format. 125 cases insufficient for 5-way classification.

5. **SKIP F1: +0.043.** Marginal improvement, but still low (0.535 vs gold).

6. **Sensitive store: unchanged (33.3%).** Same 10 cases, same difficulty.

## 2. JSON LoRA 125 vs Qwen3-4B JSON Few-Shot (Dev)

| Metric | JSON Few-Shot | JSON LoRA 125 | Delta |
|--------|:------------:|:-------------:|:-----:|
| Parse success | 99.0% | **100.0%** | +1.0pp |
| Exact match | **23.0%** | 11.0% | -12.0pp |
| STORE F1 | **0.961** | 0.910 | -0.051 |
| Target accuracy | **67.1%** | 55.7% | -11.4pp |
| SKIP F1 | **0.851** | 0.535 | -0.316 |
| Sensitive store | 33.3% | 33.3% | 0 |

JSON LoRA 125 does NOT beat JSON few-shot on any semantic metric. This is expected for 125 cases — same as DSL LoRA 125 not beating DSL few-shot.

## 3. JSON LoRA 125 vs Qwen3-4B DSL Few-Shot (Dev)

| Metric | DSL Few-Shot | JSON LoRA 125 | Delta |
|--------|:-----------:|:-------------:|:-----:|
| Parse success | 96.0% | **100.0%** | +4.0pp |
| STORE F1 | 0.936 | 0.910 | -0.026 |
| Target accuracy | **71.1%** | 55.7% | -15.4pp |
| SKIP F1 | **0.770** | 0.535 | -0.235 |

JSON LoRA 125 has better structure but lags on semantics vs prompting. More data needed.

## 4. Summary Table (All Dev Baselines)

| System | Parse | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:-----:|:--------:|:----------:|:-------:|:---------:|
| Qwen3-4B JSON fs | 99% | 23% | 0.961 | 67.1% | 0.851 | 33.3% |
| Qwen3-4B DSL fs | 96% | 22% | 0.936 | 71.1% | 0.770 | 33.3% |
| **JSON LoRA 125** | **100%** | 11% | **0.910** | 55.7% | 0.535 | 33.3% |
| DSL LoRA 125 | 86% | 12% | 0.867 | **60.0%** | 0.492 | 33.3% |

---

## 5. Interpretation

- JSON LoRA 125 achieves perfect structural quality — a clean win over DSL.
- STORE/SKIP routing improves (+0.043 STORE F1, +0.043 SKIP F1).
- Target classification is slightly worse — likely a small-N phenomenon.
- Both LoRA variants trail few-shot prompting on semantics.
- The JSON format advantage in structure suggests the model finds JSON easier to produce correctly.

**The JSON format eliminates the DSL parse-failure problem entirely.** This alone justifies proceeding to 250 cases.

---

*End of V0.5b JSON LoRA 125 vs DSL 125 Comparison.*

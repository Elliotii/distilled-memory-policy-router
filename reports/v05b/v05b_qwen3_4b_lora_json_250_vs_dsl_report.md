# V0.5b Qwen3-4B Unit JSON LoRA 250 vs DSL Baselines

**Date:** 2026-06-02  
**Context:** 5.7-C — cross-format comparison on dev  
**Split:** Dev only (100 cases) — NOT locked gold  

---

## 1. JSON 250 vs DSL 250 (Same Split, Same Train Size)

| Metric | DSL 250 | JSON 250 | Delta |
|--------|:-------:|:--------:|:-----:|
| Parse success | 99.0% | **100.0%** | +1.0pp |
| Exact match | 14.0% | **20.0%** | **+6.0pp** |
| READ F1 | **0.900** | 0.884 | -0.016 |
| STORE unit F1 | 0.944 | **0.947** | +0.003 |
| STORE target acc | 55.7% | **63.8%** | **+8.1pp** |
| SKIP F1 | 0.684 | **0.747** | **+0.063** |
| False store rate | 7.4% | **4.6%** | -2.8pp ✅ |
| Irrelevant read rate | **17.5%** | 19.0% | +1.5pp |
| Sensitive store rate | 66.7% | 66.7% | 0 |

**JSON wins on 6/9 metrics, DSL wins on 2, tie on 1.**

Key wins:
- **+8.1pp target accuracy** — the main research question answered: JSON SFT improves target classification over DSL SFT at 250 cases.
- **+6pp exact match** — more complete correct decisions.
- **+0.063 SKIP F1** — better skip prediction.
- **-2.8pp false store** — fewer incorrect stores.

## 2. JSON 250 vs DSL 500

| Metric | DSL 500 | JSON 250 | Delta |
|--------|:-------:|:--------:|:-----:|
| Parse success | (not in dev eval) | 100.0% | — |
| Exact match | 24.0% | 20.0% | -4.0pp |
| READ F1 | — | 0.884 | — |
| STORE unit F1 | **0.962** | 0.947 | -0.015 |
| STORE target acc | 54.1% | **63.8%** | **+9.7pp** |
| SKIP F1 | 0.773 | 0.747 | -0.026 |
| Sensitive store rate | 66.7% (dev) | 66.7% | 0 |

**JSON 250 at 63.8% target accuracy already exceeds DSL 500 at 54.1% by 9.7pp.** This is a dramatic finding: half the training data in JSON format achieves significantly better target classification than double the data in DSL format.

## 3. JSON 250 vs Qwen3-4B JSON Few-Shot (Dev)

| Metric | JSON Few-Shot | JSON 250 | Delta |
|--------|:------------:|:--------:|:-----:|
| Parse success | 99.0% | **100.0%** | +1.0pp |
| Exact match | **23.0%** | 20.0% | -3.0pp |
| STORE F1 | **0.961** | 0.947 | -0.014 |
| Target accuracy | **67.1%** | 63.8% | -3.3pp |
| SKIP F1 | **0.851** | 0.747 | -0.104 |

**JSON 250 is approaching but not yet beating JSON few-shot** on semantic metrics. The gap has narrowed significantly from 125 (e.g., target acc gap: -11.4pp at 125 → -3.3pp at 250).

## 4. Full Dev Baselines Table

| System | Parse | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:-----:|:--------:|:----------:|:-------:|:---------:|
| Qwen3-4B JSON fs | 99% | 23% | 0.961 | 67.1% | 0.851 | 33.3% |
| Qwen3-4B DSL fs | 96% | 22% | 0.936 | 71.1% | 0.770 | 33.3% |
| **JSON LoRA 250** | **100%** | 20% | **0.947** | 63.8% | 0.747 | 66.7% |
| DSL LoRA 500 | — | 24% | 0.962 | 54.1% | 0.773 | — |
| DSL LoRA 250 | 99% | 14% | 0.944 | 55.7% | 0.684 | 66.7% |
| JSON LoRA 125 | 100% | 11% | 0.910 | 55.7% | 0.535 | 33.3% |
| DSL LoRA 125 | 86% | 12% | 0.867 | 60.0% | 0.492 | 33.3% |

---

## 5. Critical Finding: Target Accuracy Trajectory

| System | 125 | 250 | 500 |
|--------|:---:|:---:|:---:|
| DSL target acc | 60.0% | 55.7% | 54.1% |
| JSON target acc | 55.7% | **63.8%** | ? |

**DSL target accuracy decreases with more data, while JSON target accuracy increases.** This is the strongest evidence so far that JSON SFT is fundamentally better for target classification. The DSL format may be confusing the model (e.g., "STORE service_memory u1" vs "STORE task_state u1" — the target word appears before the unit, which may trigger positional confusion), while JSON's structured `{"target": "service_memory", "unit_id": "u1"}` provides cleaner separation.

---

*End of V0.5b JSON 250 vs DSL Comparison.*

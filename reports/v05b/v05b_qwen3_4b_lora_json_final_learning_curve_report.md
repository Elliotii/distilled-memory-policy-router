# V0.5b Qwen3-4B Unit JSON LoRA Final Learning Curve (Dev + Gold)

**Date:** 2026-06-02  
**Context:** 5.7-E — complete v0.5b learning curve with gold endpoint  

---

## 1. JSON LoRA Dev Learning Curve

| Metric | 125 | 250 | 500 | Δ (125→500) |
|--------|:---:|:---:|:---:|:---:|
| Parse success | 100% | 100% | 100% | 0 |
| Exact match | 11% | 20% | 34% | **+23pp** |
| READ F1 | 0.889 | 0.884 | 0.902 | +0.013 |
| STORE unit F1 | 0.910 | 0.947 | 0.958 | +0.048 |
| Target accuracy | 55.7% | 63.8% | 68.5% | **+12.8pp** |
| SKIP F1 | 0.535 | 0.747 | 0.753 | +0.218 |
| False store | 9.5% | 4.6% | 6.5% | -3.0pp |
| Irrelevant read | 16.3% | 19.0% | 15.9% | -0.4pp |

## 2. DSL LoRA Dev Learning Curve (Reference)

| Metric | 125 | 250 | 500 | Trend |
|--------|:---:|:---:|:---:|:-----:|
| Parse | 86% | 99% | — | ↗ |
| Exact | 12% | 14% | 24% | ↗ |
| STORE F1 | 0.867 | 0.944 | 0.962 | ↗ |
| Target acc | 60.0% | 55.7% | 54.1% | **↘** |
| SKIP F1 | 0.492 | 0.684 | 0.773 | ↗ |

## 3. Gold Endpoint Comparison

| System | Exact | STORE F1 | Target Acc | SKIP F1 | Sensitive |
|--------|:-----:|:--------:|:----------:|:-------:|:---------:|
| Qwen3.5 JSON fs | 42% | 0.963 | 79.1% | 0.851 | 0 |
| Qwen3.5 DSL fs | 36% | 0.959 | 77.6% | 0.795 | 0 |
| JSON LoRA 500 | 31% | 0.941 | 67.3% | 0.706 | 6 |
| Qwen3-4B JSON fs | 26% | 0.923 | 57.5% | 0.766 | 0 |
| DSL LoRA 500 | 16% | 0.946 | 47.5% | 0.718 | 6 |
| Qwen3-4B DSL fs | 7% | 0.850 | 60.5% | 0.422 | 0 |

## 4. Training Convergence

| System | Epoch 1 | Epoch 2 | Epoch 3 | Final Token Acc |
|--------|:-------:|:-------:|:-------:|:---------------:|
| JSON 125 | 1.919 | 1.424 | 1.300 | 72.6% |
| JSON 250 | 1.326 | 0.659 | 0.608 | 86.5% |
| JSON 500 | 0.611 | 0.548 | 0.544 | 87.2% |
| DSL 125 | 2.30 | 1.67 | 1.52 | — |
| DSL 250 | 1.54 | 0.73 | 0.68 | — |
| DSL 500 | — | — | 0.62 | — |

JSON trains to lower loss at every data size. The format is intrinsically easier to learn.

## 5. Key Visualizations (Text)

### Target Accuracy Trajectory
```
        80% ┤
            │                              ● Q3.5 JSON fs (79.1%)
        70% ┤                    ●━━━━━━━━● JSON 500 gold (67.3%)
            │              ●━━━━●          JSON 250→500 dev
        60% ┤        ●━━━━●                JSON 125→250 dev
            │  ●━━━━●                      DSL 125→250 dev
        50% ┤                    ●━━━━━━━━● DSL 500 gold (47.5%)
            │
        40% ┤
            └─────┬─────┬─────┬─────┬──────
                 125   250   500   gold
```

### Exact Match Trajectory
```
        45% ┤ ● Q3.5 JSON fs (42%)
            │
        35% ┤           ●━━━━● JSON 500 gold (31%)
            │     ●━━━━●       JSON 250→500 dev
        25% ┤ ●━━━━●           JSON 125→250 dev
            │           ●━━━━● DSL 500 gold (16%)
        15% ┤ ●━━━━●           DSL 125→250 dev
            │
         5% ┤
            └─────┬─────┬─────┬─────┬──────
                 125   250   500   gold
```

---

*End of V0.5b Final Learning Curve Report.*

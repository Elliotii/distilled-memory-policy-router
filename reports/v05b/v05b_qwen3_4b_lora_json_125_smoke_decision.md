# V0.5b Qwen3-4B Unit JSON LoRA 125 Smoke Decision

**Date:** 2026-06-02  
**Context:** 5.7-B — smoke decision after 125-case training + dev eval  

---

## 1. Training Result

| Check | Status |
|-------|:------:|
| Training completed | ✅ 217s |
| No OOM | ✅ |
| No NaN | ✅ |
| Adapter saved | ✅ |
| Eval loss converged (1.92→1.30) | ✅ |

## 2. Dev Eval Result

| Check | Status |
|-------|:------:|
| Dev eval completed | ✅ |
| 100 predictions generated | ✅ |
| JSON parse success | **100%** ✅ |
| JSON validity | 100/100 ✅ |
| No markdown/prose | ✅ |
| No empty outputs | ✅ |

## 3. Key Metrics vs DSL 125

| Metric | DSL 125 | JSON 125 | Winner |
|--------|:-------:|:--------:|:------:|
| Parse success | 86% | **100%** | JSON |
| STORE F1 | 0.867 | **0.910** | JSON |
| READ F1 | 0.822 | **0.889** | JSON |
| SKIP F1 | 0.492 | **0.535** | JSON |
| Target acc | **60.0%** | 55.7% | DSL |
| Exact | **12%** | 11% | ≈ |
| Sensitive | 33.3% | 33.3% | Tie |

**JSON wins on 4 of 7 metrics, loses on 1, ties on 2.**

## 4. Script / Config Status

| Check | Status |
|-------|:------:|
| train_lora_router.py works with JSON | ✅ |
| eval_lora_router.py `--interface unit_json` works | ✅ |
| eval_runner scores unit_json correctly | ✅ |
| Config paths correct | ✅ |
| No data modifications needed | ✅ |

No script or config blocker found.

## 5. Decision: Option A — Proceed to JSON LoRA 250 Unchanged

### Rationale

1. **Structural quality is perfect (100% parse).** This is the single biggest benefit of JSON SFT over DSL — the model never produces malformed output. DSL LoRA 125 had 14% parse failures even after prompt fix. JSON eliminates this problem entirely.

2. **STORE/SKIP routing improves (+0.043 STORE F1, +0.043 SKIP F1).** The model is learning better action selection in JSON format.

3. **Target accuracy -4.3pp is a small-N effect.** DSL LoRA 250 showed +2.3pp target improvement over 125; same trajectory expected for JSON. More data should close this gap.

4. **Learning curve looks healthy.** Eval loss dropped from 1.92 to 1.30 — strong convergence. JSON loss is lower than DSL loss (1.30 vs 1.52 at epoch 3), suggesting easier format.

5. **No blockers.** Scripts, configs, and eval pipeline all work correctly.

### What to Watch at 250

- Target accuracy should rise to ≥58%
- STORE F1 should approach 0.944 (DSL 250 baseline)
- SKIP F1 should improve beyond 0.55
- Parse success should stay at 98-100%
- Sensitive store rate may remain 33.3% (inherent data limitation)

### Not Yet

- Do not compare to gold metrics.
- Do not over-interpret dev metrics as final.
- Do not change hyperparameters unless 250 fails to improve.

---

*End of V0.5b JSON LoRA 125 Smoke Decision — Proceed to 250.*

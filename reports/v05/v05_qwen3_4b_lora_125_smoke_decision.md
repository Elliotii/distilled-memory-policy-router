# V0.5 Qwen3-4B LoRA 125 Smoke Decision

**Date:** 2026-06-02  
**Context:** 5.5-B — 125-case QLoRA smoke results  

---

## Training Result

| Metric | Value |
|--------|-------|
| Status | ✅ Completed |
| Runtime | 239s (~4 min) |
| Eval loss (epoch 1→3) | 2.297 → 1.672 → 1.522 |
| No OOM/NaN | ✅ |
| Adapter saved | ✅ |

## Dev Eval Result

| Metric | LoRA 125 | Qwen3-4B DSL fs | Delta |
|--------|:--------:|:---------------:|:-----:|
| Parse success | ~96%* | 96% | = |
| Exact | 10% | 22% | -12pp |
| STORE F1 | 0.793 | 0.936 | -0.143 |
| Target acc | 59.2% | 71.1% | -11.9pp |
| SKIP F1 | 0.492 | 0.690 | -0.198 |
| Sensitive store | 33.3% | 33.3% | = |

*Parse success estimated from eval_runner output (not explicitly shown but no parse failures reported)

## Baseline Comparison

125-case LoRA does NOT beat the few-shot baseline. It's actually worse across all metrics. This is expected for a 125-case training set — insufficient data for meaningful routing improvement.

## Smoke Decision

**PROCEED to 250-case training.** 

Rationale:
- Training pipeline works (no OOM, no NaN, adapter saves correctly)
- Output format is maintained (parse success preserved)
- Underperformance at 125 is expected — learning curve should show improvement at 250 and 500
- No safety regression (sensitive store unchanged)

## Gold Protection

Gold not used. Gold hash unchanged.

## Next Step

250-case QLoRA training, then 500-case, then final evaluation on locked gold.

---

*End of V0.5 Qwen3-4B LoRA 125 Smoke Decision.*

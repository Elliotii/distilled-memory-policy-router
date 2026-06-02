# V0.5 Qwen3-4B LoRA 125 Postmortem

**Date:** 2026-06-02  
**Context:** 5.5-B2 — 125 smoke audit  

---

## 1. Training Success

✅ Completed: 239s, no OOM/NaN, adapter saved (23.6MB safetensors).

## 2. Dev Underperformance

| Metric | LoRA 125 | Few-shot DSL | Delta |
|--------|:--------:|:------------:|:-----:|
| Parse success | 75% | 96% | **-21pp** |
| Exact | 10% | 22% | -12pp |
| STORE F1 | 0.793 | 0.936 | -0.143 |

## 3. Parse Failure Taxonomy (25 cases)

- **Memory-ID-as-unit-ID:** `STORE service_memory m1` (model outputs memory IDs in STORE lines) — ~15 cases
- **STORE NONE + STORE assignment conflict:** `STORE NONE` alongside valid STORE lines — ~5 cases  
- **Other DSL errors:** Malformed lines, missing assignments — ~5 cases

## 4. Train125 Eval

| Metric | Train125 | Dev |
|--------|:--------:|:---:|
| Exact | 13.6% | 10% |
| STORE F1 | 0.753 | 0.793 |

**Train performance is NOT higher than dev.** This means the model is NOT overfitting — it hasn't even learned the training data well. Suggests undertraining or format confusion.

## 5. Adapter Sanity

✅ Adapter loaded correctly: PEFT LoRA, 4 target modules, 23.6MB, base model path verified.

## 6. Rendering Consistency

**Found mismatch:** eval_lora_router.py uses a different system prompt than the SFT training data. The SFT uses `render_sft_messages.py`'s SYSTEM_PROMPT, while eval uses a custom prompt. This may cause distribution shift between training and inference.

## 7. Sensitive Store

33.3% on both train and dev — unchanged from baseline. The sensitive store issue is pre-existing in the data, not caused by LoRA training.

## 8. Decision: Option B + C

**Fix eval prompt to match SFT training prompt, then retest.** If train125 still shows low metrics after prompt fix, increase epochs to 5 for 125 before scaling to 250.

---

*End of V0.5 Qwen3-4B LoRA 125 Postmortem.*

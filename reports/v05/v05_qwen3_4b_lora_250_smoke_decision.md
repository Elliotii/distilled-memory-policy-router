# V0.5 Qwen3-4B LoRA 250 Smoke Decision

**Date:** 2026-06-02  

## Training

✅ 326s, eval loss 1.54→0.73→0.68, no OOM/NaN.

## Dev Eval

| Metric | 250 LoRA | 125 LoRA | Few-shot DSL |
|--------|:--------:|:--------:|:------------:|
| Exact | 14% | 12% | 22% |
| STORE F1 | **0.944** | 0.867 | 0.936 |
| Target acc | 55.7% | 60.0% | 71.1% |
| SKIP F1 | 0.684 | 0.492 | 0.690 |
| Sensitive | 66.7% | 33.3% | 33.3% |

**STORE F1 crossed few-shot baseline** (0.944 > 0.936). Target accuracy regressed — model learns WHAT to store faster than WHICH target. Expected to improve at 500.

## Decision

**Option A: Proceed to 500 unchanged.** Learning curve shows improvement. STORE F1 beat few-shot. Target accuracy needs more data.

---

*End of V0.5 Qwen3-4B LoRA 250 Smoke Decision.*

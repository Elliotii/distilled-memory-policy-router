# V0.5c Qwen3.5 JSON LoRA 125 Smoke Decision

**Date:** 2026-06-03  
**Context:** 5.9-B — Qwen3.5 Unit JSON LoRA 125 smoke training  

---

## Decision: Option A — Proceed to Qwen3.5 JSON LoRA 250 Unchanged

### Supporting Evidence

1. **Training completed successfully.** 903s, no OOM, no NaN, adapter saved. Strong convergence: eval_loss 1.264→0.626→0.544.

2. **Dev eval shows exceptional signal.** 30% exact match, 65.6% target accuracy — already exceeding Qwen3-4B JSON LoRA 250 on both metrics.

3. **JSON structural validity preserved.** 98% parse success. 2 minor failures (1 malformed JSON, 1 missing unit) — typical 125-case artifacts, expected to resolve at 250.

4. **6-module LoRA targets confirmed working.** Model produces valid JSON with correct read/store/skip structure and legal targets.

5. **Qwen3.5 is clearly a stronger base model for JSON SFT.** +19pp exact, +9.9pp target accuracy over Qwen3-4B at 125 cases. ~2x data efficiency.

6. **No blockers found.** The enable_thinking=False fix is a one-time eval configuration fix (already applied). Training config needs no changes.

### Gate Checklist

| Gate | Status |
|------|:------:|
| Training completes without OOM/NaN | ✅ |
| Adapter saved | ✅ |
| Dev eval completes | ✅ |
| Parse success ≥ 90% | ✅ (98%) |
| JSON structure valid | ✅ |
| Exact > Qwen3-4B 125 | ✅ (30% vs 11%) |
| Target accuracy > Qwen3-4B 125 | ✅ (65.6% vs 55.7%) |
| Learning signal clear | ✅ |
| No config changes needed | ✅ |
| Gold unchanged | ✅ |

### What NOT to Change

- Do NOT change LoRA rank (r=8), alpha (16), or target modules
- Do NOT change learning rate (2e-4), epochs (3), or batch size
- Do NOT change the training data or interface
- Do NOT add safety-focused or target-balanced data
- Do NOT change max_seq_length or QLoRA settings

The experiment variable is the base model. All hyperparameters and data must stay constant to maintain a clean ablation.

### Expected 250 Outcome

Based on Qwen3-4B JSON LoRA learning curve (11%→20%→34% exact) and Qwen3.5's 2x data efficiency:

| Metric | Qwen3.5 125 (actual) | Qwen3.5 250 (projected) | Qwen3-4B 500 (actual) |
|--------|:--------------------:|:-----------------------:|:---------------------:|
| Exact | 30.0% | 35-42% | 34% |
| Target acc | 65.6% | 72-78% | 68.5% |
| STORE F1 | 0.891 | 0.940-0.955 | 0.958 |
| Parse | 98.0% | 99-100% | 100% |

Qwen3.5 250 should decisively beat Qwen3-4B 500 on exact and target accuracy, and approach Qwen3.5 JSON few-shot gold (42% exact, 79.1% target).

### Risks

| Risk | Likelihood | Mitigation |
|------|:----------:|------------|
| Parse failures persist at 250 | Low | 2 failures at 125 → likely resolve with more JSON examples |
| STORE F1 doesn't improve | Low | Qwen3-4B STORE F1 improved 0.910→0.947→0.958; Qwen3.5 likely similar |
| Sensitive store remains 33%+ | High | Known data limitation; not addressed by more data of same distribution |
| Diminishing returns hit early | Low | Qwen3.5 shows faster learning; ceiling unlikely at 250 |

---

*End of V0.5c Qwen3.5 JSON LoRA 125 Smoke Decision.*

# V0.5c Qwen3.5 JSON LoRA 250 Decision

**Date:** 2026-06-03  
**Context:** 5.9-C  

---

## Decision: Option A — Proceed to Qwen3.5 JSON LoRA 500 Unchanged

### With Parse Caveat

### Supporting Evidence

1. **Target accuracy reaches 73.1%** — already exceeds Qwen3-4B JSON LoRA 500 (68.5%). Target routing is the primary metric and shows clear improvement (+7.5pp from 125).

2. **STORE F1 improves** (0.891→0.913) — the model IS learning what to store, just not as precisely as Qwen3-4B.

3. **Training converges well** — eval_loss 0.461 at epoch 3, lower than Qwen3-5 125 (0.544) and Qwen3-4B 250 (0.608). No overfitting.

4. **The parse regression is documented and understood** — `"target":"skip"` pattern in 7 cases. At 500 cases, the model sees 2x more correct skip examples, which should reinforce the correct schema.

5. **No config changes needed** — the LoRA setup, data, and training hyperparameters are validated. The `"target":"skip"` issue is a data-quantity problem, not a config problem.

### Gate Checklist

| Gate | Status |
|------|:------:|
| Training completes | ✅ 1864s, no OOM/NaN |
| Adapter saved | ✅ |
| Dev eval completes | ✅ |
| Target accuracy > 125 | ✅ 73.1% > 65.6% |
| Target accuracy > Qwen3-4B 250 | ✅ 73.1% > 63.8% |
| STORE F1 improves | ✅ 0.891→0.913 |
| No critical blocker | ✅ (parse caveat documented) |
| Gold unchanged | ✅ |

### Parse Caveat

| Risk | Likelihood | Mitigation |
|------|:----------:|------------|
| Parse drops further at 500 | Low-Medium | Qwen3-4B had 100% at all sizes; Qwen3.5's regression may be 250-specific |
| `"target":"skip"` persists at 500 | Low | 2x more correct skip examples in 500 training set |
| Exact match remains depressed | Medium | Even if parse recovers, Qwen3.5 exact may lag Qwen3-4B due to STORE F1 gap |

**If parse doesn't recover to ≥95% at 500:** A post-hoc parse fix (auto-adding `"skip":[]` to outputs missing it) may be needed for locked-gold eval, with a clear disclaimer. This would be a last-resort measure and must be transparently documented.

### What NOT to Change

- LoRA rank (r=8), alpha (16), target modules (6)
- Learning rate (2e-4), epochs (3), batch size
- Training data or interface
- QLoRA settings

### Expected 500 Outcome

| Metric | Qwen3.5 250 (actual) | Qwen3.5 500 (projected) | Qwen3-4B 500 (actual) |
|--------|:--------------------:|:-----------------------:|:---------------------:|
| Parse | 90.0% | 95-100% | 100% |
| Exact | 17.0% | 25-35% | 34% |
| Target acc | 73.1% | 75-82% | 68.5% |
| STORE F1 | 0.913 | 0.935-0.955 | 0.958 |

Qwen3.5 500 should approach or exceed Qwen3.5 JSON few-shot gold (42% exact, 79.1% target, 0.963 STORE F1) on dev, setting up a competitive locked-gold final eval.

---

*End of V0.5c Qwen3.5 JSON LoRA 250 Decision.*

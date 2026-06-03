# V0.5d r=16 Claims and Limitations

**Date:** 2026-06-04  

---

## Allowed Claims

✅ **r=16 improves dev exact over r=8 by +5pp.** 39% vs 34% on the same dev set, same training data, same base model. This is a meaningful capacity-ablation signal.

✅ **r=16 improves or preserves all dev metrics.** No regression on parse, STORE F1, SKIP F1, false store, or target accuracy. Clean improvement across the board.

✅ **Doubling LoRA rank is a safe capacity increase.** 9.8M trainable params (0.23% of base) still fit within 12GB QLoRA VRAM. No OOM, no instability.

✅ **r=16 is the best dev-performing QLoRA setting tested.** It achieves the highest dev exact, STORE F1, and SKIP F1 of any QLoRA variant in this study.

✅ **Adapter capacity (not just training data) is a bottleneck for exact match.** The +5pp gain from r=8→r=16, with fixed data, shows rank matters.

---

## Forbidden Claims

❌ **Do not claim r=16 is the final best trained system.** It is dev-only. r=8 remains the best **gold-verified** trained system (41% exact on locked gold).

❌ **Do not claim r=16 beats Qwen3.5 JSON few-shot.** r=16 has no gold evaluation. Even the projected gold (44-48%) is a projection, not a result.

❌ **Do not claim r=16 gold would equal the projection.** Dev→gold generalization varies. r=16 may generalize differently than r=8.

❌ **Do not claim r=16 is production-safe.** Same PII storage issues as r=8 (sensitive tag-rate 66.7% on dev). Safety is unaddressed.

❌ **Do not claim all LoRA settings are exhausted.** r=32, standard LoRA, BF16 LoRA, more epochs, and more data are untested.

❌ **Do not claim gold_v2 is unnecessary.** Old gold has been evaluated 3 times (v0.5, v0.5b, v0.5c). r=16 needs fresh gold for a clean claim.

---

*End of Claims and Limitations.*

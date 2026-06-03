# V0.5c Final Claims and Limitations

**Date:** 2026-06-04  

---

## Allowed Claims

✅ **Qwen3.5 JSON LoRA 500 is the best trained router in this study.** 41% exact, 0.969 STORE F1, 73.7% target accuracy on locked gold. Beats Qwen3-4B JSON LoRA 500 by +10pp exact, +6.4pp target accuracy.

✅ **Qwen3.5 is a stronger base model than Qwen3-4B for JSON SFT.** At 500 training cases, Qwen3.5 achieves 10pp higher exact match and 6.4pp higher target accuracy on the same data and QLoRA setup.

✅ **Qwen3.5 JSON LoRA 500 achieves the highest STORE F1 of any system in this study (0.969).** This includes the Qwen3.5 JSON few-shot baseline (0.963).

✅ **Qwen3.5 JSON LoRA 500 is within 1pp of Qwen3.5 JSON few-shot on exact match (41% vs 42%).** The narrowest gap of any trained variant.

✅ **Unit JSON is the confirmed best training interface.** Re-confirms v0.5b's finding: JSON SFT eliminates parse errors, enables learnable target classification, and produces consistent generalization across two base models.

✅ **Qwen3.5 JSON LoRA 500 improved credential safety over Qwen3-4B JSON LoRA 500.** 0 credit card/token stores on gold (vs 2 for Qwen3-4B).

✅ **Dev→gold generalization is excellent.** Exact improved by +7pp, STORE F1 by +0.010, parse from 98% to 100% on gold. Dev was a conservative estimator.

---

## Forbidden Claims

❌ **Do not claim Qwen3.5 JSON LoRA beats Qwen3.5 JSON few-shot overall.** Few-shot leads on exact (42% vs 41%), target accuracy (79.1% vs 73.7%), and safety (0 vs 5). LoRA only leads on STORE F1.

❌ **Do not claim production-safe.** Model stores 5 units of PII (phones, addresses, emails) as user_profile on locked gold. Not safe for deployment.

❌ **Do not claim safety is solved or improved for PII.** Credential safety improved (0 token/credit card stores) but PII storage (phone/address/email → user_profile) persists unchanged.

❌ **Do not claim all LoRA settings are exhausted.** Only QLoRA r=8 tested. Standard LoRA, BF16 LoRA, r=16, and more data are untested.

❌ **Do not claim Qwen3.5 is universally better than Qwen3-4B.** Qwen3-4B had 100% parse across all sizes vs Qwen3.5's 90% dip at 250. Qwen3.5 is stronger on semantics but not uniformly better on structural consistency.

❌ **Do not claim target routing is fully solved.** 73.7% target accuracy means 26.3% of STORE units receive wrong targets. repo_memory and project_memory likely remain weak.

❌ **Do not claim gold remains blind for future variants.** Gold has been evaluated 3 times (v0.5 DSL 500, v0.5b JSON 500, v0.5c JSON 500). Future tuned variants on the same gold are not fully blind.

❌ **Do not claim 500 cases are sufficient for all purposes.** Target accuracy at 73.7% with diminishing returns from 250→500 (+4.3pp). Safety needs dedicated training, not just more generic data.

---

*End of V0.5c Final Claims and Limitations.*

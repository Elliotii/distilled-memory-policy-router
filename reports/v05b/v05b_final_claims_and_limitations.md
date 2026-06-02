# V0.5b Final Claims and Limitations

**Date:** 2026-06-02  

---

## Allowed Claims

✅ **Unit JSON LoRA improved target routing over Unit DSL LoRA on locked gold.** Target accuracy: 67.3% (JSON) vs 47.5% (DSL) = +19.8pp. Exact match: 31% vs 16% = +15pp. The interface-ablation hypothesis is confirmed.

✅ **Unit JSON LoRA beat Qwen3-4B JSON few-shot on exact match and target accuracy.** JSON 500: 31% exact, 67.3% target acc vs JSON fs: 26% exact, 57.5% target acc. First LoRA variant to exceed same-model prompting.

✅ **Unit JSON generated 100% valid structured outputs across 400 predictions.** Zero parse errors, invalid JSON, markdown, or structural failures. JSON format eliminates all DSL parse issues.

✅ **Unit JSON target accuracy increases with training data** (55.7%→63.8%→68.5%) while DSL target accuracy decreases (60.0%→55.7%→54.1%). JSON enables sustained learning.

✅ **Unit JSON is the preferred interface for future supervised training.** Demonstrated superiority over DSL on all metrics except STORE F1 (within 0.005).

✅ **V0.5b identified safety as the next bottleneck.** 6 sensitive failures documented — same count as DSL 500, worse than Qwen3.5 prompting (0).

✅ **Service/task distinction is learnable in JSON format.** Service memory accuracy improved from ~25% (DSL 500) to 70% (JSON 500) on gold.

---

## Forbidden Claims

❌ **Do not claim production-safe.** Model stores credit cards (with CVV), access tokens, phone numbers, and addresses. 6 genuine sensitive failures on locked gold.

❌ **Do not claim sensitive safety solved.** Safety is tied with DSL 500 (6 failures each) and worse than Qwen3.5 prompting (0 failures).

❌ **Do not claim Qwen3-4B JSON LoRA beats Qwen3.5 prompting.** Qwen3.5 JSON few-shot leads by 11pp exact, 11.8pp target accuracy, 0.022 STORE F1, and 0 sensitive failures.

❌ **Do not claim JSON is universally superior for all tasks.** This result is specific to memory policy routing with the current schema and datasets.

❌ **Do not claim target routing is fully solved.** 67.3% target accuracy on gold means 32.7% of STORE units receive wrong targets.

❌ **Do not claim repo_memory classification is adequate.** 50% accuracy on gold — weakest class.

❌ **Do not claim gold remains blind for future tuned variants.** Gold has been evaluated once. Future variants on the same gold are not fully blind.

❌ **Do not claim 500 cases are sufficient.** Target accuracy at 67.3% with diminishing returns from 250→500 suggests model is near ceiling with current architecture. Safety needs dedicated training, not just more data.

---

*End of V0.5b Final Claims and Limitations.*

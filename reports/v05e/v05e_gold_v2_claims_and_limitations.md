# V0.5e gold_v2 Claims and Limitations

**Date:** 2026-06-04  

---

## Allowed Claims (Post gold_v2)

✅ **r=16 outperforms r=8 on exact match** — ONLY if paired bootstrap 95% CI lower bound > 0.

✅ **r=16 is directionally promising** — if CI includes 0 but r=16 ≥ r=8 on exact and all secondary metrics are non-regressing.

✅ **r=16 is competitive with Qwen3.5 JSON few-shot** — if exact CI overlaps with few-shot result, with appropriate statistical qualification.

✅ **r=16 preserves or improves parse quality** — if parse ≥ r=8 parse.

✅ **r=16 does not increase sensitive-store failures** — if genuine sensitive count ≤ r=8.

✅ **Increasing LoRA rank from r=8 to r=16 provides measurable improvement** — if r=16 wins on primary metric with CI support.

## Forbidden Claims

❌ **Do not claim r=16 is production-safe.** Sensitive-store failures persist unless explicitly addressed by safety training.

❌ **Do not claim r=16 beats Qwen3.5 JSON few-shot** without CI support and qualification. "Competitive" is the ceiling absent clear statistical separation.

❌ **Do not claim globally optimal LoRA configuration.** Only r=8 and r=16 tested. r=4, r=32, standard LoRA, and BF16 LoRA are untested.

❌ **Do not claim results generalize to other tasks or domains.** Results are specific to the Memory Policy Router task with the current dataset construction methodology.

❌ **Do not compare gold_v2 metrics to old-gold metrics as final evidence.** Cross-set comparisons are not same-split evidence. Old gold is secondary/non-blind.

❌ **Do not claim n=150 eliminates all statistical uncertainty.** 5pp differences have ~3.9pp standard error at p≈0.35. Report CIs always.

❌ **Do not claim gold_v2 is fully blind after one evaluation.** gold_v2 is blind for its first evaluation only. Future experiments on gold_v2 will have the same issue.

---

*End of Claims and Limitations.*

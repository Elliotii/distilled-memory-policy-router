# V0.5e gold_v2 Pre-Registration

**Date:** 2026-06-04  
**Status:** Pre-registration — no data generated  

---

## Evaluated Systems (locked before gold_v2 generation)

All systems evaluated on the same 150 gold_v2 cases:

1. **Qwen3.5 Unit JSON QLoRA r=16 500** — primary test system
2. **Qwen3.5 Unit JSON QLoRA r=8 500** — current best gold-verified trained system
3. **Qwen3.5 JSON few-shot** — best overall baseline
4. **Qwen3-4B Unit JSON QLoRA r=8 500** — previous-generation trained baseline
5. **Empty/no-action baseline** — trivial deterministic sanity check (optional)

**Evaluation rules:**
- All systems evaluated on identical cases after gold_v2 is locked
- No system output inspected before all evaluations complete
- No gold_v2 modification after any evaluation begins
- Strict parser only — no post-processing repair

## Primary Metric

**Paired exact-match difference: r=16 vs r=8 on identical gold_v2 cases.**

## Primary Success Criterion

**r=16 can be called better than r=8 ONLY if:**
- Paired bootstrap 95% CI lower bound > 0 on exact match difference

## Secondary Metrics

- STORE F1
- SKIP F1
- READ F1
- Target accuracy
- Parse success
- False store rate
- Irrelevant read rate
- Sensitive-store failure count (genuine audit, not eval_runner tag-rate)

## Safety Gate

- r=16 sensitive-store failure count MUST be ≤ r=8
- If r=16 has MORE sensitive failures, do NOT call it a better router even if exact improves

## Fallback Conclusions

**If CI includes 0 but r=16 directionally ≥ r=8 on exact:**
> "r=16 is directionally promising / statistically indistinguishable from r=8 on gold_v2. All supporting metrics are non-regressing."

**If r=16 regresses on any metric:**
> "r=16 does not provide a clear advantage over r=8 on gold_v2. r=8 remains the recommended QLoRA setting."

## Few-Shot Comparison

- r=16 vs Qwen3.5 JSON few-shot comparison is **secondary**
- Do NOT set "beats few-shot" as success criterion
- If r=16 is close to few-shot, report as "competitive" with CIs
- Do NOT claim superiority over few-shot without CI lower bound > 0

## Statistical Reporting

- Paired bootstrap 95% CI for exact difference (r=16 − r=8)
- Effect size in percentage points AND raw case count
- McNemar-style paired disagreement counts if feasible
- All metrics reported with CIs where appropriate

---

*End of Pre-Registration.*

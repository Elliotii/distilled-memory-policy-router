# v05g BF16 LoRA — Claim Boundaries

**Date:** 2026-06-05  
**Scope:** What conclusions CAN and CANNOT be drawn from the v05g BF16 LoRA experiment

## Research Questions Under Test

| # | Question | Tested By |
|---|----------|-----------|
| Q1 | Does BF16 standard LoRA r16 improve over QLoRA r16 with identical 500 data? | BF16 r16 500 vs existing QLoRA r16 500 |
| Q2 | Does adding 500 targeted-balanced examples (broader domains) improve over BF16 r16 500? | BF16 r16 1000 vs BF16 r16 500 |

## SAFE Claims (If Measured)

### C1: BF16 vs QLoRA Precision Comparison
> "BF16 standard LoRA r16 trained on the same 500-control data achieves [better/similar/worse] dev set performance compared to QLoRA r16 500."

**Requirements:**
- Same seed data confirmed (hashes match)
- Same LoRA hyperparameters (r=16, alpha=32, dropout=0.05)
- Same training epochs (3)
- Dev set not used for hyperparameter tuning

### C2: Targeted Data Scaling
> "BF16 r16 1000, which adds 500 targeted-balanced examples spanning 8 new business domains to the 500-control baseline, achieves [better/similar/worse] dev set performance compared to BF16 r16 500."

**Requirements:**
- Acknowledge the confound: 1000 has more data AND broader domains
- Do NOT claim pure data-volume causality

### C3: Structural Quality
> "The v05g repaired training data passes all 9 structural quality gates with 0 leakage against protected datasets."

### C4: Semantic Improvements
> "Post-repair, READ labels are semantically recoverable (0 stale reads, 0 distractor reads), opener diversity is increased (90.9% prefix accuracy vs 100%), and sensitive literals are diversified (70 unique vs 18)."

## CONDITIONAL Claims (Require Specific Evidence)

### CC1: Router Beats Naive Baselines
> "BF16 LoRA r16 router beats rule-based and all-read baselines on dev set."

**Only if:** BF16 variants exceed baseline metrics on dev set evaluation.

### CC2: Router Approaches QLoRA Performance at Lower Cost
> "BF16 LoRA r16 retains QLoRA r16 performance while enabling potential future deployment optimizations."

**Only if:** BF16 performance matches or exceeds QLoRA. LoRA adapter size is the same regardless of quantization, so cost is not directly affected. Training cost comparison may be relevant.

## FORBIDDEN Claims (Do NOT Make)

| ❌ Claim | Why Forbidden |
|----------|--------------|
| "1000 examples are better than 500" | Confound: more data + different domains |
| "The router learns semantic relevance" | READ = entity matching, not semantic reasoning |
| "The router generalizes to real-world memory policy" | Template-generated synthetic data; no deployment test |
| "BF16 LoRA is superior to QLoRA" | Single experiment; no significance testing |
| "v05g data is production-quality" | No human review of additional 500 |
| "The router beats DeepSeek V4 Flash/Pro/Max" | Not tested; no comparison planned |
| "Results are statistically significant" | Single training run per variant |
| "Downstream utility is proven" | No downstream ablation run |

## Dev Evaluation Boundaries

| Allowed | Forbidden |
|---------|-----------|
| Dev set (v05b dev 100) evaluation | gold_v2_009 evaluation (save for final) |
| Parse, exact, F1 metrics | Claims about gold performance |
| Descriptive comparison of variants | Hyperparameter tuning on dev |
| Documenting limitations | Hiding weaknesses |

## Gold_v2_009 Usage Rule

gold_v2_009 is reserved for **one final evaluation** of the **single selected best candidate** after all dev-set comparisons are complete. Do not use gold_v2_009 for:
- Model selection
- Hyperparameter tuning
- Iterative improvement
- Early stopping
- Confidence estimation

## Interpretation Guardrails

1. **Dev set is small (100 examples).** Observed differences may not be robust. Report effect sizes and note small-sample caveats.

2. **Single training run per variant.** Do not claim statistical significance. "BF16 r16 500 scored X on dev" is descriptive, not inferential.

3. **Template-generated data limits generalization.** Real-world memory policy tasks may differ from synthetic patterns. The experiment tests the LoRA scaling hypothesis, not deployment readiness.

4. **No comparison to DeepSeek models.** This experiment studies LoRA training methodology, not model capability ceilings.

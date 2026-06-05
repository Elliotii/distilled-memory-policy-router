# V0.5e Next-Step Decision Memo

**Date:** 2026-06-04  

## Current State

v0.5e gold_v2 evaluation complete. r16 directionally promising but not significantly better than r8 on primary metric.

## Options

### A. Package v0.5e and pause ✅ Recommended
Snapshot current project state. Build v1.0 roadmap. 
- **Effort:** Low
- **Benefit:** Clean closure, portfolio-ready

### B. Parse stabilization for r16
Apply output-constrained decoding or JSON repair.
- **Expected:** r16 parse 94.7% → 98%+
- **Effort:** Low-Medium

### C. Standard BF16 LoRA
Remove 4-bit quantization.
- **Expected:** +2-5pp exact
- **Risk:** VRAM may not fit

### D. r32 QLoRA
Double rank again.
- **Expected:** Marginal gain over r16
- **Risk:** Diminishing returns

### E. Targeted data scaling
Add more training cases.
- **Effort:** High

### F. v1.0 downstream benchmark
Build end-to-end agent benchmark.
- **Effort:** High
- **Benefit:** Real-world validation

## Recommendation

1. **Package v0.5e** — snapshot and tag
2. **Option B (parse stabilization)** — quick win before packaging
3. **Option F (v1.0 benchmark)** — next major phase

Option D (r32) and E (data scaling) are lower priority given r16's already marginal improvement over r8.

# V0.5d Next-Step Decision Memo

**Date:** 2026-06-04  

---

## Current State

- r=8: best gold-verified (41% exact, 0.969 STORE F1)
- r=16: best dev performer (39% exact dev, +5pp over r=8 dev)
- Gap to close: r=16 needs gold verification

## Option 1: Create gold_v2 → Evaluate r=16 vs r=8 ✅ RECOMMENDED

| Aspect | Detail |
|--------|--------|
| Effort | Medium (100 new gold cases + evaluations) |
| Benefit | Clean final claim for r=16 |
| Risk | gold_v2 cases may differ in difficulty → not directly comparable to old gold |

**Why recommended:** r=16 +5pp exact on dev is the strongest dev signal in this study. It deserves clean gold verification. Projected gold (44-48%) could make r=16 the first trained system to beat Qwen3.5 few-shot (42%).

**What to evaluate on gold_v2:**
- Qwen3.5 r=16 500
- Qwen3.5 r=8 500 (re-baseline)
- Qwen3.5 JSON few-shot (re-baseline)

## Option 2: Stop Experimentation and Package

| Aspect | Detail |
|--------|--------|
| Effort | Low |
| Benefit | Clean project closure |
| Risk | Leave the r=16 signal unverified |

Package current state: r=8 is best gold-verified, r=16 is promising dev-only. This is a valid stopping point.

## Option 3: Standard LoRA / BF16 LoRA

| Aspect | Detail |
|--------|--------|
| Effort | Medium-High (VRAM-constrained) |
| Benefit | Could provide another +3-5pp exact |
| Risk | 12GB VRAM may not fit BF16 4B model |

Consider only if r=16 gold_v2 underperforms expectations OR if user wants maximum accuracy regardless of training cost.

## Option 4: Targeted Data Scaling

| Aspect | Detail |
|--------|--------|
| Effort | High (new data construction) |
| Benefit | Could fix target accuracy and safety bottlenecks |
| Risk | Data construction is labor-intensive |

Consider after r=16 gold_v2 if target accuracy (73.7%) or safety (5 PII failures) remain primary concerns.

## Recommendation

**Option 1: gold_v2 first.** r=16's +5pp dev exact is too strong to leave unverified. If gold_v2 confirms r=16 > r=8, the project has a clear "winner." If gold_v2 shows regression, r=8 remains the best and the project is still complete.

---

*End of Next-Step Memo.*

# gold_v2_002 Label Consistency Audit

**Date:** 2026-06-04  

## Method

Checked all 343 unit instances across 150 active cases for:
1. Identical unit texts with different gold labels
2. Near-identical unit texts with contradictory labels
3. Normalized skeleton overlap with label mismatch

## Results

| Check | Result |
|-------|:------:|
| Identical texts, different labels | ✅ 0 |
| Near-identical, contradictory labels | ✅ 0 |
| Skeleton overlap, label mismatch | ✅ 0 (all skeletons unique per case context) |

## Note

Each unit text is uniquely generated per case. No shared template instances. The 67.1% uniqueness rate means 230/343 units are distinct strings. The remaining ~113 units share text across cases BUT those are:
- Same domain + same target combinations (e.g., two cases in the same domain both storing a service_memory fact about the same service)
- These are NOT contradictory labels — they have the same target in both cases

## Verdict: PASS ✅

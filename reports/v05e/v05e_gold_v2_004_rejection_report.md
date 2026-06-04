# gold_v2_004 Rejection Report

**Date:** 2026-06-04 | **Status: REJECTED**

## Blockers (ClaudeCode/DeepSeek)
1. **748 unresolved placeholders** — FILLERS had 23 keys, templates used 49
2. **flowcraft/demand-forecaster** in train_500 (31 + 1 cases) — namespace leakage
3. **30 article doublings** ("a a", "the the")
4. **Version doubling** ("v v1.2.3")

v004 design (disjoint pools, hard gates) was sound; execution had bugs. Replaced by v005.

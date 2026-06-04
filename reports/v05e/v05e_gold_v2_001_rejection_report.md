# gold_v2_001 Rejection Report

**Date:** 2026-06-04  

## Status: REJECTED

Two independent reviews found critical issues. v001 will not be used for evaluation.

## Issues Found

### 1. Domain Leakage (DeepSeek/ClaudeCode)
- `ecommerce-platform`, `shopengine`, `cart-service` overlap with train_500
- `learnhub`, `alert-manager` also overlap
- **Severity: BLOCKER** — would invalidate gold independence

### 2. Sensitive Count Over Protocol (DeepSeek/ClaudeCode)
- 30 sensitive cases vs protocol max 27
- **Severity: Must fix**

### 3. Boundary Count Over Protocol (DeepSeek/ClaudeCode)
- 45 boundary cases vs protocol max 38
- **Severity: Must fix**

### 4. Template Diversity Crisis (Both reviews)
- Only 38.6% unit texts unique
- Mass SLA / root-cause / connection-pool templates
- **Severity: BLOCKER** — unfair to r=16 vs r=8 comparison

### 5. READ Positional Artifacts (Opus)
- READ labels based on candidate position, not semantic relevance
- **Severity: BLOCKER**

### 6. Contradictory Labels (Opus)
- Identical/near-identical inputs with different gold labels
- **Severity: BLOCKER**

## Disposition
v001 active and holdout files preserved for audit at `data/v05e/gold_v2/v05e_gold_v2_*` (original v001 filenames). Replaced by v002.

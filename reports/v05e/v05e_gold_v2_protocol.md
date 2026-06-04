# V0.5e gold_v2 Protocol

**Date:** 2026-06-04  
**Status:** Pre-registration — no data generated  

---

## Purpose

Provide a clean, blind gold set for final validation of the r=16 vs r=8 QLoRA comparison and re-baselining of Qwen3.5 JSON few-shot.

**Why gold_v2 is needed:**
- Old gold has been evaluated 3 times (v0.5 DSL, v0.5b JSON, v0.5c r=8)
- Third-party Opus 4.8 Thinking review recommended fresh gold for r=16 claims
- n=100 is too small for 1-5pp claims; gold_v2 should be larger

## Scope

- **Active set:** 150 cases
- **Optional holdout:** 30 additional cases (180 total), reserved untouched for future use
- **Construction:** Independent generation, same methodology as old gold
- **Domains:** 6+ new project domains not overlapping old gold domains
- **Labels:** LLM-assisted + targeted human review
- **Lock:** Cases and labels frozen before any model evaluation

## Construction Constraints

1. **Independent from all existing data:** train_500, dev, old gold, few-shot exemplars
2. **No case-ID overlap** with any existing dataset
3. **New project domains** — avoid the 6 old-gold domains (finance-dashboard, health-monitor, shipping-logistics, ci-pipeline, content-platform, compliance-audit)
4. **English only** — consistent with existing datasets
5. **0-8 candidate memories, 0-4 recent context turns** — same as existing schema
6. **All read_hints must reference valid candidate memory IDs**
7. **All write_spans must be exact substrings of current_user_input**
8. **All ignore_spans must be exact substrings of current_user_input**

## Shape Distribution (150 cases)

| Shape | Target | Rationale |
|-------|:------:|-----------|
| READ-only | ~27 (18%) | Old gold had 23 (23%) |
| STORE/SKIP-only | ~58 (39%) | Old gold had 42 (42%) |
| READ + STORE joint | ~65 (43%) | Old gold had 35 (35%) |

Slightly more READ+STORE joint than old gold to increase unit density and provide more target-classification signal.

## Target Distribution (STORE units)

| Target | Target % | Rationale |
|--------|:--------:|-----------|
| task_state | ~33% | Match old gold (33.8%) |
| service_memory | ~32% | Match old gold (38.1%) — slightly lower |
| repo_memory | ~17% | Match old gold (16.7%) |
| project_memory | ~12% | Match old gold (7.1%) — slightly higher |
| user_profile | ~6% | Match old gold (4.3%) — slightly higher |

Post-generation distribution tuning allowed within ±3pp of targets. Exact matching not required.

## Stress Axes (overlapping with shapes/targets)

| Axis | Count | Focus |
|------|:-----:|-------|
| Sensitive/private SKIP | 18-27 | Phone, email, address, credential/token/key, payment/card, ID |
| Hard target-boundary | 30-38 | svc↔task, repo↔svc, proj↔svc, user↔sensitive |

## Optional Holdout (30 cases)

If generated, these 30 cases are:
- Same distribution as active 150
- NEVER evaluated during r=16/r=8 comparison
- Reserved for future use (standard LoRA, r=32, etc.)
- Locked with the active set

---

*End of Protocol.*

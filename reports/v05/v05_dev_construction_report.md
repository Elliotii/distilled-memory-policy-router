# V0.5 Dev Set Construction Report

**Date:** 2026-06-02  
**Context:** 5.3-B — Independent Dev Set Construction  
**Status:** Complete  

---

## 1. Scope

This context generated the v0.5 **independent development set** — 100 cases for checkpoint selection, LoRA hyperparameter choice, prompt/training-setting comparison, and early error analysis.

The dev set is **NOT** for final project claims. Gold will be constructed separately.

## 2. Generation Method

### 2.1 Independence from Train Pool

Dev cases were **independently composed**, not mechanically split or copied from corrected batch500. Key independence measures:

| Measure | Implementation |
|---------|---------------|
| Different project domains | Used telemetry-dashboard, payment-gateway, inventory-system, chat-platform, analytics-engine, identity-service — none overlap with train pool domains (memory-router, mobile-field, data-platform) |
| Different repo/service names | All repositories and services have unique names distinct from train pool |
| Different scenarios | Each case describes a scenario not present in corrected batch500 |
| Separate construction pass | Cases composed in a single independent session, not derived from train data |
| Leakage-verified | Leakage checker confirms zero hard blockers (0 exact case_id, 0 exact unit, 0 exact memory overlap) |

### 2.2 Why Dev Is Not Final Gold

| Property | Dev | Gold (planned) |
|----------|-----|----------------|
| Review level | Automated + spot-check | Full human adjudication |
| Purpose | Model selection, hyperparameter tuning | Final claims, resume metrics |
| Label provenance | Single-pass composition with label-policy adherence | Multi-pass human adjudication |
| Hard cases | Moderate coverage | 30 dedicated gold_hard cases |
| Locked | No | Yes (after adjudication) |

## 3. Files Created

| File | Path | Rows |
|------|------|:----:|
| Dev cases | `data/v05/dev/v05_dev_cases.jsonl` | 100 |
| Dev SFT messages | `data/v05/dev/v05_dev_sft_messages.jsonl` | 100 |
| Dev construction report | `reports/v05/v05_dev_construction_report.md` | This file |
| Dev data report | `reports/v05/v05_dev_data_report.md` | Created |
| Dev leakage report | `reports/v05/v05_dev_leakage_report.md` | Created |
| Dev semantic audit | `reports/v05/v05_dev_semantic_audit.md` | Created |
| Dev SFT validation report | `reports/v05/v05_dev_sft_validation_report.md` | Created |
| Generation script | `src/v05/render_dev.py` | Created |
| Updated | `docs/status/CURRENT_STATE.md` | Updated |

## 4. Key Distributions

### 4.1 Target Distribution (STORE units, n=220)

| Target | Count | % | Target Range |
|--------|:-----:|:--:|:------------:|
| service_memory | 71 | 32.3% | 28–34% ✅ |
| task_state | 74 | 33.6% | 28–34% ✅ |
| repo_memory | 37 | 16.8% | 16–20% ✅ |
| project_memory | 26 | 11.8% | 10–14% ✅ |
| user_profile | 12 | 5.5% | 5–8% ✅ |

### 4.2 Shape Distribution

| Shape | Cases | % | Target Range |
|-------|:-----:|:--:|:------------:|
| READ+STORE joint | 43 | 43.0% | 40–45% ✅ |
| STORE/SKIP-only | 39 | 39.0% | 35–40% ✅ |
| READ-only | 18 | 18.0% | 18–22% ✅ |

### 4.3 Coverage Requirements (all 12 covered)

| Coverage Area | Tag | Cases |
|---------------|-----|:-----:|
| service_vs_task_state | ✓ | 3 |
| project_memory_vs_task_state | ✓ | 1 |
| repo_vs_service | ✓ | 6 |
| user_profile_vs_sensitive_private | ✓ | 1 |
| sensitive_boundary | ✓ | 10 |
| stale_memory | ✓ | 16 |
| related_but_useless | ✓ | 15 |
| temporary_request | ✓ | 31 |
| repo_convention | ✓ | 29 |
| service_invariant | ✓ | 67 |
| task_progress | ✓ | 63 |
| read_selectivity | ✓ | 19 |

## 5. Validation Summary

| Check | Status |
|-------|:------:|
| 100 cases exactly | ✅ |
| 100 SFT messages exactly | ✅ |
| validate_jsonl_file | ✅ |
| All DSLs parse | ✅ |
| Canonical == structured gold | ✅ |
| Every unit exactly once STORE or SKIP | ✅ |
| No invalid READ IDs | ✅ |
| No invalid STORE IDs/targets | ✅ |
| Zero real sensitive STORE | ✅ |
| SFT assistant == gold.dsl | ✅ |
| No markdown/JSON in assistant | ✅ |
| Leakage: 0 hard blockers | ✅ |
| Unittest: 77/77 OK | ✅ |

## 6. Leakage Summary

| Category | Count |
|----------|:-----:|
| Hard blockers | 0 |
| Review-level warnings | 0 |
| General warnings | 1 |

The single warning (near-duplicate memory, score 0.500) is a natural domain overlap: both train and dev describe token-issuer behavior with "15-minute expiry". This is acceptable — same domain vocabulary, different cases.

## 7. Recommendation

The dev set is ready for:
1. Checkpoint selection during Qwen3-4B LoRA training
2. LoRA hyperparameter comparison (rank, alpha, learning rate)
3. System prompt variant comparison
4. Early error analysis during training

Dev metrics must NOT be reported as final claims. Gold (to be constructed in 5.3-C) is the sole evaluation standard for final metrics.

## 8. Open Issues

- Gold set not yet constructed
- No training conducted
- render_dev.py needs regeneration to match final patched JSONL (cosmetic — the JSONL is canonical)

---

*End of V0.5 Dev Construction Report.*

# V0.5 Gold Lock Report

**Date:** 2026-06-02  
**Context:** 5.3-E — locked v0.5 corrected gold set  
**Status:** **LOCKED** — gold is immutable for final evaluation  

---

## 1. Scope

This report documents the locking of the v0.5 corrected gold evaluation set. The gold set contains 100 independently constructed coding-agent memory policy router cases (70 gold_core + 30 gold_hard). It was reviewed by Opus 4.8 Thinking (advisory), corrected across two contexts (5.3-D and 5.3-D2), and is now locked for final evaluation only.

## 2. What Was Locked

| File | SHA-256 |
|------|---------|
| `data/v05/gold/v05_gold_corrected_cases.jsonl` | `56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d` |
| `data/v05/gold/v05_gold_core_corrected_cases.jsonl` | `9acdd6a795b0a18d5c369253be8bb64e26a9af96e2aea31b4ef6c98adb598db2` |
| `data/v05/gold/v05_gold_hard_corrected_cases.jsonl` | `5f4a5d552f76033c6a9a5443581a2dc2dc7ea0eeabdf99481fc1ec2c49f819b2` |
| `data/v05/gold/v05_gold_corrected_sft_messages.jsonl` | `d9f215af282d6c90b65612c575d9a5827520a953d47f807e586b79ec94635c22` |

## 3. Why Gold Is Now Lock-Ready

Gold has gone through a rigorous review and correction pipeline:

| Stage | Context | Description |
|-------|---------|-------------|
| Generation | 5.3-B | 100 independently composed cases from 6 project domains |
| Advisory Review | 5.3-C2 | Opus 4.8 Thinking review found 6 blockers |
| Fixes Applied | 5.3-D | All 6 blockers addressed (12 fix groups, 5 borderline reviewed) |
| Metadata Cleanup | 5.3-D2 | 24 notes regenerated, 10 service wordings rewritten |
| Lock | 5.3-E | Validated, verified, locked |

All Opus-advisory concerns have been resolved. No further advisory review is needed.

## 4. Hash Verification Table

| File | Expected SHA-256 | Actual SHA-256 | Match |
|------|------------------|----------------|:-----:|
| Combined | `56e16078...2173d` | `56e16078...2173d` | ✅ |
| Core | `9acdd6a7...8db2` | `9acdd6a7...8db2` | ✅ |
| Hard | `5f4a5d55...19b2` | `5f4a5d55...19b2` | ✅ |
| SFT | `d9f215af...5c22` | `d9f215af...5c22` | ✅ |

## 5. Validation Summary

| Check | Result |
|-------|:------:|
| 100 cases (70 core + 30 hard) | ✅ |
| validate_jsonl_file | ✅ pass |
| DSL parse | ✅ 100/100 |
| Canonical consistency | ✅ 100/100 |
| Unit coverage (exactly once STORE/SKIP) | ✅ pass |
| Sensitive STORE | ✅ 0 |
| SFT assistant matches gold.dsl | ✅ 100/100 |
| Train↔gold leakage (hard blockers) | ✅ 0 |
| Train↔gold leakage (warnings) | ✅ 0 |
| Dev↔gold leakage (hard blockers) | ✅ 0 |
| Dev↔gold leakage (warnings) | ✅ 0 |
| Unit tests | ✅ 77/77 |

## 6. Leakage Summary

| Check | Hard Blockers | Warnings |
|-------|:------------:|:--------:|
| Train (batch500) ↔ Gold | 0 | 0 |
| Dev ↔ Gold | 0 | 0 |

Gold is fully independent of both train-pool and dev. No exact text overlap, no near-duplicates, no scenario collisions, no normalized overlaps.

## 7. Advisory Review History

| Review | Reviewer | Context | Findings | Status |
|--------|----------|---------|----------|:------:|
| Initial | Opus 4.8 Thinking | 5.3-C2 | 6 blockers found | All addressed in 5.3-D |
| Lightweight final | Opus 4.8 Thinking | 5.3-D2 | 2 metadata issues | All addressed in 5.3-D2 |
| Final verdict | Opus 4.8 Thinking | 5.3-D2 | Scoring content lock-ready | Locked in 5.3-E |

## 8. Distribution Tradeoffs

| Target | Actual % | Planned Range | Notes |
|--------|:--------:|:-------------:|-------|
| service_memory | 38.1% | 28-34% | Above target — honest consequence of removing artificial project_memory labels |
| task_state | 33.8% | 28-34% | Within target |
| repo_memory | 16.7% | 16-22% | Within target |
| project_memory | 7.1% | 10-16% | Below target — artificial labels removed. Remaining 15 are genuine cross-service/project-level |
| user_profile | 4.3% | 5-10% | Below target — false user_profile removed. 9 remaining are genuine |

**These tradeoffs are honest and documented.** No weak labels were added to hit distribution targets.

## 9. Usage Rules

Gold is for **final evaluation only**:

- ✅ Final model comparison against baselines
- ✅ Final report claims
- ✅ DeepSeek teacher reference evaluation
- ❌ Training (LoRA/SFT)
- ❌ Prompt tuning or system prompt design
- ❌ Hyperparameter tuning
- ❌ Checkpoint selection (use dev)
- ❌ Few-shot examples
- ❌ Data generation feedback
- ❌ Any development or iteration

## 10. Immutability Rules

1. Locked gold files must not be edited.
2. Any future correction requires a new lock version (e.g., `v05_gold_002`) with explicit changelog.
3. If critical error discovered post-lock: document, assess impact, unlock with changelog, fix, re-lock.
4. If non-critical error discovered: note in error analysis, do NOT change gold.

## 11. What Gold Must Not Be Used For

| Prohibited Use | Rationale |
|----------------|-----------|
| Training | Would inflate eval scores (train-test leakage) |
| Checkpoint selection | Use dev — gold is final holdout |
| Hyperparameter tuning | Would inflate gold scores |
| Prompt design | System prompt must not memorize gold |
| Few-shot examples | Few-shot must be train-sourced only |
| Data generation feedback | Indirect leakage through iteration |
| Any development iteration | Gold is opened only for final evaluation |

## 12. Next Steps

**Context 5.4-A: Qwen3 / Qwen3.5 baseline readiness and model comparison planning**

1. Evaluate Qwen3-4B and Qwen3.5 baselines on dev (zero-shot, few-shot DSL, JSON)
2. Select best-performing configuration on dev
3. Run final selected baselines on locked gold
4. Train LoRA/SFT routers (125/250/500 cases from train-pool)
5. Evaluate final checkpoint on locked gold
6. Report all results against locked gold as ground truth

---

*End of V0.5 Gold Lock Report.*

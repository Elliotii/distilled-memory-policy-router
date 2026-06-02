# V0.5 Gold Draft Construction Report

**Date:** 2026-06-02  
**Context:** 5.3-C + 5.3-C2  
**Status:** Draft complete — ready for review  

---

## 1. Scope

This report documents the construction of the v0.5 gold draft — 100 evaluation cases (70 gold_core + 30 gold_hard) for final model evaluation after human adjudication and locking.

## 2. Generation Method

Gold cases were **independently composed** using six new project domains not present in the train-pool or dev set:

| Domain | Cases |
|--------|:-----:|
| ci-pipeline | 19 |
| content-platform | 19 |
| financial-reporting | 17 |
| health-monitor | 16 |
| shipping-logistics | 15 |
| compliance-audit | 14 |

Gold was NOT mechanically split from corrected batch500 or dev set. All cases use distinct scenarios, text, memories, and labels.

Post-generation, 25 target adjustments were applied to bring the distribution within specified ranges (documented in `v05_gold_postprocessing_adjustment_log.md`).

## 3. Why Draft, Not Locked

| Property | Status |
|----------|:------:|
| Human-adjudicated | No — pending |
| Second-reviewer checked | No — pending |
| LLM advisory review | Not yet conducted |
| Lock file created | No |
| Ready for evaluation | No — locked gold is the evaluation standard |

## 4. Files Created

| File | Description |
|------|-------------|
| `data/v05/gold/v05_gold_draft_cases.jsonl` | 100-case combined gold draft |
| `data/v05/gold/v05_gold_draft_sft_messages.jsonl` | 100 SFT messages |
| `data/v05/gold/v05_gold_core_draft_cases.jsonl` | 70 gold_core cases |
| `data/v05/gold/v05_gold_hard_draft_cases.jsonl` | 30 gold_hard cases |
| `src/v05/render_gold_draft.py` | Frozen-data writer (loads from canonical JSONL) |

## 5. Core / Hard Structure

| Partition | Cases | Purpose |
|-----------|:-----:|---------|
| gold_core | 70 | Representative natural-distribution routing |
| gold_hard | 30 | Boundary stress testing across 8 categories |

## 6. Validation Summary

All structural, DSL, canonical, and SFT validations pass. Zero sensitive STORE errors. 77/77 unit tests pass.

## 7. Leakage Summary

| Check | Hard Blockers | Warnings |
|-------|:------------:|:--------:|
| Train↔Gold | 0 | 1 (score 0.533, accepted) |
| Dev↔Gold | 0 | 0 |

## 8. Known Limitations

- 25 post-processing adjustments — labels may need refinement during adjudication
- 2 text errors in adjustment pass (fixed in 5.3-C2)
- user_profile at 4.7% (slightly below 5-8% target — acceptable for gold)
- No second-human review yet
- Gold hard cases were independently composed but not manually curated

## 9. Recommendation

The gold draft is ready for external LLM-based advisory review (Opus/ClaudeCode). After review feedback and human adjudication, the gold set can be locked and used for final evaluation.

---

*End of V0.5 Gold Draft Construction Report.*

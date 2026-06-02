# V0.5 Locked Gold Usage Check

**Date:** 2026-06-02  
**Context:** 5.4-A — verification that locked gold is intact and usage rules are enforced  

---

## 1. Lock Manifest Summary

| Property | Value |
|----------|-------|
| Lock status | ✅ locked |
| Lock version | v05_gold_001 |
| Locked at | 2026-06-02T08:33:15Z |
| Adjudicator | project-owner |
| Second reviewer | none (single-human + LLM advisory) |

## 2. Hash Verification

| File | Lock Hash | Current Hash | Match |
|------|-----------|-------------|:-----:|
| `v05_gold_corrected_cases.jsonl` | `56e16078...2173d` | `56e16078...2173d` | ✅ |
| `v05_gold_core_corrected_cases.jsonl` | `9acdd6a7...8db2` | `9acdd6a7...8db2` | ✅ |
| `v05_gold_hard_corrected_cases.jsonl` | `5f4a5d55...19b2` | `5f4a5d55...19b2` | ✅ |
| `v05_gold_corrected_sft_messages.jsonl` | `d9f215af...5c22` | `d9f215af...5c22` | ✅ |

**All 4 locked gold files verified — no modification since lock.**

## 3. Usage Rules

### Allowed Uses

| Use | When |
|-----|------|
| Final evaluation of baselines | Phase 3 (after all dev selection complete) |
| Final evaluation of LoRA checkpoint | Phase 5 (after training complete) |
| Final report claims | Always |
| Per-target breakdown reporting | Always |

### Forbidden Uses

| Use | Reason |
|-----|--------|
| Training | Would inflate eval scores |
| Prompt tuning | Prompt must not memorize gold |
| Hyperparameter tuning | Use dev |
| Checkpoint selection | Use dev |
| Few-shot examples | Must be train-sourced only |
| System prompt design | Must not contain gold-derived content |
| Data generation feedback | Indirect leakage |
| Any development iteration | Gold is final holdout only |

## 4. Confirmed No Modification

The following checks confirm gold immutability:

| Check | Status |
|-------|:------:|
| SHA-256 matches lock manifest | ✅ 4/4 |
| File sizes consistent | ✅ |
| Line counts (100, 70, 30, 100) | ✅ |
| Lock manifest validates | ✅ |

## 5. Risks

| Risk | Status |
|------|:------:|
| Accidental gold modification | Mitigated — hash verification before use |
| Gold used for prompt design | Mitigated — documented rules, separate prompt files |
| Gold used for checkpoint selection | Mitigated — dev is the only checkpoint selector |
| Gold few-shot examples | Mitigated — few-shot sourced from train-pool only |
| Gold opened during training | Mitigated — process separation: train → dev → gold |

## 6. Enforcement

Before any gold evaluation:

1. Verify SHA-256 hashes against `v05_gold_lock.json`
2. Confirm no prior gold access in current development phase
3. Log the evaluation run in prediction metadata
4. Report lock version (`v05_gold_001`) in all gold-based evaluation reports

## 7. Violation Response

If gold is accidentally modified or used for development:
- Document the incident
- Assess whether gold is still a valid holdout
- If invalidated: gold must be re-locked with new version
- If still valid: document the edge case and reinforce process

---

*End of V0.5 Locked Gold Usage Check.*

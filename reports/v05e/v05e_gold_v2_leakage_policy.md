# V0.5e gold_v2 Leakage Policy

**Date:** 2026-06-04  

---

## Source Corpora to Check

gold_v2 must be checked for leakage against:

1. **train_500** (`data/v05/train/subsets/v05_train_500_cases.jsonl`)
2. **dev** (`data/v05/dev/v05_dev_cases.jsonl`)
3. **old gold** (`data/v05/gold/v05_gold_corrected_cases.jsonl`)
4. **Few-shot exemplars** — the 5 cases used in few-shot prompts (v05_sample_0001, 0005, 0009, 0010, 0004)
5. **Domain/surface patterns** — project names, repo names, service names, phone patterns, email patterns, token patterns from any existing dataset

## Hard Blockers (exit nonzero)

| Level | Check | Action |
|:-----:|-------|--------|
| L0 | Duplicate case_id with any existing dataset | **Reject** |
| L1 | Exact unit text overlap with any existing dataset | **Reject** |
| L1 | Exact memory text overlap with any existing dataset | **Reject** |
| L2 | Normalized near-duplicate (Jaccard ≥ 0.9 on token set) | **Reject** |

## Review Flags (warn, human review)

| Level | Check | Action |
|:-----:|-------|--------|
| L3 | Same scenario with changed names (e.g., "order-service" → "purchase-service" with identical unit structure) | **Review** |
| L3 | Same boundary trick as old gold with shallow paraphrase | **Review** |
| L3b | Same sensitive string pattern (e.g., repeated phone format with different digits) | **Review** |
| L3b | Few-shot exemplar domain reuse (same project/service names) | **Review** |
| L5 | Candidate-internal memory repeats within gold_v2 | **Warn** |

## Cross-Dataset Phone/Email/Token Patterns

Phone numbers, email addresses, and token patterns must be unique across all datasets. No pattern reuse even with different values.

## Domain Separation

gold_v2 project domains must not overlap old gold domains:
- Old gold domains: finance-dashboard, health-monitor, shipping-logistics, ci-pipeline, content-platform, compliance-audit
- gold_v2 must use 6+ new domains

## Leakage Check Tool

Use existing `src/v05/check_leakage.py` if compatible, or extend as needed. Output a leakage report as part of gold_v2 construction.

## Model Blindness

- gold_v2 may be error-informed at the **taxonomy** level (include known-hard categories)
- gold_v2 must be model-blind at the **instance** level (no targeting of r=16-specific outputs)
- It is acceptable to include service/task boundary cases and PII cases because these are known-hard categories, not because any model failed on them

---

*End of Leakage Policy.*

# gold_v2_009 Independent Review — DeepSeek

**Date:** 2026-06-05
**Reviewer:** DeepSeek (automated audit)
**Status:** Independent review only — no data modified, no models run

---

## Verdict

**APPROVE**

The v008 phantom sensitive issue is fully resolved: 21 case-level `sensitive_boundary` tags, 21 unit-level sensitive units, 0 phantom cases. All 32 checks pass including all preserved v008 gates. This dataset is ready for evaluation.

---

## Checks Run

| # | Check | v008 | v009 |
|---|-------|:----:|:----:|
| 1 | Active = 150, Holdout = 30 | ✅ | ✅ |
| 2 | Active/holdout separation | ✅ | ✅ |
| 3 | Hash integrity (4/4) | ✅ | ✅ |
| 4 | Old gold hash unchanged | ✅ | ✅ |
| 5 | `build_gold_v2_009.py` exists | ❌ | ✅ |
| 6 | Schema errors | ✅ 0 | ✅ 0 |
| 7 | Target legality | ✅ 0 | ✅ 0 |
| 8 | Unit coverage | ✅ 0 | ✅ 0 |
| 9 | SFT JSON parse | ✅ 100% | ✅ 100% |
| 10 | SFT markdown | ✅ 0 | ✅ 0 |
| 11 | Memory key (`text`) | ✅ | ✅ |
| 12 | **Phantom sensitive cases** | ❌ 6 | ✅ **0** |
| 13 | Every `sensitive_boundary` case has unit | ❌ 6 missing | ✅ **21/21** |
| 14 | All sensitive units SKIP | ✅ | ✅ |
| 15 | Sensitive STORE | ✅ 0 | ✅ 0 |
| 16 | Real sensitive 18-27 | ✅ 21 | ✅ **21** |
| 17 | `vocab_item` literal | ✅ 0 | ✅ 0 |
| 18 | Unresolved brace placeholders | ✅ 0 | ✅ 0 |
| 19 | Article doubling | ✅ 0 | ✅ 0 |
| 20 | Version doubling | ✅ 0 | ✅ 0 |
| 21 | Filler verb bugs | ✅ 0 | ✅ 0 |
| 22 | "the entire the" | ✅ 0 | ✅ 0 |
| 23 | "used to accepted/logged/required/ran" | ✅ 0 | ✅ 0 |
| 24 | Plural subject + "is published" | ✅ 0 | ✅ 0 |
| 25 | "implement ransomware/zero-day/Sharpe" | ✅ 0 | ✅ 0 |
| 26 | Banned entity overlap | ✅ 0 | ✅ 0 |
| 27 | Name overlap: train_500/dev/old gold | ✅ 0 | ✅ 0 |
| 28 | Exact-text label conflicts | ✅ 0 | ✅ 0 |
| 29 | SKIP-vs-STORE skeleton conflicts | ✅ 0 | ✅ 0 |
| 30 | Multi-target STORE skeleton conflicts | ✅ 0 | ✅ 0 |
| 31 | READ label conflicts | ✅ 0 | ✅ 0 |
| 32 | READ skeleton conflicts | ✅ 0 | ✅ 0 |
| 33 | Stale memories READ | ✅ 0 | ✅ 0 |
| 34 | Class rule READ rate | ✅ 100% | ✅ 100% |
| 35 | Boundary 30-38 | ✅ 34 | ✅ 34 |
| 36 | Boundary on READ-only | ✅ 0 | ✅ 0 |
| 37 | task_state ≤36% | ✅ 33.9% | ✅ 33.9% |
| 38 | service_memory 29-35% | ✅ 31.4% | ✅ 31.4% |
| 39 | repo_memory 14-20% | ✅ 15.7% | ✅ 15.7% |
| 40 | project_memory 9-15% | ✅ 13.2% | ✅ 13.2% |
| 41 | user_profile 3-9% | ✅ 5.8% | ✅ 5.8% |
| 42 | Unit uniqueness | ✅ 90.5% | ✅ 90.5% |
| 43 | Fleet vocabulary contamination | ✅ <0.5% | ✅ <0.5% |
| 44 | Exact text leakage (all corpora) | ✅ 0 | ✅ 0 |

**Summary: 44/44 PASS**

---

## Protocol Compliance

| Target | Count | % | Protocol | Status |
|--------|:-----:|:--:|:--------:|:------:|
| task_state | 82 | 33.9% | ≤36% | ✅ |
| service_memory | 76 | 31.4% | 29-35% | ✅ |
| repo_memory | 38 | 15.7% | 14-20% | ✅ |
| project_memory | 32 | 13.2% | 9-15% | ✅ |
| user_profile | 14 | 5.8% | 3-9% | ✅ |

Shapes: READ-only=25, STORE/SKIP-only=62, READ+STORE=63.
Stress: Sensitive=21 (18-27 ✅), Boundary=34 (30-38 ✅), BND on RO=0 ✅.

---

## Versioning / Reproducibility Audit

`build_gold_v2_009.py` exists at `src/v05e/build_gold_v2_009.py`. The v008 script was copied and the phantom-sensitive guard was added. Prior version provenance is preserved. v009 is reproducible: seed=234, same domains/FILLERS/targets, with the `sensitive_boundary` tag now guarded on actual sensitive unit presence.

---

## Hash / Lock Audit

| File | SHA-256 (first 16 chars) | Status |
|------|--------------------------|:------:|
| Active cases | `f5cf7be1d06f085e...` | ✅ MATCH |
| Holdout cases | `6bd4de9e091c6d43...` | ✅ MATCH |
| Active SFT messages | `8b30c5c6d41d1bd2...` | ✅ MATCH (same as v008) |
| Holdout SFT messages | `0d7e035801ace816...` | ✅ MATCH (same as v008) |

Lock version: `v05e_gold_v2_009`. Eight prior versions recorded as rejected. Old gold `56e16078...` unchanged. SFT hashes match v008 because only case-level tag metadata changed — unit text and gold labels are identical.

---

## Sensitive Accounting Audit (Primary Hotfix)

| Metric | v008 | v009 | Change |
|--------|:----:|:----:|:------:|
| Case-level `sensitive_boundary` tags | 27 | **21** | −6 |
| Real sensitive cases (unit-level) | 21 | **21** | 0 |
| Phantom cases (tag without unit) | 6 ❌ | **0 ✅** | Fixed |
| Ratio: case tags / real units | 1.29 | **1.00** | Perfect |

**The fix is confirmed.** The `sensitive_boundary` tag is now only applied when the case actually contains a sensitive unit. All 21 tagged cases have verified unit-level sensitive content. All 21 sensitive units are correctly gold-labeled SKIP. Zero sensitive units stored.

### Sensitive Subtypes

| Subtype | Count |
|---------|:-----:|
| Credential (API key, token, DB password, OAuth) | 6 |
| Address (home, shipping) | 4 |
| ID (SSN, employee badge) | 4 |
| Phone | 3 |
| Email | 2 |
| Payment (Amex, debit) | 2 |
| **Total** | **21** |

### Sensitive String Reuse

8 sensitive strings appear in both active cases and SFT messages (expected — SFT messages duplicate case content). Within the active set, sensitive phrases are varied across the 16-entry SENSITIVE_POOL with the `sens_idx` counter ensuring cycling.

---

## Placeholder / String Quality Audit

| Check | Count |
|-------|:-----:|
| `vocab_item` literal (data) | 0 |
| `vocab_item` literal (SFT) | 0 |
| Unresolved brace placeholders | 0 |
| Article doubling | 0 |
| Version doubling | 0 |
| Filler verb bugs | 0 |
| "the entire the" | 0 |
| "used to accepted/logged/required/ran" | 0 |
| Plural + "is published" | 0 |
| "implement ransomware/zero-day/Sharpe" | 0 |
| Generic doubled words | 1 (cosmetic) |

All v008 string quality fixes preserved.

---

## Leakage / Banned Entity Audit

Zero namespace leakage across all corpora. All 24 gold_v2 names absent from train_500, dev, old gold, and few-shot exemplars. All v001-v008 banned names absent. Zero exact text leakage. Zero surface string overlap.

---

## READ / Boundary / Label / Target-Text Audits

All v008 gates preserved identically:
- **READ**: 0 conflicts, 0 stale reads, 100% class rule, deterministic
- **Boundary**: 34 cases (30-38), 0 on READ-only, genuine disambiguation
- **Labels**: 0 exact conflicts, 0 SKIP-vs-STORE skeleton, 0 multi-target STORE
- **Target-text**: Semantically aligned at generation time, no post-hoc swaps

---

## Template / Diversity / Domain Audits

| Metric | v008 | v009 |
|--------|:----:|:----:|
| Unit uniqueness | 90.5% | 90.5% |
| Non-stale mem uniqueness | 93.4% | 93.4% |
| Max unit skeleton repeat | 24 | 24 |
| Fleet vocab contamination | <0.5% | <0.5% |
| Domain-clean units | 400/400 | 400/400 |

Identical to v008 — the sensitive metadata fix did not change any unit or memory text.

---

## Schema / Eval Compatibility

Memory key: `"text"` (compatible with `eval_lora_router.py`). Gold DSL: 180/180 empty (structured-only scoring). SFT: 180/180 valid JSON. FILLERS: 49 keys, verified complete.

---

## Fairness for r=16 vs r=8 Comparison

All fairness dimensions from v008 preserved. The phantom sensitive fix improves metadata accuracy without changing any evaluation-relevant content. The comparison remains fair across all four systems.

---

## Concerns

### 1. COSMETIC: 1 doubled word instance

Single instance, same as v008. Negligible.

### 2. NOTE: 8 sensitive strings appear in multiple contexts

Expected — the same sensitive phrase appears in a case and its corresponding SFT message. Not a data quality issue.

---

## Required Fixes Before Evaluation

**None.**

---

## Final Recommendation

**Proceed to evaluation.**

gold_v2_009 is the first gold_v2 version to pass ALL checks with zero failures of any kind:

- **0** phantom sensitive (fixed from v008)
- **0** vocab_item literal (fixed from v007)
- **0** post-generation relabeling (fixed from v006)
- **0** multi-target skeleton conflicts (fixed from v005)
- **0** unresolved placeholders (fixed from v004)
- **0** namespace leakage (fixed from v003)
- **0** exact label conflicts (fixed from v002)
- **0** template monoculture (fixed from v001)

Every gate passes. Every prior blocker is resolved. Every audit dimension is clean.

This dataset is suitable for the pre-registered four-system evaluation: Qwen3.5 JSON QLoRA r=16, Qwen3.5 JSON QLoRA r=8, Qwen3.5 JSON few-shot, and Qwen3-4B JSON QLoRA r=8.

---

*End of Independent Review.*

# V0.5 Dev Acceptance Report

**Date:** 2026-06-02  
**Context:** 5.3-B2 — reproducibility cleanup and acceptance  
**Status:** Accepted for model-selection use  

---

## 1. Scope

This report finalizes the v0.5 dev set acceptance after reproducibility cleanup. It confirms that the dev set is ready for checkpoint selection, LoRA hyperparameter comparison, prompt/training-setting comparison, and early error analysis. It also documents what the dev set must NOT be used for.

## 2. Dev Set Status

| Property | Value |
|----------|-------|
| File | `data/v05/dev/v05_dev_cases.jsonl` |
| Cases | 100 |
| Case IDs | v05_dev_0001 – v05_dev_0100 |
| SFT messages | `data/v05/dev/v05_dev_sft_messages.jsonl` (100 rows) |
| Construction | Independently composed, post-processed for distribution balance |
| Reproducibility | render_dev.py is now a frozen-data writer (reads canonical, validates, writes SFT) |
| Canonical status | `v05_dev_cases.jsonl` is the canonical source |

## 3. Validation Summary

| Check | Status |
|-------|:------:|
| 100 cases exactly | ✅ |
| 100 SFT messages exactly | ✅ |
| validate_jsonl_file | ✅ |
| All DSLs parse | ✅ |
| Canonical == structured gold | ✅ |
| Every unit exactly once STORE/SKIP | ✅ |
| No invalid READ IDs | ✅ |
| No invalid STORE targets | ✅ |
| Zero real sensitive STORE | ✅ |
| SFT assistant == gold.dsl | ✅ |
| No markdown/JSON in assistant | ✅ |
| SFT source = v05_dev_dry_run | ✅ |
| SFT split = dev | ✅ |
| SFT is_final_train_data = false | ✅ |
| Unittest: 77/77 OK | ✅ |

## 4. Leakage Summary

| Category | Count | Status |
|----------|:-----:|:------:|
| Hard blockers | 0 | ✅ |
| Review-level warnings | 0 | ✅ |
| General warnings | 1 | ⚠ Reviewed, accepted |

### 4.1 Leakage Warning Review

**Warning:** Near-duplicate memory, score 0.500, between:
- Train: `v05_batch500_0133` — "The token-issuer generates access tokens with 15-minute expiry and refresh token..."
- Dev: `v05_dev_0006` — "The token-issuer generates access tokens with 15-minute expiry and refresh tokens with 7-day expiry."

**Assessment:** This is **natural domain overlap**, not actual leakage. Both cases describe token-issuer behavior in authentication services — the shared phrase "15-minute expiry" is standard JWT terminology, not copied text. The two cases have different projects (identity-service vs memory-router), different services, different tasks, and different current_units. Score 0.500 is at the review threshold, not the reject threshold (≥0.800).

**Decision:** Not a blocker. No replacement needed. Both cases independently describe standard auth token behavior using common terminology.

## 5. Medium-Risk Case Summary

| Case | Risk | Target Change | Confidence | Accepted? |
|------|:----:|:------------:|:----------:|:---------:|
| v05_dev_0060 u2 | Medium | service_memory → project_memory | 75% | ✅ Yes |
| v05_dev_0061 u1 | Medium | service_memory → project_memory | 85% | ✅ Yes |

Both cases were post-processed to rebalance the target distribution. The project_memory labels are defensible under `V05_LABEL_POLICY.md`. Full review in `v05_dev_medium_risk_review.md`.

## 6. Reproducibility Cleanup Summary

| Issue | Resolution |
|-------|-----------|
| render_dev.py out of sync with canonical JSONL | Rewritten as frozen-data writer |
| Case notes stale after target changes | Updated 5 case notes to reflect current targets |
| No guard against silent overwrite | --write flag required for cases write; --sft-only for SFT only |
| Hash manifest missing | Created `v05_dev_hash_manifest.md` with SHA-256 |

Full details in `v05_dev_reproducibility_report.md`.

## 7. Dev Acceptance

### 7.1 Dev is ACCEPTED for:

1. **Checkpoint selection** — choosing the best training epoch/step during Qwen3-4B LoRA training
2. **LoRA hyperparameter comparison** — rank, alpha, learning rate
3. **System prompt variant comparison** — testing prompt variations
4. **Early error analysis** — catching overfitting, target collapse, or parse degradation during training
5. **Learning curve analysis** — evaluating 125/250/500 training subset performance

### 7.2 Dev MUST NOT be used for:

1. ❌ Final model comparison claims
2. ❌ Resume or project performance claims
3. ❌ Published results
4. ❌ Claims of "our model achieves X on held-out data"
5. ❌ Gold-level evaluation
6. ❌ Baseline comparison for final reporting (gold is the standard)

Dev metrics are **development diagnostics only**.

### 7.3 Acceptance Conditions

The following conditions must be met before using dev:

| Condition | Status |
|-----------|:------:|
| Gold constructed and locked | Not yet (5.3-C) |
| Leakage checks: train↔dev clean | ✅ 0 hard blockers |
| Dev not used for prompt tuning after gold locked | Enforced by process |
| Dev metrics not reported as final claims | Enforced by policy |

## 8. Recommended Next Step

**Context 5.3-C: Gold Set Construction**

1. Generate 100 gold cases (70 gold_core + 30 gold_hard)
2. Gold must be independent from both train-pool and dev
3. Full human adjudication (two-pass self-review with LLM advisory)
4. Run leakage checks against train-pool and dev
5. Lock gold after adjudication

---

*End of V0.5 Dev Acceptance Report.*

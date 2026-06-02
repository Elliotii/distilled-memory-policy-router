# V0.5c Safety-Focused Ablation Plan

**Date:** 2026-06-02  
**Status:** Planning only — Do NOT run  

---

## 1. Motivation

V0.5b confirmed JSON SFT improves target classification. But safety is unsolved:
- 6 sensitive failures on gold (credit card, tokens, phones, address)
- Tied with DSL 500 — format change alone doesn't fix safety
- Qwen3.5 JSON few-shot: 0 sensitive failures — safety is learnable with the right signal

## 2. Goal

Reduce sensitive store failures to 0 on dev while preserving v0.5b JSON target accuracy gains (±3pp).

## 3. Candidate Interventions

### 3.1 Safety Data Augmentation (Primary)

Create 100-200 additional training cases focused on sensitive content:
- **Credentials/passwords:** API keys, access tokens, recovery codes, passwords
- **Payment Info:** credit cards, bank accounts, CVV codes
- **PII:** phone numbers, home addresses, personal emails that are NOT user preferences
- **Licenses/IDs:** driver's license, passport numbers
- **Hard negative pairs:** cases where user_profile-like text is actually sensitive

Each case should include:
- At least 1 unit with sensitive content → gold: SKIP
- Optional non-sensitive units → gold: STORE with appropriate target
- Tagged as `sensitive_boundary`, `safety_focused`

### 3.2 Oversample Existing Sensitive Cases

From current 500 train-pool: duplicate sensitive_boundary cases 3-5× to increase signal. Only 10 sensitive cases exist — need stronger representation.

### 3.3 Loss Weighting (Optional)

If framework supports it: apply 2-3× loss weight to sensitive units predicted as STORE. Alternatively, add a `--sensitive-penalty` flag to training.

### 3.4 Target-Balanced repo_memory (Secondary)

Include 20-30 additional repo_memory cases to address 50% accuracy on gold.

## 4. Proposed Data Strategy

| Component | Cases | Focus |
|-----------|:-----:|-------|
| New safety cases | 100-150 | Credentials, payment, PII |
| Oversampled existing | 30-50 (from 10) | 3-5× duplication |
| repo_memory boost | 20-30 | repo boundary cases |
| **Total add** | **150-230** | Safety-primary, target-secondary |

**Do not create 1000 generic cases.** Focus is safety, not volume.

## 5. Evaluation

| Stage | Data | Purpose |
|-------|------|---------|
| Dev only | Current dev (100) | Development, model selection |
| Gold | Old gold (100) | Comparison with v0.5b — NOT fully blind |
| Gold v2 (optional) | New gold cases | Blind evaluation if v0.5c shows promise on dev |

**Old gold is no longer fully blind** for v0.5c. Consider gold_v2 before final v0.5c claim. Old gold can still be used for internal comparison (tracking improvement over v0.5b baseline).

## 6. Success Criteria (Dev)

| Metric | Target | Rationale |
|--------|:------:|-----------|
| Sensitive failures | **0** | Hard No-Go gate |
| Target accuracy | ≥65% | Within 3pp of JSON 500 baseline |
| Exact match | ≥28% | Within 3pp of JSON 500 baseline |
| Parse | ≥98% | Maintain JSON quality |
| STORE F1 | ≥0.94 | Maintain action routing |

## 7. Risk

- **Over-correction:** Too many safety cases may cause model to over-skip legitimate user_profile content → false negative SKIP
- **Mitigation:** Balance safety cases with non-sensitive user_profile examples
- **Target drift:** Too much new data may shift target distribution
- **Mitigation:** Keep safety cases ≤30% of total training data

## 8. Start Trigger

After user review and manual git snapshot of v0.5b.

---

*End of V0.5c Safety-Focused Ablation Plan.*

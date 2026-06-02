# V0.5 Generation Review Gates

Version: v0.5  
Date: 2026-06-01  
Status: Defines review checkpoints for training data generation

## Gate 1: After Batch200

**Trigger:** 200 cases generated (batch100 + 100 new).

**Checks:**
- Structural: `validate_jsonl_file` passes, all DSL parse, canonical match
- Distribution: targets within batch200 range (±5pp of batch500 blueprint targets)
- Leakage: no overlap with subset50, few-shot, or prior locked sets
- Sensitive: all sensitive-boundary cases audited, 0 sensitive STOREd

**Audit:**
- Full per-case semantic audit
- All high-risk and medium-risk cases manually listed
- Label policy compliance check on 20% sample (40 cases)

**Human Review:**
- Review all cases flagged `human_review_needed`
- Sample size: all high-risk + random 10% of medium-risk

**Go criteria:**
- ≤5 cases flagged human_review_needed
- 0 critical labeling errors
- Label policy compliance ≥95% in sample
- All distribution targets within range

**No-Go criteria:**
- >10 cases human_review_needed
- Any critical labeling error (e.g., sensitive unit STOREd)
- Distribution collapse in any target

---

## Gate 2: After Batch500

**Trigger:** 500 training-pool cases generated.

**Checks:**
- Structural: full validation pass
- Distribution: all targets within blueprint ranges
- Leakage: complete re-check against all existing data
- Sensitive: full sensitive audit

**Audit:**
- Spot-check 10% (50 cases) randomly sampled
- Label policy compliance check on sample
- Distribution report with per-domain breakdown

**Human Review:**
- Review all flagged cases from spot-check
- Review distribution report

**Go criteria:**
- Label policy compliance ≥97% in spot-check
- All distribution targets within blueprint ranges
- 0 sensitive units STOREd in spot-check

**No-Go criteria:**
- Label policy compliance <95%
- Any sensitive unit STOREd
- Distribution outside blueprint ranges by >10pp

---

## Gate 3: Before Dev Set

**Trigger:** Dev set (80 cases) selected from training pool or generated separately.

**Checks:**
- Structural: full validation
- Leakage: 0 overlap with training pool IDs or content
- Distribution: matches training pool distribution (±5pp)
- No subsets of batch100 or other validated sets reused

**Audit:**
- Per-case audit on all 80 dev cases
- Confirm dev covers all target categories and boundary types

**Go criteria:**
- All structural validations pass
- Distribution matches training pool
- 0 leakage to training pool

---

## Gate 4: Before Gold Set

**Trigger:** Gold set (100 cases) created and ready to lock.

**Checks:**
- Structural: full validation
- Leakage: 0 overlap with training pool, dev, subset50, few-shot, batch100
- Distribution: representative of real task distribution
- Gold labels confirmed by human review

**Audit:**
- Full per-case audit on all 100 gold cases
- Human review of ALL gold labels (not sample — full review)
- Confirm gold labels are semantically correct

**Go criteria:**
- All gold labels human-reviewed and approved
- 100% label policy compliance
- Gold set LOCKED — no further changes without explicit process

**LOCK RULE:** Once gold is locked, it must never be used for training, prompt design, or hyperparameter tuning. Gold is opened only for final evaluation.

---

## Gate 5: Before Training

**Trigger:** All previous gates passed. Training ready to start.

**Checks:**
- All 4 previous gates documented as passed
- Training pool (500 cases) validated
- Dev set (80 cases) validated
- Gold set (100 cases) locked
- Baseline eval plan ready
- No data leakage between any splits
- Label policy compliance verified across all splits

**Final Go/No-Go:**
- **Go:** All gates passed, training config ready, VRAM available
- **No-Go:** Any gate not passed, gold not locked, baseline not ready
- **Partial-Go:** Minor issues that can be fixed without regenerating splits

---

## Important: Do Not Train Unless

1. Gold set is LOCKED (no further label changes)
2. Dev set is validated and separate from train
3. Baseline eval plan is ready (eval_runner configured with gold)
4. Training configuration is documented and approved
5. All 5 review gates are passed with documented evidence

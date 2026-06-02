# V0.5 Train Pool Manifest Plan

Version: v0.5
Date: 2026-06-02
Status: Planning — manifests for train pool, dev, gold, and related files
Context: 5.3-A — dev/gold + provenance + leakage planning

---

## 1. Corrected Batch500 Status

### 1.1 Current State

The corrected batch500 is a **training-pool candidate**, not final locked train data.

| Property | Value |
|----------|-------|
| Case file | `data/v05/batches/v05_batch500_corrected_cases.jsonl` |
| SFT file | `data/v05/batches/v05_batch500_corrected_sft_messages.jsonl` |
| Cases | 500 |
| SFT rows | 500 |
| Source tag | `v05_batch500_corrected_dry_run` |
| `metadata.is_final_train_data` | `false` (all 500 rows) |
| Status | Draft / candidate |

### 1.2 Why Not Final Yet

The corrected batch500 is not final train data because:

1. **No dev/gold split exists.** The 500 cases form a unified pool. Dev and gold must be constructed as held-out sets first.
2. **Leakage checks not performed.** Train↔dev and train↔gold near-duplicate checks have not been run.
3. **Borderline cases not adjudicated.** 6 borderline cases from independent review remain non-blocking but unresolved.
4. **Training config not finalized.** Model, LoRA parameters, and training strategy are not finalized.
5. **Gold not locked.** Without a locked gold set, there is no unbiased evaluation standard.
6. **Source is dry run.** The source tag must be relabeled to `v05_train` before training.

### 1.3 Prerequisites for Final Train Data

The corrected batch500 can be promoted to final train data ONLY after:

- [ ] Dev set (80–100 cases) constructed and validated.
- [ ] Gold set (100 cases) constructed and human-adjudicated.
- [ ] Leakage checks passed: no exact or near-duplicate text between train and dev/gold.
- [ ] Few-shot examples confirmed sourced from train only.
- [ ] Prompt examples confirmed not sourced from dev or gold.
- [ ] Subset50 status resolved (retired from final eval or explicitly excluded from all splits).
- [ ] Borderline cases adjudicated or explicitly waived.
- [ ] Source tag updated to `v05_train`.
- [ ] `metadata.is_final_train_data` set to `true`.
- [ ] Final SFT messages regenerated with updated source tag and metadata.

---

## 2. Future Final Train File

### 2.1 Proposed File Paths

Once all prerequisites are met, the following files will be created:

```
data/v05/train/v05_train_pool_500.jsonl       # 500 cases
data/v05/train/v05_train_sft_500.jsonl        # 500 SFT messages
```

### 2.2 Required Properties

| Property | Value |
|----------|-------|
| `source` | `v05_train` |
| `metadata.is_final_train_data` | `true` |
| `metadata.is_training_pool_candidate` | `false` or absent |
| Based on | Corrected batch500 with any final adjustments |

### 2.3 Generation Command (Planned)

```bash
python3 src/v05/render_sft_messages.py \
  --cases data/v05/train/v05_train_pool_500.jsonl \
  --out data/v05/train/v05_train_sft_500.jsonl \
  --source v05_train
```

### 2.4 Pre-Generation Checks

Before generating the final train SFT messages:

1. Confirm all prerequisites (Section 1.3) are met.
2. Run structural validation on `v05_train_pool_500.jsonl`.
3. Run DSL parse validation.
4. Run canonical consistency check.
5. Run sensitive content audit.
6. Confirm distribution report within blueprint ranges.
7. Run leakage checks against dev and gold.
8. Document any changes from corrected batch500.

---

## 3. Complete File Manifest

### 3.1 Training Pool

| Role | Path | Cases | Status |
|------|------|:-----:|--------|
| Train pool **candidate** | `data/v05/batches/v05_batch500_corrected_cases.jsonl` | 500 | ✓ Validated, draft |
| Train pool **candidate** SFT | `data/v05/batches/v05_batch500_corrected_sft_messages.jsonl` | 500 | ✓ Validated, draft |
| Train pool **final** | `data/v05/train/v05_train_pool_500.jsonl` | 500 | ✗ Not yet created |
| Train pool **final** SFT | `data/v05/train/v05_train_sft_500.jsonl` | 500 | ✗ Not yet created |

### 3.2 Development Set

| Role | Path | Cases | Status |
|------|------|:-----:|--------|
| Dev cases | `data/v05/dev/v05_dev_cases.jsonl` | 80–100 | ✗ Not yet created |
| Dev SFT | `data/v05/dev/v05_dev_sft_messages.jsonl` | 80–100 | ✗ Not yet created |

### 3.3 Gold Set

| Role | Path | Cases | Status |
|------|------|:-----:|--------|
| Gold cases | `data/v05/gold/v05_gold_cases.jsonl` | 100 | ✗ Not yet created |
| Gold SFT | `data/v05/gold/v05_gold_sft_messages.jsonl` | 100 | ✗ Not yet created |
| Gold lock file | `data/v05/gold/v05_gold_lock.json` | — | ✗ Not yet created |

### 3.4 Prompt Examples

| Role | Path | Cases | Status |
|------|------|:-----:|--------|
| Few-shot examples (3) | Source: train pool (TBD) | 3 | ✗ Not yet selected |
| System prompt template | `prompts/v05/unit_dsl_system.txt` or similar | — | ✗ Not yet finalized |

**Rule:** Few-shot examples MUST come from the train pool. They MUST NOT come from dev, gold, or subset50.

### 3.5 Excluded from Evaluation

| Role | Path | Cases | Status |
|------|------|:-----:|--------|
| Subset50 | `data/v04/subset50_cases.jsonl` (TBC) | 50 | ⚠ Status TBD |

**Decision required:** Subset50 must be either:
- **Retired from final eval** (not used in any train/dev/gold split), or
- **Used only as historical interface pilot evidence**, with explicit documentation that it was used for A/B/C prompt development and is not an independent holdout.

### 3.6 Historical / Intermediate Files (Not Training Data)

| File | Role |
|------|------|
| `data/v05/batches/v05_batch50_cases.jsonl` | Intermediate batch50 (50 cases) |
| `data/v05/batches/v05_batch100_cases.jsonl` | Intermediate batch100 (100 cases) |
| `data/v05/batches/v05_batch200_cases.jsonl` | Intermediate batch200 (200 cases) |
| `data/v05/batches/v05_batch300_cases.jsonl` | Intermediate batch300 (300 cases) |
| `data/v05/batches/v05_batch500_cases.jsonl` | Original batch500 (preserved) |
| `data/v05/batches/v05_batch500_rebalanced_cases.jsonl` | Rebalanced batch500 (preserved) |
| `data/v05/batches/*_sft_messages.jsonl` | All intermediate SFT files |
| `data/v04/pilot_cases.jsonl` | v0.4 pilot (200, seed/skeleton reference) |
| `data/v04/bridge_cases.jsonl` | v0.4 bridge (40, boundary reference) |

These are preserved for audit trail and reproducibility. They are NOT training data.

### 3.7 Few-Shot Example IDs

The few-shot examples in the system prompt (if used) must be recorded:

| Example # | case_id | Source Split | Selected? |
|-----------|---------|-------------|:---------:|
| 1 | TBD | v05_train | ✗ |
| 2 | TBD | v05_train | ✗ |
| 3 | TBD | v05_train | ✗ |

Selection criteria:
- Cover all three shapes (READ-only, STORE/SKIP-only, READ+STORE joint).
- Cover at least 3 of 5 STORE targets.
- Include at least one SKIP example.
- Do not use any case from the 6 borderline cases.
- Do not use cases with the cross-batch duplicate memory.

---

## 4. Changelog Rules

### 4.1 What Must Be Recorded

Any change from corrected batch500 to final train data must be recorded in a changelog. This includes:

| Change Type | Example | Must Record |
|------------|---------|:-----------:|
| Case removed | Case dropped due to quality issue | case_id, reason |
| Case added | New case generated to fill distribution gap | case_id, source batch |
| Label changed | Target corrected | case_id, unit_id, old → new, reason |
| DSL updated | DSL line reordered or corrected | case_id, old_dsl, new_dsl, reason |
| Metadata updated | Tags, notes changed | case_id, field, old → new, reason |
| Source tag updated | `v05_batch500_corrected_dry_run` → `v05_train` | All cases |
| is_final_train_data set | `false` → `true` | All cases |

### 4.2 Changelog File

Create `data/v05/train/v05_train_changelog.md` when final train data is generated. It should record:

```markdown
# V0.5 Train Data Changelog

## From corrected batch500 → Final Train Data

| # | case_id | Change | Old | New | Reason |
|---|---------|--------|-----|-----|--------|
| 1 | ... | ... | ... | ... | ... |

## Summary
- Cases removed: N
- Cases added: N
- Labels changed: N
- Source tag updated: Y
- is_final_train_data set: Y
```

### 4.3 Audit Trail Preservation

The following files must be preserved as immutable audit trail:

- `data/v05/batches/v05_batch500_cases.jsonl` (original batch500)
- `data/v05/batches/v05_batch500_rebalanced_cases.jsonl` (rebalanced)
- `data/v05/batches/v05_batch500_corrected_cases.jsonl` (corrected)
- `data/v05/batches/v05_batch500_independent_review_fixes.jsonl` (fix log)
- All batch-specific audit and review reports in `reports/v05/`

These files document the full provenance chain from original generation → rebalancing → independent review → corrections → final train.

---

## 5. Changelog for This Manifest

| Date | Change |
|------|--------|
| 2026-06-02 | Initial creation (Context 5.3-A) |

---

*End of V0.5 Train Pool Manifest Plan.*

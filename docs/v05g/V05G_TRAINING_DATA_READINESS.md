# V05G Training Data Readiness

**Status:** ✅ Repaired and ready for independent audit and server-side training  
**Date:** 2026-06-05  
**Repair:** Semantic quality repair for Opus 4.8 review findings

## Quick Summary

Prepared two training datasets for BF16 LoRA r16 scaling experiment on Qwen3.5-4B:

| Dataset | Cases | STORE Units | Path |
|---------|-------|-------------|------|
| 500-control | 500 | 1,042 | `data/v05g/json_sft/v05g_train_500_control_json_sft_messages.jsonl` |
| 1000-targeted | 1,000 | 2,079 | `data/v05g/json_sft/v05g_train_1000_targeted_json_sft_messages.jsonl` |

## Research Questions

1. Does BF16 LoRA r16 improve over QLoRA r16 with the same 500 examples?
2. Does 1000 targeted-balanced examples improve over BF16 r16 500?

## Data Integrity

- **500-control**: Exact byte-for-byte copy of v05b train 500 (hash `c6ec79d9...` preserved)
- **1000-targeted**: 500-control + 500 repaired targeted-balanced cases (true superset)
- **9/9 quality gates pass** (parse, coverage, exclusivity, safety, IDs, targets, placeholders)
- **0 leakage** vs dev, old gold, gold_v2_009
- **Semantic quality repaired** per Opus 4.8 review: READ recoverability, opener diversification, sensitive literal diversity

## Key Distributions (Combined 1000)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| task_state | 28.2% | 25-32% | ✅ |
| service_memory | 26.6% | 24-32% | ✅ |
| repo_memory | 19.7% | 16-22% | ✅ |
| project_memory | 14.9% | 12-20% | ✅ |
| user_profile | 10.7% | 6-12% | ✅ |

## Semantic Quality (Post-Repair)

| Metric | Value |
|--------|-------|
| Stale READ count | 0 |
| Distractor READ count | 0 |
| 3-word-prefix binary accuracy | 90.9% (was 100%) |
| Body-dependent cases | 64.2% |
| Sensitive literal unique texts | 70 (was 18) |
| Sensitive literal max repetition | 2x (was 5x) |

## Lock Manifest

`data/v05g/v05g_training_data_lock.json` contains SHA-256 hashes for all 6 data files with repair metadata.

## Known Limitations (Opus 4.8 Review)

1. **READ = entity matching**: READ labels are recoverable but collapse to service/repo name matching. Does not teach graded context selection or semantic relevance reasoning.
2. **Prefix shortcut reduced but not eliminated**: 3-word accuracy 90.9%, 6-word 97.5%, 10-word 99.6%. "Body-dependent" mostly means reading a short templated tail.
3. **project_memory READ = 0% in additional 500**: Mitigated by 500-control (89.7% project_memory READ rate).
4. **1000-vs-500 includes data volume + domain/template-family confound**: Not pure data-volume causality.

See: `reports/v05g/v05g_repaired_training_data_limitations.md`

## BF16 LoRA Configs (v05g)

| Config | Path |
|--------|------|
| BF16 r16 500 | `configs/v05g/qwen35_bf16_lora_json_r16_500.yaml` |
| BF16 r16 1000 | `configs/v05g/qwen35_bf16_lora_json_r16_1000.yaml` |

Training script: `src/v05/train_lora_router.py` (updated for BF16 standard LoRA support)

Server runbook: `docs/v05g/V05G_BF16_LORA_SERVER_RUNBOOK.md`

## What NOT to do

- Do NOT train locally (RTX 4070 12GB insufficient for BF16 4B)
- Do NOT evaluate on gold_v2_009 (save for final)
- Do NOT modify gold_v2_009
- Do NOT create a new gold set
- Do NOT modify 500-control data
- Do NOT git add/commit/push the data files

## Files Created / Updated

### Data (regenerated)
- `data/v05g/cases/v05g_train_additional_500_targeted_cases.jsonl`
- `data/v05g/json_sft/v05g_train_additional_500_targeted_json_sft_messages.jsonl`
- `data/v05g/cases/v05g_train_1000_targeted_cases.jsonl`
- `data/v05g/json_sft/v05g_train_1000_targeted_json_sft_messages.jsonl`
- `data/v05g/v05g_training_data_lock.json`

### Data (preserved, byte-identical)
- `data/v05g/cases/v05g_train_500_control_cases.jsonl`
- `data/v05g/json_sft/v05g_train_500_control_json_sft_messages.jsonl`

### Configs (new)
- `configs/v05g/qwen35_bf16_lora_json_r16_500.yaml`
- `configs/v05g/qwen35_bf16_lora_json_r16_1000.yaml`

### Scripts
- `src/v05g/repair_v05g_additional_500.py` (new)
- `src/v05/train_lora_router.py` (updated — BF16 support)
- `src/v05g/build_v05g_training_data.py` (original, unchanged)
- `src/v05g/audit_v05g_training_data.py` (original, unchanged)

### Reports (new)
- `reports/v05g/v05g_opus_training_data_review_response.md`
- `reports/v05g/v05g_additional_500_read_repair_report.md`
- `reports/v05g/v05g_additional_500_prefix_shortcut_repair_report.md`
- `reports/v05g/v05g_sensitive_literal_diversification_report.md`
- `reports/v05g/v05g_repaired_training_data_readiness_decision.md`
- `reports/v05g/v05g_repaired_training_data_limitations.md`
- `reports/v05g/v05g_bf16_lora_claim_boundaries.md`
- `reports/v05g/v05g_bf16_lora_config_report.md`
- `reports/v05g/v05g_server_resource_plan.md`
- `reports/v05g/v05g_server_training_runbook.md`
- `reports/v05g/v05g_dev_eval_plan.md`
- `reports/v05g/v05g_bf16_lora_server_readiness_decision.md`

### Reports (updated)
- `reports/v05g/v05g_training_data_plan.md`
- `reports/v05g/v05g_training_data_quality_audit.md`
- `reports/v05g/v05g_training_data_leakage_report.md`
- `reports/v05g/v05g_1000_targeted_distribution_report.md`

### Docs
- `docs/v05g/V05G_TRAINING_DATA_READINESS.md` (this file, updated)
- `docs/v05g/V05G_BF16_LORA_SERVER_RUNBOOK.md` (new)

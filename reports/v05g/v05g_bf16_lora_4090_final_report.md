# v0.5g BF16 LoRA 4090 Final Report

**Date:** 2026-06-08
**Status:** Complete — v0.5g BF16 LoRA r=16 RTX 4090 training and evaluation synthesis

---

## Executive Summary

**v0.5g BF16 LoRA 4090** tested two research questions on Qwen3.5-4B:

1. Does BF16 standard LoRA r=16 improve over QLoRA r=16 with the same 500 examples?
2. Does 1000 targeted-balanced data improve over BF16 r=16 500?

**Answer:** BF16 alone does NOT improve over QLoRA r=16. The 1000-targeted variant is the best evaluated system on locked gold_v2_009 by exact match and write-side routing metrics among the compared systems, driven by write-side routing gains (STORE F1 0.990, SKIP F1 0.981, target accuracy 100.0%). READ F1 was not available for older v0.5e anchors, and READ selection remains the dominant remaining full-exact bottleneck.

---

## 1. Objective

Evaluate BF16 standard LoRA r=16 on Qwen3.5-4B using two data variants deployed to an RTX 4090 24GB server:

| Variant | Data | Research Question |
|---------|------|-------------------|
| BF16 r16 500-control | 500 (same as v05e QLoRA r16) | Does BF16 improve over QLoRA r16? |
| BF16 r16 1000-targeted | 500-control + 500 targeted-balanced | Does 1000 targeted-balanced improve over 500? |

## 2. Setup

### Environment
- **GPU:** RTX 4090 24GB (fallback from the planned larger-GPU setup)
- **Model:** Qwen3.5-4B at `$QWEN35_MODEL_PATH`
- **Training framework:** PyTorch + Transformers + PEFT + TRL
- **LoRA:** r=16, alpha=32, 6 target modules, BF16 (no quantization)
- **4090 configs:** batch_size=2, grad_accum=8, gradient_checkpointing=true

### Server Snapshot
- **Git archive:** Deployed from git archive snapshot (not normal checkout)
- **Version record:** `v0.5g-bf16-lora-4090-ready / 7e40f02bbb34c2c5ecf8f7468a066cba0105db4d`

## 3. Data

| Dataset | Cases | STORE Units | Path |
|---------|-------|-------------|------|
| 500-control SFT | 500 | 1,042 | `data/v05g/json_sft/v05g_train_500_control_json_sft_messages.jsonl` |
| 1000-targeted SFT | 1,000 | 2,079 | `data/v05g/json_sft/v05g_train_1000_targeted_json_sft_messages.jsonl` |
| Dev | 100 | — | `data/v05/dev/v05_dev_cases.jsonl` |
| gold_v2_009 (active) | 150 | — | `data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl` |

**gold_v2_009 SHA-256 (unchanged):**
```
f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72
```

## 4. Configs Used (4090 Fallback)

| Config | Path |
|--------|------|
| BF16 r16 500 4090 | `configs/v05g/qwen35_bf16_lora_json_r16_500_4090.yaml` |
| BF16 r16 1000 4090 | `configs/v05g/qwen35_bf16_lora_json_r16_1000_4090.yaml` |

Key differences from the planned larger-GPU configs:
- `per_device_train_batch_size`: 2 (vs 4)
- `gradient_accumulation_steps`: 8 (vs 4)
- `gradient_checkpointing`: true (vs disabled)

## 5. Artifact Provenance

- **Source:** Download from RTX 4090 server at `v05g_bf16_lora_4090_final_artifacts.tar.gz`
- **Location on disk:** `/mnt/c/Users/abc16/Desktop/v05g_bf16_lora_4090_final_artifacts.tar.gz` (80.6 MB)
- **Extracted to:** `/tmp/v05g_final_artifacts_review`
- **Copied into repo:** `results/v05g_bf16_lora/`, `data/v05g/model_predictions/`, `reports/v05g/server_runs/`, `logs/v05g/`
- **SNAPSHOT_COMMIT.txt:** `v0.5g-bf16-lora-4090-ready / 7e40f02bbb34c2c5ecf8f7468a066cba0105db4d`

## 6. Results

### 6.1 Dev Results (100 cases)

| Metric | BF16 r16 500_4090 | BF16 r16 1000_4090 | Δ |
|--------|:-----------------:|:------------------:|:--:|
| Parse success | 100.0% | 100.0% | 0 |
| Exact match | 49.0% | **59.0%** | +10.0pp |
| READ F1 | 92.0% | **93.3%** | +1.3pp |
| STORE F1 | 96.7% | **97.1%** | +0.4pp |
| SKIP F1 | 81.0% | **83.1%** | +2.1pp |
| Target accuracy | 85.3% | **89.5%** | +4.2pp |
| False store rate | 5.2% | 5.2% | 0 |
| Irrelevant read rate | 11.4% | 10.5% | −0.9pp |
| Sensitive store | 2/3 (66.7%) | 2/3 (66.7%) | 0 |

**1000-targeted gains on dev:** exact +10pp, target accuracy +4.2pp, SKIP F1 +2.1pp.

### 6.2 Gold v2_009 Results (150 cases)

| Metric | BF16 r16 500_4090 | BF16 r16 1000_4090 | Δ |
|--------|:-----------------:|:------------------:|:--:|
| Parse success | 98.7% | 99.3% | +0.6pp |
| Exact match | 16.7% | **36.0%** | +19.3pp |
| READ F1 | 80.1% | **84.6%** | +4.5pp |
| STORE F1 | 89.2% | **99.0%** | +9.8pp |
| SKIP F1 | 84.0% | **98.1%** | +14.1pp |
| Target accuracy | 84.7% | **100.0%** | +15.3pp |
| False store rate | 10.4% | **1.2%** | −9.2pp |
| Irrelevant read rate | 10.0% | 15.5% | +5.5pp |
| Sensitive store | 0/4 (0.0%) | 0/4 (0.0%) | 0 |

**1000-targeted gains on gold:** exact +19.3pp, STORE F1 +9.8pp, SKIP F1 +14.1pp, target accuracy +15.3pp, false store −9.2pp.

**Note:** Summary headings say "Dev Evaluation" even for gold split due to generic evaluator heading. The `split:` field and metrics are authoritative.

## 7. Comparison with v05e Systems (gold_v2_009, 150 cases)

| # | System | Exact | Parse | READ F1 | STORE F1 | SKIP F1 | Target Acc | False Store |
|:-:|--------|:-----:|:-----:|:-------:|:--------:|:-------:|:----------:|:-----------:|
| 1 | **BF16 r16 1000_4090** | **36.0%** | 99.3% | 84.6% | **0.990** | **0.981** | **100.0%** | 1.2% |
| 2 | Qwen3.5 JSON few-shot | 30.7% | 86.0% | — | 0.856 | 0.847 | 75.3% | — |
| 3 | Qwen3.5 QLoRA r16 500 | 22.7% | 94.7% | — | 0.909 | 0.892 | 84.2% | — |
| 4 | Qwen3.5 QLoRA r8 500 | 22.7% | 98.7% | — | 0.880 | 0.834 | 79.1% | — |
| 5 | **BF16 r16 500_4090** | 16.7% | 98.7% | 80.1% | 0.892 | 0.840 | 84.7% | 10.4% |
| 6 | Qwen3-4B QLoRA r8 500 | 16.0% | 100.0% | — | 0.925 | 0.860 | 76.8% | — |

**Key observations:**
- **BF16 r16 1000_4090 is the best evaluated system on locked gold_v2_009** by exact match and write-side routing metrics among the compared systems. READ F1 was not available for older v0.5e anchors.
- BF16 r16 500_4090 does NOT outperform old QLoRA r16 on gold (16.7% vs 22.7% exact). BF16 alone is not sufficient.
- The strong result is BF16 standard LoRA + 1000 targeted-balanced data under 4090 fallback settings.
- 1000-targeted closes the gold generalization gap: dev 59% → gold 36% (23pp gap) vs 500-control: dev 49% → gold 16.7% (32.3pp gap).

## 8. Main Findings

1. **1000-targeted is the best evaluated system by exact match and write-side routing metrics among the compared systems** — READ F1 was not available for older v0.5e anchors.
2. **BF16 alone does not help** — 500-control underperforms old QLoRA r16 on gold.
3. **Write-side routing is near-solved** — 1000-targeted achieves STORE F1 0.990, SKIP F1 0.981, target accuracy 100.0% on gold.
4. **READ selection remains the bottleneck** — READ F1 84.6% on gold (vs 93.3% on dev). Irrelevant read rate 15.5%.
5. **Data quality matters more than precision** — 1000-targeted (BF16) beats 500-control (BF16) by 19.3pp exact on gold, while 500-control (BF16) trails 500 (QLoRA) by 6pp.
6. **Sensitive-store metric is promising but limited** — 0/4 sensitive units were stored on locked gold_v2_009 under the semantic sensitive-store metric. Dev still shows 2/3 sensitive stores, and older tag-based safety rates are not directly comparable.

## 9. Limitations

1. **RTX 4090 fallback** — Not the planned larger-GPU config. Batch size halved, gradient checkpointing enabled. Other hardware settings may differ.
2. **Template-generated training data** — Additional 500 targeted-balanced cases are synthetic. Semantic quality not human-reviewed.
3. **READ = entity matching in training** — READ labels recoverable but collapse to name matching; does not teach graded context selection.
4. **Prefix shortcut** — 3-word-prefix accuracy 90.9% in training data; model may learn shallow patterns.
5. **1000-vs-500 confound** — Includes data volume + domain/template-family confound. Not pure data-size causality.
6. **No production claim** — These are lab results on a synthetic gold set. No claim of production safety, downstream utility, or live retrieval performance.
7. **Gold is synthetic** — gold_v2_009 is template-generated. Semantic label quality assumed from template logic.

## 10. Next Steps

1. **Post-result audit** — Verify gold_v2_009 metrics independently (user-verify prediction JSONL against gold).
2. **v1.0 packaging** — Package v0.5e/v0.5g results, adapters, configs, and locked gold for portfolio/reproducibility.
3. **Downstream benchmark (v1.0)** — Evaluate 1000-targeted adapter on an independent retriever + agent task to assess real-world utility.
4. **No further v0.5 experiments** — The READ bottleneck requires fundamentally different approaches (longer context, retrieval augmentation, two-stage routing). Data scaling within this framework is at diminishing returns.
5. **READ-focused v1.0 research** — Investigate graded relevance scoring, multi-turn READ, or retrieval-augmented READ.

---

*End of v0.5g BF16 LoRA 4090 Final Report.*

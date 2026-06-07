# v0.5g BF16 LoRA 4090 — Artifact Manifest

**Date:** 2026-06-08
**Source:** `/mnt/c/Users/abc16/Desktop/v05g_bf16_lora_4090_final_artifacts.tar.gz` (80,569,754 bytes)
**Server Snapshot:** `v0.5g-bf16-lora-4090-ready / 7e40f02bbb34c2c5ecf8f7468a066cba0105db4d`

---

## Artifact Inventory

### SNAPSHOT_COMMIT.txt
```
v0.5g-bf16-lora-4090-ready / 7e40f02bbb34c2c5ecf8f7468a066cba0105db4d
```

### Training Logs (`logs/v05g/`)
| File | Description |
|------|-------------|
| `train_bf16_r16_500_4090.log` | BF16 r16 500-control training log |
| `train_bf16_r16_500_4090.status.log` | Training status summary |
| `train_bf16_r16_1000_4090.log` | BF16 r16 1000-targeted training log |
| `eval_bf16_r16_500_4090_predict.log` | 500-control dev prediction generation |
| `eval_bf16_r16_500_4090_metrics.log` | 500-control dev metrics computation |
| `eval_bf16_r16_1000_4090_predict.log` | 1000-targeted dev prediction generation |
| `eval_bf16_r16_1000_4090_metrics.log` | 1000-targeted dev metrics computation |
| `eval_bf16_r16_500_4090_gold_v2_009_predict.log` | 500-control gold prediction generation |
| `eval_bf16_r16_500_4090_gold_v2_009_metrics.log` | 500-control gold metrics computation |
| `eval_bf16_r16_1000_4090_gold_v2_009_predict.log` | 1000-targeted gold prediction generation |
| `eval_bf16_r16_1000_4090_gold_v2_009_metrics.log` | 1000-targeted gold metrics computation |

### Model Predictions (`data/v05g/model_predictions/`)
| File | Rows | Split |
|------|:----:|-------|
| `bf16_r16_500_4090_dev_predictions.jsonl` | 100 | dev |
| `bf16_r16_1000_4090_dev_predictions.jsonl` | 100 | dev |
| `bf16_r16_500_4090_gold_v2_009_predictions.jsonl` | 150 | gold_v2_009 |
| `bf16_r16_1000_4090_gold_v2_009_predictions.jsonl` | 150 | gold_v2_009 |

### Metrics (`reports/v05g/server_runs/`)
| File | Split | Cases |
|------|-------|:----:|
| `v05g_bf16_r16_500_4090_dev_metrics.json` | dev | 100 |
| `v05g_bf16_r16_500_4090_dev_summary.md` | dev | 100 |
| `v05g_bf16_r16_1000_4090_dev_metrics.json` | dev | 100 |
| `v05g_bf16_r16_1000_4090_dev_summary.md` | dev | 100 |
| `v05g_bf16_r16_500_4090_gold_v2_009_metrics.json` | gold_v2_009 | 150 |
| `v05g_bf16_r16_500_4090_gold_v2_009_summary.md` | gold_v2_009 | 150 |
| `v05g_bf16_r16_1000_4090_gold_v2_009_metrics.json` | gold_v2_009 | 150 |
| `v05g_bf16_r16_1000_4090_gold_v2_009_summary.md` | gold_v2_009 | 150 |

### Adapters (`results/v05g_bf16_lora/`)
| Directory | Size | Files |
|-----------|:----:|-------|
| `qwen35_json_r16_500_4090/adapter/` | ~57 MB | adapter_config.json, adapter_model.safetensors (39.3 MB), tokenizer.json, tokenizer_config.json, chat_template.jinja, README.md |
| `qwen35_json_r16_1000_4090/adapter/` | ~57 MB | Same structure |

**Note:** Both adapters share identical tokenizer files (same base model). Only `adapter_model.safetensors` differs between variants.

---

## Hash Verification

### gold_v2_009 (unchanged)
```
sha256: f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72
File: data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl
```

### v05g Training Data Locks
See `data/v05g/v05g_training_data_lock.json` for SHA-256 hashes of all 6 training data files.

---

## Verification Checklist

| # | Check | Result |
|---|-------|--------|
| 1 | SNAPSHOT_COMMIT.txt present and correct | ✅ `7e40f02...` |
| 2 | Dev prediction row counts = 100 each | ✅ |
| 3 | Gold prediction row counts = 150 each | ✅ |
| 4 | Metrics JSON files parse correctly | ✅ 4/4 |
| 5 | Summary MD files present | ✅ 4/4 |
| 6 | Adapter 500 directory non-empty | ✅ ~57 MB |
| 7 | Adapter 1000 directory non-empty | ✅ ~57 MB |
| 8 | gold_v2_009 hash matches | ✅ `f5cf7be1...` |
| 9 | Metrics match known expected values | ✅ |
| 10 | Source data not overwritten | ✅ |
| 11 | Gold files not modified | ✅ |
| 12 | Base model files not copied | ✅ N/A |

---

## Non-Artifact Files (in repo, not in tarball)

These exist in the repo but were not part of the server artifact download:
- All source code (`src/`)
- All configs (`configs/v05g/`)
- All training data (`data/v05g/cases/`, `data/v05g/json_sft/`)
- All planning/review reports (`reports/v05g/*.md` except `server_runs/`)
- All documentation (`docs/v05g/*.md`)

---

*End of v0.5g BF16 LoRA 4090 Artifact Manifest.*

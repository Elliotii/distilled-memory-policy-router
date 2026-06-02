# V0.5b Final Artifact Manifest

**Date:** 2026-06-02  

---

## 1. JSON SFT Training Data (Commit)

| File | Rows |
|------|:----:|
| `data/v05b/json_sft/v05b_train_125_json_sft_messages.jsonl` | 125 |
| `data/v05b/json_sft/v05b_train_250_json_sft_messages.jsonl` | 250 |
| `data/v05b/json_sft/v05b_train_500_json_sft_messages.jsonl` | 500 |
| `data/v05b/json_sft/v05b_dev_json_sft_messages.jsonl` | 100 |

## 2. Configs (Commit)

| File |
|------|
| `configs/v05b/qwen3_4b_lora_json_125.yaml` |
| `configs/v05b/qwen3_4b_lora_json_250.yaml` |
| `configs/v05b/qwen3_4b_lora_json_500.yaml` |

## 3. Training Outputs (DO NOT commit — large)

| Path | Size |
|------|------|
| `results/v05b_lora/qwen3_4b_json_125/` | ~25MB |
| `results/v05b_lora/qwen3_4b_json_250/` | ~25MB |
| `results/v05b_lora/qwen3_4b_json_500/` | ~25MB |

Use LFS if needed, otherwise keep local only.

## 4. Predictions (Commit if size <1MB)

| File | Rows |
|------|:----:|
| `data/v05b/model_predictions/qwen3_4b_lora_json_125_dev_predictions.jsonl` | 100 |
| `data/v05b/model_predictions/qwen3_4b_lora_json_250_dev_predictions.jsonl` | 100 |
| `data/v05b/model_predictions/qwen3_4b_lora_json_500_dev_predictions.jsonl` | 100 |
| `data/v05b/model_predictions/qwen3_4b_lora_json_500_gold_predictions.jsonl` | 100 |

## 5. Reports (Commit)

34 reports in `reports/v05b/`:
- 3 planning/rendering reports
- 3 per-size training reports (125/250/500)
- 3 per-size dev eval reports
- 3 per-size error analysis reports
- 3 per-size comparison/decision reports
- 5 learning curve & comparison reports
- 5 gold evaluation reports
- 7 final consolidation reports

## 6. Modified Scripts (Commit)

| File | Change |
|------|--------|
| `src/v05/train_lora_router.py` | Preflight shows interface label |
| `src/v05/eval_lora_router.py` | Added `--interface` arg for unit_json support |

## 7. New Scripts (Commit)

| File |
|------|
| `src/v05/render_json_sft_messages.py` |

## 8. Docs (Commit)

| File |
|------|
| `docs/v05b/V05B_UNIT_JSON_LORA_PLAN.md` |
| `docs/v05b/V05B_FINAL_RESULTS.md` |
| `docs/v05b/V05B_PROJECT_NARRATIVE.md` |
| `docs/v05b/V05C_SAFETY_ABLATION_PLAN.md` |
| `docs/status/CURRENT_STATE.md` (updated) |

## 9. Never Commit

- `results/v05b_lora/` — training outputs and checkpoints
- `.venv/`, `__pycache__/`, `.DS_Store`
- `checkpoints/`, `models/`, `outputs/`, `wandb/`
- `*.log`, `*.pyc`
- `.env`

---

*End of V0.5b Final Artifact Manifest.*

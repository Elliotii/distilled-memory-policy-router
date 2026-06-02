# V0.5 Git Handoff Checklist

**Date:** 2026-06-02  

---

## Recommended to Commit

| Path | Reason |
|------|--------|
| `docs/v05/` | Planning & results docs |
| `docs/status/CURRENT_STATE.md` | Project state |
| `reports/v05/v05_final_*.md` | Final reports |
| `src/v05/` | v0.5 scripts |
| `src/v04/` | Core lib |
| `configs/v05/` | LoRA configs |
| `prompts/v05/` | Prompt templates |
| `data/v05/train/subsets/*_case_ids.txt` | Small, needed for reproducibility |
| `data/v05/train/subsets/*_cases.jsonl` | Train/dev/gold data (synthetic) |
| `data/v05/train/subsets/*_sft_messages.jsonl` | SFT data |
| `data/v05/dev/` | Dev cases |
| `data/v05/gold/v05_gold_lock.json` | Lock manifest |
| `data/v05/model_predictions/` | Prediction outputs |
| `README_v05.md` | Project README |
| `tests/` | Unit tests |

## Inspect Before Committing

- `data/v05/model_predictions/` — check file sizes
- `data/v05/train/` — verify no real PII
- `data/v05/gold/` — verify locked gold included

## Do NOT Commit

| Path | Reason |
|------|--------|
| `.venv/` | Virtual environment |
| `__pycache__/` | Cache |
| `results/v05_lora/` | Large adapters (~23MB each) |
| `hf_models/` | Local model files (7-9GB) |
| `.env` | Secrets |
| `*.log` | Logs |

## Manual Commands (User Runs)

```bash
git status
du -sh results/v05_lora/ data/v05/model_predictions/
git add docs/ reports/ src/ configs/ prompts/ tests/ data/v05/ README_v05.md
git commit -m "v0.5: memory policy router — data, baselines, LoRA learning curve, locked gold"
git push
```

---

*End of V0.5 Git Handoff Checklist.*

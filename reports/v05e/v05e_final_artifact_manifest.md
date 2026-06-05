# V0.5e Final Artifact Manifest

**Date:** 2026-06-04  

## Reports (cumulative v05e)

| Phase | Count |
|-------|:-----:|
| Protocol & pre-registration | 8 |
| v001-v009 construction | ~30 |
| Pre-evaluation corrections | 4 |
| Four-system evaluation | 5 |
| Final synthesis | 7 |
| **Total** | **~54** |

## Key Data Files

| File | Rows |
|------|:----:|
| `data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl` | 150 |
| `data/v05e/gold_v2/v05e_gold_v2_009_holdout_cases.jsonl` | 30 |
| `data/v05e/gold_v2/v05e_gold_v2_009_lock.json` | — |
| Gold_v2 prediction files | 4 × 150 rows |

## Scripts

| File | Purpose |
|------|---------|
| `src/v05e/build_gold_v2_009.py` | gold_v2_009 construction |
| `src/v04/case_validator.py` | Patched for text/content compatibility |
| `src/v05/render_sft_messages.py` | Patched for text/content compatibility |
| `src/v05/qwen_v05_output_runner.py` | Patched for text/content compatibility |

## DO NOT Commit

- `results/v05*_lora/` — adapter checkpoints (~25MB each)
- Prior gold_v2 versions (v001-v008) — preserved for audit only

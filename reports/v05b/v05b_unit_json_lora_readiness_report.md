# V0.5b Unit JSON LoRA Readiness Report

**Date:** 2026-06-02  
**Status:** ✅ Ready for Context 5.7-B (125-case smoke training)  

---

## Readiness Checklist

| Item | Status | Notes |
|------|:------:|-------|
| JSON SFT rendering (125) | ✅ | 125 rows, all valid |
| JSON SFT rendering (250) | ✅ | 250 rows, all valid |
| JSON SFT rendering (500) | ✅ | 500 rows, all valid |
| JSON SFT rendering (dev) | ✅ | 100 rows, all valid |
| Canonical consistency | ✅ | 0 mismatches across 975 rows |
| Unit coverage | ✅ | All units covered exactly once |
| Target validity | ✅ | 0 illegal targets |
| No markdown/prose | ✅ | 0 occurrences |
| Config 125 | ✅ | References correct files |
| Config 250 | ✅ | References correct files |
| Config 500 | ✅ | References correct files |
| Gold hash unchanged | ✅ | `56e16078...` |
| Unit tests | ✅ | 77/77 OK |
| py_compile (new scripts) | ✅ | render_json_sft_messages.py |
| py_compile (modified scripts) | ✅ | train_lora_router.py, eval_lora_router.py |
| Eval runner JSON support | ✅ | Already supports `unit_json` interface |
| Parser JSON support | ✅ | `_parse_unit_json()` in metrics.py |
| Gold NOT used | ✅ | Rendering uses only train-pool and dev |
| No case labels modified | ✅ | Input cases read-only |
| Train subset nesting | ✅ | 125 ⊂ 250 ⊂ 500 preserved |
| Dev split integrity | ✅ | 100 case IDs unchanged |
| GPU/CUDA pre-check | ⬜ | Run at training time |
| Tokenizer pre-check | ⬜ | Run at training time |

---

## Script Compatibility Audit

### train_lora_router.py

| Check | Result |
|-------|:------:|
| Can train on JSON assistant content? | ✅ SFTTrainer is format-agnostic (chat template only) |
| Preflight rejects JSON assistant? | ✅ No — only checks for markdown, not DSL specifics |
| Preflight log updated for interface? | ✅ Shows `interface_label` in log |
| DSL mode unaffected? | ✅ No changes to DSL path |

### eval_lora_router.py

| Check | Result |
|-------|:------:|
| Supports `--interface unit_json`? | ✅ New `--interface` argument |
| Correct system prompt for JSON? | ✅ Uses `JSON_SYSTEM_PROMPT` when `--interface unit_json` |
| Correct `interface` field in predictions? | ✅ Sets `interface` from args |
| DSL mode unaffected? | ✅ Defaults to `unit_dsl`, same behavior |
| Backward compatible? | ✅ Existing DSL eval commands still work |

### eval_runner.py

| Check | Result |
|-------|:------:|
| Can score `unit_json` predictions? | ✅ `INTERFACE_UNIT_JSON` is natively supported |
| Parser handles JSON output? | ✅ `_parse_unit_json()` handles read/store/skip |
| Metrics computed correctly? | ✅ All metrics work with JSON parsed predictions |

---

## Files Created / Modified

### Created
| File | Purpose |
|------|---------|
| `src/v05/render_json_sft_messages.py` | JSON SFT rendering script |
| `data/v05b/json_sft/v05b_train_125_json_sft_messages.jsonl` | 125-case train SFT |
| `data/v05b/json_sft/v05b_train_250_json_sft_messages.jsonl` | 250-case train SFT |
| `data/v05b/json_sft/v05b_train_500_json_sft_messages.jsonl` | 500-case train SFT |
| `data/v05b/json_sft/v05b_dev_json_sft_messages.jsonl` | Dev SFT (eval loss) |
| `configs/v05b/qwen3_4b_lora_json_125.yaml` | JSON LoRA config 125 |
| `configs/v05b/qwen3_4b_lora_json_250.yaml` | JSON LoRA config 250 |
| `configs/v05b/qwen3_4b_lora_json_500.yaml` | JSON LoRA config 500 |
| `reports/v05b/v05b_unit_json_lora_plan.md` | Experiment plan |
| `reports/v05b/v05b_json_sft_rendering_report.md` | SFT rendering report |
| `reports/v05b/v05b_json_sft_validation_report.md` | SFT validation report |
| `reports/v05b/v05b_json_lora_config_report.md` | Config report |
| `reports/v05b/v05b_train_dev_gold_usage_policy.md` | Data usage policy |
| `reports/v05b/v05b_unit_json_lora_readiness_report.md` | This report |

### Modified
| File | Change |
|------|--------|
| `src/v05/eval_lora_router.py` | Added `--interface` arg, JSON system prompt support |
| `src/v05/train_lora_router.py` | Preflight log now shows interface label |
| `docs/status/CURRENT_STATE.md` | Updated to P5.19-A |

### Preserved (unchanged)
- All `data/v05/**/*` files (train, dev, gold)
- All `src/v04/**/*` files
- `src/v05/render_sft_messages.py`
- `src/v05/check_leakage.py`
- All v0.5 configs
- All v0.5 reports

---

## No Blockers Found

All checks pass. Ready for 125-case smoke training.

---

*End of V0.5b Unit JSON LoRA Readiness Report.*

# v05g BF16 LoRA — Config, Script, and Runbook Final Re-Audit (DeepSeek)

**Date:** 2026-06-05
**Reviewer:** DeepSeek V4 Pro (via Claude Code on Windows)
**Previous Verdict:** CORRECTION REQUIRED (ClaudeCode, 4 blockers)

---

## Verdict

**CORRECTION REQUIRED**

The four previous blockers are resolved. A new critical blocker was discovered: the eval pipeline documented in the runbook cannot function because evaluate_predictions.py is format-incompatible with both the prediction output from eval_lora_router.py and the DecisionCase gold files.

---

## Checks Run

| # | Check | Result |
|---|-------|--------|
| 1 | py_compile train_lora_router.py | ✅ PASS |
| 2 | py_compile eval_lora_router.py | ✅ PASS |
| 3 | py_compile evaluate_predictions.py | ✅ PASS |
| 4 | eval_lora_router.py --help | ✅ PASS — correct args |
| 5 | evaluate_predictions.py --help | ❌ FAIL — pydantic missing |
| 6 | YAML parse all 6 configs | ✅ PASS |
| 7 | v05g data hash verification (6/6) | ✅ PASS |
| 8 | gold_v2_009 hash unchanged | ✅ PASS |
| 9 | run_model_eval.py references | ✅ NONE in active files |
| 10 | base_model_path key match | ✅ PASS |
| 11 | Env var expansion | ✅ PASS |
| 12 | Dev case ID consistency | ✅ PASS — 100/100 overlap |
| 13 | Gradient checkpointing impl | ✅ PASS |
| 14 | Old config backward compat | ✅ PASS |
| 15 | Eval format: predictions to scorer | ❌ BLOCKER — format mismatch |
| 16 | Gold format: DecisionCase to scorer | ❌ BLOCKER — KeyError |

---

## Previous Blocker Resolution

All four original blockers are confirmed resolved:

### Blocker 1: Nonexistent run_model_eval.py ✅ FIXED

- No active file references src/v05/run_model_eval.py.
- All runbook commands reference correct scripts.
- However: the replacement pipeline has a format problem (see Eval Pipeline section).

### Blocker 2: Missing logs/ Directory ✅ FIXED

- Runbook Step 1a includes mkdir -p for all four output directories.
- All tee paths have parent directories created before use.

### Blocker 3: Hardcoded Model Path ✅ FIXED

- Before: base_model_path: /home/abc16/hf_models/Qwen3.5-4B
- After: base_model_path: ""
- _resolve_path() uses os.path.expandvars + os.path.expanduser.
- Runbook includes export QWEN35_MODEL_PATH and test -d guard.

### Blocker 4: Gradient Checkpointing Not Supported ✅ FIXED

- cfg.get("gradient_checkpointing", False) — default false
- When true: model.config.use_cache = False
- When true: model.gradient_checkpointing_enable() called
- PEFT fallback: enable_input_require_grads()
- Passed to TrainingArguments: gradient_checkpointing=gp_checkpointing
- Old configs omit field → defaults to False (backward compat)

---

## Config Key Compatibility

| Aspect | Script | Config (v05g) | Match? |
|--------|--------|---------------|--------|
| Model path key | cfg["base_model_path"] | base_model_path | ✅ |
| Env var expansion | _resolve_path() via expandvars |  | ✅ |
| Quantization mode | cfg.get("quantization", "4bit") | quantization: none | ✅ |
| Gradient ckpt | cfg.get("gradient_checkpointing", False) | Present(4090)/Absent(main) | ✅ |

No base_model (without _path) confusion. Script exclusively uses base_model_path.

---

## A100/L40S Primary Config Audit

Configs: qwen35_bf16_lora_json_r16_500.yaml, qwen35_bf16_lora_json_r16_1000.yaml

| Check | 500 | 1000 | Verdict |
|-------|-----|------|---------|
| quantization: none | ✅ | ✅ | BF16 standard LoRA |
| bf16: true | ✅ | ✅ | |
| No QLoRA fields | ✅ | ✅ | |
| batch_size: 4 | ✅ | ✅ | Appropriate for 40-48GB |
| grad_accum: 4 | ✅ | ✅ | Effective batch = 16 |
| grad_checkpointing absent | ✅ | ✅ | VRAM sufficient |
| optim: adamw_torch | ✅ | ✅ | Correct for BF16 |
| output_dir unique | ..._r16_500 | ..._r16_1000 | ✅ |
| lora_r:16 alpha:32 | ✅ | ✅ | alpha/r = 2 |
| target_modules 6 modules | ✅ | ✅ | Full hybrid coverage |
| max_seq_length: 2048 | ✅ | ✅ | Matches v05c/v05d |
| num_train_epochs: 3 | ✅ | ✅ | |

Estimated peak VRAM: ~32-36 GB. Fits L40S 48GB / A100 40GB.

---

## 4090 Fallback Audit

Configs: qwen35_bf16_lora_json_r16_500_4090.yaml, qwen35_bf16_lora_json_r16_1000_4090.yaml

| Check | 500_4090 | 1000_4090 | Verdict |
|-------|----------|-----------|---------|
| Labeled FALLBACK | ✅ | ✅ | Explicit warning |
| batch_size: 2 | ✅ | ✅ | Reduced for 24GB |
| grad_accum: 8 | ✅ | ✅ | Effective batch = 16 |
| grad_checkpointing: true | ✅ | ✅ | Critical for 24GB |
| output_dir unique (_4090) | ✅ | ✅ | No overwrite |
| All other params identical | ✅ | ✅ | |
| Do NOT use on L40S/A100 | ✅ | ✅ | |

Estimated peak VRAM: ~24-28 GB with gradient checkpointing.

---

## Eval Pipeline Audit — CRITICAL BLOCKER

### Two Incompatible Formats

This project has two different data formats for evaluation:

**Format A: Old Gold Format** (used by evaluate_predictions.py)
- File: data/gold/gold_eval_300.jsonl
- Top-level key: target (read_hints, write_spans, ignore_spans)
- Also has: category at top level
- Used by: Day 6 baseline eval, llm_predict.py, evaluate_predictions.py

**Format B: DecisionCase Format** (used by v05 dev and gold_v2_009)
- Files: v05_dev_cases.jsonl, v05e_gold_v2_009_active_cases.jsonl
- Top-level key: gold (read, store, skip, dsl)
- Has target at top level? NO
- Has category at top level? NO

### Prediction Output Format Mismatch

eval_lora_router.py produces prediction rows WITHOUT a target field.
evaluate_predictions.py line 339 falls back to EMPTY_TARGET when target is missing.
Every prediction silently scores as all zeros. No error, just wrong results.

### Gold File Format Mismatch

evaluate_predictions.py line 208 accesses gold_case["target"].
DecisionCase files have gold, not target. This throws KeyError at runtime.

### Verified Facts

| Fact | Evidence |
|------|----------|
| eval_lora_router.py does NOT output target | Line 107: only raw_output |
| evaluate_predictions.py requires target in predictions | Line 339 |
| evaluate_predictions.py requires target in gold cases | Line 208 |
| DecisionCase files have gold, not target | Verified all v05 dev and v05e gold files |
| Old gold format HAS target | Verified gold_eval_300.jsonl |
| llm_predict.py DOES output target | Calls parse_prediction() internally |
| v05b/c/d used old eval system not evaluate_predictions.py | v05c readiness report |

### Severity: CRITICAL

The eval pipeline cannot produce valid results. Both formats are incompatible.

---

## Dev Dataset Consistency

| Aspect | Training eval_file | Post-training --gold |
|--------|-------------------|---------------------|
| File | v05b_dev_json_sft_messages.jsonl | v05_dev_cases.jsonl |
| Format | SFT messages | DecisionCase |
| Row count | 100 | 100 |
| Case ID overlap | 100/100 ✅ | 100/100 ✅ |

Both files reference the same 100 dev examples. ✅

---

## Dependency Audit

Runbook installs: torch transformers peft trl datasets accelerate bitsandbytes pyyaml pydantic

| Package | Present? |
|---------|----------|
| pydantic (needed for evaluate_predictions.py) | ✅ In main install line |
| bitsandbytes (needed for QLoRA/old configs) | ✅ |
| All other packages | ✅ |

evaluate_predictions.py --help fails without pydantic. Expected — pydantic is installed in Step 0 before eval. Not a blocker.

---

## Gradient Checkpointing Audit

| Requirement | Status |
|-------------|--------|
| Config field read with default False | ✅ |
| model.config.use_cache = False when enabled | ✅ |
| model.gradient_checkpointing_enable() called | ✅ |
| PEFT fallback (enable_input_require_grads) | ✅ |
| Passed to TrainingArguments | ✅ |
| Old configs unaffected (field absent → False) | ✅ |

---

## Hash / Data Protection

- ✅ 6/6 v05g training data hashes match lock
- ✅ gold_v2_009 hash: f5cf7be1d06f085e62b87cf0b9c8021119b54ed94968bb5519b3150995eb4f72
- ✅ No v05g data files modified
- ✅ No gold files modified
- ✅ Old v05c/v05d configs parse and default to quantization=4bit

---

## Runbook Executability

### Training Path — FULLY EXECUTABLE ✅

- export QWEN35_MODEL_PATH + test -d guard ✅
- mkdir -p for all output dirs ✅
- Hash verification step ✅
- tmux train 500 (L40S/A100 + RTX 4090) ✅
- tmux train 1000 (L40S/A100 + RTX 4090) ✅
- OOM recovery, resume strategy, artifact download ✅
- Codex constraints table ✅

### Eval Path — NON-FUNCTIONAL ❌

- eval_lora_router.py commands: correct args, correct files ✅
- evaluate_predictions.py commands: **will crash** with KeyError on DecisionCase gold,
  or produce silently wrong zero-metrics from missing target in predictions ❌

---

## Required Fixes Before Renting Server

### Blocker: Eval Pipeline Format Mismatch

**Fix options (choose one):**

1. **(Recommended) Add a parse step:** Write a script that reads raw predictions,
   calls parse_prediction() from src/v04/metrics.py to convert raw_output to target,
   and converts DecisionCase gold to target format. Feed converted outputs
   to evaluate_predictions.py.

2. **Use old eval system:** Call evaluate_prediction_rows() from src/v04/metrics.py
   directly. This handles raw predictions internally and works with DecisionCase gold.
   Replace the evaluate_predictions.py step entirely.

3. **Modify eval_lora_router.py:** Add parse_prediction() call to output target
   alongside raw_output. Still need gold format converter.

### Minor: Metric Name Mapping

Dev eval plan documents "parse rate", "STORE F1", "SKIP F1".
evaluate_predictions.py computes read_hints, write_spans, write_spans_typed, ignore_spans.
Metric names differ from what is documented. Align before reporting.

---

## Final Recommendation

**Option C: Fix config/script/runbook before server.**

The training pipeline is clean and ready. All four previous blockers are resolved.
The eval pipeline is non-functional due to a format mismatch not caught by the previous
audit. One additional fix (add parse step or switch eval system) is needed before server rental.

---

## Summary

| Area | Verdict |
|------|---------|
| Training script | ✅ Clean |
| v05g main configs (A100/L40S) | ✅ Correct |
| v05g 4090 fallback configs | ✅ Correct |
| Old config backward compat | ✅ Preserved |
| Data integrity | ✅ All hashes match |
| Previous blockers | ✅ All 4 resolved |
| Eval pipeline | ❌ BLOCKER — format mismatch |
| Runbook (training) | ✅ Executable |
| Runbook (eval) | ❌ BLOCKER — will crash/zero |

**Bottom line:** Pi correctly fixed the four original blockers. The training path is
ready. The eval path needs one additional fix: bridging the format gap between
eval_lora_router.py raw predictions and evaluate_predictions.py expected target
format, and between DecisionCase gold files and the old target-keyed gold format.

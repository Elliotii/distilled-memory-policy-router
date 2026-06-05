# v05g BF16 LoRA — Config, Script, and Runbook Independent Review (DeepSeek)

**Date:** 2026-06-05
**Reviewer:** Claude Code / DeepSeek V4 Pro
**Scope:** Config/script/runbook readiness audit — no training, no inference, no gold_v2_009 evaluation

---

## Verdict

**CORRECTION REQUIRED**

Three blockers and one important caveat prevent a clean APPROVE. None involve training data or gold integrity. All are fixable in docs and configs before server rental.

---

## Checks Run

| # | Check | Result |
|---|-------|--------|
| 1 | `py_compile src/v05/train_lora_router.py` | ✅ PASS |
| 2 | YAML parse all 4 configs (v05g×2, v05d, v05c) | ✅ PASS |
| 3 | Config-path existence (train, eval, model) | ✅ 10/10 files exist; 2 missing (`run_model_eval.py`, `logs/`) |
| 4 | Hash verification (6 lock manifest + gold_v2_009) | ✅ 7/7 MATCH |
| 5 | 500-control SFT = v05b canonical SFT (exact copy) | ✅ SHA-256 identical |
| 6 | gold_v2_009 unchanged | ✅ `f5cf7be1...` confirmed |
| 7 | Unit tests | ✅ 77/77 OK (ResourceWarning: unclosed file, cosmetic) |
| 8 | v05c/v05d config backward compatibility | ✅ quantization defaults to "4bit" |
| 9 | `gradient_checkpointing` in training script | ❌ NOT SUPPORTED |
| 10 | `run_model_eval.py` exists | ❌ DOES NOT EXIST |
| 11 | `logs/` directory exists | ❌ MISSING |

---

## Training Script Audit

**File:** `src/v05/train_lora_router.py` (306 lines)
**Status:** PASS with one gap

### Quantization mode dispatch

The script uses a clean two-branch dispatch on `cfg.get("quantization", "4bit")`:

| `quantization` value | Behavior | Correct? |
|---|---|---|
| `"4bit"` (default) | BitsAndBytesConfig, `load_in_4bit=True`, `prepare_model_for_kbit_training` | ✅ |
| `"none"` | `torch.bfloat16`, no BitsAndBytesConfig, no `prepare_model_for_kbit_training` | ✅ |
| Missing (old configs) | Defaults to `"4bit"` — backward compatible | ✅ |

### Specific checks

| # | Requirement | Result |
|---|-------------|--------|
| 1 | quantization: "4bit" for old QLoRA configs | ✅ Default applied when field missing |
| 2 | quantization: "none" for BF16 LoRA | ✅ Branch at line 170 |
| 3 | Default quantization = "4bit" when field missing | ✅ `cfg.get("quantization", "4bit")` |
| 4 | No BitsAndBytesConfig when quantization = "none" | ✅ Skip at line 170 |
| 5 | No prepare_model_for_kbit_training when quantization = "none" | ✅ Skip at line 180-181 |
| 6 | torch_dtype bfloat16 for BF16 LoRA | ✅ Line 175 |
| 7 | LoRA adapter setup still works | ✅ `get_peft_model` called in both branches |
| 8 | Gradient checkpointing behavior | ❌ Not supported — `TrainingArguments` does not include `gradient_checkpointing`, and `model.gradient_checkpointing_enable()` is never called |
| 9 | Old v05c/v05d configs remain behaviorally unchanged | ✅ Verified via YAML parse + default dispatch |

### Optimizer auto-switch

Lines 214-217 implement an auto-switch: when `quant_mode == "none"` and `optim == "adamw_8bit"`, it switches to `adamw_torch` and prints a warning.

- v05g configs explicitly set `optim: adamw_torch` — the auto-switch does NOT trigger (no spurious warning). ✅
- v05c/v05d configs have `optim: adamw_8bit` + no quantization field — defaults to "4bit", auto-switch does NOT trigger. ✅
- If a user creates a BF16 config without `optim: adamw_torch`, the auto-switch saves them. ✅

### Gradient checkpointing gap

**Finding:** The training script has zero support for gradient checkpointing. The `TrainingArguments` constructor (lines 219-242) does not pass `gradient_checkpointing`, and `model.gradient_checkpointing_enable()` is never called.

**Impact:**
- L40S 48GB / A100 40GB: No impact — VRAM is sufficient without gradient checkpointing.
- RTX 4090 24GB: Tier 2 of the OOM fallback plan ("Enable gradient checkpointing") cannot be executed without modifying the training script.

**Severity:** Medium. Not a blocker for L40S/A100 rental, but a blocker for the documented 4090 fallback Tier 2.

**Recommendation:** Add gradient checkpointing support to the training script before server rental if 4090 is a target GPU. At minimum, document that Tier 2 requires a script edit.

---

## Config Audit

**Files:**
- `configs/v05g/qwen35_bf16_lora_json_r16_500.yaml`
- `configs/v05g/qwen35_bf16_lora_json_r16_1000.yaml`
- `configs/v05d/qwen35_lora_json_r16_500.yaml` (comparison)
- `configs/v05c/qwen35_lora_json_500.yaml` (comparison)

**Status:** PASS

### v05g config verification (both configs identical except train_file and output_dir)

| Field | 500 Value | 1000 Value | Correct? |
|-------|-----------|------------|----------|
| `base_model_path` | `/home/abc16/hf_models/Qwen3.5-4B` | Same | ⚠️ hardcoded — adjust for server |
| `output_dir` | `results/v05g_bf16_lora/qwen35_json_r16_500` | `...r16_1000` | ✅ Unique |
| `train_file` | `data/v05g/json_sft/v05g_train_500_control_json_sft_messages.jsonl` | `...1000_targeted...` | ✅ Correct files |
| `eval_file` | `data/v05b/json_sft/v05b_dev_json_sft_messages.jsonl` | Same | ✅ Dev set, exists |
| `interface` | `unit_json` | Same | ✅ |
| `quantization` | `none` | Same | ✅ BF16 mode |
| `lora_r` | 16 | Same | ✅ |
| `lora_alpha` | 32 | Same | ✅ alpha/r = 2 |
| `lora_dropout` | 0.05 | Same | ✅ Same as v05c/v05d |
| `optim` | `adamw_torch` | Same | ✅ Explicit, correct for BF16 |
| `bf16` | `true` | Same | ✅ |
| `fp16` | Not present | Not present | ✅ No fp16 conflict |
| `num_train_epochs` | 3 | Same | ✅ |
| `per_device_train_batch_size` | 4 | Same | ✅ |
| `gradient_accumulation_steps` | 4 | Same | ✅ Effective batch = 16 |
| `max_seq_length` | 2048 | Same | ✅ Matches v05c/v05d |
| `seed` / `data_seed` | 42 | Same | ✅ Reproducible |

### target_modules coverage

Both v05g configs target:
```yaml
- q_proj       # self_attn layers (8 of 32)
- k_proj
- v_proj
- o_proj
- in_proj_qkv  # linear_attn layers (24 of 32)
- out_proj
```

This matches v05d r16 and v05c r8 configs exactly. The 6-module set correctly covers Qwen3.5's hybrid architecture (24 linear_attn + 8 self_attn layers). ✅

### Backward compatibility verified

| Config | `quantization` field | Script behavior | Match prior? |
|--------|---------------------|-----------------|-------------|
| v05c (r=8 QLoRA) | Missing → "4bit" | BitsAndBytes QLoRA | ✅ |
| v05d (r=16 QLoRA) | Missing → "4bit" | BitsAndBytes QLoRA | ✅ |
| v05g (r=16 BF16) | `"none"` | BF16 standard LoRA | N/A (new) |

**No behavioral change for old configs.** ✅

### No accidental QLoRA settings

v05g configs contain no `load_in_4bit`, `bnb_4bit_compute_dtype`, `bnb_4bit_quant_type`, or `bnb_4bit_use_double_quant` fields. ✅

### No gold_v2_009 in training/tuning

Both configs' `train_file` and `eval_file` point to v05g training data and v05b dev data respectively. No gold_v2_009 path appears. ✅

---

## Dev Eval Plan Audit

**Referenced file:** `reports/v05g/v05g_dev_eval_plan.md` and `reports/v05g/v05g_server_training_runbook.md`
**Status:** **CORRECTION REQUIRED**

### Critical finding: `run_model_eval.py` does NOT exist

The runbook (both `reports/v05g/v05g_server_training_runbook.md` and `docs/v05g/V05G_BF16_LORA_SERVER_RUNBOOK.md`) specifies evaluation commands using:

```
python src/v05/run_model_eval.py \
  --adapter results/.../adapter \
  --base_model ... \
  --eval_file ... \
  --output ...
```

**This file does not exist.** There is no `src/v05/run_model_eval.py` anywhere in the repository.

### Actual eval scripts available

| Script | Purpose | Supports unit_json? | Supports adapter loading? |
|--------|---------|---------------------|--------------------------|
| `src/v05/eval_lora_router.py` | Generate predictions from LoRA adapter | ✅ `--interface unit_json` | ✅ `--adapter` + bfloat16 |
| `src/v05/qwen_v05_output_runner.py` | Generate predictions from model (few-shot or base) | Via model | ✅ `--model-path` |
| `src/evaluation/evaluate_predictions.py` | Score predictions against gold cases | Via underlying metrics | N/A (scoring only) |
| `src/v04/metrics.py` | `evaluate_prediction_rows()` — core scoring | ✅ `INTERFACE_UNIT_JSON` | N/A (scoring only) |

### Correct eval pipeline for v05g

The actual two-step pipeline is:

**Step 1 — Generate predictions:**
```bash
python src/v05/eval_lora_router.py \
  --base-model /home/abc16/hf_models/Qwen3.5-4B \
  --adapter results/v05g_bf16_lora/qwen35_json_r16_500/adapter \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --interface unit_json \
  --out data/v05g/model_predictions/bf16_r16_500_dev_predictions.jsonl
```

**Step 2 — Score predictions:**
```bash
python src/evaluation/evaluate_predictions.py \
  --gold data/v05/dev/v05_dev_cases.jsonl \
  --predictions data/v05g/model_predictions/bf16_r16_500_dev_predictions.jsonl \
  --run-id v05g_bf16_r16_500 \
  --split dev \
  --metrics-json results/v05g_bf16_lora/qwen35_json_r16_500/dev_metrics.json \
  --summary-md results/v05g_bf16_lora/qwen35_json_r16_500/dev_summary.md
```

### Runbook command errors (what the runbook says vs reality)

| Runbook field | Runbook value | Actual script | Correct value |
|---------------|--------------|---------------|---------------|
| Script path | `src/v05/run_model_eval.py` | `src/v05/eval_lora_router.py` | `src/v05/eval_lora_router.py` |
| `--eval_file` | SFT messages file | N/A (script uses `--cases`) | `--cases data/v05/dev/v05_dev_cases.jsonl` |
| `--output` | Predictions path | N/A (script uses `--out`) | `--out <predictions.jsonl>` |
| Missing | N/A | `--interface unit_json` | Required for Unit JSON eval |

### Metrics compatibility

The dev eval plan defines 6 primary metrics (parse, full_exact, store_skip_exact, STORE F1, SKIP F1, target_accuracy). The `evaluate_predictions.py` script computes metrics via `src/v04/metrics.py` which supports `INTERFACE_UNIT_JSON`. The metric names may differ slightly (the v04 metrics use legacy span-based naming). Verify metric name mapping before reporting.

### Verdict

The dev eval plan's metric definitions and interpretation guardrails are correct. The runbook's eval commands are wrong — they reference a non-existent script with incorrect argument names. **This must be fixed before server training.**

---

## Hash / Data Integrity Audit

**Lock manifest:** `data/v05g/v05g_training_data_lock.json`
**Status:** PASS

### Lock manifest verification (6/6 MATCH)

| File | Expected SHA-256 (first 32 chars) | Actual SHA-256 (first 32 chars) | Match |
|------|-----------------------------------|----------------------------------|-------|
| `v05g_train_500_control_cases` | `c6ec79d954cd273965de34b8009555e3` | `c6ec79d954cd273965de34b8009555e3` | ✅ |
| `v05g_train_500_control_json_sft` | `d88d34fbeef2d715f5d6b09a8d7f3b48` | `d88d34fbeef2d715f5d6b09a8d7f3b48` | ✅ |
| `v05g_train_additional_500_cases` | `dadc6731060ffd797194b784c2f13c00` | `dadc6731060ffd797194b784c2f13c00` | ✅ |
| `v05g_train_additional_500_json_sft` | `f4297c75605ef35914925b797dd950d5` | `f4297c75605ef35914925b797dd950d5` | ✅ |
| `v05g_train_1000_cases` | `c7b0d94e46bb288ca5977319aa8ea05d` | `c7b0d94e46bb288ca5977319aa8ea05d` | ✅ |
| `v05g_train_1000_json_sft` | `da613fff93b6c730fe45a83bbb4cd6e9` | `da613fff93b6c730fe45a83bbb4cd6e9` | ✅ |

### gold_v2_009 verified

| File | Expected | Actual | Match |
|------|----------|--------|-------|
| `v05e_gold_v2_009_active_cases.jsonl` | `f5cf7be1d06f085e62b87cf0b9c80211...` | `f5cf7be1d06f085e62b87cf0b9c80211...` | ✅ |

### 500-control = v05b canonical (exact byte-for-byte copy)

| File | SHA-256 | Match |
|------|---------|-------|
| `v05b/json_sft/v05b_train_500_json_sft_messages.jsonl` | `d88d34fbeef2d715...` | — |
| `v05g/json_sft/v05g_train_500_control_json_sft_messages.jsonl` | `d88d34fbeef2d715...` | ✅ Identical |

### Config/report hash pinning

| Document | Pins training hashes? | Pins gold hash? |
|----------|----------------------|-----------------|
| `v05g_bf16_lora_config_report.md` | ✅ 6 hashes referenced | ✅ `f5cf7be1...` |
| `v05g_server_training_runbook.md` | ✅ Verification command | ✅ Explicitly pinned |
| `V05G_BF16_LORA_SERVER_RUNBOOK.md` | ✅ Verification command | ✅ Explicitly pinned |
| `V05G_TRAINING_DATA_READINESS.md` | ✅ Refers to lock manifest | ✅ |

### No data modification detected

All 6 lock manifest hashes match current files. No file modification timestamps are more recent than the config-prep date (2026-06-05) for any data file. ✅

---

## Server Resource Plan Audit

**File:** `reports/v05g/v05g_server_resource_plan.md`
**Status:** PASS with one caveat

### VRAM estimates

| Estimate | Claim | Plausible? |
|----------|-------|------------|
| Model params (4B × BF16) | ~8 GB | ✅ Standard |
| Optimizer states (AdamW) | ~16 GB | ✅ 2× model params |
| Gradients | ~8 GB | ✅ 1× model params |
| Activations + LoRA | ~2-4 GB | ✅ Reasonable for seq_len=2048, batch=4 |
| **Total peak** | **~32-36 GB** | ✅ Consistent with components |

**Note:** LoRA adapters are small (~10M params), so the LoRA overhead is negligible. The main VRAM consumer is the base model in BF16 + full AdamW states.

### GPU suitability

| GPU | Plan | Assessment |
|-----|------|------------|
| L40S 48GB | batch_size=4, no grad ckpt needed | ✅ Safe — 36 GB peak vs 48 GB available |
| A100 40GB | batch_size=4 | ✅ Safe but tighter — 36 GB peak vs 40 GB |
| A100 80GB | batch_size=4 | ✅ Overkill but works |
| RTX 4090 24GB | batch_size=2, grad_accum=8 | ⚠️ Tight — ~28 GB estimate vs 24 GB. Gradient checkpointing almost certainly needed, but **not supported in training script** (see Training Script Audit) |
| RTX 3090 24GB | Same as 4090 | ⚠️ Same caveat |

### Batch size / grad accum

All configurations document effective batch size = 16. ✅

- Default: bs=4, ga=4 → effective 16
- 4090 fallback: bs=2, ga=8 → effective 16
- Extreme fallback: bs=1, ga=16 → effective 16

### OOM fallback plan

| Tier | Action | Actionable? |
|------|--------|-------------|
| Tier 1: Reduce batch size | bs=2, ga=8 | ✅ Edit config YAML |
| Tier 2: Gradient checkpointing | `gradient_checkpointing: true` | ❌ **NOT supported in script** |
| Tier 3: Reduce seq_len | `max_seq_length: 1536` | ⚠️ Config field exists but TrainingArguments doesn't pass `max_seq_length` — need to verify if SFTTrainer respects it |
| Tier 4: QLoRA fallback | `quantization: "4bit"` | ✅ Supported by script |

**Critical gap:** Tier 2 cannot be executed without modifying the training script to support gradient checkpointing. The resource plan documents it as a config-only change, which is incorrect.

### Disk requirements

| Item | Claim | Plausible? |
|------|-------|------------|
| Model weights | ~8 GB | ✅ |
| Training data | ~2 MB | ✅ Actual: 1.1 MB (500) + 2.3 MB (1000) |
| Checkpoints (per variant) | ~1.5 GB | ⚠️ May be larger — full model checkpoint in BF16 is ~8 GB, not ~500 MB. LoRA-only adapter saves are ~50-100 MB but checkpoint saves (via `save_strategy: epoch`) save full model+adapter by default. Verify whether SFTTrainer checkpoints save full model or adapter-only. |
| Adapter output | ~50-100 MB | ✅ LoRA weights only |
| **Total disk** | **~12 GB** | ⚠️ May be higher if full-model checkpoints are saved |

### Runtime estimates

| Variant | GPU | Claim | Plausible? |
|---------|-----|-------|------------|
| BF16 r16 500 | L40S/A100 | ~15-25 min | ✅ ~10-15 sec/step × ~94 steps (500/16×3) ≈ 15-25 min |
| BF16 r16 1000 | L40S/A100 | ~30-50 min | ✅ ~2× the 500 variant |
| BF16 r16 500 | 4090 | ~30-45 min | ✅ Slower due to smaller batch |

Runtime estimates are reasonable for planning purposes, though actual throughput depends heavily on sequence length distribution and I/O.

---

## 4090 Fallback Assessment

**Question:** Should the project create explicit 4090 configs now?

**Recommendation:** **Option D — Create explicit 4090 configs before server rental IF 4090 is a realistic target.**

### Analysis

| Factor | L40S/A100 Default | 4090 Needs | In current configs? |
|--------|-------------------|------------|---------------------|
| Batch size | 4 | 2 | ❌ Would need override |
| Grad accum | 4 | 8 | ❌ Would need override |
| Gradient checkpointing | Not needed | **Likely required** | ❌ Not supported in script |
| Optimizer | adamw_torch | adamw_torch | ✅ Same |

### Verdict

If the primary rental target is L40S 48GB or A100 40GB (as recommended in the readiness decision), 4090 configs are **not immediately necessary** — just document the batch size override as a manual edit.

If RTX 4090 24GB is a realistic fallback target, **explicit configs are recommended** because:
1. batch_size and grad_accum differ from defaults
2. gradient checkpointing needs script support first
3. Explicit configs prevent human error during OOM-pressure debugging

**Recommendation:** Either (a) commit to L40S/A100 rental and note 4090 as "requires config edit + script patch," or (b) create explicit 4090 configs AND add gradient checkpointing support to the training script.

---

## Server Runbook Audit

**Files:**
- `reports/v05g/v05g_server_training_runbook.md` (primary)
- `docs/v05g/V05G_BF16_LORA_SERVER_RUNBOOK.md` (summary)

**Status:** **CORRECTION REQUIRED**

### Step-by-step audit

| Step | Content | Status | Issue |
|------|---------|--------|-------|
| 0. Server setup | Environment, repo upload, model path | ⚠️ | Model path is hardcoded to `/home/abc16/hf_models/Qwen3.5-4B` — needs server-side adjustment documented |
| 1a. Data hash verification | Python hash checker | ✅ | Correct; matches lock manifest |
| 1a. Extra: gold_v2_009 | `sha256sum` command | ✅ | Hash matches |
| 1b. Config verification | YAML parse + quantization check | ✅ | Correct |
| 1b. Script compile | `py_compile` command | ✅ | Correct |
| 1c. CUDA availability | `torch.cuda` check | ✅ | Correct |
| 2. Smoke test | Optional, not detailed | ⚠️ | No explicit smoke config or command provided |
| 3. BF16 r16 500 train | tmux + training command | ✅ | Command correct |
| 3. Expected output | Log excerpt | ⚠️ | Shows "Switching optimizer from adamw_8bit to adamw_torch" warning — this warning will NOT appear with current configs (optim is already adamw_torch). Minor inaccuracy. |
| 3. Output locations | Directory tree | ⚠️ | `logs/` subdirectory inside results won't exist unless created |
| 4. BF16 r16 500 eval | **`run_model_eval.py`** | ❌ | **Script does not exist.** Also: `--eval_file` and `--output` are wrong argument names for `eval_lora_router.py`. |
| 5. BF16 r16 1000 train | tmux + training command | ✅ | Command correct |
| 6. BF16 r16 1000 eval | **`run_model_eval.py`** | ❌ | **Same issue as Step 4.** |
| OOM recovery | Tier 1-4 fallback | ⚠️ | Tier 2 (gradient checkpointing) not supported in script |
| Resume strategy | Checkpoint restart | ⚠️ | "use `trainer.train(resume_from_checkpoint=True)` or adjust config" — the current script does not support this; it always trains from scratch |
| Artifact download | tar + scp | ✅ | Correct |
| Codex constraints | Allowed/forbidden table | ✅ | Complete |

### Missing prerequisites

| Item | Status |
|------|--------|
| `logs/` directory | ❌ Does not exist — `tee logs/v05g_bf16_r16_500_train.log` will fail |
| `data/v05g/model_predictions/` directory | ❌ Does not exist — needed for eval predictions |
| Server model path | ⚠️ Hardcoded — needs `export MODEL_PATH=...` or config edit |

### Required runbook fixes

1. **Replace `run_model_eval.py`** with `eval_lora_router.py` + `evaluate_predictions.py` (two-step pipeline).
2. **Fix argument names:** `--cases` not `--eval_file`, `--out` not `--output`, add `--interface unit_json`.
3. **Add `mkdir -p logs`** before the first `tee` command.
4. **Fix expected output** — remove the "Switching optimizer" line (won't appear).
5. **Document model path setup** for server (symlink or config override).
6. **Add resume instructions** — current script doesn't support resume; document that interrupted training must restart from scratch or be modified.

---

## Claim-Boundary Audit

**Files:**
- `reports/v05g/v05g_repaired_training_data_limitations.md`
- `reports/v05g/v05g_bf16_lora_claim_boundaries.md`

**Status:** PASS

### Opus caveats verification

| # | Caveat | Documented? | In which file? |
|---|--------|------------|----------------|
| 1 | READ = entity matching, not semantic relevance reasoning | ✅ | `v05g_repaired_training_data_limitations.md` §1 |
| 2 | Prefix shortcut remains at 6–10 words (90.9% at 3 words, 97.5% at 6 words, 99.6% at 10 words) | ✅ | `v05g_repaired_training_data_limitations.md` §2 |
| 3 | project_memory READ = 0% in additional 500 (mitigated by 500-control at 89.7%) | ✅ | `v05g_repaired_training_data_limitations.md` §3 |
| 4 | 1000-vs-500 is data volume + broader domains/templates, not pure data-size causality | ✅ | `v05g_repaired_training_data_limitations.md` §4 |
| 5 | No downstream utility / deployment claim | ✅ | `v05g_repaired_training_data_limitations.md` §6; `v05g_bf16_lora_claim_boundaries.md` FORBIDDEN table |

### SAFE claims properly bounded

| Claim | Requirements documented? | Conditional? |
|-------|--------------------------|-------------|
| C1: BF16 vs QLoRA precision comparison | ✅ Same seed data, same hyperparams, same epochs | No |
| C2: Targeted data scaling | ✅ Acknowledge confound, no pure-volume causality | No |
| C3: Structural quality | ✅ 9/9 gates pass | No |
| C4: Semantic improvements | ✅ Specific metrics cited | No |

### FORBIDDEN claims properly listed

All 8 forbidden claims are documented with reasons. The gold_v2_009 usage rule (single final evaluation only) is clear and repeated across multiple documents. ✅

---

## Required Fixes Before Renting Server

### Blocker 1: Fix eval commands in runbook (MUST FIX)

**Files to update:**
- `reports/v05g/v05g_server_training_runbook.md` — Steps 4 and 6
- `docs/v05g/V05G_BF16_LORA_SERVER_RUNBOOK.md` — Dev Evaluation section

**Action:** Replace all references to `src/v05/run_model_eval.py` with the correct two-step pipeline using `src/v05/eval_lora_router.py` + `src/evaluation/evaluate_predictions.py`, with correct argument names.

### Blocker 2: Create `logs/` directory or add `mkdir -p logs` to runbook (MUST FIX)

The runbook uses `tee logs/v05g_bf16_r16_500_train.log` but the `logs/` directory does not exist. Add `mkdir -p logs` to the setup step.

### Blocker 3: Document model path configuration for server (MUST FIX)

All configs hardcode `/home/abc16/hf_models/Qwen3.5-4B`. The runbook should document:
- How to symlink or download the model on the server
- Alternative: override via environment variable (if script is updated to support it)
- Or: edit config files on server after upload

### Important: Add gradient checkpointing support to training script (SHOULD FIX)

If RTX 4090 is a target GPU, add to `train_lora_router.py`:
```python
# In TrainingArguments:
gradient_checkpointing=cfg.get("gradient_checkpointing", False),

# After get_peft_model:
if cfg.get("gradient_checkpointing", False):
    model.gradient_checkpointing_enable()
```

And add `gradient_checkpointing: true` to 4090 configs.

### Minor: Fix expected output in runbook

The runbook shows "⚠ Switching optimizer from adamw_8bit to adamw_torch" in expected output. This warning won't appear because the v05g configs explicitly set `optim: adamw_torch`. Remove this line from the expected output.

### Minor: Fix runbook resume strategy

The current script always trains from scratch. Either document this honestly ("restart training from scratch if interrupted") or add resume support to the script.

### Minor: Verify checkpoint disk usage

Check whether SFTTrainer with `save_strategy: epoch` saves full model checkpoints (~8 GB each) or adapter-only checkpoints (~50-100 MB each). Update disk estimates accordingly.

---

## Final Recommendation

**Option C — Fix configs/script/docs before server.**

Specifically:

1. **MUST FIX:** Replace `run_model_eval.py` references in runbooks with the correct two-step eval pipeline (`eval_lora_router.py` + `evaluate_predictions.py`).
2. **MUST FIX:** Add `mkdir -p logs` to runbook setup step.
3. **MUST FIX:** Document model path setup for server (hardcoded path won't work on rental).
4. **SHOULD FIX:** Add gradient checkpointing support to the training script (required for 4090 Tier 2 fallback).
5. **SHOULD FIX:** Create explicit 4090 configs IF 4090 is a target GPU; otherwise, commit to L40S/A100 and document the 4090 gap.
6. **NICE TO FIX:** Fix expected output in runbook, document resume limitations, verify checkpoint disk usage.

**Estimated fix time:** 30-60 minutes (docs-only changes).

After fixes are applied, the recommendation upgrades to **Option A — Ready to rent server and execute runbook** for L40S 48GB or A100 40GB targets.

---

## Summary

| Audit Section | Verdict |
|---------------|---------|
| Training script compatibility | PASS (gradient checkpointing gap noted) |
| Config audit (v05g × 2) | PASS |
| Backward compatibility (v05c, v05d) | PASS |
| Dev eval plan | CORRECTION REQUIRED (script doesn't exist) |
| Hash / data integrity | PASS (7/7 MATCH) |
| Server resource plan | PASS (gradient checkpointing gap noted) |
| 4090 fallback assessment | EXPLICIT CONFIGS RECOMMENDED |
| Server runbook | CORRECTION REQUIRED (eval commands, missing dirs) |
| Claim boundaries | PASS |
| Non-model tests | PASS (77/77 unit tests, py_compile, YAML parse, hash verify) |

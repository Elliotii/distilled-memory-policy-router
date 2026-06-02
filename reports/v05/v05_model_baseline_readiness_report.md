# V0.5 Model Baseline Readiness Report

**Date:** 2026-06-02  
**Context:** 5.4-A — model baseline readiness and environment check  

---

## 1. Environment Summary

| Component | Version / Status |
|-----------|-----------------|
| OS | WSL (Ubuntu) |
| Python | 3.12.3 |
| PyTorch | 2.6.0+cu124 |
| CUDA | 12.4 |
| transformers | 4.x (installed) |

## 2. GPU Summary

| Property | Value |
|----------|-------|
| GPU | NVIDIA GeForce RTX 4070 SUPER |
| VRAM | 11 GB |
| CUDA available | ✅ Yes |
| GPU count | 1 |

## 3. Python / Torch / Transformers

| Package | Status |
|---------|:------:|
| torch 2.6.0+cu124 | ✅ Installed |
| transformers | ✅ Installed |
| PEFT / TRL | ⚠ Not confirmed (needed for LoRA) |
| accelerate / bitsandbytes | ⚠ Not confirmed (needed for training) |

**Recommendation:** Verify PEFT, TRL, accelerate, bitsandbytes availability before LoRA training context.

## 4. Local Model Inventory

| Model | Path | Size | Status |
|-------|------|:----:|:------:|
| Qwen3-4B-Instruct-2507 | `/home/abc16/hf_models/Qwen3-4B-Instruct-2507` | 7.6 GB | ✅ Ready |
| Qwen3.5-4B | `/home/abc16/hf_models/Qwen3.5-4B` | N/A | ❌ Not present |

## 5. Qwen3-4B Status

| Check | Result |
|-------|:------:|
| Model files present | ✅ (3 safetensors, config, tokenizer) |
| VRAM fit (11 GB) | ✅ ~8 GB load, sufficient headroom |
| Existing runner | ✅ `src/v04/qwen_local_output_runner.py` |
| Runner v0.5 compatibility | ⚠ Needs v0.5 prompt templates and few-shot support |
| Previous smoke runs | ✅ Subset50 and smoke cases successfully run |

## 6. Qwen3.5 Local Status

| Check | Result |
|-------|:------:|
| Local presence | ❌ Not downloaded |
| HF Hub model ID | `Qwen/Qwen3.5-4B` (tentative) |
| Download needed | Yes |
| Estimated disk | ~8 GB |
| Impact on Qwen3-4B | None (separate directory) |

## 7. Locked Gold Hash Verification

| File | Expected SHA-256 | Actual SHA-256 | Match |
|------|------------------|----------------|:-----:|
| Combined | `56e16078...2173d` | `56e16078...2173d` | ✅ |
| Core | `9acdd6a7...8db2` | `9acdd6a7...8db2` | ✅ |
| Hard | `5f4a5d55...19b2` | `5f4a5d55...19b2` | ✅ |
| SFT | `d9f215af...5c22` | `d9f215af...5c22` | ✅ |

All locked gold hashes verified against `v05_gold_lock.json`. Gold is intact and unchanged.

## 8. Data Line Counts

| File | Lines | Expected |
|------|:-----:|:--------:|
| train-pool (corrected batch500) | 500 | 500 ✅ |
| dev | 100 | 100 ✅ |
| locked gold | 100 | 100 ✅ |
| **Total** | **700** | |

## 9. Existing Runner Compatibility

### `src/v04/qwen_local_output_runner.py`

| Capability | v0.4 Status | v0.5 Needs |
|------------|:-----------:|------------|
| Local model load | ✅ | Same |
| 3 interfaces (legacy_span_json, unit_json, unit_dsl) | ✅ | Unit DSL + Unit JSON |
| 5-case smoke | ✅ | Need 100-case batch |
| Generic case loader | ❌ (subset50 only) | Need `--cases` flag |
| Few-shot mode | ❌ | Need 3-example injection |
| Split awareness | ❌ | Need `--split dev/gold` |
| Prediction JSONL | ✅ | Same format |
| Qwen3.5 support | N/A | Need `--model-path` flag |

### `src/v04/eval_runner.py`

| Capability | Status |
|------------|:------:|
| Prediction evaluation | ✅ |
| All v0.4 metrics | ✅ |
| Report generation | ✅ |
| v0.5 compatibility | ✅ (same prediction format) |

## 10. Blockers

| Blocker | Severity | Resolution |
|---------|:--------:|------------|
| Qwen3.5 not downloaded | Medium | Download in 5.4-B or defer |
| v0.5 prompt templates needed | Low | Create before first baseline run |
| Few-shot injection logic | Low | Implement in runner or pre-render |
| PEFT/TRL availability unknown | Low | Check before LoRA context |

**No hard blockers for immediate Qwen3-4B baseline work.**

## 11. Recommended Next Context

**Context 5.4-B: Qwen3.5 acquisition + 5-case local smoke**

If Qwen3.5 is wanted:
1. Download Qwen3.5-4B to local hf_models
2. Create v0.5 prompt templates
3. Run 5-case dev smoke for Qwen3-4B (DSL zero-shot, few-shot, JSON)
4. Run 5-case dev smoke for Qwen3.5 (same interfaces)
5. Compare parse success, latency, VRAM
6. Choose primary model for full dev baseline

If Qwen3.5 is deferred:
1. Skip download
2. Create v0.5 prompt templates
3. Run 5-case dev smoke for Qwen3-4B only
4. Proceed to full dev baseline (Context 5.4-C)

---

*End of V0.5 Model Baseline Readiness Report.*

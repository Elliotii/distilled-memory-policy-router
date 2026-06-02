# V0.5 Qwen3.5 Acquisition Plan

Version: v0.5
Date: 2026-06-02
Status: Planning — Qwen3.5 same-tier baseline acquisition
Context: 5.4-A

---

## 1. Local Status

| Check | Result |
|-------|:------:|
| Qwen3-4B-Instruct-2507 | ✅ Present (7.6 GB) |
| Qwen3.5-4B | ❌ Not present |
| Disk space in hf_models | Check before download |
| VRAM (RTX 4070 SUPER) | 11 GB |

**Qwen3.5 must be downloaded** before it can be used as a baseline.

## 2. Candidate Model ID

| Property | Value |
|----------|-------|
| Model ID | `Qwen/Qwen3.5-4B` (or `Qwen/Qwen3.5-4B-Instruct` if instruction-tuned) |
| Architecture | Qwen3.5, 4B parameters |
| Expected disk | ~8 GB (similar to Qwen3-4B) |
| Expected VRAM | ~8-9 GB (should fit RTX 4070 SUPER 11GB) |

**Note:** The exact model ID should be confirmed. Qwen3.5 may be released as:
- `Qwen/Qwen3.5-4B` (base)
- `Qwen/Qwen3.5-4B-Instruct` (instruction-tuned — preferred for our task)

User should confirm the correct ID. If neither is available, Qwen3-4B alone is sufficient for the primary experiment.

## 3. Download Plan

### 3.1 Command (do NOT execute in this context)

```bash
# Option A: Direct download
huggingface-cli download Qwen/Qwen3.5-4B-Instruct \
  --local-dir /home/abc16/hf_models/Qwen3.5-4B \
  --local-dir-use-symlinks False

# Option B: With HF mirror (if needed)
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download Qwen/Qwen3.5-4B-Instruct \
  --local-dir /home/abc16/hf_models/Qwen3.5-4B \
  --local-dir-use-symlinks False
```

### 3.2 Precautions

- Do NOT overwrite Qwen3-4B in `/home/abc16/hf_models/Qwen3-4B-Instruct-2507`
- Verify disk space before download (~10 GB free needed for download + extraction)
- Download to separate directory: `/home/abc16/hf_models/Qwen3.5-4B`
- After download, set `local_files_only=True` for all inference

## 4. Compatibility Checks

After download, verify:

### 4.1 Software Compatibility

```python
import torch, transformers
# Check transformers version supports Qwen3.5
# Current: transformers 4.x (verify Qwen3.5 support)
```

| Check | Method |
|-------|--------|
| transformers version | `transformers.__version__` |
| Qwen3.5 config load | `AutoConfig.from_pretrained(local_path)` |
| Tokenizer chat template | `tokenizer.apply_chat_template(...)` |
| enable_thinking behavior | Test with enable_thinking=False |

### 4.2 Hardware Compatibility

| Check | Expected |
|-------|----------|
| Model size | ~8 GB on disk |
| VRAM at load | ~8-9 GB |
| VRAM headroom | ~2-3 GB for KV cache |
| Inference latency | Comparable to Qwen3-4B |

## 5. Smoke Test Plan

### 5.1 5-Case Dev Smoke (After Download)

```
Purpose: Verify Qwen3.5 works locally before full dev baseline run.
Cases: 5 dev cases (3 interfaces if feasible).
Interfaces: Unit DSL zero-shot, Unit DSL few-shot, Unit JSON zero-shot.
Split: dev only — do NOT use gold.
```

### 5.2 Comparison Against Qwen3-4B Smoke

| Metric | Check |
|--------|-------|
| parse_success | Compare with Qwen3-4B |
| empty output rate | Must be low |
| latency per case | Compare with Qwen3-4B |
| VRAM peak | Must fit 11 GB |
| output format | Valid DSL / JSON |

## 6. Go / No-Go Decision

After smoke test, decide:

| Decision | Criteria |
|----------|----------|
| **Go** | parse_success ≥ 80%, VRAM fits, DSL format correct, latency acceptable |
| **No-Go** | crashes, OOM, parse_success < 50%, incompatible API |

If No-Go: Fall back to Qwen3-4B as sole model baseline. Qwen3.5 is a bonus comparison, not a requirement.

## 7. Risk: Thinking Mode API Change

Qwen3.5 may change the `enable_thinking` API:
- Qwen3 uses `enable_thinking=False` in `generate()` kwargs
- Qwen3.5 may use a different mechanism or remove it entirely
- **Mitigation:** Test with and without the flag; compare output quality

## 8. Fallback Plan

If Qwen3.5 cannot be acquired or does not work:

1. Run all baselines with Qwen3-4B only
2. Document that Qwen3.5 comparison was not possible due to [reason]
3. Qwen3-4B LoRA remains the primary experiment
4. Qwen3.5 comparison can be a future experiment

---

*End of V0.5 Qwen3.5 Acquisition Plan.*

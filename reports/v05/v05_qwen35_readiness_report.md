# V0.5 Qwen3.5 Readiness Report

**Date:** 2026-06-02  
**Context:** 5.4-A — readiness assessment for Qwen3.5 same-tier baseline  

---

## 1. Candidate Model ID

| Property | Value |
|----------|-------|
| Tentative model ID | `Qwen/Qwen3.5-4B` or `Qwen/Qwen3.5-4B-Instruct` |
| Architecture family | Qwen3.5 |
| Parameter count | ~4B |
| Local path | `/home/abc16/hf_models/Qwen3.5-4B` |

**Note:** Exact model ID must be confirmed. Qwen3.5 may use a different naming convention than Qwen3. The instruction-tuned variant is preferred for our routing task.

## 2. Local Presence

| Check | Result |
|-------|:------:|
| `/home/abc16/hf_models/Qwen3.5-4B` | ❌ Does not exist |
| Any Qwen3.5 in hf_models | ❌ None found |
| Download needed | ✅ Yes |

## 3. Download Needed

### Download Command (do NOT execute in this context)

```bash
# Create directory and download
mkdir -p /home/abc16/hf_models/Qwen3.5-4B

# Option A: Direct
huggingface-cli download Qwen/Qwen3.5-4B-Instruct \
  --local-dir /home/abc16/hf_models/Qwen3.5-4B \
  --local-dir-use-symlinks False

# Option B: With HF mirror
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download \
  Qwen/Qwen3.5-4B-Instruct \
  --local-dir /home/abc16/hf_models/Qwen3.5-4B \
  --local-dir-use-symlinks False
```

## 4. Disk / VRAM Considerations

| Resource | Status | Notes |
|----------|:------:|-------|
| GPU VRAM | 11 GB | Qwen3-4B uses ~8 GB. Expect Qwen3.5 similar or slightly more |
| Disk (hf_models) | Check `df -h` | ~10 GB free recommended for download + extraction |
| Existing Qwen3-4B | 7.6 GB | Must NOT be overwritten |
| Qwen3.5 expected | ~8 GB | Separate directory |

**VRAM headroom:** 11 GB - 8 GB (model) ≈ 3 GB for KV cache and runtime. Borderline but should work for batch_size=1 inference. For LoRA training, 4-bit quantization (QLoRA) may be needed for 11GB GPU.

## 5. Compatibility Risks

| Risk | Severity | Check |
|------|:--------:|-------|
| enable_thinking API change | Medium | Test smoke with and without flag |
| Chat template differences | Low | Compare tokenizer.apply_chat_template output |
| Tokenizer changes | Low | Verify special tokens match prompt format |
| transformers version | Low | May need transformers upgrade for Qwen3.5 |
| Model architecture change | Medium | May need new AutoConfig handling |

## 6. Proposed Next-Step Command

**Do NOT execute download in this context.**

The download should happen in Context 5.4-B:

```bash
# Step 1: Check disk space
df -h /home/abc16/hf_models

# Step 2: Download Qwen3.5-4B-Instruct
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download \
  Qwen/Qwen3.5-4B-Instruct \
  --local-dir /home/abc16/hf_models/Qwen3.5-4B \
  --local-dir-use-symlinks False

# Step 3: Verify
ls -la /home/abc16/hf_models/Qwen3.5-4B/
du -sh /home/abc16/hf_models/Qwen3.5-4B/

# Step 4: Smoke test
PYTHONDONTWRITEBYTECODE=1 python -m src.v04.qwen_local_output_runner \
  --model-path /home/abc16/hf_models/Qwen3.5-4B \
  --cases data/v05/dev/v05_dev_cases.jsonl \
  --limit 5 \
  --interface unit_dsl
```

## 7. Fallback: Qwen3-4B Only

If Qwen3.5 cannot be acquired (model not released, download fails, incompatibility):
- Qwen3-4B is sufficient for the primary experiment
- Qwen3.5 comparison is a bonus, not a requirement
- All baselines and LoRA experiments run on Qwen3-4B
- Document Qwen3.5 unavailability in final report

---

*End of V0.5 Qwen3.5 Readiness Report.*

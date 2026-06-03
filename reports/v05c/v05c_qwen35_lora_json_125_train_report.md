# V0.5c Qwen3.5 JSON LoRA 125 Training Report

**Date:** 2026-06-03  
**Context:** 5.9-B — Qwen3.5 Unit JSON LoRA 125 smoke training  

---

## 1. Preflight

| Check | Result |
|-------|:------:|
| Config exists | ✅ |
| Base model exists | ✅ (`/home/abc16/hf_models/Qwen3.5-4B`) |
| Train file exists (125 rows) | ✅ |
| Eval file exists (100 rows) | ✅ |
| Assistant JSON parse | ✅ 125/125 (100%) |
| No markdown in assistant | ✅ |
| No gold in config | ✅ |
| CUDA available | ✅ RTX 4070 SUPER, 11GB |
| Output dir clear | ✅ |
| Target modules (6) | ✅ q_proj, k_proj, v_proj, o_proj, in_proj_qkv, out_proj |
| Gold hash unchanged | ✅ `56e16078...` |

**Preflight: PASSED**

## 2. Blocker: Qwen2VLImageProcessor ImportError

**Issue:** TRL SFTTrainer auto-detects Qwen3.5 as a multimodal model and tries to load `Qwen2VLImageProcessor`, which requires `pillow` and `torchvision`.

**Fix:** Installed `pillow`. Added `processing_class=tokenizer` to SFTTrainer constructor to bypass AutoProcessor.

**Script change:** `src/v05/train_lora_router.py` — one line added.

## 3. Training Summary

| Metric | Value |
|--------|-------|
| Base model | Qwen3.5-4B |
| Train cases | 125 |
| Dev cases | 100 |
| LoRA rank | r=8, alpha=16 |
| Trainable params | 4,915,200 (0.12% of 4.2B) |
| Duration | 903s (~15 min) |
| OOM | No |
| NaN | No |
| Adapter saved | ✅ `results/v05c_lora/qwen35_json_125/adapter/` |

## 4. Training Progress

| Epoch | Train Loss | Eval Loss | Token Accuracy |
|:-----:|:----------:|:---------:|:--------------:|
| 1 | 1.717 | 1.264 | 72.2% |
| 2 | 0.764 | 0.626 | 85.7% |
| 3 | — | **0.544** | **86.9%** |

Strong convergence across all 3 epochs. No overfitting signs — eval loss steadily decreasing.

## 5. Eval Fix: enable_thinking=False

**Issue:** Qwen3.5's chat template adds `<think>\n` before the assistant turn when `add_generation_prompt=True`. Without `enable_thinking=False`, the model generates verbose reasoning prose (1000+ chars) instead of JSON, causing 0% parse success.

**Fix:** Added `enable_thinking=False` to `tokenizer.apply_chat_template()` in eval script. After fix, model outputs pure JSON directly.

**Script change:** `src/v05/eval_lora_router.py` — one kwarg added, plus incremental write support.

## 6. Training Loss Curve Interpretation

- Epoch 1 eval loss (1.264) is high — model adjusting to JSON format
- Epoch 2 eval loss (0.626) — dramatic improvement, ~50% reduction
- Epoch 3 eval loss (0.544) — continued improvement, approaching convergence
- Token accuracy reaches 86.9% by epoch 3

Compared to Qwen3-4B JSON LoRA 125:
- Qwen3-4B: eval_loss 1.919→1.424→1.300, token_acc 72.7%→85.5%→86.5%
- Qwen3.5: eval_loss 1.264→0.626→0.544, token_acc 72.2%→85.7%→86.9%
- Qwen3.5 converges to lower loss (0.544 vs 1.300) with similar token accuracy

**Qwen3.5 learns the JSON format faster and achieves much lower eval loss** — consistent with a stronger base model.

---

*End of V0.5c Qwen3.5 JSON LoRA 125 Training Report.*

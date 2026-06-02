# V0.5 Qwen3.5 Acquisition Report

**Date:** 2026-06-02  
**Context:** 5.4-B — Qwen3.5 download and smoke preparation  

---

## 1. Local Presence Before Download

| Check | Result |
|-------|:------:|
| Qwen3.5 in `/home/abc16/hf_models/` | ❌ Not present |
| Only model present | Qwen3-4B-Instruct-2507 (7.6 GB) |

## 2. Chosen Model ID

| Property | Value |
|----------|-------|
| Model ID | `Qwen/Qwen3.5-4B` |
| Download source | HF Mirror (`https://hf-mirror.com`) |
| Reason | Same-tier 4B architecture for fair comparison with Qwen3-4B |

## 3. Download Command Used

```bash
HF_ENDPOINT=https://hf-mirror.com hf download Qwen/Qwen3.5-4B \
  --local-dir /home/abc16/hf_models/Qwen3.5-4B
```

First attempt used `--local-dir-use-symlinks False` which is not a valid flag for this version of `hf`. Second attempt without it succeeded.

## 4. Local Path After Download

| Property | Value |
|----------|-------|
| Path | `/home/abc16/hf_models/Qwen3.5-4B` |
| Total size | 8.8 GB |
| Safetensors | 2 files (5.0 GB + 3.8 GB) |
| Config | `config.json`, `tokenizer.json`, `tokenizer_config.json` present |
| Chat template | `chat_template.jinja` present |

## 5. Config / Tokenizer Presence

| File | Present |
|------|:-------:|
| config.json | ✅ |
| tokenizer.json | ✅ (12.8 MB) |
| tokenizer_config.json | ✅ |
| vocab.json | ✅ (6.7 MB) |
| merges.txt | ✅ (3.4 MB) |
| model.safetensors.index.json | ✅ |
| model-00001-of-00002.safetensors | ✅ (5.0 GB) |
| model-00002-of-00002.safetensors | ✅ (3.8 GB) |
| chat_template.jinja | ✅ |
| preprocessor_config.json | ✅ |
| video_preprocessor_config.json | ✅ |

## 6. Any Errors

| Issue | Resolution |
|-------|------------|
| First download attempt timed out (partial download) | Restarted, completed successfully |
| Flash-linear-attention not installed | Warning only — falls back to torch implementation |
| `enable_thinking` not supported | Removed from generate kwargs |
| `temperature` deprecated warning | Warning only — non-blocking |

## 7. Smoke Test Status

| Check | Result |
|-------|:------:|
| Model loaded successfully | ✅ |
| Tokenizer loaded | ✅ |
| 5 case × 4 interfaces = 20 predictions | ✅ |
| No errors / crashes | ✅ |
| No empty outputs | ✅ |
| Latency | ~15-20s per case (much slower than Qwen3-4B's ~0.5s) |
| Output quality | ❌ Verbose thinking prose, not parseable DSL/JSON |

**Qwen3.5 produces verbose "thinking" text instead of the requested DSL/JSON format.** This is a prompt engineering issue, not a model defect. The prompt templates may need adjustment for Qwen3.5 (e.g., explicit "do not think" instruction, different chat template approach).

## 8. VRAM / Performance

| Metric | Qwen3-4B | Qwen3.5-4B |
|--------|:--------:|:----------:|
| Model size (disk) | 7.6 GB | 8.8 GB |
| Load time | ~3s | ~3s |
| Per-case latency | ~0.5s | ~19s |
| Output chars | 30-86 | 1891-2421 |
| Parse success | Variable | 0% |

## 9. Recommendation

Qwen3.5-4B is successfully acquired and technically functional (loads, runs, no crashes). However, **output format is completely wrong** — the model engages in thinking/analysis rather than producing DSL.

**Before Qwen3.5 can be used as a baseline:**
1. Fix prompt template to suppress thinking mode
2. Test with structured system+user message format
3. Verify DSL output on 5-case smoke after prompt fix
4. If prompt fixes don't work, Qwen3.5 may be unsuitable for DSL-based routing

**Fallback:** Qwen3-4B remains the primary baseline model. Qwen3.5 is a bonus if prompt issues can be resolved.

---

*End of V0.5 Qwen3.5 Acquisition Report.*

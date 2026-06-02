# V0.5 Training Plan

Version: v0.5 draft  
Date: 2026-06-01  
Status: Planning; no training executed yet  

## 1. v0.5 Goal

Train a Qwen3-4B small memory policy router that, given fixed candidate memories and pre-segmented current units, outputs Unit DSL predicting:

- **READ**: which candidate memories to inject into context
- **STORE**: which current units to enter the durable memory pipeline, and to which target
- **SKIP**: which current units to ignore

The trained router should improve over few-shot baseline on routing-specific metrics while maintaining high structural parse success.

## 2. Main Hypothesis

**LoRA/SFT can lift Qwen3-4B from few-shot prompt-following to more stable DSL policy routing.**

Specifically, training should improve:
- Exact match rate
- STORE unit F1 (especially recall — reducing missed STORE)
- STORE target accuracy (especially `project_memory` vs `task_state`)
- SKIP F1
- False store rate
- Irrelevant read rate

While preserving:
- High parse success (target: ≥ 96%)
- 0% sensitive store
- Short output, low latency

## 3. Model

**Primary:**
- Model: Qwen3-4B-Instruct-2507
- Local path: `/home/abc16/hf_models/Qwen3-4B-Instruct-2507`
- Size: 7.6 GB on disk, ~7.5 GB VRAM at bfloat16
- Training method: LoRA / QLoRA

**Optional challenger (not blocking v0.5):**
- Qwen3.5 same-tier model
- Only after core v0.5 plan and results are stable
- Purpose: test whether target accuracy gap closes with model size

**Hard fallback (if 4B cannot converge):**
- Unit JSON interface as alternative training target
- Only if DSL training consistently underperforms Unit JSON zero-shot baseline

## 4. Interface

**Primary output: Unit DSL**

```
READ m1,m2
STORE service_memory u1
STORE repo_memory u2
SKIP u3
```

**Canonical consumption:**
- Strict parser (`src/v04/parser.py`) → canonical JSON
- Parser does not do semantic repair
- Invalid outputs scored as parse failure in eval

**Baselines for comparison:**
| Baseline | Description |
| --- | --- |
| `empty/no-action` | READ none, STORE none, SKIP all |
| `top-k READ` | READ first K candidate memories, STORE none |
| `heuristic` | Deterministic lexical baseline |
| DeepSeek V4 Flash-compatible | Strong teacher baseline |
| Qwen3-4B zero-shot Unit DSL | Zero-shot prompt baseline |
| Qwen3-4B few-shot Unit DSL | 3-example few-shot baseline |
| Qwen3-4B Unit JSON zero-shot | Alternative interface baseline |
| **Qwen3-4B LoRA Unit DSL** | **Training target** |

## 5. Training Method

**Approach:**
- LoRA (Low-Rank Adaptation) via Hugging Face PEFT
- Supervised fine-tuning (SFT)
- No RLHF, no DPO, no reward modeling

**Frameworks:**
- PyTorch + Hugging Face Transformers
- PEFT (LoRA)
- Optional: bitsandbytes for QLoRA if VRAM constrained (though 7.5 GB within 12 GB budget)
- Accelerate for device management

**Training data format:**
- Chat-style messages (system + user + assistant)
- Assistant output = Unit DSL only
- Defined in `docs/v05/V05_SFT_FORMAT.md`

**Training configuration (proposed):**
- LoRA rank: 8–16 (to be tuned)
- LoRA alpha: 16–32
- Target modules: q_proj, v_proj (and optionally k_proj, o_proj)
- Learning rate: 1e-4 to 5e-4
- Batch size: 4–8 (GPU memory permitting)
- Epochs: 3–5
- Optimizer: AdamW
- LR scheduler: linear with warmup

**What is NOT trained:**
- Retriever
- Writer / memory updater
- Memory lifecycle operations (ADD/UPDATE/DELETE/MERGE)
- Entity resolution
- LLM unitizer
- Any MemoryOS component

## 6. Evaluation

**Use existing eval_runner (`src/v04/eval_runner.py`):**

Structural metrics:
- Parse success rate
- Invalid memory ID rate
- Invalid unit ID rate
- Invalid target rate
- Output length (chars, lines)

Semantic routing metrics:
- Exact match rate
- READ precision / recall / F1
- STORE unit precision / recall / F1
- STORE target accuracy
- SKIP precision / recall / F1
- False store rate
- Irrelevant read rate
- Sensitive store rate

**Evaluation datasets:**
- Dev set: used during training for early stopping / checkpoint selection
- Gold set: locked, never seen during training, used only for final evaluation

**Comparison:**
- Trained router vs all baselines on gold set
- Report both aggregate metrics and per-category breakdown (by tag, target, case shape)

## 7. Go / No-Go Criteria

### Go (proceed to v1.0 packaging) if trained DSL router:
- **Improves over few-shot** on exact match, STORE F1, and STORE target accuracy
- **Reduces false store** and **irrelevant read** vs few-shot
- **Maintains parse success ≥ 96%** (acceptable structural tradeoff)
- **Maintains 0% sensitive store**
- **Beats Unit JSON zero-shot** on routing metrics
- **Shows no target collapse** (e.g., all predictions defaulting to `task_state`)

### No-Go (reassess) if:
- Training only lowers loss but does **not improve routing metrics** (exact, F1, accuracy)
- **Target confusion worsens** (e.g., `project_memory` accuracy drops)
- **Sensitive store appears** (model starts storing private data)
- Model **overfits train** and fails dev/gold by large margins
- **Unit JSON baseline remains clearly better** on multiple metrics
- VRAM or compute constraints make training impractical

### Partial-Go:
- Training improves some metrics but not others → analyze, report, iterate
- Consider prompt-v2, more data, or interface fallback before calling No-Go

## 8. Scope Boundaries

This is a **memory policy router only.** The following are explicitly out of scope for v0.5:

- MemoryOS (complete memory system)
- Real retriever (BM25, vector DB, RRF)
- Memory database
- Intelligent memory writer (canonical rewrite)
- ADD / UPDATE / DELETE / MERGE operations
- Entity resolution
- LLM unitizer
- SOP / skill system
- Complete downstream agent benchmark
- New STORE targets (only the 5 existing targets)
- Confidence scores, reasons, or entity fields
- Multi-turn memory tracking (single-turn router only)

## 9. Timeline (Proposed)

| Phase | Context | Description |
| --- | --- | --- |
| Planning | 5.0-A | This document + interface decision + data plan + SFT format |
| Data prep | 5.0-B | Train/dev/gold split plan, sample generation |
| Training | 5.1 | LoRA/SFT implementation and training run |
| Evaluation | 5.2 | Full eval on gold set, baseline comparison, error analysis |
| Packaging | 6.0 | README, reports, resume bullets, demo |

## 10. Files Reference

| File | Purpose |
| --- | --- |
| `docs/v05/V05_TRAINING_PLAN.md` | This document |
| `docs/v05/V05_DATA_PLAN.md` | Data split and distribution plan |
| `docs/v05/V05_SFT_FORMAT.md` | SFT message format specification |
| `reports/v04/interface_decision_report.md` | Interface decision evidence |
| `src/v04/parser.py` | DSL → canonical JSON parser |
| `src/v04/eval_runner.py` | Evaluation harness |
| `src/v04/metrics.py` | Metric computation |
| `src/v04/case_validator.py` | Case structure validator |

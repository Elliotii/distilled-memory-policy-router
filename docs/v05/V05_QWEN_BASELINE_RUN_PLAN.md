# V0.5 Qwen Baseline Run Plan

Version: v0.5
Date: 2026-06-02
Status: Planning — baseline run configuration and output schema
Context: 5.4-A

---

## 1. Prompt / Interface Conditions

### 1.1 Unit DSL (Primary Interface)

**Zero-shot:**
- System prompt: Standard memory policy router instruction (see `render_sft_messages.py`)
- Input rendering: RUNTIME_CONTEXT + CANDIDATE_MEMORIES + CURRENT_UNITS
- Format: As rendered by `render_user_input()` from `src/v05/render_sft_messages.py`

**Few-shot:**
- 3 examples drawn from train-pool only
- Example format: USER block + ASSISTANT block
- Must NOT include any dev or gold cases

### 1.2 Unit JSON (Secondary Interface)

**Zero-shot:**
- System prompt with JSON output schema
- Input: Same rendered context + memories + units
- Output: JSON with `read_hints`, `store`, `skip` fields

**Few-shot (optional):**
- 3 JSON examples from train-pool
- Lower priority than DSL

### 1.3 Prompt Versioning

```
prompts/v05/unit_dsl_zero_shot.txt    — v0.5 Unit DSL zero-shot prompt
prompts/v05/unit_dsl_few_shot.txt     — v0.5 Unit DSL few-shot prompt
prompts/v05/unit_json_zero_shot.txt   — v0.5 Unit JSON zero-shot prompt
```

Few-shot examples are embedded at inference time, not in the prompt file.

## 2. Decoding Settings

| Parameter | Value | Reason |
|-----------|-------|--------|
| temperature | 0 | Deterministic output for reproducibility |
| max_new_tokens | 256 | Sufficient for DSL lines (typically <100 tokens) |
| do_sample | False | Greedy decoding |
| enable_thinking | False | Disable thinking mode for instruction-following tasks |
| repetition_penalty | 1.0 | No penalty |

**Model-specific notes:**
- Qwen3-4B: `enable_thinking=False` passed via `generate()` kwarg or chat template parameter
- Qwen3.5: Verify `enable_thinking` API — may differ from Qwen3

## 3. Output Storage

### 3.1 Prediction JSONL Format

Each line is a JSON object:

```json
{
  "case_id": "v05_dev_0001",
  "model_id": "qwen3-4b",
  "model_path": "/home/abc16/hf_models/Qwen3-4B-Instruct-2507",
  "interface": "unit_dsl",
  "prompt_version": "v05_zero_shot",
  "split": "dev",
  "raw_output": "READ m1\nSTORE NONE\nSKIP u1",
  "latency_ms": 1234.5,
  "error": null,
  "metadata": {
    "temperature": 0,
    "max_new_tokens": 256,
    "enable_thinking": false,
    "timestamp_utc": "2026-06-02T12:00:00Z"
  }
}
```

### 3.2 File Naming Convention

```
predictions/v05/<split>/<model>_<interface>_<config>_predictions.jsonl
```

Examples:
```
predictions/v05/dev/qwen3_4b_unit_dsl_zero_shot_predictions.jsonl
predictions/v05/dev/qwen3_4b_unit_dsl_few_shot_predictions.jsonl
predictions/v05/gold/qwen3_4b_unit_dsl_zero_shot_predictions.jsonl
predictions/v05/gold/deepseek_teacher_unit_dsl_predictions.jsonl
```

## 4. Eval

### 4.1 Evaluation Pipeline

```
prediction JSONL → eval_runner.py → aggregate metrics + per-case metrics
```

- All scoring through `src/v04/eval_runner.py`
- No manual metric calculation as final source
- Report generation: `eval_runner.py` with `--report` and `--error-report` flags

### 4.2 Primary Metrics

| Metric | Target |
|--------|:------:|
| parse_success | ≥ 96% |
| store_unit_f1 | Higher than zero-shot baseline |
| store_target_accuracy | Higher than zero-shot baseline |
| skip_f1 | Higher than zero-shot baseline |
| read_f1 | Maintain or improve |
| false_store_rate | Decrease vs zero-shot |
| sensitive_store_count | = 0 |

## 5. Dev vs Gold

### Dev (Model Selection Phase)

```
Purpose: Compare configurations, select best model/interface.
Allowed: Iterative evaluation, checkpoint comparison, prompt variation.
Not for: Final claims, reporting as "held-out results."
```

### Locked Gold (Final Evaluation Phase)

```
Purpose: Single evaluation pass for final report.
Allowed: ONE evaluation per system after all selection is complete.
Not for: Prompt tuning, hyperparameter search, iterative improvement.
```

## 6. Smoke Test Plan (Before Full Runs)

### 6.1 5-Case Dev Smoke

```
Cases: First 5 dev cases (v05_dev_0001 - v05_dev_0005)
Systems: Qwen3-4B zero-shot DSL, few-shot DSL, zero-shot JSON
Check:
  - Parse success rate
  - Latency per case
  - VRAM usage
  - Output format correctness
  - No crashes on varying input sizes
Split: dev only — do NOT use gold
```

### 6.2 Smoke Pass Criteria

| Check | Threshold |
|-------|:---------:|
| parse_success | ≥ 80% (small sample, stricter for full run) |
| per-case latency | < 30s per case |
| VRAM | < 10.5 GB (fits 11GB GPU) |
| no crashes | 100% of cases complete |

## 7. Runner Compatibility

### 7.1 Existing: `src/v04/qwen_local_output_runner.py`

```
Capabilities:
- Loads Qwen3-4B from local path
- Renders 3 v0.4 prompt interfaces (legacy_span_json, unit_json, unit_dsl)
- Runs on 5-case smoke
- Writes prediction JSONL

Limitations for v0.5:
- Uses v0.4 prompt templates — needs v0.5 prompt files
- Case loading from subset50 pattern — needs generic case loader
- Few-shot mode not implemented
- Single-model, single-interface per run
```

### 7.2 Required Changes for v0.5 Baseline Runs

```
1. Create v0.5 prompt templates (unit_dsl.txt, unit_dsl_fewshot.txt, unit_json.txt)
2. Add few-shot example injection (3 examples from train-pool)
3. Add generic case file loading (--cases flag)
4. Add split-aware metadata (--split dev|gold)
5. Add multiple interface flag (--interfaces dsl|json|all)
6. Add deterministic seed setting
7. Add Qwen3.5 model path support (--model-path flag)
8. Preserve backward compatibility with existing v0.4 runner
```

### 7.3 Existing: `src/v04/eval_runner.py`

```
Capabilities:
- Evaluates prediction JSONL against gold cases
- Computes all v0.4 metrics
- Generates aggregate + per-case reports

Compatibility with v0.5:
- Same prediction JSONL format
- Same metric computation
- May need v0.5 split awareness for report grouping
```

---

*End of V0.5 Qwen Baseline Run Plan.*

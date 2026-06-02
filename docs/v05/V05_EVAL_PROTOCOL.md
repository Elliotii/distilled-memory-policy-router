# V0.5 Evaluation Protocol

Version: v0.5
Date: 2026-06-02
Status: Planning — evaluation methodology, systems, metrics, and reporting
Context: 5.3-A — dev/gold + provenance + leakage planning

---

## 1. Evaluation Goal

Evaluate whether a LoRA/SFT-trained Qwen3-4B memory policy router can approximate a teacher routing policy under the Unit DSL interface while preserving safety constraints.

The evaluation answers:

1. Does training improve routing metrics over few-shot baselines?
2. Does the trained router maintain high parse success (≥96%)?
3. Is sensitive store rate exactly 0% on gold?
4. Does target accuracy improve, especially on hard boundaries?
5. Does training cause target collapse (e.g., all predictions defaulting to one target)?

---

## 2. Systems to Compare

### 2.1 Complete System Inventory

| # | System | Type | Description |
|---|--------|------|-------------|
| 1 | `empty` | Baseline | READ none, STORE none, SKIP all units |
| 2 | `topk_read` | Baseline | READ first K candidate memories, STORE none, SKIP all |
| 3 | `heuristic` | Baseline | Deterministic lexical rules for READ/STORE/SKIP |
| 4 | `per_target_majority` | Baseline | Always predict most common target; STORE all non-sensitive units |
| 5 | `deepseek_teacher` | Teacher reference | DeepSeek V4 Flash-compatible with same prompt |
| 6 | `qwen_zero_shot_dsl` | Baseline | Qwen3-4B zero-shot Unit DSL |
| 7 | `qwen_few_shot_dsl` | Baseline | Qwen3-4B few-shot Unit DSL (3 examples from train) |
| 8 | `qwen_zero_shot_json` | Baseline | Qwen3-4B zero-shot Unit JSON |
| 9 | `qwen_lora_dsl` | **Primary** | Qwen3-4B LoRA/SFT-trained Unit DSL router |

### 2.2 System Descriptions

**empty:** Returns `READ NONE` / `STORE NONE` / `SKIP all`. Measures task difficulty floor — if the trained router can't beat this, something is seriously wrong.

**topk_read:** Reads the first K candidate memories (K = 1 or K = min(2, len(candidate_memories))). STORE none. SKIP all. Measures whether simple retrieval heuristics capture most of the value.

**heuristic:** Deterministic lexical rules:
- READ memories whose content shares ≥3 content words with any current unit.
- STORE units containing known patterns (file paths → repo_memory, action verbs → task_state, etc.).
- SKIP everything else.

Measures whether a simple non-learned policy can already perform well.

**per_target_majority:** Always predicts the most frequent target in the train set (expected: `task_state`). STORE every non-sensitive unit. SKIP nothing. Measures the "always-guess-majority" floor for target accuracy.

**deepseek_teacher:** DeepSeek V4 Flash-compatible prompted with the same system prompt and input rendering. Acts as a **teacher ceiling / policy reference** — the strongest available routing policy. NOT objective truth. Any evaluation against DeepSeek is "does the student approach the teacher?", not "does the student approach truth?"

**qwen_zero_shot_dsl:** Qwen3-4B with zero-shot Unit DSL prompt. The base model without training. Measures how much training helps over prompt alone.

**qwen_few_shot_dsl:** Qwen3-4B with few-shot Unit DSL prompt (3 examples from train). Measures the ceiling of prompt-based learning without weight updates.

**qwen_zero_shot_json:** Qwen3-4B with zero-shot Unit JSON prompt. Interface fallback baseline — if JSON is comparable to DSL, the DSL interface advantage is questionable.

**qwen_lora_dsl:** Qwen3-4B with LoRA/SFT training on Unit DSL. The primary system under evaluation. Compare against qwen_zero_shot_dsl and qwen_few_shot_dsl to measure training gain.

---

## 3. Teacher Ceiling

### 3.1 DeepSeek as Teacher Reference

The DeepSeek teacher system is evaluated on the human-adjudicated gold set to establish a **teacher ceiling / policy reference**.

Important caveats:

- DeepSeek labels are NOT objective truth.
- DeepSeek may make errors that the human adjudicator would correct.
- DeepSeek may have different target-boundary biases than the human annotation.
- The teacher ceiling is an aspirational reference, not a correctness oracle.

### 3.2 Interpreting Teacher Comparisons

| Scenario | Interpretation |
|----------|---------------|
| Student ≈ Teacher on gold | Student successfully distills the teacher policy |
| Student > Teacher on gold | Student may be overfitting gold, or teacher has systematic errors |
| Student < Teacher on gold | Expected — student is a smaller model; quantify the gap |
| Student ≪ Teacher on gold | Training failed or teacher is fundamentally stronger |

**Important:** Teacher-student direct agreement should NOT be used as a primary conclusion. The primary comparison should be **each system vs human-adjudicated gold**. The teacher serves as a policy reference / upper-bound estimate — it tells us how close we can get to a strong teacher, but gold is the evaluation standard.

### 3.3 Teacher Evaluation Requirements

- DeepSeek must be evaluated on the SAME human-adjudicated gold set as the student.
- DeepSeek must use the SAME prompt family (comparable input rendering).
- DeepSeek evaluation is a ONE-TIME measurement — not iterative tuning.
- DeepSeek results are reported alongside student results, not as a separate section.
- DeepSeek on gold is a **policy reference / teacher ceiling estimate**, not objective truth.

---

## 4. Metrics

### 4.1 Structural Metrics

| Metric | Definition | Target |
|--------|-----------|:------:|
| `parse_success` | % of outputs that parse into valid canonical structure | ≥ 96% |
| `invalid_memory_id_rate` | % of predicted READ IDs not in candidate_memories | 0% |
| `invalid_unit_id_rate` | % of predicted unit IDs not in current_units | 0% |
| `invalid_target_rate` | % of predicted STORE targets not in legal targets | 0% |
| `output_length_chars` | Mean raw output characters | Lower is better |
| `output_length_lines` | Mean raw output lines | Lower is better |

### 4.2 Semantic Routing Metrics

| Metric | Definition |
|--------|-----------|
| `exact_match` | % of cases where predicted == gold exactly (all READ, STORE, SKIP match) |
| `read_precision` | |predicted_READ ∩ gold_READ| / |predicted_READ| |
| `read_recall` | |predicted_READ ∩ gold_READ| / |gold_READ| |
| `read_f1` | Harmonic mean of read_precision and read_recall |
| `store_unit_precision` | |predicted_STORE_unit_ids ∩ gold_STORE_unit_ids| / |predicted_STORE_unit_ids| |
| `store_unit_recall` | |predicted_STORE_unit_ids ∩ gold_STORE_unit_ids| / |gold_STORE_unit_ids| |
| `store_unit_f1` | Harmonic mean of store_unit_precision and store_unit_recall |
| `store_target_accuracy` | Among correctly predicted STORE units, % with correct target |
| `skip_precision` | |predicted_SKIP ∩ gold_SKIP| / |predicted_SKIP| |
| `skip_recall` | |predicted_SKIP ∩ gold_SKIP| / |gold_SKIP| |
| `skip_f1` | Harmonic mean of skip_precision and skip_recall |
| `false_store_rate` | Units predicted STORE that gold says SKIP / predicted STORE units |
| `irrelevant_read_rate` | Predicted READ not in gold READ / predicted READ |
| `sensitive_store_count` | Number of sensitive units predicted as STORE (must be 0) |

### 4.3 Derived Diagnostic Metrics

| Metric | Definition |
|--------|-----------|
| `target_confusion_rate` | Among correctly predicted STORE units, % with wrong target |
| `over_read_rate` | Predicted READ not in gold READ / gold READ (how much over-reading) |
| `under_read_rate` | Gold READ not in predicted READ / gold READ (how much under-reading) |
| `unit_coverage` | % of current units that appear exactly once in STORE/SKIP |

### 4.4 Efficiency Metrics (Optional)

| Metric | Definition |
|--------|-----------|
| `latency_ms` | Mean end-to-end inference latency per case |
| `tokens_per_case` | Mean output tokens per case |

---

## 5. Primary Success Criteria

### 5.1 Primary Metrics (Required Improvements)

Trained router (`qwen_lora_dsl`) must improve over `qwen_few_shot_dsl` on these primary metrics:

| Metric | Improvement |
|--------|:-----------:|
| `store_unit_f1` | Increase (especially recall) |
| `store_target_accuracy` | Increase |
| `skip_f1` | Increase (especially precision — fewer false stores) |
| `read_f1` | Maintain or improve |
| `false_store_rate` | Decrease |

### 5.2 Secondary Strict Metric

`exact_match` is demoted from a primary required success metric to a **secondary strict metric**:

- It remains useful as a holistic correctness signal (perfect routing across all dimensions).
- It should NOT be the sole success criterion — it penalizes minor differences (e.g., READ order) that do not affect downstream memory quality.
- If exact_match improves, it is supporting evidence; if it does not, the primary metrics above determine success.

### 5.3 Required Preservation

Trained router must maintain:

| Metric | Requirement |
|--------|:-----------:|
| `parse_success` | ≥ 96% |
| `sensitive_store_count` | = 0 |
| `invalid_memory_id_rate` | = 0% |
| `invalid_unit_id_rate` | = 0% |
| `invalid_target_rate` | = 0% |

### 5.4 Hard No-Go Gates

| Condition | Consequence |
|-----------|------------|
| `sensitive_store_count > 0` on gold | **No-Go** — model must not be deployed or claimed |
| `parse_success < 90%` on gold | **No-Go** — interface is too unstable |
| Target collapse (>80% of STORE predictions to single target) | **No-Go** — model hasn't learned routing |
| `store_unit_f1 < qwen_zero_shot_dsl store_unit_f1` | **Partial-Go** — training didn't improve routing |

### 5.5 Soft Success Criteria

Desirable but not required:

| Metric | Goal |
|--------|------|
| `qwen_lora_dsl` beats `qwen_zero_shot_json` on routing metrics | Training + DSL > zero-shot JSON |
| `qwen_lora_dsl` within 10pp of `deepseek_teacher` on exact_match | Student approaches teacher |
| `irrelevant_read_rate` decreases vs few-shot | Training reduces over-reading |

---

## 6. Reporting

### 6.1 Report Sections

The final evaluation report must include:

1. **Aggregate metrics table**: All systems × all metrics on full gold.
2. **Gold core metrics**: All systems × gold_core (70 cases).
3. **Gold hard metrics**: All systems × gold_hard (30 cases).
4. **Per-target breakdown**: STORE target accuracy per target for each system.
5. **Per-tag breakdown**: Metrics grouped by case tags (boundary types, shapes).
6. **Target confusion matrix**: For each system, which targets are confused with which.
7. **Error analysis**: Examples of false stores, irrelevant reads, target confusions.
8. **Sensitive store report**: Must be 0; if not 0, list all cases.
9. **Baseline comparison narrative**: What each baseline teaches us.
10. **Limitations**: Label provenance, gold size, LLM-assisted labeling caveats.

### 6.2 What NOT to Report

Do NOT report:

- Dev metrics as final claims.
- "Our model achieves X on dev" without explicit caveat.
- Teacher performance as if it were ground truth.
- Per-target accuracy without noting gold n per target.
- Aggregate metrics without error bars or confidence intervals.

### 6.3 Honest Reporting Language

| ✅ Say This | ❌ Not This |
|------------|------------|
| "On human-adjudicated gold (n=100), the trained router achieves..." | "Our model achieves 92% accuracy" |
| "The teacher (DeepSeek) serves as a policy reference, not ground truth" | "Compared to the ground truth teacher" |
| "Gold labels were human-adjudicated with LLM-assisted review suggestions" | "Gold was independently labeled by Opus" |
| "The 70-case gold core represents natural distribution" | "Our evaluation set covers all scenarios" |
| "Sensitive store rate is 0% on gold (n=100)" | "The model is safe" |

---

## 7. Evaluation Execution

### 7.1 Eval Harness

Use the existing `src/v04/eval_runner.py` for all evaluations. It supports:

- Multiple interfaces (unit_dsl, unit_json, legacy_span_json).
- Batch evaluation of prediction JSONL files.
- Aggregate and per-case metrics.
- Report generation.

### 7.2 Prediction File Convention

Each system produces a prediction JSONL file:

```
predictions/v05/<system>_<split>_predictions.jsonl
```

Example:
```
predictions/v05/qwen_lora_dsl_gold_predictions.jsonl
predictions/v05/deepseek_teacher_gold_predictions.jsonl
predictions/v05/qwen_few_shot_dsl_dev_predictions.jsonl
```

### 7.3 Evaluation Command

```bash
python3 -m src.v04.eval_runner \
  --cases data/v05/gold/v05_gold_cases.jsonl \
  --predictions predictions/v05/qwen_lora_dsl_gold_predictions.jsonl \
  --report reports/v05/v05_final_eval_report.md \
  --error-report reports/v05/v05_final_error_analysis.md
```

---

## 8. Changelog

| Date | Change |
|------|--------|
| 2026-06-02 | Initial creation (Context 5.3-A) |

---

*End of V0.5 Evaluation Protocol.*

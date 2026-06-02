# V0.5 Baseline Evaluation Plan

Version: v0.5
Date: 2026-06-02
Status: Planning — baseline inventory, rationale, and output schema
Context: 5.3-A — dev/gold + provenance + leakage planning

---

## 1. Baseline Inventory

### 1.1 Complete List

| # | System ID | What It Predicts | Requires Model? |
|---|-----------|-----------------|:---------------:|
| 1 | `empty` | READ NONE, STORE NONE, SKIP all | No |
| 2 | `topk_read_k1` | READ first candidate memory, STORE NONE, SKIP all | No |
| 3 | `topk_read_k2` | READ first 2 candidate memories, STORE NONE, SKIP all | No |
| 4 | `heuristic_lexical` | Lexical-rule-based READ/STORE/SKIP | No |
| 5 | `heuristic_read_all` | READ all candidate memories, STORE NONE, SKIP all | No |
| 6 | `per_target_majority` | STORE all units as most-common target, SKIP none | No |
| 7 | `per_target_task_state` | STORE all units as task_state, SKIP none | No |
| 8 | `deepseek_teacher` | DeepSeek V4 Flash Unit DSL | Yes (API) |
| 9 | `qwen_zero_shot_dsl` | Qwen3-4B zero-shot Unit DSL | Yes (local) |
| 10 | `qwen_few_shot_dsl` | Qwen3-4B few-shot Unit DSL (3 examples) | Yes (local) |
| 11 | `qwen_zero_shot_json` | Qwen3-4B zero-shot Unit JSON | Yes (local) |
| 12 | `qwen_few_shot_json` | Qwen3-4B few-shot Unit JSON (optional) | Yes (local) |
| 13 | `qwen_lora_dsl` | Qwen3-4B LoRA/SFT Unit DSL | Yes (local) |
| 14 | `qwen_lora_dsl_shuffled_labels` | Qwen3-4B LoRA on shuffled-label DSL (optional sanity) | Yes (local) |

### 1.2 System Descriptions

#### `empty` — No-Action Baseline

```
READ NONE
STORE NONE
SKIP u1,u2,u3
```

Measures: Task difficulty floor. If the trained router can't beat empty on SKIP F1, it's learning nothing.

#### `topk_read_k1` — Top-1 READ Baseline

```
READ m1
STORE NONE
SKIP u1,u2,u3
```

Measures: Value of simple retrieval heuristic. How much does reading the most recent/top memory help?

#### `topk_read_k2` — Top-2 READ Baseline

```
READ m1,m2
STORE NONE
SKIP u1,u2,u3
```

Measures: Whether reading more memories from a naive top-K helps or hurts (irrelevant reads).

#### `heuristic_lexical` — Lexical Rule Baseline

Deterministic rules:
- READ: candidate memories with ≥3 shared content words (non-stop) with any current unit text.
- STORE service_memory: units containing "must", "requires", "rejects", "returns", "validates", "computes", "converts", "should" or ending with "invariant".
- STORE repo_memory: units containing file paths (regex), "test", "pytest", "under", "directory", "command".
- STORE project_memory: units containing "project does not", "project scope", "all services must", "cross-cutting".
- STORE user_profile: units containing "I prefer", "I like", "my default".
- STORE task_state: units containing "Add", "Implement", "Next", "blocked", "in progress", "not yet".
- SKIP: everything else + units with "password", "token", "key", "phone", "email", "secret", "credential".

Measures: Non-learned policy performance. How much does learning add over hand-crafted rules?

#### `heuristic_read_all` — READ-All Baseline

```
READ m1,m2,...,mN
STORE NONE
SKIP u1,u2,u3
```

Measures: Ceiling of "just read everything." If READ precision is 0 but recall is 1, this baseline quantifies over-reading cost.

#### `per_target_majority` — Majority Target Baseline

STORE every non-sensitive unit as the most common target in train (expected: `task_state`). SKIP none.

Measures: Target accuracy floor. If the trained router can't beat majority-class guessing, target learning failed.

#### `per_target_task_state` — Task State Default Baseline

STORE every unit as `task_state`. SKIP none.

Measures: Performance of always-defaulting to the most common coding-agent target.

#### `deepseek_teacher` — Teacher Policy Reference

DeepSeek V4 Flash-compatible model, same system prompt and input rendering as student.

Measures: Teacher ceiling. Upper bound for what the student might approximate.

#### `qwen_zero_shot_dsl` — Base Model Zero-Shot

Qwen3-4B with zero-shot Unit DSL prompt. No training, no few-shot examples.

Measures: Base model capability. Is training even needed, or can a 4B model already do this well?

#### `qwen_few_shot_dsl` — Base Model Few-Shot

Qwen3-4B with 3 few-shot examples in the system prompt (sourced from train).

Measures: Prompt-learning ceiling without weight updates. How much does LoRA add over good prompting?

#### `qwen_zero_shot_json` — JSON Interface Baseline

Qwen3-4B with zero-shot Unit JSON prompt. Alternative output format.

Measures: Whether DSL interface is actually better than JSON, or if the model just needs training regardless of format.

#### `qwen_few_shot_json` — JSON Few-Shot Baseline (Optional)

Qwen3-4B with few-shot Unit JSON prompt (3 examples from train).

**Purpose:** Checks whether Unit JSON improves with examples. Prevents unfair DSL-vs-JSON comparison where DSL gets few-shot and JSON only gets zero-shot. If `qwen_few_shot_json` matches `qwen_few_shot_dsl`, the interface format difference is negligible; if DSL is clearly better, the interface advantage is real.

#### `qwen_lora_dsl` — Trained Router (Primary System)

Qwen3-4B LoRA/SFT-trained on Unit DSL.

Measures: The system under test. Compare against all baselines.

#### `qwen_lora_dsl_shuffled_labels` — Shuffled-Label Sanity Baseline (Optional)

Qwen3-4B LoRA/SFT-trained on Unit DSL with **shuffled labels** (READ/STORE/SKIP re-assigned randomly while preserving output format).

**Purpose:** Sanity check that LoRA learns routing signal rather than only output format. If the model achieves comparable routing metrics with shuffled labels, the training signal is dominated by format learning rather than routing policy. Optional — do not block training if time is limited.

Qwen3-4B LoRA/SFT-trained on Unit DSL.

Measures: The system under test. Compare against all baselines.

---

## 2. Why Each Baseline Matters

| Baseline | Research Question Answered |
|----------|---------------------------|
| `empty` | Is the task learnable, or is there no signal? |
| `topk_read_k1/k2` | How much value does simple retrieval capture? |
| `heuristic_lexical` | Can hand-crafted rules already solve this? |
| `heuristic_read_all` | What's the cost of over-reading? |
| `per_target_majority` | Does the model learn targets, or just guess the majority? |
| `per_target_task_state` | Is `task_state` a strong default, making target learning moot? |
| `deepseek_teacher` | What does a strong teacher policy look like? |
| `qwen_zero_shot_dsl` | Does the base model already understand the task? |
| `qwen_few_shot_dsl` | Does prompt engineering suffice without training? |
| `qwen_zero_shot_json` | Is the DSL interface advantage real? |
| `qwen_few_shot_json` | Does JSON improve with examples, or is DSL inherently better? |
| `qwen_lora_dsl` | Does LoRA/SFT training improve over all of the above? |
| `qwen_lora_dsl_shuffled_labels` | Does LoRA learn routing signal, or just output format? |

---

## 3. Same-Prompt Requirement

### 3.1 Comparable Input Rendering

All Qwen-based systems (zero-shot DSL, few-shot DSL, LoRA DSL) must use the **same input rendering format** — same system prompt structure, same RUNTIME_CONTEXT / CANDIDATE_MEMORIES / CURRENT_UNITS layout.

This ensures improvements are attributable to training, not prompt engineering.

### 3.2 Permitted Differences

| System | Difference from LoRA DSL |
|--------|--------------------------|
| `qwen_zero_shot_dsl` | System prompt has NO few-shot examples |
| `qwen_few_shot_dsl` | System prompt HAS 3 few-shot examples (from train) |
| `qwen_zero_shot_json` | Assistant format is Unit JSON, not Unit DSL |
| `qwen_few_shot_json` | Assistant format is Unit JSON with 3 few-shot examples (from train) |
| `qwen_lora_dsl` | System prompt has NO few-shot examples (model learns from weights) |
| `qwen_lora_dsl_shuffled_labels` | Same as `qwen_lora_dsl` but trained on shuffled-label data |
| `deepseek_teacher` | Same prompt as `qwen_zero_shot_dsl` (zero-shot, no few-shot) |

### 3.3 Few-Shot Sourcing

Few-shot examples for `qwen_few_shot_dsl` MUST:

- Come from the train pool (NOT dev, NOT gold, NOT subset50).
- Cover all three shapes (READ-only, STORE/SKIP-only, READ+STORE joint).
- Cover at least 3 of 5 STORE targets.
- Include at least one SKIP example.
- Be recorded in the train pool manifest.

---

## 4. Eval Split Usage

| System | Dev | Gold | Notes |
|--------|:---:|:----:|-------|
| `empty` | ✓ | ✓ | Deterministic, same on both splits |
| `topk_read_k1/k2` | ✓ | ✓ | Deterministic |
| `heuristic_lexical` | ✓ | ✓ | Deterministic |
| `heuristic_read_all` | ✓ | ✓ | Deterministic |
| `per_target_majority` | ✓ | ✓ | Deterministic (target from train distribution) |
| `per_target_task_state` | ✓ | ✓ | Deterministic |
| `deepseek_teacher` | Optional | ✓ | Evaluate on gold for teacher ceiling |
| `qwen_zero_shot_dsl` | ✓ | ✓ | Evaluate on both for training gain analysis |
| `qwen_few_shot_dsl` | ✓ | ✓ | Evaluate on both |
| `qwen_zero_shot_json` | ✓ | ✓ | Evaluate on both |
| `qwen_few_shot_json` | ✓ | ✓ | Evaluate on both (optional) |
| `qwen_lora_dsl` | ✓ (checkpoints) | ✓ (final) | Dev for checkpoint selection, gold for final report |
| `qwen_lora_dsl_shuffled_labels` | ✓ | ✓ | Evaluate on both (optional sanity) |

---

## 5. Risks and Caveats

### 5.1 DeepSeek Is Not Objective Truth

DeepSeek is a larger model with different training data and biases. It may:
- Have different target-boundary preferences.
- Store content that the human adjudicator would SKIP.
- READ memories that the human adjudicator would not.

The teacher ceiling is a **policy reference**, not a correctness oracle.

**Primary comparison rule:** The primary comparison is **each system vs human-adjudicated gold**. Do NOT use teacher-student direct agreement as a primary conclusion. DeepSeek-on-gold is a teacher ceiling estimate — it tells us how close the student can get to a strong routing policy — but gold is the evaluation standard.

Do not report DeepSeek-gold agreement as "accuracy."

### 5.2 Unit JSON vs Unit DSL Interface Difference

`qwen_zero_shot_json` uses a different output format. Differences may reflect:
- JSON vs DSL structural stability.
- Model's JSON generation capability.
- Not necessarily routing quality differences.

If JSON significantly outperforms DSL, reconsider the DSL interface choice.

### 5.3 Latency / Size Differences

| System | Model Size | Expected Latency |
|--------|:----------:|:----------------:|
| DeepSeek teacher | Large (cloud) | Higher (API call) |
| Qwen3-4B systems | ~7.5 GB | Lower (local) |
| Deterministic baselines | N/A | Negligible |

Latency comparisons between DeepSeek and Qwen3-4B are not apples-to-apples. Report latency for completeness but do not claim "faster than teacher" as a primary finding — it's expected.

### 5.4 Dev Overfitting Risk

Repeated evaluation on dev during training can lead to overfitting dev, especially with only 80–100 cases. Mitigations:
- Use dev sparingly — evaluate every N steps, not every step.
- Select final checkpoint based on dev, but report only gold.
- If dev and gold metrics diverge significantly, report the divergence as a finding.

### 5.5 LLM-Generated Labels

All baselines except `empty` and `heuristic` are compared against gold labels that were influenced by LLM-assisted generation (for train) or human-adjudicated (for gold). The teacher model (DeepSeek) may share label-style biases with the LLM that generated train labels. This could inflate teacher-student agreement artificially.

---

## 6. Required Output Table Schema

### 6.1 Main Results Table

| System | Split | Parse % | Exact % | READ F1 | STORE F1 | Target Acc % | SKIP F1 | False Store % | Sensitive Store | Latency ms | Notes |
|--------|-------|:-------:|:-------:|:-------:|:--------:|:------------:|:-------:|:-------------:|:---------------:|:----------:|-------|
| `empty` | gold | 100 | ... | ... | ... | ... | ... | ... | 0 | ... | — |
| `topk_read_k1` | gold | 100 | ... | ... | ... | ... | ... | ... | 0 | ... | — |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| `qwen_lora_dsl` | gold | ... | ... | ... | ... | ... | ... | ... | 0 | ... | **Primary** |

### 6.2 Per-Target Breakdown Table

| System | Split | Target | STORE Count | Target Acc % | Notes |
|--------|-------|--------|:-----------:|:------------:|-------|
| `qwen_lora_dsl` | gold | service_memory | N | X% | — |
| `qwen_lora_dsl` | gold | task_state | N | X% | — |
| ... | ... | ... | ... | ... | ... |

### 6.3 Per-Tag Breakdown Table

| System | Split | Tag | Cases | Exact % | STORE F1 | Target Acc % | Notes |
|--------|-------|-----|:-----:|:-------:|:--------:|:------------:|-------|
| `qwen_lora_dsl` | gold | service_vs_task_state | N | X% | X | X% | — |
| `qwen_lora_dsl` | gold | sensitive_boundary | N | X% | X | X% | Must be 0 sensitive store |
| ... | ... | ... | ... | ... | ... | ... | ... |

### 6.4 Gold Core vs Gold Hard Table

| System | Subset | Cases | Exact % | STORE F1 | Target Acc % | Sensitive Store |
|--------|--------|:-----:|:-------:|:--------:|:------------:|:---------------:|
| `qwen_lora_dsl` | gold_core | 70 | X% | X | X% | 0 |
| `qwen_lora_dsl` | gold_hard | 30 | X% | X | X% | 0 |
| `deepseek_teacher` | gold_core | 70 | X% | X | X% | 0 |
| `deepseek_teacher` | gold_hard | 30 | X% | X | X% | 0 |

---

## 7. Changelog

| Date | Change |
|------|--------|
| 2026-06-02 | Initial creation (Context 5.3-A) |

---

*End of V0.5 Baseline Evaluation Plan.*

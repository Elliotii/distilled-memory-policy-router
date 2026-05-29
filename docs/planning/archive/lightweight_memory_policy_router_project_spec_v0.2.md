# Distilled Memory Policy Router for Coding-Agent Contexts

Version: v0.2  
Date: 2026-05-24  
Status: Project planning spec after external review  
Previous working title: Lightweight Memory Policy Router for Coding Agents

## 0. One-Sentence Summary

Train and evaluate a small fine-tuned router that predicts structured read/write/ignore memory-policy hints for coding-agent interactions, learning from a prompt-based teacher while reducing false memory writes and irrelevant memory reads compared with naive baselines.

## 1. Project Motivation

Long-running coding agents need memory, but better memory does not simply mean storing or retrieving more history. The harder problem is policy:

- Which candidate memories should be read for the current task?
- Which spans in the current user input deserve long-term memory?
- Which temporary, noisy, incorrect, or irrelevant spans should be explicitly ignored?

This project turns agent-memory policy into a measurable structured-prediction task. It does not build a full autonomous agent or a complete memory operating system. Instead, it builds and evaluates a lightweight router that provides memory-relevant attention hints to a stronger LLM or downstream coding agent.

## 2. Core Research Question and Hypotheses

Main research question:

> Can a small fine-tuned router learn structured read/write/ignore memory-policy decisions for coding-agent interactions from a strong prompt teacher, while reducing false memory writes and irrelevant memory reads compared with naive baselines?

Hypotheses:

- **H1:** LoRA/SFT improves JSON validity and read/write/ignore F1 over the same student model in zero-shot mode.
- **H2:** Explicit `ignore_spans` supervision should reduce memory-pollution components, especially false writes and missed-ignore cases. In the MVP, this is evaluated against rule-based, zero-shot, and naive baselines; a stronger causal test would add a no-ignore/write-only ablation as stretch work.

The project should be evaluated as a research-engineering project, not as a claim of novel agent-memory theory.

## 3. MVP and Stretch Boundary

### 3.1 Must-Finish MVP

The MVP should be clean, small, and credible:

```text
Seed examples: 50
Synthetic train: 5,000 examples
Dev: 250 examples
Gold eval: 300 human-reviewed examples
Multi-turn traces: 6-8 traces
Teacher: DeepSeek V4 Flash
Student: one selected 3B-4B model
Fine-tuning: one final LoRA/QLoRA router
Baselines: empty, naive all-read, rule-based, prompt teacher, zero-shot student, fine-tuned student
Docs: README, report, error analysis, resume bullets
```

### 3.2 Stretch Version

Only after the MVP is complete:

```text
Synthetic train: 10,000-15,000 examples
Gold eval: 500-800 examples
Multi-turn traces: 12-20 traces
Full three-model bake-off
Optional non-Qwen comparison
Optional classifier-style baseline
Optional no-ignore/write-only ablation
LLM semantic judge audit
Cost-normalized comparison
Richer game-dev workflow traces
```

Do not touch real Godot/godogen integration during the MVP.

## 4. Project Scope

### 4.1 In Scope

- Structured input/output schema for memory attention hints.
- Synthetic English dataset generation.
- Programmatic validation and LLM review.
- Human-reviewed gold evaluation set.
- Prompt teacher using DeepSeek V4 Flash.
- Minimal CLI harness.
- Baseline implementations.
- Zero-shot student evaluation.
- LoRA/SFT fine-tuned student router.
- Span-level evaluation.
- Memory-pollution component analysis.
- Per-category breakdown.
- Small multi-turn trace demo.
- English README, report, and resume bullets.

### 4.2 Out of Scope for MVP

- Full coding agent implementation.
- Full game-development agent implementation.
- Agent Memory OS.
- KV cache, hidden state, or Transformer-internal memory research.
- Context-budget router or RAG reranker as the main project.
- Real Godot/godogen workflow integration.
- Memory delete/update/merge/decay operations.
- Having the small model generate final rewritten memory content.
- Having the small model manage project scope or project IDs.
- Numeric confidence prediction.
- `needs_review` prediction.
- Summary Memory baseline.
- Classifier-style baseline.
- Public benchmark adaptation.
- Pi / pi-agent integration as a main dependency.

Pi, Claude Code-style workflow, and godogen integration are future work.

### 4.3 MVP Limitation

The MVP evaluates second-stage memory policy given a small candidate set. It does not evaluate an end-to-end retrieval system over the full memory store.

In other words:

```text
This project studies whether the router can select, write, and ignore well after candidate memories are provided.
It does not claim to solve full memory retrieval from an unbounded memory database.
```

## 5. System Architecture

```text
Memory Store
        |
        v
Harness / Retriever
        |
        v
Candidate memories (0-8)
        |
        v
Current user input + Recent context + Candidate memories
        |
        v
Small Memory Policy Router
        |
        v
Structured attention hints
        |
        v
Strong LLM / Prompt Controller
        |
        v
Final memory rewrite / injection decision
        |
        v
Downstream coding agent / LLM
```

The `read` path is intentionally two-stage:

```text
1. Harness/retriever selects a small candidate set from the full memory store.
2. Small router selects read_hints from those candidates.
```

The small router is a learned component inside the memory harness. It is not an independent agent, a full retriever, or a complete memory manager. It predicts memory-relevant attention hints:

- `read_hints`
- `write_spans`
- `ignore_spans`

The strong LLM or prompt controller handles:

- Final memory rewriting.
- Correction handling.
- Conflict resolution.
- Memory injection formatting.

The harness handles:

- Project/session scope.
- Short-term context buffer.
- Long-term memory store.
- Candidate memory retrieval.
- Hard constraints and validation.
- Trace logging.
- Evaluation execution.
- The final decision about whether a proposed memory write is accepted into storage.

## 6. Input and Output Schema

All dataset content should be in English.

### 6.1 Case Metadata

Each decision case should include metadata useful for validation, splitting, and analysis:

```json
{
  "case_id": "train_000001",
  "split": "train",
  "family_id": "correction_engine_version_03",
  "category": "correction_or_revision",
  "tags": ["context_dependent", "hard_negative_memory"],
  "domain": "game_dev",
  "difficulty": "medium",
  "generator_prompt_id": "gen_prompt_b",
  "review_status": "synthetic",
  "gold_notes": null
}
```

Recommended metadata fields:

- `family_id`: mandatory for leakage control.
- `category`: mandatory for per-category breakdowns.
- `tags`: optional but useful for fine-grained analysis.
- `generator_prompt_id`: useful for detecting prompt/template bias.
- `review_status`: `synthetic`, `llm_reviewed`, or `human_reviewed`.
- `gold_notes`: optional notes for gold examples and error analysis.

### 6.2 Input Schema

```json
{
  "current_user_input": "I misspoke earlier: Godot 4.2 should be changed to Godot 4.3, and we should postpone Steam SDK integration, and the dev server froze for a second but it is fine now.",
  "recent_context": [
    {
      "role": "user",
      "content": "Let's use Godot 4.2 for this project."
    },
    {
      "role": "assistant",
      "content": "Got it. I will assume the project uses Godot 4.2."
    }
  ],
  "candidate_memories": [
    {
      "id": "m1",
      "type": "fact",
      "content": "The project uses Godot 4.2."
    },
    {
      "id": "m2",
      "type": "sop",
      "content": "Use a dark UI style for this project."
    }
  ]
}
```

Required input fields:

- `current_user_input`
- `candidate_memories`

Recommended input field:

- `recent_context`

Constraints:

- `recent_context`: 0-4 turns.
- `candidate_memories`: 0-8 items.
- `candidate_memories[*].id` must be unique within a case.

The router never receives the full memory store. It only receives the small `candidate_memories` list produced by the harness/retriever.

### 6.3 Model Prediction Schema

The router predicts only:

```json
{
  "read_hints": ["m1"],
  "write_spans": [
    {
      "span": "we should postpone Steam SDK integration",
      "type": "decision"
    }
  ],
  "ignore_spans": [
    "the dev server froze for a second"
  ]
}
```

The router does not output:

- Final rewritten memory content.
- Delete/update operations.
- Numeric confidence.
- `needs_review`.
- Project ID.
- Related memory IDs.
- Character offsets.

### 6.4 Gold Evaluation Target Schema

Gold evaluation examples must include character offsets for span labels:

Offsets should use half-open character ranges: `[char_start, char_end)`.

```json
{
  "read_hints": ["m1"],
  "write_spans": [
    {
      "span": "Godot 4.2 should be changed to Godot 4.3",
      "char_start": 20,
      "char_end": 60,
      "type": "fact"
    },
    {
      "span": "we should postpone Steam SDK integration",
      "char_start": 66,
      "char_end": 106,
      "type": "decision"
    }
  ],
  "ignore_spans": [
    {
      "span": "the dev server froze for a second but it is fine now",
      "char_start": 112,
      "char_end": 164
    }
  ]
}
```

Training data may omit offsets. Gold evaluation data should require offsets. The model should not be trained to predict offsets.

## 7. Memory Types and Annotation Rules

The project uses four memory types:

```text
sop
fact
decision
task_state
```

Definitions:

- `sop`: Long-term rules, standards, preferences, coding style, workflow rules.
- `fact`: Objective facts, architecture facts, technical stack facts, API/module relationships.
- `decision`: Project direction, trade-offs, postponed items, constraints, priorities, accepted choices.
- `task_state`: Current progress, active task, unfinished work, next step, debugging status.

In a downstream agent system, `sop` memories may map to skill files, rule files, `AGENTS.md`, `CLAUDE.md`, or a project-rule memory store rather than an ordinary fact memory database. In this project, `sop` is a router label for persistent rules/preferences, not a claim about the final storage backend.

### 7.1 Decision vs Task State Tie-Breaker

Use `decision` when the span changes or records a durable project direction, constraint, priority, trade-off, or accepted choice.

Use `task_state` when the span describes current progress, unfinished work, active debugging state, or the next step.

Examples:

```text
"We will postpone Steam SDK integration." -> decision
"Steam SDK integration is still not implemented." -> task_state
"Always use GDScript for gameplay scripts." -> sop
"The project currently uses Godot 4.3." -> fact
```

For ambiguous cases, use this annotation priority:

```text
sop > decision > fact > task_state
```

This priority rule is an annotation convention, not a claim about an ideal memory ontology.

## 8. Ignore Span Policy

`ignore_spans` should be explicit but selective.

Do label spans that are likely to become memory pollution if mistakenly written, such as:

- Temporary environment errors.
- One-off debugging noise.
- Casual chatter with no long-term value.
- Incorrect statements that are immediately corrected.
- Irrelevant implementation details.
- Transient tool or server failures.
- Prompt-injection-like memory requests in small controlled amounts.

Do not label every leftover piece of text that is not part of `write_spans`.

The purpose of `ignore_spans` is to train write-gating behavior, not to turn the task into exhaustive text segmentation.

## 9. Dataset Design

### 9.1 Data Files

Use two primary JSONL files:

```text
decision_cases.jsonl
multi_turn_traces.jsonl
```

Recommended derived files:

```text
train.jsonl
dev.jsonl
gold_eval.jsonl
```

`decision_cases.jsonl` and its split files are used for:

- Training.
- Dev evaluation.
- Gold evaluation.
- Baseline evaluation.
- LoRA/SFT.

`multi_turn_traces.jsonl` is used for:

- Demo.
- README visualization.
- Trace replay.
- Supplementary evaluation.

### 9.2 MVP Dataset Scale

Recommended MVP scale:

```text
Seed examples: 50 high-quality examples
Training set: 5,000 synthetic examples
Dev set: 250 examples
Gold eval set: 300 human-reviewed examples
Multi-turn traces: 6-8 traces
Turns per trace: 4-8 turns
```

### 9.3 Stretch Dataset Scale

Only after MVP:

```text
Training set: 10,000-15,000 synthetic examples
Gold eval set: 500-800 examples
Multi-turn traces: 12-20 traces
```

Principle:

> A clean 300-example gold set is better than a noisy 800-example gold set.

## 10. Data Category Design

The dataset should be organized by capability category, not only by memory type.

Core categories:

```text
simple_write
multi_write
read_relevant_memory
ignore_noise
correction_or_revision
context_dependent_reference
conflicting_memory
mixed_write_and_ignore
no_action_needed
distractor_memory_selection
```

Recommended MVP training distribution:

```text
simple_write: 10%
multi_write: 12%
read_relevant_memory: 12%
ignore_noise: 12%
correction_or_revision: 12%
context_dependent_reference: 10%
conflicting_memory: 10%
mixed_write_and_ignore: 8%
no_action_needed: 8%
distractor_memory_selection: 6%
```

Useful secondary tags:

```text
read_without_write
write_without_read
ambiguous_type
hard_negative_memory
implicit_reference
temporary_preference
prompt_injection_like_memory_request
```

These tags should not become top-level categories in the MVP.

Gold eval should include enough examples per category to make per-category breakdowns meaningful.

MVP target:

```text
About 30 examples per category for 300 gold examples
```

Stretch target:

```text
50+ examples per category for 500-800 gold examples
```

## 11. Data Generation Pipeline

Recommended pipeline:

```text
Human seed examples
-> DeepSeek V4 Flash generation
-> independent LLM judge/reviewer
-> programmatic validation
-> deduplication
-> family-based train/dev/eval split
-> human review for gold eval
```

Use at least three generation prompt variants to avoid overly uniform synthetic data style.

### 11.1 Two-Stage Generation

Prefer two-stage generation:

```text
Scenario card
-> Final JSON decision case
```

Scenario card fields may include:

- Domain.
- Recent context.
- Candidate memory store.
- Current user intent.
- Hidden target behavior.
- Hard distractor pattern.
- Whether the case needs recent context.
- Whether the case contains no action.
- Whether the case contains ignore-worthy noise.

This reduces shallow template repetition.

### 11.2 Programmatic Validation Rules

Each generated case must satisfy:

- Valid JSON.
- Required fields exist.
- Memory type is one of `sop`, `fact`, `decision`, `task_state`.
- `read_hints` IDs must exist in `candidate_memories`.
- `write_spans[*].span` must be an exact substring of `current_user_input`.
- `ignore_spans[*]` must be an exact substring of `current_user_input`.
- Gold eval span labels must have valid `char_start` and `char_end`.
- No empty spans.
- `candidate_memories` length must be 0-8.
- `recent_context` length must be 0-4 turns.
- No duplicate or near-duplicate cases.

### 11.3 Leakage Control

Use `family_id` or equivalent metadata to avoid leakage.

Examples from the same template family should not appear across train/dev/gold eval splits.

Additional leakage controls:

- Near-duplicate text filtering.
- Entity holdout where feasible.
- Scenario-template holdout where feasible.
- Generator-prompt analysis.
- Embedding-cluster deduplication as stretch.

At minimum, avoid putting the same project/entity family in both train and gold eval.

## 12. Teacher and Student Models

### 12.1 Prompt Teacher

Use:

```text
DeepSeek V4 Flash
```

Rationale:

- New model.
- Cost-effective.
- Supports JSON output and tool calls.
- Strong enough to serve as a practical teacher.
- Suitable as a minimum viable strong teacher rather than an unrealistically expensive upper bound.

Use non-thinking mode for data generation unless thinking mode clearly improves label quality while preserving strict JSON.

### 12.2 Student Model Strategy

Default primary student:

```text
Qwen3-4B-Instruct-2507
```

Fallback:

```text
Qwen2.5-Coder-3B-Instruct
```

Optional smoke test:

```text
Qwen3.5-4B
```

Rationale:

- Qwen3-4B-Instruct-2507 is the default because it is a recent instruction model with strong structured-output potential and manageable size.
- Qwen2.5-Coder-3B-Instruct is the fallback because it is code-specific and mature.
- Qwen3.5-4B may be promising but should not be the default until text-only LoRA/SFT compatibility is verified.

### 12.3 Bake-Off Protocol

Run a small bake-off before LoRA:

```text
Cases: 150-200 stratified dev examples
Models: Qwen3-4B-Instruct-2507, Qwen2.5-Coder-3B-Instruct, optional Qwen3.5-4B
Decoding: temperature 0 or very low
Repair: disabled for main score, optional for secondary score
Metrics: JSON validity, schema validity, read F1, write overlap F1, ignore overlap F1, type macro-F1, latency
```

Pick the model with the best combination of:

- Schema stability.
- Write/ignore behavior.
- Trainability.
- Inference speed.
- Low setup friction.

Train one final model for the MVP.

### 12.4 Training Setup

Use LoRA or QLoRA, not full fine-tuning.

Recommended starting setup:

```text
Method: QLoRA / 4-bit LoRA
Model size: 3B-4B
Sequence length: 2048 or 4096
LoRA rank: 16 or 32
Epochs: 1-3
Train examples: 3k-8k, MVP target 5k
Batch size: 1-2
Gradient accumulation: yes
Validation: every few hundred steps
```

Avoid:

- Full fine-tuning.
- Huge context lengths.
- Training all candidate models.
- Offset prediction.
- Complex multi-turn training in MVP.

## 13. Baselines

Required MVP baselines:

```text
Empty / No-action Router
Naive All-read Router
Rule-based Router
Prompt Teacher
Zero-shot Student
Fine-tuned Student
```

Definitions:

- `Empty / No-action Router`: outputs no reads, no writes, and no ignores.
- `Naive All-read Router`: reads all candidate memories and applies no selective policy.
- `Rule-based Router`: uses deterministic heuristics for lexical read selection, write triggers, ignore triggers, and type mapping.
- `Prompt Teacher`: DeepSeek V4 Flash produces structured memory attention hints.
- `Zero-shot Student`: the selected student model predicts the schema without fine-tuning.
- `Fine-tuned Student`: the selected student model after LoRA/SFT.

Optional future baselines:

```text
No-ignore / write-only ablation
Classifier-style sentence baseline
Summary Memory
Recent History
```

These are not required for the MVP.

## 14. Evaluation Plan

Primary evaluation should be deterministic/programmatic whenever possible. LLM-based evaluation can be used as a secondary semantic audit.

### 14.1 Core Metrics

- JSON validity rate.
- Schema validity rate.
- `read_hints` precision / recall / F1.
- `write_span` exact-match precision / recall / F1.
- `write_span` overlap precision / recall / F1.
- `write_type` accuracy and macro-F1.
- `ignore_span` exact-match precision / recall / F1.
- `ignore_span` overlap precision / recall / F1.
- Teacher-router agreement.
- Memory-pollution components.
- Per-category breakdown.
- Latency and cost estimate.
- Repair rate, if JSON repair is enabled.

Do not report only overall micro-F1. Include category-level and type-level breakdowns.

### 14.2 Span Matching Options

Keep three span matching options:

1. Exact match.
2. Character-overlap F1.
3. Token-level F1.

Initial tendency:

- Use exact match as a strict diagnostic metric.
- Use character-overlap F1 or token-level F1 as the main span metric.
- Report at least one strict metric and one overlap-based metric.

Recommended matching process:

```text
1. Compute pairwise overlap scores between predicted spans and gold spans.
2. Match predictions to gold spans greedily or with Hungarian matching.
3. Count a match if overlap F1 exceeds a threshold, such as 0.5 or 0.7.
4. Evaluate write type only on matched write spans.
```

### 14.3 Memory-Pollution Components

Do not collapse pollution into a single required score for the MVP. Report components:

```text
false_write_count
missed_ignore_count
irrelevant_read_count
wrong_write_type_count
false_write_on_no_action_count
```

These are easier to interpret than a subjective weighted score.

A weighted pollution score can be a stretch or appendix analysis, but it is not required.

### 14.4 Teacher-Router Agreement

Teacher-router agreement is an imitation metric, not a quality metric.

Report separately:

```text
Prompt Teacher vs gold
Zero-shot Student vs gold
Fine-tuned Student vs gold
Fine-tuned Student vs Prompt Teacher
```

Agreement with an imperfect teacher is not success unless it also improves gold performance.

### 14.5 LLM-as-Judge Usage

Use GPT/Claude-style LLM judging only for secondary analysis:

- Semantic span match review.
- Type ambiguity review.
- Error analysis.
- Judge disagreement analysis.

Do not let LLM-as-judge replace the primary programmatic metrics.

### 14.6 Human Review and Error Analysis

MVP human review target:

```text
300 gold examples human-reviewed
50 model errors spot-checked
10-20 representative error examples included in report
```

If gold eval grows beyond 300 examples, mark additional examples honestly as `llm_reviewed` unless they receive human review.

Required error analysis:

- Confusion matrix for memory type.
- False-write examples.
- Missed-write examples.
- Missed-ignore examples.
- Over-ignore examples.
- Read-hint false positives.
- Read-hint false negatives.
- No-action false positives.
- Correction/revision failures.
- `decision` vs `task_state` confusion.
- JSON/schema failure examples.
- Category-level performance table.
- Latency/cost comparison.

## 15. Minimal CLI Harness

Build a small self-contained harness.

Required functions:

- CLI user input.
- Short-term context buffer.
- JSONL memory store.
- Candidate memory retrieval.
- Prompt teacher call.
- Student router call.
- Structured output display.
- Trace logging.
- Evaluation runner.

Candidate retrieval is not the research focus.

Implementation:

- During eval: use `candidate_memories` provided by dataset.
- During demo: use simple keyword/top-k retrieval.

The harness owns hard system responsibilities:

- Project/session scoping.
- Candidate retrieval from the full memory store.
- Memory-store writes and acceptance policy.
- Validation and schema enforcement.
- Trace logging and reproducibility metadata.

The router only proposes structured hints. The strong LLM/controller or harness decides how proposed write spans become final memory content, and whether they are stored.

Example CLI display:

```text
> user: ...

[router]
read_hints: ...
write_spans: ...
ignore_spans: ...

[memory]
candidate memories: ...
selected memories: ...

[trace saved]
```

### 15.1 Trace Logging

Evaluation traces should log:

```json
{
  "case_id": "gold_00123",
  "timestamp": "...",
  "model_name": "qwen3-4b-lora",
  "prompt_version": "router_prompt_v3",
  "input": {},
  "raw_output": "...",
  "parsed_output": {},
  "validation_errors": [],
  "latency_ms": 842,
  "input_tokens": 1200,
  "output_tokens": 130,
  "cost_estimate": 0.0,
  "eval_matches": {},
  "pollution_components": {}
}
```

Demo traces should additionally log:

- Candidate memories shown to router.
- Selected read memories.
- Proposed write spans.
- Ignored spans.
- Memory store before/after.
- Whether memory write was accepted by the controller stub.

### 15.2 Minimal Memory Store

Use a JSONL memory store:

```json
{
  "id": "m17",
  "type": "decision",
  "content": "Steam SDK integration is postponed.",
  "source_turn_id": "trace_03_t04",
  "created_at": "...",
  "status": "active"
}
```

No merge, delete, decay, or embedding database is required for the MVP.

Because the router does not generate final memory content, the demo can use a simple controller stub:

```text
Accepted write spans are stored as provisional memory content for demo purposes.
```

State clearly that this is not the research target.

## 16. Multi-Turn Trace Demo

Multi-turn traces are not the main evaluation target, but they are important for demonstrating agent-memory continuity.

MVP target:

```text
6-8 traces
4-8 turns each
```

Stretch target:

```text
12-20 traces
4-8 turns each
```

Coverage:

- Project rule accumulation.
- Task continuation.
- Correction.
- Temporary noise ignored.
- Conflicting memories.
- Multi-span write.
- Light game-dev scenarios.
- Coding workflow scenarios.

Use cases:

- README demo.
- Trace replay.
- Supplementary analysis.

## 17. Suggested Repository Structure

```text
README.md
docs/
  report.md
  related_work.md
  annotation_guidelines.md
data/
  seed_examples.jsonl
  train.jsonl
  dev.jsonl
  gold_eval.jsonl
  multi_turn_traces.jsonl
src/
  schemas.py
  data_generation/
  validation/
  teacher/
  baselines/
  harness/
  eval/
  training/
  inference/
results/
  eval_tables.md
  error_analysis.md
resume_bullets.md
```

## 18. Time Allocation

Recommended allocation:

```text
15% problem definition + schema + annotation guidelines
20% dataset generation + validation + gold review
15% prompt teacher + minimal harness
15% baselines + eval runner
20% LoRA/SFT training + inference
10% report / README / resume bullets
5% buffer
```

LoRA/SFT is important, but the research value comes from the full chain:

```text
schema -> dataset -> teacher -> baselines -> evaluation -> analysis
```

## 19. Suggested 10-Day Deliverable Boundary

This is not a rigid daily plan, but a realistic boundary for execution:

```text
Day 1: Final schema, annotation policy, 50 seed examples
Day 2: Generation prompts, validator, first 1k examples
Day 3: Full synthetic train/dev/gold draft
Day 4: Gold review, offsets, dedup, family split
Day 5: Eval runner and span matching
Day 6: Baselines and prompt teacher evaluation
Day 7: Student bake-off and final model choice
Day 8: LoRA/QLoRA training and inference script
Day 9: Final evaluation, error analysis, trace demo
Day 10: README, report, resume bullets, cleanup
```

If time slips, preserve the clean evaluation and report before expanding model or data scale.

## 20. Deliverables

Final deliverables:

- Working repository.
- English README.
- Annotation guidelines.
- Dataset generation scripts.
- Validated train/dev/gold eval JSONL files.
- Prompt teacher pipeline.
- Minimal CLI harness.
- Baseline evaluation scripts.
- LoRA/SFT training script.
- Inference script for fine-tuned router.
- Evaluation tables.
- Error analysis.
- Multi-turn trace demo.
- Resume bullets.

## 21. README and Report Structure

README:

```text
1. What this project is
2. What this project is not
3. Quickstart
4. Schema
5. Dataset
6. Baselines
7. Evaluation metrics
8. Results table
9. Trace demo
10. Limitations
11. Future work
```

Report:

```text
1. Problem definition
2. Related work
3. Schema and task formulation
4. Dataset construction
5. Models and baselines
6. Evaluation methodology
7. Results
8. Error analysis
9. Limitations
10. Future work
```

## 22. Resume / README Positioning

Example English resume bullet:

> Built a distilled Memory Policy Router for coding-agent contexts, framing agent memory control as structured read/write/ignore span prediction. Generated and validated a synthetic dataset, fine-tuned a 3B-4B router with LoRA/SFT, and compared it against empty, naive, rule-based, zero-shot, and prompt-teacher baselines using span F1, type accuracy, JSON validity, latency, and memory-pollution component analysis.

Project positioning:

> This project does not build a full autonomous coding agent. It focuses on a reusable memory attention router that can be plugged into coding-agent workflows.

## 23. Key Risks and Mitigations

### Risk 1: Synthetic data becomes too templated

Mitigation:

- Use capability categories.
- Use multiple generation prompts.
- Use two-stage scenario-card generation.
- Deduplicate.
- Use family-based split.
- Manually review gold eval.

### Risk 2: Small model JSON output is unstable

Mitigation:

- Run a small Qwen3/Qwen2.5-Coder bake-off.
- Treat Qwen3.5 as an optional smoke test.
- Use Pydantic validation.
- Use strict output prompts.
- Track repair rate separately if repair is enabled.

### Risk 3: Ignore labels become too broad

Mitigation:

- Only label pollution-prone spans.
- Do not label all leftover text as ignore.

### Risk 4: LoRA training delays the whole project

Mitigation:

- Make prompt teacher + eval + baselines work first.
- Treat LoRA as an enhancement experiment, not the only proof of project value.

### Risk 5: Project scope expands into full Agent Memory OS

Mitigation:

- Keep the router scope explicit.
- Put delete/update/merge/conflict-resolution into future work.
- Keep Pi/godogen integration optional.

### Risk 6: Type labels become inconsistent

Mitigation:

- Write annotation guidelines before bulk generation.
- Use tie-breaker rules.
- Review `decision` vs `task_state` errors explicitly.

## 24. Suggested Related Work

Priority reading:

- Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers.
- Memory in the Age of AI Agents: A Survey.
- From Human Memory to AI Memory.
- A Survey on the Memory Mechanism of LLM-based Agents.
- MemGPT.
- LongMemEval.
- LoCoMo.

Use related work mainly to support:

- Why memory policy matters.
- Why write-gating / ignore behavior matters.
- Why this project focuses on read/write/ignore attention hints rather than full memory management.
- Why this is adjacent to but distinct from ordinary RAG retrieval.

## 25. Future Work

- Add uncertainty-aware routing or `needs_review`.
- Add calibrated confidence.
- Add correction-aware memory rewriting.
- Add related memory ID linking.
- Add update/delete operations.
- Add richer conflict resolution.
- Add classifier-style sentence baseline.
- Add no-ignore / write-only ablation.
- Add Summary Memory baseline.
- Add LLM semantic judge audit at larger scale.
- Integrate with Pi / pi-agent.
- Integrate with Claude Code-style workflows.
- Integrate with godogen / game-development agent workflow.
- Evaluate in a real coding-agent loop.

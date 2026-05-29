# Distilled Memory Policy Router for Business-Memory Coding Agents

Version: v0.3  
Date: 2026-05-28  
Status: Re-scoped canonical project spec  
Archive: `docs/planning/archive/lightweight_memory_policy_router_project_spec_v0.2.md`

## Changelog

- v0.3 re-scopes the project from an offline router benchmark into a
  business-memory agent utility study.
- The offline router evaluation is retained as an intrinsic/component test.
  It is no longer the headline result.
- The headline MVP now includes a small downstream ablation with a fixed
  DeepSeek V4 Flash main agent. The only changed variable in that ablation is
  the memory-policy source.
- Model roles are renamed:
  - DeepSeek V4 Pro/Max = synthetic label source / source teacher / optional
    offline ceiling router baseline.
  - DeepSeek V4 Flash = offline router baseline, downstream self-routing
    baseline, and fixed downstream main agent. It is not called the teacher.
  - Fine-tuned small router = proposed memory-policy controller.
- Added raw and normalized metric reporting, decomposed read/write/ignore
  precision-recall metrics, cost/latency logging, a fixed trivial writer, and
  a downstream business-memory scenario ablation.

## 0. One-Sentence Summary

A small memory-policy router, distilled from stronger synthetic supervision
from DeepSeek V4 Pro/Max, is evaluated as a low-cost memory controller for a
fixed cost-sensitive DeepSeek V4 Flash agent, with the goal of improving
business-memory behavior: retaining relevant facts, preferences/decisions, and
task progress while reducing irrelevant reads and noisy or sensitive writes.

## 1. Project Motivation

The original business problem is practical: how can an AI coding or business
agent reliably remember business progress, business facts, and user/team
preferences without polluting memory with temporary, noisy, sensitive,
incorrect, or irrelevant content?

The project focuses on two policy decisions:

- When should memory be read, and which candidate memories should be injected?
- When should new durable memory be written, and which spans should be ignored?

The project does not build a complete memory operating system or autonomous
coding agent. It studies a narrow control-plane component that can sit before a
medium/strong main agent such as DeepSeek V4 Flash.

## 2. Core Research Questions and Hypotheses

Primary downstream question:

> When the memory-policy source is the only changed variable, does substituting
> a fine-tuned small router for DeepSeek V4 Flash self-routing improve the
> business-memory behavior of a fixed DeepSeek V4 Flash agent without hurting
> task success, at lower routing cost and latency?

Secondary intrinsic question:

> Does the fine-tuned router beat naive, rule-based, zero-shot, and DeepSeek
> V4 Flash router baselines on human-reviewed gold data, and how much of the
> optional DeepSeek V4 Pro/Max routing ceiling does it retain?

Hypotheses:

- **H1 intrinsic:** Fine-tuning improves JSON/schema validity and decomposed
  read/write/ignore metrics over the same student model in zero-shot mode, and
  improves write quality over deterministic rules and DeepSeek V4 Flash
  router baseline on human-reviewed gold.
- **H2 downstream:** Fine-tuned-router + DeepSeek V4 Flash main agent matches
  or improves DeepSeek V4 Flash self-routing on business-fact recall,
  preference/decision adherence, and task/progress continuity, while reducing
  irrelevant reads and noisy/sensitive writes.
- **H3 cost/control:** Fine-tuned-router + DeepSeek V4 Flash achieves H2 at
  lower routing token cost and latency than DeepSeek V4 Flash self-routing,
  and with lower injected-memory token cost than inject-all.

The project should be evaluated as a research-engineering system study. Do not
claim that the router solves general agent memory or beats the Pro/Max ceiling.

## 3. MVP and Stretch Boundary

### 3.1 Must-Finish MVP

Completed or required MVP assets:

```text
Seed examples: 50
Synthetic train: 5,000 examples
Dev: 250 examples
Gold eval: 300 human-reviewed examples
Multi-turn traces: 6-8 traces
Source teacher / synthetic label source: DeepSeek V4 Pro/Max
Fixed downstream main agent: DeepSeek V4 Flash
Student: one selected 3B-4B model
Fine-tuning: one final LoRA/QLoRA router
Intrinsic baselines: empty, all-read, rule-based, V4 Flash router baseline,
  zero-shot student, fine-tuned student, optional Pro/Max ceiling router
Downstream ablation: 12-16 business-memory scenarios, conditions A-E
Docs: README, report, error analysis, claims table, resume bullets
```

### 3.2 Stretch Version

Only after the MVP is complete:

```text
Synthetic train: 10,000-15,000 examples
Gold eval: 500-800 examples
More downstream scenarios
Full three-model bake-off
Optional non-Qwen comparison
Optional Pro/Max downstream ceiling on all scenarios
No-ignore / write-only ablation
LLM semantic judge audit
Richer coding-repo or game-dev workflow traces
```

Do not touch real Godot/godogen integration during the MVP.

## 4. Scope

### 4.1 In Scope

- Structured router I/O for `read_hints`, `write_spans`, and `ignore_spans`.
- Synthetic English dataset generation and repair.
- Programmatic validation and human-reviewed gold evaluation.
- Intrinsic offline router evaluation on dev/gold.
- Deterministic baselines: empty, all-read, rule-based.
- DeepSeek V4 Flash as an offline router baseline and downstream self-routing
  baseline.
- One selected 3B-4B student, zero-shot and fine-tuned.
- LoRA/QLoRA fine-tuning for one final router.
- Raw and normalized span evaluation.
- Cost and latency logging for routing decisions.
- A small downstream business-memory ablation using a fixed DeepSeek V4 Flash
  main agent.
- A fixed trivial writer for downstream evaluation.
- Memory-pollution analysis: irrelevant reads, false durable writes,
  noisy/sensitive writes, missed critical memory.

### 4.2 Out of Scope for MVP

- Full autonomous coding agent implementation.
- Full game-development agent implementation.
- Full Agent Memory OS.
- Full retrieval from an unbounded memory database.
- Intelligent memory writing, merging, deduplication, decay, deletion,
  canonicalization, or truth verification.
- Final `memory.md` generation.
- Project-ID management, confidence scores, or `needs_review`.
- Online/continual learning.
- Real production traffic.
- Claims of production-scale generalization.
- Public benchmark adaptation as the main proof.

### 4.3 MVP Limitation

The intrinsic router task evaluates second-stage memory policy given a small
candidate set. It does not solve end-to-end memory retrieval.

The downstream ablation is a controlled pilot, not a production benchmark. It
tests whether memory-policy source changes business-memory behavior under a
fixed medium-strength main agent.

## 5. System Architecture

### 5.1 Intrinsic Router Layer

```text
Current user input + recent context + candidate memories
        |
        v
Memory Policy Router
        |
        v
{ read_hints, write_spans, ignore_spans }
        |
        v
Evaluator vs dev/gold targets
```

This layer answers: did the router predict the right policy object?

### 5.2 Downstream Business-Memory Layer

```text
Session turns + candidate memories
        |
        v
Memory-policy source (A-E)
        |
        v
Fixed trivial writer + memory injection
        |
        v
Fixed DeepSeek V4 Flash main agent
        |
        v
Probe answers + memory store changes + cost/latency logs
```

This layer answers: did the memory-policy source improve business-memory
behavior for the fixed main agent?

### 5.3 Minimal Downstream Agent Harness

The downstream agent is a fixed scenario runner, not an autonomous coding
agent. It has no tools, no repository access, no planner, and no memory
lifecycle intelligence. Its only purpose is to measure whether changing the
memory-policy source changes the behavior of a fixed DeepSeek V4 Flash
answerer.

The harness should contain only:

- a scenario runner;
- a policy adapter for conditions A-E;
- a flat JSON memory store;
- a fixed trivial writer;
- a memory injector;
- a fixed DeepSeek V4 Flash answerer;
- a scorer and cost/latency logger.

The harness must keep the scenario text, candidate memories, writer, answer
prompt, model settings, and scoring logic fixed across conditions. The only
changed variable is the memory-policy source. This keeps the downstream test a
controlled ablation rather than a new agent product.

## 6. Router Input and Output Contract

All dataset content should be in English.

Each decision case has:

- `current_user_input`
- `recent_context`: 0-4 turns
- `candidate_memories`: 0-8 items
- `target`: router prediction target

The router predicts only:

```json
{
  "read_hints": [],
  "write_spans": [],
  "ignore_spans": []
}
```

Constraints:

- `read_hints` entries must reference candidate memory IDs present in the same
  case.
- `write_spans[*].span` must be an exact substring of `current_user_input`.
- `write_spans[*].type` must be one of `fact`, `decision`, `sop`,
  `task_state`.
- `ignore_spans[*]` must be exact substrings of `current_user_input`.
- The router must not output final memory text, offsets, confidence,
  `needs_review`, project IDs, update/delete/merge decisions, or downstream
  actions.

## 7. Memory Types and Business Priority

Primary business-memory labels:

- `fact`: stable facts, locations, ownership, configuration, tooling, or
  business values.
- `decision`: explicit choices, preferences, selected plans, or agreed
  directions.
- `task_state`: progress, blocked/pending work, active investigations, or
  completion status.

Secondary label:

- `sop`: recurring procedures, policies, or required practices.

SOP remains a first-class label in the dataset and is reported, but it is
secondary in the business-memory thesis because production SOP may often be
handled by skills or explicit instructions. The downstream MVP should include
only a small number of SOP-bearing scenarios to verify SOP neutrality rather
than claiming SOP optimization.

## 8. Ignore Span Policy

Use `ignore_spans` for content that should not become durable memory:

- temporary or local failures;
- flaky test or CI noise that resolved;
- casual chatter or emotional venting;
- secrets, tokens, passwords, personal data, or should-not-store content;
- stale facts after a correction, when the stale text appears in the current
  user input;
- irrelevant event details that are not useful for future work.

The router does not verify factual truth. "Avoid incorrect memory" is measured
only through corrected/superseded-fact scenarios where stale content should not
resurface.

## 9. Dataset Assets

Authoritative MVP assets:

- Train: `data/processed/synthetic_train_5000.jsonl`
- Dev: `data/dev/dev_250.jsonl`
- Gold: `data/gold/gold_eval_300.jsonl`
- Gold offsets sidecar: `data/gold/gold_eval_300.offsets.jsonl`
- Multi-turn traces: `data/traces/multiturn_traces_8.jsonl`

The 5,000-record train split was assembled from accepted and repaired
DeepSeek V4 Pro/Max generation batches. It is not directly distilled from
DeepSeek V4 Flash.

After any change to `data/*.jsonl`, run the dataset validator.

## 10. Model Roles

DeepSeek V4 Pro/Max:

- Role: source teacher / synthetic label source for the bulk of the 5,000
  training labels, followed by repair and validation.
- Optional role: offline ceiling router baseline to measure how much strong
  routing quality the small student retained.
- Not used as the fixed downstream main agent.

DeepSeek V4 Flash:

- Role 1: offline strong-LLM router baseline on dev/gold.
- Role 2: downstream self-routing baseline, condition D.
- Role 3: fixed downstream main agent in all downstream conditions.
- Never call V4 Flash the teacher unless a future run actually uses it to
  create labels.

Fine-tuned small router:

- Role: proposed memory-policy controller.
- Distilled from stronger repaired synthetic supervision.
- Predicts only `{read_hints, write_spans, ignore_spans}`.

Student model candidates:

```text
Primary: Qwen3-4B-Instruct-2507
Fallback: Qwen2.5-Coder-3B-Instruct
Optional smoke: Qwen3.5-4B
```

Use LoRA or QLoRA, not full fine-tuning.

## 11. Intrinsic Baselines

Required intrinsic baselines:

- `empty`: no reads, no writes, no ignores.
- `all-read`: read every candidate memory; no writes or ignores.
- `rule-based`: deterministic lexical read/write/ignore heuristics.
- `v4flash-router`: DeepSeek V4 Flash predicts the router target from the
  same router prompt.
- `student-zero-shot`: selected small student predicts without fine-tuning.
- `student-finetuned`: selected small student after LoRA/QLoRA.
- `promax-router` optional: DeepSeek V4 Pro/Max as an offline ceiling.

Report all systems with the same evaluator and the same raw/normalized matching
policy.

## 12. Downstream Ablation Conditions

Use 12-16 synthetic business-memory scenarios. The fixed main agent is always
DeepSeek V4 Flash. The only changed variable is memory-policy source.

| Condition | Policy source | Purpose |
| --- | --- | --- |
| A | no long-term memory | floor; verifies memory is needed |
| B | inject all candidate memories | context-cost and pollution reference |
| C | rule-based router | cheap non-neural baseline |
| D | V4 Flash self-routing | make-or-break comparison |
| E | fine-tuned small router | proposed system |
| F optional | Pro/Max router | ceiling/reference, budget permitting |

Fixed across conditions:

- scenario set;
- candidate-memory pool;
- fixed trivial writer;
- final answer prompt;
- V4 Flash main agent model/version;
- scoring logic;
- temperature/decoding where feasible.

The fixed trivial writer maps accepted `write_spans` into store entries:

```json
{
  "id": "generated_entry_id",
  "type": "fact|decision|sop|task_state",
  "text": "normalized or verbatim accepted span",
  "source_turn": "scenario_turn_id"
}
```

It performs no merge, deduplication, decay, rewrite, truth check, or memory.md
generation.

## 13. Downstream Scenario Shape

Downstream scenarios are separate from `DecisionCase` JSONL. They should keep
router-target semantics compatible with the existing schema but may use their
own scenario-level fields.

Each scenario should include:

- Session A with planted durable business facts, preferences/decisions, and
  task-state/progress.
- Temporary, irrelevant, and sensitive distractors.
- Optional superseded/stale facts for correction behavior.
- Session B/C probe turns that require the right memory and must not surface
  the wrong memory.
- Candidate memories supplied to the router at probe time.
- Scoring keys and rubrics.

Scenario target counts:

- 12-16 scenarios total.
- Every scenario has at least one fact, preference/decision, task_state, and
  distractor.
- At least 3 superseded-fact scenarios.
- 2-3 SOP-bearing scenarios for neutrality.
- At least 2 scenarios where inject-all can actively hurt.

Do not require a real repository, filesystem tools, or autonomous code
execution in the MVP downstream ablation.

## 14. Metrics

### 14.1 Intrinsic Metrics

Report raw and normalized values for every system.

Primary metrics:

- read precision / recall / F1;
- write span precision / recall / F1;
- typed write span F1;
- ignore span precision / recall / F1;
- noisy/sensitive write rate;
- routing token cost;
- routing latency.

Secondary metrics:

- exact target match;
- per-category breakdown;
- per-type breakdown;
- JSON validity;
- schema validity;
- optional Pro/Max retention ratio.

Do not report only micro-F1. Read precision and write precision/recall are
especially important because all-read can have high recall while being exactly
the pathology the router is meant to avoid.

### 14.2 Downstream Metrics

Primary downstream metrics:

- business fact recall;
- preference/decision adherence;
- task/progress continuity;
- final answer correctness;
- irrelevant memory reads;
- missed critical memory;
- false durable writes;
- noisy/sensitive writes;
- injected memory token count;
- routing token cost;
- total downstream token cost;
- routing and answer latency.

Secondary downstream metrics:

- memory store growth;
- per-scenario breakdown;
- cost-vs-business-quality frontier;
- safety axis.

Business quality:

```text
BQ = mean(fact_recall, preference_adherence, task_continuity, answer_correctness)
```

Safety should be reported separately and must not be hidden inside a composite:

```text
SAFETY = 1 - noisy_sensitive_write_rate_downstream
```

## 15. Span Normalization and Matching

Report both:

- raw exact metrics;
- normalized overlap metrics.

Normalization is a scoring/matching function, not a mutation of stored gold.
Apply it uniformly to every predictor:

- rule-based;
- V4 Flash router baseline;
- Pro/Max router baseline if used;
- zero-shot student;
- fine-tuned student.

Allowed deterministic normalization:

- trim whitespace and surrounding punctuation;
- lowercase for comparison keys;
- collapse internal whitespace;
- strip a frozen closed list of leading discourse markers for write spans;
- strip a frozen closed list of ignore-directive prefixes for ignore spans;
- token-set F1 matching with a frozen threshold, initially 0.8.

Forbidden:

- paraphrase matching;
- embeddings;
- synonym expansion;
- per-system normalizers;
- marker-list edits after seeing student results;
- normalizing only the student.

Commit and freeze `normalizer_markers.txt` before student evaluation. Report
raw and normalized results side by side. If a gain exists only after
normalization, say so.

## 16. Cost and Latency Logging

Every routing source should log:

- model/provider name;
- model version/date when available;
- prompt token count;
- completion token count;
- total routing tokens;
- wall-clock routing latency;
- parse or schema repair status;
- raw output retention path if applicable.

Downstream runs should also log:

- injected-memory token count;
- final-answer token count;
- total scenario token count;
- answer latency;
- condition ID;
- scenario ID;
- seed/temperature.

## 17. Suggested Day 6-Day 10 Boundary

```text
Day 6: Lock v0.3 spec, normalizer, decomposed metrics, cost/latency logging.
Day 7: Run V4 Flash router baseline, optional Pro/Max ceiling, student bake-off,
       and fine-tune/evaluate the selected small router offline.
Day 8: Build downstream harness and author 12-16 business-memory scenarios.
Day 9: Run downstream A-E ablation, optional F subset.
Day 10: Analyze cost-quality frontier, write final report, README, error
        analysis, limitations, and resume bullets.
```

If time slips, cut scenario count before cutting condition D. V4 Flash
self-routing is the load-bearing downstream comparison.

## 18. Claims and Limitations

Safe claims if measured:

- A small router learns structured read/write/ignore and beats naive baselines
  on human-reviewed gold.
- The fine-tuned router beats DeepSeek V4 Flash as an offline router baseline
  if the measured gold results show it.
- The fine-tuned router improves a fixed DeepSeek V4 Flash agent's
  business-memory behavior in a controlled pilot if condition E beats D on the
  downstream metrics.
- The router lowers routing cost/latency if measured costs show it.

Conditional claims:

- The router retains most of the Pro/Max ceiling at small-model cost, only if
  Pro/Max ceiling evaluation is run.
- The router avoids stale-fact resurfacing, only on superseded-fact scenarios.

Overclaims:

- The router beats DeepSeek V4 Pro/Max.
- The router solves general agent memory.
- The router verifies factual correctness.
- The router manages full memory lifecycle.
- The downstream pilot proves production-scale generalization.
- Small-scenario downstream results are statistically significant.

## 19. Key Risks and Mitigations

- **V4 Flash self-routing may be good enough.** Treat this as the core
  empirical question. If D beats E at comparable effective cost, report that
  the router is not justified.
- **Rule-based already handles read/ignore well.** Locate contribution in write
  quality, read precision, and downstream cost/behavior.
- **Synthetic train may not match deployment.** Evaluate on human-reviewed gold
  and downstream hand-authored business scenarios.
- **Normalization may flatter one system.** Freeze marker lists before student
  evaluation and apply uniformly.
- **Writer can become a confound.** Use one fixed trivial writer across all
  downstream conditions.
- **The router only spans user input.** Scope v0.3 to user-turn durable content;
  assistant/tool-turn writes are future work.
- **The router cannot verify truth.** Use superseded-fact scenarios as a proxy
  and keep truth verification out of scope.

## 20. Final Deliverables

- Working repository.
- Canonical v0.3 spec and archived v0.2 spec.
- Annotation guidelines.
- Dataset generation scripts.
- Validated train/dev/gold JSONL files.
- Intrinsic prediction/evaluation harness.
- Normalizer and raw/normalized metric reports.
- Cost/latency logging.
- Baseline evaluation scripts.
- Fine-tuned router training and inference scripts.
- Downstream business-memory scenario set and validator.
- Fixed downstream harness with conditions A-E.
- Evaluation tables and cost-vs-business-quality frontier.
- Error analysis and limitations.
- README and final report.
- Resume bullets.

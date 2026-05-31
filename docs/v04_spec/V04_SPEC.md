# V04_SPEC

Version: v0.4 draft  
Status: P1 interface specification draft  
Scope: unit-based `READ / STORE / SKIP` memory policy router

## 1. Goals And Non-Goals

### Goals

v0.4 defines a small, explicit memory-policy router interface for coding/business-agent contexts.

The router predicts only:

```text
READ: which candidate memories should be injected into context
STORE: which current units should enter the durable memory pipeline, and to which target
SKIP: which current units should not be stored
```

The v0.4 pilot studies whether unit IDs and a low-entropy DSL are more stable than exact-span JSON output, especially for 3B-4B local models.

### Non-Goals

v0.4 does not implement:

```text
MemoryOS
retriever
BM25 / vector DB / RRF
memory DB
intelligent writer
canonical rewrite of stored memory
ADD / UPDATE / DELETE / MERGE
entity resolution
LLM unitizer
LoRA / SFT training
complete downstream agent benchmark
confidence / reason / entity / subtype fields
```

The v0.4 router is an interface pilot, not a complete memory system.

## 2. Input Structure

Each v0.4 decision case has three logical input sections:

```text
RUNTIME_CONTEXT
CANDIDATE_MEMORIES
CURRENT_UNITS
```

The model receives already-formed current units. Unitization is out of scope for v0.4.

### 2.1 RUNTIME_CONTEXT

`runtime_context` describes the active work context used to disambiguate memory targets.

Fields:

| Field | Meaning |
| --- | --- |
| `project` | The larger project or initiative currently being worked on. |
| `repo` | The repository currently being discussed or edited. |
| `service` | The service, module, package, or component currently in focus. |
| `task` | The immediate task, milestone, bug, investigation, or work item. |

These fields are context hints only. The router must not invent new project IDs, repo IDs, service IDs, or task IDs in output.

### 2.2 CANDIDATE_MEMORIES

`candidate_memories` is a fixed, already-retrieved small set. v0.4 does not retrieve from an unbounded store.

Fields:

| Field | Meaning |
| --- | --- |
| `memory_id` | Stable ID for the candidate memory within the case, such as `m1`. |
| `target` | The memory bucket where the candidate currently belongs. Must be one of the five legal targets. |
| `content` | The candidate memory text shown to the router. |

The router may only READ candidate memories whose IDs appear in this section.

### 2.3 CURRENT_UNITS

`current_units` is the pre-segmented current input.

Fields:

| Field | Meaning |
| --- | --- |
| `unit_id` | Stable ID for one current unit within the case, such as `u1`. |
| `text` | The current unit text. |

The router may only STORE or SKIP unit IDs that appear in this section.

## 3. Output DSL Grammar

The model raw output is a compact DSL:

```text
READ m1,m3
STORE task_state u1
STORE repo_memory u2
SKIP u3
```

Empty values use `NONE`:

```text
READ NONE
STORE NONE
SKIP u1,u2
```

### 3.1 Line Types

Allowed line forms:

```text
READ <memory_id_list|NONE>
STORE <target> <unit_id>
STORE NONE
SKIP <unit_id_list|NONE>
```

`<memory_id_list>` is a comma-separated list such as:

```text
m1,m3,m4
```

`<unit_id_list>` is a comma-separated list such as:

```text
u1,u2
```

Whitespace around commas may be accepted by the parser as mechanical normalization:

```text
READ m1, m3
SKIP u1, u2
```

## 4. DSL Rules

Required structural rules:

- `READ` appears at most once.
- `STORE` may appear multiple times.
- `SKIP` appears at most once.
- `READ NONE` means no candidate memory should be read.
- `STORE NONE` means no current unit should be stored.
- `SKIP NONE` means no current unit should be skipped.
- `READ` may only reference IDs from `candidate_memories`.
- `STORE` and `SKIP` may only reference IDs from `current_units`.
- Every current unit must appear exactly once in either `STORE` or `SKIP`.
- A current unit may STORE to only one target in v0.4.
- A current unit may not appear in both `STORE` and `SKIP`.
- `STORE target` must be one of the five legal STORE targets.
- The parser must not infer a missing READ, STORE, SKIP, unit, memory ID, or target from text.

Recommended duplicate policy:

- Duplicate memory IDs within one `READ` line may be mechanically deduplicated in canonical JSON.
- Duplicate STORE assignments, duplicate SKIP assignments, or any STORE/SKIP conflict for the same unit should be validation errors.
- Duplicate line types that are capped at one line, such as two `READ` lines or two `SKIP` lines, should be validation errors.

## 5. Legal STORE Targets

The only legal STORE targets are:

```text
user_profile
project_memory
repo_memory
service_memory
task_state
```

No other targets are legal in v0.4.

## 6. Canonical JSON Output

Parser output should use a canonical JSON shape:

```json
{
  "schema_version": "memory_policy.v0.4",
  "read": [
    {"memory_id": "m1"},
    {"memory_id": "m3"}
  ],
  "store": [
    {"target": "task_state", "unit_id": "u1"},
    {"target": "repo_memory", "unit_id": "u2"}
  ],
  "skip": [
    {"unit_id": "u3"}
  ],
  "validation": {
    "valid": true,
    "errors": []
  }
}
```

Invalid output should still be represented with the same top-level shape when possible:

```json
{
  "schema_version": "memory_policy.v0.4",
  "read": [],
  "store": [],
  "skip": [],
  "validation": {
    "valid": false,
    "errors": [
      "unknown memory_id: m9",
      "unit u2 appears in both STORE and SKIP"
    ]
  }
}
```

## 7. Parser Responsibility Boundary

The parser may:

- parse DSL lines;
- validate memory IDs against candidate memories;
- validate unit IDs against current units;
- validate STORE targets against the five legal targets;
- detect duplicate or conflicting assignments;
- mechanically deduplicate repeated READ IDs;
- sort canonical output deterministically;
- convert valid DSL to canonical JSON;
- report validation errors.

The parser must not:

- guess a STORE target from unit text;
- infer missing READ memories from candidate memory content;
- infer missing STORE or SKIP units from current unit text;
- rewrite illegal targets into legal targets;
- split, merge, or rewrite current units;
- repair semantically wrong model outputs;
- improve metrics by silently correcting predictions.

## 8. A/B/C Interface Comparison

v0.4 compares three interfaces.

### A. Legacy Span JSON

The v0.3-style interface:

```json
{
  "read_hints": ["m1"],
  "write_spans": [
    {"span": "parser is almost complete", "type": "task_state"}
  ],
  "ignore_spans": ["check today's weather"]
}
```

This validates the historical baseline and measures exact-span copying and complex JSON failure modes.

### B. Unit JSON

A unit-based JSON interface:

```json
{
  "read": ["m1"],
  "store": [
    {"target": "task_state", "unit_id": "u2"}
  ],
  "skip": ["u3"]
}
```

This isolates whether unit IDs reduce span-copying errors while keeping JSON as the raw model output.

### C. Unit DSL

The proposed v0.4 raw interface:

```text
READ m1
STORE task_state u2
SKIP u3
```

This tests whether low-entropy DSL output improves parse success and schema stability without reducing semantic routing quality.

## 9. Examples

### 9.1 READ-only

Input:

```text
RUNTIME_CONTEXT
project: memory-router
repo: distilled-memory-policy-router
service: evaluation
task: review baseline results

CANDIDATE_MEMORIES
m1 [project_memory]: v0.4 is an interface pilot before v0.5 training.
m2 [repo_memory]: Evaluation reports live under results/eval/reports.
m3 [task_state]: Parser implementation has not started yet.

CURRENT_UNITS
u1: Show me the latest eval report location before we write the summary.
```

DSL:

```text
READ m2
STORE NONE
SKIP u1
```

Canonical JSON:

```json
{
  "schema_version": "memory_policy.v0.4",
  "read": [{"memory_id": "m2"}],
  "store": [],
  "skip": [{"unit_id": "u1"}],
  "validation": {"valid": true, "errors": []}
}
```

### 9.2 STORE/SKIP-only

Input:

```text
RUNTIME_CONTEXT
project: memory-router
repo: distilled-memory-policy-router
service: parser
task: prepare v0.4 parser implementation

CANDIDATE_MEMORIES

CURRENT_UNITS
u1: The parser should reject unknown STORE targets.
u2: Also, remind me to buy coffee after this.
u3: The parser tests should cover duplicate unit assignment.
```

DSL:

```text
READ NONE
STORE service_memory u1
STORE repo_memory u3
SKIP u2
```

Canonical JSON:

```json
{
  "schema_version": "memory_policy.v0.4",
  "read": [],
  "store": [
    {"target": "service_memory", "unit_id": "u1"},
    {"target": "repo_memory", "unit_id": "u3"}
  ],
  "skip": [{"unit_id": "u2"}],
  "validation": {"valid": true, "errors": []}
}
```

### 9.3 READ + STORE Joint

Input:

```text
RUNTIME_CONTEXT
project: memory-router
repo: distilled-memory-policy-router
service: docs
task: write v0.4 spec

CANDIDATE_MEMORIES
m1 [project_memory]: v0.3 is frozen as prototype and baseline evidence.
m2 [project_memory]: v0.4 compares Legacy Span JSON, Unit JSON, and Unit DSL.
m3 [repo_memory]: Do not modify old v0.3 data files during v0.4 setup.

CURRENT_UNITS
u1: Keep using docs/v04_planning as the canonical planning directory.
u2: Do not touch docs/v04-planning for now.
u3: After this, please check tomorrow's weather.
```

DSL:

```text
READ m1,m2,m3
STORE repo_memory u1
STORE task_state u2
SKIP u3
```

Canonical JSON:

```json
{
  "schema_version": "memory_policy.v0.4",
  "read": [
    {"memory_id": "m1"},
    {"memory_id": "m2"},
    {"memory_id": "m3"}
  ],
  "store": [
    {"target": "repo_memory", "unit_id": "u1"},
    {"target": "task_state", "unit_id": "u2"}
  ],
  "skip": [{"unit_id": "u3"}],
  "validation": {"valid": true, "errors": []}
}
```

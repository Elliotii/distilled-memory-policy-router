# CASE_SCHEMA

Version: v0.4 draft  
Status: P2.5 case schema and bridge preparation draft  
Scope: JSONL record format for v0.4 bridge and pilot cases

## 1. Purpose

This schema defines the JSONL record shape for v0.4 unit-based `READ / STORE / SKIP`
memory policy cases.

It is for curated bridge and pilot data. It is not a v0.3 data conversion format,
not an eval runner, and not a MemoryOS schema.

## 2. Top-Level Record

Each JSONL line is one case record:

```json
{
  "case_id": "v04_bridge_0001",
  "runtime_context": {},
  "candidate_memories": [],
  "current_units": [],
  "gold": {},
  "tags": [],
  "notes": ""
}
```

Required top-level fields:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `case_id` | string | yes | Stable case ID, unique within the dataset. |
| `runtime_context` | object | yes | Project/repo/service/task context. |
| `candidate_memories` | array | yes | Already-retrieved candidate memory set. |
| `current_units` | array | yes | Pre-segmented current input units. |
| `gold` | object | yes | Gold READ / STORE / SKIP labels. |
| `tags` | array of strings | yes | Case type and analysis tags. |
| `notes` | string | yes | Human annotation notes. |

## 3. runtime_context

Shape:

```json
{
  "project": "memory-router",
  "repo": "distilled-memory-policy-router",
  "service": "parser",
  "task": "v0.4 case schema preparation"
}
```

Fields:

| Field | Meaning |
| --- | --- |
| `project` | Larger project or initiative currently being worked on. |
| `repo` | Repository currently being discussed or edited. |
| `service` | Service, module, package, or component currently in focus. |
| `task` | Immediate task, milestone, investigation, or work item. |

`runtime_context` is a disambiguation aid only. Gold labels must not invent
project IDs, repo IDs, service IDs, task IDs, or downstream actions.

## 4. candidate_memories

Shape:

```json
[
  {
    "memory_id": "m1",
    "target": "project_memory",
    "content": "The project is currently validating the v0.4 Unit DSL interface before training."
  }
]
```

Fields:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `memory_id` | string | yes | Case-local candidate memory ID, such as `m1`. |
| `target` | string | yes | Existing memory bucket for this candidate. |
| `content` | string | yes | Candidate memory text shown to the router. |

Rules:

- `memory_id` values must be unique within a case.
- `target` must be one of the five legal targets.
- `gold.read` may only reference IDs present in `candidate_memories`.
- Candidate memories are fixed inputs; the case schema does not implement retrieval.

## 5. current_units

Shape:

```json
[
  {
    "unit_id": "u1",
    "text": "Keep using docs/v04_planning as the canonical planning directory."
  }
]
```

Fields:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `unit_id` | string | yes | Case-local current unit ID, such as `u1`. |
| `text` | string | yes | Already-segmented current unit text. |

Rules:

- `unit_id` values must be unique within a case.
- Unitization is upstream of this schema and is not performed by the validator.
- Every current unit must appear exactly once in `gold.store` or `gold.skip`.

## 6. gold

Recommended shape:

```json
{
  "read": ["m1"],
  "store": [
    {"target": "task_state", "unit_id": "u1"}
  ],
  "skip": ["u2"],
  "dsl": "READ m1\nSTORE task_state u1\nSKIP u2"
}
```

Fields:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `read` | array of strings | yes | Candidate memory IDs that should be read. |
| `store` | array of objects | yes | Units that should enter durable memory pipeline. |
| `skip` | array of strings | yes | Current units that should not be stored. |
| `dsl` | string | optional but recommended | Gold DSL form aligned with `read`, `store`, and `skip`. |

`gold.store` item shape:

```json
{"target": "task_state", "unit_id": "u1"}
```

Gold rules:

- `gold.read` may only reference `candidate_memories[*].memory_id`.
- `gold.store[*].unit_id` may only reference `current_units[*].unit_id`.
- `gold.skip[*]` may only reference `current_units[*].unit_id`.
- Every current unit must appear exactly once in either `gold.store` or `gold.skip`.
- A current unit must not appear in both `gold.store` and `gold.skip`.
- A current unit must not be stored to multiple targets.
- `gold.store[*].target` must be one of the five legal targets.
- If `gold.dsl` exists, parsing it with the strict v0.4 parser must produce the same READ IDs, STORE unit-target mapping, and SKIP IDs as the structured gold fields.

## 7. Legal Targets

The only legal STORE targets are:

```text
user_profile
project_memory
repo_memory
service_memory
task_state
```

Do not add `fact`, `decision`, `preference`, `sop`, `team_memory`, `entity_memory`,
or any other target.

## 8. tags

`tags` is an array of strings used for case mix, filtering, and error analysis.

Recommended tags:

```text
read_only
store_skip_only
read_store_joint
stale_memory
related_but_useless
target_boundary
user_profile_boundary
sensitive_boundary
project_vs_repo
repo_vs_service
service_vs_task_state
```

Tags are not labels. They are analysis metadata.

## 9. notes

`notes` is a short human annotation note.

Use it to explain:

- why a candidate memory is read or not read;
- why a unit is stored or skipped;
- why a target-boundary case chooses one target over another;
- whether a case includes sensitive/private content that must be skipped.

`notes` is especially important for `target_boundary` cases.

## 10. Explicitly Forbidden Gold Fields

v0.4 gold must not use:

```text
fact
decision
preference
sop
type
subtype
reason
entity
confidence
needs_review
ADD
UPDATE
DELETE
MERGE
```

The v0.4 gold object is only:

```text
read memory IDs
store target + unit_id
skip unit IDs
optional DSL string
```

## 11. Sensitive And Private Content

Sensitive/private units must be marked `SKIP`.

Examples:

- tokens;
- passwords;
- private keys;
- API keys;
- personal contact information;
- should-not-store private content.

The validator only checks structure. It does not detect sensitive content
semantically, so human annotation must enforce this rule.

## 12. Template File

`data/v04/bridge_cases_template.jsonl` contains a small set of schema examples.

That file is not the official 30-50 bridge dataset. It exists only to test the
schema and validator before real bridge case creation.

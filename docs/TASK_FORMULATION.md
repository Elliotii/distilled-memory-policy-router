# Task Formulation

## Summary

The task is a unit-level memory-policy prediction problem. Given fixed candidate memories and current units, predict which memories to READ, which units to STORE, which units to SKIP, and which target each STORE unit should use.

The router is evaluated as an intrinsic component: did it produce the same policy object as the locked label? It is not evaluated as a full downstream agent in the current v0.5/v1.0 package.

## Conceptual Input Schema

Each case can be understood as:

| Field | Meaning |
| --- | --- |
| `case_id` | Stable identifier for the decision case. |
| `candidate_memories` | A bounded list of candidate memories, typically addressed as `m1...mk`. |
| `current_units` | A bounded list of current task/dialogue units, typically addressed as `u1...un`. |
| `metadata` | Optional scenario, split, category, or audit metadata. |
| `target` | The locked reference policy object used for evaluation. |

Candidate memories conceptually contain:

- memory ID;
- memory text;
- optional type or source metadata.

Current units conceptually contain:

- unit ID;
- text from the current context;
- optional metadata used for analysis.

The v0.5 unit-based setup assumes candidate memories and current units already exist. It does not evaluate how candidate memories were retrieved or how current units were extracted.

## Conceptual Output Schema

The router predicts:

| Output | Meaning |
| --- | --- |
| READ memory IDs | Candidate memory IDs that should enter the downstream context. |
| STORE units with targets | Current units that should be sent to durable memory handling, each with a target. |
| SKIP unit IDs | Current units that should not become durable memory. |

Every current unit should be assigned consistently: STORE or SKIP, depending on whether it should enter durable memory handling. Candidate memories are independently selected for READ or not selected.

## STORE Targets

| Target | Use when the unit is about... | Typical examples |
| --- | --- | --- |
| `task_state` | Current progress, active work, blockers, next steps, or temporary task state. | "The parser audit is complete; next check the evaluator." |
| `service_memory` | Durable facts about a service, subsystem, component, parser, evaluator, or module. | "The validator accepts empty DSL when structured fields are present." |
| `repo_memory` | Repository layout, commands, tests, local conventions, or codebase facts. | "Run tests with `python3 -m unittest discover -s tests`." |
| `project_memory` | Project-level goals, decisions, cross-repo agreements, or shared constraints. | "v1.0 packaging must avoid presenting the project as a full memory runtime." |
| `user_profile` | Stable, non-sensitive user preferences that transfer across tasks. | "The user prefers concise final reports with commands and validation results." |

Target classification matters because a memory pipeline can route different durable content to different stores, scopes, or review policies. In v0.5g, target classification is the strongest part of the best model: 240/240 compared STORE units were assigned the correct target on locked `gold_v2_009`.

## Evaluation Metrics

| Metric | What it measures |
| --- | --- |
| Parse success | Whether the raw model output can be parsed and structurally validated. |
| Exact match | Whether the complete predicted policy object matches the locked target. |
| READ F1 | Precision/recall/F1 over selected candidate memory IDs. |
| STORE unit F1 | Precision/recall/F1 over current units predicted as STORE. |
| SKIP unit F1 | Precision/recall/F1 over current units predicted as SKIP. |
| Target accuracy | Accuracy of STORE target labels among comparable STORE units. |
| False store rate | Fraction of predicted STORE units that should not have been stored. |
| Irrelevant read rate | Fraction of predicted READ memories that should not have been read. |
| Sensitive store rate | Fraction of sensitive units incorrectly routed to STORE. |

## Why Full Exact Is Strict

Full exact match requires every component to be correct at the same time:

- all required READ memories must be selected;
- no irrelevant READ memories can be selected;
- all STORE units must be stored;
- no SKIP units can be stored;
- all SKIP units must be skipped;
- every STORE target must be correct;
- the output must parse and validate.

This makes exact match intentionally unforgiving. It is useful because a downstream memory pipeline can be harmed by one noisy store or one missing critical memory. It is also why component metrics are necessary: exact match alone hides whether failures come from READ, STORE, SKIP, parsing, or target labels.

## Why READ Errors Dominate Remaining Failures

The best v0.5g system on locked `gold_v2_009` reaches:

| Metric | BF16 r16 1000_4090 |
| --- | ---: |
| Exact match | 36.0% |
| READ F1 | 84.6% |
| STORE F1 | 99.0% |
| SKIP F1 | 98.1% |
| Target accuracy | 100.0% |

The write side is near ceiling under the current benchmark, but READ still has 64 false-positive reads and 63 missed reads. Because full exact requires the entire READ set to match, either type of READ error breaks exact match.

The READ task is harder because it requires relevance between user intent and candidate memory content. In the current data, READ labels are often recoverable from entity or domain matching, which is not enough to teach robust graded relevance.

## v0.3 JSON/span to v0.4/v0.5 Unit Formulation

The canonical v0.3 spec framed the router as a JSON/span predictor:

```json
{
  "read_hints": [],
  "write_spans": [],
  "ignore_spans": []
}
```

That formulation captured the original policy problem: read useful memories, write durable content, and ignore noisy content. Later v0.4/v0.5 work shifted to a unit-based formulation:

```text
READ memory IDs
STORE unit IDs + targets
SKIP unit IDs
```

The unit formulation reduces ambiguity for small-model supervised fine-tuning:

- the model predicts IDs instead of copying spans;
- STORE/SKIP decisions operate over explicit units;
- target classification is evaluated directly;
- parser and evaluator behavior are more stable.

The underlying research question did not change. The operational representation changed to make the router easier to train and evaluate.

## Current Interpretation

The strongest measured result is BF16 standard LoRA r16 with 1000 targeted-balanced training cases under RTX 4090 fallback settings. The result shows strong write-side routing and target classification on the locked benchmark, but it does not establish downstream agent utility or production safety.


# EVAL_PLAN

Version: v0.4 draft  
Status: P1 interface evaluation plan draft  
Scope: v0.4 interface pilot, not model training

## 1. Design Judgments To Validate

v0.4 should produce evidence for three interface design judgments:

1. Unit IDs are more stable than exact spans.
2. DSL output is more stable than JSON output.
3. `READ / STORE / SKIP` is parseable, annotatable, and evaluable as a memory-policy interface.

The pilot should not claim that v0.4 solves retrieval, writing, memory lifecycle, or production agent memory.

## 2. A/B/C Experiment Design

All interfaces should be evaluated on the same cases where possible. The only changed variable is the raw output interface requested from the model.

### A. Legacy Span JSON

Historical v0.3-style output:

```json
{
  "read_hints": ["m1"],
  "write_spans": [
    {"span": "parser is almost complete", "type": "task_state"}
  ],
  "ignore_spans": ["check today's weather"]
}
```

Measures:

- JSON validity;
- schema validity;
- exact span copying stability;
- read selection quality;
- write/ignore span quality;
- failure modes from complex nested JSON.

### B. Unit JSON

Unit-based JSON output:

```json
{
  "read": ["m1"],
  "store": [
    {"target": "task_state", "unit_id": "u2"}
  ],
  "skip": ["u3"]
}
```

Measures:

- whether unit IDs reduce exact-span copying failures;
- whether target selection is feasible;
- whether JSON schema remains a source of avoidable errors.

### C. Unit DSL

Proposed v0.4 raw output:

```text
READ m1
STORE task_state u2
SKIP u3
```

Measures:

- parse success;
- invalid ID rates;
- invalid target rate;
- READ / STORE / SKIP quality;
- whether a low-entropy DSL improves stability without semantic quality loss.

## 3. 30-50 Bridge Cases Plan

### Purpose

Bridge cases are a small, hand-curated set used to validate the interface before scaling data.

They should answer:

- Is the v0.4 case schema clear?
- Are the five STORE targets distinguishable?
- Does the DSL grammar cover expected outputs?
- Can parser/eval logic consume the same gold labels?
- Are A/B/C outputs fairly comparable?
- Which target boundaries require guideline revision?

### Case Mix

Recommended bridge mix:

| Case type | Count |
| --- | ---: |
| READ-only | 8-10 |
| STORE/SKIP-only | 10-12 |
| READ + STORE joint | 10-12 |
| stale / related-but-useless memories | 5-8 |
| target-boundary cases | 5-8 |
| user_profile / sensitive boundary cases | 3-5 |

Bridge cases should be English, hand-reviewed, and explicitly tagged. Target-boundary cases should include notes explaining the intended label.

### Passing Standard

Bridge passes only if:

- all cases can be read by the future schema validator;
- gold labels can be represented as Unit JSON and Unit DSL;
- every current unit has exactly one STORE or SKIP label;
- target-boundary disagreements are documented;
- no obvious missing target is discovered;
- the project owner reviews the result before expansion.

## 4. 200-300 Pilot Cases Plan

The pilot dataset expands only after bridge review.

Recommended pilot mix:

| Case type | Count |
| --- | ---: |
| READ-only | 40-50 |
| STORE/SKIP-only | 50-70 |
| READ + STORE joint | 60-80 |
| stale / related-but-useless memories | 30-40 |
| target-boundary cases | 30-40 |
| user_profile / sensitive boundary cases | 20-30 |

Pilot cases should include:

- candidate memories that are useful;
- candidate memories that are related but should not be read;
- stale or superseded memories;
- current units with one-off requests;
- sensitive/private units that must be skipped;
- target-boundary examples across all five targets.

v0.3 hard cases may inspire pilot cases, but v0.3 labels must not be mechanically converted into v0.4 labels.

## 5. Metrics

### 5.1 Structural Metrics

`parse_success`:

```text
count(outputs parsed into valid canonical structure) / count(outputs)
```

`invalid_memory_id_rate`:

```text
count(predicted READ ids not in candidate_memories) / count(predicted READ ids)
```

`invalid_unit_id_rate`:

```text
count(predicted STORE/SKIP unit ids not in current_units) / count(predicted STORE/SKIP unit ids)
```

`invalid_target_rate`:

```text
count(predicted STORE targets not in legal target set) / count(predicted STORE targets)
```

`output_length`:

```text
raw output characters, lines, and approximate tokens
```

### 5.2 Semantic Routing Metrics

`READ precision / recall / F1`:

```text
Compare predicted memory_id set against gold READ memory_id set.
```

`STORE unit F1`:

```text
Compare predicted STORE unit_id set against gold STORE unit_id set.
```

`STORE target accuracy`:

```text
Among correctly predicted STORE units, count target matches / correctly predicted STORE units.
```

`SKIP F1`:

```text
Compare predicted SKIP unit_id set against gold SKIP unit_id set.
```

`false_store_rate`:

```text
count(units predicted STORE where gold is SKIP) / count(predicted STORE units)
```

`irrelevant_read_rate`:

```text
count(predicted READ memories not in gold READ) / count(predicted READ memories)
```

`human_repair_cost`:

```text
manual edits required to make output structurally valid and semantically aligned.
```

Suggested measurement levels for human repair cost:

```text
0 = no repair
1 = mechanical format repair only
2 = ID / target repair
3 = semantic relabeling needed
```

## 6. Baselines And Comparisons

Use simple baselines to separate interface gains from task difficulty.

Possible baselines:

- `empty / no-action`: READ none, STORE none, SKIP all current units.
- `top-k READ`: read the first or top-scored candidate memories, STORE none, SKIP all units.
- `heuristic`: lexical rules for obvious read/store/skip cases.
- `teacher LLM`: stronger LLM prompted with the same interface.
- `zero-shot small model`: selected 3B-4B model without training.
- `Unit DSL prompt`: the proposed v0.4 prompt and DSL output.

For A/B/C comparison, report each system under the same case split, parser rules, and metric definitions.

## 7. Success Criteria

v0.4 interface pilot supports moving toward v0.5 training if:

- Unit DSL parse success is clearly better than Legacy Span JSON;
- Unit DSL semantic metrics are not worse than Unit JSON;
- Unit DSL has lower or comparable invalid ID and invalid target rates;
- target guideline does not require major restructuring;
- strict parser works without semantic repair;
- false store and irrelevant read errors are explainable and reducible;
- results allow a clear go/no-go decision for v0.5 training.

The pilot does not need perfect metrics. It needs enough evidence that the interface is stable enough to justify training data creation.

## 8. No-Go Criteria

Do not proceed to v0.5 training if:

- STORE targets are confused across a large fraction of cases;
- unit segmentation causes many units to require both STORE and SKIP;
- Unit DSL is not more structurally stable than JSON;
- parser success requires semantic repair;
- A/B/C cannot be compared fairly on the same cases;
- `project_memory` becomes a catch-all target;
- sensitive or private units are frequently stored;
- guideline changes would invalidate most pilot labels.

If any no-go criterion is hit, revise v0.4 spec, target guideline, unitization assumptions, or DSL grammar before scaling data or training.

## 9. Reporting Requirements

The final interface pilot report should include:

- case mix and tag distribution;
- structural metrics table for A/B/C;
- semantic metrics table for A/B/C;
- target confusion analysis;
- examples of parse failures;
- examples of target-boundary errors;
- false store and irrelevant read analysis;
- human repair cost estimate;
- go/no-go recommendation for v0.5.

Do not hide safety failures inside aggregate F1. Sensitive-store and false-store behavior should be reported explicitly.

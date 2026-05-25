# Teacher Generation Smoke Test Plan

This plan defines the first controlled test for real teacher-model synthetic data generation. It is a smoke test only. It does not start full dataset generation, model training, model downloading, or baseline evaluation.

## Goal

Verify that a teacher model can produce structurally valid and semantically useful JSONL decision cases for the memory policy router.

The smoke test should answer:

- Can the teacher follow the `target` schema?
- Can it keep `write_spans` and `ignore_spans` as exact substrings of `current_user_input`?
- Can it select only existing candidate memory IDs in `read_hints`?
- Can it generate realistic coding-agent memory-policy scenarios?
- Does it overproduce generic `sop` labels instead of facts, decisions, preferences, and task state?
- What failure modes appear before scaling generation?

## Non-Goals

Do not use this smoke test to:

- Train a model.
- Download a model.
- Generate thousands of examples.
- Create final train/dev/gold files.
- Replace human review.
- Claim semantic quality from structural validation alone.
- Connect multiple providers at once.
- Build a UI.

## Scope

Recommended first run:

```text
case_count: 20-50
provider: one teacher provider only
temperature: low
output_format: JSONL
schema_field: target
review_status: synthetic
destination: data/synthetic_drafts/<run_id>/
```

The run must use existing pipeline conventions:

```text
data/synthetic_drafts/<run_id>/
  raw_cases.jsonl
  cases.jsonl
  invalid_samples.jsonl
  metadata.json
  validation_report.txt
  distribution_report.md
```

## Required Metadata

Record these fields in `metadata.json`:

- `run_id`
- `generated_at_utc`
- `provider_name`
- `provider_version`
- `model_name`
- `prompt_template_name`
- `generator_prompt_id`
- `prompt_version`
- `requested_count`
- `raw_count`
- `valid_count`
- `invalid_count`
- `validation_passed`
- `validation_scope`: `structural_only`
- `semantic_quality_checked`
- `review_sample_size`
- `cost_estimate`, if available
- `notes`, if any provider-specific behavior appears

Do not store API keys, access tokens, or provider secrets in metadata.

## Prompt Selection

Use one prompt template per smoke test run unless there is a specific reason to compare templates.

Recommended first order:

1. `hard_negative_noisy_memory`
2. `direct_coding_agent`
3. `game_dev_workflow`

Reasoning:

- `hard_negative_noisy_memory` quickly exposes false writes, missed ignores, and irrelevant reads.
- `direct_coding_agent` checks general business/project memory behavior.
- `game_dev_workflow` is useful but less central to the current business-facing MVP framing.

## Output Rules

Teacher output must satisfy:

- JSONL only, one complete JSON object per line.
- English dataset content only.
- `target`, not `expected_output`.
- `candidate_memories`: 0-8 items.
- `recent_context`: 0-4 turns.
- `read_hints` IDs must exist in `candidate_memories`.
- `write_spans[*].span` must be an exact substring of `current_user_input`.
- `ignore_spans[*]` must be an exact substring of `current_user_input`.
- No character offsets in training or seed examples.
- No final rewritten memory content.
- No update/delete/merge operations.
- No project IDs, confidence scores, or `needs_review`.

## Type Distribution Targets

For the first teacher smoke test, do not enforce strict quotas, but inspect whether the output roughly follows this direction:

```text
sop: rare, explicit workflow rules only
decision: common, durable choices and preferences
fact: common, architecture/business/module facts
task_state: common, progress, blockers, active bugs, next steps
```

Red flags:

- `sop` dominates the generated write spans.
- `task_state` is absent.
- Candidate memories rarely include distractors.
- `ignore_spans` are either absent or exhaustive.
- Most cases are simple writes with no read challenge.

## Structural Validation Procedure

After generation:

1. Save all raw provider output to `raw_cases.jsonl`.
2. Run structural validation and invalid quarantine through the pipeline.
3. Write structurally valid cases to `cases.jsonl`.
4. Write failed records to `invalid_samples.jsonl`.
5. Write `validation_report.txt`.
6. Write `distribution_report.md`.

Run the validator on valid cases:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/elliot/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 src/validation/validate_cases.py data/synthetic_drafts/<run_id>/cases.jsonl --min-per-category 0
```

For a balanced 50-case smoke test, `--min-per-category 2` is useful but not mandatory.

## Semantic Review Procedure

Structural validation must be followed by semantic review.

Use `docs/semantic_review_checklist.md`.

Recommended review sample:

```text
If generated cases <= 20: review all valid cases.
If generated cases 21-50: review at least 20 valid cases.
Always review all invalid samples if invalid_count <= 20.
Sample across categories, memory types, and cases with/without candidate memories.
```

For each reviewed case, assign:

- `accept`
- `minor_fix`
- `major_fix`
- `reject`

Track repeated issues, especially:

- False writes on temporary noise.
- Missed ignore spans.
- Irrelevant read hints.
- Missing relevant read hints.
- `decision` vs `task_state` confusion.
- Overuse of `sop`.
- Write spans that are too broad.
- Structurally valid but semantically weak no-action cases.

## Pass/Fail Criteria

The smoke test passes only if:

- Structural validation succeeds on most generated records.
- Invalid samples are quarantined and inspectable.
- No invalid records are silently mixed into `cases.jsonl`.
- A semantic review sample shows that most cases are usable or fixable.
- Prompt failures are understandable enough to improve the next run.

Suggested thresholds for the first 20-50 case run:

```text
structural_valid_rate >= 80%
review_accept_or_minor_fix_rate >= 70%
invalid_samples inspected: yes
semantic_quality_checked: yes
```

Fail the run if:

- The provider does not produce JSONL reliably.
- Exact substring failures are common.
- `read_hints` often reference missing IDs.
- More than half the reviewed cases are `major_fix` or `reject`.
- The output drifts into final memory rewriting or update/delete operations.

## Next Step After Passing

If the smoke test passes:

1. Improve prompts using observed failure patterns.
2. Run a second 50-100 case teacher draft.
3. Review another stratified sample.
4. Only then consider scaling toward a few hundred synthetic draft cases.

Do not move to 5,000 training examples until structural validation, invalid quarantine, and semantic review are stable.

# Dev and Gold Phase Plan

This plan defines the preparation work for the MVP dev and gold evaluation
datasets. It does not generate the datasets yet.

## Purpose

The synthetic train split is complete:

- `data/processed/synthetic_train_5000.jsonl`

The next data phase creates two different assets:

- Dev set: 250 examples for development and model selection.
- Gold eval set: 300 human-reviewed examples for final reporting.

These assets must not be treated as more training data. Their job is to measure
whether the router learned memory-policy behavior rather than memorizing train
templates.

## Dev Set

Target:

- 250 records.
- 25 records per MVP category.
- `split="dev"`.
- `review_status="synthetic"` unless a later review pass promotes individual
  records.

Primary uses:

- Tune prompt teacher formatting.
- Tune zero-shot student prompting.
- Tune fine-tuning checkpoints and decoding settings.
- Test validation, span matching, and metric scripts.
- Select the final model before touching gold eval.

Recommended paths:

- Draft handoff: `handoffs/deepseek_v4pro_dev_250/`
- Draft output: `handoffs/deepseek_v4pro_dev_250/output/raw_cases.jsonl`
- Promoted file: `data/dev/dev_250.jsonl`
- Metadata: `data/dev/dev_250.metadata.json`
- Validation report: `data/dev/dev_250.validation_report.txt`
- Distribution report: `data/dev/dev_250.distribution_report.md`

Generation source:

- ClaudeCode connected to DeepSeek V4 Pro Max.

Quality requirements:

- No train family reuse from C-L.
- No copied project/entity names from final train where avoidable.
- No exact or near-duplicate `current_user_input` values.
- Same router contract as train: only `read_hints`, `write_spans`,
  `ignore_spans`.
- Keep all content in English.
- Use `target`, not `expected_output`.

## Gold Eval Set

Target:

- 300 records.
- 30 records per MVP category.
- Final split value: `split="gold_eval"`.
- Final review status: `review_status="human_reviewed"`.

Primary uses:

- Final model comparison.
- Prompt teacher vs gold.
- Zero-shot student vs gold.
- Fine-tuned student vs gold.
- Rule baseline vs gold.
- Error analysis and memory-pollution component reporting.

Recommended paths:

- Draft handoff: `handoffs/deepseek_v4pro_gold_draft_300/`
- Draft output: `handoffs/deepseek_v4pro_gold_draft_300/output/raw_cases.jsonl`
- Review working file: `data/gold/gold_eval_300.review.jsonl`
- Final file: `data/gold/gold_eval_300.jsonl`
- Metadata: `data/gold/gold_eval_300.metadata.json`
- Validation report: `data/gold/gold_eval_300.validation_report.txt`
- Distribution report: `data/gold/gold_eval_300.distribution_report.md`

Generation source:

- ClaudeCode connected to DeepSeek V4 Pro Max for the first draft.
- Optional web Opus 4.7 audit for semantic review.
- Human review before final promotion.

Important offset rule:

- Do not ask DeepSeek to hand-generate character offsets.
- Generate exact substring spans first.
- After validation and human review, derive `char_start` and `char_end` locally
  from `current_user_input`.
- Keep the final gold JSONL on the same router schema as train/dev: the router
  target predicts only `read_hints`, `write_spans`, and `ignore_spans`.
- Store derived offsets in a sidecar file joined by `case_id`, rather than
  embedding offsets in the final gold JSONL.

This avoids model mistakes from manually counting characters.

## Required Preparation Before Generation

Before generating either set:

1. Create a small handoff folder for the external model.
2. Include the schema contract, category guidance, a few reference examples, and
   train-avoidance notes.
3. Use the prompt in `docs/manual_generation/deepseek_v4pro_dev_gold_prompts.md`.
4. Run local validators after generation.
5. Run semantic spot checks before promotion.

Before finalizing gold:

1. Derive offsets from exact spans into a sidecar file.
2. Validate that sidecar offsets round-trip to the exact original spans.
3. Human-review all 300 examples.
4. Mark final records as `review_status="human_reviewed"`.
5. Keep review notes in `gold_notes` only when the note is useful for later
   error analysis.

## Split Leakage Controls

Minimum controls:

- No same `family_id` across train/dev/gold.
- No exact duplicate `current_user_input` across train/dev/gold.
- Avoid reusing the same project names, service names, table names, tool names,
  and business scenarios from final train.
- Avoid the known weak templates from Day 5 repairs, especially:
  - conflict resolution followed by unrelated trailing facts;
  - context-dependent spans that say only `that approach` or `same rule`;
  - no-action cases that actually contain durable facts or task states;
  - correction spans that include meta prefixes like `Correction:` or `Update:`.

Recommended stronger controls:

- Run near-duplicate checks against `data/processed/synthetic_train_5000.jsonl`.
- Spot-check at least 5 records per category for dev.
- Human-review all gold records.

## Suggested Order

1. Generate and validate dev 250.
2. Use dev 250 to shake down metric scripts and baseline prompts.
3. Generate gold draft 300.
4. Run structural validator and semantic audit.
5. Run Opus 4.7 or equivalent semantic review on the gold draft.
6. Human-review and repair gold.
7. Derive offsets and run gold-specific validation.
8. Freeze the data manifest before baseline and model evaluation.

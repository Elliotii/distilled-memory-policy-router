# Data Asset Inventory

This file records which dataset artifacts are authoritative for the current
MVP stage and which artifacts are retained only for audit or generation
history.

## Authoritative MVP Train Asset

Use this file as the synthetic training entrypoint:

- `data/processed/synthetic_train_5000.jsonl`

Companion artifacts:

- `data/processed/synthetic_train_5000.metadata.json`
- `data/processed/synthetic_train_5000.validation_report.txt`
- `data/processed/synthetic_train_5000.distribution_report.md`

Current status:

- Split: `train`
- Review status: `synthetic`
- Record count: 5000
- Categories: 10 categories x 500 records
- Hard validator status: passed
- This is not a human-reviewed gold dataset.

Final structural metrics:

| metric | value |
| --- | ---: |
| total records | 5000 |
| invalid JSON records | 0 |
| schema errors | 0 |
| invalid read_hints | 0 |
| invalid spans | 0 |
| duplicate case_id | 0 |
| duplicate current_user_input | 0 |
| read_hints | 3847 |
| write_spans | 3857 |
| ignore_spans | 1375 |
| cases with candidate_memories | 3908 |
| cases with recent_context | 2794 |
| cases with 5-8 candidate_memories | 1598 |
| cases with ignore_spans | 1261 |

Final target write-type counts:

| write type | count |
| --- | ---: |
| fact | 1120 |
| decision | 1114 |
| task_state | 856 |
| sop | 767 |

## Included Source Batches

The processed 5000-record train file is assembled from these accepted and
repaired DeepSeek V4 Pro batches:

- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_c_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_d_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_e_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_f_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_g_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_h_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_i_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_j_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_k_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_l_repaired`

Each included batch keeps its own:

- `raw_cases.jsonl`
- `cases.jsonl`
- `metadata.json`
- `validation_report.txt`
- `distribution_report.md`
- `invalid_samples.jsonl`

Some batches also keep targeted replacement files used during repair. These are
audit artifacts, not separate train inputs.

## Excluded Synthetic Drafts

These Day 5 batches are intentionally excluded from the final train file:

- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_repaired`
- `data/synthetic_drafts/day5_deepseek_v4pro_batch500_b_repaired`

They are retained because they are useful for provenance and comparison, but
their generation and repair standards were earlier than the final C-L workflow.

Earlier Day 2-Day 4 mock, smoke, manual, and Packy/Opus draft directories under
`data/synthetic_drafts/` are also retained as generation history. They should
not be mixed into the final MVP train split unless explicitly promoted by a new
review pass.

Manual raw exports under `data/manual_drafts/` are source material only. They
are not train-ready by default.

## Dataset Stage Boundaries

Current completed assets:

- Synthetic train: 5000 examples, complete.
- Synthetic dev: 250 examples, complete.
- Human-reviewed gold eval: 300 examples, complete.
- Multi-turn traces: 8 traces, complete.

Gold eval entrypoint:

- `data/gold/gold_eval_300.jsonl`

Gold companion artifacts:

- `data/gold/gold_eval_300.metadata.json`
- `data/gold/gold_eval_300.validation_report.txt`
- `data/gold/gold_eval_300.semantic_audit_report.txt`
- `data/gold/gold_eval_300.distribution_report.md`
- `data/gold/gold_eval_300.offsets.jsonl`

Gold review/source artifacts retained for audit:

- `data/gold/gold_eval_300.review.jsonl`
- `data/gold/gold_eval_300.review.metadata.json`
- `data/gold/gold_eval_300.review_repair_notes.md`

Multi-turn trace entrypoint:

- `data/traces/multiturn_traces_8.jsonl`

Multi-turn trace companion artifacts:

- `data/traces/multiturn_traces_8.metadata.json`
- `data/traces/multiturn_traces_8.validation_report.txt`
- `docs/multiturn_trace_schema.md`

Still required for the MVP data stage:

- None. MVP data assets are complete.

Still required for the MVP project:

- Evaluation harness.
- Baselines: empty, naive all-read, rule-based, prompt teacher, zero-shot
  student, fine-tuned student.
- Final LoRA/QLoRA router training and evaluation.
- Report, error analysis, README refresh, and resume bullets.

Do not treat synthetic train validation as a substitute for gold review. The
hard validator proves schema and substring contracts only; semantic quality
still depends on spot checks, batch audits, and later evaluation.

## Operational Rules

- After any change to `data/*.jsonl`, run the dataset validator.
- Keep generated caches, logs, local API outputs, and large temporary files out
  of commit scope.
- For training, use only `data/processed/synthetic_train_5000.jsonl` unless a
  later data manifest supersedes this inventory.

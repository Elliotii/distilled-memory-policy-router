# LLM Downstream-Lite Design Report

This report describes derived prompt fixtures for a later harness-style LLM downstream-lite run. No LLM was called and no router model was loaded.

## Command

```bash
python3 scripts/build_llm_downstream_lite_prompt_pack.py --gold data/v05e/gold_v2/v05e_gold_v2_009_active_cases.jsonl --predictions data/v05g/model_predictions/bf16_r16_1000_4090_gold_v2_009_predictions.jsonl --out-cases data/v10/llm_downstream_lite/llm_downstream_lite_cases.jsonl --out-prompts data/v10/llm_downstream_lite/llm_downstream_lite_prompt_pack.jsonl --out-report reports/v10/llm_downstream_lite_design_report.md
```

## Selected Cases

| Case ID | Category | Selection reason | Gold READ | Router READ |
| --- | --- | --- | --- | --- |
| `v05e_gold_active_0002` | `full_exact_or_read_exact` | Router READ, STORE, and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm2', 'm3'] |
| `v05e_gold_active_0004` | `full_exact_or_read_exact` | Router READ, STORE, and SKIP match the locked reference. | ['m1', 'm2'] | ['m1', 'm2'] |
| `v05e_gold_active_0009` | `full_exact_or_read_exact` | Router READ, STORE, and SKIP match the locked reference. | ['m1', 'm2'] | ['m1', 'm2'] |
| `v05e_gold_active_0010` | `full_exact_or_read_exact` | Router READ, STORE, and SKIP match the locked reference. | ['m1', 'm2'] | ['m1', 'm2'] |
| `v05e_gold_active_0012` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m2', 'm3', 'm4'] | ['m1', 'm2', 'm3', 'm4'] |
| `v05e_gold_active_0015` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm2'] |
| `v05e_gold_active_0016` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm3'] |
| `v05e_gold_active_0017` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m2', 'm3', 'm4'] | ['m1', 'm2', 'm3', 'm4'] |
| `v05e_gold_active_0001` | `irrelevant_memory_reduction` | Router selects fewer irrelevant memories than all-candidates injection. | ['m1', 'm3', 'm5'] | ['m1', 'm3', 'm5'] |
| `v05e_gold_active_0006` | `irrelevant_memory_reduction` | Router selects fewer irrelevant memories than all-candidates injection. | ['m2', 'm3', 'm4'] | ['m2', 'm4'] |

## Counts

- Cases generated: 10
- Prompt objects generated: 50
- Case category distribution: {'full_exact_or_read_exact': 4, 'irrelevant_memory_reduction': 2, 'read_mismatch_write_correct': 4}
- Strategy distribution: {'all_candidates': 10, 'no_memory': 10, 'oracle_selected': 10, 'router_selected': 10, 'top_k_naive': 10}

## Skipped Cases

The builder skips cases with sensitive-boundary tags, long raw text, missing predictions, or categories not needed for this small balanced pack.
Skipped count: 26

| Case ID | Reason |
| --- | --- |
| `v05e_gold_active_0003` | excluded sensitive-boundary case |
| `v05e_gold_active_0005` | excluded sensitive-boundary case |
| `v05e_gold_active_0008` | excluded sensitive-boundary case |
| `v05e_gold_active_0014` | excluded sensitive-boundary case |
| `v05e_gold_active_0028` | excluded sensitive-boundary case |
| `v05e_gold_active_0031` | excluded sensitive-boundary case |
| `v05e_gold_active_0032` | excluded long case |
| `v05e_gold_active_0034` | excluded sensitive-boundary case |
| `v05e_gold_active_0036` | excluded long case |
| `v05e_gold_active_0038` | excluded sensitive-boundary case |
| `v05e_gold_active_0039` | excluded sensitive-boundary case |
| `v05e_gold_active_0063` | excluded sensitive-boundary case |
| `v05e_gold_active_0068` | excluded sensitive-boundary case |
| `v05e_gold_active_0070` | excluded sensitive-boundary case |
| `v05e_gold_active_0071` | excluded sensitive-boundary case |
| `v05e_gold_active_0077` | excluded sensitive-boundary case |
| `v05e_gold_active_0105` | excluded sensitive-boundary case |
| `v05e_gold_active_0106` | excluded sensitive-boundary case |
| `v05e_gold_active_0109` | excluded long case |
| `v05e_gold_active_0113` | excluded long case |
| `v05e_gold_active_0116` | excluded sensitive-boundary case |
| `v05e_gold_active_0118` | excluded long case |
| `v05e_gold_active_0130` | excluded sensitive-boundary case |
| `v05e_gold_active_0135` | excluded sensitive-boundary case |
| `v05e_gold_active_0146` | excluded sensitive-boundary case |
| `v05e_gold_active_0149` | excluded sensitive-boundary case |

## Risks And Claim Boundaries

- The fixtures are derived benchmark inputs, not new locked gold.
- The pack compares memory injection strategies with fixed candidate memories; it does not evaluate retrieval.
- It uses saved router predictions, not live router inference.
- The prompt pack has not been executed or judged.
- Any later answer-quality claim needs collected responses, manual or LLM-judge scoring, and clear uncertainty notes.

## Review Recommendation

Ask an Opus/friend reviewer to inspect this prompt pack before execution, especially the rubric, prompt wording, and whether selected cases are sufficiently understandable without adding fabricated context.

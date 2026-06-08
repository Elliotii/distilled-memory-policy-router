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
| `v05e_gold_active_0021` | `full_exact_or_read_exact` | Router READ, STORE, and SKIP match the locked reference. | ['m1', 'm2'] | ['m1', 'm2'] |
| `v05e_gold_active_0023` | `full_exact_or_read_exact` | Router READ, STORE, and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm2', 'm3'] |
| `v05e_gold_active_0024` | `full_exact_or_read_exact` | Router READ, STORE, and SKIP match the locked reference. | ['m1', 'm2'] | ['m1', 'm2'] |
| `v05e_gold_active_0026` | `full_exact_or_read_exact` | Router READ, STORE, and SKIP match the locked reference. | ['m1', 'm2'] | ['m1', 'm2'] |
| `v05e_gold_active_0015` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm2'] |
| `v05e_gold_active_0016` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm3'] |
| `v05e_gold_active_0018` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m2', 'm3', 'm4'] | ['m1', 'm2', 'm3', 'm4'] |
| `v05e_gold_active_0027` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm2'] |
| `v05e_gold_active_0035` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm2'] |
| `v05e_gold_active_0037` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm3'] |
| `v05e_gold_active_0041` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm3', 'm4'] | ['m1', 'm2', 'm4'] |
| `v05e_gold_active_0042` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m1', 'm2', 'm3', 'm4'] |
| `v05e_gold_active_0043` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm3'] | ['m2', 'm3'] |
| `v05e_gold_active_0044` | `read_mismatch_write_correct` | Router READ differs while STORE and SKIP match the locked reference. | ['m1', 'm2', 'm4'] | ['m1', 'm2', 'm3'] |
| `v05e_gold_active_0001` | `irrelevant_memory_reduction` | Router selects fewer irrelevant memories than all-candidates injection. | ['m1', 'm3', 'm5'] | ['m1', 'm3', 'm5'] |
| `v05e_gold_active_0006` | `irrelevant_memory_reduction` | Router selects fewer irrelevant memories than all-candidates injection. | ['m2', 'm3', 'm4'] | ['m2', 'm4'] |
| `v05e_gold_active_0007` | `irrelevant_memory_reduction` | Router selects fewer irrelevant memories than all-candidates injection. | ['m1', 'm3', 'm5'] | ['m1', 'm2', 'm3', 'm5'] |
| `v05e_gold_active_0011` | `irrelevant_memory_reduction` | Router selects fewer irrelevant memories than all-candidates injection. | ['m1', 'm2', 'm4'] | ['m1', 'm2', 'm4', 'm5'] |
| `v05e_gold_active_0013` | `irrelevant_memory_reduction` | Router selects fewer irrelevant memories than all-candidates injection. | ['m1', 'm3', 'm5'] | ['m1', 'm2', 'm3', 'm5'] |
| `v05e_gold_active_0019` | `irrelevant_memory_reduction` | Router selects fewer irrelevant memories than all-candidates injection. | ['m1', 'm2', 'm3'] | ['m1', 'm2', 'm4'] |

## Counts

- Cases generated: 24
- Prompt objects generated: 168
- Case category distribution: {'full_exact_or_read_exact': 8, 'irrelevant_memory_reduction': 6, 'read_mismatch_write_correct': 10}
- Strategy distribution: {'all_candidates': 24, 'no_memory': 24, 'oracle_selected': 24, 'random_k': 24, 'router_selected': 24, 'shuffled_top_k': 24, 'top_k_naive': 24}
- Each prompt requires memory-id citations for used memory facts.
- Cases with simple numeric contradiction risk are excluded from the main execution pack rather than silently mixed in.

## Skipped Cases

The builder skips cases with sensitive-boundary tags, long raw text, simple numeric contradiction risk, missing predictions, or categories not needed for this balanced pack.
Skipped count: 30

| Case ID | Reason |
| --- | --- |
| `v05e_gold_active_0003` | excluded sensitive-boundary case |
| `v05e_gold_active_0005` | excluded sensitive-boundary case |
| `v05e_gold_active_0008` | excluded sensitive-boundary case |
| `v05e_gold_active_0012` | excluded contradiction risk: Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test. |
| `v05e_gold_active_0014` | excluded sensitive-boundary case |
| `v05e_gold_active_0017` | excluded contradiction risk: Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test. |
| `v05e_gold_active_0028` | excluded sensitive-boundary case |
| `v05e_gold_active_0031` | excluded sensitive-boundary case |
| `v05e_gold_active_0034` | excluded sensitive-boundary case |
| `v05e_gold_active_0038` | excluded sensitive-boundary case |
| `v05e_gold_active_0039` | excluded sensitive-boundary case |
| `v05e_gold_active_0040` | excluded contradiction risk: Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test. |
| `v05e_gold_active_0053` | excluded contradiction risk: Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test. |
| `v05e_gold_active_0055` | excluded contradiction risk: Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test. |
| `v05e_gold_active_0063` | excluded sensitive-boundary case |
| `v05e_gold_active_0068` | excluded sensitive-boundary case |
| `v05e_gold_active_0070` | excluded sensitive-boundary case |
| `v05e_gold_active_0071` | excluded sensitive-boundary case |
| `v05e_gold_active_0077` | excluded sensitive-boundary case |
| `v05e_gold_active_0085` | excluded contradiction risk: Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test. |
| `v05e_gold_active_0086` | excluded contradiction risk: Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test. |
| `v05e_gold_active_0100` | excluded contradiction risk: Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test. |
| `v05e_gold_active_0105` | excluded sensitive-boundary case |
| `v05e_gold_active_0106` | excluded sensitive-boundary case |
| `v05e_gold_active_0116` | excluded sensitive-boundary case |
| `v05e_gold_active_0130` | excluded sensitive-boundary case |
| `v05e_gold_active_0135` | excluded sensitive-boundary case |
| `v05e_gold_active_0144` | excluded contradiction risk: Memory and current units contain different numeric facts with shared units; exclude from main execution pack unless reviewed as a stress test. |
| `v05e_gold_active_0146` | excluded sensitive-boundary case |
| `v05e_gold_active_0149` | excluded sensitive-boundary case |

## Risks And Claim Boundaries

- The fixtures are derived benchmark inputs, not new locked gold.
- The pack compares memory injection strategies with fixed candidate memories; it does not evaluate retrieval.
- It uses saved router predictions, not live router inference.
- The pack includes citation instructions to support partial automatic checks, but final scoring still requires response review.
- End-to-end required-memory coverage should penalize strategies that failed to inject required memory; conditional injected-required coverage is only a diagnostic decomposition.
- The prompt pack has not been executed or judged.
- Any later answer-quality claim needs collected responses, manual or LLM-judge scoring, and clear uncertainty notes.

## Review Recommendation

Ask an Opus/friend reviewer to inspect this prompt pack before execution, especially the rubric, prompt wording, and whether selected cases are sufficiently understandable without adding fabricated context.

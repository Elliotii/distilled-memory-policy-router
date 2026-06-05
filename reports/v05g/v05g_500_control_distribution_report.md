# v05g 500-Control Distribution Report

**Date:** 2026-06-05  
**Source:** Exact copy of `data/v05b/json_sft/v05b_train_500_json_sft_messages.jsonl` and `data/v05/train/subsets/v05_train_500_cases.jsonl`

## Summary

| Metric | Value |
|--------|-------|
| Total cases | 500 |
| Total STORE units | 1,042 |
| Unique projects | 17 |
| Unique services | 198 |
| Unique repos | 19 |

## Shape Distribution

| Shape | Count | % |
|-------|-------|---|
| READ-only | 105 | 21.0% |
| STORE/SKIP-only | 182 | 36.4% |
| READ+STORE | 213 | 42.6% |

## Target Distribution (STORE units)

| Target | Count | % |
|--------|-------|---|
| task_state | 338 | 32.4% |
| service_memory | 323 | 31.0% |
| repo_memory | 201 | 19.3% |
| project_memory | 122 | 11.7% |
| user_profile | 58 | 5.6% |

## Stress Coverage

| Category | Count | % |
|----------|-------|---|
| Sensitive cases (tagged) | 30 | 6.0% |
| Target-boundary cases | 100 | 20.0% |

## Domain Coverage (Top 10)

| Project | Cases |
|---------|-------|
| customer-support | 46 |
| analytics-dashboard | 45 |
| ecommerce-platform | 44 |
| memory-router | 38 |
| data-platform | 34 |
| docs-assistant | 33 |
| finance-dashboard | 33 |
| mobile-field | 33 |
| learning-assistant | 31 |
| workflow-automation | 31 |

## Notes

- This is the exact dataset used to train the Qwen3.5 QLoRA r16 experiment (v0.5d).
- Contains some domain names that later leaked into rejected gold_v2 builds (ecommerce-platform, shopengine, learnhub). These are retained as-is for the control experiment.
- Distribution is skewed toward task_state (32.4%) and service_memory (31.0%), with low user_profile (5.6%).
- This file is NOT regenerated — it is the canonical 500-control source.

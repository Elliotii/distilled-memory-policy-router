# v05g Training Data Plan

**Date:** 2026-06-05  
**Status:** Complete  
**Version:** v0.5g

## Context

Following v0.5f parse-stabilization audit which concluded that parse repair is not the main path forward, the user decided to stop small repair loops and prepare a real LoRA scaling experiment.

## Research Questions

1. Does standard **BF16 LoRA r16** improve over existing QLoRA r16 when using the same 500 training examples?
2. Does expanding to **1000 targeted-balanced** examples improve over BF16 LoRA r16 500?

## Target Experiment

- Model: Qwen3.5-4B
- Interface: Unit JSON standard
- Precision: BF16 LoRA r16
- Server: rent once, train two variants

## Data Products

| # | Product | Path | Description |
|---|---------|------|-------------|
| 1 | 500-control cases | `data/v05g/cases/v05g_train_500_control_cases.jsonl` | Exact copy of v05b train 500 cases |
| 2 | 500-control SFT | `data/v05g/json_sft/v05g_train_500_control_json_sft_messages.jsonl` | Exact copy of v05b train 500 SFT |
| 3 | Additional 500 cases | `data/v05g/cases/v05g_train_additional_500_targeted_cases.jsonl` | New targeted-balanced cases |
| 4 | Additional 500 SFT | `data/v05g/json_sft/v05g_train_additional_500_targeted_json_sft_messages.jsonl` | SFT messages for additional 500 |
| 5 | Combined 1000 cases | `data/v05g/cases/v05g_train_1000_targeted_cases.jsonl` | Concatenation of 1+3 |
| 6 | Combined 1000 SFT | `data/v05g/json_sft/v05g_train_1000_targeted_json_sft_messages.jsonl` | Concatenation of 2+4 |
| 7 | Lock manifest | `data/v05g/v05g_training_data_lock.json` | SHA-256 hashes + quality gates |

## Key Design Decisions

1. **500-control is a true subset of 1000**: The 1000 set concatenates 500-control + additional 500. This ensures the LoRA scaling comparison is fair — BF16 r16 500 and BF16 r16 1000 differ only in data volume, not seed data.

2. **8 new domains**: energy-monitoring, fleet-management, agriculture-tech, hr-analytics, compliance-management, manufacturing-ops, network-operations, content-moderation. All verified against gold_v2_009, rejected gold_v2, dev, and old gold namespace bans.

3. **Targeted-balanced distribution**: Additional 500 designed to shift combined 1000 toward recommended target ranges.

4. **No gold_v2_009 leakage**: New STALE_POOL with entirely distinct texts; 0 namespace overlap; 0 exact text overlap.

## Quality Gates (all pass)

| Gate | Status |
|------|--------|
| SFT JSON parse = 100% | ✅ |
| Unit coverage = 100% | ✅ |
| Store/skip mutually exclusive | ✅ |
| Sensitive STORE = 0 | ✅ |
| No target:"skip" in store | ✅ |
| No duplicate unit assignment | ✅ |
| No invalid targets | ✅ |
| No invalid read/store/skip IDs | ✅ |
| No unresolved placeholders | ✅ |

## Gold Protection

- gold_v2_009: unchanged and not used for v05g training-data generation except as exclusion/leakage reference
- Old gold: unchanged
- Dev: unchanged
- No new gold set created

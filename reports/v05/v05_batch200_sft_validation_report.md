# V0.5 Batch200 SFT Validation Report

Date: 2026-06-01  
Context: 5.1-A — SFT validation for batch200  
Status: Format validation; no training

## 1. Counts
200 SFT messages, all `source=v05_batch200_dry_run`, all `is_final_train_data=false`.

## 2. Checks
- Schema: all 200 valid ✓
- Assistant == gold.dsl: 200/200 ✓
- Parse OK: 200/200 ✓
- No markdown/JSON: 0 violations ✓

## 3. Risks
System prompt fixed at ~980 chars. Assistant must remain pure DSL for training. Format stable at 200-case scale.

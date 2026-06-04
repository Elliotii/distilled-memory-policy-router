# V0.5e gold_v2 Lock Report

**Date:** 2026-06-04  

## Lock Status: LOCKED

| Property | Value |
|----------|-------|
| Lock version | v05e_gold_v2_001 |
| Lock file | `data/v05e/gold_v2/v05e_gold_v2_lock.json` |
| Active cases | 150 |
| Holdout cases | 30 (reserved, unused) |
| Hashes recorded | 4 (cases + SFT) |

## Statement

> gold_v2 has NOT been evaluated by any model. Active set (150) is for final r=16/r=8/few-shot evaluation. Holdout (30) is reserved for future use.

## Post-Lock Rules

- Active cases must not be modified
- Holdout cases must remain unused
- Any modification requires new lock version (v05e_gold_v2_002+)
- Model evaluation may begin after lock

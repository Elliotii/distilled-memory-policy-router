# V0.5 Gold Final Prelock Hash Manifest

**Date:** 2026-06-02  
**Context:** 5.3-D2 — prelock hashes after final metadata cleanup  
**⚠ IMPORTANT: These are PRELOCK hashes, NOT locked gold hashes.**

---

## Prelock File Hashes

| File | SHA-256 |
|------|---------|
| `data/v05/gold/v05_gold_corrected_cases.jsonl` | `56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d` |
| `data/v05/gold/v05_gold_core_corrected_cases.jsonl` | `9acdd6a795b0a18d5c369253be8bb64e26a9af96e2aea31b4ef6c98adb598db2` |
| `data/v05/gold/v05_gold_hard_corrected_cases.jsonl` | `5f4a5d552f76033c6a9a5443581a2dc2dc7ea0eeabdf99481fc1ec2c49f819b2` |
| `data/v05/gold/v05_gold_corrected_sft_messages.jsonl` | `d9f215af282d6c90b65612c575d9a5827520a953d47f807e586b79ec94635c22` |

## Hash Change Notes

| File | Changed from 5.3-D? | Reason |
|------|:-------------------:|--------|
| combined | Yes | Notes and u2 texts rewritten |
| core | Yes | Notes and u2 texts rewritten (all changes in gold_core) |
| hard | No | No gold_hard cases modified by cleanup |
| SFT | Yes | Regenerated from updated combined file |

## Lock Status

These hashes represent the **prelock corrected gold** after Opus lightweight final review metadata cleanup (Context 5.3-D2).

Gold is **NOT locked**. The lock file (`data/v05/gold/v05_gold_lock.json`) has **NOT been created**.

**If lock happens next without additional changes, these hashes should match the lock hashes.**

## File Properties

| Property | Combined | Core | Hard | SFT |
|----------|:--------:|:----:|:----:|:---:|
| Cases/Rows | 100 | 70 | 30 | 100 |
| is_locked_gold | false | false | false | false |
| is_final_train_data | false | false | false | false |

---

*End of V0.5 Gold Final Prelock Hash Manifest.*

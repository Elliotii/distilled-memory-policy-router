# gold_v2_002 Validation Report

**Date:** 2026-06-04  

## All Checks Passed

| Check | Result |
|-------|:------:|
| Schema validation | ✅ 0 errors |
| Target legality | ✅ All valid |
| Unit coverage | ✅ 100% |
| Sensitive STORE | ✅ 0 stored |
| Duplicate IDs | ✅ 0 |
| SFT JSON parse | ✅ 150/150 (100%) |
| SFT markdown | ✅ 0 |
| READ IDs in memories | ✅ All valid |
| No phantom units | ✅ |

## Leakage

| Check | Result |
|-------|:------:|
| Exact text overlap (train_500) | ✅ 0 |
| Exact text overlap (dev) | ✅ 0 |
| Exact text overlap (old gold) | ✅ 0 |
| Domain overlap (old gold) | ✅ 0 |
| ID overlap | ✅ 0 |

## Label Consistency

All unit texts are uniquely generated per case. No shared template instances. Manual spot-checks passed.

## Lock

Version: `v05e_gold_v2_002`  
Active SHA-256: `44ee596dae441258...`

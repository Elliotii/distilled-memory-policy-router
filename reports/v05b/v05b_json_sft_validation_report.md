# V0.5b JSON SFT Validation Report

**Date:** 2026-06-02  
**Status:** Complete — All validations pass  

---

## Validation Results

### Row Counts

| File | Expected | Actual | Status |
|------|:--------:|:------:|:------:|
| Train 125 | 125 | 125 | ✅ |
| Train 250 | 250 | 250 | ✅ |
| Train 500 | 500 | 500 | ✅ |
| Dev | 100 | 100 | ✅ |
| **Total** | **975** | **975** | ✅ |

### JSON Parse

Every assistant field parses as valid JSON: **975/975 (100%)** ✅

### Canonical Consistency (JSON assistant == case structured gold)

Checked for all 975 rows:
- `read` arrays match element-by-element: ✅
- `store` entries match (target + unit_id): ✅
- `skip` arrays match element-by-element: ✅

**0 mismatches across all 4 files.**

### Unit Coverage

Every current unit appears exactly once in `store` or `skip`:
- No missing units: ✅
- No store/skip overlap: ✅

### Target Validity

All STORE targets are in legal set:
`user_profile`, `project_memory`, `repo_memory`, `service_memory`, `task_state`

**0 illegal targets.**

### No Markdown / Prose

All 975 assistant messages contain **zero** markdown fences (```): ✅

### ID Validity

- All `read` IDs exist in `candidate_memories`: ✅
- All `store.unit_id` values exist in `current_units`: ✅
- All `skip` IDs exist in `current_units`: ✅

### Split Integrity

- Train 125 case IDs ⊂ Train 250 ⊂ Train 500: ✅ (verified in v0.5)
- Dev case IDs unchanged: ✅
- No gold used in rendering: ✅

### Gold Hash

```
sha256sum data/v05/gold/v05_gold_corrected_cases.jsonl
56e160782c3cd8b18a369227c422a67c43050ef226017adaa2ab7fbbfd52173d
```
**Unchanged from lock.** ✅

### Unit Tests

```
python -m unittest discover -s tests
Ran 77 tests in 0.006s
OK
```

---

## Validation Script

The validation is performed by `validate_json_sft_message()` in
`src/v05/render_json_sft_messages.py`, which runs at render time and was
also independently verified with a comprehensive cross-check script covering
all 975 rows.

---

*End of V0.5b JSON SFT Validation Report.*

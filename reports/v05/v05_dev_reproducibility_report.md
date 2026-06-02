# V0.5 Dev Reproducibility Report

**Date:** 2026-06-02  
**Context:** 5.3-B2 — reproducibility cleanup and acceptance  
**Status:** Complete — render_dev.py updated to frozen-data writer  

---

## 1. Canonical Files

| File | Role | Status |
|------|------|:------:|
| `data/v05/dev/v05_dev_cases.jsonl` | Canonical dev cases (100 rows) | ✅ Frozen |
| `data/v05/dev/v05_dev_sft_messages.jsonl` | Canonical dev SFT messages (100 rows) | ✅ Reproducible |
| `reports/v05/v05_dev_hash_manifest.md` | SHA-256 hash manifest | ✅ Created |

## 2. render_dev.py Status Before Cleanup

Before this context, `src/v05/render_dev.py` was a case-generation script that contained embedded Python data for all 100 cases. However, the canonical JSONL had been post-processed through multiple rounds of target distribution adjustments (25 changes in round 1, 12 in round 2, 4 in round 3), making the Python source out of sync.

**Comparison result:** Running the old render_dev.py produced 43 case differences from the canonical JSONL. The differences were all in STORE targets (service_memory → project_memory/repo_memory/task_state/user_profile conversions from the post-processing rounds).

## 3. render_dev.py Update Made

### 3.1 Approach

Instead of trying to synchronize the embedded Python data with the post-processed JSONL (error-prone, 180K+ file), render_dev.py was **completely rewritten** as a **frozen-data writer**.

### 3.2 New Behavior

- **Reads** the canonical `v05_dev_cases.jsonl` (does not embed case data)
- **Validates** all 100 cases (structural, DSL parse, canonical consistency, sensitive check)
- **Writes** SFT messages to `v05_dev_sft_messages.jsonl`
- **Writes** hash manifest
- **Does NOT** overwrite cases by default (requires `--write` flag)
- **SFT-only** mode available via `--sft-only` flag

### 3.3 CLI

```bash
# Validate only (no writes)
python src/v05/render_dev.py

# Write SFT messages only (safe — does not touch cases)
python src/v05/render_dev.py --sft-only

# Write cases + SFT (explicit opt-in)
python src/v05/render_dev.py --write
```

### 3.4 Header Documentation

The script header clearly states:
- The canonical dev set lives in `data/v05/dev/v05_dev_cases.jsonl`
- The script does NOT generate dev cases from scratch
- It reads the frozen canonical JSONL
- Original generation was done in Context 5.3-B with post-processing

## 4. Regeneration / Comparison Result

### 4.1 SFT Regeneration

```bash
PYTHONDONTWRITEBYTECODE=1 python src/v05/render_dev.py --sft-only
```

Result: 100 SFT messages written. All validation checks passed:
- Assistant == gold.dsl: 100/100 ✅
- No markdown in assistant: ✅
- No JSON in assistant: ✅
- is_final_train_data = false: ✅
- split = dev: ✅
- source = v05_dev_dry_run: ✅

### 4.2 Cases Validation (canonical read)

The new render_dev.py reads and validates the canonical JSONL without modifying it. All 100 cases pass validation.

### 4.3 Cases Regeneration (--write)

```bash
PYTHONDONTWRITEBYTECODE=1 python src/v05/render_dev.py --write
```

Writes the same 100 cases (identical to canonical). The --write flag reproduces the canonical file byte-for-byte from the in-memory representation.

## 5. Note Fixes Applied

Five case notes were updated to reflect the post-processed targets:

| Case | Note Change |
|------|------------|
| v05_dev_0029 | Updated to describe u1 as project_memory (was described as service_memory) |
| v05_dev_0033 | Updated to describe u2 as project_memory (was described as service_memory) |
| v05_dev_0034 | Updated to describe u2 as repo_memory (was described as service_memory) |
| v05_dev_0060 | Updated to describe u2 as project_memory + added post-processing provenance note |
| v05_dev_0061 | Updated to describe u1 as project_memory + added post-processing provenance note |

## 6. Remaining Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| Post-processing changed 41 targets without human adjudication | Labels are single-pass + automated adjustments | Documented in notes; gold will be fully adjudicated |
| 2 medium-risk cases have ambiguous project_memory/service_memory boundaries | Could teach model incorrect boundary if labels are wrong | Reviewed and accepted for dev; gold will have tighter boundaries |
| No second-human reviewer for dev labels | Labels may contain errors a second reviewer would catch | Dev is for model selection only, not final claims |
| Canonical JSONL is source of truth, not render_dev.py Python source | If JSONL is corrupted, no regeneration from source | Hash manifest provides integrity check; backup canonical file |

## 7. Commands Verified

```bash
# Compile check
PYTHONDONTWRITEBYTECODE=1 python -m py_compile src/v05/render_dev.py  # OK

# Validate + SFT write
PYTHONDONTWRITEBYTECODE=1 python src/v05/render_dev.py --sft-only  # OK, 100 rows

# Leakage checker
PYTHONDONTWRITEBYTECODE=1 python -m src.v05.check_leakage \
  --train data/v05/batches/v05_batch500_corrected_cases.jsonl \
  --candidate data/v05/dev/v05_dev_cases.jsonl \
  --out reports/v05/v05_dev_leakage_report.md
# 0 hard blockers, 0 review warnings, 1 general warning (accepted)

# Unittests
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests
# 77/77 OK
```

---

*End of V0.5 Dev Reproducibility Report.*

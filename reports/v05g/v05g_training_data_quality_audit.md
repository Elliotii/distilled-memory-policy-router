# v05g Training Data Quality Audit

**Date:** 2026-06-05  
**Auditor:** `src/v05g/audit_v05g_training_data.py` + repair validation  
**Status:** ALL GATES PASS (Repaired data)

## Quality Gates (9/9 PASS)

| # | Gate | Status |
|---|------|--------|
| 1 | SFT JSON parse = 100% | ✅ 1000/1000 valid JSON |
| 2 | Unit coverage = 100% | ✅ All units assigned to store or skip |
| 3 | Store/skip mutually exclusive | ✅ 0 units in both store and skip |
| 4 | Sensitive STORE = 0 | ✅ 0 sensitive units in STORE |
| 5 | No target:"skip" in store | ✅ 0 invalid targets |
| 6 | No duplicate unit assignment | ✅ 0 duplicate unit_ids |
| 7 | No invalid targets | ✅ All targets in legal set |
| 8 | No invalid read/store/skip IDs | ✅ All IDs reference valid entities |
| 9 | No unresolved placeholders | ✅ 0 filler key residue |

## SFT Format Validation

| File | Records | JSON Parse | Canonical Match |
|------|---------|------------|-----------------|
| 500-control SFT | 500 | 100% | 100% |
| Additional 500 SFT | 500 | 100% | 100% |
| Combined 1000 SFT | 1000 | 100% | 100% |

### Detailed Checks
- 0 markdown fences detected
- 0 malformed JSON
- 0 missing required keys (read/store/skip)
- 0 invented IDs
- 0 invalid memory IDs in read
- 0 invalid unit IDs in store/skip
- 0 canonical mismatches

## Structural Validation

### Case-level checks (all 1000 cases)
- 0 cases with unassigned units
- 0 cases with units in both store and skip
- 0 cases with duplicate store entries
- 0 cases with invalid targets
- 0 cases with sensitive content in STORE

### Sensitive audit
- Total sensitive units: 90 (additional 500) + 30 (500-control) = 120 combined
- Sensitive units in STORE: 0
- Sensitive categories covered: phone (14 variants), email (12), credential (14), address (10), payment (10), ID (10)
- Max sensitive literal repetition: 2x (repaired from 5x)

## Placeholder Audit

### Additional 500 (repaired)
- 0 `{vocab_item}` residues
- 0 unresolved filler keys
- All templates properly filled with domain-specific vocabulary

### 500-control
- Contains intentional template syntax (e.g., `{version}`, `{status}`, `{RUN_ID}`) representing actual code templates — these are by design, not generation artifacts.

## Data Integrity

- 500-control case_ids match v05b train 500 exactly (500/500 match)
- 500-control is byte-identical to original source (hash `c6ec79d9...`)
- 500-control is a proper subset of combined 1000
- Additional 500 case_ids are unique (v05g_add_0001 through v05g_add_0500)
- Combined 1000 has exactly 1000 unique case_ids

## Semantic Quality (Post-Repair)

| Check | Result |
|-------|--------|
| Stale READ count | 0 ✅ |
| Distractor READ count | 0 ✅ |
| Non-stale in-domain not-read without visible reason | 0 ✅ |
| READ semantic recoverability | All READ decisions visible from prompt context ✅ |
| 3-word-prefix binary accuracy | 90.9% (was 100%) ✅ |
| Body-dependent cases | 64.2% (>10% minimum) ✅ |
| Sensitive literal diversity | 70 unique (was 18), max 2x ✅ |

## Recommendations

- Data is clean and semantically repaired.
- The 500-control file should NOT be regenerated — it is the canonical source.
- Future training experiments should reference these exact files by hash.
- All Opus 4.8-identified defects have been addressed.

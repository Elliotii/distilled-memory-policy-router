# V0.5 Batch500 Corrected — SFT Validation Report

**Date:** 2026-06-02  
**Context:** 5.2-D — SFT messages regenerated from corrected batch500  
**Source:** data/v05/batches/v05_batch500_corrected_sft_messages.jsonl  

---

## 1. SFT Row Count

| Metric | Value |
|--------|-------|
| SFT rows | 500 |
| Expected | 500 (1:1 with corrected cases) |
| Status | ✓ Match |

---

## 2. Assistant == Gold DSL

Each SFT message's `assistant` content was compared against the corresponding case's `gold.dsl`.

| Check | Result |
|-------|--------|
| Assistant matches gold.dsl | 500/500 ✓ |
| Mismatches | 0 |

---

## 3. Parse Check

All 500 assistant outputs parse correctly via `src/v04/parser.py`:

| Check | Result |
|-------|--------|
| DSL parse valid | 500/500 ✓ |
| Parse errors | 0 |
| Parse canonical matches structured gold | 500/500 ✓ |

---

## 4. No Markdown / No JSON Check

| Check | Result |
|-------|--------|
| Markdown (``` fence) in assistant | 0 ✓ |
| JSON (starting with `{`) in assistant | 0 ✓ |
| Plain text/commentary in assistant | 0 ✓ |

All assistant messages contain only clean Unit DSL lines.

---

## 5. Source and Metadata Check

| Field | Value |
|-------|-------|
| Source tag | `v05_batch500_corrected_dry_run` |
| `metadata.is_final_train_data` | `false` (all 500 rows) |
| `metadata.num_candidate_memories` | 0–5 per row |
| `metadata.num_current_units` | 1–3 per row |

All 500 rows consistently have `is_final_train_data: false` — this is still draft data, not locked.

---

## 6. Example Row

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a memory policy router for coding-agent contexts.\n\nTask:\nGiven RUNTIME_CONTEXT, CANDIDATE_MEMORIES, and CURRENT_UNITS, choose:\n- which candidate memories to READ;\n- which current unit IDs to STORE and to which target;\n- which current unit IDs to SKIP.\n\nOutput only the DSL. Do not include comments, prose, explanations, or JSON.\n\nAllowed DSL lines:\nREAD <memory_id_list|NONE>\nSTORE <target> <unit_id>\nSTORE NONE\nSKIP <unit_id_list|NONE>\n\nLegal STORE targets:\nuser_profile, project_memory, repo_memory, service_memory, task_state\n\nRules:\n- READ useful memories only; skip merely related or stale ones.\n- STORE durable, reusable information with correct target.\n- SKIP sensitive, temporary, one-off, or out-of-scope content.\n- Every current unit must appear exactly once in STORE or SKIP.\n- Do not invent IDs, targets, or content."
    },
    {
      "role": "user",
      "content": "RUNTIME_CONTEXT\nproject: education-platform\nrepo: learnhub\nservice: grading\ntask: add grade appeal workflow\n\nCANDIDATE_MEMORIES\nm1 [service_memory]: The grading service stores final grades in the submissions table with a graded_at timestamp and instructor ID.\nm2 [project_memory]: The learnhub project requires all grade changes to have an audit trail with the original grade, new grade, and reason.\n\nCURRENT_UNITS\nu1: Add a grade appeal workflow where students can submit an appeal within 14 days of grade posting with a written justification.\nu2: Appeals must be reviewed by a different instructor than the one who assigned the original grade.\nu3: All grade changes from appeals must be logged to the grade_audit table with the original grade, new grade, and reviewer ID."
    },
    {
      "role": "assistant",
      "content": "READ m1,m2\nSTORE task_state u1\nSTORE service_memory u2\nSTORE service_memory u3\nSKIP NONE"
    }
  ],
  "case_id": "v05_batch100_0039",
  "source": "v05_batch500_corrected_dry_run",
  "metadata": {
    "tags": ["read_store_joint", "service_invariant", "project_vs_repo"],
    "num_candidate_memories": 2,
    "num_current_units": 3,
    "gold_shape": "READ + STORE joint",
    "store_targets": ["task_state", "service_memory", "service_memory"],
    "is_final_train_data": false
  }
}
```

---

## 7. Risks Before Dev/Gold

| Risk | Severity | Status |
|------|----------|--------|
| Cross-batch duplicate (v05_batch50_0003 m1 == v05_batch300_0001 m1) | Low | Model sees same text twice. Acceptable for training. |
| 6 borderline cases from independent review | Low | Non-blocking. Can be adjudicated during dev/gold split. |
| 38% of replacement cases share structural pattern | Medium | Diluted to 3.8% of full pool. Not a template concern. |
| Source is dry run, not locked | Info | Must be relabeled before training. |
| No dev/gold split yet | Blocking (process) | Must be done in Context 5.3. |

---

*End of SFT validation report.*

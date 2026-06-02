# V0.5 Leakage and Near-Duplicate Plan

Version: v0.5
Date: 2026-06-02
Status: Planning — leakage prevention and near-duplicate detection
Context: 5.3-A — dev/gold + provenance + leakage planning

---

## 1. Leakage Sources

The following data sources exist or will exist in the project. Each is subject to leakage checks.

| # | Source | Cases | Role |
|---|--------|:-----:|------|
| 1 | Corrected batch500 | 500 | Train-pool candidate |
| 2 | Dev set (planned) | 80–100 | Model selection |
| 3 | Gold set (planned) | 100 | Final evaluation |
| 4 | Subset50 (v0.4) | 50 | Historical A/B/C pilot |
| 5 | Few-shot examples (planned) | 3 | System prompt examples |
| 6 | Prompt examples (if any) | TBD | Prompt design reference |
| 7 | v0.4 pilot cases | 200 | Interface pilot (different era) |
| 8 | v0.4 bridge cases | 40 | Boundary reference (different era) |

### 1.1 Cross-Context Leakage Vectors

Leakage can occur through:

| Vector | Example |
|--------|---------|
| Exact case_id match | Same case_id in train and gold |
| Exact current_unit text match | Same unit text in different splits |
| Exact candidate_memory text match | Same memory text in different splits |
| Near-duplicate current_unit text | Slightly reworded unit text |
| Near-duplicate candidate_memory text | Slightly reworded memory text |
| Same scenario, different wording | Same domain+task+service with paraphrased text |
| Same boundary pattern | Same target ambiguity, same resolution |
| Few-shot example in gold | Gold case used as few-shot example |
| Prompt example from gold | Gold case studied during prompt design |
| Gold used for hyperparameter tuning | Indirect leakage through model selection |

---

## 2. Prohibited Leakage

### 2.1 Hard Prohibitions (Must Never Happen)

| # | Prohibition | Detection |
|---|------------|-----------|
| P1 | Exact duplicate case_id across splits | Direct ID comparison |
| P2 | Exact duplicate current_unit text (any unit) between train↔gold | Exact text match |
| P3 | Exact duplicate candidate_memory text (any memory) between train↔gold | Exact text match |
| P4 | Gold cases used as few-shot examples | ID check |
| P5 | Gold cases used as prompt examples | ID check |
| P6 | Train cases copied verbatim into gold | Exact case match |
| P7 | Gold used for hyperparameter/prompt tuning | Process enforcement |
| P8 | Dev cases copied into gold | Exact case match |
| P9 | Subset50 cases in train/dev/gold | ID check |

### 2.2 Soft Prohibitions (Must Review Before Accepting)

| # | Prohibition | Detection |
|---|------------|-----------|
| S1 | Near-duplicate current_unit text (Jaccard ≥ 0.8) between train↔gold | n-gram overlap |
| S2 | Near-duplicate candidate_memory text (Jaccard ≥ 0.8) between train↔gold | n-gram overlap |
| S3 | Same scenario with minor rewording across splits | Human review |
| S4 | Same boundary pattern with different text across splits | Human review |
| S5 | Dev↔gold overlap (any level) | All checks |

---

## 3. Near-Duplicate Checks

### 3.1 Check Levels

| Level | Method | What It Catches | Automation |
|-------|--------|-----------------|:----------:|
| L1: Exact text | String equality | Copy-paste leakage | Fully automated |
| L2: Normalized text | Lowercase, strip whitespace, remove punctuation | Trivial rewording | Fully automated |
| L3: n-gram overlap | Jaccard similarity on word 3-grams | Paraphrased content | Automated script |
| L4: Embedding similarity | Cosine similarity of sentence embeddings | Semantic near-duplicates | Optional, if embeddings available |
| L5: Human review | Manual inspection of high-similarity pairs | Conceptual leakage | Human required |

### 3.2 L1: Exact Text Match

For every pair of splits (train↔dev, train↔gold, dev↔gold):

1. Collect all `current_units[*].text` strings from each split.
2. Set intersection: any text string appearing in both splits is a hit.
3. Collect all `candidate_memories[*].content` strings.
4. Set intersection: any content string appearing in both splits is a hit.
5. Collect all `case_id` strings.
6. Set intersection: any case_id appearing in both splits is a hit.

Expected result: 0 hits. Any hit is a blocking issue.

### 3.3 L2: Normalized Text Match

Same as L1, but text is preprocessed:
- Lowercased.
- Leading/trailing whitespace stripped.
- Punctuation removed (keep alphanumeric + spaces).
- Multiple spaces collapsed to single space.

Catches trivial rewording like:
- "The parser rejects unknown targets." vs "the parser rejects unknown targets"
- "Add a priority field" vs "Add a priority field."

Expected result: 0 hits. Any hit is likely a blocking issue.

### 3.4 L3: n-gram Overlap (Jaccard)

For each current_unit text and candidate_memory content across splits:

1. Tokenize into word 3-grams.
2. Compute Jaccard similarity: `|A ∩ B| / |A ∪ B|`.
3. Flag pairs with Jaccard ≥ 0.5 for review.
4. Flag pairs with Jaccard ≥ 0.8 as likely near-duplicates.

**Short-text fallback:** For short texts (fewer than 3 words), word-level 3-grams produce empty sets. Use **token-level Jaccard** (single-word set overlap) as a fallback. The token Jaccard score can replace the n-gram score when the n-gram score is 0.

**Tentative thresholds:**

| Jaccard | Action |
|:-------:|--------|
| ≥ 0.9 | Treat as duplicate — reject or justify explicitly |
| ≥ 0.8 | High similarity — require human review and explicit approval |
| ≥ 0.5 | Moderate similarity — review in batch, note if concerning |
| < 0.5 | Acceptable — natural domain overlap |

### 3.5 L3b: Scenario Collision via Runtime Context

Check for **runtime context tuple collision** between train and candidate splits:

- Create a tuple `(project, repo, service, task)` from each case's `runtime_context`.
- Exact tuple match across splits indicates the same scenario was used in both sets, even if text differs.
- This is a **warning, not a hard blocker** — same scenario with different text may be acceptable if independently written.
- Flag all collisions for review.

### 3.6 L4: Embedding Similarity (Optional)

If sentence-transformer embeddings become available:

1. Embed all current_unit texts and candidate_memory contents.
2. Compute cosine similarity between all cross-split pairs.
3. Flag pairs with cosine similarity ≥ 0.95 for review.
4. Flag pairs with cosine similarity ≥ 0.90 for batch inspection.

This is optional — n-gram overlap may be sufficient for this project's scale.

### 3.7 L5: Human Review

All flagged pairs from L3 and L4 that exceed thresholds must be human-reviewed. The reviewer determines whether the similarity is:

| Category | Definition | Action |
|----------|------------|--------|
| **True duplicate** | Same information, same scenario, same text or trivial paraphrase | Reject — must not appear in both splits |
| **Shared domain** | Same project/repo domain but different scenarios/tasks | Accept — natural domain overlap |
| **Shared boundary pattern** | Same target ambiguity type but different concrete content | Accept only if independently written; flag for awareness |
| **False positive** | N-gram overlap from common phrases, different meaning | Accept |

---

## 4. Similarity Thresholds Summary

| Type | Threshold | Action |
|------|:---------:|--------|
| Exact text duplicate (L1) | — | **Reject** (hard block) |
| Normalized text duplicate (L2) | — | **Reject** (hard block if exact unit/memory) |
| High n-gram overlap (L3) | Jaccard ≥ 0.9 | **Reject** |
| Moderate-high n-gram overlap (L3) | Jaccard ≥ 0.8 | **Review required** |
| Moderate n-gram overlap (L3) | Jaccard ≥ 0.5 | **Batch review** |
| Short-text token Jaccard fallback (L3) | Token Jaccard ≥ 0.8 | **Review required** |
| Scenario collision (L3b) | Exact runtime_context tuple match | **Warn / review** |
| High embedding similarity (L4) | Cosine ≥ 0.95 | **Review required** |
| Same domain only | — | Accept if text/scenario differ |
| Same boundary pattern | — | Accept only if independently written |

---

## 5. Required Reports

### 5.1 Before Training: Train↔Dev Near-Duplicate Report

Must be generated after dev set is constructed and before training begins.

Report contents:
- L1 exact match results (must be 0).
- L2 normalized match results (must be 0).
- L3 n-gram overlap distribution (histogram of all cross-split Jaccard scores).
- L3 flagged pairs list (all pairs with Jaccard ≥ 0.5).
- Human review decisions for all flagged pairs.
- Summary: number of pairs reviewed, number rejected, number accepted.

File: `reports/v05/v05_train_dev_leakage_report.md`

### 5.2 Before Final Eval: Train↔Gold Near-Duplicate Report

Must be generated after gold set is locked and before final evaluation.

Report contents:
- L1 exact match results (must be 0).
- L2 normalized match results (must be 0).
- L3 n-gram overlap distribution.
- L3 flagged pairs list.
- Human review decisions for all flagged pairs.
- Summary.

File: `reports/v05/v05_train_gold_leakage_report.md`

### 5.3 Before Final Eval: Dev↔Gold Near-Duplicate Report

Must be generated to confirm dev and gold are independent.

File: `reports/v05/v05_dev_gold_leakage_report.md`

### 5.4 Cross-Batch Duplicate Audit

The known cross-batch duplicate (`v05_batch50_0003` m1 == `v05_batch300_0001` m1) must be documented:

- Which splits contain it (train only, if both cases stay in train pool).
- Whether it appears in dev or gold (must not).
- Impact assessment (low — model sees same text twice in training; acceptable).

---

## 6. Subset50 Status Decision

### 6.1 Background

Subset50 (50 cases from v0.4) was used extensively for:
- A/B/C interface pilot experiments.
- Prompt development (unit_dsl.txt, unit_dsl_fewshot.txt).
- Parser and eval_runner development.
- Multiple model inference runs (Qwen zero-shot, few-shot, etc.).

Subset50 is **not a clean holdout**. It has been studied, tuned against, and used for interface design decisions.

### 6.2 Required Decision

Subset50 must be:

**Option A: Retired from final eval** (Recommended)

- Subset50 is preserved as historical interface pilot evidence.
- It is NOT used in train, dev, or gold.
- All v0.4 A/B/C results are documented as pilot evidence, not final claims.
- The v0.5 evaluation uses entirely new dev and gold sets.

**Option B: Used only as historical evidence**

- Same as Option A, but subset50 results may be cited as historical baseline comparisons.
- Must be clearly labeled: "Historical pilot results on subset50 (v0.4 interface pilot). Not an independent holdout for v0.5."

**Option C: Incorporated into gold** (NOT Recommended)

- Subset50 cases added to gold after review.
- Risk: these cases have been studied, tuned against, and used for prompt design.
- Would require explicit documentation that gold includes previously-studied cases.
- Not ideal for a clean evaluation.

### 6.3 Recommendation

**Option A — Retire subset50 from final eval.**

Subset50 served its purpose as an interface pilot evaluation set. For v0.5 training evaluation, fresh dev and gold sets constructed independently provide a cleaner evaluation standard.

---

## 7. Implementation Plan (Future Context)

The leakage check script (`src/v05/check_leakage.py`, to be created in a future context) should:

1. Accept two JSONL case files as input.
2. Run L1 (exact text match) on case_id, current_unit texts, candidate_memory contents.
3. Run L2 (normalized text match) on the same fields.
4. Run L3 (n-gram Jaccard) and flag pairs above thresholds.
5. Output a JSON report with all flagged pairs and summary statistics.
6. Optionally run L4 (embedding similarity) if a sentence-transformer model is available.

Command sketch:
```bash
python3 src/v05/check_leakage.py \
  --train data/v05/train/v05_train_pool_500.jsonl \
  --eval data/v05/gold/v05_gold_cases.jsonl \
  --output reports/v05/v05_train_gold_leakage_report.json \
  --jaccard-threshold 0.5 \
  --high-jaccard-threshold 0.8
```

---

## 8. Changelog

| Date | Change |
|------|--------|
| 2026-06-02 | Initial creation (Context 5.3-A) |

---

*End of V0.5 Leakage and Near-Duplicate Plan.*

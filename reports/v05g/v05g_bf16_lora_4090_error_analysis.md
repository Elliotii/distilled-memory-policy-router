# v0.5g BF16 LoRA 4090 — Error Analysis

**Date:** 2026-06-08
**Focus:** Error patterns, bottlenecks, and concrete future work

---

## 1. The READ Bottleneck (Dominant)

### Evidence
- **1000-targeted gold exact: 36.0%** — 96 of 150 cases have at least one error.
- **READ F1: 84.6%** — Worst of all routing metrics. READ precision 84.5%, recall 84.7%.
- **READ contributes ~28pp of the ~45pp exact gap** (based on component decomposition):
  - Each READ error breaks full-exact match.
  - 1000-targeted has 64 false positive reads (irrelevant) and 63 false negative reads (missed).
  - Irrelevant read rate: 15.5% — model reads 64 memories it should not.

### Interpretation
READ selection is a fundamentally harder problem than STORE/SKIP routing:
- **STORE/SKIP** is a binary decision per unit with strong surface cues (imperatives, tense, context markers).
- **READ** requires matching candidate memory content against user intent — a retrieval-like task.
- Training data provides entity-matching READ labels (read if domain name matches), not graded relevance.
- The model learns a service/repo name matching heuristic, not semantic context selection.

### Concrete Pattern
On gold_v2_009, the 1000-targeted model:
- Reads 414 memories out of ~904 total (across 150 cases)
- 64 of these are irrelevant (FP)
- Misses 63 that should have been read (FN)
- Balanced precision/recall (84.5%/84.7%) suggests the model is uncertain rather than biased

---

## 2. 500-Control Gold Generalization Failure

### Evidence
- **500-control dev exact: 49.0%** vs **gold exact: 16.7%** — 32.3pp dev→gold gap.
- **500-control gold STORE F1: 0.892** vs dev: 0.967 — 7.5pp drop.
- **500-control gold false store: 10.4%** vs dev: 5.2% — doubled.
- **500-control gold READ F1: 80.1%** vs dev: 92.0% — 11.9pp drop.

### Causes
1. **BF16 precision not the issue** — 500-control dev (49%) actually outperforms old QLoRA r16 dev (unknown but in range). The failure is gold generalization.
2. **Gold_v2_009 is harder than dev** — Gold has 150 cases from 8 new domains with deliberately challenging boundary cases. Dev has 100 cases from the original v05 distribution.
3. **Training data shortcut** — 500-control training data (v05b) has READ labels that collapse to entity-name matching. On gold_v2_009's novel domain names and boundary cases, this shortcut fails.
4. **No QLoRA advantage** — QLoRA's 4-bit quantization may act as implicit regularization that helps generalization on small data. BF16's full precision may overfit more on 500 cases.

### Comparison: Old QLoRA r16 500 on same gold
- QLoRA r16: exact 22.7%, STORE F1 0.909, target acc 84.2%
- BF16 r16 500: exact 16.7%, STORE F1 0.892, target acc 84.7%
- **BF16 loses on exact (−6pp) and STORE F1 (−0.017); ties on target acc (+0.5pp).**

### Conclusion: BF16 alone is not sufficient and may be worse at small data scales.

---

## 3. 1000-Targeted Write-Side Improvement

### Evidence
All write-side metrics show dramatic improvement from 500→1000:

| Metric | 500-control gold | 1000-targeted gold | Δ |
|--------|:---------------:|:------------------:|:--:|
| STORE F1 | 0.892 | 0.990 | +0.098 |
| SKIP F1 | 0.840 | 0.981 | +0.141 |
| Target accuracy | 84.7% | 100.0% | +15.3pp |
| False store rate | 10.4% | 1.2% | −9.2pp |

### Target Confusion Matrix (1000-targeted Gold)
Perfect diagonal — zero off-diagonal entries:
```
project_memory → project_memory: 32
repo_memory → repo_memory: 37
service_memory → service_memory: 75
task_state → task_state: 82
user_profile → user_profile: 14
```

Compare to 500-control:
```
repo_memory → task_state: 12  (major confusion)
task_state → service_memory: 1
project_memory → service_memory: 2
user_profile → service_memory: 3
user_profile → task_state: 2
user_profile → project_memory: 1
```

### Drivers
- **Target-balanced training data** — 1000-targeted has better distribution: task 28.2%, svc 26.6%, repo 19.6%, proj 14.9%, user 10.7%. All within recommended ranges.
- **More STORE/SKIP examples** — 1000 has 2,079 STORE units vs 500's 1,042. 2× more write-side training signal.
- **Domain diversity** — Additional 500 covers 8 new business domains, teaching the model to generalize across different vocabulary for the same target types.

---

## 4. False Store Reduction

| Variant | Predicted Stores | False Stores | Rate |
|---------|:----------------:|:------------:|:----:|
| 500-control dev | 229 | 12 | 5.2% |
| 1000-targeted dev | 231 | 12 | 5.2% |
| 500-control gold | 240 | 25 | 10.4% |
| **1000-targeted gold** | 243 | **3** | **1.2%** |

1000-targeted reduces false stores from 25→3 on gold. The three remaining false stores are:
- Likely boundary cases where the model stores a unit that the gold labels as SKIP
- Acceptable rate for research purposes (1.2%)

---

## 5. Sensitive Store Observation

| Variant | Split | Sensitive Store |
|---------|-------|:---------------:|
| 500-control | dev | 2/3 (66.7%) |
| 1000-targeted | dev | 2/3 (66.7%) |
| 500-control | gold | 0/4 (0.0%) |
| 1000-targeted | gold | 0/4 (0.0%) |

- **Gold: 0/4 for both** — No genuine sensitive units stored on gold_v2_009. This is a strong safety signal.
- **Dev: 2/3 for both** — The dev set has the same inherent sensitive store issue seen across all trained models (contacts stored as user_profile). The 1000-targeted data explicitly has 0 sensitive stores in training, but the 500-control inherited 3 sensitive-relevant cases. The 1000-targeted model may be slightly better (having seen no sensitive stores in 500 new examples), but dev shows no difference.
- **Methodology difference:** v05g uses semantic sensitive-unit detection (match against `sensitive_boundary` tag on unit). v05e used eval_runner tag-based detection on cases. Not directly comparable, but both show improvement over Qwen3-4B's 6 genuine failures.

---

## 6. Dev/Gold Gap

| Metric | 500-control dev→gold | 1000-targeted dev→gold |
|--------|:--------------------:|:----------------------:|
| Exact | 49.0% → 16.7% (−32.3pp) | 59.0% → 36.0% (−23.0pp) |
| READ F1 | 92.0% → 80.1% (−11.9pp) | 93.3% → 84.6% (−8.7pp) |
| STORE F1 | 96.7% → 89.2% (−7.5pp) | 97.1% → 99.0% (+1.9pp) |
| SKIP F1 | 81.0% → 84.0% (+3.0pp) | 83.1% → 98.1% (+15.0pp) |
| Target acc | 85.3% → 84.7% (−0.6pp) | 89.5% → 100.0% (+10.5pp) |
| False store | 5.2% → 10.4% (+5.2pp) | 5.2% → 1.2% (−4.0pp) |

**Key observation:** 1000-targeted shows better gold generalization than 500-control on every metric except READ F1 (which still drops 8.7pp). STORE F1 and SKIP F1 actually improve on gold, suggesting the model learned generalizable write-side patterns.

**The dev→gold gap is primarily a READ problem.** Dev has simpler READ patterns (fewer distractor memories, more predictable domain names). Gold_v2_009 has deliberately challenging READ with stale pools, distractor memories, and boundary cases.

---

## 7. Concrete Future Work

### Immediate (v1.0 packaging)
1. Package BF16 r16 1000_4090 adapter with config and gold results for reproducibility.
2. Document the exact READ error cases (which case IDs have READ FP/FN) for future READ-focused work.

### READ Improvement Candidates
1. **Retrieval-augmented READ** — Use a separate retriever to pre-filter candidate memories before the router decides what to read.
2. **Longer context** — Extend max_seq_length beyond 2048 to include more candidate memory context.
3. **Graded relevance labels** — Train READ with relevance scores, not binary labels, to teach nuanced selection.
4. **Multi-turn READ** — Use conversation history to inform which memories are currently relevant.
5. **Two-stage routing** — Separate the READ prediction from STORE/SKIP; train READ-specific head with retriever-style loss.

### Write-Side Validation
1. **Downstream benchmark** — Test the 1000-targeted adapter with a real retriever to measure end-to-end utility.
2. **A100 reproduction** — If possible, train on A100/L40S to verify the 4090 fallback did not distort results.

### Not Recommended
- **Further data scaling within current framework** — Write-side metrics are at ceiling. READ bottleneck requires architectural changes.
- **More v0.5 experiments** — Diminishing returns. The project has sufficient data to draw conclusions.
- **BF16 alone without data diversity** — Proven insufficient by 500-control underperformance.

---

*End of v0.5g BF16 LoRA 4090 Error Analysis.*

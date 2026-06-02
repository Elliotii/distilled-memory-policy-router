# V0.5b Qwen3-4B Unit JSON LoRA 250 Smoke Decision

**Date:** 2026-06-02  
**Context:** 5.7-C — smoke decision after 250-case training + dev eval  

---

## 1. Training Result

| Check | Status |
|-------|:------:|
| Training completed | ✅ 367s |
| No OOM | ✅ |
| No NaN | ✅ |
| Adapter saved | ✅ |
| Eval loss converged (1.33→0.61) | ✅ |
| Mean token accuracy 86.5% | ✅ Very strong |

## 2. Dev Eval Result

| Check | Status |
|-------|:------:|
| Dev eval completed | ✅ |
| 100 predictions generated | ✅ |
| JSON parse success | **100%** ✅ |
| JSON validity | 100/100 ✅ |
| No markdown/prose | ✅ |
| No empty outputs | ✅ |

## 3. Key Metrics: JSON 125 → 250

| Metric | 125 | 250 | Direction |
|--------|:---:|:---:|:---------:|
| Parse success | 100% | 100% | Maintained ✅ |
| Exact | 11% | **20%** | +9pp ✅ |
| STORE F1 | 0.910 | **0.947** | +0.037 ✅ |
| Target acc | 55.7% | **63.8%** | **+8.1pp** ✅ |
| SKIP F1 | 0.535 | **0.747** | +0.212 ✅ |
| Sensitive store | 33.3% | 66.7% | ⚠ |

## 4. Key Metrics: JSON 250 vs DSL 250

| Metric | DSL 250 | JSON 250 | Winner |
|--------|:-------:|:--------:|:------:|
| Target acc | 55.7% | **63.8%** | JSON +8.1pp |
| Exact | 14% | **20%** | JSON +6pp |
| STORE F1 | 0.944 | **0.947** | JSON +0.003 |
| SKIP F1 | 0.684 | **0.747** | JSON +0.063 |
| Parse | 99% | **100%** | JSON |

**JSON dominates DSL at 250 cases.** Wins on all 5 primary metrics.

## 5. Critical Finding

**JSON target accuracy INCREASES with more data (55.7% → 63.8%), while DSL target accuracy DECREASES (60.0% → 55.7% → 54.1%).** JSON 250 target accuracy (63.8%) already exceeds DSL 500 (54.1%) by 9.7pp.

This confirms the Unit JSON LoRA hypothesis: JSON SFT training is fundamentally better for target classification than DSL SFT training. The structured key-value format provides cleaner separation between target and unit ID, reducing positional confusion.

## 6. Decision: Option A — Proceed to JSON LoRA 500 Unchanged

### Rationale

1. **JSON 250 dominates DSL 250 across all primary metrics.** The ablation is clearly positive.

2. **Target accuracy trajectory is upward (55.7→63.8) vs DSL's downward.** JSON format enables sustained learning. 500 cases may push target accuracy to 65-70%.

3. **STORE F1 (0.947) is approaching JSON few-shot (0.961).** 500 may close this gap.

4. **SKIP F1 improved dramatically (+0.212).** The model figured out skip prediction.

5. **Parse continues perfect at 100%.** No structural regression risk.

6. **Sensitive store worsened to 66.7%.** This matches DSL 250 and is an inherent data limitation (only 10 sensitive cases in 500). Not a JSON-specific issue.

### What to Watch at 500

- Target accuracy should reach ≥65% (extrapolating 125→250 trajectory)
- STORE F1 should approach 0.961 (JSON few-shot)
- SKIP F1 should maintain or improve
- Parse success must stay at 98-100%
- Sensitive store rate may stay high — needs dedicated safety-focused training later

### Risk: Sensitive Store

The sensitive store rate jumped from 33.3% (125) to 66.7% (250). This is concerning but matches DSL 250. With only ~10 sensitive cases in 500 training examples, the model has insufficient signal to learn sensitive content boundaries. This is a v0.5b candidate ablation #3 (safety-focused training), not a reason to stop JSON LoRA.

---

*End of V0.5b JSON LoRA 250 Smoke Decision — Proceed to 500.*

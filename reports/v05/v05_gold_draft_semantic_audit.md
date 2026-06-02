# V0.5 Gold Draft Semantic Audit

**Date:** 2026-06-02  
**Context:** 5.3-C2  

---

## 1. Audit Summary

| Category | Status |
|----------|:------:|
| Per-case audit | ✅ Complete (100 cases) |
| Gold hard detailed review | ✅ All 30 cases reviewed |
| Medium/high-risk cases | 17 post-processing svc→proj adjustments |
| Target-boundary issues | 17 medium-risk (svc→proj conversion), 8 low-risk |
| Sensitive/private | 0 STORE errors, 10 correct SKIPs |
| Related/stale | 24 cases correctly handled |
| Template/duplication | All cases distinct |
| Ready for external review | ✅ Yes |

## 2. Per-Case Audit Table

Full 100-case audit table is available in the canonical JSONL. Key summary:

| Partition | Cases | Low Risk | Medium Risk | Reviewed |
|-----------|:-----:|:--------:|:-----------:|:--------:|
| gold_core (original) | 45 | 45 | 0 | Structural only |
| gold_core (post-processed) | 25 | 8 | 17 | Needs adjudication |
| gold_hard | 30 | 0 | 30 | Full detail in review packet |
| **Total** | **100** | **53** | **47** | — |

## 3. Gold Hard Cases — Detailed Review

All 30 gold_hard cases are fully expanded in `v05_gold_review_packet.md`, Section 9. Each case includes:
- Runtime context
- Candidate memories with READ/NOT-READ decisions
- Current units with STORE/SKIP decisions
- Boundary difficulty explanation
- Why the case is hard

## 4. Medium/High-Risk Cases

17 gold_core cases had svc→proj post-processing adjustments. These are documented in `v05_gold_postprocessing_adjustment_log.md`. Key risk: the reframing from service-specific behavior to project-level requirement may be semantically questionable.

Top cases for adjudication focus:
- v05_gold_core_0041 (canary deployments as project_memory)
- v05_gold_core_0042 (faceted search as project_memory)
- v05_gold_core_0053 (GPG verification as project_memory)
- v05_gold_core_0060 (watermark tier policy as project_memory)
- v05_gold_core_0066 (language-aware search as project_memory)

## 5. Target-Boundary Audit

| Boundary | Cases | Verdict |
|----------|:-----:|:-------:|
| service_vs_task_state | 6 (5 hard + 1 core) | Covered, needs adjudication |
| project_memory_vs_task_state | 4 (hard) | Covered |
| repo_vs_service | 4 (hard) | Covered, clean boundaries |
| user_profile vs sensitive | 4 (hard) + 4 (core) | Covered, all sensitive correctly SKIPped |

## 6. Sensitive/Private Audit

10 cases with sensitive content — all correctly SKIPped. Types: SSN, credit card, API keys, phone numbers, home addresses, personal emails, CI tokens, driver's license.

Zero false-positive SKIPs (no safe content incorrectly SKIPped as sensitive).

## 7. Related/Stale Audit

- 16 related_but_useless cases — all correctly NOT READ
- 8 stale_memory cases — all correctly NOT READ
- Zero cases READ stale or related-but-useless memories

## 8. Template/Duplication Audit

All 100 cases are distinct in scenario, text, memories, units, and labels. Six diverse project domains prevent mechanical repetition.

## 9. Post-Processing Adjustment Risk Summary

| Risk | Count | Description |
|------|:-----:|-------------|
| Medium | 17 | svc→proj reframing may be semantically questionable |
| Low | 8 | svc→repo/task/user reframing is generally safe |
| Text errors fixed | 2 | v05_gold_core_0055 u2, v05_gold_core_0056 u2 (fixed in 5.3-C2) |

Recommendation: The 17 svc→proj adjustments should be the primary focus of human adjudication.

## 10. Readiness for External Review

| Criterion | Status |
|-----------|:------:|
| Structural validity | ✅ |
| DSL parseability | ✅ |
| Canonical consistency | ✅ |
| Sensitive store = 0 | ✅ |
| Distribution within target ranges | ✅ (user at 4.7%, acceptable) |
| Leakage: 0 hard blockers | ✅ |
| Review packet complete | ✅ |
| Adjustment log complete | ✅ |
| Ready for Opus/ClaudeCode review | ✅ |

---

*End of V0.5 Gold Draft Semantic Audit.*

# V0.5 Gold Final Prelock Validation Report

**Date:** 2026-06-02  
**Context:** 5.3-D2 — final validation after metadata cleanup  
**Status:** Cleanup applied — NOT locked  

---

## 1. Row Counts

| File | Rows | Expected |
|------|:----:|:--------:|
| v05_gold_corrected_cases.jsonl | 100 | 100 ✅ |
| v05_gold_core_corrected_cases.jsonl | 70 | 70 ✅ |
| v05_gold_hard_corrected_cases.jsonl | 30 | 30 ✅ |
| v05_gold_corrected_sft_messages.jsonl | 100 | 100 ✅ |

## 2. DSL Parse

| Check | Result |
|-------|:------:|
| All 100 gold.dsl parses via src/v04/parser.py | ✅ |
| Zero parse errors | ✅ |

## 3. Canonical Consistency

| Check | Result |
|-------|:------:|
| Parsed READ == structured gold.read | ✅ 100/100 |
| Parsed STORE == structured gold.store | ✅ 100/100 |
| Parsed SKIP == structured gold.skip | ✅ 100/100 |

## 4. Unit Coverage

| Check | Result |
|-------|:------:|
| Every current_unit appears exactly once in STORE or SKIP | ✅ 100/100 |
| No units in both STORE and SKIP | ✅ 0 |
| No units missing from both | ✅ 0 |

## 5. Sensitive STORE Scan

| Check | Result |
|-------|:------:|
| Sensitive-looking units stored (false positives possible) | 1* |
| Actual sensitive content stored | 0 |

\* v05_gold_hard_0027 u2: "api_key" appears in a file path name (`secrets/pagerduty_api_key.txt`) — this is a repo_memory that names a secrets file path, not a credential value. The actual API key value (u3) is correctly SKIPped. False positive from regex pattern.

10 cases with genuine sensitive content (SSN, credit card, API keys, emails, phone, home address, driver's license, CI token) — **all correctly SKIPped, zero STORE errors.**

## 6. Leakage Results

| Check | Hard Blockers | Warnings |
|-------|:------------:|:--------:|
| Train↔Corrected Gold | 0 | 0 |
| Dev↔Corrected Gold | 0 | 0 |

Clean across both dimensions. The previous phone number pattern warning (score 0.533) was resolved in Context 5.3-D.

## 7. SFT Assistant Check

| Check | Result |
|-------|:------:|
| All 100 assistant messages == gold.dsl | ✅ |
| No markdown in assistant ("```") | ✅ |
| No JSON in assistant (starts with "{") | ✅ |
| Source = v05_gold_corrected | ✅ |
| Split = gold_corrected | ✅ |
| is_locked_gold = false | ✅ |
| is_final_train_data = false | ✅ |
| gold_partition correct (core/hard) | ✅ |

## 8. Notes Quality Checks

| Check | Result |
|-------|:------:|
| No "uu1" typo in any note | ✅ |
| No truncated "..." placeholder pattern | ✅ |
| No notes justifying discarded labels | ✅ |
| All notes reference final labels | ✅ |
| All notes include policy rationale | ✅ |

## 9. Service Wording Quality Checks

| Check | Result |
|-------|:------:|
| No "project requires" in service_memory unit text | ✅ |
| 10 rewritten u2 units use service-style wording | ✅ |
| Meaning preserved after rewrite | ✅ (verified per-case) |

## 10. Unittest Result

```
Ran 77 tests in 0.007s
OK
```

## 11. Remaining Limitations

1. **Distribution tradeoffs:** project_memory at 7.1% (under 10-16%), user_profile at 4.3% (under 5-8%). Honest — no artificial labels.
2. **Single-adjudicator:** Gold is single-human research with LLM advisory, as documented.
3. **Gold not locked:** Lock file not yet created. Final two-pass self-review needed.
4. **100 cases:** Small for some statistical claims but sufficient for this project's scale.

---

*End of V0.5 Gold Final Prelock Validation Report.*

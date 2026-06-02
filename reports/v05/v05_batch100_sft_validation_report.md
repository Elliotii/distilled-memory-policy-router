# V0.5 Batch100 SFT Validation Report

Date: 2026-06-01  
Context: 5.0-F — SFT format validation for batch100  
Status: Format validation only; no training performed

## 1. SFT Row Count

| Item | Count |
| --- | ---: |
| Batch100 cases | 100 |
| SFT messages | 100 |
| Source tag | `v05_batch100_dry_run` |
| `is_final_train_data` | all `false` |

## 2. Schema Check

All 100 SFT messages follow the standard chat format with system/user/assistant roles, case_id, source, and metadata. All required fields present.

## 3. Assistant == gold.dsl

All 100 assistant messages exactly match their case's `gold.dsl`. **0 mismatches.**

## 4. Parse Check

All 100 assistant DSL outputs parse correctly with `src.v04.parser.parse_policy_dsl()`. **0 parse errors.**

## 5. No Markdown / No JSON Check

- 0 messages contain markdown fences (```)
- 0 messages start with `{` (no JSON output)
- All messages are pure DSL text

## 6. System / User Rendering Summary

- System prompt: consistent across all 100 messages (~980 chars)
- User message format: `RUNTIME_CONTEXT / CANDIDATE_MEMORIES / CURRENT_UNITS`
- `CANDIDATE_MEMORIES` renders `NONE` when empty
- Average user message length: ~420 chars
- Average assistant message length: ~50 chars

## 7. One Rendered Example

### v05_batch100_0029 (education-platform, user_profile)

**User:**
```
RUNTIME_CONTEXT
project: education-platform
repo: learnhub
service: grading
task: add rubric-based grading

CANDIDATE_MEMORIES
m1 [service_memory]: The grading service currently supports points-based grading with configurable weights per assignment type.
m2 [repo_memory]: Grading configuration per course is stored in config/grading/course_overrides.yaml.

CURRENT_UNITS
u1: Add rubric-based grading as an alternative to points-based. Each rubric criterion has a max score and a description.
u2: The rubric definitions should be stored in the course configuration, not hardcoded in the grading service.
u3: I prefer grade reports that show a breakdown by rubric criterion with comments from the instructor.
```

**Assistant:**
```
READ m1,m2
STORE service_memory u1
STORE repo_memory u2
STORE user_profile u3
SKIP NONE
```

## 8. Risks Before Real Training

- System prompt length fixed at ~980 chars; training must use this exact prompt
- Assistant is pure DSL; model deviations (markdown, JSON) would break parsing
- Tokenizer must handle DSL line breaks correctly (previously validated on Qwen3-4B with 100% parse success)
- Max token length not a concern at 100-case scale with 32K context window

## 9. Recommendation

The SFT format is stable and validated at 100-case scale. Ready for training data generation at 500+ case scale.

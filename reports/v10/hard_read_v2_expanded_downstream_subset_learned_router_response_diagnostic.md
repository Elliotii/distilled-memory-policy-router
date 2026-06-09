# Learned-Router Downstream Response Diagnostic

## API Run Boundary

- Context: 7.6-E learned_router-only downstream subset extension.
- Prompt count: 8
- Response rows: 8
- API OK count: 8
- Usable nonempty response count: 7
- Empty OK count: 1
- Error count: 0
- Retry distribution: {'0': 7, '2': 1}
- Payload metadata sent: false, per runner report.
- Existing 48 prompts were not rerun.
- New AutoDL inference, Qwen/LoRA loading, training, live serving, and UI work were not run.

## Citation Hygiene

- Hallucinated memory citation rows: 0
- Current-unit citation rows: 0
- Bare memory reference rows: 0
- No-response rows: 1
- Contradictory citation rows: 4
- Avoid citation rows: 6
- Stale citation rows: 1

| issue | prompt_id | details |
| --- | --- | --- |
| no_response | `hard_read_v2_009__learned_router` | `n/a` |
| contradictory | `hard_read_v2_026__learned_router` | `m456` |
| contradictory | `hard_read_v2_011__learned_router` | `m306` |
| contradictory | `hard_read_v2_013__learned_router` | `m326` |
| contradictory | `hard_read_v2_031__learned_router` | `m506` |
| avoid | `hard_read_v2_026__learned_router` | `m456` |
| avoid | `hard_read_v2_011__learned_router` | `m305, m306` |
| avoid | `hard_read_v2_020__learned_router` | `m394` |
| avoid | `hard_read_v2_013__learned_router` | `m326` |
| avoid | `hard_read_v2_031__learned_router` | `m506` |
| avoid | `hard_read_v2_032__learned_router` | `m514` |
| stale | `hard_read_v2_011__learned_router` | `m305` |

## Automatic Citation Metrics

| metric | learned_router |
| --- | ---: |
| response_coverage | 0.875 |
| e2e_required_citation_recall | 0.5 |
| conditional_required_citation_recall | 0.75 |
| avg_avoid_citations | 0.875 |
| avg_stale_citations | 0.125 |
| avg_contradictory_citations | 0.5 |
| avg_wrong_scope_citations | 0.0 |
| avg_hallucinated_memory_citations | 0.0 |
| avg_bare_memory_refs | 0.0 |
| avg_current_unit_citations | 0.0 |
| no_response_count | 1 |

## Selection-vs-Response Observation

- Selection-level learned_router mean post required recall was 0.890625.
- Selection-level contradictory contamination existed: 19 contradictory memories injected across 32 cases.
- On this 8-prompt subset, automatic scoring found contradictory citations in 4 rows.
- Automatic scoring alone cannot judge whether those contradictions actually harmed answer quality; rubric review is required.

## Claim Boundary

- Automatic diagnostics only.
- No rubric review yet.
- No downstream utility proof yet.

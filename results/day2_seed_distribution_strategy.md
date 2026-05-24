# Day 2 Seed Distribution and Generation Strategy

## Scope

This report describes structural dataset distribution only. Passing the validator means the JSONL records satisfy schema constraints, exact-span constraints, candidate-memory ID constraints, duplicate checks, and category minimums. It does not prove semantic quality.

Semantic quality still requires human or LLM-assisted review for:

- Whether `read_hints` are genuinely relevant.
- Whether `write_spans` capture durable memory-worthy information.
- Whether `ignore_spans` are selective rather than exhaustive.
- Whether memory types are consistently labeled.
- Whether hard negatives are realistic.

## Current Seed Dataset

File: `data/seed_examples.jsonl`

Total cases: 40

### Category Counts

| category | count |
| --- | --- |
| simple_write | 4 |
| multi_write | 4 |
| read_relevant_memory | 4 |
| ignore_noise | 4 |
| correction_or_revision | 4 |
| context_dependent_reference | 4 |
| conflicting_memory | 4 |
| mixed_write_and_ignore | 4 |
| no_action_needed | 4 |
| distractor_memory_selection | 4 |

The seed set is category-balanced for Day 2.

### Memory Type Counts

Candidate memory types:

| memory_type | count |
| --- | --- |
| sop | 18 |
| fact | 24 |
| decision | 10 |
| task_state | 2 |

Target write types:

| memory_type | count |
| --- | --- |
| sop | 14 |
| fact | 3 |
| decision | 16 |
| task_state | 3 |

Target totals:

| target_field | count |
| --- | --- |
| read_hints | 28 |
| write_spans | 36 |
| ignore_spans | 15 |

## Observed Biases

The current seed set is intentionally small and category-balanced, but it has several type-level biases:

- `decision` and `sop` dominate `target.write_spans`.
- `fact` and `task_state` are underrepresented as write targets.
- `task_state` is rare in `candidate_memories`.
- Read-selection examples mostly involve `fact`, `sop`, and `decision`; more task-state read cases are needed.
- Ignore labels are present but still sparse relative to the importance of memory-pollution control.
- The seed set does not yet stress enough examples with many candidate memories, especially 5-8 candidates.
- The seed set does not yet include enough cases where structurally valid labels are semantically tempting but wrong.

Recent business-facing framing suggests a sharper MVP emphasis: the router should help an AI assistant remember project progress, durable preferences/decisions, and important facts while avoiding memory pollution. `sop` remains a valid label, but generic workflow rules are lower priority because many real systems handle SOP-like behavior through skills, rule files, `AGENTS.md`, `CLAUDE.md`, or project instructions.

## Generation Strategy

For the first synthetic draft, keep category coverage close to balanced while deliberately correcting memory-type bias.

Recommended type targets for a first 500-case draft:

| dimension | target |
| --- | --- |
| category counts | 40-60 per category |
| target.write_spans `sop` | 10-15% |
| target.write_spans `decision` | 30-35% |
| target.write_spans `fact` | 25-30% |
| target.write_spans `task_state` | 20-25% |
| cases with ignore_spans | 25-35% |
| cases with candidate_memories | 50-70% |
| cases with recent_context | 25-40% |
| cases with 5-8 candidate_memories | 15-25% |

Prompt-level adjustments:

- Ask the direct coding-agent prompt to generate more durable `fact`, preference/decision, and active `task_state` writes.
- Ask the game-dev prompt to generate more task continuation, active debugging, and next-step cases.
- Ask the hard-negative prompt to generate more irrelevant candidate memories and more no-action cases with tempting candidates.
- Keep generic `sop` generation low unless the user explicitly states a durable workflow rule.
- Add explicit scenario-card fields for desired memory type mix before asking for final JSONL.
- Keep `ignore_spans` selective; do not ask the generator to label every non-written phrase.

Validation strategy:

- Treat validator success as structural validity only.
- Review a stratified sample of generated records by category and memory type.
- Track type confusion manually, especially `decision` vs `task_state` and `sop` vs `decision`.
- Quarantine invalid records automatically and inspect recurring failure modes before increasing generation scale.

## DeepSeek API Readiness

The project is ready to connect a real teacher API only after:

- The offline pipeline output paths and invalid quarantine have been committed.
- The generation prompt versions are treated as stable run metadata.
- A small real API smoke test plan exists with a strict budget and a maximum case count.
- Generated API output is first written to `raw_cases.jsonl`, then validated and split into `cases.jsonl` and `invalid_samples.jsonl`.
- No real API output is allowed directly into train/dev/gold files without structural validation and review.

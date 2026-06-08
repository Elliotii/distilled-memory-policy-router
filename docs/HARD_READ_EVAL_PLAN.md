# Hard READ Eval Plan

## Why Current gold_v2_009 Is Not Enough For READ Value

The locked `gold_v2_009` benchmark is useful for intrinsic router evaluation, but it is not sufficient to establish READ value in an applied memory setting.

Known issues:

- Candidate pools are small and clean.
- Distractor density is low.
- Candidate ordering can make simple top-k unexpectedly strong.
- READ labels often correlate with entity/domain matching.
- The benchmark does not fully test stale, contradictory, wrong-scope, or near-duplicate candidate memories.

The hard READ evaluation should test whether a selector can improve answer quality and reduce contamination when the candidate pool contains realistic distractors.

## Eval Size

Target size:

- 30-40 cases.
- 8-15 candidate memories per case.
- At least 3 strategies that do not use learned routing.
- At least 1 oracle reference strategy.

The set should be small enough for manual/rubric review and large enough to expose repeated failure patterns.

## Relevance Categories

Relevance labels are case-specific judgments, not global memory properties. The same memory can be required in one task, helpful in another, and irrelevant or wrong-scope in a third. Each case should label each candidate memory as one of:

| Category | Meaning |
| --- | --- |
| `required` | Needed for a high-quality grounded answer. |
| `helpful` | Useful but not necessary. |
| `irrelevant` | Not useful for the current task. |
| `stale_or_harmful` | Old, resolved, misleading, or harmful if treated as active. |
| `contradictory` | Conflicts with current task facts or other trusted memory. |
| `wrong_scope` | Belongs to another repo, service, user, or project. |

## Hard Negative Types

Hard negative labels are also case-specific. They should describe why a candidate is difficult or risky for this particular task. Hard negative labels should include:

- `same_entity_irrelevant`;
- `stale`;
- `contradictory`;
- `wrong_scope`;
- `near_duplicate`;
- `sensitive_boundary`.

These negatives are critical because easy irrelevant memories do not test READ relevance.

## Case JSONL Schema

Planned schema:

```json
{
  "case_id": "hard_read_001",
  "task": {
    "user_input": "string",
    "project": "string",
    "repo": "string",
    "service": "string",
    "current_units": [
      {
        "unit_id": "u1",
        "text": "string",
        "flags": []
      }
    ]
  },
  "candidate_memory_ids": ["m1", "m2"],
  "labels": {
    "required_memory_ids": ["m1"],
    "helpful_memory_ids": ["m2"],
    "avoid_memory_ids": ["m3"],
    "stale_or_harmful_memory_ids": ["m4"],
    "contradictory_memory_ids": ["m5"],
    "wrong_scope_memory_ids": ["m6"],
    "candidate_labels": {
      "m1": {
        "relevance_category": "required",
        "hard_negative_type": null
      },
      "m4": {
        "relevance_category": "stale_or_harmful",
        "hard_negative_type": "stale"
      }
    }
  },
  "expected_answer_requirements": [
    "must mention repo test command",
    "must avoid stale incident note"
  ],
  "notes": "string"
}
```

## Memory Pool Schema

Planned schema for a shared memory pool. It contains intrinsic memory fields only:

```json
{
  "memory_id": "m1",
  "text": "string",
  "target": "repo_memory",
  "project": "string",
  "repo": "string",
  "service": "string",
  "flags": ["stale", "sensitive_boundary"],
  "created_at": "fixture timestamp",
  "source": "fixture"
}
```

If a memory pool is shared across cases, relevance and hard-negative type must live in the case label section. Only case-local candidate files may place `relevance_category` or `hard_negative_type` directly on candidate rows.

## Strategies

Evaluate at least:

| Strategy | Meaning |
| --- | --- |
| `no_memory` | Inject no memories. |
| `all_candidates` | Inject all candidates. |
| `keyword_top_k` / `BM25_top_k` | Select top-k lexical matches. |
| `embedding_top_k` | Optional if feasible; honest semantic similarity baseline. |
| `random_k` | Fixed-seed random k. |
| `router_or_reranker_selected` | Learned router or reranker selection. |
| `oracle_selected` | Required plus chosen helpful memories. |

## Automatic Metrics

Automatic metrics should be diagnostic, not final answer-quality proof:

| Metric | Meaning |
| --- | --- |
| `selected_count` | Number of selected memories. |
| `context_chars` | Character count of selected memory context. |
| `required_selected_recall` | Required memories selected / required memories. |
| `avoid_selected_count` | Avoid memories selected. |
| `stale_selected_count` | Stale or harmful memories selected. |
| `contradiction_selected_count` | Contradictory memories selected. |
| `cited_required_recall` | Required memories cited in answer / required memories. |
| `cited_avoid_count` | Avoid memories cited in answer. |

## Qualitative / Judge Metrics

Use rubric-based manual or judge review:

| Metric | Direction | Meaning |
| --- | --- | --- |
| `required_fact_coverage` | Higher is better | Required facts are used correctly. |
| `irrelevant_memory_contamination` | Lower is better | Irrelevant selected memories affect the answer. |
| `stale_or_contradictory_use` | Lower is better | Stale or contradictory facts are used. |
| `hallucinated_memory_use` | Lower is better | Unsupported memory facts appear. |
| `task_response_quality` | Higher is better | Answer is useful and aligned with task. |
| `citation_compliance` | Higher is better | Citations are well formed and appropriate. |

Optional utility score:

```text
utility = required_fact_coverage
        + task_response_quality
        + citation_compliance
        - irrelevant_memory_contamination
        - stale_or_contradictory_use
        - hallucinated_memory_use
```

Do not overinterpret this score. It is a compact review aid, not a universal quality metric.

## Decisive Question

The decisive question is:

> Does router/reranker selection beat all-candidates and simple baselines on answer quality and contamination when realistic distractors exist?

The answer may be negative. That is acceptable and valuable. A negative result would show that lexical or embedding retrieval is sufficient for READ, and that learned routing should focus on STORE/SKIP/target or on reranking only after stronger supervision.

## Reporting Requirements

Reports should separate:

- selection quality;
- downstream answer quality;
- contamination;
- citation compliance;
- context size;
- examples where the router/reranker loses to simple baselines.

Do not collapse all evidence into a single headline score.

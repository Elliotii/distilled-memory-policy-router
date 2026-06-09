# Learned-Router Case Audit

This audit is diagnostic. It uses `reports/v10/hard_read_v2_expanded_learned_router_selection_eval/by_case.jsonl` and does not make downstream response-quality claims.

## Full Required Recall

`replay_learned_router` reached full post-budget required recall on 25 of 32 cases:

```text
hard_read_v2_001, hard_read_v2_002, hard_read_v2_003, hard_read_v2_004,
hard_read_v2_006, hard_read_v2_007, hard_read_v2_008, hard_read_v2_009,
hard_read_v2_010, hard_read_v2_012, hard_read_v2_013, hard_read_v2_014,
hard_read_v2_015, hard_read_v2_016, hard_read_v2_018, hard_read_v2_019,
hard_read_v2_021, hard_read_v2_022, hard_read_v2_023, hard_read_v2_024,
hard_read_v2_025, hard_read_v2_027, hard_read_v2_028, hard_read_v2_029,
hard_read_v2_030
```

Ten cases had full required recall and no avoid-memory injection:

| case | injected memory IDs |
| --- | --- |
| `hard_read_v2_002` | `m211`, `m213`, `m212` |
| `hard_read_v2_003` | `m223`, `m221`, `m222` |
| `hard_read_v2_004` | `m231`, `m232`, `m233` |
| `hard_read_v2_007` | `m261`, `m262` |
| `hard_read_v2_012` | `m311`, `m312`, `m313` |
| `hard_read_v2_014` | `m331`, `m332` |
| `hard_read_v2_016` | `m353`, `m351`, `m352` |
| `hard_read_v2_018` | `m371`, `m373`, `m372` |
| `hard_read_v2_024` | `m431`, `m432`, `m433` |
| `hard_read_v2_029` | `m481`, `m482` |

## Missed Required Memories

Seven cases missed one required memory post-budget:

| case | recall | required IDs | injected IDs |
| --- | ---: | --- | --- |
| `hard_read_v2_005` | 0.50 | `m241`, `m242` | `m241`, `m243`, `m246`, `m248` |
| `hard_read_v2_011` | 0.50 | `m301`, `m302` | `m301`, `m303`, `m305`, `m306` |
| `hard_read_v2_017` | 0.50 | `m361`, `m362` | `m361`, `m363`, `m364` |
| `hard_read_v2_020` | 0.50 | `m391`, `m392` | `m394`, `m391`, `m393` |
| `hard_read_v2_026` | 0.50 | `m451`, `m452` | `m451`, `m453`, `m456` |
| `hard_read_v2_031` | 0.50 | `m501`, `m502` | `m501`, `m503`, `m506` |
| `hard_read_v2_032` | 0.50 | `m511`, `m512` | `m511`, `m513`, `m514` |

These are the main cases for diagnosing READ transfer limitations.

## Contradictory Injection

Contradictory memory was injected in 19 cases:

```text
hard_read_v2_001, hard_read_v2_005, hard_read_v2_006, hard_read_v2_008,
hard_read_v2_009, hard_read_v2_010, hard_read_v2_011, hard_read_v2_013,
hard_read_v2_015, hard_read_v2_019, hard_read_v2_021, hard_read_v2_022,
hard_read_v2_023, hard_read_v2_025, hard_read_v2_026, hard_read_v2_027,
hard_read_v2_028, hard_read_v2_030, hard_read_v2_031
```

This is the most important downstream risk. A downstream answerer may still answer correctly if the required memories dominate, but that must be tested rather than assumed.

## Avoid-Memory Injection

Avoid memory was injected in 22 cases, totaling 25 post-budget avoid injections. The largest avoid counts were:

| case | avoid injected | injected IDs |
| --- | ---: | --- |
| `hard_read_v2_005` | 2 | `m241`, `m243`, `m246`, `m248` |
| `hard_read_v2_011` | 2 | `m301`, `m303`, `m305`, `m306` |
| `hard_read_v2_030` | 2 | `m491`, `m495`, `m496`, `m492` |

Stale memory was injected in `hard_read_v2_011` and `hard_read_v2_030`. Wrong-scope and sensitive-boundary memory were not injected post-budget.

## Zero-Selection Cases

There were no zero-selected or zero-injected learned-router cases.

## Downstream Subset Candidates

Recommended examples for the next downstream learned-router subset:

- `hard_read_v2_002`: clean full-recall/no-avoid case.
- `hard_read_v2_003`: clean full-recall/no-avoid case.
- `hard_read_v2_005`: miss plus contradictory/avoid injection.
- `hard_read_v2_011`: miss plus stale and contradictory injection.
- `hard_read_v2_030`: full required recall but stale and contradictory injection.
- `hard_read_v2_031`: miss plus contradictory injection.
- `hard_read_v2_032`: miss plus avoid injection.
- One existing downstream subset case with strong all-candidates contamination, to compare whether learned-router selection reduces answer pollution.

The downstream subset should report positive and negative outcomes without modifying fixture labels.

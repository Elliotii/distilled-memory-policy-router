# Learned-Router Manual Review Report

This is an internal rubric review of the 8 learned_router downstream responses. It uses the same 0/1/2 rubric dimensions as the existing expanded downstream subset review.

## Aggregate

| Strategy | Count | Utility | Req facts | Irrelevant clean | Stale/contrad clean | Hallucination clean | Quality | Citation | Missing req | Material contamination | Stale/contrad material | No response |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `learned_router` | 8 | 7.12 | 0.75 | 0.88 | 1.12 | 2.00 | 0.62 | 1.75 | 7 | 3 | 3 | 1 |

## Case Notes

| Case | Utility | Empty | Rationale |
| --- | ---: | --- | --- |
| `hard_read_v2_009` | 6 | true | Empty API response after retries. It has no harmful content, but it is unusable and covers no required facts or citations. |
| `hard_read_v2_026` | 4 | false | The answer follows the contradictory one-failure quarantine memory and omits the required three-failures-within-24-hours rule and Swift test command. |
| `hard_read_v2_011` | 8 | false | The response correctly suppresses revoked opt-in rows and includes audit fields, but misses the pytest command. It cites stale/contradictory memories only to reject them. |
| `hard_read_v2_020` | 9 | false | The response covers the high-volume activation blocking rule and optional fields, but misses the pytest command and leans on an irrelevant profile-completeness memory. |
| `hard_read_v2_013` | 4 | false | The response uses the contradictory Account-Owners route and directly violates the required Escalations-Refunds routing rule, despite including the pytest command. |
| `hard_read_v2_014` | 12 | false | Complete, useful answer with the recovery_code_set_id rotation rule and correct pytest command; no hard-negative contamination. |
| `hard_read_v2_031` | 5 | false | The response cites the 2 percent/6 minute threshold and annotation fields, but adopts the contradictory dashboard-only/business-hours suppression and misses the promtool validation command. |
| `hard_read_v2_032` | 9 | false | The response requires primary and backup owners and includes optional metadata, but misses the pytest command and cites an irrelevant style-check memory as a harmless validation note. |

## Boundary

This report does not call APIs, rerun responses, or prove general downstream utility. It is a small diagnostic rubric review.

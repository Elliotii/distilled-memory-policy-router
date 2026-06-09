# v1.0 Applied Downstream Empty Response Sensitivity

This sensitivity analysis uses only the committed learned_router manual review rows. It does not rerun the empty response and does not replace the primary audited metric.

## Result

| metric | value |
| --- | ---: |
| learned_router mean utility including all 8 rows | 7.125 |
| learned_router mean utility excluding empty/unusable rows | 7.286 |
| empty-response prompt_id | `hard_read_v2_009__learned_router` |
| empty-response case_id | `hard_read_v2_009` |
| empty-response total utility score | 6 |
| no_memory mean utility | 8.000 |
| all_candidates mean utility | 8.750 |
| oracle_selected mean utility | 12.000 |

Excluding the empty response does not change the comparison with no_memory: learned_router rises from 7.125 to 7.286, but remains below no_memory at 8.000. The primary audited metric remains the all-row mean of 7.125 because the empty response is part of the actual downstream run.

## Interpretation

The empty response worsened learned_router's mean utility, but it is not the only failure mechanism. The non-empty rows still show missed required facts and contradictory contamination. This supports a negative/limited downstream transfer interpretation, not a downstream win.

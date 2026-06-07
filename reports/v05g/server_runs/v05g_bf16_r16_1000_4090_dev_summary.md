# Dev Evaluation: v05g_bf16_r16_1000_4090

- Split: `dev`
- Cases: 100
- Interface: unit_json

## Structural

| Metric | Value |
|--------|-------|
| Parse success | 100/100 (100.0%) |
| Exact match | 59/100 (59.0%) |

## Semantic

| Metric | F1 |
|--------|-----|
| Read | P=89.5% R=97.4% F1=93.3% |
| Store unit | P=94.8% R=99.5% F1=97.1% |
| Skip unit | P=97.0% R=72.7% F1=83.1% |

## Store Target Accuracy

| Metric | Value |
|--------|-------|
| Target correct / compared | 196 / 219 |
| Target accuracy | 89.5% |

## Safety / Pollution

| Metric | Value |
|--------|-------|
| False store rate | 5.2% |
| Irrelevant read rate | 10.5% |
| Sensitive store rate | 2/3 (66.7%) |

## Target Confusion Matrix

| Gold target → Predicted target | Count |
|-------------------------------|-------|
| project_memory → project_memory | 26 |
| repo_memory → repo_memory | 34 |
| repo_memory → task_state | 2 |
| repo_memory → service_memory | 1 |
| service_memory → service_memory | 64 |
| service_memory → task_state | 5 |
| service_memory → repo_memory | 1 |
| service_memory → project_memory | 1 |
| task_state → task_state | 60 |
| task_state → service_memory | 8 |
| task_state → repo_memory | 5 |
| user_profile → user_profile | 12 |

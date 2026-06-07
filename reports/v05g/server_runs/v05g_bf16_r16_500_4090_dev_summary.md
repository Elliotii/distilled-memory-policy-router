# Dev Evaluation: v05g_bf16_r16_500_4090

- Split: `dev`
- Cases: 100
- Interface: unit_json

## Structural

| Metric | Value |
|--------|-------|
| Parse success | 100/100 (100.0%) |
| Exact match | 49/100 (49.0%) |

## Semantic

| Metric | F1 |
|--------|-----|
| Read | P=88.6% R=95.6% F1=92.0% |
| Store unit | P=94.8% R=98.6% F1=96.7% |
| Skip unit | P=91.4% R=72.7% F1=81.0% |

## Store Target Accuracy

| Metric | Value |
|--------|-------|
| Target correct / compared | 185 / 217 |
| Target accuracy | 85.3% |

## Safety / Pollution

| Metric | Value |
|--------|-------|
| False store rate | 5.2% |
| Irrelevant read rate | 11.4% |
| Sensitive store rate | 2/3 (66.7%) |

## Target Confusion Matrix

| Gold target → Predicted target | Count |
|-------------------------------|-------|
| project_memory → project_memory | 21 |
| project_memory → service_memory | 2 |
| project_memory → task_state | 2 |
| project_memory → repo_memory | 1 |
| repo_memory → repo_memory | 30 |
| repo_memory → task_state | 5 |
| repo_memory → project_memory | 1 |
| repo_memory → service_memory | 1 |
| service_memory → service_memory | 65 |
| service_memory → task_state | 5 |
| service_memory → repo_memory | 1 |
| task_state → task_state | 58 |
| task_state → service_memory | 9 |
| task_state → repo_memory | 4 |
| task_state → project_memory | 1 |
| user_profile → user_profile | 11 |

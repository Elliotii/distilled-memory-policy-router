# V0.5 Leakage Checker Report

**Train file:** `data/v05/batches/v05_batch500_corrected_cases.jsonl`  
**Candidate file:** `data/v05/batches/v05_batch500_corrected_cases.jsonl`  
**Train cases:** 500  
**Candidate cases:** 500  

> ⚠ **SELF-CHECK:** Train and candidate files are the same.  
> Exact overlaps are **expected** — this report is a tool sanity check,  
> not evidence of cross-split leakage.

## Summary

| Category | Count |
|----------|:----:|
| Hard blockers | 2385 |
| Review-level warnings | 6 |
| General warnings | 2409 |

## ❌ Hard Blockers (2385)

| Kind | Train case_id | Candidate case_id | Details |
|------|---------------|-------------------|---------|
| duplicate_case_id | `v05_batch100_0001` | `v05_batch100_0001` | (id-only) |
| duplicate_case_id | `v05_batch100_0002` | `v05_batch100_0002` | (id-only) |
| duplicate_case_id | `v05_batch100_0003` | `v05_batch100_0003` | (id-only) |
| duplicate_case_id | `v05_batch100_0004` | `v05_batch100_0004` | (id-only) |
| duplicate_case_id | `v05_batch100_0005` | `v05_batch100_0005` | (id-only) |
| duplicate_case_id | `v05_batch100_0006` | `v05_batch100_0006` | (id-only) |
| duplicate_case_id | `v05_batch100_0007` | `v05_batch100_0007` | (id-only) |
| duplicate_case_id | `v05_batch100_0008` | `v05_batch100_0008` | (id-only) |
| duplicate_case_id | `v05_batch100_0009` | `v05_batch100_0009` | (id-only) |
| duplicate_case_id | `v05_batch100_0010` | `v05_batch100_0010` | (id-only) |
| duplicate_case_id | `v05_batch100_0011` | `v05_batch100_0011` | (id-only) |
| duplicate_case_id | `v05_batch100_0012` | `v05_batch100_0012` | (id-only) |
| duplicate_case_id | `v05_batch100_0013` | `v05_batch100_0013` | (id-only) |
| duplicate_case_id | `v05_batch100_0014` | `v05_batch100_0014` | (id-only) |
| duplicate_case_id | `v05_batch100_0015` | `v05_batch100_0015` | (id-only) |
| duplicate_case_id | `v05_batch100_0016` | `v05_batch100_0016` | (id-only) |
| duplicate_case_id | `v05_batch100_0017` | `v05_batch100_0017` | (id-only) |
| duplicate_case_id | `v05_batch100_0018` | `v05_batch100_0018` | (id-only) |
| duplicate_case_id | `v05_batch100_0019` | `v05_batch100_0019` | (id-only) |
| duplicate_case_id | `v05_batch100_0020` | `v05_batch100_0020` | (id-only) |
| duplicate_case_id | `v05_batch100_0021` | `v05_batch100_0021` | (id-only) |
| duplicate_case_id | `v05_batch100_0022` | `v05_batch100_0022` | (id-only) |
| duplicate_case_id | `v05_batch100_0023` | `v05_batch100_0023` | (id-only) |
| duplicate_case_id | `v05_batch100_0024` | `v05_batch100_0024` | (id-only) |
| duplicate_case_id | `v05_batch100_0025` | `v05_batch100_0025` | (id-only) |
| duplicate_case_id | `v05_batch100_0026` | `v05_batch100_0026` | (id-only) |
| duplicate_case_id | `v05_batch100_0027` | `v05_batch100_0027` | (id-only) |
| duplicate_case_id | `v05_batch100_0028` | `v05_batch100_0028` | (id-only) |
| duplicate_case_id | `v05_batch100_0029` | `v05_batch100_0029` | (id-only) |
| duplicate_case_id | `v05_batch100_0030` | `v05_batch100_0030` | (id-only) |
| duplicate_case_id | `v05_batch100_0031` | `v05_batch100_0031` | (id-only) |
| duplicate_case_id | `v05_batch100_0032` | `v05_batch100_0032` | (id-only) |
| duplicate_case_id | `v05_batch100_0033` | `v05_batch100_0033` | (id-only) |
| duplicate_case_id | `v05_batch100_0034` | `v05_batch100_0034` | (id-only) |
| duplicate_case_id | `v05_batch100_0035` | `v05_batch100_0035` | (id-only) |
| duplicate_case_id | `v05_batch100_0036` | `v05_batch100_0036` | (id-only) |
| duplicate_case_id | `v05_batch100_0037` | `v05_batch100_0037` | (id-only) |
| duplicate_case_id | `v05_batch100_0038` | `v05_batch100_0038` | (id-only) |
| duplicate_case_id | `v05_batch100_0039` | `v05_batch100_0039` | (id-only) |
| duplicate_case_id | `v05_batch100_0040` | `v05_batch100_0040` | (id-only) |
| duplicate_case_id | `v05_batch100_0041` | `v05_batch100_0041` | (id-only) |
| duplicate_case_id | `v05_batch100_0042` | `v05_batch100_0042` | (id-only) |
| duplicate_case_id | `v05_batch100_0043` | `v05_batch100_0043` | (id-only) |
| duplicate_case_id | `v05_batch100_0044` | `v05_batch100_0044` | (id-only) |
| duplicate_case_id | `v05_batch100_0045` | `v05_batch100_0045` | (id-only) |
| duplicate_case_id | `v05_batch100_0046` | `v05_batch100_0046` | (id-only) |
| duplicate_case_id | `v05_batch100_0047` | `v05_batch100_0047` | (id-only) |
| duplicate_case_id | `v05_batch100_0048` | `v05_batch100_0048` | (id-only) |
| duplicate_case_id | `v05_batch100_0049` | `v05_batch100_0049` | (id-only) |
| duplicate_case_id | `v05_batch100_0050` | `v05_batch100_0050` | (id-only) |
| duplicate_case_id | `v05_batch200_0001` | `v05_batch200_0001` | (id-only) |
| duplicate_case_id | `v05_batch200_0002` | `v05_batch200_0002` | (id-only) |
| duplicate_case_id | `v05_batch200_0003` | `v05_batch200_0003` | (id-only) |
| duplicate_case_id | `v05_batch200_0004` | `v05_batch200_0004` | (id-only) |
| duplicate_case_id | `v05_batch200_0005` | `v05_batch200_0005` | (id-only) |
| duplicate_case_id | `v05_batch200_0006` | `v05_batch200_0006` | (id-only) |
| duplicate_case_id | `v05_batch200_0007` | `v05_batch200_0007` | (id-only) |
| duplicate_case_id | `v05_batch200_0008` | `v05_batch200_0008` | (id-only) |
| duplicate_case_id | `v05_batch200_0009` | `v05_batch200_0009` | (id-only) |
| duplicate_case_id | `v05_batch200_0010` | `v05_batch200_0010` | (id-only) |
| duplicate_case_id | `v05_batch200_0011` | `v05_batch200_0011` | (id-only) |
| duplicate_case_id | `v05_batch200_0012` | `v05_batch200_0012` | (id-only) |
| duplicate_case_id | `v05_batch200_0013` | `v05_batch200_0013` | (id-only) |
| duplicate_case_id | `v05_batch200_0014` | `v05_batch200_0014` | (id-only) |
| duplicate_case_id | `v05_batch200_0015` | `v05_batch200_0015` | (id-only) |
| duplicate_case_id | `v05_batch200_0016` | `v05_batch200_0016` | (id-only) |
| duplicate_case_id | `v05_batch200_0017` | `v05_batch200_0017` | (id-only) |
| duplicate_case_id | `v05_batch200_0018` | `v05_batch200_0018` | (id-only) |
| duplicate_case_id | `v05_batch200_0019` | `v05_batch200_0019` | (id-only) |
| duplicate_case_id | `v05_batch200_0020` | `v05_batch200_0020` | (id-only) |
| duplicate_case_id | `v05_batch200_0021` | `v05_batch200_0021` | (id-only) |
| duplicate_case_id | `v05_batch200_0022` | `v05_batch200_0022` | (id-only) |
| duplicate_case_id | `v05_batch200_0023` | `v05_batch200_0023` | (id-only) |
| duplicate_case_id | `v05_batch200_0024` | `v05_batch200_0024` | (id-only) |
| duplicate_case_id | `v05_batch200_0025` | `v05_batch200_0025` | (id-only) |
| duplicate_case_id | `v05_batch200_0026` | `v05_batch200_0026` | (id-only) |
| duplicate_case_id | `v05_batch200_0027` | `v05_batch200_0027` | (id-only) |
| duplicate_case_id | `v05_batch200_0028` | `v05_batch200_0028` | (id-only) |
| duplicate_case_id | `v05_batch200_0029` | `v05_batch200_0029` | (id-only) |
| duplicate_case_id | `v05_batch200_0030` | `v05_batch200_0030` | (id-only) |
| duplicate_case_id | `v05_batch200_0031` | `v05_batch200_0031` | (id-only) |
| duplicate_case_id | `v05_batch200_0032` | `v05_batch200_0032` | (id-only) |
| duplicate_case_id | `v05_batch200_0033` | `v05_batch200_0033` | (id-only) |
| duplicate_case_id | `v05_batch200_0034` | `v05_batch200_0034` | (id-only) |
| duplicate_case_id | `v05_batch200_0035` | `v05_batch200_0035` | (id-only) |
| duplicate_case_id | `v05_batch200_0036` | `v05_batch200_0036` | (id-only) |
| duplicate_case_id | `v05_batch200_0037` | `v05_batch200_0037` | (id-only) |
| duplicate_case_id | `v05_batch200_0038` | `v05_batch200_0038` | (id-only) |
| duplicate_case_id | `v05_batch200_0039` | `v05_batch200_0039` | (id-only) |
| duplicate_case_id | `v05_batch200_0040` | `v05_batch200_0040` | (id-only) |
| duplicate_case_id | `v05_batch200_0041` | `v05_batch200_0041` | (id-only) |
| duplicate_case_id | `v05_batch200_0042` | `v05_batch200_0042` | (id-only) |
| duplicate_case_id | `v05_batch200_0043` | `v05_batch200_0043` | (id-only) |
| duplicate_case_id | `v05_batch200_0044` | `v05_batch200_0044` | (id-only) |
| duplicate_case_id | `v05_batch200_0045` | `v05_batch200_0045` | (id-only) |
| duplicate_case_id | `v05_batch200_0046` | `v05_batch200_0046` | (id-only) |
| duplicate_case_id | `v05_batch200_0047` | `v05_batch200_0047` | (id-only) |
| duplicate_case_id | `v05_batch200_0048` | `v05_batch200_0048` | (id-only) |
| duplicate_case_id | `v05_batch200_0049` | `v05_batch200_0049` | (id-only) |
| duplicate_case_id | `v05_batch200_0050` | `v05_batch200_0050` | (id-only) |
| duplicate_case_id | `v05_batch200_0051` | `v05_batch200_0051` | (id-only) |
| duplicate_case_id | `v05_batch200_0052` | `v05_batch200_0052` | (id-only) |
| duplicate_case_id | `v05_batch200_0053` | `v05_batch200_0053` | (id-only) |
| duplicate_case_id | `v05_batch200_0054` | `v05_batch200_0054` | (id-only) |
| duplicate_case_id | `v05_batch200_0055` | `v05_batch200_0055` | (id-only) |
| duplicate_case_id | `v05_batch200_0056` | `v05_batch200_0056` | (id-only) |
| duplicate_case_id | `v05_batch200_0057` | `v05_batch200_0057` | (id-only) |
| duplicate_case_id | `v05_batch200_0058` | `v05_batch200_0058` | (id-only) |
| duplicate_case_id | `v05_batch200_0059` | `v05_batch200_0059` | (id-only) |
| duplicate_case_id | `v05_batch200_0060` | `v05_batch200_0060` | (id-only) |
| duplicate_case_id | `v05_batch200_0061` | `v05_batch200_0061` | (id-only) |
| duplicate_case_id | `v05_batch200_0062` | `v05_batch200_0062` | (id-only) |
| duplicate_case_id | `v05_batch200_0063` | `v05_batch200_0063` | (id-only) |
| duplicate_case_id | `v05_batch200_0064` | `v05_batch200_0064` | (id-only) |
| duplicate_case_id | `v05_batch200_0065` | `v05_batch200_0065` | (id-only) |
| duplicate_case_id | `v05_batch200_0066` | `v05_batch200_0066` | (id-only) |
| duplicate_case_id | `v05_batch200_0067` | `v05_batch200_0067` | (id-only) |
| duplicate_case_id | `v05_batch200_0068` | `v05_batch200_0068` | (id-only) |
| duplicate_case_id | `v05_batch200_0069` | `v05_batch200_0069` | (id-only) |
| duplicate_case_id | `v05_batch200_0070` | `v05_batch200_0070` | (id-only) |
| duplicate_case_id | `v05_batch200_0071` | `v05_batch200_0071` | (id-only) |
| duplicate_case_id | `v05_batch200_0072` | `v05_batch200_0072` | (id-only) |
| duplicate_case_id | `v05_batch200_0073` | `v05_batch200_0073` | (id-only) |
| duplicate_case_id | `v05_batch200_0074` | `v05_batch200_0074` | (id-only) |
| duplicate_case_id | `v05_batch200_0075` | `v05_batch200_0075` | (id-only) |
| duplicate_case_id | `v05_batch200_0076` | `v05_batch200_0076` | (id-only) |
| duplicate_case_id | `v05_batch200_0077` | `v05_batch200_0077` | (id-only) |
| duplicate_case_id | `v05_batch200_0078` | `v05_batch200_0078` | (id-only) |
| duplicate_case_id | `v05_batch200_0079` | `v05_batch200_0079` | (id-only) |
| duplicate_case_id | `v05_batch200_0080` | `v05_batch200_0080` | (id-only) |
| duplicate_case_id | `v05_batch200_0081` | `v05_batch200_0081` | (id-only) |
| duplicate_case_id | `v05_batch200_0082` | `v05_batch200_0082` | (id-only) |
| duplicate_case_id | `v05_batch200_0083` | `v05_batch200_0083` | (id-only) |
| duplicate_case_id | `v05_batch200_0084` | `v05_batch200_0084` | (id-only) |
| duplicate_case_id | `v05_batch200_0085` | `v05_batch200_0085` | (id-only) |
| duplicate_case_id | `v05_batch200_0086` | `v05_batch200_0086` | (id-only) |
| duplicate_case_id | `v05_batch200_0087` | `v05_batch200_0087` | (id-only) |
| duplicate_case_id | `v05_batch200_0088` | `v05_batch200_0088` | (id-only) |
| duplicate_case_id | `v05_batch200_0089` | `v05_batch200_0089` | (id-only) |
| duplicate_case_id | `v05_batch200_0090` | `v05_batch200_0090` | (id-only) |
| duplicate_case_id | `v05_batch200_0091` | `v05_batch200_0091` | (id-only) |
| duplicate_case_id | `v05_batch200_0092` | `v05_batch200_0092` | (id-only) |
| duplicate_case_id | `v05_batch200_0093` | `v05_batch200_0093` | (id-only) |
| duplicate_case_id | `v05_batch200_0094` | `v05_batch200_0094` | (id-only) |
| duplicate_case_id | `v05_batch200_0095` | `v05_batch200_0095` | (id-only) |
| duplicate_case_id | `v05_batch200_0096` | `v05_batch200_0096` | (id-only) |
| duplicate_case_id | `v05_batch200_0097` | `v05_batch200_0097` | (id-only) |
| duplicate_case_id | `v05_batch200_0098` | `v05_batch200_0098` | (id-only) |
| duplicate_case_id | `v05_batch200_0099` | `v05_batch200_0099` | (id-only) |
| duplicate_case_id | `v05_batch200_0100` | `v05_batch200_0100` | (id-only) |
| duplicate_case_id | `v05_batch300_0001` | `v05_batch300_0001` | (id-only) |
| duplicate_case_id | `v05_batch300_0002` | `v05_batch300_0002` | (id-only) |
| duplicate_case_id | `v05_batch300_0003` | `v05_batch300_0003` | (id-only) |
| duplicate_case_id | `v05_batch300_0004` | `v05_batch300_0004` | (id-only) |
| duplicate_case_id | `v05_batch300_0005` | `v05_batch300_0005` | (id-only) |
| duplicate_case_id | `v05_batch300_0006` | `v05_batch300_0006` | (id-only) |
| duplicate_case_id | `v05_batch300_0007` | `v05_batch300_0007` | (id-only) |
| duplicate_case_id | `v05_batch300_0008` | `v05_batch300_0008` | (id-only) |
| duplicate_case_id | `v05_batch300_0009` | `v05_batch300_0009` | (id-only) |
| duplicate_case_id | `v05_batch300_0010` | `v05_batch300_0010` | (id-only) |
| duplicate_case_id | `v05_batch300_0011` | `v05_batch300_0011` | (id-only) |
| duplicate_case_id | `v05_batch300_0012` | `v05_batch300_0012` | (id-only) |
| duplicate_case_id | `v05_batch300_0013` | `v05_batch300_0013` | (id-only) |
| duplicate_case_id | `v05_batch300_0014` | `v05_batch300_0014` | (id-only) |
| duplicate_case_id | `v05_batch300_0015` | `v05_batch300_0015` | (id-only) |
| duplicate_case_id | `v05_batch300_0016` | `v05_batch300_0016` | (id-only) |
| duplicate_case_id | `v05_batch300_0017` | `v05_batch300_0017` | (id-only) |
| duplicate_case_id | `v05_batch300_0018` | `v05_batch300_0018` | (id-only) |
| duplicate_case_id | `v05_batch300_0019` | `v05_batch300_0019` | (id-only) |
| duplicate_case_id | `v05_batch300_0020` | `v05_batch300_0020` | (id-only) |
| duplicate_case_id | `v05_batch300_0021` | `v05_batch300_0021` | (id-only) |
| duplicate_case_id | `v05_batch300_0022` | `v05_batch300_0022` | (id-only) |
| duplicate_case_id | `v05_batch300_0023` | `v05_batch300_0023` | (id-only) |
| duplicate_case_id | `v05_batch300_0024` | `v05_batch300_0024` | (id-only) |
| duplicate_case_id | `v05_batch300_0025` | `v05_batch300_0025` | (id-only) |
| duplicate_case_id | `v05_batch300_0026` | `v05_batch300_0026` | (id-only) |
| duplicate_case_id | `v05_batch300_0027` | `v05_batch300_0027` | (id-only) |
| duplicate_case_id | `v05_batch300_0028` | `v05_batch300_0028` | (id-only) |
| duplicate_case_id | `v05_batch300_0029` | `v05_batch300_0029` | (id-only) |
| duplicate_case_id | `v05_batch300_0030` | `v05_batch300_0030` | (id-only) |
| duplicate_case_id | `v05_batch300_0031` | `v05_batch300_0031` | (id-only) |
| duplicate_case_id | `v05_batch300_0032` | `v05_batch300_0032` | (id-only) |
| duplicate_case_id | `v05_batch300_0033` | `v05_batch300_0033` | (id-only) |
| duplicate_case_id | `v05_batch300_0034` | `v05_batch300_0034` | (id-only) |
| duplicate_case_id | `v05_batch300_0035` | `v05_batch300_0035` | (id-only) |
| duplicate_case_id | `v05_batch300_0036` | `v05_batch300_0036` | (id-only) |
| duplicate_case_id | `v05_batch300_0037` | `v05_batch300_0037` | (id-only) |
| duplicate_case_id | `v05_batch300_0038` | `v05_batch300_0038` | (id-only) |
| duplicate_case_id | `v05_batch300_0039` | `v05_batch300_0039` | (id-only) |
| duplicate_case_id | `v05_batch300_0040` | `v05_batch300_0040` | (id-only) |
| duplicate_case_id | `v05_batch300_0041` | `v05_batch300_0041` | (id-only) |
| duplicate_case_id | `v05_batch300_0042` | `v05_batch300_0042` | (id-only) |
| duplicate_case_id | `v05_batch300_0043` | `v05_batch300_0043` | (id-only) |
| duplicate_case_id | `v05_batch300_0044` | `v05_batch300_0044` | (id-only) |
| duplicate_case_id | `v05_batch300_0045` | `v05_batch300_0045` | (id-only) |
| duplicate_case_id | `v05_batch300_0046` | `v05_batch300_0046` | (id-only) |
| duplicate_case_id | `v05_batch300_0047` | `v05_batch300_0047` | (id-only) |
| duplicate_case_id | `v05_batch300_0048` | `v05_batch300_0048` | (id-only) |
| duplicate_case_id | `v05_batch300_0049` | `v05_batch300_0049` | (id-only) |
| duplicate_case_id | `v05_batch300_0050` | `v05_batch300_0050` | (id-only) |
| duplicate_case_id | `v05_batch300_0051` | `v05_batch300_0051` | (id-only) |
| duplicate_case_id | `v05_batch300_0052` | `v05_batch300_0052` | (id-only) |
| duplicate_case_id | `v05_batch300_0053` | `v05_batch300_0053` | (id-only) |
| duplicate_case_id | `v05_batch300_0054` | `v05_batch300_0054` | (id-only) |
| duplicate_case_id | `v05_batch300_0055` | `v05_batch300_0055` | (id-only) |
| duplicate_case_id | `v05_batch300_0056` | `v05_batch300_0056` | (id-only) |
| duplicate_case_id | `v05_batch300_0057` | `v05_batch300_0057` | (id-only) |
| duplicate_case_id | `v05_batch300_0058` | `v05_batch300_0058` | (id-only) |
| duplicate_case_id | `v05_batch300_0059` | `v05_batch300_0059` | (id-only) |
| duplicate_case_id | `v05_batch300_0060` | `v05_batch300_0060` | (id-only) |
| duplicate_case_id | `v05_batch300_0061` | `v05_batch300_0061` | (id-only) |
| duplicate_case_id | `v05_batch300_0062` | `v05_batch300_0062` | (id-only) |
| duplicate_case_id | `v05_batch300_0063` | `v05_batch300_0063` | (id-only) |
| duplicate_case_id | `v05_batch300_0064` | `v05_batch300_0064` | (id-only) |
| duplicate_case_id | `v05_batch300_0065` | `v05_batch300_0065` | (id-only) |
| duplicate_case_id | `v05_batch300_0066` | `v05_batch300_0066` | (id-only) |
| duplicate_case_id | `v05_batch300_0067` | `v05_batch300_0067` | (id-only) |
| duplicate_case_id | `v05_batch300_0068` | `v05_batch300_0068` | (id-only) |
| duplicate_case_id | `v05_batch300_0069` | `v05_batch300_0069` | (id-only) |
| duplicate_case_id | `v05_batch300_0070` | `v05_batch300_0070` | (id-only) |
| duplicate_case_id | `v05_batch300_0071` | `v05_batch300_0071` | (id-only) |
| duplicate_case_id | `v05_batch300_0072` | `v05_batch300_0072` | (id-only) |
| duplicate_case_id | `v05_batch300_0073` | `v05_batch300_0073` | (id-only) |
| duplicate_case_id | `v05_batch300_0074` | `v05_batch300_0074` | (id-only) |
| duplicate_case_id | `v05_batch300_0075` | `v05_batch300_0075` | (id-only) |
| duplicate_case_id | `v05_batch300_0076` | `v05_batch300_0076` | (id-only) |
| duplicate_case_id | `v05_batch300_0077` | `v05_batch300_0077` | (id-only) |
| duplicate_case_id | `v05_batch300_0078` | `v05_batch300_0078` | (id-only) |
| duplicate_case_id | `v05_batch300_0079` | `v05_batch300_0079` | (id-only) |
| duplicate_case_id | `v05_batch300_0080` | `v05_batch300_0080` | (id-only) |
| duplicate_case_id | `v05_batch300_0081` | `v05_batch300_0081` | (id-only) |
| duplicate_case_id | `v05_batch300_0082` | `v05_batch300_0082` | (id-only) |
| duplicate_case_id | `v05_batch300_0083` | `v05_batch300_0083` | (id-only) |
| duplicate_case_id | `v05_batch300_0084` | `v05_batch300_0084` | (id-only) |
| duplicate_case_id | `v05_batch300_0085` | `v05_batch300_0085` | (id-only) |
| duplicate_case_id | `v05_batch300_0086` | `v05_batch300_0086` | (id-only) |
| duplicate_case_id | `v05_batch300_0087` | `v05_batch300_0087` | (id-only) |
| duplicate_case_id | `v05_batch300_0088` | `v05_batch300_0088` | (id-only) |
| duplicate_case_id | `v05_batch300_0089` | `v05_batch300_0089` | (id-only) |
| duplicate_case_id | `v05_batch300_0090` | `v05_batch300_0090` | (id-only) |
| duplicate_case_id | `v05_batch300_0091` | `v05_batch300_0091` | (id-only) |
| duplicate_case_id | `v05_batch300_0092` | `v05_batch300_0092` | (id-only) |
| duplicate_case_id | `v05_batch300_0093` | `v05_batch300_0093` | (id-only) |
| duplicate_case_id | `v05_batch300_0094` | `v05_batch300_0094` | (id-only) |
| duplicate_case_id | `v05_batch300_0095` | `v05_batch300_0095` | (id-only) |
| duplicate_case_id | `v05_batch300_0096` | `v05_batch300_0096` | (id-only) |
| duplicate_case_id | `v05_batch300_0097` | `v05_batch300_0097` | (id-only) |
| duplicate_case_id | `v05_batch300_0098` | `v05_batch300_0098` | (id-only) |
| duplicate_case_id | `v05_batch300_0099` | `v05_batch300_0099` | (id-only) |
| duplicate_case_id | `v05_batch300_0100` | `v05_batch300_0100` | (id-only) |
| duplicate_case_id | `v05_batch500_0001` | `v05_batch500_0001` | (id-only) |
| duplicate_case_id | `v05_batch500_0002` | `v05_batch500_0002` | (id-only) |
| duplicate_case_id | `v05_batch500_0003` | `v05_batch500_0003` | (id-only) |
| duplicate_case_id | `v05_batch500_0004` | `v05_batch500_0004` | (id-only) |
| duplicate_case_id | `v05_batch500_0005` | `v05_batch500_0005` | (id-only) |
| duplicate_case_id | `v05_batch500_0006` | `v05_batch500_0006` | (id-only) |
| duplicate_case_id | `v05_batch500_0007` | `v05_batch500_0007` | (id-only) |
| duplicate_case_id | `v05_batch500_0008` | `v05_batch500_0008` | (id-only) |
| duplicate_case_id | `v05_batch500_0009` | `v05_batch500_0009` | (id-only) |
| duplicate_case_id | `v05_batch500_0010` | `v05_batch500_0010` | (id-only) |
| duplicate_case_id | `v05_batch500_0011` | `v05_batch500_0011` | (id-only) |
| duplicate_case_id | `v05_batch500_0012` | `v05_batch500_0012` | (id-only) |
| duplicate_case_id | `v05_batch500_0013` | `v05_batch500_0013` | (id-only) |
| duplicate_case_id | `v05_batch500_0014` | `v05_batch500_0014` | (id-only) |
| duplicate_case_id | `v05_batch500_0015` | `v05_batch500_0015` | (id-only) |
| duplicate_case_id | `v05_batch500_0016` | `v05_batch500_0016` | (id-only) |
| duplicate_case_id | `v05_batch500_0017` | `v05_batch500_0017` | (id-only) |
| duplicate_case_id | `v05_batch500_0018` | `v05_batch500_0018` | (id-only) |
| duplicate_case_id | `v05_batch500_0019` | `v05_batch500_0019` | (id-only) |
| duplicate_case_id | `v05_batch500_0020` | `v05_batch500_0020` | (id-only) |
| duplicate_case_id | `v05_batch500_0021` | `v05_batch500_0021` | (id-only) |
| duplicate_case_id | `v05_batch500_0022` | `v05_batch500_0022` | (id-only) |
| duplicate_case_id | `v05_batch500_0023` | `v05_batch500_0023` | (id-only) |
| duplicate_case_id | `v05_batch500_0024` | `v05_batch500_0024` | (id-only) |
| duplicate_case_id | `v05_batch500_0025` | `v05_batch500_0025` | (id-only) |
| duplicate_case_id | `v05_batch500_0026` | `v05_batch500_0026` | (id-only) |
| duplicate_case_id | `v05_batch500_0027` | `v05_batch500_0027` | (id-only) |
| duplicate_case_id | `v05_batch500_0028` | `v05_batch500_0028` | (id-only) |
| duplicate_case_id | `v05_batch500_0029` | `v05_batch500_0029` | (id-only) |
| duplicate_case_id | `v05_batch500_0030` | `v05_batch500_0030` | (id-only) |
| duplicate_case_id | `v05_batch500_0031` | `v05_batch500_0031` | (id-only) |
| duplicate_case_id | `v05_batch500_0032` | `v05_batch500_0032` | (id-only) |
| duplicate_case_id | `v05_batch500_0033` | `v05_batch500_0033` | (id-only) |
| duplicate_case_id | `v05_batch500_0034` | `v05_batch500_0034` | (id-only) |
| duplicate_case_id | `v05_batch500_0035` | `v05_batch500_0035` | (id-only) |
| duplicate_case_id | `v05_batch500_0036` | `v05_batch500_0036` | (id-only) |
| duplicate_case_id | `v05_batch500_0037` | `v05_batch500_0037` | (id-only) |
| duplicate_case_id | `v05_batch500_0038` | `v05_batch500_0038` | (id-only) |
| duplicate_case_id | `v05_batch500_0039` | `v05_batch500_0039` | (id-only) |
| duplicate_case_id | `v05_batch500_0040` | `v05_batch500_0040` | (id-only) |
| duplicate_case_id | `v05_batch500_0041` | `v05_batch500_0041` | (id-only) |
| duplicate_case_id | `v05_batch500_0042` | `v05_batch500_0042` | (id-only) |
| duplicate_case_id | `v05_batch500_0043` | `v05_batch500_0043` | (id-only) |
| duplicate_case_id | `v05_batch500_0044` | `v05_batch500_0044` | (id-only) |
| duplicate_case_id | `v05_batch500_0045` | `v05_batch500_0045` | (id-only) |
| duplicate_case_id | `v05_batch500_0046` | `v05_batch500_0046` | (id-only) |
| duplicate_case_id | `v05_batch500_0047` | `v05_batch500_0047` | (id-only) |
| duplicate_case_id | `v05_batch500_0048` | `v05_batch500_0048` | (id-only) |
| duplicate_case_id | `v05_batch500_0049` | `v05_batch500_0049` | (id-only) |
| duplicate_case_id | `v05_batch500_0050` | `v05_batch500_0050` | (id-only) |
| duplicate_case_id | `v05_batch500_0051` | `v05_batch500_0051` | (id-only) |
| duplicate_case_id | `v05_batch500_0052` | `v05_batch500_0052` | (id-only) |
| duplicate_case_id | `v05_batch500_0053` | `v05_batch500_0053` | (id-only) |
| duplicate_case_id | `v05_batch500_0054` | `v05_batch500_0054` | (id-only) |
| duplicate_case_id | `v05_batch500_0055` | `v05_batch500_0055` | (id-only) |
| duplicate_case_id | `v05_batch500_0056` | `v05_batch500_0056` | (id-only) |
| duplicate_case_id | `v05_batch500_0057` | `v05_batch500_0057` | (id-only) |
| duplicate_case_id | `v05_batch500_0058` | `v05_batch500_0058` | (id-only) |
| duplicate_case_id | `v05_batch500_0059` | `v05_batch500_0059` | (id-only) |
| duplicate_case_id | `v05_batch500_0060` | `v05_batch500_0060` | (id-only) |
| duplicate_case_id | `v05_batch500_0061` | `v05_batch500_0061` | (id-only) |
| duplicate_case_id | `v05_batch500_0062` | `v05_batch500_0062` | (id-only) |
| duplicate_case_id | `v05_batch500_0063` | `v05_batch500_0063` | (id-only) |
| duplicate_case_id | `v05_batch500_0064` | `v05_batch500_0064` | (id-only) |
| duplicate_case_id | `v05_batch500_0065` | `v05_batch500_0065` | (id-only) |
| duplicate_case_id | `v05_batch500_0066` | `v05_batch500_0066` | (id-only) |
| duplicate_case_id | `v05_batch500_0067` | `v05_batch500_0067` | (id-only) |
| duplicate_case_id | `v05_batch500_0068` | `v05_batch500_0068` | (id-only) |
| duplicate_case_id | `v05_batch500_0069` | `v05_batch500_0069` | (id-only) |
| duplicate_case_id | `v05_batch500_0070` | `v05_batch500_0070` | (id-only) |
| duplicate_case_id | `v05_batch500_0071` | `v05_batch500_0071` | (id-only) |
| duplicate_case_id | `v05_batch500_0072` | `v05_batch500_0072` | (id-only) |
| duplicate_case_id | `v05_batch500_0073` | `v05_batch500_0073` | (id-only) |
| duplicate_case_id | `v05_batch500_0074` | `v05_batch500_0074` | (id-only) |
| duplicate_case_id | `v05_batch500_0075` | `v05_batch500_0075` | (id-only) |
| duplicate_case_id | `v05_batch500_0076` | `v05_batch500_0076` | (id-only) |
| duplicate_case_id | `v05_batch500_0077` | `v05_batch500_0077` | (id-only) |
| duplicate_case_id | `v05_batch500_0078` | `v05_batch500_0078` | (id-only) |
| duplicate_case_id | `v05_batch500_0079` | `v05_batch500_0079` | (id-only) |
| duplicate_case_id | `v05_batch500_0080` | `v05_batch500_0080` | (id-only) |
| duplicate_case_id | `v05_batch500_0081` | `v05_batch500_0081` | (id-only) |
| duplicate_case_id | `v05_batch500_0082` | `v05_batch500_0082` | (id-only) |
| duplicate_case_id | `v05_batch500_0083` | `v05_batch500_0083` | (id-only) |
| duplicate_case_id | `v05_batch500_0084` | `v05_batch500_0084` | (id-only) |
| duplicate_case_id | `v05_batch500_0085` | `v05_batch500_0085` | (id-only) |
| duplicate_case_id | `v05_batch500_0086` | `v05_batch500_0086` | (id-only) |
| duplicate_case_id | `v05_batch500_0087` | `v05_batch500_0087` | (id-only) |
| duplicate_case_id | `v05_batch500_0088` | `v05_batch500_0088` | (id-only) |
| duplicate_case_id | `v05_batch500_0089` | `v05_batch500_0089` | (id-only) |
| duplicate_case_id | `v05_batch500_0090` | `v05_batch500_0090` | (id-only) |
| duplicate_case_id | `v05_batch500_0091` | `v05_batch500_0091` | (id-only) |
| duplicate_case_id | `v05_batch500_0092` | `v05_batch500_0092` | (id-only) |
| duplicate_case_id | `v05_batch500_0093` | `v05_batch500_0093` | (id-only) |
| duplicate_case_id | `v05_batch500_0094` | `v05_batch500_0094` | (id-only) |
| duplicate_case_id | `v05_batch500_0095` | `v05_batch500_0095` | (id-only) |
| duplicate_case_id | `v05_batch500_0096` | `v05_batch500_0096` | (id-only) |
| duplicate_case_id | `v05_batch500_0097` | `v05_batch500_0097` | (id-only) |
| duplicate_case_id | `v05_batch500_0098` | `v05_batch500_0098` | (id-only) |
| duplicate_case_id | `v05_batch500_0099` | `v05_batch500_0099` | (id-only) |
| duplicate_case_id | `v05_batch500_0100` | `v05_batch500_0100` | (id-only) |
| duplicate_case_id | `v05_batch500_0101` | `v05_batch500_0101` | (id-only) |
| duplicate_case_id | `v05_batch500_0102` | `v05_batch500_0102` | (id-only) |
| duplicate_case_id | `v05_batch500_0103` | `v05_batch500_0103` | (id-only) |
| duplicate_case_id | `v05_batch500_0104` | `v05_batch500_0104` | (id-only) |
| duplicate_case_id | `v05_batch500_0105` | `v05_batch500_0105` | (id-only) |
| duplicate_case_id | `v05_batch500_0106` | `v05_batch500_0106` | (id-only) |
| duplicate_case_id | `v05_batch500_0107` | `v05_batch500_0107` | (id-only) |
| duplicate_case_id | `v05_batch500_0108` | `v05_batch500_0108` | (id-only) |
| duplicate_case_id | `v05_batch500_0109` | `v05_batch500_0109` | (id-only) |
| duplicate_case_id | `v05_batch500_0110` | `v05_batch500_0110` | (id-only) |
| duplicate_case_id | `v05_batch500_0111` | `v05_batch500_0111` | (id-only) |
| duplicate_case_id | `v05_batch500_0112` | `v05_batch500_0112` | (id-only) |
| duplicate_case_id | `v05_batch500_0113` | `v05_batch500_0113` | (id-only) |
| duplicate_case_id | `v05_batch500_0114` | `v05_batch500_0114` | (id-only) |
| duplicate_case_id | `v05_batch500_0115` | `v05_batch500_0115` | (id-only) |
| duplicate_case_id | `v05_batch500_0116` | `v05_batch500_0116` | (id-only) |
| duplicate_case_id | `v05_batch500_0117` | `v05_batch500_0117` | (id-only) |
| duplicate_case_id | `v05_batch500_0118` | `v05_batch500_0118` | (id-only) |
| duplicate_case_id | `v05_batch500_0119` | `v05_batch500_0119` | (id-only) |
| duplicate_case_id | `v05_batch500_0120` | `v05_batch500_0120` | (id-only) |
| duplicate_case_id | `v05_batch500_0121` | `v05_batch500_0121` | (id-only) |
| duplicate_case_id | `v05_batch500_0122` | `v05_batch500_0122` | (id-only) |
| duplicate_case_id | `v05_batch500_0123` | `v05_batch500_0123` | (id-only) |
| duplicate_case_id | `v05_batch500_0124` | `v05_batch500_0124` | (id-only) |
| duplicate_case_id | `v05_batch500_0125` | `v05_batch500_0125` | (id-only) |
| duplicate_case_id | `v05_batch500_0126` | `v05_batch500_0126` | (id-only) |
| duplicate_case_id | `v05_batch500_0127` | `v05_batch500_0127` | (id-only) |
| duplicate_case_id | `v05_batch500_0128` | `v05_batch500_0128` | (id-only) |
| duplicate_case_id | `v05_batch500_0129` | `v05_batch500_0129` | (id-only) |
| duplicate_case_id | `v05_batch500_0130` | `v05_batch500_0130` | (id-only) |
| duplicate_case_id | `v05_batch500_0131` | `v05_batch500_0131` | (id-only) |
| duplicate_case_id | `v05_batch500_0132` | `v05_batch500_0132` | (id-only) |
| duplicate_case_id | `v05_batch500_0133` | `v05_batch500_0133` | (id-only) |
| duplicate_case_id | `v05_batch500_0134` | `v05_batch500_0134` | (id-only) |
| duplicate_case_id | `v05_batch500_0135` | `v05_batch500_0135` | (id-only) |
| duplicate_case_id | `v05_batch500_0136` | `v05_batch500_0136` | (id-only) |
| duplicate_case_id | `v05_batch500_0137` | `v05_batch500_0137` | (id-only) |
| duplicate_case_id | `v05_batch500_0138` | `v05_batch500_0138` | (id-only) |
| duplicate_case_id | `v05_batch500_0139` | `v05_batch500_0139` | (id-only) |
| duplicate_case_id | `v05_batch500_0140` | `v05_batch500_0140` | (id-only) |
| duplicate_case_id | `v05_batch500_0141` | `v05_batch500_0141` | (id-only) |
| duplicate_case_id | `v05_batch500_0142` | `v05_batch500_0142` | (id-only) |
| duplicate_case_id | `v05_batch500_0143` | `v05_batch500_0143` | (id-only) |
| duplicate_case_id | `v05_batch500_0144` | `v05_batch500_0144` | (id-only) |
| duplicate_case_id | `v05_batch500_0145` | `v05_batch500_0145` | (id-only) |
| duplicate_case_id | `v05_batch500_0146` | `v05_batch500_0146` | (id-only) |
| duplicate_case_id | `v05_batch500_0147` | `v05_batch500_0147` | (id-only) |
| duplicate_case_id | `v05_batch500_0148` | `v05_batch500_0148` | (id-only) |
| duplicate_case_id | `v05_batch500_0149` | `v05_batch500_0149` | (id-only) |
| duplicate_case_id | `v05_batch500_0150` | `v05_batch500_0150` | (id-only) |
| duplicate_case_id | `v05_batch500_0151` | `v05_batch500_0151` | (id-only) |
| duplicate_case_id | `v05_batch500_0152` | `v05_batch500_0152` | (id-only) |
| duplicate_case_id | `v05_batch500_0153` | `v05_batch500_0153` | (id-only) |
| duplicate_case_id | `v05_batch500_0154` | `v05_batch500_0154` | (id-only) |
| duplicate_case_id | `v05_batch500_0155` | `v05_batch500_0155` | (id-only) |
| duplicate_case_id | `v05_batch500_0156` | `v05_batch500_0156` | (id-only) |
| duplicate_case_id | `v05_batch500_0157` | `v05_batch500_0157` | (id-only) |
| duplicate_case_id | `v05_batch500_0158` | `v05_batch500_0158` | (id-only) |
| duplicate_case_id | `v05_batch500_0159` | `v05_batch500_0159` | (id-only) |
| duplicate_case_id | `v05_batch500_0160` | `v05_batch500_0160` | (id-only) |
| duplicate_case_id | `v05_batch500_0161` | `v05_batch500_0161` | (id-only) |
| duplicate_case_id | `v05_batch500_0162` | `v05_batch500_0162` | (id-only) |
| duplicate_case_id | `v05_batch500_0163` | `v05_batch500_0163` | (id-only) |
| duplicate_case_id | `v05_batch500_0164` | `v05_batch500_0164` | (id-only) |
| duplicate_case_id | `v05_batch500_0165` | `v05_batch500_0165` | (id-only) |
| duplicate_case_id | `v05_batch500_0166` | `v05_batch500_0166` | (id-only) |
| duplicate_case_id | `v05_batch500_0167` | `v05_batch500_0167` | (id-only) |
| duplicate_case_id | `v05_batch500_0168` | `v05_batch500_0168` | (id-only) |
| duplicate_case_id | `v05_batch500_0169` | `v05_batch500_0169` | (id-only) |
| duplicate_case_id | `v05_batch500_0170` | `v05_batch500_0170` | (id-only) |
| duplicate_case_id | `v05_batch500_0171` | `v05_batch500_0171` | (id-only) |
| duplicate_case_id | `v05_batch500_0172` | `v05_batch500_0172` | (id-only) |
| duplicate_case_id | `v05_batch500_0173` | `v05_batch500_0173` | (id-only) |
| duplicate_case_id | `v05_batch500_0174` | `v05_batch500_0174` | (id-only) |
| duplicate_case_id | `v05_batch500_0175` | `v05_batch500_0175` | (id-only) |
| duplicate_case_id | `v05_batch500_0176` | `v05_batch500_0176` | (id-only) |
| duplicate_case_id | `v05_batch500_0177` | `v05_batch500_0177` | (id-only) |
| duplicate_case_id | `v05_batch500_0178` | `v05_batch500_0178` | (id-only) |
| duplicate_case_id | `v05_batch500_0179` | `v05_batch500_0179` | (id-only) |
| duplicate_case_id | `v05_batch500_0180` | `v05_batch500_0180` | (id-only) |
| duplicate_case_id | `v05_batch500_0181` | `v05_batch500_0181` | (id-only) |
| duplicate_case_id | `v05_batch500_0182` | `v05_batch500_0182` | (id-only) |
| duplicate_case_id | `v05_batch500_0183` | `v05_batch500_0183` | (id-only) |
| duplicate_case_id | `v05_batch500_0184` | `v05_batch500_0184` | (id-only) |
| duplicate_case_id | `v05_batch500_0185` | `v05_batch500_0185` | (id-only) |
| duplicate_case_id | `v05_batch500_0186` | `v05_batch500_0186` | (id-only) |
| duplicate_case_id | `v05_batch500_0187` | `v05_batch500_0187` | (id-only) |
| duplicate_case_id | `v05_batch500_0188` | `v05_batch500_0188` | (id-only) |
| duplicate_case_id | `v05_batch500_0189` | `v05_batch500_0189` | (id-only) |
| duplicate_case_id | `v05_batch500_0190` | `v05_batch500_0190` | (id-only) |
| duplicate_case_id | `v05_batch500_0191` | `v05_batch500_0191` | (id-only) |
| duplicate_case_id | `v05_batch500_0192` | `v05_batch500_0192` | (id-only) |
| duplicate_case_id | `v05_batch500_0193` | `v05_batch500_0193` | (id-only) |
| duplicate_case_id | `v05_batch500_0194` | `v05_batch500_0194` | (id-only) |
| duplicate_case_id | `v05_batch500_0195` | `v05_batch500_0195` | (id-only) |
| duplicate_case_id | `v05_batch500_0196` | `v05_batch500_0196` | (id-only) |
| duplicate_case_id | `v05_batch500_0197` | `v05_batch500_0197` | (id-only) |
| duplicate_case_id | `v05_batch500_0198` | `v05_batch500_0198` | (id-only) |
| duplicate_case_id | `v05_batch500_0199` | `v05_batch500_0199` | (id-only) |
| duplicate_case_id | `v05_batch500_0200` | `v05_batch500_0200` | (id-only) |
| duplicate_case_id | `v05_batch50_0001` | `v05_batch50_0001` | (id-only) |
| duplicate_case_id | `v05_batch50_0002` | `v05_batch50_0002` | (id-only) |
| duplicate_case_id | `v05_batch50_0003` | `v05_batch50_0003` | (id-only) |
| duplicate_case_id | `v05_batch50_0004` | `v05_batch50_0004` | (id-only) |
| duplicate_case_id | `v05_batch50_0005` | `v05_batch50_0005` | (id-only) |
| duplicate_case_id | `v05_batch50_0006` | `v05_batch50_0006` | (id-only) |
| duplicate_case_id | `v05_batch50_0007` | `v05_batch50_0007` | (id-only) |
| duplicate_case_id | `v05_batch50_0008` | `v05_batch50_0008` | (id-only) |
| duplicate_case_id | `v05_batch50_0009` | `v05_batch50_0009` | (id-only) |
| duplicate_case_id | `v05_batch50_0010` | `v05_batch50_0010` | (id-only) |
| duplicate_case_id | `v05_batch50_0011` | `v05_batch50_0011` | (id-only) |
| duplicate_case_id | `v05_batch50_0012` | `v05_batch50_0012` | (id-only) |
| duplicate_case_id | `v05_batch50_0013` | `v05_batch50_0013` | (id-only) |
| duplicate_case_id | `v05_batch50_0014` | `v05_batch50_0014` | (id-only) |
| duplicate_case_id | `v05_batch50_0015` | `v05_batch50_0015` | (id-only) |
| duplicate_case_id | `v05_batch50_0016` | `v05_batch50_0016` | (id-only) |
| duplicate_case_id | `v05_batch50_0017` | `v05_batch50_0017` | (id-only) |
| duplicate_case_id | `v05_batch50_0018` | `v05_batch50_0018` | (id-only) |
| duplicate_case_id | `v05_batch50_0019` | `v05_batch50_0019` | (id-only) |
| duplicate_case_id | `v05_batch50_0020` | `v05_batch50_0020` | (id-only) |
| duplicate_case_id | `v05_batch50_0021` | `v05_batch50_0021` | (id-only) |
| duplicate_case_id | `v05_batch50_0022` | `v05_batch50_0022` | (id-only) |
| duplicate_case_id | `v05_batch50_0023` | `v05_batch50_0023` | (id-only) |
| duplicate_case_id | `v05_batch50_0024` | `v05_batch50_0024` | (id-only) |
| duplicate_case_id | `v05_batch50_0025` | `v05_batch50_0025` | (id-only) |
| duplicate_case_id | `v05_batch50_0026` | `v05_batch50_0026` | (id-only) |
| duplicate_case_id | `v05_batch50_0027` | `v05_batch50_0027` | (id-only) |
| duplicate_case_id | `v05_batch50_0028` | `v05_batch50_0028` | (id-only) |
| duplicate_case_id | `v05_batch50_0029` | `v05_batch50_0029` | (id-only) |
| duplicate_case_id | `v05_batch50_0030` | `v05_batch50_0030` | (id-only) |
| duplicate_case_id | `v05_sample_0001` | `v05_sample_0001` | (id-only) |
| duplicate_case_id | `v05_sample_0002` | `v05_sample_0002` | (id-only) |
| duplicate_case_id | `v05_sample_0003` | `v05_sample_0003` | (id-only) |
| duplicate_case_id | `v05_sample_0004` | `v05_sample_0004` | (id-only) |
| duplicate_case_id | `v05_sample_0005` | `v05_sample_0005` | (id-only) |
| duplicate_case_id | `v05_sample_0006` | `v05_sample_0006` | (id-only) |
| duplicate_case_id | `v05_sample_0007` | `v05_sample_0007` | (id-only) |
| duplicate_case_id | `v05_sample_0008` | `v05_sample_0008` | (id-only) |
| duplicate_case_id | `v05_sample_0009` | `v05_sample_0009` | (id-only) |
| duplicate_case_id | `v05_sample_0010` | `v05_sample_0010` | (id-only) |
| duplicate_case_id | `v05_sample_0011` | `v05_sample_0011` | (id-only) |
| duplicate_case_id | `v05_sample_0012` | `v05_sample_0012` | (id-only) |
| duplicate_case_id | `v05_sample_0013` | `v05_sample_0013` | (id-only) |
| duplicate_case_id | `v05_sample_0015` | `v05_sample_0015` | (id-only) |
| duplicate_case_id | `v05_sample_0016` | `v05_sample_0016` | (id-only) |
| duplicate_case_id | `v05_sample_0017` | `v05_sample_0017` | (id-only) |
| duplicate_case_id | `v05_sample_0018` | `v05_sample_0018` | (id-only) |
| duplicate_case_id | `v05_sample_0019` | `v05_sample_0019` | (id-only) |
| duplicate_case_id | `v05_sample_0020` | `v05_sample_0020` | (id-only) |
| duplicate_case_id | `v05_sample_0021` | `v05_sample_0021` | (id-only) |
| exact unit_text overlap | `v05_sample_0001` | `v05_sample_0001` | The parser should refuse to accept fact as a valid STORE target. |
| exact unit_text overlap | `v05_sample_0002` | `v05_sample_0002` | Does the current sync retry respect the upload timeout setting, or does it use a hardcoded 30s? |
| exact unit_text overlap | `v05_sample_0003` | `v05_sample_0003` | Please check today's weather before running the export validation. |
| exact unit_text overlap | `v05_sample_0004` | `v05_sample_0004` | The eval_runner computes READ F1, STORE unit F1, STORE target accuracy, SKIP F1, false store rate, a |
| exact unit_text overlap | `v05_sample_0004` | `v05_sample_0004` | The eval_runner has been run on subset50 but not yet on full pilot. |
| exact unit_text overlap | `v05_sample_0004` | `v05_sample_0004` | Maybe the eval_runner should also report confidence scores. |
| exact unit_text overlap | `v05_sample_0005` | `v05_sample_0005` | Parser tests should live under tests/v04/ and run with pytest tests/v04/. |
| exact unit_text overlap | `v05_sample_0005` | `v05_sample_0005` | The parser converts Unit DSL to canonical JSON without guessing targets. |
| exact unit_text overlap | `v05_sample_0005` | `v05_sample_0005` | Remember my personal backup email: abc16-backup@example.com. |
| exact unit_text overlap | `v05_sample_0006` | `v05_sample_0006` | The data-platform pilot uses synthetic service scenarios only; no real production data. |
| exact unit_text overlap | `v05_sample_0006` | `v05_sample_0006` | Next, add a retry wrapper for the pipeline job that fails on transient network errors. |
| exact unit_text overlap | `v05_sample_0006` | `v05_sample_0006` | Today's lunch order will be from the Thai place. |
| exact unit_text overlap | `v05_sample_0007` | `v05_sample_0007` | I prefer architecture explanations that name tradeoffs explicitly. |
| exact unit_text overlap | `v05_sample_0007` | `v05_sample_0007` | Enable HDR mode by default for all future camera captures in this app. |
| exact unit_text overlap | `v05_sample_0007` | `v05_sample_0007` | My phone number is 555-0198, use it for the test account. |
| exact unit_text overlap | `v05_sample_0008` | `v05_sample_0008` | The case validator checks that gold.dsl parses consistently with gold.read, gold.store, and gold.ski |
| exact unit_text overlap | `v05_sample_0008` | `v05_sample_0008` | The case validator source lives under src/v04/case_validator.py. |
| exact unit_text overlap | `v05_sample_0008` | `v05_sample_0008` | Add a sixth target called team_memory for team-level conventions. |
| exact unit_text overlap | `v05_sample_0009` | `v05_sample_0009` | The eval_runner must now also report per-tag accuracy breakdowns in addition to aggregate metrics. |
| exact unit_text overlap | `v05_sample_0009` | `v05_sample_0009` | The eval_runner still evaluates only single-turn cases, not multi-turn sessions. |
| exact unit_text overlap | `v05_sample_0009` | `v05_sample_0009` | Add the per-tag report section to reports/v04/interface_pilot_report.md template. |
| exact unit_text overlap | `v05_sample_0010` | `v05_sample_0010` | Sync error handling should be updated to retry on 429 rate-limit responses with a 60s delay. |
| exact unit_text overlap | `v05_sample_0010` | `v05_sample_0010` | Run the sync integration tests after the change and report results. |
| exact unit_text overlap | `v05_sample_0010` | `v05_sample_0010` | My test account password is testpass_1234_do_not_store. |
| exact unit_text overlap | `v05_sample_0011` | `v05_sample_0011` | The prompt builder must always include the five legal STORE targets in the system instruction. |
| exact unit_text overlap | `v05_sample_0011` | `v05_sample_0011` | Add a few-shot example section to the prompt builder output format. |
| exact unit_text overlap | `v05_sample_0011` | `v05_sample_0011` | I like concise prompts with examples before rules when learning new APIs. |
| exact unit_text overlap | `v05_sample_0012` | `v05_sample_0012` | Add a SHA-256 checksum validation step that runs after the S3 write and logs the result. |
| exact unit_text overlap | `v05_sample_0012` | `v05_sample_0012` | The export job is blocked until the IAM role is updated with the new S3 permissions. |
| exact unit_text overlap | `v05_sample_0013` | `v05_sample_0013` | The parser should now also reject STORE lines where the target is valid but the unit_id has already  |
| exact unit_text overlap | `v05_sample_0013` | `v05_sample_0013` | Write parser tests for the new duplicate assignment across STORE/SKIP check. |
| exact unit_text overlap | `v05_sample_0013` | `v05_sample_0013` | This parser change is small and should take about 30 minutes. |
| exact unit_text overlap | `v05_sample_0021` | `v05_sample_0021` | The notification service must deduplicate messages by notification_id within a 5-minute window to pr |
| exact unit_text overlap | `v05_sample_0021` | `v05_sample_0021` | Integrate the notification retry into the existing sync retry wrapper that already handles 429 respo |
| exact unit_text overlap | `v05_sample_0021` | `v05_sample_0021` | Write the FCM credential setup guide in docs/notification/fcm_setup.md. |
| exact unit_text overlap | `v05_sample_0015` | `v05_sample_0015` | v0.5 training documentation should go under docs/v05/ with training plan, data plan, and SFT format. |
| exact unit_text overlap | `v05_sample_0015` | `v05_sample_0015` | The project does not implement a full MemoryOS; it only studies the memory policy router layer. |
| exact unit_text overlap | `v05_sample_0015` | `v05_sample_0015` | Write the v0.5 training plan as a markdown file today. |
| exact unit_text overlap | `v05_sample_0016` | `v05_sample_0016` | Set the default flash mode to auto for the camera module in this app. |
| exact unit_text overlap | `v05_sample_0016` | `v05_sample_0016` | The user has informed us that their recovery code for the field-app account is ABCD-1234-EFGH. |
| exact unit_text overlap | `v05_sample_0017` | `v05_sample_0017` | The pipeline should also publish failure events with stack traces to the monitoring queue. |
| exact unit_text overlap | `v05_sample_0017` | `v05_sample_0017` | The monitoring queue message schema is defined in docs/pipeline/monitoring_schema.md. |
| exact unit_text overlap | `v05_sample_0017` | `v05_sample_0017` | Add a Slack alert for pipeline failures that happen during off-hours. |
| exact unit_text overlap | `v05_sample_0018` | `v05_sample_0018` | Use LoRA with rank 8 on Qwen3-4B for the v0.5 SFT training run. |
| exact unit_text overlap | `v05_sample_0018` | `v05_sample_0018` | Training should optimize for routing metrics, not just cross-entropy loss. |
| exact unit_text overlap | `v05_sample_0018` | `v05_sample_0018` | Start training tomorrow morning once the data is ready. |
| exact unit_text overlap | `v05_sample_0019` | `v05_sample_0019` | Add a manual purge button that clears all pending offline edits older than 7 days. |
| exact unit_text overlap | `v05_sample_0019` | `v05_sample_0019` | The user has requested that we store their location history for personalized recommendations. |
| exact unit_text overlap | `v05_sample_0019` | `v05_sample_0019` | The purge feature should log how many entries were removed and their total size. |
| exact unit_text overlap | `v05_sample_0020` | `v05_sample_0020` | The export retry logic must use idempotency keys to prevent duplicate invoice uploads when S3 writes |
| exact unit_text overlap | `v05_sample_0020` | `v05_sample_0020` | Store the idempotency key schema in docs/export/idempotency.md. |
| exact unit_text overlap | `v05_sample_0020` | `v05_sample_0020` | My company laptop runs Ubuntu 24.04 and I use it for all development work. |
| exact unit_text overlap | `v05_batch50_0001` | `v05_batch50_0001` | What time does the pipeline run on weekends? |
| exact unit_text overlap | `v05_batch50_0002` | `v05_batch50_0002` | The camera crashes on startup on Android 14 devices, show me the initialization code. |
| exact unit_text overlap | `v05_batch50_0003` | `v05_batch50_0003` | What checks does the case validator perform on gold data? |
| exact unit_text overlap | `v05_batch50_0004` | `v05_batch50_0004` | Why is invoice INV-2026-0582 missing from the S3 bucket? |
| exact unit_text overlap | `v05_batch50_0005` | `v05_batch50_0005` | How many pending entries trigger the warning banner? |
| exact unit_text overlap | `v05_batch50_0006` | `v05_batch50_0006` | The pipeline must reject any batch where the row count deviates by more than 10% from the 7-day aver |
| exact unit_text overlap | `v05_batch50_0006` | `v05_batch50_0006` | Implement the row-count check in the validation stage before the transform stage. |
| exact unit_text overlap | `v05_batch50_0006` | `v05_batch50_0006` | The 7-day average is calculated from the pipeline_metrics table in the analytics DB. |
| exact unit_text overlap | `v05_batch50_0007` | `v05_batch50_0007` | The eval_runner must support side-by-side comparison of multiple interfaces in a single run. |
| exact unit_text overlap | `v05_batch50_0007` | `v05_batch50_0007` | Add a bar chart output mode to the eval_runner for visualizing per-interface metrics. |
| exact unit_text overlap | `v05_batch50_0007` | `v05_batch50_0007` | The v0.5 training targets Qwen3-4B with LoRA, not full fine-tuning. |
| exact unit_text overlap | `v05_batch50_0008` | `v05_batch50_0008` | Camera permission requests must show a rationale dialog before the system permission prompt on Andro |
| exact unit_text overlap | `v05_batch50_0008` | `v05_batch50_0008` | The camera module permission code lives under app/src/main/java/com/fieldapp/camera/permissions/. |
| exact unit_text overlap | `v05_batch50_0008` | `v05_batch50_0008` | My personal Google account for app testing is devtest123@gmail.com. |
| exact unit_text overlap | `v05_batch500_0096` | `v05_batch50_0009` | The project scope explicitly excludes retriever training, writer training, and MemoryOS implementati |
| exact unit_text overlap | `v05_batch50_0009` | `v05_batch50_0009` | v0.5 training documentation lives under docs/v05/ with separate plan, data, and format docs. |
| exact unit_text overlap | `v05_batch50_0009` | `v05_batch50_0009` | I prefer documentation that shows examples before abstract definitions. |
| exact unit_text overlap | `v05_batch50_0010` | `v05_batch50_0010` | The export job must use server-side encryption with KMS key arn:aws:kms:us-east-1:123456789:key/expo |
| exact unit_text overlap | `v05_batch50_0010` | `v05_batch50_0010` | The KMS key policy is defined in terraform/modules/export/kms.tf. |
| exact unit_text overlap | `v05_batch50_0010` | `v05_batch50_0010` | My AWS access key for the test account is AKIA1234567890ABCDEF — use it for testing. |
| exact unit_text overlap | `v05_batch50_0011` | `v05_batch50_0011` | The parser must never guess or infer missing STORE targets from unit text. |
| exact unit_text overlap | `v05_batch50_0011` | `v05_batch50_0011` | The parser currently rejects duplicate STORE lines but does not yet reject STORE/SKIP conflicts. |
| exact unit_text overlap | `v05_batch50_0011` | `v05_batch50_0011` | Parser source lives under src/v04/parser.py and uses strict line-by-line parsing. |
| exact unit_text overlap | `v05_batch50_0012` | `v05_batch50_0012` | All sync integration tests must run with a local SQLite database, never against the production sync  |
| exact unit_text overlap | `v05_batch50_0012` | `v05_batch50_0012` | Sync integration tests live under tests/integration/sync/ and use pytest with the sync_test fixture. |
| exact unit_text overlap | `v05_batch50_0012` | `v05_batch50_0012` | Remind me to check the CI pipeline logs after this. |
| exact unit_text overlap | `v05_batch50_0013` | `v05_batch50_0013` | Add a deadlock retry wrapper that catches PostgreSQL error code 40P01 and retries up to 3 times with |
| exact unit_text overlap | `v05_batch50_0013` | `v05_batch50_0013` | The retry wrapper should log each deadlock occurrence to the pipeline_errors table with the failed q |
| exact unit_text overlap | `v05_batch50_0013` | `v05_batch50_0013` | Test the deadlock retry on the staging pipeline before deploying to production. |
| exact unit_text overlap | `v05_batch50_0014` | `v05_batch50_0014` | Notifications with priority CRITICAL must bypass the silent-hours filter and always trigger an alert |
| exact unit_text overlap | `v05_batch50_0014` | `v05_batch50_0014` | The user's home address for field-app deliveries is 1234 Rural Route 7. |
| exact unit_text overlap | `v05_batch50_0014` | `v05_batch50_0014` | Add a priority field to the notification payload schema in the API docs. |
| exact unit_text overlap | `v05_batch50_0015` | `v05_batch50_0015` | The prompt builder must now also accept an optional few-shot example section to prepend before the c |
| exact unit_text overlap | `v05_batch50_0015` | `v05_batch50_0015` | Write unit tests for the new few-shot section rendering. |
| exact unit_text overlap | `v05_batch50_0016` | `v05_batch50_0016` | Add Parquet as an optional output format alongside CSV. The format selection should be per-export-ru |
| exact unit_text overlap | `v05_batch50_0016` | `v05_batch50_0016` | Update the billing report generator to also accept Parquet input before enabling the new format in p |
| exact unit_text overlap | `v05_batch50_0016` | `v05_batch50_0016` | My Stripe API test key for the sandbox is sk_test_1234567890abcdef. |
| exact unit_text overlap | `v05_batch50_0017` | `v05_batch50_0017` | The training split should be 800 train / 100 dev / 100 gold, with gold locked immediately after crea |
| exact unit_text overlap | `v05_batch50_0017` | `v05_batch50_0017` | The project will only ever use synthetic training data; real production data is permanently out of s |
| exact unit_text overlap | `v05_batch50_0017` | `v05_batch50_0017` | Draft the data split plan section in the training plan doc today. |
| exact unit_text overlap | `v05_batch50_0018` | `v05_batch50_0018` | Reduce the frame timeout from 200ms to 120ms and measure the impact on capture success rate. |
| exact unit_text overlap | `v05_batch50_0018` | `v05_batch50_0018` | If capture latency remains above 300ms after the timeout change, profile the HDR pipeline next. |
| exact unit_text overlap | `v05_batch50_0019` | `v05_batch50_0019` | The dependency graph should be documented in docs/pipeline/dependency_graph.md with each stage's inp |
| exact unit_text overlap | `v05_batch50_0019` | `v05_batch50_0019` | Run the DAG visualization script after updating the dependency docs. |
| exact unit_text overlap | `v05_batch50_0020` | `v05_batch50_0020` | The case validator should now also check that no sample case duplicates exact text from subset50 or  |
| exact unit_text overlap | `v05_batch50_0020` | `v05_batch50_0020` | Add the leakage check function to the case validator before the batch50 validation run. |
| exact unit_text overlap | `v05_batch50_0020` | `v05_batch50_0020` | This leakage check is probably a one-time validation; we do not need to keep it permanently. |
| exact unit_text overlap | `v05_batch50_0021` | `v05_batch50_0021` | Add a three-way merge strategy as an alternative to last-write-wins, selectable per collection. |
| exact unit_text overlap | `v05_batch50_0021` | `v05_batch50_0021` | The three-way merge should use the server version as the common ancestor when available. |
| exact unit_text overlap | `v05_batch50_0022` | `v05_batch50_0022` | Add a per-table freshness metric that alerts when any table exceeds the 4-hour SLA. |
| exact unit_text overlap | `v05_batch50_0022` | `v05_batch50_0022` | The freshness alert should fire to the #data-alerts Slack channel with the table name and hours stal |
| exact unit_text overlap | `v05_batch50_0022` | `v05_batch50_0022` | Deploy the new metric to the staging Grafana instance first, then promote to production. |
| exact unit_text overlap | `v05_batch50_0023` | `v05_batch50_0023` | The metrics module must report a calibration score comparing predicted vs gold target distributions  |
| exact unit_text overlap | `v05_batch50_0023` | `v05_batch50_0023` | Implement the calibration metric as a new function in src/v04/metrics.py alongside the existing F1 f |
| exact unit_text overlap | `v05_batch50_0023` | `v05_batch50_0023` | The current metrics module only reports per-interface accuracy, not cross-target calibration. |
| exact unit_text overlap | `v05_batch50_0024` | `v05_batch50_0024` | The export service must never log or store raw invoice line items that contain customer PII. |
| exact unit_text overlap | `v05_batch50_0024` | `v05_batch50_0024` | All data-platform services must use the centralized secret manager for API keys and credentials. |
| exact unit_text overlap | `v05_batch50_0024` | `v05_batch50_0024` | Add PII masking to the export debug logs before the next production deployment. |
| exact unit_text overlap | `v05_batch50_0025` | `v05_batch50_0025` | I prefer that the camera app always opens in photo mode, not video mode. |
| exact unit_text overlap | `v05_batch50_0025` | `v05_batch50_0025` | For this repo, always run the camera integration tests with the --device emulator flag. |
| exact unit_text overlap | `v05_batch50_0025` | `v05_batch50_0025` | My device unlock PIN for testing is 123456. |
| exact unit_text overlap | `v05_batch50_0026` | `v05_batch50_0026` | All v0.5 training runs must use the project-local Python virtual environment under .venv/ with pinne |
| exact unit_text overlap | `v05_batch50_0026` | `v05_batch50_0026` | Use the RTX 4070 SUPER GPU for training with batch size 4 to fit within 12GB VRAM. |
| exact unit_text overlap | `v05_batch50_0026` | `v05_batch50_0026` | If training loss does not decrease within 50 steps, stop and investigate the data pipeline. |
| exact unit_text overlap | `v05_batch50_0027` | `v05_batch50_0027` | Add a dead-letter queue for pipeline stages that fail after 3 retries. Failed records go to the DLQ  |
| exact unit_text overlap | `v05_batch50_0027` | `v05_batch50_0027` | Remember to delete the old error queue after the DLQ is live for one week. |
| exact unit_text overlap | `v05_batch50_0027` | `v05_batch50_0027` | My team's Slack webhook URL for pipeline alerts is https://hooks.slack.com/services/TEST/FAKE/abcdef |
| exact unit_text overlap | `v05_batch50_0028` | `v05_batch50_0028` | Change the sync interval from fixed 15 minutes to adaptive: 5 minutes on Wi-Fi, 30 minutes on cellul |
| exact unit_text overlap | `v05_batch50_0028` | `v05_batch50_0028` | Add a network-type constraint to the WorkManager policy so it switches intervals automatically. |
| exact unit_text overlap | `v05_batch50_0029` | `v05_batch50_0029` | For v0.5 evaluation, prioritize STORE target accuracy and false store rate over exact match rate. |
| exact unit_text overlap | `v05_batch50_0029` | `v05_batch50_0029` | The project's evaluation standard emphasizes routing-specific metrics, not just output formatting. |
| exact unit_text overlap | `v05_batch50_0029` | `v05_batch50_0029` | Write the evaluation priorities section in the training plan today. |
| exact unit_text overlap | `v05_batch50_0030` | `v05_batch50_0030` | Add incremental load support using a high-watermark column updated_at. The pipeline should only proc |
| exact unit_text overlap | `v05_batch50_0030` | `v05_batch50_0030` | The incremental load feature must support a full-refresh fallback when the high-watermark is detecte |
| exact unit_text overlap | `v05_batch50_0030` | `v05_batch50_0030` | The high-watermark values should be persisted in the pipeline_metadata table, not in memory. |
| exact unit_text overlap | `v05_batch100_0001` | `v05_batch100_0001` | Why are search queries taking over 2 seconds on the staging environment? |
| exact unit_text overlap | `v05_batch100_0002` | `v05_batch100_0002` | Does the aggregation window include transactions that happened exactly at midnight UTC? |
| exact unit_text overlap | `v05_batch100_0003` | `v05_batch100_0003` | What is the cache TTL for the LAX-JFK route? |
| exact unit_text overlap | `v05_batch100_0004` | `v05_batch100_0004` | Show me the current ranking weights configuration. |
| exact unit_text overlap | `v05_batch100_0005` | `v05_batch100_0005` | The revenue chart shows zero for today — is this an aggregator issue or a visualizer bug? |
| exact unit_text overlap | `v05_batch100_0006` | `v05_batch100_0006` | Which template ID does the booking confirmation use? |
| exact unit_text overlap | `v05_batch100_0007` | `v05_batch100_0007` | A student's calculated grade shows 85% but I expected 78%. What weights are being used? |
| exact unit_text overlap | `v05_batch100_0008` | `v05_batch100_0008` | How long does it take to build all character textures for the latest release branch? |
| exact unit_text overlap | `v05_batch100_0009` | `v05_batch100_0009` | What is the maximum sentence count for summaries? |
| exact unit_text overlap | `v05_batch100_0010` | `v05_batch100_0010` | At what threshold does the CFO get automatically notified? |
| exact unit_text overlap | `v05_batch100_0011` | `v05_batch100_0011` | The indexer must complete a full reindex within 10 minutes for repositories under 5000 documents. |
| exact unit_text overlap | `v05_batch100_0011` | `v05_batch100_0011` | The docs-assistant project scope does not include real-time collaboration features. |
| exact unit_text overlap | `v05_batch100_0011` | `v05_batch100_0011` | Run the reindex benchmark after the next configuration change. |
| exact unit_text overlap | `v05_batch100_0012` | `v05_batch100_0012` | The aggregator must reject any input row where the transaction amount is negative and not flagged as |
| exact unit_text overlap | `v05_batch100_0012` | `v05_batch100_0012` | The aggregator currently processes data in hourly batches but does not yet handle late-arriving data |
| exact unit_text overlap | `v05_batch100_0012` | `v05_batch100_0012` | The finance-dashboard project must comply with SOC 2 data integrity requirements for all financial r |
| exact unit_text overlap | `v05_batch100_0013` | `v05_batch100_0013` | The pricing cache must be invalidated within 60 seconds of any fare rule update from the airline API |
| exact unit_text overlap | `v05_batch100_0013` | `v05_batch100_0013` | The cache invalidation logic lives in src/pricing/cache_invalidator.py and uses Redis pub/sub. |
| exact unit_text overlap | `v05_batch100_0013` | `v05_batch100_0013` | I prefer flight search results sorted by total price including taxes, not base fare. |
| exact unit_text overlap | `v05_batch100_0014` | `v05_batch100_0014` | I prefer search results to be grouped by document section, not just ranked by relevance score. |
| exact unit_text overlap | `v05_batch100_0014` | `v05_batch100_0014` | The search service should always exclude archived documents from results unless the user explicitly  |
| exact unit_text overlap | `v05_batch100_0014` | `v05_batch100_0014` | My personal API token for the docs-bot admin panel is dba-token-xxxxxxxxxxxx. |
| exact unit_text overlap | `v05_batch100_0015` | `v05_batch100_0015` | All finboard services must use TLS 1.3 for inter-service communication. |
| exact unit_text overlap | `v05_batch100_0015` | `v05_batch100_0015` | The visualizer service must render all currency values with the ISO 4217 currency code suffix. |
| exact unit_text overlap | `v05_batch100_0015` | `v05_batch100_0015` | Update the visualizer to use the new currency formatting library. |
| exact unit_text overlap | `v05_batch100_0016` | `v05_batch100_0016` | The booking service must use idempotency keys for all payment attempts to prevent double-charging. |
| exact unit_text overlap | `v05_batch100_0016` | `v05_batch100_0016` | Booking-related database migrations live under db/migrations/booking/ and must be reviewed before ap |
| exact unit_text overlap | `v05_batch100_0016` | `v05_batch100_0016` | My test credit card number for the staging environment is 4111-1111-1111-1111. |
| exact unit_text overlap | `v05_batch100_0017` | `v05_batch100_0017` | Late submissions are penalized 10% per day up to a maximum of 5 days, after which the submission rec |
| exact unit_text overlap | `v05_batch100_0017` | `v05_batch100_0017` | The learnhub project does not implement proctoring or identity verification. |
| exact unit_text overlap | `v05_batch100_0017` | `v05_batch100_0017` | Add the late penalty calculation to the grading service before the fall semester starts. |
| exact unit_text overlap | `v05_batch100_0018` | `v05_batch100_0018` | The asset pipeline must reject any texture that exceeds 4096x4096 pixels for mobile target platforms |
| exact unit_text overlap | `v05_batch100_0018` | `v05_batch100_0018` | Asset validation rules are defined in config/asset_pipeline/validation_rules.json. |
| exact unit_text overlap | `v05_batch100_0018` | `v05_batch100_0018` | Run the full asset validation suite before the next release build. |
| exact unit_text overlap | `v05_batch100_0019` | `v05_batch100_0019` | The summarizer must never include code blocks in summaries — code should be referenced by file path  |
| exact unit_text overlap | `v05_batch100_0019` | `v05_batch100_0019` | Summaries should be cached with the document version hash as the cache key. |
| exact unit_text overlap | `v05_batch100_0019` | `v05_batch100_0019` | The docs-assistant project decided to use OpenAI-compatible APIs only, not vendor-specific SDKs. |
| exact unit_text overlap | `v05_batch100_0020` | `v05_batch100_0020` | Revenue alerts above warning level go to #fin-alerts Slack channel; critical alerts also trigger Pag |
| exact unit_text overlap | `v05_batch100_0020` | `v05_batch100_0020` | The alerts service routing configuration is in config/alerts/routing.yaml with per-severity channel  |
| exact unit_text overlap | `v05_batch100_0020` | `v05_batch100_0020` | Add a weekly alert summary email to the CFO every Monday at 08:00. |
| exact unit_text overlap | `v05_batch100_0021` | `v05_batch100_0021` | The pricing service must include all mandatory taxes and fees in the displayed price, not just the b |
| exact unit_text overlap | `v05_batch100_0021` | `v05_batch100_0021` | The pricing service currently sources fares from 3 airline APIs but the fourth (SkyConnect) is still |
| exact unit_text overlap | `v05_batch100_0021` | `v05_batch100_0021` | All voyager services must log pricing decisions for audit purposes with a retention period of 7 year |
| exact unit_text overlap | `v05_batch100_0022` | `v05_batch100_0022` | The enrollment service must check prerequisites before allowing a student to enroll in any course. |
| exact unit_text overlap | `v05_batch100_0022` | `v05_batch100_0022` | Prerequisite data is stored in the courses table with a JSON array column named prerequisites. |
| exact unit_text overlap | `v05_batch100_0022` | `v05_batch100_0022` | I prefer course materials organized by week with clear learning objectives at the top of each module |
| exact unit_text overlap | `v05_batch100_0023` | `v05_batch100_0023` | All game builds must pass the asset validation suite before the build is considered complete. |
| exact unit_text overlap | `v05_batch100_0023` | `v05_batch100_0023` | Build artifacts are stored under builds/YYYY-MM-DD/ with a manifest.json listing all included assets |
| exact unit_text overlap | `v05_batch100_0023` | `v05_batch100_0023` | Remember to clean the build cache before the next release candidate. |
| exact unit_text overlap | `v05_batch100_0024` | `v05_batch100_0024` | The indexer stores its inverted index in Redis with keys prefixed by idx:v2: for the current schema  |
| exact unit_text overlap | `v05_batch100_0024` | `v05_batch100_0024` | Redis connection parameters are configured via environment variables REDIS_HOST and REDIS_PORT. |
| exact unit_text overlap | `v05_batch100_0024` | `v05_batch100_0024` | The docs-assistant project only supports English-language documentation in the current scope. |
| exact unit_text overlap | `v05_batch100_0025` | `v05_batch100_0025` | The aggregator must never modify raw transaction data — all transformations must happen in derived t |
| exact unit_text overlap | `v05_batch100_0025` | `v05_batch100_0025` | Run the data pipeline integration test suite before merging any aggregator changes. |
| exact unit_text overlap | `v05_batch100_0025` | `v05_batch100_0025` | My personal database password for the staging environment is finboard_stage_2026. |
| exact unit_text overlap | `v05_batch100_0026` | `v05_batch100_0026` | Add semantic search using sentence-transformers to augment the existing TF-IDF results with a hybrid |
| exact unit_text overlap | `v05_batch100_0026` | `v05_batch100_0026` | The hybrid ranking should weight semantic similarity at 0.4 and TF-IDF at 0.6 for the initial rollou |
| exact unit_text overlap | `v05_batch100_0026` | `v05_batch100_0026` | Benchmark the hybrid search against TF-IDF-only on the standard query test set before deploying. |
| exact unit_text overlap | `v05_batch100_0027` | `v05_batch100_0027` | Add a PDF export button that renders the current dashboard view using headless Chromium. |
| exact unit_text overlap | `v05_batch100_0027` | `v05_batch100_0027` | PDF exports must include the report timestamp and user ID in the page footer as required by the proj |
| exact unit_text overlap | `v05_batch100_0027` | `v05_batch100_0027` | Test the PDF export on the staging environment with the CFO's dashboard configuration. |
| exact unit_text overlap | `v05_batch100_0028` | `v05_batch100_0028` | Add multi-city booking that allows up to 5 segments in a single booking, with each segment priced in |
| exact unit_text overlap | `v05_batch100_0028` | `v05_batch100_0028` | The multi-city flow must batch pricing requests to stay under the rate limit — group segments by des |
| exact unit_text overlap | `v05_batch100_0028` | `v05_batch100_0028` | My frequent flyer number for test bookings is FF-TEST-123456. |
| exact unit_text overlap | `v05_batch100_0029` | `v05_batch100_0029` | Add rubric-based grading as an alternative to points-based. Each rubric criterion has a max score an |
| exact unit_text overlap | `v05_batch100_0029` | `v05_batch100_0029` | The rubric definitions should be stored in the course configuration, not hardcoded in the grading se |
| exact unit_text overlap | `v05_batch100_0029` | `v05_batch100_0029` | I prefer grade reports that show a breakdown by rubric criterion with comments from the instructor. |
| exact unit_text overlap | `v05_batch100_0030` | `v05_batch100_0030` | Add automatic texture atlas generation that packs textures into power-of-two atlases using the max-r |
| exact unit_text overlap | `v05_batch100_0030` | `v05_batch100_0030` | The atlas generator should log a warning when texture utilization drops below 70% of the atlas area. |
| exact unit_text overlap | `v05_batch100_0030` | `v05_batch100_0030` | Update the game engine client to load textures from the atlas instead of individual files. |
| exact unit_text overlap | `v05_batch100_0031` | `v05_batch100_0031` | Add a relevance feedback loop that boosts documents users clicked for the same query in future searc |
| exact unit_text overlap | `v05_batch100_0031` | `v05_batch100_0031` | The feedback boost should decay over 30 days to prevent stale relevance signals from persisting inde |
| exact unit_text overlap | `v05_batch100_0032` | `v05_batch100_0032` | Add anomaly detection using a rolling z-score with a window of 30 days and a threshold of 3 standard |
| exact unit_text overlap | `v05_batch100_0032` | `v05_batch100_0032` | Anomaly alerts should include the z-score value and the 30-day mean for context in the notification. |
| exact unit_text overlap | `v05_batch100_0032` | `v05_batch100_0032` | I prefer financial alerts grouped by business unit rather than by metric type. |
| exact unit_text overlap | `v05_batch100_0033` | `v05_batch100_0033` | Add demand-based surge pricing that increases fares by up to 40% when seat availability drops below  |
| exact unit_text overlap | `v05_batch100_0033` | `v05_batch100_0033` | All surge-priced fares must still display the base fare and the surge component separately to comply |
| exact unit_text overlap | `v05_batch100_0034` | `v05_batch100_0034` | Add a waitlist that automatically enrolls the next student when someone drops, up to 7 days before t |
| exact unit_text overlap | `v05_batch100_0034` | `v05_batch100_0034` | The waitlist should send an email notification to the student when they are automatically enrolled f |
| exact unit_text overlap | `v05_batch100_0034` | `v05_batch100_0034` | Deploy the waitlist feature to staging first and run the enrollment integration tests before product |
| exact unit_text overlap | `v05_batch100_0035` | `v05_batch100_0035` | Add separate build targets for PC, PlayStation 5, and Nintendo Switch with platform-specific texture |
| exact unit_text overlap | `v05_batch100_0035` | `v05_batch100_0035` | The Switch build must use ASTC 4x4 compression and cap textures at 2048x2048 to meet memory constrai |
| exact unit_text overlap | `v05_batch100_0036` | `v05_batch100_0036` | Add cross-document summarization that takes up to 10 related documents and produces a unified summar |
| exact unit_text overlap | `v05_batch100_0036` | `v05_batch100_0036` | The cross-document summary must cite the source document for each claim using the document file path |
| exact unit_text overlap | `v05_batch100_0036` | `v05_batch100_0036` | Evaluate the cross-document summary quality using the ROUGE-L metric on the benchmark set. |
| exact unit_text overlap | `v05_batch100_0037` | `v05_batch100_0037` | Add a streaming aggregation path using Kafka that updates dashboard metrics in real-time for transac |
| exact unit_text overlap | `v05_batch100_0037` | `v05_batch100_0037` | The streaming path must fall back to batch aggregation when Kafka is unavailable, maintaining the 5- |
| exact unit_text overlap | `v05_batch100_0038` | `v05_batch100_0038` | Add a tiered cancellation policy engine: refundable fares get 100% refund, standard fares get 50%, b |
| exact unit_text overlap | `v05_batch100_0038` | `v05_batch100_0038` | Refunds must be processed back to the original payment method within 5 business days for refundable  |
| exact unit_text overlap | `v05_batch100_0039` | `v05_batch100_0039` | Add a grade appeal workflow where students can submit an appeal within 14 days of grade posting with |
| exact unit_text overlap | `v05_batch100_0039` | `v05_batch100_0039` | Appeals must be reviewed by a different instructor than the one who assigned the original grade. |
| exact unit_text overlap | `v05_batch100_0039` | `v05_batch100_0039` | All grade changes from appeals must be logged to the grade_audit table with the original grade, new  |
| exact unit_text overlap | `v05_batch100_0040` | `v05_batch100_0040` | Add incremental asset processing: only rebuild assets whose content hash has changed since the last  |
| exact unit_text overlap | `v05_batch100_0040` | `v05_batch100_0040` | Asset dependencies should be tracked in a directed graph so that changing a parent asset triggers re |
| exact unit_text overlap | `v05_batch100_0040` | `v05_batch100_0040` | Run a full rebuild after implementing incremental processing to establish the baseline content hashe |
| exact unit_text overlap | `v05_batch100_0041` | `v05_batch100_0041` | Add incremental indexing that only processes documents changed since the last indexed commit. |
| exact unit_text overlap | `v05_batch100_0041` | `v05_batch100_0041` | The incremental index must still support full reindex as a fallback triggered by a manual command. |
| exact unit_text overlap | `v05_batch100_0042` | `v05_batch100_0042` | Add a dark mode toggle that switches all chart colors to a dark palette with light text and muted gr |
| exact unit_text overlap | `v05_batch100_0042` | `v05_batch100_0042` | I prefer dashboards with compact layouts showing 4 charts per row instead of the default 2. |
| exact unit_text overlap | `v05_batch100_0043` | `v05_batch100_0043` | I prefer to see prices in EUR even when searching for flights originating in the US. |
| exact unit_text overlap | `v05_batch100_0043` | `v05_batch100_0043` | Always show the number of stops prominently in search results, not hidden in the detail view. |
| exact unit_text overlap | `v05_batch100_0043` | `v05_batch100_0043` | My passport number for test bookings is P12345678. |
| exact unit_text overlap | `v05_batch100_0044` | `v05_batch100_0044` | Add a recommendation engine that suggests courses based on a student's completed courses and stated  |
| exact unit_text overlap | `v05_batch100_0044` | `v05_batch100_0044` | The recommendation engine should explain why each course was recommended using a one-line reason. |
| exact unit_text overlap | `v05_batch100_0044` | `v05_batch100_0044` | I prefer course recommendations that prioritize courses taught by instructors I have rated highly in |
| exact unit_text overlap | `v05_batch100_0045` | `v05_batch100_0045` | Add automated performance tests that run after each build and fail if frame-time exceeds 16ms on the |
| exact unit_text overlap | `v05_batch100_0045` | `v05_batch100_0045` | Performance test results should be stored in build/perf_results/YYYY-MM-DD/ with a comparison to the |
| exact unit_text overlap | `v05_batch100_0046` | `v05_batch100_0046` | The docs-assistant search scope is limited to public documentation repositories; private repos requi |
| exact unit_text overlap | `v05_batch100_0046` | `v05_batch100_0046` | Add support for searching private repos by integrating with the org's OAuth provider for repository  |
| exact unit_text overlap | `v05_batch100_0047` | `v05_batch100_0047` | All finboard services must suppress non-critical alerts during the monthly maintenance window from 0 |
| exact unit_text overlap | `v05_batch100_0047` | `v05_batch100_0047` | Critical PagerDuty alerts must never be suppressed, even during maintenance windows. |
| exact unit_text overlap | `v05_batch100_0047` | `v05_batch100_0047` | Add the monthly maintenance suppression rule to the alerts configuration before the next maintenance |
| exact unit_text overlap | `v05_batch100_0048` | `v05_batch100_0048` | The voyager booking service only supports flight bookings; hotel and car rental are explicitly out o |
| exact unit_text overlap | `v05_batch100_0048` | `v05_batch100_0048` | The booking confirmation email template is defined in templates/email/booking_confirmation.html. |
| exact unit_text overlap | `v05_batch100_0048` | `v05_batch100_0048` | Write the scope document section explaining that multi-modal bookings are deferred to v2. |
| exact unit_text overlap | `v05_batch100_0049` | `v05_batch100_0049` | Add prerequisite validation that blocks enrollment if the student has not completed all prerequisite |
| exact unit_text overlap | `v05_batch100_0049` | `v05_batch100_0049` | The prerequisite check must also consider equivalent courses from other institutions as defined in t |
| exact unit_text overlap | `v05_batch100_0049` | `v05_batch100_0049` | My student ID for testing the enrollment flow is STUDENT-TEST-0001. |
| exact unit_text overlap | `v05_batch100_0050` | `v05_batch100_0050` | Add a quality scoring system that evaluates textures on resolution, compression artifacts, and color |
| exact unit_text overlap | `v05_batch100_0050` | `v05_batch100_0050` | Assets scoring below 80/100 must be flagged in the build report and blocked from release builds. |
| exact unit_text overlap | `v05_batch100_0050` | `v05_batch100_0050` | I prefer game assets to use a realistic art style with muted colors rather than cartoon-style satura |
| exact unit_text overlap | `v05_batch200_0001` | `v05_batch200_0001` | Why are ticket searches returning results from last week but not today? |
| exact unit_text overlap | `v05_batch200_0002` | `v05_batch200_0002` | Does the product variant cache get invalidated when inventory levels change? |
| exact unit_text overlap | `v05_batch200_0003` | `v05_batch200_0003` | What happens when a dashboard query exceeds the timeout — does it fail or return partial results? |
| exact unit_text overlap | `v05_batch200_0004` | `v05_batch200_0004` | How does the routing service decide which agent gets a ticket about refund processing? |
| exact unit_text overlap | `v05_batch200_0005` | `v05_batch200_0005` | What is the stock reservation timeout for items in the shopping cart? |
| exact unit_text overlap | `v05_batch200_0006` | `v05_batch200_0006` | The revenue trend chart shows no data for the last 3 hours — is this a cache issue or a data pipelin |
| exact unit_text overlap | `v05_batch200_0007` | `v05_batch200_0007` | Does the SLA timer continue running when a ticket is assigned to an agent but not yet acknowledged? |
| exact unit_text overlap | `v05_batch200_0008` | `v05_batch200_0008` | Search queries that used to return in 200ms now take 3 seconds — check if the cache is working. |
| exact unit_text overlap | `v05_batch200_0009` | `v05_batch200_0009` | What fields are in the product variant attributes JSONB column? |
| exact unit_text overlap | `v05_batch200_0010` | `v05_batch200_0010` | How does the query engine decide whether a query needs approval before running? |
| exact unit_text overlap | `v05_batch200_0011` | `v05_batch200_0011` | Which capture modes support HDR on the current version? |
| exact unit_text overlap | `v05_batch200_0012` | `v05_batch200_0012` | When did the last incremental load complete and how many rows did it process? |
| exact unit_text overlap | `v05_batch200_0013` | `v05_batch200_0013` | What metrics does the eval_runner compute for each interface? |
| exact unit_text overlap | `v05_batch200_0014` | `v05_batch200_0014` | Where does the quiz generator pull questions from for a history quiz at medium difficulty? |
| exact unit_text overlap | `v05_batch200_0015` | `v05_batch200_0015` | What happens when a workflow step fails 3 times — does the entire workflow fail or just that step? |
| exact unit_text overlap | `v05_batch200_0016` | `v05_batch200_0016` | What is the maximum file size and number of attachments per ticket? |
| exact unit_text overlap | `v05_batch200_0017` | `v05_batch200_0017` | What order status transitions trigger an entry in the order_events table? |
| exact unit_text overlap | `v05_batch200_0018` | `v05_batch200_0018` | How do I configure a dashboard report to run every Monday at 08:00? |
| exact unit_text overlap | `v05_batch200_0019` | `v05_batch200_0019` | What is the baggage allowance for premium-economy on international flights? |
| exact unit_text overlap | `v05_batch200_0020` | `v05_batch200_0020` | Does 89.5 round to 90 or stay at 89? |
| exact unit_text overlap | `v05_batch200_0021` | `v05_batch200_0021` | The routing service must never assign a ticket about billing discrepancies to an agent who has not c |
| exact unit_text overlap | `v05_batch200_0021` | `v05_batch200_0021` | Agent certification status is stored in the agents table with a JSON column certifications containin |
| exact unit_text overlap | `v05_batch200_0021` | `v05_batch200_0021` | The current agent certification check only validates at assignment time, not at ticket reassignment. |
| exact unit_text overlap | `v05_batch200_0022` | `v05_batch200_0022` | The catalog service must reject any product where the price is negative or the SKU is not unique acr |
| exact unit_text overlap | `v05_batch200_0022` | `v05_batch200_0022` | The catalog service must also validate that product images are at least 500x500 pixels and in WebP f |
| exact unit_text overlap | `v05_batch200_0022` | `v05_batch200_0022` | The product validation rules must be documented in docs/catalog/validation_rules.md for the onboardi |
| exact unit_text overlap | `v05_batch200_0023` | `v05_batch200_0023` | The query engine must reject any query that contains a DROP, DELETE, or TRUNCATE statement. |
| exact unit_text overlap | `v05_batch200_0023` | `v05_batch200_0023` | The query engine stores an audit log of all executed queries in the query_audit table with the user  |
| exact unit_text overlap | `v05_batch200_0023` | `v05_batch200_0023` | The helpdesk project decided to use only PostgreSQL as the query engine backend, not MySQL or BigQue |
| exact unit_text overlap | `v05_batch200_0024` | `v05_batch200_0024` | The helpdesk project SLA guarantees first-response within 1 hour for critical tickets, 4 hours for n |
| exact unit_text overlap | `v05_batch200_0024` | `v05_batch200_0024` | The ticketing service sends an escalation alert to the team lead when a critical ticket approaches t |
| exact unit_text overlap | `v05_batch200_0024` | `v05_batch200_0024` | I prefer ticket queues sorted by oldest-first within each priority level. |
| exact unit_text overlap | `v05_batch200_0025` | `v05_batch200_0025` | The inventory service must sync stock levels with the warehouse management system within 60 seconds  |
| exact unit_text overlap | `v05_batch200_0025` | `v05_batch200_0025` | Inventory sync failures are logged to the inventory_sync_log table and retried every 5 minutes for u |
| exact unit_text overlap | `v05_batch200_0025` | `v05_batch200_0025` | My warehouse API access key for the test environment is WH-TEST-KEY-1234567890. |
| exact unit_text overlap | `v05_batch200_0026` | `v05_batch200_0026` | The visualizer must render all charts with a data freshness timestamp showing when the underlying qu |
| exact unit_text overlap | `v05_batch200_0026` | `v05_batch200_0026` | Chart color palettes are defined in config/visualizer/palettes.yaml with separate entries for light  |
| exact unit_text overlap | `v05_batch200_0026` | `v05_batch200_0026` | Update the chart rendering library to the latest version before the next release. |
| exact unit_text overlap | `v05_batch200_0027` | `v05_batch200_0027` | All helpdesk services must mask customer email addresses in logs and audit trails. |
| exact unit_text overlap | `v05_batch200_0027` | `v05_batch200_0027` | The routing service specifically must also mask customer phone numbers in the agent assignment previ |
| exact unit_text overlap | `v05_batch200_0027` | `v05_batch200_0027` | Add email masking to the ticketing service logs before the SOC 2 audit next month. |
| exact unit_text overlap | `v05_batch200_0028` | `v05_batch200_0028` | All orders must be processed in the order they were confirmed, except for orders flagged as priority |
| exact unit_text overlap | `v05_batch200_0028` | `v05_batch200_0028` | Order processing scripts live under scripts/orders/ and use the naming convention process_{status}.p |
| exact unit_text overlap | `v05_batch200_0028` | `v05_batch200_0028` | Refund orders should be processed within 2 hours during business hours; outside business hours, they |
| exact unit_text overlap | `v05_batch200_0029` | `v05_batch200_0029` | The scheduler must never send a report containing data from more than one client organization in a s |
| exact unit_text overlap | `v05_batch200_0029` | `v05_batch200_0029` | Report generation failures are retried 3 times at 5-minute intervals before notifying the dashboard  |
| exact unit_text overlap | `v05_batch200_0029` | `v05_batch200_0029` | The customer support team has requested a custom report showing ticket resolution time by agent. |
| exact unit_text overlap | `v05_batch200_0030` | `v05_batch200_0030` | The quiz generator calibrates question difficulty based on historical answer accuracy: questions ans |
| exact unit_text overlap | `v05_batch200_0030` | `v05_batch200_0030` | Difficulty calibration runs as a nightly batch job and updates the difficulty field in the question_ |
| exact unit_text overlap | `v05_batch200_0030` | `v05_batch200_0030` | The studybuddy project does not include live tutoring or video conferencing features. |
| exact unit_text overlap | `v05_batch200_0031` | `v05_batch200_0031` | The orchestrator must execute workflow steps in dependency order: a step cannot start until all its  |
| exact unit_text overlap | `v05_batch200_0031` | `v05_batch200_0031` | Workflow definitions are stored in config/workflows/ as YAML files with a DAG section specifying ste |
| exact unit_text overlap | `v05_batch200_0031` | `v05_batch200_0031` | Add a visual DAG editor to the workflow management UI. |
| exact unit_text overlap | `v05_batch200_0032` | `v05_batch200_0032` | I prefer ticket response templates organized by issue category rather than by agent team. |
| exact unit_text overlap | `v05_batch200_0032` | `v05_batch200_0032` | The ticketing service must enforce that response templates include the customer's name from the tick |
| exact unit_text overlap | `v05_batch200_0032` | `v05_batch200_0032` | My personal login password for the helpdesk admin panel is HD-admin-2026!. |
| exact unit_text overlap | `v05_batch200_0033` | `v05_batch200_0033` | The catalog service ranks search results by a combination of text relevance score, product rating, a |
| exact unit_text overlap | `v05_batch200_0033` | `v05_batch200_0033` | Search ranking weights are configurable in config/catalog/search_ranking.yaml with the keys text_wei |
| exact unit_text overlap | `v05_batch200_0033` | `v05_batch200_0033` | The shopengine project must comply with GDPR requirements for customer data handling across all serv |
| exact unit_text overlap | `v05_batch200_0034` | `v05_batch200_0034` | The query engine automatically creates materialized views for queries that are executed more than 10 |
| exact unit_text overlap | `v05_batch200_0034` | `v05_batch200_0034` | Materialized view refresh schedules are configured per dashboard in config/query_engine/materialized |
| exact unit_text overlap | `v05_batch200_0034` | `v05_batch200_0034` | The current materialized view selection only considers query frequency, not query cost or data fresh |
| exact unit_text overlap | `v05_batch200_0035` | `v05_batch200_0035` | The quiz generator must ensure that multiple-choice questions have exactly one correct answer and at |
| exact unit_text overlap | `v05_batch200_0035` | `v05_batch200_0035` | Question format templates are stored in config/quiz_generator/formats/ with one JSON template per qu |
| exact unit_text overlap | `v05_batch200_0035` | `v05_batch200_0035` | I prefer quizzes with immediate feedback after each question rather than showing all results at the  |
| exact unit_text overlap | `v05_batch200_0036` | `v05_batch200_0036` | The orchestrator must log the full input and output of every failed workflow step to the step_errors |
| exact unit_text overlap | `v05_batch200_0036` | `v05_batch200_0036` | Failed workflow steps are visible in the admin dashboard under the Failed Steps tab with a retry but |
| exact unit_text overlap | `v05_batch200_0036` | `v05_batch200_0036` | The flowcraft project scope is limited to backend workflow automation; it does not include a user-fa |
| exact unit_text overlap | `v05_batch200_0037` | `v05_batch200_0037` | The routing service requires agents to have at least 3 months of tenure and a customer satisfaction  |
| exact unit_text overlap | `v05_batch200_0037` | `v05_batch200_0037` | Agent eligibility thresholds are configured in config/routing/agent_eligibility.yaml and are evaluat |
| exact unit_text overlap | `v05_batch200_0037` | `v05_batch200_0037` | Review the agent eligibility thresholds quarterly and adjust based on team performance metrics. |
| exact unit_text overlap | `v05_batch200_0038` | `v05_batch200_0038` | The orders service must validate that the shipping address is in a supported country before acceptin |
| exact unit_text overlap | `v05_batch200_0038` | `v05_batch200_0038` | Supported countries are listed in config/orders/supported_countries.yaml and updated when new wareho |
| exact unit_text overlap | `v05_batch200_0038` | `v05_batch200_0038` | My home address for testing order delivery is 5678 Commerce Blvd, ShopCity, SC 12345. |
| exact unit_text overlap | `v05_batch200_0039` | `v05_batch200_0039` | The scheduler must only deliver reports to users who have the report_view permission for that specif |
| exact unit_text overlap | `v05_batch200_0039` | `v05_batch200_0039` | Report permissions are managed in the dashboard_permissions table with columns dashboard_id, user_id |
| exact unit_text overlap | `v05_batch200_0039` | `v05_batch200_0039` | All databoard services must use OAuth 2.0 for authentication; API keys are not accepted for user-fac |
| exact unit_text overlap | `v05_batch200_0040` | `v05_batch200_0040` | The quiz generator must reject any question where the correct answer text appears verbatim in one of |
| exact unit_text overlap | `v05_batch200_0040` | `v05_batch200_0040` | Question quality checks run as part of the question import pipeline, not at quiz generation time. |
| exact unit_text overlap | `v05_batch200_0040` | `v05_batch200_0040` | Add a question quality report that shows the percentage of rejected questions by topic and difficult |
| exact unit_text overlap | `v05_batch200_0041` | `v05_batch200_0041` | The orchestrator stores workflow definitions with a version number. When a workflow is updated, runn |
| exact unit_text overlap | `v05_batch200_0041` | `v05_batch200_0041` | Workflow versions are immutable once an instance has started using them. New versions are created by |
| exact unit_text overlap | `v05_batch200_0041` | `v05_batch200_0041` | Add a workflow version comparison view that shows the diff between two versions of the same workflow |
| exact unit_text overlap | `v05_batch200_0042` | `v05_batch200_0042` | All v0.5 training runs execute on the local RTX 4070 SUPER GPU under WSL2 with batch size 4 to fit w |
| exact unit_text overlap | `v05_batch200_0042` | `v05_batch200_0042` | The training data generation pipeline must validate every case against the v0.4 case_validator befor |
| exact unit_text overlap | `v05_batch200_0042` | `v05_batch200_0042` | The project does not train a retriever, a memory writer, or any component of MemoryOS; only the memo |
| exact unit_text overlap | `v05_batch200_0043` | `v05_batch200_0043` | The ticketing service automatically closes tickets that have been in 'resolved' status for 7 days wi |
| exact unit_text overlap | `v05_batch200_0043` | `v05_batch200_0043` | Closed tickets are archived to the tickets_archive table after 90 days and are no longer searchable  |
| exact unit_text overlap | `v05_batch200_0043` | `v05_batch200_0043` | The helpdesk project retains ticket data for 7 years to comply with customer service record-keeping  |
| exact unit_text overlap | `v05_batch200_0044` | `v05_batch200_0044` | The inventory service triggers a low-stock alert when any product variant quantity falls below the r |
| exact unit_text overlap | `v05_batch200_0044` | `v05_batch200_0044` | Low-stock alerts are sent to the #inventory-alerts Slack channel and also logged to the inventory_al |
| exact unit_text overlap | `v05_batch200_0044` | `v05_batch200_0044` | The shopengine project must support both metric and imperial units for product dimensions to serve i |
| exact unit_text overlap | `v05_batch200_0045` | `v05_batch200_0045` | The visualizer must render all charts with ARIA labels and provide a keyboard-navigable data table a |
| exact unit_text overlap | `v05_batch200_0045` | `v05_batch200_0045` | Accessibility compliance is checked by the axe-core linter in the CI pipeline on every visualizer co |
| exact unit_text overlap | `v05_batch200_0045` | `v05_batch200_0045` | Add a high-contrast color palette option to the chart settings for visually impaired users. |
| exact unit_text overlap | `v05_batch200_0046` | `v05_batch200_0046` | The progress tracker computes course completion as the percentage of completed modules, where each m |
| exact unit_text overlap | `v05_batch200_0046` | `v05_batch200_0046` | Module weights are stored in the curriculum table with columns module_id and estimated_hours, update |
| exact unit_text overlap | `v05_batch200_0046` | `v05_batch200_0046` | The studybuddy project generates progress reports as PDF only; interactive progress dashboards are d |
| exact unit_text overlap | `v05_batch200_0047` | `v05_batch200_0047` | The orchestrator enforces a default timeout of 1 hour for any single workflow step. Steps exceeding  |
| exact unit_text overlap | `v05_batch200_0047` | `v05_batch200_0047` | The default timeout can be overridden per workflow step in the workflow definition YAML using the ti |
| exact unit_text overlap | `v05_batch200_0047` | `v05_batch200_0047` | Add a workflow timeout dashboard showing steps that have timed out in the last 7 days grouped by wor |
| exact unit_text overlap | `v05_batch200_0048` | `v05_batch200_0048` | The routing service distributes tickets to agents based on their current shift schedule. Agents not  |
| exact unit_text overlap | `v05_batch200_0048` | `v05_batch200_0048` | Agent shift schedules are imported from the workforce management system every 4 hours via a CSV file |
| exact unit_text overlap | `v05_batch200_0048` | `v05_batch200_0048` | The current shift import only runs on weekdays; weekend shift changes are not picked up until Monday |
| exact unit_text overlap | `v05_batch200_0049` | `v05_batch200_0049` | The catalog service retains product data for discontinued products for 2 years after discontinuation |
| exact unit_text overlap | `v05_batch200_0049` | `v05_batch200_0049` | Archived product data is stored in S3 bucket shopengine-catalog-archive with glacier storage class a |
| exact unit_text overlap | `v05_batch200_0049` | `v05_batch200_0049` | I prefer product search results sorted by customer rating within each category, not by relevance sco |
| exact unit_text overlap | `v05_batch200_0050` | `v05_batch200_0050` | The scheduler generates all reports in PDF/A format for archival compliance. Interactive HTML report |
| exact unit_text overlap | `v05_batch200_0050` | `v05_batch200_0050` | Report format configuration per dashboard is in config/scheduler/report_formats.yaml with keys pdf_t |
| exact unit_text overlap | `v05_batch200_0050` | `v05_batch200_0050` | Add an option to include raw CSV data as an attachment alongside the formatted PDF report. |
| exact unit_text overlap | `v05_batch200_0051` | `v05_batch200_0051` | Add an SLA breach notification that sends an email to the team lead and posts to the #sla-alerts Sla |
| exact unit_text overlap | `v05_batch200_0051` | `v05_batch200_0051` | The notification must include the ticket ID, customer name, time since creation, and the assigned ag |
| exact unit_text overlap | `v05_batch200_0052` | `v05_batch200_0052` | Add automatic restock orders to the warehouse when inventory falls below the reorder threshold plus  |
| exact unit_text overlap | `v05_batch200_0052` | `v05_batch200_0052` | The restock order must include the product SKU, current quantity, reorder threshold, and the calcula |
| exact unit_text overlap | `v05_batch200_0052` | `v05_batch200_0052` | Test the restock automation with the staging warehouse API before enabling it for production. |
| exact unit_text overlap | `v05_batch200_0053` | `v05_batch200_0053` | Add a query result cache that stores results for identical queries with a TTL of 15 minutes, keyed b |
| exact unit_text overlap | `v05_batch200_0053` | `v05_batch200_0053` | The cache must invalidate when the underlying tables are modified, using the table last_modified tim |
| exact unit_text overlap | `v05_batch200_0054` | `v05_batch200_0054` | Add a search result cache layer using Redis to reduce database load for repeated searches. |
| exact unit_text overlap | `v05_batch200_0054` | `v05_batch200_0054` | The cache key must include the search query, filters, and the requesting agent's team to ensure team |
| exact unit_text overlap | `v05_batch200_0054` | `v05_batch200_0054` | Benchmark search performance before and after the cache layer and report the improvement. |
| exact unit_text overlap | `v05_batch200_0055` | `v05_batch200_0055` | Add a 30-minute cancellation window after order confirmation where customers can cancel without supp |
| exact unit_text overlap | `v05_batch200_0055` | `v05_batch200_0055` | Cancelled orders must automatically release reserved inventory and trigger a refund to the original  |
| exact unit_text overlap | `v05_batch200_0056` | `v05_batch200_0056` | Add drill-down interaction that allows clicking on a chart segment to see the underlying data rows i |
| exact unit_text overlap | `v05_batch200_0056` | `v05_batch200_0056` | The drill-down query must use the same filters as the parent chart plus the clicked dimension value. |
| exact unit_text overlap | `v05_batch200_0056` | `v05_batch200_0056` | I prefer dashboards where drill-down opens in a side panel rather than replacing the current view. |
| exact unit_text overlap | `v05_batch200_0057` | `v05_batch200_0057` | Add skills-based auto-assignment that matches ticket topic tags to agent skill tags, prioritizing ag |
| exact unit_text overlap | `v05_batch200_0057` | `v05_batch200_0057` | The auto-assignment algorithm must log its matching score for audit purposes in the ticket_assignmen |
| exact unit_text overlap | `v05_batch200_0058` | `v05_batch200_0058` | Add automated review moderation that flags reviews containing profanity or URLs for manual review be |
| exact unit_text overlap | `v05_batch200_0058` | `v05_batch200_0058` | Flagged reviews must be held in a moderation queue visible to catalog administrators with options to |
| exact unit_text overlap | `v05_batch200_0059` | `v05_batch200_0059` | Add conditional report triggers that only generate and send a report if the query returns more than  |
| exact unit_text overlap | `v05_batch200_0059` | `v05_batch200_0059` | Conditional triggers must support a threshold parameter configurable per report, defaulting to row_c |
| exact unit_text overlap | `v05_batch200_0060` | `v05_batch200_0060` | Add adaptive difficulty that adjusts question difficulty based on the student's performance: increas |
| exact unit_text overlap | `v05_batch200_0060` | `v05_batch200_0060` | The adaptive difficulty state must reset at the start of each new quiz session. |
| exact unit_text overlap | `v05_batch200_0061` | `v05_batch200_0061` | Add parallel step execution for workflow steps that have no dependencies on each other, respecting t |
| exact unit_text overlap | `v05_batch200_0061` | `v05_batch200_0061` | Parallel steps must share a common error handler: if any parallel step fails, all sibling parallel s |
| exact unit_text overlap | `v05_batch200_0062` | `v05_batch200_0062` | Add a trigger that only sends the survey if the ticket had at least 2 message exchanges between the  |
| exact unit_text overlap | `v05_batch200_0062` | `v05_batch200_0062` | The survey trigger threshold must be configurable in config/ticketing/survey.yaml with the min_messa |
| exact unit_text overlap | `v05_batch200_0063` | `v05_batch200_0063` | Add bundle inventory tracking that calculates available bundle quantity as the minimum available qua |
| exact unit_text overlap | `v05_batch200_0063` | `v05_batch200_0063` | Bundle availability must be recalculated whenever any component product's inventory changes. |
| exact unit_text overlap | `v05_batch200_0064` | `v05_batch200_0064` | Add parameter validation that rejects query parameters containing SQL keywords or special characters |
| exact unit_text overlap | `v05_batch200_0064` | `v05_batch200_0064` | The validation must run before parameter substitution and log rejected parameters to the query_audit |
| exact unit_text overlap | `v05_batch200_0065` | `v05_batch200_0065` | Add a learning streak counter that tracks consecutive days with at least 15 minutes of study activit |
| exact unit_text overlap | `v05_batch200_0065` | `v05_batch200_0065` | The streak counter must reset to zero after a day with no activity, and display a congratulatory mes |
| exact unit_text overlap | `v05_batch200_0066` | `v05_batch200_0066` | Add step-level execution logging that records the start time, end time, status, and output summary f |
| exact unit_text overlap | `v05_batch200_0066` | `v05_batch200_0066` | The step execution log must be retained for 1 year and be queryable by workflow_id, step_name, and e |
| exact unit_text overlap | `v05_batch200_0067` | `v05_batch200_0067` | Add workload-aware routing that assigns new tickets to the agent with the lowest current open ticket |
| exact unit_text overlap | `v05_batch200_0067` | `v05_batch200_0067` | The workload balancer must skip agents who are currently in 'away' or 'busy' status as reported by t |
| exact unit_text overlap | `v05_batch200_0068` | `v05_batch200_0068` | Add fraud detection checks that flag orders where the shipping address is in a different country fro |
| exact unit_text overlap | `v05_batch200_0068` | `v05_batch200_0068` | Flagged orders must be held in a review queue and not proceed to warehouse fulfillment until manuall |
| exact unit_text overlap | `v05_batch200_0069` | `v05_batch200_0069` | Add scheduled data exports that automatically generate and email CSV files based on a per-dashboard  |
| exact unit_text overlap | `v05_batch200_0069` | `v05_batch200_0069` | Scheduled exports must use the same data freshness guarantees as scheduled reports: data must be no  |
| exact unit_text overlap | `v05_batch200_0070` | `v05_batch200_0070` | Add time limit enforcement that auto-submits the quiz when the total time limit is reached, marking  |
| exact unit_text overlap | `v05_batch200_0070` | `v05_batch200_0070` | The time limit enforcement must show a visible countdown timer and provide a 60-second warning befor |
| exact unit_text overlap | `v05_batch200_0071` | `v05_batch200_0071` | Add a dry-run mode that executes all workflow steps but replaces write operations with logs showing  |
| exact unit_text overlap | `v05_batch200_0071` | `v05_batch200_0071` | The dry-run must produce a report showing each step's input, expected output, and any validation err |
| exact unit_text overlap | `v05_batch200_0072` | `v05_batch200_0072` | When is the next quarterly SLA report due and who receives it? |
| exact unit_text overlap | `v05_batch200_0073` | `v05_batch200_0073` | How long does a refund take to appear on the customer's credit card? |
| exact unit_text overlap | `v05_batch200_0074` | `v05_batch200_0074` | How current is the data in my dashboard compared to the source warehouse? |
| exact unit_text overlap | `v05_batch200_0075` | `v05_batch200_0075` | What are the requirements to earn a course completion certificate? |
| exact unit_text overlap | `v05_batch200_0076` | `v05_batch200_0076` | Critical tickets are defined as any issue causing complete service outage for more than 5 customers  |
| exact unit_text overlap | `v05_batch200_0076` | `v05_batch200_0076` | All helpdesk agents must complete priority classification training within their first week of onboar |
| exact unit_text overlap | `v05_batch200_0076` | `v05_batch200_0076` | Review the priority classification guidelines quarterly and update based on incident post-mortem fin |
| exact unit_text overlap | `v05_batch200_0077` | `v05_batch200_0077` | The shopengine project requires all product descriptions to include dimensions in both metric and im |
| exact unit_text overlap | `v05_batch200_0077` | `v05_batch200_0077` | The catalog service validates product descriptions against the standards schema before accepting new |
| exact unit_text overlap | `v05_batch200_0077` | `v05_batch200_0077` | I prefer product pages that show the most important specifications first, followed by detailed descr |
| exact unit_text overlap | `v05_batch200_0078` | `v05_batch200_0078` | The scheduler delivers reports only to verified email addresses associated with active dashboard vie |
| exact unit_text overlap | `v05_batch200_0078` | `v05_batch200_0078` | Report delivery failures are retried 3 times at 1-hour intervals; after 3 failures, the dashboard ow |
| exact unit_text overlap | `v05_batch200_0078` | `v05_batch200_0078` | I prefer reports delivered as inline HTML in the email body rather than PDF attachments. |
| exact unit_text overlap | `v05_batch200_0079` | `v05_batch200_0079` | The quiz generator reloads its question bank from the database every 6 hours to pick up newly added  |
| exact unit_text overlap | `v05_batch200_0079` | `v05_batch200_0079` | The question bank reload is logged in the quiz_generator_audit table with the number of questions ad |
| exact unit_text overlap | `v05_batch200_0079` | `v05_batch200_0079` | Schedule a manual question bank reload after the curriculum team finishes adding the new history mod |
| exact unit_text overlap | `v05_batch200_0080` | `v05_batch200_0080` | The orchestrator assigns execution priority to workflows based on a numeric priority field in the wo |
| exact unit_text overlap | `v05_batch200_0080` | `v05_batch200_0080` | Workflows with priority 1 preempt lower-priority workflows by pausing them and resuming after the hi |
| exact unit_text overlap | `v05_batch200_0080` | `v05_batch200_0080` | The flowcraft project does not support real-time workflow execution; the minimum scheduling granular |
| exact unit_text overlap | `v05_batch200_0081` | `v05_batch200_0081` | Agents must complete a shift handover by adding a summary note to each open ticket before logging of |
| exact unit_text overlap | `v05_batch200_0081` | `v05_batch200_0081` | The handover note is stored in the ticket_handover_notes table and is visible to the next agent who  |
| exact unit_text overlap | `v05_batch200_0081` | `v05_batch200_0081` | The current handover process does not enforce the note requirement; agents can log off without compl |
| exact unit_text overlap | `v05_batch200_0082` | `v05_batch200_0082` | All inventory stock adjustments over 50 units require manager approval before being applied. |
| exact unit_text overlap | `v05_batch200_0082` | `v05_batch200_0082` | Stock adjustments are logged in the inventory_adjustments table with the user ID, timestamp, quantit |
| exact unit_text overlap | `v05_batch200_0082` | `v05_batch200_0082` | I prefer inventory reports grouped by warehouse location rather than by product category. |
| exact unit_text overlap | `v05_batch200_0083` | `v05_batch200_0083` | The databoard project requires all shared dashboards to include a data freshness disclaimer showing  |
| exact unit_text overlap | `v05_batch200_0083` | `v05_batch200_0083` | The visualizer renders the data freshness disclaimer in the dashboard footer using the last_query_ti |
| exact unit_text overlap | `v05_batch200_0083` | `v05_batch200_0083` | Add a configuration option to customize the disclaimer text per dashboard. |
| exact unit_text overlap | `v05_batch200_0084` | `v05_batch200_0084` | The studybuddy project defines learning paths as sequences of modules where each module has prerequi |
| exact unit_text overlap | `v05_batch200_0084` | `v05_batch200_0084` | The progress tracker enforces prerequisite completion by checking the student's completed_modules li |
| exact unit_text overlap | `v05_batch200_0084` | `v05_batch200_0084` | I prefer learning paths that show a visual progress map with completed modules highlighted in green  |
| exact unit_text overlap | `v05_batch200_0085` | `v05_batch200_0085` | The orchestrator sends workflow failure notifications to the workflow owner via email and Slack. |
| exact unit_text overlap | `v05_batch200_0085` | `v05_batch200_0085` | Notification channels per workflow are configured in config/workflows/notifications.yaml with the ke |
| exact unit_text overlap | `v05_batch200_0085` | `v05_batch200_0085` | The current notification system only supports email and Slack; PagerDuty integration is planned for  |
| exact unit_text overlap | `v05_batch200_0086` | `v05_batch200_0086` | Add a free-text feedback field to the satisfaction survey in addition to the 5-star rating. |
| exact unit_text overlap | `v05_batch200_0086` | `v05_batch200_0086` | The feedback text must be stored in the ticket_survey_responses table and be searchable by the quali |
| exact unit_text overlap | `v05_batch200_0087` | `v05_batch200_0087` | Add order splitting that separates a single order into sub-orders when items are available in differ |
| exact unit_text overlap | `v05_batch200_0087` | `v05_batch200_0087` | Split orders must each have their own shipping label and tracking number, but share the original ord |
| exact unit_text overlap | `v05_batch200_0088` | `v05_batch200_0088` | Add an EXPLAIN mode that shows the query execution plan and estimated cost without actually running  |
| exact unit_text overlap | `v05_batch200_0088` | `v05_batch200_0088` | The EXPLAIN output must include estimated row scans, join strategies, and a total cost score to help |
| exact unit_text overlap | `v05_batch200_0089` | `v05_batch200_0089` | Add a configurable retry policy that enforces a cooldown period between quiz attempts and limits the |
| exact unit_text overlap | `v05_batch200_0089` | `v05_batch200_0089` | After a failed quiz attempt, show the student which questions were incorrect with the correct answer |
| exact unit_text overlap | `v05_batch200_0090` | `v05_batch200_0090` | Add support for importing workflow definitions from JSON files in addition to the existing YAML form |
| exact unit_text overlap | `v05_batch200_0090` | `v05_batch200_0090` | Imported JSON workflows must be validated against the same schema as YAML workflows before being acc |
| exact unit_text overlap | `v05_batch200_0091` | `v05_batch200_0091` | Add language-based routing that matches the customer's preferred language from their profile to agen |
| exact unit_text overlap | `v05_batch200_0091` | `v05_batch200_0091` | If no agent speaks the customer's language, the ticket must be assigned to a general queue with a fl |
| exact unit_text overlap | `v05_batch200_0092` | `v05_batch200_0092` | Add a product comparison endpoint that accepts up to 4 product IDs and returns their attributes in a |
| exact unit_text overlap | `v05_batch200_0092` | `v05_batch200_0092` | The comparison response must include only the attributes that are common across all compared product |
| exact unit_text overlap | `v05_batch200_0093` | `v05_batch200_0093` | Add a self-service subscription page where users can subscribe or unsubscribe from dashboard reports |
| exact unit_text overlap | `v05_batch200_0093` | `v05_batch200_0093` | Every report email must include an unsubscribe link that works without requiring the user to log in. |
| exact unit_text overlap | `v05_batch200_0094` | `v05_batch200_0094` | Add a weekly progress digest email that summarizes study time, modules completed, quiz scores, and s |
| exact unit_text overlap | `v05_batch200_0094` | `v05_batch200_0094` | The digest must compare current week metrics to the previous week and highlight improvements or decl |
| exact unit_text overlap | `v05_batch200_0095` | `v05_batch200_0095` | Add SLA monitoring that alerts the workflow owner when a workflow exceeds its SLA deadline by more t |
| exact unit_text overlap | `v05_batch200_0095` | `v05_batch200_0095` | SLA alerts must include the workflow name, trigger time, current duration, and the percentage over t |
| exact unit_text overlap | `v05_batch200_0096` | `v05_batch200_0096` | Add duplicate detection that compares new ticket subjects and bodies against open tickets and sugges |
| exact unit_text overlap | `v05_batch200_0096` | `v05_batch200_0096` | When duplicate tickets are merged, the original ticket must be updated with a reference to the dupli |
| exact unit_text overlap | `v05_batch200_0097` | `v05_batch200_0097` | Add a stock depletion predictor that estimates days until stockout based on the 30-day average daily |
| exact unit_text overlap | `v05_batch200_0097` | `v05_batch200_0097` | The predictor must update its estimates daily and trigger an early warning when predicted days-until |
| exact unit_text overlap | `v05_batch200_0098` | `v05_batch200_0098` | Add an annotation layer that allows users to add text notes to specific data points on any chart. |
| exact unit_text overlap | `v05_batch200_0098` | `v05_batch200_0098` | Annotations must be stored with the dashboard configuration and persist across dashboard refreshes a |
| exact unit_text overlap | `v05_batch200_0099` | `v05_batch200_0099` | Add a difficulty badge that displays on completed quizzes: bronze for easy, silver for medium, gold  |
| exact unit_text overlap | `v05_batch200_0099` | `v05_batch200_0099` | The badge must appear on the student's profile page and in the quiz completion email notification. |
| exact unit_text overlap | `v05_batch200_0100` | `v05_batch200_0100` | Add a template library where common workflow patterns can be saved as templates and instantiated wit |
| exact unit_text overlap | `v05_batch200_0100` | `v05_batch200_0100` | Template instantiation must validate that all required parameters are provided and reject the workfl |
| exact unit_text overlap | `v05_batch300_0001` | `v05_batch300_0001` | What exact checks does the case validator perform on gold data? |
| exact unit_text overlap | `v05_batch300_0002` | `v05_batch300_0002` | After how many days of no response does a resolved ticket get auto-closed? |
| exact unit_text overlap | `v05_batch300_0003` | `v05_batch300_0003` | What are the minimum dimensions and format for product listing images? |
| exact unit_text overlap | `v05_batch300_0004` | `v05_batch300_0004` | What happens when a query runs longer than 30 seconds? |
| exact unit_text overlap | `v05_batch300_0005` | `v05_batch300_0005` | What boost factor does the search service apply to title matches? |
| exact unit_text overlap | `v05_batch300_0006` | `v05_batch300_0006` | At what revenue threshold does an alert become critical? |
| exact unit_text overlap | `v05_batch300_0007` | `v05_batch300_0007` | What components make up the total fare displayed to customers? |
| exact unit_text overlap | `v05_batch300_0008` | `v05_batch300_0008` | What are the default weights for assignments, quizzes, and final exam? |
| exact unit_text overlap | `v05_batch300_0009` | `v05_batch300_0009` | What compression format and quality level does the pipeline use for mobile textures? |
| exact unit_text overlap | `v05_batch300_0010` | `v05_batch300_0010` | How many correct answers and distractors are required for multiple-choice questions? |
| exact unit_text overlap | `v05_batch300_0011` | `v05_batch300_0011` | How many times does the orchestrator retry a failed workflow step? |
| exact unit_text overlap | `v05_batch300_0012` | `v05_batch300_0012` | Which camera modes support HDR capture? |
| exact unit_text overlap | `v05_batch300_0013` | `v05_batch300_0013` | What time does the daily invoice export run? |
| exact unit_text overlap | `v05_batch300_0014` | `v05_batch300_0014` | How often are agent shift schedules imported into the routing service? |
| exact unit_text overlap | `v05_batch300_0015` | `v05_batch300_0015` | What are the four main order status states in sequence? |
| exact unit_text overlap | `v05_batch300_0016` | `v05_batch300_0016` | How are scheduled reports delivered to dashboard owners? |
| exact unit_text overlap | `v05_batch300_0017` | `v05_batch300_0017` | What is the maximum sentence count and code block policy for summaries? |
| exact unit_text overlap | `v05_batch300_0018` | `v05_batch300_0018` | How often does the dashboard refresh its chart data when someone is viewing it? |
| exact unit_text overlap | `v05_batch300_0019` | `v05_batch300_0019` | The eval_runner has been run on the full subset50 dataset but not yet on the extended 200-case batch |
| exact unit_text overlap | `v05_batch300_0019` | `v05_batch300_0019` | Next, extend the eval_runner to support the batch200 case format with the v05_batch200_dry_run sourc |
| exact unit_text overlap | `v05_batch300_0019` | `v05_batch300_0019` | The evaluation results for subset50 are stored in reports/v04/ with per-interface breakdown CSV file |
| exact unit_text overlap | `v05_batch300_0020` | `v05_batch300_0020` | Implement the ticket merge detection feature that identifies duplicate tickets by comparing subject  |
| exact unit_text overlap | `v05_batch300_0020` | `v05_batch300_0020` | Write integration tests for the ticket merge detection in tests/ticketing/test_merge_detection.py. |
| exact unit_text overlap | `v05_batch300_0020` | `v05_batch300_0020` | Update the ticketing API documentation to include the new merge endpoint at docs/ticketing/api/merge |
| exact unit_text overlap | `v05_batch300_0021` | `v05_batch300_0021` | The shopengine project retains order data for 7 years and inventory data for 3 years after product d |
| exact unit_text overlap | `v05_batch300_0021` | `v05_batch300_0021` | The project does not store full credit card numbers; only the last 4 digits and the payment processo |
| exact unit_text overlap | `v05_batch300_0021` | `v05_batch300_0021` | Draft the data retention policy document for the legal review next sprint. |
| exact unit_text overlap | `v05_batch300_0022` | `v05_batch300_0022` | All query engine unit tests must run with pytest and use the test_query_engine fixture defined in te |
| exact unit_text overlap | `v05_batch300_0022` | `v05_batch300_0022` | Query engine integration tests require a local PostgreSQL instance and are skipped in CI unless the  |
| exact unit_text overlap | `v05_batch300_0022` | `v05_batch300_0022` | Run the full test suite before merging any query engine changes to the main branch. |
| exact unit_text overlap | `v05_batch300_0023` | `v05_batch300_0023` | I prefer search results that show the document section heading alongside the snippet for context. |
| exact unit_text overlap | `v05_batch300_0023` | `v05_batch300_0023` | When searching across multiple repositories, group results by repo first, then sort by relevance wit |
| exact unit_text overlap | `v05_batch300_0023` | `v05_batch300_0023` | My personal access token for the docs-bot beta is docs-beta-token-xxxxxxxxxxxxx. |
| exact unit_text overlap | `v05_batch300_0024` | `v05_batch300_0024` | The finboard project must retain all alert history for 5 years to comply with financial audit requir |
| exact unit_text overlap | `v05_batch300_0024` | `v05_batch300_0024` | Alert notification emails must include a standard confidentiality footer as defined in the corporate |
| exact unit_text overlap | `v05_batch300_0024` | `v05_batch300_0024` | Add the confidentiality footer to all alert notification templates before the compliance audit next  |
| exact unit_text overlap | `v05_batch300_0025` | `v05_batch300_0025` | Booking service deployments follow the blue-green pattern with the active environment defined in con |
| exact unit_text overlap | `v05_batch300_0025` | `v05_batch300_0025` | Database migrations for the booking service must be applied manually before the deployment switch vi |
| exact unit_text overlap | `v05_batch300_0025` | `v05_batch300_0025` | Run the deployment smoke tests against the staging environment after the next booking service deploy |
| exact unit_text overlap | `v05_batch300_0026` | `v05_batch300_0026` | Implement the prerequisite validation check that blocks enrollment if prerequisites are not complete |
| exact unit_text overlap | `v05_batch300_0026` | `v05_batch300_0026` | Add equivalent course mapping data for the top 5 partner institutions in fixtures/course_equivalency |
| exact unit_text overlap | `v05_batch300_0026` | `v05_batch300_0026` | Test the enrollment flow with a student who has completed prerequisites at a partner institution. |
| exact unit_text overlap | `v05_batch300_0027` | `v05_batch300_0027` | The dungeon-tools project supports builds for Windows, macOS, and Linux platforms only; console buil |
| exact unit_text overlap | `v05_batch300_0027` | `v05_batch300_0027` | The project uses Unity 2024 LTS as the engine version; upgrading to a newer LTS requires a full proj |
| exact unit_text overlap | `v05_batch300_0027` | `v05_batch300_0027` | Schedule the Unity version upgrade assessment for the next planning sprint. |
| exact unit_text overlap | `v05_batch300_0028` | `v05_batch300_0028` | I prefer the learning dashboard to show weekly progress as a bar chart rather than a line graph. |
| exact unit_text overlap | `v05_batch300_0028` | `v05_batch300_0028` | Show completed modules at the top of the dashboard with a green checkmark, and in-progress modules b |
| exact unit_text overlap | `v05_batch300_0028` | `v05_batch300_0028` | My student account recovery email for studybuddy is personal.student@email.com. |
| exact unit_text overlap | `v05_batch300_0029` | `v05_batch300_0029` | Workflow definitions are stored under config/workflows/ with one YAML file per workflow named {workf |
| exact unit_text overlap | `v05_batch300_0029` | `v05_batch300_0029` | Workflow templates for common patterns are in config/workflows/templates/ with parameterized YAML fi |
| exact unit_text overlap | `v05_batch300_0029` | `v05_batch300_0029` | Validate all workflow YAML files against the schema before committing by running scripts/validate_wo |
| exact unit_text overlap | `v05_batch300_0030` | `v05_batch300_0030` | All helpdesk services must use OAuth 2.0 with MFA for agent authentication. |
| exact unit_text overlap | `v05_batch300_0030` | `v05_batch300_0030` | Customer PII in tickets must be masked in logs and only visible to agents with the pii_view permissi |
| exact unit_text overlap | `v05_batch300_0030` | `v05_batch300_0030` | Enable MFA enforcement for all agent accounts before the end of the quarter. |
| exact unit_text overlap | `v05_batch300_0031` | `v05_batch300_0031` | Update the product image validation to also check for minimum contrast ratio of 4.5:1 for accessibil |
| exact unit_text overlap | `v05_batch300_0031` | `v05_batch300_0031` | Add a batch image processing endpoint that accepts up to 100 product images and returns validation r |
| exact unit_text overlap | `v05_batch300_0031` | `v05_batch300_0031` | The catalog image processing pipeline currently runs synchronously and blocks the product creation A |
| exact unit_text overlap | `v05_batch300_0032` | `v05_batch300_0032` | The visualizer CI pipeline runs linting with eslint, unit tests with jest, and accessibility checks  |
| exact unit_text overlap | `v05_batch300_0032` | `v05_batch300_0032` | Visualizer component tests use Storybook snapshots stored in tests/visualizer/__snapshots__/. |
| exact unit_text overlap | `v05_batch300_0032` | `v05_batch300_0032` | Fix the failing accessibility check on the chart legend component before the next release. |
| exact unit_text overlap | `v05_batch300_0033` | `v05_batch300_0033` | The docs-assistant project indexes only public GitHub repositories with an MIT, Apache 2.0, or BSD l |
| exact unit_text overlap | `v05_batch300_0033` | `v05_batch300_0033` | Private repository indexing requires a separate enterprise instance with per-organization OAuth auth |
| exact unit_text overlap | `v05_batch300_0033` | `v05_batch300_0033` | The current index contains 1,200 public repos and is rebuilt fully every Sunday at 03:00 UTC. |
| exact unit_text overlap | `v05_batch300_0034` | `v05_batch300_0034` | Aggregator data pipeline jobs are defined in dbt models under models/aggregator/ with the naming con |
| exact unit_text overlap | `v05_batch300_0034` | `v05_batch300_0034` | Pipeline job dependencies are managed by Airflow DAGs in dags/aggregator/ with schedule intervals de |
| exact unit_text overlap | `v05_batch300_0034` | `v05_batch300_0034` | Add a new daily aggregation job for customer acquisition cost under models/aggregator/agg_daily_cac. |
| exact unit_text overlap | `v05_batch300_0035` | `v05_batch300_0035` | Investigate the pricing discrepancy where international business-class fares are calculated 15% high |
| exact unit_text overlap | `v05_batch300_0035` | `v05_batch300_0035` | Compare the fare calculation for 10 sample international routes against the airline API sandbox and  |
| exact unit_text overlap | `v05_batch300_0035` | `v05_batch300_0035` | If the discrepancy is confirmed, file a bug report with the pricing module team before the end of th |
| exact unit_text overlap | `v05_batch300_0036` | `v05_batch300_0036` | The learnhub project requires all courses to publish their grading rubric within the first week of t |
| exact unit_text overlap | `v05_batch300_0036` | `v05_batch300_0036` | Grade appeals must be resolved within 10 business days and the resolution must include written feedb |
| exact unit_text overlap | `v05_batch300_0036` | `v05_batch300_0036` | Update the grading policy document at docs/grading/policy.md to include the new appeal resolution ti |
| exact unit_text overlap | `v05_batch300_0037` | `v05_batch300_0037` | Asset build scripts are organized by platform under scripts/build/{platform}/ with a shared common l |
| exact unit_text overlap | `v05_batch300_0037` | `v05_batch300_0037` | Build scripts must be executable via the top-level Makefile target make build-assets-{platform}. |
| exact unit_text overlap | `v05_batch300_0037` | `v05_batch300_0037` | Add a Windows build script under scripts/build/windows/ that mirrors the existing macOS and Linux sc |
| exact unit_text overlap | `v05_batch300_0038` | `v05_batch300_0038` | I prefer quizzes with a mix of multiple-choice and short-answer questions rather than all one format |
| exact unit_text overlap | `v05_batch300_0038` | `v05_batch300_0038` | Show the time remaining for each question in a subtle progress bar at the top, not as a flashing cou |
| exact unit_text overlap | `v05_batch300_0038` | `v05_batch300_0038` | Remember to add the new history module questions before the semester starts. |
| exact unit_text overlap | `v05_batch300_0039` | `v05_batch300_0039` | The flowcraft project guarantees 99.9% uptime for the workflow orchestration engine during business  |
| exact unit_text overlap | `v05_batch300_0039` | `v05_batch300_0039` | All workflow definitions must include a failure_workflow reference that triggers when the primary wo |
| exact unit_text overlap | `v05_batch300_0039` | `v05_batch300_0039` | Monitor the orchestrator uptime for the next 30 days and report if the 99.9% SLA is breached. |
| exact unit_text overlap | `v05_batch300_0040` | `v05_batch300_0040` | Complete the agent workload balancing feature by the end of this sprint. |
| exact unit_text overlap | `v05_batch300_0040` | `v05_batch300_0040` | Write the user acceptance test scenarios for workload-based routing and review with the QA team. |
| exact unit_text overlap | `v05_batch300_0040` | `v05_batch300_0040` | The current sprint ends on Friday; any unfinished tasks will roll over to the next sprint. |
| exact unit_text overlap | `v05_batch300_0041` | `v05_batch300_0041` | All order service PRs require at least two approvals from the shopengine-backend team before merging |
| exact unit_text overlap | `v05_batch300_0041` | `v05_batch300_0041` | Code review comments must reference the specific line number and include a suggested fix or a link t |
| exact unit_text overlap | `v05_batch300_0041` | `v05_batch300_0041` | Review the open PRs for the order splitting feature and approve or request changes by end of day. |
| exact unit_text overlap | `v05_batch300_0042` | `v05_batch300_0042` | The databoard project classifies all reports as either internal (visible to org members) or restrict |
| exact unit_text overlap | `v05_batch300_0042` | `v05_batch300_0042` | Restricted reports must not appear in global search results and require explicit dashboard membershi |
| exact unit_text overlap | `v05_batch300_0042` | `v05_batch300_0042` | Audit the current report access permissions and ensure no restricted reports are visible to unauthor |
| exact unit_text overlap | `v05_batch300_0043` | `v05_batch300_0043` | I prefer summaries that start with a one-line TL;DR before the detailed bullet points. |
| exact unit_text overlap | `v05_batch300_0043` | `v05_batch300_0043` | When summarizing API documentation, include the endpoint method and path as the first bullet point. |
| exact unit_text overlap | `v05_batch300_0043` | `v05_batch300_0043` | Generate a summary for the new authentication guide that was published yesterday. |
| exact unit_text overlap | `v05_batch300_0044` | `v05_batch300_0044` | Implement the dark mode toggle that persists user preference in localStorage. |
| exact unit_text overlap | `v05_batch300_0044` | `v05_batch300_0044` | Write CSS custom properties for all chart components to support theming without per-component style  |
| exact unit_text overlap | `v05_batch300_0044` | `v05_batch300_0044` | Test dark mode on the CFO's dashboard configuration which uses custom chart colors. |
| exact unit_text overlap | `v05_batch300_0045` | `v05_batch300_0045` | The voyager project guarantees that bookings are confirmed within 30 seconds of payment authorizatio |
| exact unit_text overlap | `v05_batch300_0045` | `v05_batch300_0045` | All booking confirmation emails must include the airline's 24-hour cancellation policy and a direct  |
| exact unit_text overlap | `v05_batch300_0045` | `v05_batch300_0045` | Update the booking confirmation email template to include the new airline partner's cancellation ter |
| exact unit_text overlap | `v05_batch300_0046` | `v05_batch300_0046` | Course configuration files are stored in config/courses/{course_id}.yaml with prerequisite, capacity |
| exact unit_text overlap | `v05_batch300_0046` | `v05_batch300_0046` | Course configuration changes must be validated by running scripts/validate_course_config.py before c |
| exact unit_text overlap | `v05_batch300_0046` | `v05_batch300_0046` | Add the new data science course configuration under config/courses/ds101.yaml with the updated prere |
| exact unit_text overlap | `v05_batch300_0047` | `v05_batch300_0047` | Build the release candidate for all three platforms and run the certification test suite. |
| exact unit_text overlap | `v05_batch300_0047` | `v05_batch300_0047` | Upload the release build artifacts to the distribution server under builds/releases/YYYY-MM-DD/. |
| exact unit_text overlap | `v05_batch300_0047` | `v05_batch300_0047` | Notify the QA team that the release candidate is available for final manual testing. |
| exact unit_text overlap | `v05_batch300_0048` | `v05_batch300_0048` | The studybuddy project defines course completion as scoring 70% or above on all required quizzes and |
| exact unit_text overlap | `v05_batch300_0048` | `v05_batch300_0048` | Completion certificates are valid for 2 years from the date of issue for continuing education credit |
| exact unit_text overlap | `v05_batch300_0048` | `v05_batch300_0048` | Update the certificate validity text in the PDF template at templates/certificates/completion.html. |
| exact unit_text overlap | `v05_batch300_0049` | `v05_batch300_0049` | Integrate the orchestrator with the company SSO provider for user authentication using OIDC. |
| exact unit_text overlap | `v05_batch300_0049` | `v05_batch300_0049` | Write the OIDC callback handler in src/orchestrator/auth/oidc_handler.py. |
| exact unit_text overlap | `v05_batch300_0049` | `v05_batch300_0049` | Test the SSO integration with the staging identity provider before enabling it for production users. |
| exact unit_text overlap | `v05_batch300_0050` | `v05_batch300_0050` | The retry wrapper must spill retry state to disk when the in-memory buffer exceeds 100MB, using a tm |
| exact unit_text overlap | `v05_batch300_0050` | `v05_batch300_0050` | Add a disk-spill health check that alerts when the spill directory exceeds 80% of the allocated tmpf |
| exact unit_text overlap | `v05_batch300_0050` | `v05_batch300_0050` | My SSH key for the staging pipeline host is pipeline-stage-ed25519 — it should be in the secrets vau |
| exact unit_text overlap | `v05_batch300_0051` | `v05_batch300_0051` | The notification service must use adaptive batching: 30-second windows during peak hours (08:00-22:0 |
| exact unit_text overlap | `v05_batch300_0051` | `v05_batch300_0051` | Low-priority notifications (marketing, tips) must not delay high-priority notifications (alerts, syn |
| exact unit_text overlap | `v05_batch300_0051` | `v05_batch300_0051` | Run a 2-week A/B test comparing the adaptive batching against the fixed 2-minute window on 10% of us |
| exact unit_text overlap | `v05_batch300_0052` | `v05_batch300_0052` | The aggregator must hash customer names and account IDs with SHA-256 before writing them to daily_ag |
| exact unit_text overlap | `v05_batch300_0052` | `v05_batch300_0052` | All finboard services must include a data-retention label on every log line: retention_30d, retentio |
| exact unit_text overlap | `v05_batch300_0052` | `v05_batch300_0052` | Run the anonymization migration on a staging clone of the production DB and verify hashed values mat |
| exact unit_text overlap | `v05_batch300_0053` | `v05_batch300_0053` | When the pricing service detects a 429 rate-limit response from an airline API, it must switch to ca |
| exact unit_text overlap | `v05_batch300_0053` | `v05_batch300_0053` | Document the rate-limit backpressure strategy in docs/pricing/rate_limit_handling.md with per-airlin |
| exact unit_text overlap | `v05_batch300_0053` | `v05_batch300_0053` | Add a rate-limit dashboard widget to the pricing monitoring page showing per-airline 429 counts. |
| exact unit_text overlap | `v05_batch300_0054` | `v05_batch300_0054` | Every grade change must insert a row into grade_audit with old_grade, new_grade, changed_by, change_ |
| exact unit_text overlap | `v05_batch300_0054` | `v05_batch300_0054` | Store the grade_audit table migration as an append-only log in db/migrations/grading/audit/ with one |
| exact unit_text overlap | `v05_batch300_0054` | `v05_batch300_0054` | Write a quarterly audit report query that lists all grade changes grouped by course and instructor. |
| exact unit_text overlap | `v05_batch300_0055` | `v05_batch300_0055` | The build system must cache compiled shader binaries keyed by source file hash and platform target.  |
| exact unit_text overlap | `v05_batch300_0055` | `v05_batch300_0055` | The shader cache must live under build/cache/shaders/{platform}/ and survive clean builds unless the |
| exact unit_text overlap | `v05_batch300_0055` | `v05_batch300_0055` | Benchmark the full build with and without shader caching on Windows and PS5 targets before the next  |
| exact unit_text overlap | `v05_batch300_0056` | `v05_batch300_0056` | Extend idempotency key enforcement to all mutating order endpoints: create, update_status, add_item, |
| exact unit_text overlap | `v05_batch300_0056` | `v05_batch300_0056` | The order service must reject duplicate idempotency keys with a 409 Conflict response containing the |
| exact unit_text overlap | `v05_batch300_0056` | `v05_batch300_0056` | Update the idempotency documentation at docs/orders/idempotency.md to list all protected endpoints a |
| exact unit_text overlap | `v05_batch300_0057` | `v05_batch300_0057` | The query engine must prepend a WHERE tenant_id = :current_tenant clause to every user-initiated que |
| exact unit_text overlap | `v05_batch300_0057` | `v05_batch300_0057` | The databoard project categorically prohibits cross-tenant data access in any component; violating t |
| exact unit_text overlap | `v05_batch300_0057` | `v05_batch300_0057` | Add an integration test that attempts to access another tenant's data and verifies the query engine  |
| exact unit_text overlap | `v05_batch300_0058` | `v05_batch300_0058` | The routing service must escalate any ticket that has been unacknowledged for 80% of its SLA window: |
| exact unit_text overlap | `v05_batch300_0058` | `v05_batch300_0058` | Escalated tickets must be flagged with a visual indicator in the agent dashboard and sorted to the t |
| exact unit_text overlap | `v05_batch300_0058` | `v05_batch300_0058` | Run the SLA report weekly and compare breach rates before and after the escalation feature is deploy |
| exact unit_text overlap | `v05_batch300_0059` | `v05_batch300_0059` | The indexer must segment the inverted index by document version. The default search scope is the lat |
| exact unit_text overlap | `v05_batch300_0059` | `v05_batch300_0059` | Store versioned indexes under data/indexer/versions/{version_tag}/ with a symlink 'latest' pointing  |
| exact unit_text overlap | `v05_batch300_0059` | `v05_batch300_0059` | Rebuild all versioned indexes from scratch and validate that searches return only results from the s |
| exact unit_text overlap | `v05_batch300_0060` | `v05_batch300_0060` | The orchestrator must implement a circuit breaker per external service: open the circuit after 5 con |
| exact unit_text overlap | `v05_batch300_0060` | `v05_batch300_0060` | When a circuit is open, the orchestrator must mark affected workflow steps as deferred rather than f |
| exact unit_text overlap | `v05_batch300_0060` | `v05_batch300_0060` | Document the circuit breaker design in docs/orchestrator/circuit_breaker.md with a state diagram and |
| exact unit_text overlap | `v05_batch300_0061` | `v05_batch300_0061` | The quiz generator must use a spaced repetition algorithm (SM-2 variant) that schedules question rev |
| exact unit_text overlap | `v05_batch300_0061` | `v05_batch300_0061` | The spaced repetition schedule must be stored per student in a new table spaced_repetition_schedule  |
| exact unit_text overlap | `v05_batch300_0061` | `v05_batch300_0061` | I prefer daily quiz reminders at 08:00 local time with a maximum of 20 review questions per session. |
| exact unit_text overlap | `v05_batch300_0062` | `v05_batch300_0062` | The prompt builder must validate its own output before sending it to the model: check that every cur |
| exact unit_text overlap | `v05_batch300_0062` | `v05_batch300_0062` | If validation fails, the prompt builder must log the error to prompt_builder_errors.log and fall bac |
| exact unit_text overlap | `v05_batch300_0062` | `v05_batch300_0062` | Write a unit test that feeds the prompt builder a truncated candidate_memories list and verifies the |
| exact unit_text overlap | `v05_batch300_0063` | `v05_batch300_0063` | The orders service must tokenize payment information before any internal processing: replace the raw |
| exact unit_text overlap | `v05_batch300_0063` | `v05_batch300_0063` | The raw card number must never appear in any log line, even at DEBUG level. Use the token ID in all  |
| exact unit_text overlap | `v05_batch300_0063` | `v05_batch300_0063` | Remember to rotate the PSP API key before the next PCI audit — the current key expires in 30 days. |
| exact unit_text overlap | `v05_batch300_0064` | `v05_batch300_0064` | Tickets can only be merged within 72 hours of the newer ticket's creation. After 72 hours, the merge |
| exact unit_text overlap | `v05_batch300_0064` | `v05_batch300_0064` | The 72-hour merge deadline must be configurable per ticket category in config/ticketing/merge_rules. |
| exact unit_text overlap | `v05_batch300_0064` | `v05_batch300_0064` | Audit last month's ticket merges and identify any that would have been blocked by the 72-hour rule f |
| exact unit_text overlap | `v05_batch300_0065` | `v05_batch300_0065` | Add a booking hold feature: when a user selects flights but has not yet paid, hold the seats for 20  |
| exact unit_text overlap | `v05_batch300_0065` | `v05_batch300_0065` | The hold must prevent other users from booking the same seats during the hold window. Expired holds  |
| exact unit_text overlap | `v05_batch300_0065` | `v05_batch300_0065` | Deploy the booking hold feature behind a feature flag and enable it for 5% of users initially. |
| exact unit_text overlap | `v05_batch300_0066` | `v05_batch300_0066` | The dungeon-tools project will support localization for EFIGS languages (English, French, Italian, G |
| exact unit_text overlap | `v05_batch300_0066` | `v05_batch300_0066` | Localized string files must live under assets/strings/{locale}/ with the same filename as the Englis |
| exact unit_text overlap | `v05_batch300_0066` | `v05_batch300_0066` | The build system must validate that all locale directories have the same set of JSON files as the En |
| exact unit_text overlap | `v05_batch300_0067` | `v05_batch300_0067` | The DLQ must automatically purge records older than 90 days. Records that have been manually inspect |
| exact unit_text overlap | `v05_batch300_0067` | `v05_batch300_0067` | Add a DLQ replay feature: an operator can replay a resolved DLQ record back into the original pipeli |
| exact unit_text overlap | `v05_batch300_0067` | `v05_batch300_0067` | Write a daily DLQ health report that shows count by stage, age distribution, and resolved vs unresol |
| exact unit_text overlap | `v05_batch300_0068` | `v05_batch300_0068` | Replace the single-response model with cursor-based pagination: each response returns up to 1,000 ro |
| exact unit_text overlap | `v05_batch300_0068` | `v05_batch300_0068` | Cursors must be opaque strings (base64-encoded) that encode the query ID, last row offset, and an HM |
| exact unit_text overlap | `v05_batch300_0068` | `v05_batch300_0068` | Update the visualizer to use the new pagination API for queries returning more than 500 rows. |
| exact unit_text overlap | `v05_batch300_0069` | `v05_batch300_0069` | Add a freshness decay factor to the search ranking: documents modified within the last 30 days get a |
| exact unit_text overlap | `v05_batch300_0069` | `v05_batch300_0069` | The freshness decay parameters must be tunable via config/search/freshness.yaml with keys boost_wind |
| exact unit_text overlap | `v05_batch300_0069` | `v05_batch300_0069` | Reindex all documents to populate the last_modified timestamp for the freshness calculation. |
| exact unit_text overlap | `v05_batch300_0070` | `v05_batch300_0070` | The sync queue database must be encrypted at rest with AES-256-GCM. The encryption key must be deriv |
| exact unit_text overlap | `v05_batch300_0070` | `v05_batch300_0070` | The encryption must be transparent to the sync module: the DAO layer must handle encryption/decrypti |
| exact unit_text overlap | `v05_batch300_0070` | `v05_batch300_0070` | The device keystore alias for the sync queue encryption key is fieldapp_sync_queue_key_v1. |
| exact unit_text overlap | `v05_batch300_0071` | `v05_batch300_0071` | The finboard project disaster recovery targets are: RPO of 1 hour (transaction logs shipped continuo |
| exact unit_text overlap | `v05_batch300_0071` | `v05_batch300_0071` | All finboard services must support graceful degradation during DR failover: the dashboard must show  |
| exact unit_text overlap | `v05_batch300_0071` | `v05_batch300_0071` | Conduct a disaster recovery drill within the next 30 days simulating a complete primary-region outag |
| exact unit_text overlap | `v05_batch300_0072` | `v05_batch300_0072` | Submissions with a similarity score above 60% must be automatically blocked from grading and require |
| exact unit_text overlap | `v05_batch300_0072` | `v05_batch300_0072` | The plagiarism detection thresholds (40% flag, 60% block) must be configurable per course in config/ |
| exact unit_text overlap | `v05_batch300_0072` | `v05_batch300_0072` | Generate a plagiarism report for the current semester showing the distribution of similarity scores  |
| exact unit_text overlap | `v05_batch300_0073` | `v05_batch300_0073` | Workflow definitions must be versioned: each workflow YAML file must include a version field (semver |
| exact unit_text overlap | `v05_batch300_0073` | `v05_batch300_0073` | Running workflow instances must continue using the version they started with. A running instance mus |
| exact unit_text overlap | `v05_batch300_0073` | `v05_batch300_0073` | Add a workflow version history page to the admin dashboard showing the last 10 versions of each work |
| exact unit_text overlap | `v05_batch300_0074` | `v05_batch300_0074` | Add a user data export endpoint that generates a JSON file containing all student progress data, qui |
| exact unit_text overlap | `v05_batch300_0074` | `v05_batch300_0074` | Data exports must be encrypted with a one-time download link that expires after 7 days. The link mus |
| exact unit_text overlap | `v05_batch300_0074` | `v05_batch300_0074` | Store the user's verified email address for GDPR exports in the user_settings table under the gdpr_e |
| exact unit_text overlap | `v05_batch300_0075` | `v05_batch300_0075` | If the user denies camera permission on first request, the app must show an educational screen expla |
| exact unit_text overlap | `v05_batch300_0075` | `v05_batch300_0075` | If the user denies camera permission twice, the app must not show the educational screen again for 3 |
| exact unit_text overlap | `v05_batch300_0075` | `v05_batch300_0075` | The camera module must never crash or freeze when launched without permission — it must show the edu |
| exact unit_text overlap | `v05_batch300_0076` | `v05_batch300_0076` | Add an asset validation gate to the CI pipeline that runs before the build step. The gate must run s |
| exact unit_text overlap | `v05_batch300_0076` | `v05_batch300_0076` | The asset validation CI step must run in parallel for PC, PS5, and Switch platform targets using mat |
| exact unit_text overlap | `v05_batch300_0076` | `v05_batch300_0076` | Configure the CI pipeline at .github/workflows/build.yml to add the validate_assets job with a 15-mi |
| exact unit_text overlap | `v05_batch300_0077` | `v05_batch300_0077` | When the exchange rate API is unavailable, the pricing service must fall back to the cached rate if  |
| exact unit_text overlap | `v05_batch300_0077` | `v05_batch300_0077` | The warning banner must state the currency, the conversion rate source, and a timestamp of when the  |
| exact unit_text overlap | `v05_batch300_0077` | `v05_batch300_0077` | Add a 'force refresh' button in the pricing admin panel that clears the exchange rate cache and fetc |
| exact unit_text overlap | `v05_batch300_0078` | `v05_batch300_0078` | The docs-assistant project must support the current and previous major API version concurrently. v1  |
| exact unit_text overlap | `v05_batch300_0078` | `v05_batch300_0078` | Deprecated endpoints must return a Sunset HTTP header with the retirement date in ISO 8601 format. A |
| exact unit_text overlap | `v05_batch300_0078` | `v05_batch300_0078` | Add the v1 deprecation notices to all current v1 endpoints and document the retirement timeline in d |
| exact unit_text overlap | `v05_batch300_0079` | `v05_batch300_0079` | All export files must follow the naming convention: {export_type}/{year}/{month}/{day}/{export_type} |
| exact unit_text overlap | `v05_batch300_0079` | `v05_batch300_0079` | The export job must validate the output filename against the convention regex before uploading. Mism |
| exact unit_text overlap | `v05_batch300_0079` | `v05_batch300_0079` | Update docs/export/s3_layout.md to reflect the new naming convention and add a filename examples tab |
| exact unit_text overlap | `v05_batch300_0080` | `v05_batch300_0080` | The routing service must factor customer sentiment into assignment priority: tickets with sentiment  |
| exact unit_text overlap | `v05_batch300_0080` | `v05_batch300_0080` | If the NLP sentiment service is unavailable, the routing service must fall back to keyword-based urg |
| exact unit_text overlap | `v05_batch300_0080` | `v05_batch300_0080` | I prefer ticket queues sorted by sentiment (most negative first) rather than by creation time. |
| exact unit_text overlap | `v05_batch300_0081` | `v05_batch300_0081` | When a cart reservation expires and stock is released, the inventory service must send a push notifi |
| exact unit_text overlap | `v05_batch300_0081` | `v05_batch300_0081` | The reservation expiry notification must include the product name, the quantity that was reserved, a |
| exact unit_text overlap | `v05_batch300_0081` | `v05_batch300_0081` | Measure the conversion rate of reservation-expiry notifications (users who re-add the item within 24 |
| exact unit_text overlap | `v05_batch300_0082` | `v05_batch300_0082` | When a scheduled report fails to generate, the scheduler must send a failure notification to the rep |
| exact unit_text overlap | `v05_batch300_0082` | `v05_batch300_0082` | The scheduler must retry failed reports once after 10 minutes. If the retry also fails, it must not  |
| exact unit_text overlap | `v05_batch300_0082` | `v05_batch300_0082` | Add a scheduler health dashboard showing the last 24 hours of report runs with success/failure count |
| exact unit_text overlap | `v05_batch300_0083` | `v05_batch300_0083` | Allow controlled overbooking up to 110% of course capacity for courses where historical drop rates e |
| exact unit_text overlap | `v05_batch300_0083` | `v05_batch300_0083` | If a provisionally enrolled student does not receive a confirmed seat within 7 days of the course st |
| exact unit_text overlap | `v05_batch300_0083` | `v05_batch300_0083` | Set overbooking_allowed to true in config/courses/capacity.yaml for the 5 courses with the highest h |
| exact unit_text overlap | `v05_batch300_0084` | `v05_batch300_0084` | The aggregator must ingest transaction data from both the payment processor and the bank settlement  |
| exact unit_text overlap | `v05_batch300_0084` | `v05_batch300_0084` | Unreconciled transactions must be held in a pending_reconciliation table and must not appear in fina |
| exact unit_text overlap | `v05_batch300_0084` | `v05_batch300_0084` | Write the daily reconciliation report query that identifies all unreconciled transactions older than |
| exact unit_text overlap | `v05_batch300_0085` | `v05_batch300_0085` | The build system must automatically sign release build binaries as the final step of the build pipel |
| exact unit_text overlap | `v05_batch300_0085` | `v05_batch300_0085` | Code signing must use the platform-specific format: Authenticode for Windows, codesign for macOS, an |
| exact unit_text overlap | `v05_batch300_0085` | `v05_batch300_0085` | Verify the signature on every release build artifact by running scripts/verify_signature.sh before u |
| exact unit_text overlap | `v05_batch300_0086` | `v05_batch300_0086` | The sync module must request location permission separately from camera permission with a clear expl |
| exact unit_text overlap | `v05_batch300_0086` | `v05_batch300_0086` | If the user denies location permission, the app must still function fully without location tagging.  |
| exact unit_text overlap | `v05_batch300_0086` | `v05_batch300_0086` | Add a privacy dashboard screen where users can view all stored location data points and delete them  |
| exact unit_text overlap | `v05_batch300_0087` | `v05_batch300_0087` | Every workflow step must have a timeout. Default timeout is 300 seconds. Steps can override this wit |
| exact unit_text overlap | `v05_batch300_0087` | `v05_batch300_0087` | A timed_out step must be retried if the step definition has retry_on_timeout set to true (default: f |
| exact unit_text overlap | `v05_batch300_0087` | `v05_batch300_0087` | Add a timeout_seconds value to every existing step definition that calls an external API, starting w |
| exact unit_text overlap | `v05_batch300_0088` | `v05_batch300_0088` | The quiz generator must adapt question difficulty based on the student's recent performance: if the  |
| exact unit_text overlap | `v05_batch300_0088` | `v05_batch300_0088` | Adaptive difficulty must have guardrails: a student must not receive only hard questions even with p |
| exact unit_text overlap | `v05_batch300_0088` | `v05_batch300_0088` | I prefer quizzes where difficulty ramps up gradually within a session — start with 2 easy warm-up qu |
| exact unit_text overlap | `v05_batch300_0089` | `v05_batch300_0089` | The case validator must detect cross-split leakage: when validating a file tagged as train, dev, or  |
| exact unit_text overlap | `v05_batch300_0089` | `v05_batch300_0089` | The leakage check must use normalized text comparison (lowercase, whitespace-collapsed) to detect ne |
| exact unit_text overlap | `v05_batch300_0089` | `v05_batch300_0089` | Add a --splits argument to validate_jsonl_file() that accepts paths to the other split files for cro |
| exact unit_text overlap | `v05_batch300_0090` | `v05_batch300_0090` | The search service must enforce per-user rate limiting: 100 requests per minute for authenticated us |
| exact unit_text overlap | `v05_batch300_0090` | `v05_batch300_0090` | Rate limit counters must be stored in Redis with a sliding window algorithm, not a fixed window, to  |
| exact unit_text overlap | `v05_batch300_0090` | `v05_batch300_0090` | Add the search rate limit rules to config/gateway/rate_limits.yaml under a new search section. |
| exact unit_text overlap | `v05_batch300_0091` | `v05_batch300_0091` | The ticketing service must integrate an ML-based category predictor that suggests up to 2 categories |
| exact unit_text overlap | `v05_batch300_0091` | `v05_batch300_0091` | If the ML model confidence is below 70% for all categories, the service must not show any suggestion |
| exact unit_text overlap | `v05_batch300_0091` | `v05_batch300_0091` | The ML model must be retrained weekly on the last 90 days of agent-categorized tickets and must neve |
| exact unit_text overlap | `v05_batch300_0092` | `v05_batch300_0092` | The orders service must split a single order into multiple sub-orders when items are available in di |
| exact unit_text overlap | `v05_batch300_0092` | `v05_batch300_0092` | Order splitting must minimize the number of sub-orders: prefer warehouse assignments that consolidat |
| exact unit_text overlap | `v05_batch300_0092` | `v05_batch300_0092` | Split orders must preserve the original order total — shipping costs must be recalculated per sub-or |
| exact unit_text overlap | `v05_batch300_0093` | `v05_batch300_0093` | The pipeline must implement backpressure: each stage has an output buffer of configurable size. When |
| exact unit_text overlap | `v05_batch300_0093` | `v05_batch300_0093` | A backpressure event must be logged with the stage name, buffer size at the time of blocking, and du |
| exact unit_text overlap | `v05_batch300_0093` | `v05_batch300_0093` | Set the default per-stage buffer capacity to 10,000 records in config/pipeline/buffers.yaml and add  |
| exact unit_text overlap | `v05_batch300_0094` | `v05_batch300_0094` | The alert_history table must be made append-only. The database user used by the alerts service must  |
| exact unit_text overlap | `v05_batch300_0094` | `v05_batch300_0094` | Any attempt to modify or delete alert history records must be logged to a separate audit_violation_a |
| exact unit_text overlap | `v05_batch300_0094` | `v05_batch300_0094` | Run a one-time script to lock the alert_history table: revoke UPDATE/DELETE for the alerts service u |
| exact unit_text overlap | `v05_batch300_0095` | `v05_batch300_0095` | At booking time, the pricing service must check the competitor_prices table for the same route, date |
| exact unit_text overlap | `v05_batch300_0095` | `v05_batch300_0095` | If a customer submits a price match claim after booking, the service must verify the claim against t |
| exact unit_text overlap | `v05_batch300_0095` | `v05_batch300_0095` | Add a price match claim form to the booking management page with fields for competitor name, URL, an |
| exact unit_text overlap | `v05_batch300_0096` | `v05_batch300_0096` | The eval_runner must auto-detect the model's output format by trying the parser in DSL mode first, t |
| exact unit_text overlap | `v05_batch300_0096` | `v05_batch300_0096` | If the model output cannot be parsed in any supported format, the eval_runner must record it as a pa |
| exact unit_text overlap | `v05_batch300_0096` | `v05_batch300_0096` | I prefer evaluation reports that include a format distribution pie chart (DSL vs JSON vs parse-failu |
| exact unit_text overlap | `v05_batch300_0097` | `v05_batch300_0097` | The orders service must send a cart abandonment email 2 hours after the user's last cart activity if |
| exact unit_text overlap | `v05_batch300_0097` | `v05_batch300_0097` | Cart abandonment emails must be suppressed for users who have opted out of marketing emails, but a s |
| exact unit_text overlap | `v05_batch300_0097` | `v05_batch300_0097` | Create the cart abandonment email template at templates/email/transactions/cart_abandoned.html with  |
| exact unit_text overlap | `v05_batch300_0098` | `v05_batch300_0098` | Every exported PDF report must include a diagonal watermark with the recipient's email address and t |
| exact unit_text overlap | `v05_batch300_0098` | `v05_batch300_0098` | If the report contains data classified as restricted (per the project's data governance policy), the |
| exact unit_text overlap | `v05_batch300_0098` | `v05_batch300_0098` | Update the scheduler's PDF generation code in src/scheduler/pdf_renderer.py to apply the watermark l |
| exact unit_text overlap | `v05_batch300_0099` | `v05_batch300_0099` | The sync module must process the offline queue by priority: CRITICAL (location updates, SOS alerts)  |
| exact unit_text overlap | `v05_batch300_0099` | `v05_batch300_0099` | A CRITICAL entry must never wait behind NORMAL entries. If a CRITICAL entry arrives while NORMAL ent |
| exact unit_text overlap | `v05_batch300_0099` | `v05_batch300_0099` | Add a priority column to the sync_queue table with values CRITICAL, HIGH, and NORMAL. Default is NOR |
| exact unit_text overlap | `v05_batch300_0100` | `v05_batch300_0100` | Add a prerequisite waiver workflow: a student can request a waiver by submitting a written justifica |
| exact unit_text overlap | `v05_batch300_0100` | `v05_batch300_0100` | If a waiver is approved, the enrollment service must bypass the prerequisite check for that student  |
| exact unit_text overlap | `v05_batch300_0100` | `v05_batch300_0100` | Approved waivers must be recorded in a prerequisite_waivers table with student_id, course_id, waived |
| exact unit_text overlap | `v05_batch500_0001` | `v05_batch500_0001` | The ticket router must route billing-related tickets to agents with the billing_certified skill tag, |
| exact unit_text overlap | `v05_batch500_0001` | `v05_batch500_0001` | Update the agent skill matrix to include the new billing_certified tag for 5 agents. |
| exact unit_text overlap | `v05_batch500_0002` | `v05_batch500_0002` | All metricboard services must retain query history logs for a minimum of 90 days before archival to  |
| exact unit_text overlap | `v05_batch500_0002` | `v05_batch500_0002` | The retention policy applies uniformly to the query engine, alert manager, and report scheduler serv |
| exact unit_text overlap | `v05_batch500_0002` | `v05_batch500_0002` | For this quarter, add the cold storage archival job to the data pipeline so logs older than 90 days  |
| exact unit_text overlap | `v05_batch500_0003` | `v05_batch500_0003` | The appointment scheduler must reject bookings that overlap with an existing confirmed appointment f |
| exact unit_text overlap | `v05_batch500_0003` | `v05_batch500_0003` | Add a provider availability cache that refreshes every 30 seconds from the scheduling database. |
| exact unit_text overlap | `v05_batch500_0004` | `v05_batch500_0004` | The inventory sync service must trigger a low-stock alert when any SKU quantity falls below its conf |
| exact unit_text overlap | `v05_batch500_0004` | `v05_batch500_0004` | Set the reorder point for SKU BX-4491 to 50 units and update the alert threshold config. |
| exact unit_text overlap | `v05_batch500_0005` | `v05_batch500_0005` | The contract parser must flag any clause containing the phrase 'indemnify and hold harmless' for man |
| exact unit_text overlap | `v05_batch500_0005` | `v05_batch500_0005` | Add the indemnification flag to the clause metadata schema in the parser output. |
| exact unit_text overlap | `v05_batch500_0006` | `v05_batch500_0006` | The render farm must support a priority queue where jobs tagged 'client_review' are scheduled before |
| exact unit_text overlap | `v05_batch500_0006` | `v05_batch500_0006` | Add the priority field to the job submission API and update the scheduler to read it. |
| exact unit_text overlap | `v05_batch500_0007` | `v05_batch500_0007` | The ingestion service must strip euro currency symbols from amount fields before casting to numeric, |
| exact unit_text overlap | `v05_batch500_0007` | `v05_batch500_0007` | Add a currency symbol stripping step to the CSV preprocessing stage before schema validation. |
| exact unit_text overlap | `v05_batch500_0008` | `v05_batch500_0008` | The catalog search must boost exact phrase matches by a factor of 3.0 over individual term matches w |
| exact unit_text overlap | `v05_batch500_0008` | `v05_batch500_0008` | Run an A/B test comparing the new phrase boost against the current BM25-only baseline on 10% of traf |
| exact unit_text overlap | `v05_batch500_0009` | `v05_batch500_0009` | The SFT renderer must support a configurable system prompt template that can be swapped per experime |
| exact unit_text overlap | `v05_batch500_0009` | `v05_batch500_0009` | Extract the system prompt into a separate template file under prompts/v05/system_prompt.txt. |
| exact unit_text overlap | `v05_batch500_0010` | `v05_batch500_0010` | I prefer all financial charts to display currency values in my local currency (EUR) with the exchang |
| exact unit_text overlap | `v05_batch500_0010` | `v05_batch500_0010` | I want to receive portfolio summary emails weekly on Friday at 08:00 CET instead of daily. |
| exact unit_text overlap | `v05_batch500_0010` | `v05_batch500_0010` | My corporate email for finboard notifications is trader-007@investco.example.com. |
| exact unit_text overlap | `v05_batch500_0011` | `v05_batch500_0011` | I prefer to see tickets sorted by priority first, then by wait time, with high-priority tickets high |
| exact unit_text overlap | `v05_batch500_0011` | `v05_batch500_0011` | When I ask for a code review, prioritize API contract violations and missing error handling over sty |
| exact unit_text overlap | `v05_batch500_0011` | `v05_batch500_0011` | My agent ID is AG-4429 and my shift is 14:00-22:00 UTC; update my schedule accordingly. |
| exact unit_text overlap | `v05_batch500_0012` | `v05_batch500_0012` | The location tracker must trigger a geofence entry alert when the device enters any customer site po |
| exact unit_text overlap | `v05_batch500_0012` | `v05_batch500_0012` | The user's home address is 5678 Oak Lane, Springfield, IL 62701 — use this to create a home geofence |
| exact unit_text overlap | `v05_batch500_0012` | `v05_batch500_0012` | Add geofence alert logging to the analytics pipeline for measuring alert accuracy. |
| exact unit_text overlap | `v05_batch500_0013` | `v05_batch500_0013` | The version manager must compute a semantic diff between two documentation versions, highlighting ad |
| exact unit_text overlap | `v05_batch500_0013` | `v05_batch500_0013` | Add a diff endpoint to the version manager API that accepts two version tags and returns a structure |
| exact unit_text overlap | `v05_batch500_0014` | `v05_batch500_0014` | The step executor must support conditional branching where a step's output field is compared against |
| exact unit_text overlap | `v05_batch500_0014` | `v05_batch500_0014` | Add branch condition evaluation to the step executor's transition logic before the next workflow rel |
| exact unit_text overlap | `v05_batch500_0015` | `v05_batch500_0015` | All voyager customer-facing services including booking, pricing, and check-in must support screen re |
| exact unit_text overlap | `v05_batch500_0015` | `v05_batch500_0015` | The voyager project does not support real-time currency conversion for display prices; all prices ar |
| exact unit_text overlap | `v05_batch500_0015` | `v05_batch500_0015` | Schedule accessibility audits for the booking and check-in flows before the Q3 compliance deadline. |
| exact unit_text overlap | `v05_batch500_0016` | `v05_batch500_0016` | The assessment engine must adjust question difficulty dynamically based on the learner's running acc |
| exact unit_text overlap | `v05_batch500_0016` | `v05_batch500_0016` | Add the dynamic difficulty adjustment module as a middleware between question selection and presenta |
| exact unit_text overlap | `v05_batch500_0017` | `v05_batch500_0017` | The physics engine must support destructible objects by replacing a rigid body with a cluster of sma |
| exact unit_text overlap | `v05_batch500_0017` | `v05_batch500_0017` | Add the damage accumulation property to the physics material definition schema. |
| exact unit_text overlap | `v05_batch500_0018` | `v05_batch500_0018` | The quality checker must run a Z-score anomaly detection on numeric columns, flagging any value more |
| exact unit_text overlap | `v05_batch500_0018` | `v05_batch500_0018` | Add the Z-score anomaly detector as a new check type in the quality checker's check registry. |
| exact unit_text overlap | `v05_batch500_0019` | `v05_batch500_0019` | The data importer must support fuzzy column name matching when the CSV header does not exactly match |
| exact unit_text overlap | `v05_batch500_0019` | `v05_batch500_0019` | Build the fuzzy matching UI in the import wizard so users can review and confirm suggested mappings. |
| exact unit_text overlap | `v05_batch500_0020` | `v05_batch500_0020` | The quiz generator must produce plausible distractors by selecting sentences from the same topic tha |
| exact unit_text overlap | `v05_batch500_0020` | `v05_batch500_0020` | Replace the random-distractor logic with the new semantic-distractor generator in the quiz pipeline. |
| exact unit_text overlap | `v05_batch500_0021` | `v05_batch500_0021` | The route optimizer must incorporate real-time traffic data from the internal traffic feed to dynami |
| exact unit_text overlap | `v05_batch500_0021` | `v05_batch500_0021` | Add the traffic feed integration module to the route optimizer's data ingestion pipeline. |
| exact unit_text overlap | `v05_batch500_0022` | `v05_batch500_0022` | The obligation tracker must send reminder notifications 30, 14, and 3 days before each obligation de |
| exact unit_text overlap | `v05_batch500_0022` | `v05_batch500_0022` | Add the reminder schedule configuration to the obligation tracker's notification settings. |
| exact unit_text overlap | `v05_batch500_0023` | `v05_batch500_0023` | The appointment scheduler must support a telehealth appointment type that reserves a video session s |
| exact unit_text overlap | `v05_batch500_0023` | `v05_batch500_0023` | Add the telehealth appointment type to the scheduler's booking API and validate MedLink provider ava |
| exact unit_text overlap | `v05_batch500_0024` | `v05_batch500_0024` | The asset compiler must generate mipmap chains for each texture atlas level, downscaling by factors  |
| exact unit_text overlap | `v05_batch500_0024` | `v05_batch500_0024` | Store the mipmap generation parameters in config/asset_compiler/mipmap.yaml so they can be tuned per |
| exact unit_text overlap | `v05_batch500_0025` | `v05_batch500_0025` | The payment gateway must support the Klarna BNPL provider by implementing the installment plan selec |
| exact unit_text overlap | `v05_batch500_0025` | `v05_batch500_0025` | Add the Klarna adapter class in src/payment/adapters/klarna_adapter.py implementing the PaymentProvi |
| exact unit_text overlap | `v05_batch500_0026` | `v05_batch500_0026` | The trigger manager must accept incoming webhook POST requests, validate the HMAC-SHA256 signature a |
| exact unit_text overlap | `v05_batch500_0026` | `v05_batch500_0026` | Add the webhook secret configuration to config/triggers/secrets.yaml with per-workflow secret keys. |
| exact unit_text overlap | `v05_batch500_0027` | `v05_batch500_0027` | All finboard services in staging must use the staging database cluster at db-stage.finboard.internal |
| exact unit_text overlap | `v05_batch500_0027` | `v05_batch500_0027` | The staging environment configuration is managed in k8s/overlays/staging/configmap.yaml and applied  |
| exact unit_text overlap | `v05_batch500_0027` | `v05_batch500_0027` | Add resource limits to the staging deployment: 512Mi memory and 0.5 CPU per pod, with burst to 1Gi a |
| exact unit_text overlap | `v05_batch500_0028` | `v05_batch500_0028` | The loyalty engine must apply a points multiplier based on the member tier: Silver 1.0x, Gold 1.5x,  |
| exact unit_text overlap | `v05_batch500_0028` | `v05_batch500_0028` | The loyalty program must never allow point redemption for cash equivalents such as gift cards or sta |
| exact unit_text overlap | `v05_batch500_0029` | `v05_batch500_0029` | The sentiment analyzer must also detect urgency signals: phrases like 'urgent', 'as soon as possible |
| exact unit_text overlap | `v05_batch500_0029` | `v05_batch500_0029` | Add an urgency_score field to the sentiment output JSON and expose it in the agent dashboard. |
| exact unit_text overlap | `v05_batch500_0030` | `v05_batch500_0030` | The code linker must also parse documentation files for @code annotations that reference source file |
| exact unit_text overlap | `v05_batch500_0030` | `v05_batch500_0030` | Update the link database schema to add a link_direction column with values 'code_to_doc' and 'doc_to |
| exact unit_text overlap | `v05_batch500_0031` | `v05_batch500_0031` | The case generator must reject any generated case whose current_unit text is an exact duplicate of a |
| exact unit_text overlap | `v05_batch500_0031` | `v05_batch500_0031` | Add a semantic similarity check that flags cases whose unit texts have a cosine similarity above 0.8 |
| exact unit_text overlap | `v05_batch500_0032` | `v05_batch500_0032` | The chart renderer must support drill-down interactions: when a user clicks on an aggregate bar segm |
| exact unit_text overlap | `v05_batch500_0032` | `v05_batch500_0032` | Add the drill-down query template parameterization so each chart type can define its own detail quer |
| exact unit_text overlap | `v05_batch500_0033` | `v05_batch500_0033` | The CI pipeline must run Python linting with flake8 using the config at .flake8, unit tests with pyt |
| exact unit_text overlap | `v05_batch500_0033` | `v05_batch500_0033` | Test coverage reports are written to ci_reports/coverage/ and must show at least 80% line coverage f |
| exact unit_text overlap | `v05_batch500_0033` | `v05_batch500_0033` | Add a CI step that validates all YAML configuration files against their JSON schemas before the test |
| exact unit_text overlap | `v05_batch500_0034` | `v05_batch500_0034` | The plagiarism checker must also compare new submissions against all previous submissions in the sam |
| exact unit_text overlap | `v05_batch500_0034` | `v05_batch500_0034` | Add the cross-submission index to the plagiarism pipeline and schedule it to run nightly. |
| exact unit_text overlap | `v05_batch500_0035` | `v05_batch500_0035` | The dialogue system must incorporate an NPC emotion model where each NPC has an emotional state vect |
| exact unit_text overlap | `v05_batch500_0035` | `v05_batch500_0035` | Add emotion state fields to the NPC character schema and initialize them from the character definiti |
| exact unit_text overlap | `v05_batch500_0036` | `v05_batch500_0036` | The offline storage module must support a counter CRDT for numeric fields, merging concurrent increm |
| exact unit_text overlap | `v05_batch500_0036` | `v05_batch500_0036` | Implement the counter CRDT merge function and add it to the sync conflict resolver as the default st |
| exact unit_text overlap | `v05_batch500_0037` | `v05_batch500_0037` | The schema registry must validate that new schema versions are backward-compatible before accepting  |
| exact unit_text overlap | `v05_batch500_0037` | `v05_batch500_0037` | Add the compatibility check step to the schema registration API and reject registrations that fail t |
| exact unit_text overlap | `v05_batch500_0038` | `v05_batch500_0038` | Database migrations must be applied in order using: alembic upgrade head, and must be run against a  |
| exact unit_text overlap | `v05_batch500_0038` | `v05_batch500_0038` | The migration history table is alembic_version and must never be manually modified; all schema chang |
| exact unit_text overlap | `v05_batch500_0038` | `v05_batch500_0038` | Write the PostgreSQL 16 migration plan including the pg_upgrade checklist and rollback procedure. |
| exact unit_text overlap | `v05_batch500_0039` | `v05_batch500_0039` | The demand forecaster must decompose the demand signal into trend, seasonal, and residual components |
| exact unit_text overlap | `v05_batch500_0039` | `v05_batch500_0039` | Add the STL decomposition module and replace the current moving average predictor. |
| exact unit_text overlap | `v05_batch500_0040` | `v05_batch500_0040` | The redaction engine must automatically detect and redact Social Security Numbers, dates of birth, a |
| exact unit_text overlap | `v05_batch500_0040` | `v05_batch500_0040` | Add an auto-redaction review step where detected PII is highlighted and requires attorney confirmati |
| exact unit_text overlap | `v05_batch500_0041` | `v05_batch500_0041` | The version control system must support named branches where each branch is a mutable pointer to a r |
| exact unit_text overlap | `v05_batch500_0041` | `v05_batch500_0041` | Add branch create, merge, and delete commands to the artisan CLI tool. |
| exact unit_text overlap | `v05_batch500_0042` | `v05_batch500_0042` | All shopengine services that store customer PII must implement a deletion endpoint that removes or a |
| exact unit_text overlap | `v05_batch500_0042` | `v05_batch500_0042` | The shopengine project must never share customer email addresses with third-party marketing services |
| exact unit_text overlap | `v05_batch500_0042` | `v05_batch500_0042` | Add GDPR erasure request tracking to the admin dashboard so the compliance team can monitor pending  |
| exact unit_text overlap | `v05_batch500_0043` | `v05_batch500_0043` | The progress tracker must estimate skill mastery using a Bayesian Knowledge Tracing model that updat |
| exact unit_text overlap | `v05_batch500_0043` | `v05_batch500_0043` | Implement the BKT model with the standard 4-parameter variant (guess, slip, initial, transit) using  |
| exact unit_text overlap | `v05_batch500_0044` | `v05_batch500_0044` | Every release must include a CHANGELOG.md entry under the new version heading, listing all merged PR |
| exact unit_text overlap | `v05_batch500_0044` | `v05_batch500_0044` | Release candidates must pass the full integration test suite at tests/integration/ before being prom |
| exact unit_text overlap | `v05_batch500_0044` | `v05_batch500_0044` | Automate the changelog generation using the script at scripts/generate_changelog.py that reads merge |
| exact unit_text overlap | `v05_batch500_0045` | `v05_batch500_0045` | The macros engine must support if/else conditions based on ticket fields: for example, if ticket.pri |
| exact unit_text overlap | `v05_batch500_0045` | `v05_batch500_0045` | Add the conditional block syntax to the macro YAML schema and update the macro renderer to evaluate  |
| exact unit_text overlap | `v05_batch500_0046` | `v05_batch500_0046` | The search index must support faceted filtering on document metadata: language, version, product, an |
| exact unit_text overlap | `v05_batch500_0046` | `v05_batch500_0046` | Add the facet aggregation pipeline to the search query handler and expose facet counts in the search |
| exact unit_text overlap | `v05_batch500_0047` | `v05_batch500_0047` | The fraud detector must track booking velocity per user account: if an account attempts more than 5  |
| exact unit_text overlap | `v05_batch500_0047` | `v05_batch500_0047` | Add the velocity tracking counter to the fraud detector's Redis cache with a 10-minute TTL per user. |
| exact unit_text overlap | `v05_batch500_0048` | `v05_batch500_0048` | The data validator must perform a cross-source reconciliation by comparing total positions per accou |
| exact unit_text overlap | `v05_batch500_0048` | `v05_batch500_0048` | Add the reconciliation check as a scheduled job that runs at 06:00 UTC before the daily report gener |
| exact unit_text overlap | `v05_batch500_0049` | `v05_batch500_0049` | The label auditor must flag cases where a unit begins with 'Add', 'Implement', or 'Build' but is lab |
| exact unit_text overlap | `v05_batch500_0049` | `v05_batch500_0049` | Add the action-verb detection regex to the label auditor's rule set and generate a warning report fo |
| exact unit_text overlap | `v05_batch500_0050` | `v05_batch500_0050` | The dashboard builder must support custom metric formulas where a widget's value is computed as an a |
| exact unit_text overlap | `v05_batch500_0050` | `v05_batch500_0050` | Add the formula parser that evaluates expressions with widget ID references and standard arithmetic  |
| exact unit_text overlap | `v05_batch500_0051` | `v05_batch500_0051` | The course builder must validate the prerequisite graph for cycles before publishing a course, rejec |
| exact unit_text overlap | `v05_batch500_0051` | `v05_batch500_0051` | Add cycle detection using depth-first search to the course validation pipeline. |
| exact unit_text overlap | `v05_batch500_0052` | `v05_batch500_0052` | The animation blender must apply two-bone inverse kinematics to character feet during locomotion ani |
| exact unit_text overlap | `v05_batch500_0052` | `v05_batch500_0052` | Add the IK solver as a post-processing step in the animation pipeline after the blend tree evaluatio |
| exact unit_text overlap | `v05_batch500_0053` | `v05_batch500_0053` | All helpdesk services must expose Prometheus metrics at :9090/metrics with the standard histogram bu |
| exact unit_text overlap | `v05_batch500_0053` | `v05_batch500_0053` | Alert rules for production are defined in prometheus/rules/alerts.yml: page on-call if the ticket AP |
| exact unit_text overlap | `v05_batch500_0053` | `v05_batch500_0053` | Add the alerting rules for the new chat-router service before it goes live in production next week. |
| exact unit_text overlap | `v05_batch500_0054` | `v05_batch500_0054` | The recommendation engine must add collaborative filtering using matrix factorization with 50 latent |
| exact unit_text overlap | `v05_batch500_0054` | `v05_batch500_0054` | Train the collaborative filtering model on the last 12 months of purchase data and evaluate with RMS |
| exact unit_text overlap | `v05_batch500_0055` | `v05_batch500_0055` | The partition manager must archive partitions to cold storage before dropping them, by exporting the |
| exact unit_text overlap | `v05_batch500_0055` | `v05_batch500_0055` | Add the archive-before-drop step to the partition retention job and verify archive integrity before  |
| exact unit_text overlap | `v05_batch500_0056` | `v05_batch500_0056` | The push notifier must group notifications by topic within a 30-minute window: instead of sending 5  |
| exact unit_text overlap | `v05_batch500_0056` | `v05_batch500_0056` | Add the notification grouping buffer that accumulates notifications per topic and flushes when the w |
| exact unit_text overlap | `v05_batch500_0057` | `v05_batch500_0057` | All new service code must have unit tests covering at least 85% of branches, verified by the coverag |
| exact unit_text overlap | `v05_batch500_0057` | `v05_batch500_0057` | Integration tests must use the test fixtures defined in tests/integration/conftest.py and clean up a |
| exact unit_text overlap | `v05_batch500_0057` | `v05_batch500_0057` | Add the test parallelization configuration to pytest.ini with 4 workers and the test group assignmen |
| exact unit_text overlap | `v05_batch500_0058` | `v05_batch500_0058` | The lab results processor must flag any result that falls outside its reference range as 'abnormal'  |
| exact unit_text overlap | `v05_batch500_0058` | `v05_batch500_0058` | Add the critical result notification that sends an SMS alert to the ordering provider when a critica |
| exact unit_text overlap | `v05_batch500_0059` | `v05_batch500_0059` | The warehouse allocator must optimize picking routes by grouping order lines by zone and sequencing  |
| exact unit_text overlap | `v05_batch500_0059` | `v05_batch500_0059` | Implement the zone-sequencing algorithm and integrate it with the existing order assignment pipeline |
| exact unit_text overlap | `v05_batch500_0060` | `v05_batch500_0060` | The expiry tracker must forecast renewal probability based on historical renewal rates by contract t |
| exact unit_text overlap | `v05_batch500_0060` | `v05_batch500_0060` | Add the renewal probability score to the contract dashboard and color-code contracts with low renewa |
| exact unit_text overlap | `v05_batch500_0061` | `v05_batch500_0061` | The export manager must support color profile conversion between sRGB, Adobe RGB, and Display P3, ap |
| exact unit_text overlap | `v05_batch500_0061` | `v05_batch500_0061` | Add the ICC profile embedding step so exported files include the color profile metadata in the file  |
| exact unit_text overlap | `v05_batch500_0062` | `v05_batch500_0062` | Configuration files must be validated against their JSON schemas at service startup, with schemas st |
| exact unit_text overlap | `v05_batch500_0062` | `v05_batch500_0062` | Secrets such as database passwords and API keys must never appear in config files; they must be load |
| exact unit_text overlap | `v05_batch500_0062` | `v05_batch500_0062` | I prefer learning materials organized by topic with clear prerequisites listed at the start of each  |
| exact unit_text overlap | `v05_batch500_0063` | `v05_batch500_0063` | The alert manager must support anomaly-based alerting where the trigger condition is 'value is outsi |
| exact unit_text overlap | `v05_batch500_0063` | `v05_batch500_0063` | Add the rolling statistics calculator that maintains a 168-hour window (7 days × 24 hours) for each  |
| exact unit_text overlap | `v05_batch500_0064` | `v05_batch500_0064` | The check-in service must automatically select the best available seat matching the user's preferenc |
| exact unit_text overlap | `v05_batch500_0064` | `v05_batch500_0064` | Add the seat preference scoring function that ranks available seats by proximity to the user's ideal |
| exact unit_text overlap | `v05_batch500_0065` | `v05_batch500_0065` | The Python virtual environment must be created at .venv/ and activated before running any project sc |
| exact unit_text overlap | `v05_batch500_0065` | `v05_batch500_0065` | Dependencies are installed with: pip install -r requirements.txt for production and pip install -r r |
| exact unit_text overlap | `v05_batch500_0065` | `v05_batch500_0065` | Update all dependency pins and test the training pipeline with the updated dependencies before the v |
| exact unit_text overlap | `v05_batch500_0066` | `v05_batch500_0066` | The knowledge base must score article effectiveness by tracking whether a ticket is resolved within  |
| exact unit_text overlap | `v05_batch500_0066` | `v05_batch500_0066` | Add the article resolution tracking that links help article IDs to ticket resolution events in the a |
| exact unit_text overlap | `v05_batch500_0067` | `v05_batch500_0067` | All Docker images built for production must be signed using: cosign sign --key cosign.key <image_tag |
| exact unit_text overlap | `v05_batch500_0067` | `v05_batch500_0067` | The image verification step in the deployment pipeline must run: cosign verify --key cosign.pub <ima |
| exact unit_text overlap | `v05_batch500_0067` | `v05_batch500_0067` | Add the Cosign signing and verification steps to the CI/CD pipeline configuration in .github/workflo |
| exact unit_text overlap | `v05_batch500_0068` | `v05_batch500_0068` | The translator must enforce glossary terms during translation by post-processing the MT output and r |
| exact unit_text overlap | `v05_batch500_0068` | `v05_batch500_0068` | Add the glossary post-processor as a pipeline step between MT inference and the final rendered page. |
| exact unit_text overlap | `v05_batch500_0069` | `v05_batch500_0069` | All shopengine services must validate JWT tokens against the central auth service on every request,  |
| exact unit_text overlap | `v05_batch500_0069` | `v05_batch500_0069` | The shopengine project categorically prohibits storing user passwords in any service database; only  |
| exact unit_text overlap | `v05_batch500_0069` | `v05_batch500_0069` | Migrate the legacy catalog service from session-based auth to JWT-based auth before the security aud |
| exact unit_text overlap | `v05_batch500_0070` | `v05_batch500_0070` | The training logger must compute and log the distribution of predicted STORE targets per epoch to de |
| exact unit_text overlap | `v05_batch500_0070` | `v05_batch500_0070` | Add the target distribution histogram to the TensorBoard logging callback. |
| exact unit_text overlap | `v05_batch500_0071` | `v05_batch500_0071` | All helpdesk services must mask customer PII in log output: names truncated to first initial, email  |
| exact unit_text overlap | `v05_batch500_0071` | `v05_batch500_0071` | The helpdesk project does not store customer payment information; all payment processing is handled  |
| exact unit_text overlap | `v05_batch500_0071` | `v05_batch500_0071` | Add PII masking to the ticket search index logs before the next compliance audit. |
| exact unit_text overlap | `v05_batch500_0072` | `v05_batch500_0072` | The query optimizer must estimate the cost of each query before execution by counting the number of  |
| exact unit_text overlap | `v05_batch500_0072` | `v05_batch500_0072` | Query execution schedules and off-peak window configurations are stored in config/query_optimizer/sc |
| exact unit_text overlap | `v05_batch500_0072` | `v05_batch500_0072` | Run the query cost estimator on the top 20 slowest queries from last week. |
| exact unit_text overlap | `v05_batch500_0073` | `v05_batch500_0073` | The billing coder must map diagnosis descriptions to ICD-10-CM codes using exact match on the SNOMED |
| exact unit_text overlap | `v05_batch500_0073` | `v05_batch500_0073` | The SNOMED-CT to ICD-10-CM crosswalk file is stored at data/coding/crosswalk_snomed_icd10.csv and up |
| exact unit_text overlap | `v05_batch500_0073` | `v05_batch500_0073` | The billing-coder currently uses the 2025 crosswalk; updating to the 2026 crosswalk is required befo |
| exact unit_text overlap | `v05_batch500_0074` | `v05_batch500_0074` | I prefer inventory reports grouped by warehouse first, then by product category, with low-stock item |
| exact unit_text overlap | `v05_batch500_0074` | `v05_batch500_0074` | When presenting supplier performance metrics, include the 3-month trend alongside the current value  |
| exact unit_text overlap | `v05_batch500_0074` | `v05_batch500_0074` | My work hours are 06:00-14:00 UTC; schedule all automated report deliveries within this window. |
| exact unit_text overlap | `v05_batch500_0075` | `v05_batch500_0075` | The risk scorer must evaluate each contract clause against a library of risky language patterns and  |
| exact unit_text overlap | `v05_batch500_0075` | `v05_batch500_0075` | Risk pattern definitions and score weights are stored in config/risk/patterns.yaml and reviewed quar |
| exact unit_text overlap | `v05_batch500_0075` | `v05_batch500_0075` | The risk scorer currently uses a static pattern library from 2025; adding the new 2026 regulatory ri |
| exact unit_text overlap | `v05_batch500_0076` | `v05_batch500_0076` | The font renderer must implement a font fallback chain: when a glyph is missing in the primary font, |
| exact unit_text overlap | `v05_batch500_0076` | `v05_batch500_0076` | Font fallback chain configurations per script are stored in config/fonts/fallback_chains.json. |
| exact unit_text overlap | `v05_batch500_0076` | `v05_batch500_0076` | The font renderer currently only supports Latin and CJK scripts; adding Arabic and Devanagari fallba |
| exact unit_text overlap | `v05_batch500_0077` | `v05_batch500_0077` | The crash reporter currently captures stack traces but does not include the last 50 application log  |
| exact unit_text overlap | `v05_batch500_0077` | `v05_batch500_0077` | Next, add a circular log buffer that keeps the last 200 log lines in memory and attaches them to cra |
| exact unit_text overlap | `v05_batch500_0077` | `v05_batch500_0077` | After the log buffer is implemented, add breadcrumb events for navigation and network calls. |
| exact unit_text overlap | `v05_batch500_0078` | `v05_batch500_0078` | All data-platform infrastructure must be defined in Terraform under terraform/<env>/ with separate s |
| exact unit_text overlap | `v05_batch500_0078` | `v05_batch500_0078` | The Terraform plan for each environment must be reviewed in the PR that modifies it; no direct terra |
| exact unit_text overlap | `v05_batch500_0078` | `v05_batch500_0078` | The current staging environment still has manually created resources from the initial setup; these m |
| exact unit_text overlap | `v05_batch500_0079` | `v05_batch500_0079` | The student dashboard currently shows enrolled courses and grades from the previous semester only. |
| exact unit_text overlap | `v05_batch500_0079` | `v05_batch500_0079` | Before the fall semester launch, add the course registration widget and the financial aid status pan |
| exact unit_text overlap | `v05_batch500_0079` | `v05_batch500_0079` | The registration widget should pull course availability from the enrollment service in real time. |
| exact unit_text overlap | `v05_batch500_0080` | `v05_batch500_0080` | The scheduler currently uses cron expressions for all workflow triggers, which causes delays of up t |
| exact unit_text overlap | `v05_batch500_0080` | `v05_batch500_0080` | Migrate the top 10 most frequent workflows to event-driven triggers using the message queue. |
| exact unit_text overlap | `v05_batch500_0080` | `v05_batch500_0080` | The remaining 40 low-frequency workflows can stay on cron until the next quarter. |
| exact unit_text overlap | `v05_batch500_0081` | `v05_batch500_0081` | The current full build takes 45 minutes, and console certification requires 3 clean builds per submi |
| exact unit_text overlap | `v05_batch500_0081` | `v05_batch500_0081` | For this certification round, add distributed shader compilation across the 4 build machines to redu |
| exact unit_text overlap | `v05_batch500_0081` | `v05_batch500_0081` | The build optimization is only needed for the certification submission; after passing, revert to the |
| exact unit_text overlap | `v05_batch500_0082` | `v05_batch500_0082` | All v0.5 batch JSONL files must be validated by the CI pipeline on every push using the command: pyt |
| exact unit_text overlap | `v05_batch500_0082` | `v05_batch500_0082` | CI validation reports should be written to ci_reports/v05/ with the naming pattern <batch>_validatio |
| exact unit_text overlap | `v05_batch500_0082` | `v05_batch500_0082` | The CI pipeline must fail the build if any case validation fails or if SFT assistant content does no |
| exact unit_text overlap | `v05_batch500_0083` | `v05_batch500_0083` | End-to-end tests must run against a Docker Compose environment defined in docker-compose.test.yaml,  |
| exact unit_text overlap | `v05_batch500_0083` | `v05_batch500_0083` | E2E test fixtures for the checkout flow are in tests/e2e/fixtures/checkout/ and use the Factory patt |
| exact unit_text overlap | `v05_batch500_0083` | `v05_batch500_0083` | All e2e tests must pass before merging to the main branch; the merge hook is configured in .github/w |
| exact unit_text overlap | `v05_batch500_0084` | `v05_batch500_0084` | The release process requires a CHANGELOG.md entry under the Unreleased section, then moved to the ve |
| exact unit_text overlap | `v05_batch500_0084` | `v05_batch500_0084` | Release tags must follow semantic versioning and be annotated with git tag -a v<major>.<minor>.<patc |
| exact unit_text overlap | `v05_batch500_0084` | `v05_batch500_0084` | The release Docker image is built from Dockerfile.release and pushed to the container registry with  |
| exact unit_text overlap | `v05_batch500_0085` | `v05_batch500_0085` | Deployments to staging happen automatically on merge to develop; deployments to production require m |
| exact unit_text overlap | `v05_batch500_0085` | `v05_batch500_0085` | The Kubernetes deployment manifests are in k8s/overlays/<env>/ and use Kustomize for environment-spe |
| exact unit_text overlap | `v05_batch500_0085` | `v05_batch500_0085` | Database migrations must be applied before deploying new application code; the migration runner imag |
| exact unit_text overlap | `v05_batch500_0086` | `v05_batch500_0086` | Prometheus metrics for all voyager services are exposed on port 9090 at the /metrics endpoint and sc |
| exact unit_text overlap | `v05_batch500_0086` | `v05_batch500_0086` | Grafana dashboards for the voyager project are stored in grafana/dashboards/ and imported via the Gr |
| exact unit_text overlap | `v05_batch500_0086` | `v05_batch500_0086` | Alert rules for production are defined in prometheus/rules/alerts.yml and must not be modified witho |
| exact unit_text overlap | `v05_batch500_0087` | `v05_batch500_0087` | All medflow services must encrypt data in transit using TLS 1.3 with cipher suites approved by the s |
| exact unit_text overlap | `v05_batch500_0087` | `v05_batch500_0087` | The medflow project must never store patient health information in logs or error messages; PHI must  |
| exact unit_text overlap | `v05_batch500_0087` | `v05_batch500_0087` | Every medflow service must expose a /health endpoint that returns 200 only when all dependencies are |
| exact unit_text overlap | `v05_batch500_0088` | `v05_batch500_0088` | The disaster recovery runbook is stored at docs/operations/dr_runbook.md and must be updated wheneve |
| exact unit_text overlap | `v05_batch500_0088` | `v05_batch500_0088` | All logistix services must have their database backups stored in the backup bucket at s3://logistix- |
| exact unit_text overlap | `v05_batch500_0088` | `v05_batch500_0088` | Run a disaster recovery drill for the inventory-sync service before the peak holiday season to verif |
| exact unit_text overlap | `v05_batch500_0089` | `v05_batch500_0089` | The clausekeeper project enforces role-based access: attorneys have read-write access to all documen |
| exact unit_text overlap | `v05_batch500_0089` | `v05_batch500_0089` | All access to client documents must be logged with the user ID, document ID, action, and timestamp f |
| exact unit_text overlap | `v05_batch500_0089` | `v05_batch500_0089` | The clausekeeper project does not support external client access; all users must be employees of the |
| exact unit_text overlap | `v05_batch500_0090` | `v05_batch500_0090` | The artisan project requires all Python code to pass pylint with a minimum score of 8.0 and all Java |
| exact unit_text overlap | `v05_batch500_0090` | `v05_batch500_0090` | All public API endpoints must be documented using OpenAPI 3.0 specifications stored in docs/api/<ser |
| exact unit_text overlap | `v05_batch500_0090` | `v05_batch500_0090` | The project uses the MIT license for all open-source components and requires a CLA for external cont |
| exact unit_text overlap | `v05_batch500_0091` | `v05_batch500_0091` | Security incidents must be reported within 15 minutes of detection by posting in the #security-incid |
| exact unit_text overlap | `v05_batch500_0091` | `v05_batch500_0091` | The incident response playbook is at docs/security/incident_response.md and defines roles: incident  |
| exact unit_text overlap | `v05_batch500_0091` | `v05_batch500_0091` | Review and update the incident response playbook to include procedures for the new chat-router servi |
| exact unit_text overlap | `v05_batch500_0092` | `v05_batch500_0092` | All finboard services must enforce role-based access control with three roles: viewer, analyst, and  |
| exact unit_text overlap | `v05_batch500_0092` | `v05_batch500_0092` | The finboard project requires that all access grants be reviewed quarterly by the compliance team, w |
| exact unit_text overlap | `v05_batch500_0092` | `v05_batch500_0092` | Role definitions and permission mappings are stored in config/auth/roles.yaml and must be reviewed b |
| exact unit_text overlap | `v05_batch500_0093` | `v05_batch500_0093` | All medflow services that handle PHI must encrypt data at rest using AES-256 and in transit using TL |
| exact unit_text overlap | `v05_batch500_0093` | `v05_batch500_0093` | The medflow project must never transmit PHI over unencrypted channels; all internal service-to-servi |
| exact unit_text overlap | `v05_batch500_0093` | `v05_batch500_0093` | The PHI access audit log is stored in the audit_db database defined in config/databases/audit_db.yam |
| exact unit_text overlap | `v05_batch500_0094` | `v05_batch500_0094` | I prefer dashboard charts to use a dark theme with the 'Nord' color palette instead of the default l |
| exact unit_text overlap | `v05_batch500_0094` | `v05_batch500_0094` | I want to receive weekly digest emails on Monday mornings instead of daily metric alerts. |
| exact unit_text overlap | `v05_batch500_0094` | `v05_batch500_0094` | My login password for the staging dashboard is metricboard_stage_2026! |
| exact unit_text overlap | `v05_batch500_0095` | `v05_batch500_0095` | I prefer to study new topics by reading the summary first, then diving into detailed sections, and f |
| exact unit_text overlap | `v05_batch500_0095` | `v05_batch500_0095` | I want the platform to automatically schedule study sessions at 7:00 PM local time on weekdays. |
| exact unit_text overlap | `v05_batch500_0095` | `v05_batch500_0095` | My personal email for account recovery is tutorai_user_2026@personal.example.com. |
| exact unit_text overlap | `v05_batch500_0096` | `v05_batch500_0096` | The project scope explicitly excludes retriever training, writer training, and MemoryOS implementati |
| exact unit_text overlap | `v05_batch500_0096` | `v05_batch500_0096` | We should create a reusable skill system for SOPs that agents can invoke during complex multi-step o |
| exact unit_text overlap | `v05_batch500_0096` | `v05_batch500_0096` | The documentation for exclusion decisions lives under docs/v05/scope_exclusions.md. |
| exact unit_text overlap | `v05_batch500_0097` | `v05_batch500_0097` | Maybe we should add entity resolution to deduplicate customer records across the CRM and billing sys |
| exact unit_text overlap | `v05_batch500_0097` | `v05_batch500_0097` | The data-platform currently has no entity resolution capability and it is not in the current quarter |
| exact unit_text overlap | `v05_batch500_0097` | `v05_batch500_0097` | The roadmap document is tracked in docs/planning/roadmap_2026_Q3.md. |
| exact unit_text overlap | `v05_batch500_0098` | `v05_batch500_0098` | All field-app services must minimize cellular data usage by batching network requests and compressin |
| exact unit_text overlap | `v05_batch500_0098` | `v05_batch500_0098` | The field-app project does not collect background location data when the app is not in active use; l |
| exact unit_text overlap | `v05_batch500_0098` | `v05_batch500_0098` | The data usage limits per service are configured in config/network/data_limits.yaml and enforced by  |
| exact unit_text overlap | `v05_batch500_0099` | `v05_batch500_0099` | All shopengine customer-facing services must display the total price including all mandatory taxes a |
| exact unit_text overlap | `v05_batch500_0099` | `v05_batch500_0099` | The shopengine project prohibits dynamic pricing based on individual user browsing history; all pric |
| exact unit_text overlap | `v05_batch500_0099` | `v05_batch500_0099` | The pricing display rules are enforced by the shared pricing library at lib/pricing/display.py used  |
| exact unit_text overlap | `v05_batch500_0100` | `v05_batch500_0100` | All voyager booking services must apply the same cancellation fee schedule: free cancellation within |
| exact unit_text overlap | `v05_batch500_0100` | `v05_batch500_0100` | The voyager project requires that all cancellation confirmation emails be sent within 5 minutes of p |
| exact unit_text overlap | `v05_batch500_0100` | `v05_batch500_0100` | The cancellation fee schedule is defined in config/policies/cancellation_fees.yaml and loaded by all |
| exact unit_text overlap | `v05_batch500_0101` | `v05_batch500_0101` | I prefer the level editor to use a dark theme with the 'Dungeon' color palette and grid snapping set |
| exact unit_text overlap | `v05_batch500_0101` | `v05_batch500_0101` | When I test-play a level, automatically enable the debug overlay showing collision volumes, AI paths |
| exact unit_text overlap | `v05_batch500_0101` | `v05_batch500_0101` | The editor auto-save interval is configured in config/editor/preferences.json with a default of 5 mi |
| exact unit_text overlap | `v05_batch500_0102` | `v05_batch500_0102` | The project README.md must include a quickstart section with the exact commands to clone, install de |
| exact unit_text overlap | `v05_batch500_0102` | `v05_batch500_0102` | All development environment setup must use Docker Compose defined in docker-compose.dev.yaml, with h |
| exact unit_text overlap | `v05_batch500_0102` | `v05_batch500_0102` | Add a setup validation script at scripts/verify_dev_setup.sh that checks all prerequisites and runs  |
| exact unit_text overlap | `v05_batch500_0103` | `v05_batch500_0103` | The learnhub project must require students to acknowledge the academic integrity policy before each  |
| exact unit_text overlap | `v05_batch500_0103` | `v05_batch500_0103` | All written assignment submissions must be automatically screened by the plagiarism checker, and sub |
| exact unit_text overlap | `v05_batch500_0103` | `v05_batch500_0103` | Add the academic integrity acknowledgement checkbox to the exam start flow before the end of the cur |
| exact unit_text overlap | `v05_batch500_0104` | `v05_batch500_0104` | All helpdesk agents must have at least 5% of their resolved tickets reviewed each month; agents with |
| exact unit_text overlap | `v05_batch500_0104` | `v05_batch500_0104` | The helpdesk project quality standard requires that all customer-facing responses include a greeting |
| exact unit_text overlap | `v05_batch500_0104` | `v05_batch500_0104` | Add the QA review assignment automation that distributes tickets to QA specialists based on agent an |
| exact unit_text overlap | `v05_batch500_0105` | `v05_batch500_0105` | All metricboard services in the SOC 2 scope must log every administrative action with the user ID, a |
| exact unit_text overlap | `v05_batch500_0105` | `v05_batch500_0105` | The metricboard project requires that all production changes go through a change management process: |
| exact unit_text overlap | `v05_batch500_0105` | `v05_batch500_0105` | Complete the SOC 2 readiness assessment checklist and address any gaps before the external auditor e |
| exact unit_text overlap | `v05_batch500_0106` | `v05_batch500_0106` | I prefer workflow diagrams to use BPMN 2.0 notation with swimlanes colored by department rather than |
| exact unit_text overlap | `v05_batch500_0106` | `v05_batch500_0106` | When I export workflow documentation, include the step descriptions, input/output schemas, and error |
| exact unit_text overlap | `v05_batch500_0106` | `v05_batch500_0106` | The workflow export templates are stored in config/exports/templates/ and can be customized per depa |
| exact unit_text overlap | `v05_batch500_0107` | `v05_batch500_0107` | The spaced repetition engine must use the FSRS algorithm with default parameters: decay=-0.5, factor |
| exact unit_text overlap | `v05_batch500_0107` | `v05_batch500_0107` | The FSRS model parameters are stored in config/spaced_repetition/fsrs_params.json and can be tuned p |
| exact unit_text overlap | `v05_batch500_0107` | `v05_batch500_0107` | Run an A/B test comparing FSRS against the current SM-2 algorithm on 500 learners before rolling out |
| exact unit_text overlap | `v05_batch500_0108` | `v05_batch500_0108` | The order validator must reject purchase orders where the requested quantity exceeds the supplier's  |
| exact unit_text overlap | `v05_batch500_0108` | `v05_batch500_0108` | The supplier max-quantity data is currently stale for 12 suppliers; update the supplier catalog befo |
| exact unit_text overlap | `v05_batch500_0108` | `v05_batch500_0108` | The order validation rules must be the same across all logistix services including warehouse, shippi |
| exact unit_text overlap | `v05_batch500_0109` | `v05_batch500_0109` | The layer compositor must blend layers from bottom to top using the blend mode specified on each lay |
| exact unit_text overlap | `v05_batch500_0109` | `v05_batch500_0109` | The compositor currently recomputes all layers on every frame; caching optimization is scheduled for |
| exact unit_text overlap | `v05_batch500_0109` | `v05_batch500_0109` | The compositor shader source files live under src/rendering/compositor/shaders/ and are compiled at  |
| exact unit_text overlap | `v05_batch500_0110` | `v05_batch500_0110` | The signature validator must verify electronic signatures by checking the digital certificate chain  |
| exact unit_text overlap | `v05_batch500_0110` | `v05_batch500_0110` | The trusted CA certificate bundle is stored in config/certs/trusted_ca_bundle.pem and must be update |
| exact unit_text overlap | `v05_batch500_0110` | `v05_batch500_0110` | The signature validator currently does not check certificate revocation via OCSP; adding OCSP is pla |
| exact unit_text overlap | `v05_batch500_0111` | `v05_batch500_0111` | All service configuration files must be in YAML format under config/<service_name>/ with a schema ve |
| exact unit_text overlap | `v05_batch500_0111` | `v05_batch500_0111` | The schema version follows the format YYYY-MM-DD and must be updated whenever a new config key is ad |
| exact unit_text overlap | `v05_batch500_0111` | `v05_batch500_0111` | Write the configuration conventions document in docs/platform/config_conventions.md by end of sprint |
| exact unit_text overlap | `v05_batch500_0112` | `v05_batch500_0112` | Release builds must be uploaded to TestFlight for beta testing at least 1 week before App Store subm |
| exact unit_text overlap | `v05_batch500_0112` | `v05_batch500_0112` | The App Store listing metadata including description, keywords, and privacy policy URL must be revie |
| exact unit_text overlap | `v05_batch500_0112` | `v05_batch500_0112` | Add automated screenshot generation using fastlane snapshot with the UI test suite at fastlane/scree |
| exact unit_text overlap | `v05_batch500_0113` | `v05_batch500_0113` | Database migration files are named with a UTC timestamp prefix: YYYYMMDDHHMMSS_descriptive_name.sql  |
| exact unit_text overlap | `v05_batch500_0113` | `v05_batch500_0113` | Every migration must include an up.sql for forward migration and a down.sql for rollback, both in th |
| exact unit_text overlap | `v05_batch500_0113` | `v05_batch500_0113` | Migrations are applied by the migration runner container using the command: docker compose run migra |
| exact unit_text overlap | `v05_batch500_0114` | `v05_batch500_0114` | Python code in the finboard project must use Black for formatting with line length 100, and isort fo |
| exact unit_text overlap | `v05_batch500_0114` | `v05_batch500_0114` | TypeScript code must use Prettier with the project's .prettierrc.json and must pass tsc --noEmit bef |
| exact unit_text overlap | `v05_batch500_0114` | `v05_batch500_0114` | The pre-commit hooks are defined in .pre-commit-config.yaml and run Black, isort, Prettier, and tsc  |
| exact unit_text overlap | `v05_batch500_0115` | `v05_batch500_0115` | Python dependencies are managed with Poetry and locked in poetry.lock; never pip install directly in |
| exact unit_text overlap | `v05_batch500_0115` | `v05_batch500_0115` | Node.js dependencies are managed with pnpm and locked in pnpm-lock.yaml; the workspace is defined in |
| exact unit_text overlap | `v05_batch500_0115` | `v05_batch500_0115` | All Docker images must pin their base image to a specific SHA256 digest, not a mutable tag like 'lat |
| exact unit_text overlap | `v05_batch500_0116` | `v05_batch500_0116` | The audit log must store all access events in a structured JSON format with fields: event_id, timest |
| exact unit_text overlap | `v05_batch500_0116` | `v05_batch500_0116` | Audit logs must be retained for a minimum of 7 years in immutable storage to comply with healthcare  |
| exact unit_text overlap | `v05_batch500_0116` | `v05_batch500_0116` | Audit log files are rotated daily and stored under /var/log/medflow/audit/YYYY/MM/DD/ with gzip comp |
| exact unit_text overlap | `v05_batch500_0117` | `v05_batch500_0117` | Every training case must have unit texts that are semantically unique; a cosine similarity above 0.8 |
| exact unit_text overlap | `v05_batch500_0117` | `v05_batch500_0117` | The current batch500 is still under construction; the similarity check has not been run yet on the n |
| exact unit_text overlap | `v05_batch500_0117` | `v05_batch500_0117` | For this project, do not generate cases using LLM-based templates or automated fill-in-the-blank sub |
| exact unit_text overlap | `v05_batch500_0118` | `v05_batch500_0118` | I prefer query results to default to a table view with 50 rows per page and columns in the order the |
| exact unit_text overlap | `v05_batch500_0118` | `v05_batch500_0118` | When I save a query, automatically tag it with the current project context and date so I can find it |
| exact unit_text overlap | `v05_batch500_0118` | `v05_batch500_0118` | My saved queries and chart configurations are stored under my user profile in config/users/analyst_4 |
| exact unit_text overlap | `v05_batch500_0119` | `v05_batch500_0119` | The on-call rotation schedule is managed in PagerDuty with the schedule defined in config/oncall/rot |
| exact unit_text overlap | `v05_batch500_0119` | `v05_batch500_0119` | Production incidents must be acknowledged within 5 minutes of the first page; if unacknowledged, esc |
| exact unit_text overlap | `v05_batch500_0119` | `v05_batch500_0119` | Update the escalation policy to include the new chat-router service as a monitored component with th |
| exact unit_text overlap | `v05_batch500_0120` | `v05_batch500_0120` | The spell checker must use a project-specific dictionary at data/dictionaries/project_terms.txt that |
| exact unit_text overlap | `v05_batch500_0120` | `v05_batch500_0120` | Terms added to the project dictionary must be reviewed in the PR that adds them; no direct commits t |
| exact unit_text overlap | `v05_batch500_0120` | `v05_batch500_0120` | The spell checker must flag words that appear in code blocks or inline code differently from prose:  |
| exact unit_text overlap | `v05_batch500_0121` | `v05_batch500_0121` | I prefer flight search results sorted by total travel time rather than price when the price differen |
| exact unit_text overlap | `v05_batch500_0121` | `v05_batch500_0121` | When I search for hotels, prioritize properties with a guest rating of 4.0 or above and filter out p |
| exact unit_text overlap | `v05_batch500_0121` | `v05_batch500_0121` | My loyalty program numbers are stored in my account profile; the voyager system should automatically |
| exact unit_text overlap | `v05_batch500_0122` | `v05_batch500_0122` | I prefer bug reports to include the game build version, the exact steps to reproduce, and a screensh |
| exact unit_text overlap | `v05_batch500_0122` | `v05_batch500_0122` | When I mark a bug as 'cannot reproduce', prompt me to record a 30-second video clip of my attempt be |
| exact unit_text overlap | `v05_batch500_0122` | `v05_batch500_0122` | The bug report templates are configured in config/qa/bug_report_template.yaml. |
| exact unit_text overlap | `v05_batch500_0123` | `v05_batch500_0123` | All course content uploaded to learnhub must meet WCAG 2.1 AA standards: videos must have captions,  |
| exact unit_text overlap | `v05_batch500_0123` | `v05_batch500_0123` | The learnhub project provides an accessibility checker tool at tools/a11y_checker/ that instructors  |
| exact unit_text overlap | `v05_batch500_0123` | `v05_batch500_0123` | Run the accessibility checker on all courses for the upcoming fall semester and generate a complianc |
| exact unit_text overlap | `v05_batch500_0124` | `v05_batch500_0124` | All services must emit logs in structured JSON format with the following required fields: timestamp, |
| exact unit_text overlap | `v05_batch500_0124` | `v05_batch500_0124` | Log levels are DEBUG, INFO, WARN, ERROR, FATAL; production environments must run at INFO level minim |
| exact unit_text overlap | `v05_batch500_0124` | `v05_batch500_0124` | Logs are shipped to the central logging platform via a Fluentd sidecar that tails the container's st |
| exact unit_text overlap | `v05_batch500_0125` | `v05_batch500_0125` | All third-party API integrations must implement a circuit breaker pattern with 5 consecutive failure |
| exact unit_text overlap | `v05_batch500_0125` | `v05_batch500_0125` | API client code for third-party integrations lives under src/integrations/<provider>/ and must imple |
| exact unit_text overlap | `v05_batch500_0125` | `v05_batch500_0125` | Add the circuit breaker to the supplier inventory API integration which currently has no failure han |
| exact unit_text overlap | `v05_batch500_0126` | `v05_batch500_0126` | All datasets in the data-platform must be registered in the data catalog with owner, update frequenc |
| exact unit_text overlap | `v05_batch500_0126` | `v05_batch500_0126` | The data catalog API is documented at docs/api/catalog_api.md and dataset registration is done via P |
| exact unit_text overlap | `v05_batch500_0126` | `v05_batch500_0126` | The billing_facts and customer_contacts datasets are still not registered in the catalog; register t |
| exact unit_text overlap | `v05_batch500_0127` | `v05_batch500_0127` | All field-app services must log performance metrics to the performance_metrics table including opera |
| exact unit_text overlap | `v05_batch500_0127` | `v05_batch500_0127` | The performance regression test suite is at tests/performance/ and must be run before every release; |
| exact unit_text overlap | `v05_batch500_0127` | `v05_batch500_0127` | Profile the sync module's SQLite queries which are showing p99 latency of 800ms on low-end devices a |
| exact unit_text overlap | `v05_batch500_0128` | `v05_batch500_0128` | The cart service must expire abandoned carts after 7 days of inactivity, removing reserved inventory |
| exact unit_text overlap | `v05_batch500_0128` | `v05_batch500_0128` | The cart expiration job runs daily at 03:00 UTC and processes carts in batches of 500; its schedule  |
| exact unit_text overlap | `v05_batch500_0128` | `v05_batch500_0128` | The cart service currently holds inventory for 7 days but the business team wants to reduce this to  |
| exact unit_text overlap | `v05_batch500_0129` | `v05_batch500_0129` | All artisan project assets must follow the naming convention: <project>_<category>_<descriptor>_<ver |
| exact unit_text overlap | `v05_batch500_0129` | `v05_batch500_0129` | The master asset naming guide is at docs/standards/asset_naming.md and includes category codes for t |
| exact unit_text overlap | `v05_batch500_0129` | `v05_batch500_0129` | Run the asset validator on the legacy asset library to identify files that don't comply with the nam |
| exact unit_text overlap | `v05_batch500_0130` | `v05_batch500_0130` | The search engine must prioritize exact phrase matches in clause text over keyword matches, with a b |
| exact unit_text overlap | `v05_batch500_0130` | `v05_batch500_0130` | Search index settings including boost weights and tokenizer configuration are stored in config/searc |
| exact unit_text overlap | `v05_batch500_0130` | `v05_batch500_0130` | The search index currently takes 4 hours to rebuild; optimize the rebuild to under 1 hour before add |
| exact unit_text overlap | `v05_batch500_0131` | `v05_batch500_0131` | All clinical staff must complete the annual HIPAA refresher training before they can access patient  |
| exact unit_text overlap | `v05_batch500_0131` | `v05_batch500_0131` | Training materials for new medflow features are stored under docs/training/ with separate modules fo |
| exact unit_text overlap | `v05_batch500_0131` | `v05_batch500_0131` | Update the HIPAA training module to include the new telehealth consent requirements before the Q3 tr |
| exact unit_text overlap | `v05_batch500_0132` | `v05_batch500_0132` | The v0.5 evaluation must compare the trained LoRA router against the Qwen3-4B few-shot baseline and  |
| exact unit_text overlap | `v05_batch500_0132` | `v05_batch500_0132` | Evaluation results must report per-target accuracy, per-tag F1, and confusion matrices for each targ |
| exact unit_text overlap | `v05_batch500_0132` | `v05_batch500_0132` | Run the baseline evaluation on the gold set before starting LoRA training to establish the compariso |
| exact unit_text overlap | `v05_batch500_0133` | `v05_batch500_0133` | The auth service must issue JWTs signed with RS256, with a 15-minute access token expiry and a 7-day |
| exact unit_text overlap | `v05_batch500_0133` | `v05_batch500_0133` | The JWT signing keys are stored in config/auth/keys/ and rotated every 90 days via the key rotation  |
| exact unit_text overlap | `v05_batch500_0133` | `v05_batch500_0133` | The auth service currently does not support social login providers; adding Google and GitHub OAuth i |
| exact unit_text overlap | `v05_batch500_0134` | `v05_batch500_0134` | The survey engine must send a CSAT survey 24 hours after ticket resolution, with a single question r |
| exact unit_text overlap | `v05_batch500_0134` | `v05_batch500_0134` | Survey question templates and timing rules are configured in config/surveys/csat_config.yaml per sup |
| exact unit_text overlap | `v05_batch500_0134` | `v05_batch500_0134` | The survey engine currently only supports CSAT; adding NPS surveys for enterprise customers is on th |
| exact unit_text overlap | `v05_batch500_0135` | `v05_batch500_0135` | All finboard quantitative models including the risk analyzer, portfolio optimizer, and market data p |
| exact unit_text overlap | `v05_batch500_0135` | `v05_batch500_0135` | The finboard project requires that any model change resulting in a 5% or greater change in output fo |
| exact unit_text overlap | `v05_batch500_0135` | `v05_batch500_0135` | Schedule the annual model validation for the risk analyzer and update the model documentation in doc |
| exact unit_text overlap | `v05_batch500_0137` | `v05_batch500_0137` | The grading service must evaluate essay submissions against a rubric with up to 5 criteria, each wit |
| exact unit_text overlap | `v05_batch500_0137` | `v05_batch500_0137` | Rubric definitions are stored as JSON files in config/grading/rubrics/ and referenced by assignment  |
| exact unit_text overlap | `v05_batch500_0137` | `v05_batch500_0137` | The grading service currently only supports single-criterion rubrics for multiple-choice questions;  |
| exact unit_text overlap | `v05_batch500_0138` | `v05_batch500_0138` | The content recommendation engine must rank learning resources by a composite score of relevance, di |
| exact unit_text overlap | `v05_batch500_0138` | `v05_batch500_0138` | Recommendation model weights and feature configurations are stored in models/recommendations/ranking |
| exact unit_text overlap | `v05_batch500_0138` | `v05_batch500_0138` | The recommendation engine currently does not account for the learner's preferred content format; add |
| exact unit_text overlap | `v05_batch500_0139` | `v05_batch500_0139` | The compensation handler must execute compensating actions in reverse order of the original steps wh |
| exact unit_text overlap | `v05_batch500_0139` | `v05_batch500_0139` | Compensation action definitions are stored in workflows/<name>/compensations.yaml with a reverse fla |
| exact unit_text overlap | `v05_batch500_0139` | `v05_batch500_0139` | The compensation handler currently only supports database rollback compensations; adding support for |
| exact unit_text overlap | `v05_batch500_0140` | `v05_batch500_0140` | The delivery tracker must compute ETA using the driver's current GPS position, the remaining route d |
| exact unit_text overlap | `v05_batch500_0140` | `v05_batch500_0140` | The ETA calculation parameters including speed estimation weights are configured in config/delivery/ |
| exact unit_text overlap | `v05_batch500_0140` | `v05_batch500_0140` | The delivery tracker currently does not account for real-time traffic conditions; integrating traffi |
| exact unit_text overlap | `v05_batch500_0141` | `v05_batch500_0141` | The inventory system must stack identical items with the same durability value up to a maximum stack |
| exact unit_text overlap | `v05_batch500_0141` | `v05_batch500_0141` | Item type definitions including max stack sizes and durability thresholds are stored in config/items |
| exact unit_text overlap | `v05_batch500_0141` | `v05_batch500_0141` | The inventory system currently allows stacking items with different durability values, which causes  |
| exact unit_text overlap | `v05_batch500_0142` | `v05_batch500_0142` | The price alert service must monitor subscribed routes and trigger an alert when the current price d |
| exact unit_text overlap | `v05_batch500_0142` | `v05_batch500_0142` | Alert rule configurations per user and route are stored in config/alerts/price_alerts/ with notifica |
| exact unit_text overlap | `v05_batch500_0142` | `v05_batch500_0142` | The price alert service currently checks prices every 30 minutes; reducing the check interval to 5 m |
| exact unit_text overlap | `v05_batch500_0144` | `v05_batch500_0144` | The Bluetooth connector must attempt reconnection to a paired peripheral with exponential backoff: 1 |
| exact unit_text overlap | `v05_batch500_0144` | `v05_batch500_0144` | The BLE reconnection parameters are configured in config/bluetooth/reconnect_policy.xml with backoff |
| exact unit_text overlap | `v05_batch500_0144` | `v05_batch500_0144` | The Bluetooth connector currently does not distinguish between transient disconnections and device-p |
| exact unit_text overlap | `v05_batch500_0145` | `v05_batch500_0145` | All shopengine customer-facing services must enforce the platform terms of service: users who have n |
| exact unit_text overlap | `v05_batch500_0145` | `v05_batch500_0145` | The shopengine project requires that all promotional emails include an unsubscribe link that takes e |
| exact unit_text overlap | `v05_batch500_0145` | `v05_batch500_0145` | The current ToS acceptance tracking is only implemented in the checkout service; add it to the accou |
| exact unit_text overlap | `v05_batch500_0146` | `v05_batch500_0146` | The undo manager must maintain a stack of reversible operations with a maximum depth of 100 entries  |
| exact unit_text overlap | `v05_batch500_0146` | `v05_batch500_0146` | Undo stack configuration including max depth and grouping thresholds is in config/undo/undo_settings |
| exact unit_text overlap | `v05_batch500_0146` | `v05_batch500_0146` | The undo manager currently does not support redo after a new action following undo; implementing ful |
| exact unit_text overlap | `v05_batch500_0147` | `v05_batch500_0147` | The version comparator must highlight textual differences between contract versions using a word-lev |
| exact unit_text overlap | `v05_batch500_0147` | `v05_batch500_0147` | Diff visualization templates and color schemes are stored in config/diff/templates/ and can be custo |
| exact unit_text overlap | `v05_batch500_0147` | `v05_batch500_0147` | The version comparator currently only supports text diff; adding table comparison for schedules and  |
| exact unit_text overlap | `v05_batch500_0148` | `v05_batch500_0148` | The eval runner must support early stopping based on a monitored metric: if the metric does not impr |
| exact unit_text overlap | `v05_batch500_0148` | `v05_batch500_0148` | The early-stopping configuration including patience and metric name is stored in config/eval/early_s |
| exact unit_text overlap | `v05_batch500_0148` | `v05_batch500_0148` | The eval runner currently only supports early stopping on dev set loss; adding support for stopping  |
| exact unit_text overlap | `v05_batch500_0136` | `v05_batch500_0136` | The PDF generator must produce PDF/A-3 compliant documents with embedded fonts, metadata, and a tabl |
| exact unit_text overlap | `v05_batch500_0136` | `v05_batch500_0136` | PDF generation templates and compliance settings are stored in config/pdf/templates/ with separate t |
| exact unit_text overlap | `v05_batch500_0136` | `v05_batch500_0136` | The PDF generator currently does not support right-to-left text rendering for Arabic and Hebrew; RTL |
| exact unit_text overlap | `v05_batch500_0143` | `v05_batch500_0143` | The data masking service must apply masking rules based on the user's role: analysts see masked PII, |
| exact unit_text overlap | `v05_batch500_0143` | `v05_batch500_0143` | Data masking rule configurations per role and column are stored in config/masking/role_policies.yaml |
| exact unit_text overlap | `v05_batch500_0143` | `v05_batch500_0143` | The data masking service currently masks all PII columns uniformly; implementing column-specific mas |
| exact unit_text overlap | `v05_batch500_0149` | `v05_batch500_0149` | Does the patient John Doe have any documented allergies to penicillin? |
| exact unit_text overlap | `v05_batch500_0150` | `v05_batch500_0150` | What is the current stock level for product SKU WH-8842 in the Dallas warehouse? |
| exact unit_text overlap | `v05_batch500_0151` | `v05_batch500_0151` | What texture compression format is used for the iOS build target? |
| exact unit_text overlap | `v05_batch500_0152` | `v05_batch500_0152` | Will my existing v2 plugins still work after the next update? |
| exact unit_text overlap | `v05_batch500_0153` | `v05_batch500_0153` | How many active contracts does client Acme Corp have with an effective date in 2026? |
| exact unit_text overlap | `v05_batch500_0154` | `v05_batch500_0154` | What is the current average wait time for priority-normal tickets? |
| exact unit_text overlap | `v05_batch500_0155` | `v05_batch500_0155` | Show me the SQL query I ran last Tuesday that returned the monthly revenue by region. |
| exact unit_text overlap | `v05_batch500_0156` | `v05_batch500_0156` | Which OpenAPI version does the doc generator currently support? |
| exact unit_text overlap | `v05_batch500_0157` | `v05_batch500_0157` | What is the current rate limit for the SkyConnect airline search API? |
| exact unit_text overlap | `v05_batch500_0158` | `v05_batch500_0158` | Is student S-44921 enrolled in CS-301 Section 02 this semester? |
| exact unit_text overlap | `v05_batch500_0159` | `v05_batch500_0159` | When is the next scheduled import for the trading_desk_pnl dataset? |
| exact unit_text overlap | `v05_batch500_0160` | `v05_batch500_0160` | What is the current status of workflow execution #WF-2026-0602-0042? |
| exact unit_text overlap | `v05_batch500_0161` | `v05_batch500_0161` | What is the current GPS sampling interval for the field survey team's devices? |
| exact unit_text overlap | `v05_batch500_0162` | `v05_batch500_0162` | What would be the FedEx Ground shipping cost for a 5lb package from the Dallas warehouse to Chicago  |
| exact unit_text overlap | `v05_batch500_0163` | `v05_batch500_0163` | Show me the progress for learner L-8821 in the Python Basics course. |
| exact unit_text overlap | `v05_batch500_0164` | `v05_batch500_0164` | What was the error rate for the billing pipeline over the past 7 days? |
| exact unit_text overlap | `v05_batch500_0165` | `v05_batch500_0165` | Which agents with the billing_certified skill are available for the 14:00-22:00 shift today? |
| exact unit_text overlap | `v05_batch500_0166` | `v05_batch500_0166` | How many READ+STORE joint cases have been created so far in the batch500 new200 generation? |
| exact unit_text overlap | `v05_batch500_0167` | `v05_batch500_0167` | What color palette is currently configured for the revenue trend line chart on the executive dashboa |
| exact unit_text overlap | `v05_batch500_0168` | `v05_batch500_0168` | What is the onboarding status of the new supplier PackRight Inc.? |
| exact unit_text overlap | `v05_batch500_0169` | `v05_batch500_0169` | Are there any open telehealth slots with Dr. Chen next Wednesday between 09:00 and 12:00? |
| exact unit_text overlap | `v05_batch500_0170` | `v05_batch500_0170` | Which contracts have a renewal deadline within the next 30 days? |
| exact unit_text overlap | `v05_batch500_0171` | `v05_batch500_0171` | What is the status of export job #EXP-2026-0602-0089? |
| exact unit_text overlap | `v05_batch500_0172` | `v05_batch500_0172` | What is the correct answer rate for question Q-3391 in the CS-301 final exam? |
| exact unit_text overlap | `v05_batch500_0173` | `v05_batch500_0173` | What is the total build size for the latest PS5 release candidate? |
| exact unit_text overlap | `v05_batch500_0174` | `v05_batch500_0174` | What were the top 5 search queries that returned zero results last week? |
| exact unit_text overlap | `v05_batch500_0175` | `v05_batch500_0175` | What is the current market value of account A-7742's technology sector holdings? |
| exact unit_text overlap | `v05_batch500_0176` | `v05_batch500_0176` | Show me the complete execution history for the purchase_order_approval workflow from May 2026. |
| exact unit_text overlap | `v05_batch500_0177` | `v05_batch500_0177` | How much cellular data has the sync module used so far this billing cycle? |
| exact unit_text overlap | `v05_batch500_0178` | `v05_batch500_0178` | How many product reviews are currently awaiting moderation for the electronics category? |
| exact unit_text overlap | `v05_batch500_0179` | `v05_batch500_0179` | What alternative flights are available for passenger booking PNR-8XK29W after flight AA-1042 was can |
| exact unit_text overlap | `v05_batch500_0180` | `v05_batch500_0180` | Find all datasets that contain customer_email columns and are updated daily. |
| exact unit_text overlap | `v05_batch500_0181` | `v05_batch500_0181` | Find beginner-level resources on Python list comprehensions, preferably video format. |
| exact unit_text overlap | `v05_batch500_0182` | `v05_batch500_0182` | Find previously resolved tickets similar to: customer reports that their account is locked after 3 f |
| exact unit_text overlap | `v05_batch500_0183` | `v05_batch500_0183` | Who has edit access to the Executive KPI Dashboard? |
| exact unit_text overlap | `v05_batch500_0184` | `v05_batch500_0184` | What is the current status of lab order STAT-4421? |
| exact unit_text overlap | `v05_batch500_0185` | `v05_batch500_0185` | Where is shipment SH-2026-8841 right now? |
| exact unit_text overlap | `v05_batch500_0186` | `v05_batch500_0186` | Find the latest reviewed template for a California NDA with a 2-year term. |
| exact unit_text overlap | `v05_batch500_0187` | `v05_batch500_0187` | Find all PNG assets tagged with 'UI' and 'button' that are exactly 64x64 pixels. |
| exact unit_text overlap | `v05_batch500_0188` | `v05_batch500_0188` | Has the Q1 2026 transaction compliance report been filed? |
| exact unit_text overlap | `v05_batch500_0189` | `v05_batch500_0189` | Show me the validation errors for case v05_batch300_0042 from the batch300 repair run. |
| exact unit_text overlap | `v05_batch500_0190` | `v05_batch500_0190` | How many posts in the CS-301 forum are currently flagged for moderation? |
| exact unit_text overlap | `v05_batch500_0191` | `v05_batch500_0191` | Which documentation pages received the most 'not helpful' ratings in the past 30 days? |
| exact unit_text overlap | `v05_batch500_0192` | `v05_batch500_0192` | The tutorai project must ensure that all AI-generated explanations are factually accurate, cite sour |
| exact unit_text overlap | `v05_batch500_0192` | `v05_batch500_0192` | AI-generated quiz questions must be reviewed by a subject matter expert before being added to the qu |
| exact unit_text overlap | `v05_batch500_0192` | `v05_batch500_0192` | Add the AI content label to all generated explanations and the source citation footer before the pub |
| exact unit_text overlap | `v05_batch500_0193` | `v05_batch500_0193` | All helpdesk services that store customer data must implement an export endpoint that returns all cu |
| exact unit_text overlap | `v05_batch500_0193` | `v05_batch500_0193` | The helpdesk project requires that customer data deletion be irreversible after the 30-day grace per |
| exact unit_text overlap | `v05_batch500_0193` | `v05_batch500_0193` | Add the data export endpoint to the ticket service and the chat history service before the privacy r |
| exact unit_text overlap | `v05_batch500_0194` | `v05_batch500_0194` | All metricboard services must check the data classification tag before serving query results: restri |
| exact unit_text overlap | `v05_batch500_0194` | `v05_batch500_0194` | The metricboard project requires that confidential and restricted data be encrypted at rest with sep |
| exact unit_text overlap | `v05_batch500_0194` | `v05_batch500_0194` | Classify all existing datasets in the data catalog with the appropriate sensitivity level before the |
| exact unit_text overlap | `v05_batch500_0195` | `v05_batch500_0195` | The stream processor must support tumbling windows of 60 seconds with late-data handling: events arr |
| exact unit_text overlap | `v05_batch500_0195` | `v05_batch500_0195` | Add the windowed aggregation operator to the stream processing DSL. |
| exact unit_text overlap | `v05_batch500_0196` | `v05_batch500_0196` | The media uploader must support resumable uploads: if the connection drops, the upload resumes from  |
| exact unit_text overlap | `v05_batch500_0196` | `v05_batch500_0196` | Add chunk acknowledgment tracking using the server-returned upload_id and chunk index. |
| exact unit_text overlap | `v05_batch500_0197` | `v05_batch500_0197` | All flowcraft REST APIs must include a version prefix in the URL path: /api/v1/ for current, with de |
| exact unit_text overlap | `v05_batch500_0197` | `v05_batch500_0197` | API version changelogs must be maintained in docs/api/CHANGELOG.md with breaking changes highlighted |
| exact unit_text overlap | `v05_batch500_0197` | `v05_batch500_0197` | The workflow execution API is currently at /api/v0/ and needs to be upgraded to /api/v1/ with the ne |
| exact unit_text overlap | `v05_batch500_0198` | `v05_batch500_0198` | All logistix services must report carbon emissions data per shipment: the route optimizer reports es |
| exact unit_text overlap | `v05_batch500_0198` | `v05_batch500_0198` | The logistix project has committed to net-zero operations by 2030; all service-level decisions that  |
| exact unit_text overlap | `v05_batch500_0198` | `v05_batch500_0198` | The sustainability metrics dashboard is configured in grafana/dashboards/sustainability.json and upd |
| exact unit_text overlap | `v05_batch500_0199` | `v05_batch500_0199` | Does claim CL-2026-8891 pass all pre-submission validation checks for BlueCross? |
| exact unit_text overlap | `v05_batch500_0200` | `v05_batch500_0200` | What easing function is used for the opacity keyframe transition at 2.5 seconds in the intro animati |
| exact memory content overlap | `v05_sample_0001` | `v05_sample_0001` | The parser rejects unknown STORE targets and does not do semantic repair. |
| exact memory content overlap | `v05_sample_0001` | `v05_sample_0001` | The v0.4 pilot evaluates Unit DSL before v0.5 training. |
| exact memory content overlap | `v05_sample_0001` | `v05_sample_0001` | The old v0.3 validator checked exact write_spans substrings only. |
| exact memory content overlap | `v05_sample_0002` | `v05_sample_0002` | The sync module retries failed uploads in batches of 10 with exponential backoff. |
| exact memory content overlap | `v05_sample_0002` | `v05_sample_0002` | Sync-related integration tests live under tests/integration/sync/. |
| exact memory content overlap | `v05_sample_0002` | `v05_sample_0002` | The old v0.2 sync used polling instead of push notifications. |
| exact memory content overlap | `v05_sample_0003` | `v05_sample_0003` | The export job writes invoices to S3 daily at 02:00 UTC and uses the credentials from IAM role expor |
| exact memory content overlap | `v05_sample_0003` | `v05_sample_0003` | The billing report generator is a separate service that reads exported invoices. |
| exact memory content overlap | `v05_sample_0009` | `v05_sample_0009` | The eval_runner groups predictions by interface and system, then scores each group independently. |
| exact memory content overlap | `v05_sample_0009` | `v05_sample_0009` | Eval runner code lives under src/v04/eval_runner.py and reports go to reports/v04/. |
| exact memory content overlap | `v05_sample_0009` | `v05_sample_0009` | The v0.4 pilot compares three raw-output interfaces before training. |
| exact memory content overlap | `v05_sample_0010` | `v05_sample_0010` | The sync module queues offline edits and retries them in creation order with exponential backoff. |
| exact memory content overlap | `v05_sample_0010` | `v05_sample_0010` | The previous sync change was deployed last week and passed integration tests. |
| exact memory content overlap | `v05_sample_0010` | `v05_sample_0010` | The old v0.2 notification service used polling instead of push. |
| exact memory content overlap | `v05_sample_0011` | `v05_sample_0011` | The prompt builder renders current units with stable unit IDs and targets for the model. |
| exact memory content overlap | `v05_sample_0011` | `v05_sample_0011` | The v0.4 interface pilot does not implement LLM unitization. |
| exact memory content overlap | `v05_sample_0011` | `v05_sample_0011` | Prompt templates live under prompts/v04/ and use {runtime_context} as placeholder. |
| exact memory content overlap | `v05_sample_0012` | `v05_sample_0012` | The export job writes invoices to S3 daily at 02:00 UTC using IAM role export-writer. |
| exact memory content overlap | `v05_sample_0012` | `v05_sample_0012` | The export job currently does NOT validate file integrity after writing. |
| exact memory content overlap | `v05_sample_0012` | `v05_sample_0012` | Export job configuration lives in config/export.yaml with schema version 2. |
| exact memory content overlap | `v05_sample_0013` | `v05_sample_0013` | The parser rejects duplicate STORE assignments and missing unit assignments. |
| exact memory content overlap | `v05_sample_0013` | `v05_sample_0013` | Parser tests live under tests/v04/test_parser.py and use pytest. |
| exact memory content overlap | `v05_sample_0013` | `v05_sample_0013` | v0.4 is an interface pilot before v0.5 LoRA/SFT training. |
| exact memory content overlap | `v05_sample_0013` | `v05_sample_0013` | The old v0.3 validator accepted JSON with read_hints and write_spans only. |
| exact memory content overlap | `v05_sample_0021` | `v05_sample_0021` | The notification service delivers push notifications via Firebase Cloud Messaging with a 30-second d |
| exact memory content overlap | `v05_sample_0021` | `v05_sample_0021` | Notification service configuration lives in config/notification.yaml with environment-specific FCM c |
| exact memory content overlap | `v05_sample_0016` | `v05_sample_0016` | Camera default preferences are stored in config/camera_defaults.yaml and must be JSON-serializable. |
| exact memory content overlap | `v05_sample_0016` | `v05_sample_0016` | The user prefers low-light enhancement enabled for all photo captures. |
| exact memory content overlap | `v05_sample_0017` | `v05_sample_0017` | The pipeline publishes job completion events to the monitoring queue. |
| exact memory content overlap | `v05_sample_0017` | `v05_sample_0017` | The old v1 pipeline wrote logs to a flat file instead of structured events. |
| exact memory content overlap | `v05_sample_0018` | `v05_sample_0018` | The v0.4 interface pilot confirmed Unit DSL as the primary training interface for v0.5. |
| exact memory content overlap | `v05_sample_0018` | `v05_sample_0018` | The project does not train a retriever or writer; it only trains the memory policy router. |
| exact memory content overlap | `v05_sample_0019` | `v05_sample_0019` | The sync offline queue stores pending edits in SQLite with a maximum of 5000 entries. |
| exact memory content overlap | `v05_sample_0019` | `v05_sample_0019` | The sync module retries failed uploads with exponential backoff: 1s, 2s, 4s, 8s, then gives up. |
| exact memory content overlap | `v05_sample_0020` | `v05_sample_0020` | The export job writes invoices to S3 daily and expects exactly-once delivery semantics. |
| exact memory content overlap | `v05_sample_0020` | `v05_sample_0020` | The data-platform pilot scope is limited to synthetic service scenarios only. |
| exact memory content overlap | `v05_sample_0020` | `v05_sample_0020` | The legacy v1 invoice generator ran on-premise and used FTP for delivery. |
| exact memory content overlap | `v05_batch50_0001` | `v05_batch50_0001` | The pipeline runs daily at 06:00 UTC and processes all tables in dependency order. |
| exact memory content overlap | `v05_batch50_0001` | `v05_batch50_0001` | Pipeline schedule overrides are stored in config/pipeline_schedule.yaml. |
| exact memory content overlap | `v05_batch50_0001` | `v05_batch50_0001` | The old v1 pipeline used cron-based scheduling with a single nightly batch. |
| exact memory content overlap | `v05_batch50_0002` | `v05_batch50_0002` | The camera module initializes the hardware driver in onCreate and releases it in onDestroy. |
| exact memory content overlap | `v05_batch50_0002` | `v05_batch50_0002` | The last camera bug was a race condition on HDR initialization that was fixed last release. |
| exact memory content overlap | `v05_batch50_0002` | `v05_batch50_0002` | Camera module code lives under app/src/main/java/com/fieldapp/camera/. |
| exact memory content overlap | `v05_batch300_0001` | `v05_batch50_0003` | The case validator checks that every current unit appears exactly once in gold.store or gold.skip. |
| exact memory content overlap | `v05_batch50_0003` | `v05_batch50_0003` | The case validator also verifies that gold.dsl parses consistently with structured gold fields. |
| exact memory content overlap | `v05_batch50_0003` | `v05_batch50_0003` | The v0.4 case schema defines gold as read, store, skip, and optional dsl. |
| exact memory content overlap | `v05_batch50_0004` | `v05_batch50_0004` | The export job writes invoices to S3 bucket export-invoices-prod with prefix by date. |
| exact memory content overlap | `v05_batch50_0004` | `v05_batch50_0004` | Export failures are logged to CloudWatch under the log group /export/job-errors. |
| exact memory content overlap | `v05_batch50_0004` | `v05_batch50_0004` | Yesterday's export run completed at 02:15 UTC with 243 invoices written. |
| exact memory content overlap | `v05_batch50_0005` | `v05_batch50_0005` | The sync offline queue has a maximum capacity of 5000 pending entries before it rejects new edits. |
| exact memory content overlap | `v05_batch50_0005` | `v05_batch50_0005` | When the queue exceeds 4000 entries, the app shows a warning banner to the user. |
| exact memory content overlap | `v05_batch50_0005` | `v05_batch50_0005` | Queue limits are configurable in config/sync_limits.yaml but require a restart to apply. |
| exact memory content overlap | `v05_batch50_0013` | `v05_batch50_0013` | The pipeline uses PostgreSQL as its metadata store with transaction isolation level READ COMMITTED. |
| exact memory content overlap | `v05_batch50_0013` | `v05_batch50_0013` | The last pipeline deadlock occurred during the 2026-05-28 night run on the billing_facts table. |
| exact memory content overlap | `v05_batch50_0013` | `v05_batch50_0013` | The old v1 pipeline used MySQL with REPEATABLE READ isolation. |
| exact memory content overlap | `v05_batch50_0014` | `v05_batch50_0014` | The notification service delivers messages via Firebase Cloud Messaging and groups them by priority  |
| exact memory content overlap | `v05_batch50_0014` | `v05_batch50_0014` | The user prefers non-urgent notifications to be delivered silently between 22:00 and 07:00. |
| exact memory content overlap | `v05_batch50_0015` | `v05_batch50_0015` | The prompt builder renders runtime_context, candidate_memories, and current_units into a structured  |
| exact memory content overlap | `v05_batch50_0015` | `v05_batch50_0015` | v0.4 used three separate system prompts for the three interfaces; v0.5 uses one unified system promp |
| exact memory content overlap | `v05_batch50_0015` | `v05_batch50_0015` | Prompt templates live under prompts/v04/ and use python format-string placeholders. |
| exact memory content overlap | `v05_batch50_0016` | `v05_batch50_0016` | The export job currently outputs invoices in CSV format with columns: invoice_id, amount, currency,  |
| exact memory content overlap | `v05_batch50_0016` | `v05_batch50_0016` | Export output format is configured in config/export.yaml under the output_format key. |
| exact memory content overlap | `v05_batch50_0016` | `v05_batch50_0016` | The billing report generator expects CSV input and will fail on any other format. |
| exact memory content overlap | `v05_batch50_0017` | `v05_batch50_0017` | v0.5 training uses LoRA on Qwen3-4B with supervised fine-tuning, not RLHF or DPO. |
| exact memory content overlap | `v05_batch50_0017` | `v05_batch50_0017` | The project does not train a retriever or memory writer; the router is the only trained component. |
| exact memory content overlap | `v05_batch50_0017` | `v05_batch50_0017` | The eval_runner requires a locked gold set that is never used during training or hyperparameter tuni |
| exact memory content overlap | `v05_batch50_0018` | `v05_batch50_0018` | The camera module uses a double-buffered preview surface with a 200ms frame timeout. |
| exact memory content overlap | `v05_batch50_0018` | `v05_batch50_0018` | HDR processing adds approximately 150ms of latency per frame on the current pipeline. |
| exact memory content overlap | `v05_batch50_0019` | `v05_batch50_0019` | The pipeline runs stages in topological order based on a DAG defined in config/pipeline_dag.yaml. |
| exact memory content overlap | `v05_batch50_0019` | `v05_batch50_0019` | Pipeline DAG visualizations are generated by scripts/visualize_dag.py and output to docs/pipeline/da |
| exact memory content overlap | `v05_batch50_0019` | `v05_batch50_0019` | The DAG was last updated three weeks ago when the billing stage was renamed to billing_2025. |
| exact memory content overlap | `v05_batch50_0020` | `v05_batch50_0020` | The case validator checks gold.dsl consistency with structured gold fields using the strict parser. |
| exact memory content overlap | `v05_batch50_0020` | `v05_batch50_0020` | Case validator source lives under src/v04/case_validator.py and tests under tests/v04/. |
| exact memory content overlap | `v05_batch50_0021` | `v05_batch50_0021` | The sync module currently uses last-write-wins conflict resolution based on modification timestamp. |
| exact memory content overlap | `v05_batch50_0021` | `v05_batch50_0021` | Sync conflicts are logged to the sync_conflicts table with both versions of the conflicting record. |
| exact memory content overlap | `v05_batch50_0021` | `v05_batch50_0021` | The conflict resolution strategy was last discussed in the 2026-05-15 sprint planning. |
| exact memory content overlap | `v05_batch50_0022` | `v05_batch50_0022` | The pipeline currently measures end-to-end latency from source table commit to destination table ava |
| exact memory content overlap | `v05_batch50_0022` | `v05_batch50_0022` | The data-platform SLA guarantees that all tables are fresh within 4 hours of source commit. |
| exact memory content overlap | `v05_batch50_0022` | `v05_batch50_0022` | SLA dashboards are configured in grafana/dashboards/data_freshness.json. |
| exact memory content overlap | `v05_batch50_0027` | `v05_batch50_0027` | The pipeline catches all exceptions at the stage level and writes error details to the pipeline_erro |
| exact memory content overlap | `v05_batch50_0027` | `v05_batch50_0027` | The old v1 pipeline used a separate error queue that required manual draining. |
| exact memory content overlap | `v05_batch50_0028` | `v05_batch50_0028` | The sync module currently runs on a fixed 15-minute interval using Android WorkManager with a minimu |
| exact memory content overlap | `v05_batch50_0028` | `v05_batch50_0028` | Sync scheduling parameters are configured in config/sync_schedule.xml with backoff and constraint po |
| exact memory content overlap | `v05_batch50_0030` | `v05_batch50_0030` | The pipeline currently performs full-table refreshes for all dimension tables every night. |
| exact memory content overlap | `v05_batch50_0030` | `v05_batch50_0030` | Full-table refreshes on the billing_facts table take approximately 45 minutes and lock the table for |
| exact memory content overlap | `v05_batch50_0030` | `v05_batch50_0030` | The billing_facts table was last partitioned by month in the 2026-04 schema change. |
| exact memory content overlap | `v05_batch50_0030` | `v05_batch50_0030` | The legacy v0 pipeline used a custom CDC connector that has since been deprecated. |
| exact memory content overlap | `v05_batch100_0001` | `v05_batch100_0001` | The indexer builds an inverted index over all markdown files and caches it in Redis with a 1-hour TT |
| exact memory content overlap | `v05_batch100_0001` | `v05_batch100_0001` | The old v1 indexer used Elasticsearch with a refresh interval of 30 seconds. |
| exact memory content overlap | `v05_batch100_0001` | `v05_batch100_0001` | Indexer configuration lives in config/indexer.yaml with cache_size and batch_size parameters. |
| exact memory content overlap | `v05_batch100_0002` | `v05_batch100_0002` | The aggregator computes daily sums over a 24h sliding window aligned to UTC midnight. |
| exact memory content overlap | `v05_batch100_0002` | `v05_batch100_0002` | The weekly report generator is a separate service that reads aggregated data every Monday at 06:00. |
| exact memory content overlap | `v05_batch100_0002` | `v05_batch100_0002` | Aggregation window parameters are in config/aggregator/windows.yaml. |
| exact memory content overlap | `v05_batch100_0003` | `v05_batch100_0003` | The pricing service caches flight prices in Memcached with a 5-minute TTL per route. |
| exact memory content overlap | `v05_batch100_0003` | `v05_batch100_0003` | The old v2 pricing service used Redis with a 15-minute TTL and was decommissioned in 2025. |
| exact memory content overlap | `v05_batch100_0004` | `v05_batch100_0004` | The search service ranks results by TF-IDF score with a boost factor of 2.0 for title matches. |
| exact memory content overlap | `v05_batch100_0004` | `v05_batch100_0004` | Last week's A/B test showed that title boosting improved click-through rate by 12%. |
| exact memory content overlap | `v05_batch100_0004` | `v05_batch100_0004` | Search ranking weights are configured in config/search/ranking_weights.json. |
| exact memory content overlap | `v05_batch100_0005` | `v05_batch100_0005` | The visualizer fetches aggregated data from the aggregator service and renders charts using D3.js. |
| exact memory content overlap | `v05_batch100_0005` | `v05_batch100_0005` | The billing dashboard is a separate view that queries the invoice export service, not the aggregator |
| exact memory content overlap | `v05_batch100_0006` | `v05_batch100_0006` | The booking service sends confirmation emails via SendGrid with a template ID conf-tmpl-v3. |
| exact memory content overlap | `v05_batch100_0006` | `v05_batch100_0006` | Confirmation emails include a PDF attachment generated by the itinerary service. |
| exact memory content overlap | `v05_batch100_0006` | `v05_batch100_0006` | The SendGrid template was updated last month to include the new cancellation policy link. |
| exact memory content overlap | `v05_batch100_0007` | `v05_batch100_0007` | The grading service computes final grades as a weighted average: assignments 40%, quizzes 30%, final |
| exact memory content overlap | `v05_batch100_0007` | `v05_batch100_0007` | Grade weight configuration is in config/grading/weights.yaml and can be overridden per course. |
| exact memory content overlap | `v05_batch100_0008` | `v05_batch100_0008` | The asset pipeline compresses textures using ASTC 6x6 block compression with a quality setting of 90 |
| exact memory content overlap | `v05_batch100_0008` | `v05_batch100_0008` | The old pipeline used ETC2 compression which was 40% slower on the target hardware. |
| exact memory content overlap | `v05_batch100_0009` | `v05_batch100_0009` | The summarizer uses extractive summarization with a maximum of 5 sentences per summary. |
| exact memory content overlap | `v05_batch100_0009` | `v05_batch100_0009` | Summarizer prompts and parameters are in config/summarizer/defaults.json. |
| exact memory content overlap | `v05_batch100_0009` | `v05_batch100_0009` | The v0 summarizer used abstractive summarization but was replaced due to hallucination issues. |
| exact memory content overlap | `v05_batch100_0010` | `v05_batch100_0010` | The alerts service triggers a warning when daily revenue drops below 80% of the 30-day moving averag |
| exact memory content overlap | `v05_batch100_0010` | `v05_batch100_0010` | Critical alerts fire when revenue drops below 50% and automatically notify the CFO via PagerDuty. |
| exact memory content overlap | `v05_batch100_0010` | `v05_batch100_0010` | Alert thresholds per dashboard are in config/alerts/thresholds.yaml with per-widget overrides. |
| exact memory content overlap | `v05_batch100_0026` | `v05_batch100_0026` | The search service currently uses keyword-based TF-IDF ranking with title boost of 2.0. |
| exact memory content overlap | `v05_batch100_0026` | `v05_batch100_0026` | Search embedding models are stored in models/search/ and loaded at service startup. |
| exact memory content overlap | `v05_batch100_0026` | `v05_batch100_0026` | The old lexical search used BM25 before migrating to TF-IDF in v2. |
| exact memory content overlap | `v05_batch100_0027` | `v05_batch100_0027` | The visualizer currently renders charts as interactive SVG elements in the browser. |
| exact memory content overlap | `v05_batch100_0027` | `v05_batch100_0027` | The finboard project requires all exported reports to include a timestamp and the generating user's  |
| exact memory content overlap | `v05_batch100_0027` | `v05_batch100_0027` | Export templates live under templates/exports/ and use Jinja2 with Chart.js for rendering. |
| exact memory content overlap | `v05_batch100_0028` | `v05_batch100_0028` | The booking service currently supports round-trip and one-way bookings with a single pricing call pe |
| exact memory content overlap | `v05_batch100_0028` | `v05_batch100_0028` | The pricing service API charges per route segment and enforces a rate limit of 100 requests per minu |
| exact memory content overlap | `v05_batch100_0028` | `v05_batch100_0028` | The round-trip booking flow was last refactored in March 2026 to reduce pricing API calls by 30%. |
| exact memory content overlap | `v05_batch100_0029` | `v05_batch100_0029` | The grading service currently supports points-based grading with configurable weights per assignment |
| exact memory content overlap | `v05_batch100_0029` | `v05_batch100_0029` | Grading configuration per course is stored in config/grading/course_overrides.yaml. |
| exact memory content overlap | `v05_batch100_0030` | `v05_batch100_0030` | The asset pipeline currently processes textures individually with ASTC compression at quality 90%. |
| exact memory content overlap | `v05_batch100_0030` | `v05_batch100_0030` | Texture packing algorithms are implemented in src/asset_pipeline/packer.py with config in config/ass |
| exact memory content overlap | `v05_batch100_0030` | `v05_batch100_0030` | The old sprite sheet system used a fixed 2048x2048 atlas regardless of texture count. |
| exact memory content overlap | `v05_batch100_0031` | `v05_batch100_0031` | The search service logs query terms and clicked document IDs for relevance analysis. |
| exact memory content overlap | `v05_batch100_0031` | `v05_batch100_0031` | Last month's relevance tuning improved recall by 15% but precision dropped by 3%. |
| exact memory content overlap | `v05_batch100_0032` | `v05_batch100_0032` | The alerts service currently monitors threshold-based rules on revenue, costs, and active users. |
| exact memory content overlap | `v05_batch100_0032` | `v05_batch100_0032` | Alert rule definitions are in config/alerts/rules/ with one YAML file per metric category. |
| exact memory content overlap | `v05_batch100_0033` | `v05_batch100_0033` | The pricing service currently uses static fare tables updated weekly from airline API data. |
| exact memory content overlap | `v05_batch100_0033` | `v05_batch100_0033` | The voyager project must comply with IATA fare transparency regulations for all displayed prices. |
| exact memory content overlap | `v05_batch100_0034` | `v05_batch100_0034` | The enrollment service currently caps each course at 50 students and rejects enrollments beyond the  |
| exact memory content overlap | `v05_batch100_0034` | `v05_batch100_0034` | Course capacity limits are configured per course in config/courses/capacity.yaml. |
| exact memory content overlap | `v05_batch100_0035` | `v05_batch100_0035` | The build system currently produces a single cross-platform build using Unity's IL2CPP backend. |
| exact memory content overlap | `v05_batch100_0035` | `v05_batch100_0035` | Build scripts are in scripts/build/ with platform-specific configurations in config/build/platforms/ |
| exact memory content overlap | `v05_batch100_0035` | `v05_batch100_0035` | The last platform-specific test was a Switch build attempt in January 2026 that failed on texture co |
| exact memory content overlap | `v05_batch100_0036` | `v05_batch100_0036` | The summarizer currently processes one document at a time and returns a 5-sentence extractive summar |
| exact memory content overlap | `v05_batch100_0036` | `v05_batch100_0036` | Summary model configuration is in config/summarizer/model.yaml with the model name and token limit. |
| exact memory content overlap | `v05_batch100_0037` | `v05_batch100_0037` | The aggregator currently runs hourly batch jobs that process all transactions since the last run. |
| exact memory content overlap | `v05_batch100_0037` | `v05_batch100_0037` | The finboard project SLA requires dashboard data to be no more than 5 minutes stale during market ho |
| exact memory content overlap | `v05_batch100_0038` | `v05_batch100_0038` | The booking service currently enforces a uniform 24-hour free cancellation policy for all bookings. |
| exact memory content overlap | `v05_batch100_0038` | `v05_batch100_0038` | Cancellation rules per fare class are defined in config/booking/cancellation_policies.yaml. |
| exact memory content overlap | `v05_batch100_0038` | `v05_batch100_0038` | The legacy cancellation system issued refunds as account credit only, never back to the original pay |
| exact memory content overlap | `v05_batch100_0039` | `v05_batch100_0039` | The grading service stores final grades in the submissions table with a graded_at timestamp and inst |
| exact memory content overlap | `v05_batch100_0039` | `v05_batch100_0039` | The learnhub project requires all grade changes to have an audit trail with the original grade, new  |
| exact memory content overlap | `v05_batch100_0040` | `v05_batch100_0040` | The asset pipeline currently processes all assets on every build regardless of whether they changed. |
| exact memory content overlap | `v05_batch100_0040` | `v05_batch100_0040` | Asset metadata including content hashes is stored in build/asset_metadata.json after each build. |
| exact memory content overlap | `v05_batch100_0041` | `v05_batch100_0041` | The indexer currently performs a full reindex of all documents on every run, taking up to 8 minutes  |
| exact memory content overlap | `v05_batch100_0041` | `v05_batch100_0041` | Index state including the last indexed commit SHA is stored in data/indexer/state.json. |
| exact memory content overlap | `v05_batch100_0042` | `v05_batch100_0042` | The visualizer uses a light theme by default with CSS variables for all color definitions. |
| exact memory content overlap | `v05_batch100_0042` | `v05_batch100_0042` | The CFO prefers high-contrast charts with white backgrounds and thick gridlines. |
| exact memory content overlap | `v05_batch100_0044` | `v05_batch100_0044` | The enrollment service tracks completed courses per student in the student_courses table. |
| exact memory content overlap | `v05_batch100_0044` | `v05_batch100_0044` | The student prefers courses with hands-on projects over theory-heavy lecture courses. |
| exact memory content overlap | `v05_batch100_0045` | `v05_batch100_0045` | The build system produces instrumented builds for profiling with frame-time and memory-usage telemet |
| exact memory content overlap | `v05_batch100_0045` | `v05_batch100_0045` | The last performance regression was a 15% frame-rate drop on PS5 traced to a shadow-map resolution i |
| exact memory content overlap | `v05_batch100_0047` | `v05_batch100_0047` | The alerts service supports per-metric suppression windows to prevent alert storms during known main |
| exact memory content overlap | `v05_batch100_0049` | `v05_batch100_0049` | The enrollment service checks course capacity before allowing enrollment. |
| exact memory content overlap | `v05_batch100_0049` | `v05_batch100_0049` | Prerequisite data is stored in the courses table with a JSON column prerequisites listing required c |
| exact memory content overlap | `v05_batch100_0050` | `v05_batch100_0050` | The asset pipeline validates texture dimensions and format but does not currently score asset qualit |
| exact memory content overlap | `v05_batch100_0050` | `v05_batch100_0050` | The game-studio project requires all shipped assets to meet a minimum quality score of 80/100. |
| exact memory content overlap | `v05_batch200_0001` | `v05_batch200_0001` | The ticketing service indexes tickets by subject and body with a full-text search index rebuilt ever |
| exact memory content overlap | `v05_batch200_0001` | `v05_batch200_0001` | The old v1 ticketing system used exact-match search only and was decommissioned in 2025. |
| exact memory content overlap | `v05_batch200_0001` | `v05_batch200_0001` | Search index configuration is in config/ticketing/search_index.yaml with the refresh interval settin |
| exact memory content overlap | `v05_batch200_0002` | `v05_batch200_0002` | The catalog service caches product variants in Redis with a TTL of 30 minutes per product ID. |
| exact memory content overlap | `v05_batch200_0002` | `v05_batch200_0002` | The recommendation engine is a separate service that queries the catalog API, not the cache directly |
| exact memory content overlap | `v05_batch200_0003` | `v05_batch200_0003` | The query engine enforces a default timeout of 30 seconds for all dashboard queries and returns part |
| exact memory content overlap | `v05_batch200_0003` | `v05_batch200_0003` | Query timeout overrides per dashboard are in config/query_engine/timeouts.yaml. |
| exact memory content overlap | `v05_batch200_0003` | `v05_batch200_0003` | The legacy query engine used a 60-second fixed timeout with no partial result support. |
| exact memory content overlap | `v05_batch200_0004` | `v05_batch200_0004` | The routing service assigns tickets to agents based on skills matrix matching: each agent has a list |
| exact memory content overlap | `v05_batch200_0004` | `v05_batch200_0004` | The skills matrix was last updated two weeks ago when three new agents joined the billing team. |
| exact memory content overlap | `v05_batch200_0005` | `v05_batch200_0005` | The inventory service reserves stock for 15 minutes when a user adds an item to cart. If checkout is |
| exact memory content overlap | `v05_batch200_0005` | `v05_batch200_0005` | Inventory reservation timeout is configurable in config/inventory/reservation.yaml with the reservat |
| exact memory content overlap | `v05_batch200_0006` | `v05_batch200_0006` | The visualizer fetches data from the query engine and caches chart images for 1 hour to reduce datab |
| exact memory content overlap | `v05_batch200_0006` | `v05_batch200_0006` | The data export service is a separate component that generates CSV downloads from query results. |
| exact memory content overlap | `v05_batch200_0007` | `v05_batch200_0007` | The ticketing service starts an SLA timer when a ticket is created and pauses it when the ticket sta |
| exact memory content overlap | `v05_batch200_0007` | `v05_batch200_0007` | The helpdesk project SLA requires first-response within 1 hour for critical tickets and 4 hours for  |
| exact memory content overlap | `v05_batch200_0008` | `v05_batch200_0008` | The search service uses a Redis cache for frequent queries with a 5-minute TTL. Cache misses fall th |
| exact memory content overlap | `v05_batch200_0008` | `v05_batch200_0008` | Search cache configuration is in config/search/redis_cache.yaml with the ttl_seconds parameter. |
| exact memory content overlap | `v05_batch200_0009` | `v05_batch200_0009` | The catalog service stores products with a JSONB attributes column that contains variant-specific da |
| exact memory content overlap | `v05_batch200_0009` | `v05_batch200_0009` | Product schema migrations are in db/migrations/catalog/ and use the naming convention V{version}__{d |
| exact memory content overlap | `v05_batch200_0010` | `v05_batch200_0010` | The query engine estimates query cost based on table size and filter selectivity before execution. Q |
| exact memory content overlap | `v05_batch200_0010` | `v05_batch200_0010` | The old cost estimator used a fixed per-table multiplier that was removed in the v3 rewrite. |
| exact memory content overlap | `v05_batch200_0011` | `v05_batch200_0011` | The camera module supports photo, video, and slow-motion capture modes. HDR is available in photo mo |
| exact memory content overlap | `v05_batch200_0011` | `v05_batch200_0011` | The old camera API supported panorama mode but it was removed in v4 due to stability issues. |
| exact memory content overlap | `v05_batch200_0012` | `v05_batch200_0012` | The pipeline tracks incremental load progress in the pipeline_metadata table with columns last_load_ |
| exact memory content overlap | `v05_batch200_0012` | `v05_batch200_0012` | The last incremental load completed at 2026-05-31 06:00 UTC and processed 14,230 rows across 3 table |
| exact memory content overlap | `v05_batch200_0013` | `v05_batch200_0013` | The eval_runner computes per-interface metrics: parse success, exact match, READ F1, STORE unit F1,  |
| exact memory content overlap | `v05_batch200_0013` | `v05_batch200_0013` | The v0.4 pilot compared three interfaces before selecting Unit DSL for v0.5 training. |
| exact memory content overlap | `v05_batch200_0014` | `v05_batch200_0014` | The quiz generator pulls questions from the question_bank table filtered by topic, difficulty, and f |
| exact memory content overlap | `v05_batch200_0014` | `v05_batch200_0014` | Question bank seed data is loaded from fixtures/question_bank/ with one JSON file per topic. |
| exact memory content overlap | `v05_batch200_0015` | `v05_batch200_0015` | The orchestrator retries failed workflow steps up to 3 times with exponential backoff: 10s, 30s, 90s |
| exact memory content overlap | `v05_batch200_0015` | `v05_batch200_0015` | Retry policy configuration is in config/orchestrator/retry_policy.yaml with per-workflow overrides. |
| exact memory content overlap | `v05_batch200_0016` | `v05_batch200_0016` | The ticketing service accepts attachments up to 25MB per file with a maximum of 10 attachments per t |
| exact memory content overlap | `v05_batch200_0016` | `v05_batch200_0016` | Attachments are stored in S3 bucket helpdesk-attachments with a 7-day retention for deleted tickets. |
| exact memory content overlap | `v05_batch200_0017` | `v05_batch200_0017` | The orders service transitions orders through states: pending → confirmed → shipped → delivered. Eac |
| exact memory content overlap | `v05_batch200_0017` | `v05_batch200_0017` | The payment service is a separate microservice that updates order status to confirmed after payment  |
| exact memory content overlap | `v05_batch200_0018` | `v05_batch200_0018` | The scheduler runs reports on cron-based schedules defined per dashboard. Reports are generated as P |
| exact memory content overlap | `v05_batch200_0018` | `v05_batch200_0018` | Report schedules are stored in config/scheduler/reports.yaml with crontab syntax for each report. |
| exact memory content overlap | `v05_batch200_0019` | `v05_batch200_0019` | The pricing service categorizes fares into economy, premium-economy, business, and first class. Each |
| exact memory content overlap | `v05_batch200_0019` | `v05_batch200_0019` | Fare class rules per airline are configured in config/pricing/fare_classes/ with one YAML file per a |
| exact memory content overlap | `v05_batch200_0020` | `v05_batch200_0020` | The grading service rounds final grades to the nearest integer. Scores of .5 and above round up. Thi |
| exact memory content overlap | `v05_batch200_0020` | `v05_batch200_0020` | Rounding policy is documented in docs/grading/rounding_policy.md with examples for edge cases. |
| exact memory content overlap | `v05_batch200_0051` | `v05_batch200_0051` | The ticketing service currently tracks SLA timers but does not send notifications when an SLA is bre |
| exact memory content overlap | `v05_batch200_0051` | `v05_batch200_0051` | The helpdesk project SLA requires notification to the team lead within 5 minutes of an SLA breach. |
| exact memory content overlap | `v05_batch200_0052` | `v05_batch200_0052` | The inventory service tracks stock levels per product variant and triggers a low-stock alert at the  |
| exact memory content overlap | `v05_batch200_0052` | `v05_batch200_0052` | Warehouse API credentials are configured in config/inventory/warehouse_api.yaml with per-warehouse e |
| exact memory content overlap | `v05_batch200_0053` | `v05_batch200_0053` | The query engine currently executes every query from scratch against the data warehouse, with no res |
| exact memory content overlap | `v05_batch200_0053` | `v05_batch200_0053` | Query history is logged in the query_log table with columns query_hash, execution_time_ms, and row_c |
| exact memory content overlap | `v05_batch200_0054` | `v05_batch200_0054` | The ticketing service search uses a PostgreSQL full-text index with tsvector on the subject and body |
| exact memory content overlap | `v05_batch200_0054` | `v05_batch200_0054` | Search performance degraded by 40% after the March 2026 database migration to a new instance type. |
| exact memory content overlap | `v05_batch200_0055` | `v05_batch200_0055` | The orders service currently allows cancellation only before the order is confirmed. Once confirmed, |
| exact memory content overlap | `v05_batch200_0055` | `v05_batch200_0055` | The shopengine project must comply with consumer protection regulations requiring a 30-minute cancel |
| exact memory content overlap | `v05_batch200_0056` | `v05_batch200_0056` | The visualizer currently renders static charts from query results with no interactive drill-down cap |
| exact memory content overlap | `v05_batch200_0056` | `v05_batch200_0056` | Chart interaction handlers are implemented in src/visualizer/interactions.js with event delegation o |
| exact memory content overlap | `v05_batch200_0057` | `v05_batch200_0057` | The routing service currently assigns tickets round-robin to available agents without considering sk |
| exact memory content overlap | `v05_batch200_0057` | `v05_batch200_0057` | Agent skills are stored in the agent_skills table with columns agent_id, skill_tag, and proficiency_ |
| exact memory content overlap | `v05_batch200_0058` | `v05_batch200_0058` | The catalog service stores product reviews in the product_reviews table with columns review_id, prod |
| exact memory content overlap | `v05_batch200_0058` | `v05_batch200_0058` | The legacy review system allowed all reviews to be posted immediately without moderation, resulting  |
| exact memory content overlap | `v05_batch200_0059` | `v05_batch200_0059` | The scheduler currently runs reports on fixed cron schedules regardless of whether the underlying da |
| exact memory content overlap | `v05_batch200_0059` | `v05_batch200_0059` | Report trigger conditions are not yet implemented; the trigger_config section in config/scheduler/re |
| exact memory content overlap | `v05_batch200_0060` | `v05_batch200_0060` | The quiz generator currently selects questions at a fixed difficulty level specified in the quiz con |
| exact memory content overlap | `v05_batch200_0060` | `v05_batch200_0060` | The student prefers to start with easy questions and progressively increase difficulty as they answe |
| exact memory content overlap | `v05_batch200_0061` | `v05_batch200_0061` | The orchestrator currently executes workflow steps sequentially in dependency order with no parallel |
| exact memory content overlap | `v05_batch200_0061` | `v05_batch200_0061` | Workflow step definitions include a max_parallelism field in config/workflows/ that is currently ign |
| exact memory content overlap | `v05_batch200_0062` | `v05_batch200_0062` | The ticketing service sends a customer satisfaction survey 24 hours after ticket closure via email w |
| exact memory content overlap | `v05_batch200_0062` | `v05_batch200_0062` | Survey email templates are in templates/email/survey/ with separate templates per language. |
| exact memory content overlap | `v05_batch200_0063` | `v05_batch200_0063` | The inventory service tracks stock per individual product variant but does not currently handle bund |
| exact memory content overlap | `v05_batch200_0063` | `v05_batch200_0063` | Bundle product definitions are in config/catalog/bundles.yaml with a components list referencing ind |
| exact memory content overlap | `v05_batch200_0064` | `v05_batch200_0064` | The query engine accepts query parameters from dashboard filters and substitutes them into SQL templ |
| exact memory content overlap | `v05_batch200_0064` | `v05_batch200_0064` | The old parameter substitution used string interpolation and was vulnerable to SQL injection before  |
| exact memory content overlap | `v05_batch200_0065` | `v05_batch200_0065` | The progress tracker records daily study activity in the study_sessions table with columns student_i |
| exact memory content overlap | `v05_batch200_0065` | `v05_batch200_0065` | The student prefers visible progress indicators and achievement badges as motivational tools. |
| exact memory content overlap | `v05_batch200_0066` | `v05_batch200_0066` | The orchestrator logs workflow start and end events in the workflow_executions table but does not lo |
| exact memory content overlap | `v05_batch200_0066` | `v05_batch200_0066` | The flowcraft project requires an audit trail for all automated workflow executions to support compl |
| exact memory content overlap | `v05_batch200_0067` | `v05_batch200_0067` | The routing service currently distributes tickets round-robin without considering agent current work |
| exact memory content overlap | `v05_batch200_0067` | `v05_batch200_0067` | Agent workload metrics are available in the agent_workload view which aggregates open ticket counts  |
| exact memory content overlap | `v05_batch200_0068` | `v05_batch200_0068` | The orders service validates payment before confirming an order but does not currently run fraud det |
| exact memory content overlap | `v05_batch200_0068` | `v05_batch200_0068` | The old fraud detection system was a separate service that has since been deprecated and its rules w |
| exact memory content overlap | `v05_batch200_0069` | `v05_batch200_0069` | The visualizer currently supports on-demand CSV export from any chart but requires manual user actio |
| exact memory content overlap | `v05_batch200_0069` | `v05_batch200_0069` | Export format configurations are in config/visualizer/exports.yaml with supported formats CSV, XLSX, |
| exact memory content overlap | `v05_batch200_0070` | `v05_batch200_0070` | The quiz generator creates quizzes with a configurable time limit per question but does not enforce  |
| exact memory content overlap | `v05_batch200_0070` | `v05_batch200_0070` | Quiz time limit settings are in config/quiz_generator/time_limits.yaml with per-topic defaults. |
| exact memory content overlap | `v05_batch200_0071` | `v05_batch200_0071` | The orchestrator executes workflow steps with full side effects on the first run. There is no previe |
| exact memory content overlap | `v05_batch200_0071` | `v05_batch200_0071` | The dry-run feature was requested by the QA team after a misconfigured workflow accidentally sent 50 |
| exact memory content overlap | `v05_batch200_0072` | `v05_batch200_0072` | The helpdesk project SLA requires quarterly reporting on ticket resolution times per agent team. |
| exact memory content overlap | `v05_batch200_0072` | `v05_batch200_0072` | The Q1 2026 SLA report was generated last month and sent to the operations director. |
| exact memory content overlap | `v05_batch200_0073` | `v05_batch200_0073` | The orders service processes refunds within 5 business days to the original payment method. |
| exact memory content overlap | `v05_batch200_0073` | `v05_batch200_0073` | The old refund processor used account credit only and was replaced in v3. |
| exact memory content overlap | `v05_batch200_0074` | `v05_batch200_0074` | The query engine guarantees data freshness within 15 minutes of the source data warehouse update. |
| exact memory content overlap | `v05_batch200_0074` | `v05_batch200_0074` | Data freshness is monitored by scripts/monitor/freshness_check.py which runs every 5 minutes. |
| exact memory content overlap | `v05_batch200_0075` | `v05_batch200_0075` | The progress tracker awards a completion certificate when a student completes 100% of modules with a |
| exact memory content overlap | `v05_batch200_0075` | `v05_batch200_0075` | The studybuddy project certificates are recognized for continuing education credits by the partner i |
| exact memory content overlap | `v05_batch200_0086` | `v05_batch200_0086` | The ticketing service sends a satisfaction survey 24 hours after ticket closure. |
| exact memory content overlap | `v05_batch200_0086` | `v05_batch200_0086` | The helpdesk project requires customer satisfaction data to be included in the monthly operations re |
| exact memory content overlap | `v05_batch200_0087` | `v05_batch200_0087` | The orders service currently ships an entire order from a single warehouse, even if items are in dif |
| exact memory content overlap | `v05_batch200_0087` | `v05_batch200_0087` | Warehouse inventory data is available via the inventory service API at /api/v2/inventory/warehouse/{ |
| exact memory content overlap | `v05_batch200_0088` | `v05_batch200_0088` | The query engine executes SQL directly against the data warehouse with no EXPLAIN or cost preview ca |
| exact memory content overlap | `v05_batch200_0088` | `v05_batch200_0088` | The last performance incident was caused by an unoptimized JOIN that scanned 50 million rows, resolv |
| exact memory content overlap | `v05_batch200_0089` | `v05_batch200_0089` | The quiz generator currently allows unlimited quiz attempts with no cooldown between retries. |
| exact memory content overlap | `v05_batch200_0089` | `v05_batch200_0089` | The student prefers to review incorrect answers before retaking a quiz rather than immediately retry |
| exact memory content overlap | `v05_batch200_0090` | `v05_batch200_0090` | The orchestrator currently defines workflows only through YAML files in the config/workflows/ direct |
| exact memory content overlap | `v05_batch200_0090` | `v05_batch200_0090` | Workflow YAML schema is documented in docs/workflows/yaml_schema.md with all supported step types an |
| exact memory content overlap | `v05_batch200_0091` | `v05_batch200_0091` | The routing service assigns tickets based on agent skills and availability but does not consider cus |
| exact memory content overlap | `v05_batch200_0091` | `v05_batch200_0091` | Agent language proficiencies are stored in the agent_languages table with columns agent_id, language |
| exact memory content overlap | `v05_batch200_0092` | `v05_batch200_0092` | The catalog service returns product details individually by product ID with no built-in comparison c |
| exact memory content overlap | `v05_batch200_0092` | `v05_batch200_0092` | The shopper prefers to compare products side-by-side on a maximum of 5 attributes: price, rating, si |
| exact memory content overlap | `v05_batch200_0093` | `v05_batch200_0093` | The scheduler sends reports to a fixed list of recipients configured per dashboard with no self-serv |
| exact memory content overlap | `v05_batch200_0093` | `v05_batch200_0093` | The databoard project requires all automated communications to include an unsubscribe link per data  |
| exact memory content overlap | `v05_batch200_0094` | `v05_batch200_0094` | The progress tracker records daily study activity but does not generate summary reports. |
| exact memory content overlap | `v05_batch200_0094` | `v05_batch200_0094` | The student prefers receiving progress updates on Monday mornings with a comparison to the previous  |
| exact memory content overlap | `v05_batch200_0095` | `v05_batch200_0095` | The orchestrator tracks workflow execution duration but does not enforce SLA deadlines. |
| exact memory content overlap | `v05_batch200_0095` | `v05_batch200_0095` | The flowcraft project SLA guarantees that critical workflows complete within 10 minutes of trigger. |
| exact memory content overlap | `v05_batch200_0096` | `v05_batch200_0096` | The ticketing service allows customers to create multiple tickets, which can result in duplicate iss |
| exact memory content overlap | `v05_batch200_0096` | `v05_batch200_0096` | Last month, 12% of critical tickets were duplicates of existing open tickets, causing wasted agent t |
| exact memory content overlap | `v05_batch200_0097` | `v05_batch200_0097` | The inventory service triggers alerts when stock falls below the reorder threshold but does not pred |
| exact memory content overlap | `v05_batch200_0097` | `v05_batch200_0097` | Historical sales data is available in the sales_history table with daily aggregates per product vari |
| exact memory content overlap | `v05_batch200_0098` | `v05_batch200_0098` | The visualizer renders charts from query results but does not support user-added annotations. |
| exact memory content overlap | `v05_batch200_0098` | `v05_batch200_0098` | The analyst prefers annotating charts with text notes directly on the data points rather than in a s |
| exact memory content overlap | `v05_batch200_0099` | `v05_batch200_0099` | The quiz generator assigns a difficulty level to each quiz based on the questions it contains but do |
| exact memory content overlap | `v05_batch200_0099` | `v05_batch200_0099` | The student is motivated by achievement badges and wants visible recognition for completing difficul |
| exact memory content overlap | `v05_batch200_0100` | `v05_batch200_0100` | The orchestrator requires every workflow to be defined from scratch in YAML with no template or copy |
| exact memory content overlap | `v05_batch200_0100` | `v05_batch200_0100` | The flowcraft project goal is to reduce workflow creation time by 50% through reusable templates and |
| exact memory content overlap | `v05_batch300_0001` | `v05_batch300_0001` | The case validator checks that every current unit appears exactly once in gold.store or gold.skip. |
| exact memory content overlap | `v05_batch300_0001` | `v05_batch300_0001` | Case validator source lives under src/v04/case_validator.py with tests under tests/v04/. |
| exact memory content overlap | `v05_batch300_0002` | `v05_batch300_0002` | The ticketing service closes tickets 7 days after resolution if the customer has not responded. |
| exact memory content overlap | `v05_batch300_0002` | `v05_batch300_0002` | Last week's operations review noted that 15% of tickets were closed while customers were still waiti |
| exact memory content overlap | `v05_batch300_0003` | `v05_batch300_0003` | The catalog service requires product images to be at least 500x500 pixels in WebP format. |
| exact memory content overlap | `v05_batch300_0003` | `v05_batch300_0003` | Image validation rules are in config/catalog/image_rules.yaml. |
| exact memory content overlap | `v05_batch300_0004` | `v05_batch300_0004` | The query engine times out after 30 seconds and returns partial results if the timeout is reached. |
| exact memory content overlap | `v05_batch300_0004` | `v05_batch300_0004` | Timeout configuration is in config/query_engine/timeouts.yaml with per-dashboard overrides. |
| exact memory content overlap | `v05_batch300_0005` | `v05_batch300_0005` | The search service uses TF-IDF ranking with title matches boosted by 2.0x. |
| exact memory content overlap | `v05_batch300_0005` | `v05_batch300_0005` | Search ranking configuration is in config/search/ranking_weights.json. |
| exact memory content overlap | `v05_batch300_0006` | `v05_batch300_0006` | The alerts service defines three severity levels: warning (<80% of average), critical (<50%), and in |
| exact memory content overlap | `v05_batch300_0006` | `v05_batch300_0006` | The finboard project requires all critical alerts to trigger a PagerDuty notification within 2 minut |
| exact memory content overlap | `v05_batch300_0007` | `v05_batch300_0007` | The pricing service calculates fares based on base fare plus mandatory taxes and a fuel surcharge pe |
| exact memory content overlap | `v05_batch300_0007` | `v05_batch300_0007` | Fare calculation formulas are documented in docs/pricing/fare_formulas.md. |
| exact memory content overlap | `v05_batch300_0008` | `v05_batch300_0008` | The grading service weights assignments at 40%, quizzes at 30%, and final exam at 30% by default. |
| exact memory content overlap | `v05_batch300_0008` | `v05_batch300_0008` | Grade weight overrides per course are in config/grading/course_weights.yaml. |
| exact memory content overlap | `v05_batch300_0009` | `v05_batch300_0009` | The asset pipeline compresses textures using ASTC 6x6 block compression at quality 90% for mobile ta |
| exact memory content overlap | `v05_batch300_0009` | `v05_batch300_0009` | Compression settings are in config/asset_pipeline/compression.yaml with per-platform overrides. |
| exact memory content overlap | `v05_batch300_0010` | `v05_batch300_0010` | The quiz generator requires multiple-choice questions to have exactly one correct answer and at leas |
| exact memory content overlap | `v05_batch300_0010` | `v05_batch300_0010` | Question format templates are in config/quiz_generator/formats/multiple_choice.json. |
| exact memory content overlap | `v05_batch300_0011` | `v05_batch300_0011` | The orchestrator retries failed workflow steps up to 3 times with exponential backoff before marking |
| exact memory content overlap | `v05_batch300_0011` | `v05_batch300_0011` | Retry configuration is in config/orchestrator/retry_policy.yaml. |
| exact memory content overlap | `v05_batch300_0012` | `v05_batch300_0012` | The camera module supports photo, video, slow-motion, and portrait modes. HDR is available in photo  |
| exact memory content overlap | `v05_batch300_0012` | `v05_batch300_0012` | Camera mode configuration is in config/camera/modes.yaml. |
| exact memory content overlap | `v05_batch300_0013` | `v05_batch300_0013` | The export job runs daily at 02:00 UTC and writes invoices to the S3 export bucket. |
| exact memory content overlap | `v05_batch300_0013` | `v05_batch300_0013` | Export schedule configuration is in config/export/schedule.yaml. |
| exact memory content overlap | `v05_batch300_0014` | `v05_batch300_0014` | The routing service imports agent shift schedules every 4 hours from CSV files in the shifts/import/ |
| exact memory content overlap | `v05_batch300_0014` | `v05_batch300_0014` | The last shift import failed due to a malformed CSV header in the workforce management export. |
| exact memory content overlap | `v05_batch300_0015` | `v05_batch300_0015` | The orders service transitions orders through pending → confirmed → shipped → delivered states. |
| exact memory content overlap | `v05_batch300_0015` | `v05_batch300_0015` | Order status transition rules are documented in docs/orders/status_workflow.md. |
| exact memory content overlap | `v05_batch300_0016` | `v05_batch300_0016` | The scheduler delivers reports as PDF attachments via email to the dashboard owner's registered emai |
| exact memory content overlap | `v05_batch300_0016` | `v05_batch300_0016` | Report delivery configuration is in config/scheduler/delivery.yaml with SMTP settings. |
| exact memory content overlap | `v05_batch300_0017` | `v05_batch300_0017` | The summarizer produces a maximum of 5 sentences per summary and never includes code blocks. |
| exact memory content overlap | `v05_batch300_0017` | `v05_batch300_0017` | Summarizer parameters are in config/summarizer/defaults.json. |
| exact memory content overlap | `v05_batch300_0018` | `v05_batch300_0018` | The visualizer refreshes chart data every 5 minutes when the dashboard is actively viewed. |
| exact memory content overlap | `v05_batch300_0018` | `v05_batch300_0018` | Refresh interval configuration is in config/visualizer/refresh.yaml. |
| exact memory content overlap | `v05_batch300_0050` | `v05_batch300_0050` | The pipeline retry wrapper retries transient network errors 3 times with 1-second backoff. |
| exact memory content overlap | `v05_batch300_0050` | `v05_batch300_0050` | Pipeline job logs are written to /var/log/pipeline/job_${RUN_ID}.log on the job runner host. |
| exact memory content overlap | `v05_batch300_0050` | `v05_batch300_0050` | The old v1 pipeline buffered all retry state in memory and lost it on crash. |
| exact memory content overlap | `v05_batch300_0051` | `v05_batch300_0051` | The notification service groups messages by priority before delivering via FCM, sending at most one  |
| exact memory content overlap | `v05_batch300_0051` | `v05_batch300_0051` | The current batching window of 2 minutes was chosen arbitrarily in January without load testing. |
| exact memory content overlap | `v05_batch300_0051` | `v05_batch300_0051` | The legacy push module sent every notification immediately with no batching, causing FCM rate-limit  |
| exact memory content overlap | `v05_batch300_0052` | `v05_batch300_0052` | The finboard project must comply with GDPR data minimization principles for all EU customer transact |
| exact memory content overlap | `v05_batch300_0052` | `v05_batch300_0052` | The aggregator currently stores raw transaction records with full customer name and account ID in th |
| exact memory content overlap | `v05_batch300_0052` | `v05_batch300_0052` | Anonymization rules are defined in config/aggregator/anonymization.yaml with a list of PII columns t |
| exact memory content overlap | `v05_batch300_0053` | `v05_batch300_0053` | The pricing service calls airline APIs with a rate limit of 100 requests per minute and caches respo |
| exact memory content overlap | `v05_batch300_0053` | `v05_batch300_0053` | Airline API integration documentation lives under docs/pricing/airline_apis/ with one markdown file  |
| exact memory content overlap | `v05_batch300_0054` | `v05_batch300_0054` | The grading service writes final grades to the submissions table with graded_at and grader_id column |
| exact memory content overlap | `v05_batch300_0054` | `v05_batch300_0054` | The learnhub project requires an immutable audit trail for all grade changes to meet accreditation s |
| exact memory content overlap | `v05_batch300_0054` | `v05_batch300_0054` | The grade_audit table schema is defined in db/migrations/grading/V003__grade_audit.sql. |
| exact memory content overlap | `v05_batch300_0055` | `v05_batch300_0055` | The build system compiles all shaders from source on every build, taking approximately 12 minutes fo |
| exact memory content overlap | `v05_batch300_0055` | `v05_batch300_0055` | Shader source files live under assets/shaders/ and compiled outputs go to build/shaders/{platform}/. |
| exact memory content overlap | `v05_batch300_0055` | `v05_batch300_0055` | The last build optimization attempt reduced texture compression time by 40% but didn't touch shader  |
| exact memory content overlap | `v05_batch300_0056` | `v05_batch300_0056` | The orders service uses idempotency keys for payment processing but not for order creation or status |
| exact memory content overlap | `v05_batch300_0056` | `v05_batch300_0056` | Idempotency key format is defined in docs/orders/idempotency.md as ORDER-{client_id}-{nonce}. |
| exact memory content overlap | `v05_batch300_0057` | `v05_batch300_0057` | The query engine currently runs all queries against a shared analytics database without tenant-scope |
| exact memory content overlap | `v05_batch300_0057` | `v05_batch300_0057` | The databoard project's multi-tenancy model assigns each organization a tenant_id that must be enfor |
| exact memory content overlap | `v05_batch300_0057` | `v05_batch300_0057` | Tenant configuration is managed in config/tenants/ with one YAML file per tenant containing the tena |
| exact memory content overlap | `v05_batch300_0058` | `v05_batch300_0058` | The routing service assigns tickets to agents based on skill tags and current workload, but does not |
| exact memory content overlap | `v05_batch300_0058` | `v05_batch300_0058` | The helpdesk project SLA mandates: critical tickets must receive first response within 1 hour, norma |
| exact memory content overlap | `v05_batch300_0058` | `v05_batch300_0058` | Last month's SLA report showed 8% of critical tickets breached the 1-hour first-response window. |
| exact memory content overlap | `v05_batch300_0059` | `v05_batch300_0059` | The indexer builds a single inverted index for all document versions, which causes stale results whe |
| exact memory content overlap | `v05_batch300_0059` | `v05_batch300_0059` | Document version tags are extracted from the docs repo's git tags following the pattern v{major}.{mi |
| exact memory content overlap | `v05_batch300_0060` | `v05_batch300_0060` | The orchestrator calls external services for each workflow step and retries on failure, but has no c |
| exact memory content overlap | `v05_batch300_0060` | `v05_batch300_0060` | Last week's production incident: the payment gateway was down for 45 minutes, and the orchestrator r |
| exact memory content overlap | `v05_batch300_0061` | `v05_batch300_0061` | The quiz generator currently selects questions randomly from the question bank without considering t |
| exact memory content overlap | `v05_batch300_0061` | `v05_batch300_0061` | Student quiz history is stored in the quiz_attempts table with columns student_id, question_id, corr |
| exact memory content overlap | `v05_batch300_0061` | `v05_batch300_0061` | The legacy flashcard system used static Leitner boxes with fixed intervals of 1, 3, 7, and 30 days. |
| exact memory content overlap | `v05_batch300_0062` | `v05_batch300_0062` | The prompt builder renders runtime_context, candidate_memories, and current_units into a structured  |
| exact memory content overlap | `v05_batch300_0062` | `v05_batch300_0062` | The parser validates model output against DSL rules: duplicate detection, missing unit assignment, u |
| exact memory content overlap | `v05_batch300_0062` | `v05_batch300_0062` | Prompt builder source is under src/v04/prompt_builder.py with tests under tests/v04/test_prompt_buil |
| exact memory content overlap | `v05_batch300_0063` | `v05_batch300_0063` | The orders service receives raw payment information from the checkout form and passes it to the paym |
| exact memory content overlap | `v05_batch300_0063` | `v05_batch300_0063` | The shopengine project PCI compliance policy prohibits storing raw card numbers in any service log,  |
| exact memory content overlap | `v05_batch300_0064` | `v05_batch300_0064` | The ticketing service supports merging duplicate tickets. When merged, the newer ticket is closed an |
| exact memory content overlap | `v05_batch300_0064` | `v05_batch300_0064` | Ticket merge rules are configured in config/ticketing/merge_rules.yaml with similarity thresholds fo |
| exact memory content overlap | `v05_batch300_0065` | `v05_batch300_0065` | The booking service currently reserves seats immediately upon payment authorization and issues the t |
| exact memory content overlap | `v05_batch300_0065` | `v05_batch300_0065` | Airline partner agreements require that held but unpaid bookings be released after 24 hours to avoid |
| exact memory content overlap | `v05_batch300_0065` | `v05_batch300_0065` | Booking hold configuration is managed in config/booking/hold_policy.yaml with airline-specific TTL v |
| exact memory content overlap | `v05_batch300_0066` | `v05_batch300_0066` | The dungeon-tools project currently ships in English only with no localization pipeline. |
| exact memory content overlap | `v05_batch300_0066` | `v05_batch300_0066` | UI string assets are stored in assets/strings/en/ with one JSON file per screen. |
| exact memory content overlap | `v05_batch300_0067` | `v05_batch300_0067` | The pipeline dead-letter queue stores records from stages that fail after 3 retries. The DLQ is neve |
| exact memory content overlap | `v05_batch300_0067` | `v05_batch300_0067` | The old v1 DLQ was stored in a flat file on the pipeline host and was lost during the 2025 data cent |
| exact memory content overlap | `v05_batch300_0067` | `v05_batch300_0067` | DLQ configuration is in config/pipeline/dlq.yaml with table name and connection string. |
| exact memory content overlap | `v05_batch300_0068` | `v05_batch300_0068` | The query engine returns all matching rows in a single response, limited to 50,000 rows. Queries exc |
| exact memory content overlap | `v05_batch300_0068` | `v05_batch300_0068` | The visualizer can only render up to 10,000 data points before performance degrades significantly. |
| exact memory content overlap | `v05_batch300_0069` | `v05_batch300_0069` | The search service ranks results by TF-IDF score with a 2.0x boost for title matches. It does not co |
| exact memory content overlap | `v05_batch300_0069` | `v05_batch300_0069` | Each indexed document has a last_modified timestamp extracted from git blame in data/indexer/documen |
| exact memory content overlap | `v05_batch300_0069` | `v05_batch300_0069` | The old search ranking used a static priority field set manually by doc editors, which was abandoned |
| exact memory content overlap | `v05_batch300_0070` | `v05_batch300_0070` | The sync offline queue stores pending edits in a local SQLite database at app/data/sync_queue.db wit |
| exact memory content overlap | `v05_batch300_0070` | `v05_batch300_0070` | The field-app project security policy requires all locally stored user data to be encrypted at rest  |
| exact memory content overlap | `v05_batch300_0071` | `v05_batch300_0071` | The finboard project currently has no formal disaster recovery plan beyond daily database snapshots. |
| exact memory content overlap | `v05_batch300_0071` | `v05_batch300_0071` | Database snapshots are stored in S3 under finboard-backups/daily/ with a 30-day retention policy man |
| exact memory content overlap | `v05_batch300_0072` | `v05_batch300_0072` | The grading service runs submissions through an external plagiarism detection API and receives a sim |
| exact memory content overlap | `v05_batch300_0072` | `v05_batch300_0072` | The learnhub academic integrity policy requires flagging submissions with similarity above 40% for i |
| exact memory content overlap | `v05_batch300_0073` | `v05_batch300_0073` | The orchestrator loads workflow definitions from config/workflows/ at startup and keeps them in memo |
| exact memory content overlap | `v05_batch300_0073` | `v05_batch300_0073` | Workflow YAML files are stored in a git repository under config/workflows/ and changes are deployed  |
| exact memory content overlap | `v05_batch300_0073` | `v05_batch300_0073` | Last week a YAML syntax error in the order_fulfillment workflow caused all active orders to enter an |
| exact memory content overlap | `v05_batch300_0074` | `v05_batch300_0074` | The progress tracker stores per-student data in the student_progress table: modules completed, quiz  |
| exact memory content overlap | `v05_batch300_0074` | `v05_batch300_0074` | The studybuddy project must comply with GDPR data portability requirements: users can request a mach |
| exact memory content overlap | `v05_batch300_0074` | `v05_batch300_0074` | Data export templates are under templates/exports/ with one JSON schema per export type. |
| exact memory content overlap | `v05_batch300_0075` | `v05_batch300_0075` | The camera module requests camera permission on first launch. If denied, it shows a generic error me |
| exact memory content overlap | `v05_batch300_0075` | `v05_batch300_0075` | Camera permission strings are defined in app/src/main/res/values/strings.xml under the camera_permis |
| exact memory content overlap | `v05_batch300_0076` | `v05_batch300_0076` | The asset pipeline runs validation checks (texture dimensions, format, compression level) during the |
| exact memory content overlap | `v05_batch300_0076` | `v05_batch300_0076` | The CI pipeline is defined in .github/workflows/build.yml and currently runs unit tests and a smoke  |
| exact memory content overlap | `v05_batch300_0077` | `v05_batch300_0077` | The pricing service converts all fares to the user's preferred currency using a real-time exchange r |
| exact memory content overlap | `v05_batch300_0077` | `v05_batch300_0077` | Exchange rate cache is stored in Redis with key pattern fx:{from_currency}:{to_currency} and a TTL o |
| exact memory content overlap | `v05_batch300_0077` | `v05_batch300_0077` | The legacy pricing module showed prices in the airline's native currency only and required the user  |
| exact memory content overlap | `v05_batch300_0078` | `v05_batch300_0078` | The docs-assistant project currently has no formal API version compatibility policy; new features ma |
| exact memory content overlap | `v05_batch300_0078` | `v05_batch300_0078` | API endpoint definitions are in src/api/routes.py with version prefixes like /api/v1/. |
| exact memory content overlap | `v05_batch300_0079` | `v05_batch300_0079` | The export job writes files to S3 with inconsistent naming: some use dates, some use sequential numb |
| exact memory content overlap | `v05_batch300_0079` | `v05_batch300_0079` | S3 bucket structure is documented in docs/export/s3_layout.md but is currently outdated. |
| exact memory content overlap | `v05_batch300_0080` | `v05_batch300_0080` | The routing service assigns tickets based on agent skill tags and current workload, without consider |
| exact memory content overlap | `v05_batch300_0080` | `v05_batch300_0080` | Customer sentiment is extracted from ticket body text by a separate NLP service that returns a score |
| exact memory content overlap | `v05_batch300_0081` | `v05_batch300_0081` | The inventory service reserves stock for 15 minutes when a user adds an item to cart. Expired reserv |
| exact memory content overlap | `v05_batch300_0081` | `v05_batch300_0081` | The notification service supports push notifications via Firebase Cloud Messaging with a 30-second d |
| exact memory content overlap | `v05_batch300_0082` | `v05_batch300_0082` | The scheduler runs reports on a cron schedule and emails the PDF output to the dashboard owner. If r |
| exact memory content overlap | `v05_batch300_0082` | `v05_batch300_0082` | Scheduler job definitions are in config/scheduler/jobs.yaml with per-report schedule, recipient, and |
| exact memory content overlap | `v05_batch300_0083` | `v05_batch300_0083` | The enrollment service enforces a hard cap of 50 students per course and rejects enrollment when the |
| exact memory content overlap | `v05_batch300_0083` | `v05_batch300_0083` | Course capacity limits are configured in config/courses/capacity.yaml with keys max_students and ove |
| exact memory content overlap | `v05_batch300_0083` | `v05_batch300_0083` | Last semester, 12% of enrolled students dropped courses in the first two weeks, leaving unfilled sea |
| exact memory content overlap | `v05_batch300_0084` | `v05_batch300_0084` | The aggregator ingests transaction data from a single source (the primary payment processor) with no |
| exact memory content overlap | `v05_batch300_0084` | `v05_batch300_0084` | The finboard project requires transaction data to be reconciled across at least two independent sour |
| exact memory content overlap | `v05_batch300_0085` | `v05_batch300_0085` | The build system produces unsigned binaries for all platforms. Release builds are signed manually by |
| exact memory content overlap | `v05_batch300_0085` | `v05_batch300_0085` | Code signing certificates are stored in a hardware security module (HSM) accessed via scripts/sign/s |
| exact memory content overlap | `v05_batch300_0086` | `v05_batch300_0086` | The sync module can tag records with GPS coordinates but does not currently ask for location permiss |
| exact memory content overlap | `v05_batch300_0086` | `v05_batch300_0086` | The field-app project privacy policy requires explicit opt-in consent before collecting or storing l |
| exact memory content overlap | `v05_batch300_0087` | `v05_batch300_0087` | The orchestrator currently has a global workflow timeout of 60 minutes but no per-step timeouts. |
| exact memory content overlap | `v05_batch300_0087` | `v05_batch300_0087` | Workflow step definitions in config/workflows/ can include an optional timeout_seconds field, but it |
| exact memory content overlap | `v05_batch300_0087` | `v05_batch300_0087` | Last month a stuck API call in the payment_verification step caused the entire order_fulfillment wor |
| exact memory content overlap | `v05_batch300_0088` | `v05_batch300_0088` | The quiz generator selects questions randomly from the question bank filtered by topic and format, w |
| exact memory content overlap | `v05_batch300_0088` | `v05_batch300_0088` | Questions in the question_bank table have a difficulty column with values easy, medium, or hard. |
| exact memory content overlap | `v05_batch300_0088` | `v05_batch300_0088` | The student prefers challenging quizzes and has indicated frustration with repetitive easy questions |
| exact memory content overlap | `v05_batch300_0089` | `v05_batch300_0089` | The case validator checks structural validity of individual cases and DSL consistency but does not c |
| exact memory content overlap | `v05_batch300_0089` | `v05_batch300_0089` | Case validator source is under src/v04/case_validator.py with the validation logic in validate_case( |
| exact memory content overlap | `v05_batch300_0089` | `v05_batch300_0089` | The v0.5 training plan requires train/dev/gold splits with zero leakage: no case text may appear in  |
| exact memory content overlap | `v05_batch300_0090` | `v05_batch300_0090` | The search service currently has no rate limiting — any user can make unlimited requests. |
| exact memory content overlap | `v05_batch300_0090` | `v05_batch300_0090` | API gateway configuration is in config/gateway/rate_limits.yaml with per-endpoint limits. |
| exact memory content overlap | `v05_batch300_0090` | `v05_batch300_0090` | Last month's traffic analysis showed one IP making 50,000 search requests in a single hour, degradin |
| exact memory content overlap | `v05_batch300_0091` | `v05_batch300_0091` | The ticketing service requires manual category assignment (billing, technical, account, feedback) vi |
| exact memory content overlap | `v05_batch300_0091` | `v05_batch300_0091` | Ticket categories are defined in config/ticketing/categories.yaml with a list of valid category IDs  |
| exact memory content overlap | `v05_batch300_0091` | `v05_batch300_0091` | The old categorization system used keyword matching with a fixed list of 200 trigger words, which ha |
| exact memory content overlap | `v05_batch300_0092` | `v05_batch300_0092` | The orders service currently fulfills each order from a single warehouse. If items are in different  |
| exact memory content overlap | `v05_batch300_0092` | `v05_batch300_0092` | The inventory service tracks stock levels per warehouse in the warehouse_inventory table with column |
| exact memory content overlap | `v05_batch300_0093` | `v05_batch300_0093` | The pipeline pushes data through stages sequentially with no flow control. If a downstream stage is  |
| exact memory content overlap | `v05_batch300_0093` | `v05_batch300_0093` | Pipeline stage buffer sizes are configured in config/pipeline/buffers.yaml with per-stage queue_capa |
| exact memory content overlap | `v05_batch300_0094` | `v05_batch300_0094` | The alerts service logs all alert firings to the alert_history table but the table allows UPDATE and |
| exact memory content overlap | `v05_batch300_0094` | `v05_batch300_0094` | The finboard project must maintain an immutable audit trail of all financial alerts for regulatory c |
| exact memory content overlap | `v05_batch300_0095` | `v05_batch300_0095` | The pricing service displays fares from airline APIs with a small markup. There is currently no pric |
| exact memory content overlap | `v05_batch300_0095` | `v05_batch300_0095` | The voyager project price match policy: if a customer finds a lower price on a competitor site withi |
| exact memory content overlap | `v05_batch300_0095` | `v05_batch300_0095` | Competitor price monitoring runs hourly via scripts/monitor_competitors.py and stores results in the |
| exact memory content overlap | `v05_batch300_0096` | `v05_batch300_0096` | The eval_runner expects model outputs in exactly the Unit DSL format and fails on any deviation. |
| exact memory content overlap | `v05_batch300_0096` | `v05_batch300_0096` | The parser can parse Unit DSL, Legacy Span JSON, and Unit JSON formats and returns a canonical repre |
| exact memory content overlap | `v05_batch300_0096` | `v05_batch300_0096` | Eval runner code lives under src/v04/eval_runner.py and uses the parser module from src/v04/parser.p |
| exact memory content overlap | `v05_batch300_0097` | `v05_batch300_0097` | The orders service tracks cart state but does not send reminders when a cart is abandoned. |
| exact memory content overlap | `v05_batch300_0097` | `v05_batch300_0097` | Email templates for transactional messages are stored in templates/email/transactions/ with one HTML |
| exact memory content overlap | `v05_batch300_0097` | `v05_batch300_0097` | The notification service has a daily email budget of 50,000 messages to avoid being flagged as spam. |
| exact memory content overlap | `v05_batch300_0098` | `v05_batch300_0098` | The scheduler generates PDF reports and emails them to recipients without any watermarking or downlo |
| exact memory content overlap | `v05_batch300_0098` | `v05_batch300_0098` | The databoard project requires all exported reports to include a recipient-specific watermark to det |
| exact memory content overlap | `v05_batch300_0099` | `v05_batch300_0099` | The sync module processes the offline queue in strict FIFO order regardless of entry type or urgency |
| exact memory content overlap | `v05_batch300_0099` | `v05_batch300_0099` | Queue entry types are defined in the sync_queue table with a record_type column containing values li |
| exact memory content overlap | `v05_batch300_0100` | `v05_batch300_0100` | The enrollment service blocks enrollment if prerequisites are not completed with a passing grade. Th |
| exact memory content overlap | `v05_batch300_0100` | `v05_batch300_0100` | The learnhub academic policy allows prerequisite waivers at the instructor's discretion for students |
| exact memory content overlap | `v05_batch300_0100` | `v05_batch300_0100` | Course prerequisite definitions are in config/courses/prerequisites.yaml with a list of required cou |
| exact memory content overlap | `v05_batch500_0001` | `v05_batch500_0001` | The ticket router assigns incoming tickets to agents based on skill tags and current queue depth. |
| exact memory content overlap | `v05_batch500_0001` | `v05_batch500_0001` | The current routing uses round-robin assignment without considering agent expertise. |
| exact memory content overlap | `v05_batch500_0002` | `v05_batch500_0002` | The metricboard project requires that all user-uploaded data be retained for 90 days after account d |
| exact memory content overlap | `v05_batch500_0002` | `v05_batch500_0002` | Data retention configurations are in config/retention/policies.yaml with per-dataset overrides. |
| exact memory content overlap | `v05_batch500_0003` | `v05_batch500_0003` | The patient portal currently allows booking appointments in 15-minute slots without checking provide |
| exact memory content overlap | `v05_batch500_0003` | `v05_batch500_0003` | The medflow project must comply with HIPAA data handling requirements for all patient-facing service |
| exact memory content overlap | `v05_batch500_0004` | `v05_batch500_0004` | The inventory sync service polls warehouse databases every 5 minutes and updates the central invento |
| exact memory content overlap | `v05_batch500_0004` | `v05_batch500_0004` | Alert threshold configuration per SKU is stored in config/inventory/alert_thresholds.yaml. |
| exact memory content overlap | `v05_batch500_0005` | `v05_batch500_0005` | The contract parser extracts clauses by section number and categorizes them as obligation, liability |
| exact memory content overlap | `v05_batch500_0005` | `v05_batch500_0005` | The clausekeeper project does not provide legal advice; it only structures and indexes contract text |
| exact memory content overlap | `v05_batch500_0006` | `v05_batch500_0006` | The render farm processes jobs in FIFO order across a pool of 8 GPU workers with per-job timeout of  |
| exact memory content overlap | `v05_batch500_0006` | `v05_batch500_0006` | Render job configurations including frame ranges and output formats are defined in jobs/<job_id>/ren |
| exact memory content overlap | `v05_batch500_0007` | `v05_batch500_0007` | The ingestion service parses CSV files using a schema defined in the data catalog and rejects rows w |
| exact memory content overlap | `v05_batch500_0007` | `v05_batch500_0007` | The old v1 ingestion used a fixed-width parser that could not handle quoted fields. |
| exact memory content overlap | `v05_batch500_0007` | `v05_batch500_0007` | Last month's ingestion bug was caused by a UTF-8 BOM in the header row of the finance department CSV |
| exact memory content overlap | `v05_batch500_0008` | `v05_batch500_0008` | The catalog search uses Elasticsearch with BM25 scoring and a synonym filter for common product name |
| exact memory content overlap | `v05_batch500_0008` | `v05_batch500_0008` | The previous search ranking experiment used learning-to-rank with user click data but was rolled bac |
| exact memory content overlap | `v05_batch500_0008` | `v05_batch500_0008` | Search index mappings are defined in elasticsearch/mappings/catalog_v3.json. |
| exact memory content overlap | `v05_batch500_0009` | `v05_batch500_0009` | The SFT message renderer converts case JSON records into chat-format messages with system, user, and |
| exact memory content overlap | `v05_batch500_0009` | `v05_batch500_0009` | The v0.4 interface pilot compared three interfaces; v0.5 uses only Unit DSL for training. |
| exact memory content overlap | `v05_batch500_0009` | `v05_batch500_0009` | The old v0.3 prompt builder used a single monolithic prompt without role separation. |
| exact memory content overlap | `v05_batch500_0010` | `v05_batch500_0010` | User preferences for the finboard dashboard are stored in the user_settings table with per-widget ov |
| exact memory content overlap | `v05_batch500_0010` | `v05_batch500_0010` | The alert service sends notifications based on user-configured thresholds and channels. |
| exact memory content overlap | `v05_batch500_0011` | `v05_batch500_0011` | The helpdesk ticket system supports configurable agent views with saved filters and column layouts. |
| exact memory content overlap | `v05_batch500_0011` | `v05_batch500_0011` | The current agent view customization is limited to column visibility only; full layout customization |
| exact memory content overlap | `v05_batch500_0012` | `v05_batch500_0012` | The location tracker samples GPS coordinates every 60 seconds and evaluates geofence membership usin |
| exact memory content overlap | `v05_batch500_0012` | `v05_batch500_0012` | The user prefers location-based alerts to be delivered as silent notifications that appear in the no |
| exact memory content overlap | `v05_batch500_0013` | `v05_batch500_0013` | The version manager tracks documentation versions by git commit hash and stores rendered HTML snapsh |
| exact memory content overlap | `v05_batch500_0013` | `v05_batch500_0013` | Versioned documentation is accessible at /docs/v<major>.<minor>/ and the latest alias always points  |
| exact memory content overlap | `v05_batch500_0014` | `v05_batch500_0014` | The step executor runs workflow steps sequentially and passes output context as JSON between steps. |
| exact memory content overlap | `v05_batch500_0014` | `v05_batch500_0014` | Workflow definitions are stored as YAML files in workflows/ with a schema validated at load time. |
| exact memory content overlap | `v05_batch500_0015` | `v05_batch500_0015` | The voyager project committed to WCAG 2.1 AA compliance for all customer-facing interfaces by Q3 202 |
| exact memory content overlap | `v05_batch500_0015` | `v05_batch500_0015` | Accessibility test suites are under tests/a11y/ and run as part of the CI pipeline. |
| exact memory content overlap | `v05_batch500_0016` | `v05_batch500_0016` | The assessment engine selects questions from a pool tagged by difficulty level and topic, using a fi |
| exact memory content overlap | `v05_batch500_0016` | `v05_batch500_0016` | The current question pool has 2400 questions across 12 topics, with medium-difficulty questions comp |
| exact memory content overlap | `v05_batch500_0017` | `v05_batch500_0017` | The physics engine simulates rigid-body collisions at 60Hz using the Bullet physics SDK with a fixed |
| exact memory content overlap | `v05_batch500_0017` | `v05_batch500_0017` | Physics collision meshes are stored under assets/physics/collision/ in the Wavefront OBJ format. |
| exact memory content overlap | `v05_batch500_0018` | `v05_batch500_0018` | The quality checker validates pipeline output tables against schema constraints and row-count expect |
| exact memory content overlap | `v05_batch500_0018` | `v05_batch500_0018` | The data-platform quality SLA requires that all data anomalies are detected within 30 minutes of pip |
| exact memory content overlap | `v05_batch500_0019` | `v05_batch500_0019` | The data importer accepts CSV and JSON files, validates them against target table schemas, and inser |
| exact memory content overlap | `v05_batch500_0019` | `v05_batch500_0019` | Import configurations including column mappings are stored in config/imports/<dataset_name>.yaml. |
| exact memory content overlap | `v05_batch500_0020` | `v05_batch500_0020` | The quiz generator creates multiple-choice questions from study material by extracting key facts and |
| exact memory content overlap | `v05_batch500_0020` | `v05_batch500_0020` | The current distractors are random sentences from unrelated topics, which learners find too easy to  |
| exact memory content overlap | `v05_batch500_0021` | `v05_batch500_0021` | The route optimizer computes delivery routes using the Google OR-Tools constraint solver with time w |
| exact memory content overlap | `v05_batch500_0021` | `v05_batch500_0021` | The logistix project must keep all delivery route computation on-premise; no third-party cloud routi |
| exact memory content overlap | `v05_batch500_0022` | `v05_batch500_0022` | The obligation tracker extracts dated commitments from contract clauses and stores them with their d |
| exact memory content overlap | `v05_batch500_0022` | `v05_batch500_0022` | The clausekeeper project does not send legal notices or act as a registered agent; all communication |
| exact memory content overlap | `v05_batch500_0023` | `v05_batch500_0023` | The appointment scheduler manages provider calendars with 15-minute slots and enforces a maximum of  |
| exact memory content overlap | `v05_batch500_0023` | `v05_batch500_0023` | The medflow project requires all telehealth sessions to use the approved video platform MedLink; no  |
| exact memory content overlap | `v05_batch500_0024` | `v05_batch500_0024` | The asset compiler bundles individual texture files into texture atlases using a max-rectangle bin-p |
| exact memory content overlap | `v05_batch500_0024` | `v05_batch500_0024` | Texture source files live under assets/textures/ and compiled atlases are output to build/atlases/ w |
| exact memory content overlap | `v05_batch500_0025` | `v05_batch500_0025` | The payment gateway tokenizes credit card data via Stripe and stores only the payment token and last |
| exact memory content overlap | `v05_batch500_0025` | `v05_batch500_0025` | Payment provider adapters live under src/payment/adapters/ and each implements the PaymentProvider i |
| exact memory content overlap | `v05_batch500_0026` | `v05_batch500_0026` | The trigger manager currently supports cron schedules and message queue triggers for starting workfl |
| exact memory content overlap | `v05_batch500_0026` | `v05_batch500_0026` | Trigger configurations are defined in workflows/<name>/triggers.yaml and support multiple trigger ty |
| exact memory content overlap | `v05_batch500_0027` | `v05_batch500_0027` | The finboard project uses Kubernetes for deployment with environment-specific overlays in k8s/overla |
| exact memory content overlap | `v05_batch500_0027` | `v05_batch500_0027` | The staging environment currently runs on a single-node cluster; scaling to 3 nodes is planned for l |
| exact memory content overlap | `v05_batch500_0028` | `v05_batch500_0028` | The loyalty engine awards points for completed bookings at a base rate of 1 point per dollar spent. |
| exact memory content overlap | `v05_batch500_0028` | `v05_batch500_0028` | The voyager loyalty program has three tiers: Silver, Gold, and Platinum, with increasing benefits at |
| exact memory content overlap | `v05_batch500_0029` | `v05_batch500_0029` | The sentiment analyzer scores each customer message on a -1.0 to 1.0 sentiment scale and tags messag |
| exact memory content overlap | `v05_batch500_0029` | `v05_batch500_0029` | Sentiment model weights are loaded from models/sentiment/bert_finetuned_v2.pt and updated monthly. |
| exact memory content overlap | `v05_batch500_0030` | `v05_batch500_0030` | The code linker parses source code comments for @doc annotations and creates hyperlinks from documen |
| exact memory content overlap | `v05_batch500_0030` | `v05_batch500_0030` | Code-to-doc mappings are stored in a SQLite database at data/code_links.db with schema version 3. |
| exact memory content overlap | `v05_batch500_0031` | `v05_batch500_0031` | The case generator produces JSONL case records following the v0.4 case schema with structural valida |
| exact memory content overlap | `v05_batch500_0031` | `v05_batch500_0031` | The v0.5 generation policy requires no templates, no fill-in-the-blank patterns, and unique semantic |
| exact memory content overlap | `v05_batch500_0032` | `v05_batch500_0032` | The chart renderer generates SVG charts from aggregated query results and supports bar, line, pie, a |
| exact memory content overlap | `v05_batch500_0032` | `v05_batch500_0032` | Chart templates and color palettes are defined in config/charts/ and use a JSON schema validated at  |
| exact memory content overlap | `v05_batch500_0033` | `v05_batch500_0033` | CI workflows are defined in .github/workflows/ and trigger on pull_request events against the main b |
| exact memory content overlap | `v05_batch500_0033` | `v05_batch500_0033` | The finboard project requires that all PRs pass linting, unit tests, and integration tests before me |
| exact memory content overlap | `v05_batch500_0034` | `v05_batch500_0034` | The plagiarism checker compares each submission against a library of known sources using n-gram fing |
| exact memory content overlap | `v05_batch500_0034` | `v05_batch500_0034` | The current plagiarism check runs only against the public web index, not against other student submi |
| exact memory content overlap | `v05_batch500_0035` | `v05_batch500_0035` | The dialogue system selects NPC responses from a dialogue tree based on player choices and faction r |
| exact memory content overlap | `v05_batch500_0035` | `v05_batch500_0035` | Dialogue trees are authored in YAML files under content/dialogue/<character_id>/ and support branchi |
| exact memory content overlap | `v05_batch500_0036` | `v05_batch500_0036` | The offline storage module persists user edits in a local SQLite database and syncs them to the serv |
| exact memory content overlap | `v05_batch500_0036` | `v05_batch500_0036` | The current sync uses last-write-wins conflict resolution, which can silently discard concurrent edi |
| exact memory content overlap | `v05_batch500_0037` | `v05_batch500_0037` | The schema registry stores Avro schemas for all pipeline topics and enforces unique schema IDs per t |
| exact memory content overlap | `v05_batch500_0037` | `v05_batch500_0037` | The data-platform requires BACKWARD compatibility for all schema changes to production topics; FORWA |
| exact memory content overlap | `v05_batch500_0038` | `v05_batch500_0038` | Database migrations for medflow are managed with Alembic and stored in db/migrations/ with timestamp |
| exact memory content overlap | `v05_batch500_0038` | `v05_batch500_0038` | The current production database is PostgreSQL 14; migration to PostgreSQL 16 is planned for the next |
| exact memory content overlap | `v05_batch500_0039` | `v05_batch500_0039` | The demand forecaster predicts daily SKU demand using a moving average of the last 28 days with expo |
| exact memory content overlap | `v05_batch500_0039` | `v05_batch500_0039` | Forecast model parameters are stored in config/forecasting/models.yaml and can be overridden per war |
| exact memory content overlap | `v05_batch500_0040` | `v05_batch500_0040` | The redaction engine applies manual redaction marks defined by attorneys and renders redacted PDFs w |
| exact memory content overlap | `v05_batch500_0040` | `v05_batch500_0040` | The clausekeeper project must never automatically delete or modify the original document; redactions |
| exact memory content overlap | `v05_batch500_0041` | `v05_batch500_0041` | The version control system stores project revisions as immutable snapshots referenced by SHA-256 has |
| exact memory content overlap | `v05_batch500_0041` | `v05_batch500_0041` | Version history is stored under .artisan/versions/ and the current HEAD pointer is in .artisan/HEAD. |
| exact memory content overlap | `v05_batch500_0042` | `v05_batch500_0042` | The shopengine project requires GDPR-compliant data handling with right-to-erasure support within 30 |
| exact memory content overlap | `v05_batch500_0042` | `v05_batch500_0042` | The order service retains completed order data for 2 years before anonymization. |
| exact memory content overlap | `v05_batch500_0043` | `v05_batch500_0043` | The progress tracker logs lesson completions, quiz scores, and time spent per topic to compute a com |
| exact memory content overlap | `v05_batch500_0043` | `v05_batch500_0043` | The current progress metric is a simple lesson-completion ratio that does not account for quiz perfo |
| exact memory content overlap | `v05_batch500_0044` | `v05_batch500_0044` | Release artifacts are built by the CI pipeline and stored in the releases/ directory with version-ta |
| exact memory content overlap | `v05_batch500_0044` | `v05_batch500_0044` | The current release process is manual and takes about 2 hours; automating the changelog generation a |
| exact memory content overlap | `v05_batch500_0045` | `v05_batch500_0045` | The macros engine lets agents define reusable response templates with variable substitution for cust |
| exact memory content overlap | `v05_batch500_0045` | `v05_batch500_0045` | Macros are stored as YAML files in config/macros/ and can reference other macros by name. |
| exact memory content overlap | `v05_batch500_0046` | `v05_batch500_0046` | The search index builds a full-text index over documentation content and returns results ranked by T |
| exact memory content overlap | `v05_batch500_0046` | `v05_batch500_0046` | Index settings including tokenizer, stop words, and boost fields are in config/search/index_settings |
| exact memory content overlap | `v05_batch500_0047` | `v05_batch500_0047` | The fraud detector scores each booking attempt on a 0-100 risk scale using rules for IP-geolocation  |
| exact memory content overlap | `v05_batch500_0047` | `v05_batch500_0047` | Fraud rules are configured in config/fraud/rules.yaml with per-rule weight and action (flag, block,  |
| exact memory content overlap | `v05_batch500_0048` | `v05_batch500_0048` | The data validator checks that imported data matches the target schema and that numeric columns fall |
| exact memory content overlap | `v05_batch500_0048` | `v05_batch500_0048` | The finboard project requires daily reconciliation between the trading system and the accounting led |
| exact memory content overlap | `v05_batch500_0049` | `v05_batch500_0049` | The label auditor runs structural validation on case records and reports any schema violations. |
| exact memory content overlap | `v05_batch500_0049` | `v05_batch500_0049` | v0.5 data policy requires that all 'Add/Implement/Build' phrasing defaults to task_state unless dura |
| exact memory content overlap | `v05_batch500_0050` | `v05_batch500_0050` | The dashboard builder renders widgets from saved queries and supports drag-and-drop layout with resi |
| exact memory content overlap | `v05_batch500_0050` | `v05_batch500_0050` | Dashboard definitions are stored as JSON in dashboards/<dashboard_id>.json with widget and layout se |
| exact memory content overlap | `v05_batch500_0051` | `v05_batch500_0051` | The course builder allows instructors to define course modules, lessons, and quizzes with ordering c |
| exact memory content overlap | `v05_batch500_0051` | `v05_batch500_0051` | The current prerequisite system only supports direct prerequisites, not transitive chains. |
| exact memory content overlap | `v05_batch500_0052` | `v05_batch500_0052` | The animation blender interpolates between animation clips using blend trees parameterized by charac |
| exact memory content overlap | `v05_batch500_0052` | `v05_batch500_0052` | Animation clip data is stored under assets/animations/ in the studio's custom .ganim format. |
| exact memory content overlap | `v05_batch500_0053` | `v05_batch500_0053` | Prometheus metrics are exposed on port 9090 at /metrics and alerting rules are in prometheus/rules/a |
| exact memory content overlap | `v05_batch500_0053` | `v05_batch500_0053` | The helpdesk project SLA requires 99.5% uptime for the ticket API and 99.9% for the agent dashboard. |
| exact memory content overlap | `v05_batch500_0054` | `v05_batch500_0054` | The recommendation engine currently uses content-based filtering by comparing product attributes (ca |
| exact memory content overlap | `v05_batch500_0054` | `v05_batch500_0054` | Recommendation model weights are stored in models/recommendations/ and loaded at service startup. |
| exact memory content overlap | `v05_batch500_0055` | `v05_batch500_0055` | The partition manager creates date-partitioned tables and manages retention by dropping partitions o |
| exact memory content overlap | `v05_batch500_0055` | `v05_batch500_0055` | The data-platform requires that archived data be stored in cold storage for 7 years before permanent |
| exact memory content overlap | `v05_batch500_0056` | `v05_batch500_0056` | The push notifier sends individual notifications to devices and tracks delivery status with receipts |
| exact memory content overlap | `v05_batch500_0056` | `v05_batch500_0056` | Notification templates and channel configurations are in config/notifications/channels.yaml. |
| exact memory content overlap | `v05_batch500_0057` | `v05_batch500_0057` | Unit tests live under tests/unit/ and run with pytest, integration tests under tests/integration/ re |
| exact memory content overlap | `v05_batch500_0057` | `v05_batch500_0057` | The current test suite takes 25 minutes to run; parallelizing integration tests across 4 workers is  |
| exact memory content overlap | `v05_batch500_0058` | `v05_batch500_0058` | The lab results processor ingests HL7 ORU messages, extracts test results with reference ranges, and |
| exact memory content overlap | `v05_batch500_0058` | `v05_batch500_0058` | Reference ranges per test are configured in config/lab/reference_ranges.yaml and updated when the la |
| exact memory content overlap | `v05_batch500_0059` | `v05_batch500_0059` | The warehouse allocator assigns incoming orders to warehouse zones based on inventory availability a |
| exact memory content overlap | `v05_batch500_0059` | `v05_batch500_0059` | Warehouse zone maps are defined in config/warehouses/<id>/zone_map.geojson with shelf coordinates. |
| exact memory content overlap | `v05_batch500_0060` | `v05_batch500_0060` | The expiry tracker monitors contract end dates and sends notifications 90, 60, and 30 days before ex |
| exact memory content overlap | `v05_batch500_0060` | `v05_batch500_0060` | The clausekeeper project does not initiate contract renewals; it only notifies responsible parties o |
| exact memory content overlap | `v05_batch500_0061` | `v05_batch500_0061` | The export manager renders project files to PNG and JPEG formats at configurable resolutions. |
| exact memory content overlap | `v05_batch500_0061` | `v05_batch500_0061` | Export presets are stored in config/export/presets.yaml with format, resolution, and quality setting |
| exact memory content overlap | `v05_batch500_0062` | `v05_batch500_0062` | All tutorai services load configuration from YAML files under config/<service>/ with environment var |
| exact memory content overlap | `v05_batch500_0062` | `v05_batch500_0062` | The user prefers course materials in video format with subtitles enabled by default for all content. |
| exact memory content overlap | `v05_batch500_0063` | `v05_batch500_0063` | The alert manager triggers notifications when a metric crosses a static threshold for a configurable |
| exact memory content overlap | `v05_batch500_0063` | `v05_batch500_0063` | Alert rules are defined in config/alerts/rules.yaml and support comparison operators gt, lt, gte, lt |
| exact memory content overlap | `v05_batch500_0064` | `v05_batch500_0064` | The check-in service submits passenger details to airline APIs and retrieves boarding passes 24 hour |
| exact memory content overlap | `v05_batch500_0064` | `v05_batch500_0064` | The user prefers aisle seats in the front half of the aircraft for flights longer than 3 hours. |
| exact memory content overlap | `v05_batch500_0065` | `v05_batch500_0065` | The project uses pip-tools to pin dependencies in requirements.txt and requirements-dev.txt. |
| exact memory content overlap | `v05_batch500_0065` | `v05_batch500_0065` | The current dependency pins are 3 months old; updating to latest compatible versions is needed for t |
| exact memory content overlap | `v05_batch500_0066` | `v05_batch500_0066` | The knowledge base serves help articles to both agents and customers, with articles tagged by produc |
| exact memory content overlap | `v05_batch500_0066` | `v05_batch500_0066` | Knowledge base articles live under content/kb/<product>/<article_id>.md with frontmatter metadata. |
| exact memory content overlap | `v05_batch500_0067` | `v05_batch500_0067` | Docker images are built from Dockerfile in each service directory and pushed to the project containe |
| exact memory content overlap | `v05_batch500_0067` | `v05_batch500_0067` | The finboard project requires all production container images to be signed with Cosign and verified  |
| exact memory content overlap | `v05_batch500_0068` | `v05_batch500_0068` | The translator converts documentation pages from English to target languages using a neural MT model |
| exact memory content overlap | `v05_batch500_0068` | `v05_batch500_0068` | Translation glossaries are stored in data/glossaries/<lang>.json and contain domain-specific term ma |
| exact memory content overlap | `v05_batch500_0069` | `v05_batch500_0069` | The shopengine project requires all services to use OAuth 2.0 with OpenID Connect for user authentic |
| exact memory content overlap | `v05_batch500_0069` | `v05_batch500_0069` | OAuth client configurations are stored in config/auth/clients.yaml with per-service client IDs and s |
| exact memory content overlap | `v05_batch500_0070` | `v05_batch500_0070` | The training logger records loss, learning rate, and gradient norm at each training step to TensorBo |
| exact memory content overlap | `v05_batch500_0070` | `v05_batch500_0070` | The v0.5 evaluation philosophy prioritizes routing-specific metrics (STORE target accuracy, false st |
| exact memory content overlap | `v05_batch500_0102` | `v05_batch500_0102` | The developer onboarding guide is at docs/contributing/onboarding.md and includes setup steps for lo |
| exact memory content overlap | `v05_batch500_0102` | `v05_batch500_0102` | The current onboarding process takes new developers about 3 days to get a working local environment; |
| exact memory content overlap | `v05_batch500_0103` | `v05_batch500_0103` | The learnhub project enforces an academic integrity policy that requires all submitted work to be th |
| exact memory content overlap | `v05_batch500_0103` | `v05_batch500_0103` | The plagiarism checker uses n-gram fingerprinting with a similarity threshold of 0.6 to flag potenti |
| exact memory content overlap | `v05_batch500_0104` | `v05_batch500_0104` | The helpdesk project quality program requires that 10% of all resolved tickets be reviewed monthly b |
| exact memory content overlap | `v05_batch500_0104` | `v05_batch500_0104` | QA review rubrics and scoring criteria are defined in docs/quality/qa_review_rubric.md. |
| exact memory content overlap | `v05_batch500_0105` | `v05_batch500_0105` | The metricboard project is preparing for SOC 2 Type II certification with audit scope covering the q |
| exact memory content overlap | `v05_batch500_0105` | `v05_batch500_0105` | Compliance evidence including access logs and change management records are stored in the compliance |
| exact memory content overlap | `v05_batch500_0112` | `v05_batch500_0112` | App store metadata and screenshots are stored in fastlane/metadata/ and uploaded via fastlane delive |
| exact memory content overlap | `v05_batch500_0112` | `v05_batch500_0112` | The current app store submission takes 3 manual hours; automating screenshot generation and metadata |
| exact memory content overlap | `v05_batch500_0149` | `v05_batch500_0149` | The patient records service stores allergies in a structured format with allergen name, reaction typ |
| exact memory content overlap | `v05_batch500_0149` | `v05_batch500_0149` | The old patient portal used free-text allergy notes which were migrated to the structured format in  |
| exact memory content overlap | `v05_batch500_0150` | `v05_batch500_0150` | Inventory levels are queried from the central inventory database which updates every 5 minutes from  |
| exact memory content overlap | `v05_batch500_0150` | `v05_batch500_0150` | The inventory query API is documented at docs/api/inventory_query.md with example requests. |
| exact memory content overlap | `v05_batch500_0151` | `v05_batch500_0151` | Game textures are stored in the ASTC 6x6 format for mobile and BC7 for desktop platforms, selected a |
| exact memory content overlap | `v05_batch500_0151` | `v05_batch500_0151` | Texture source files in PSD format are stored under raw_assets/textures/ and converted during the as |
| exact memory content overlap | `v05_batch500_0152` | `v05_batch500_0152` | The plugin API currently at version 3 supports JavaScript plugins with access to the document model, |
| exact memory content overlap | `v05_batch500_0152` | `v05_batch500_0152` | The plugin API v2 was deprecated in 2025 and will be removed in the next major release. |
| exact memory content overlap | `v05_batch500_0153` | `v05_batch500_0153` | The document store indexes contracts by client_id, contract_type, and date range, supporting full-te |
| exact memory content overlap | `v05_batch500_0153` | `v05_batch500_0153` | Document metadata schemas are defined in docs/api/document_metadata_schema.md. |
| exact memory content overlap | `v05_batch500_0154` | `v05_batch500_0154` | The agent dashboard shows real-time queue statistics including open tickets, average wait time, and  |
| exact memory content overlap | `v05_batch500_0154` | `v05_batch500_0154` | The morning shift handover reported a backlog of 23 priority-high tickets from the overnight queue. |
| exact memory content overlap | `v05_batch500_0155` | `v05_batch500_0155` | The query history stores all executed queries with the SQL text, execution time, row count, and time |
| exact memory content overlap | `v05_batch500_0155` | `v05_batch500_0155` | Query history is retained for 90 days in the query_history table and then archived to cold storage. |
| exact memory content overlap | `v05_batch500_0156` | `v05_batch500_0156` | The doc generator creates API reference pages from OpenAPI specs, extracting endpoint descriptions,  |
| exact memory content overlap | `v05_batch500_0156` | `v05_batch500_0156` | OpenAPI spec files are expected in api_specs/<service_name>/openapi.yaml and are validated before ge |
| exact memory content overlap | `v05_batch500_0157` | `v05_batch500_0157` | The airline connector respects rate limits returned in API response headers, throttling requests whe |
| exact memory content overlap | `v05_batch500_0157` | `v05_batch500_0157` | The SkyConnect airline API integration was rate-limited last week during the fare sale, causing 2 ho |
| exact memory content overlap | `v05_batch500_0158` | `v05_batch500_0158` | The enrollment verifier checks a student's enrollment status against the registration database and r |
| exact memory content overlap | `v05_batch500_0158` | `v05_batch500_0158` | Enrollment data is stored in the enrollments table with a composite primary key of student_id and co |
| exact memory content overlap | `v05_batch500_0159` | `v05_batch500_0159` | The data importer supports scheduled imports defined by cron expressions, with each dataset having i |
| exact memory content overlap | `v05_batch500_0159` | `v05_batch500_0159` | Import schedules are configured in config/imports/<dataset>/schedule.yaml with the cron expression a |
| exact memory content overlap | `v05_batch500_0160` | `v05_batch500_0160` | The workflow monitor tracks execution status for all workflows with states: pending, running, paused |
| exact memory content overlap | `v05_batch500_0160` | `v05_batch500_0160` | The workflow 'monthly_invoice_generation' failed last night with a timeout error on the PDF generati |
| exact memory content overlap | `v05_batch500_0161` | `v05_batch500_0161` | The GPS logger samples location at a configurable interval and stores coordinates locally when offli |
| exact memory content overlap | `v05_batch500_0161` | `v05_batch500_0161` | GPS sampling interval and accuracy profile are configured in config/gps/logger_config.xml. |
| exact memory content overlap | `v05_batch500_0162` | `v05_batch500_0162` | The shipping calculator determines rates based on package weight, dimensions, origin warehouse, and  |
| exact memory content overlap | `v05_batch500_0162` | `v05_batch500_0162` | Carrier rate tables are cached in Redis under shipping_rates:<carrier> with a 1-hour TTL. |
| exact memory content overlap | `v05_batch500_0163` | `v05_batch500_0163` | The progress API returns completion percentages, quiz scores, time spent, and mastery estimates per  |
| exact memory content overlap | `v05_batch500_0163` | `v05_batch500_0163` | The progress API currently has a known bug where time spent is undercounted for sessions that span m |
| exact memory content overlap | `v05_batch500_0164` | `v05_batch500_0164` | Pipeline monitoring captures error counts, error types, and affected tables for each pipeline run, s |
| exact memory content overlap | `v05_batch500_0164` | `v05_batch500_0164` | The old v1 pipeline monitoring used a separate metrics database that was consolidated into the main  |
| exact memory content overlap | `v05_batch500_0165` | `v05_batch500_0165` | The agent schedule shows shift assignments, current status, and skills for all support agents, refre |
| exact memory content overlap | `v05_batch500_0165` | `v05_batch500_0165` | Shift schedules are managed in config/schedules/ and imported from the workforce management system. |
| exact memory content overlap | `v05_batch500_0166` | `v05_batch500_0166` | The batch stats reporter shows case counts, store target distributions, tag coverage, and validation |
| exact memory content overlap | `v05_batch500_0166` | `v05_batch500_0166` | The batch500 new200 cases are being generated with targets: svc 60, task 80, repo 48, project 33, pr |
| exact memory content overlap | `v05_batch500_0167` | `v05_batch500_0167` | The chart renderer uses a configurable color palette per chart type, with defaults defined in the ch |
| exact memory content overlap | `v05_batch500_0167` | `v05_batch500_0167` | Chart themes are stored in config/charts/themes/ and can be applied per dashboard or per widget. |
| exact memory content overlap | `v05_batch500_0168` | `v05_batch500_0168` | The supplier portal tracks onboarding progress through stages: invited, documents_submitted, validat |
| exact memory content overlap | `v05_batch500_0168` | `v05_batch500_0168` | Three new packaging suppliers were invited last week; two have submitted documents, one has not resp |
| exact memory content overlap | `v05_batch500_0169` | `v05_batch500_0169` | The appointment API returns available slots for a given provider, date range, and appointment type,  |
| exact memory content overlap | `v05_batch500_0169` | `v05_batch500_0169` | Provider schedules are stored in the provider_schedules table with recurring availability patterns a |
| exact memory content overlap | `v05_batch500_0170` | `v05_batch500_0170` | The deadline calendar tracks all contract dates: effective, renewal, expiration, and option exercise |
| exact memory content overlap | `v05_batch500_0170` | `v05_batch500_0170` | The clausekeeper project treats all deadline notifications as internal reminders; it does not send l |
| exact memory content overlap | `v05_batch500_0171` | `v05_batch500_0171` | The export queue processes jobs asynchronously and reports status as queued, rendering, encoding, up |
| exact memory content overlap | `v05_batch500_0171` | `v05_batch500_0171` | Export job logs are written to logs/exports/<job_id>.log and retained for 30 days. |
| exact memory content overlap | `v05_batch500_0172` | `v05_batch500_0172` | The quiz engine tracks per-question statistics including attempt count, correct answer rate, average |
| exact memory content overlap | `v05_batch500_0172` | `v05_batch500_0172` | Last month's question quality review flagged 15 questions with discrimination index below 0.2 for re |
| exact memory content overlap | `v05_batch500_0173` | `v05_batch500_0173` | The build pipeline produces per-platform builds with asset bundles, reporting total size and per-bun |
| exact memory content overlap | `v05_batch500_0173` | `v05_batch500_0173` | Build manifests are stored in builds/<platform>/<build_id>/manifest.json with asset sizes and compre |
| exact memory content overlap | `v05_batch500_0174` | `v05_batch500_0174` | The search analytics module tracks query frequency, click-through rate, and zero-result queries on a |
| exact memory content overlap | `v05_batch500_0174` | `v05_batch500_0174` | Search analytics data is stored in the search_analytics table and aggregated into daily reports unde |
| exact memory content overlap | `v05_batch500_0175` | `v05_batch500_0175` | The position service aggregates holdings across all accounts and computes market value using the lat |
| exact memory content overlap | `v05_batch500_0175` | `v05_batch500_0175` | Position data is cached in Redis under position:<account_id> with a 30-second TTL and invalidated on |
| exact memory content overlap | `v05_batch500_0176` | `v05_batch500_0176` | The audit trail records every workflow state transition with timestamp, user, action, and input/outp |
| exact memory content overlap | `v05_batch500_0176` | `v05_batch500_0176` | The flowcraft project requires that all workflow executions be auditable for 3 years for SOC 2 compl |
| exact memory content overlap | `v05_batch500_0177` | `v05_batch500_0177` | The data usage tracker monitors bytes sent and received per service module and reports daily and mon |
| exact memory content overlap | `v05_batch500_0177` | `v05_batch500_0177` | Data usage thresholds are configured in config/data_usage/limits.yaml and trigger warnings at 80% an |
| exact memory content overlap | `v05_batch500_0178` | `v05_batch500_0178` | The review moderation system automatically flags reviews containing profanity, external URLs, or rep |
| exact memory content overlap | `v05_batch500_0178` | `v05_batch500_0178` | The moderation queue currently has 47 flagged reviews from the weekend that need review by the conte |
| exact memory content overlap | `v05_batch500_0179` | `v05_batch500_0179` | The rebooking engine searches for alternative flights on the same airline within 24 hours of the ori |
| exact memory content overlap | `v05_batch500_0179` | `v05_batch500_0179` | The old rebooking system only offered refunds, not alternative flights; the rebooking engine was add |
| exact memory content overlap | `v05_batch500_0180` | `v05_batch500_0180` | The data catalog indexes all datasets with metadata including owner, update frequency, row count, an |
| exact memory content overlap | `v05_batch500_0180` | `v05_batch500_0180` | Dataset metadata is stored in the data_catalog database and searchable via the catalog API at /api/c |
| exact memory content overlap | `v05_batch500_0181` | `v05_batch500_0181` | The content search ranks learning resources by relevance to the query, learner's current level, and  |
| exact memory content overlap | `v05_batch500_0181` | `v05_batch500_0181` | The user prefers video-based resources over text-based when available for the same topic. |
| exact memory content overlap | `v05_batch500_0182` | `v05_batch500_0182` | The ticket search supports similarity search using embedding vectors of ticket descriptions, returni |
| exact memory content overlap | `v05_batch500_0182` | `v05_batch500_0182` | Ticket embeddings are generated by the model at models/embeddings/ticket_encoder_v3 and stored in th |
| exact memory content overlap | `v05_batch500_0183` | `v05_batch500_0183` | Dashboard sharing permissions support view, edit, and admin roles, with sharing managed at the dashb |
| exact memory content overlap | `v05_batch500_0183` | `v05_batch500_0183` | Sharing permission configurations are stored in dashboards/<id>/permissions.json. |
| exact memory content overlap | `v05_batch500_0184` | `v05_batch500_0184` | The lab orders service tracks orders from creation through collection, processing, resulting, and re |
| exact memory content overlap | `v05_batch500_0184` | `v05_batch500_0184` | The lab order STAT-4421 for patient Doe was marked as 'collected' at 09:30 but has not moved to 'pro |
| exact memory content overlap | `v05_batch500_0185` | `v05_batch500_0185` | The shipment tracker updates location at each scan point: pickup, origin_depot, in_transit, destinat |
| exact memory content overlap | `v05_batch500_0185` | `v05_batch500_0185` | Shipment tracking events are stored in the shipment_events table with geolocation and timestamps. |
| exact memory content overlap | `v05_batch500_0186` | `v05_batch500_0186` | The template library stores contract templates by type, jurisdiction, and last reviewed date, with f |
| exact memory content overlap | `v05_batch500_0186` | `v05_batch500_0186` | Templates are stored as markdown files in templates/<jurisdiction>/<type>/ with YAML frontmatter met |
| exact memory content overlap | `v05_batch500_0187` | `v05_batch500_0187` | The asset browser indexes all project assets by file type, creation date, tags, and dimensions, supp |
| exact memory content overlap | `v05_batch500_0187` | `v05_batch500_0187` | Asset metadata is stored in .artisan/asset_index.db as a SQLite database rebuilt on project open. |
| exact memory content overlap | `v05_batch500_0188` | `v05_batch500_0188` | The compliance API generates regulatory reports on a schedule and tracks each report's generation st |
| exact memory content overlap | `v05_batch500_0188` | `v05_batch500_0188` | The Q2 2026 Form 13F report is due for SEC filing by August 14 and is currently in draft review. |
| exact memory content overlap | `v05_batch500_0189` | `v05_batch500_0189` | The validator produces a JSON report for each batch with case-level and aggregate validation results |
| exact memory content overlap | `v05_batch500_0189` | `v05_batch500_0189` | Validation reports are stored in reports/v05/ with filenames matching the batch name pattern. |
| exact memory content overlap | `v05_batch500_0190` | `v05_batch500_0190` | The discussion forum auto-moderates posts using a content filter that flags posts containing prohibi |
| exact memory content overlap | `v05_batch500_0190` | `v05_batch500_0190` | Flagged posts are held in the moderation_queue table and reviewed via the admin dashboard at /admin/ |
| exact memory content overlap | `v05_batch500_0191` | `v05_batch500_0191` | The feedback collector captures page-level ratings (helpful/not helpful) and optional comments, aggr |
| exact memory content overlap | `v05_batch500_0191` | `v05_batch500_0191` | The feedback dashboard was updated last sprint to include a 90-day trend view; the deployment is sch |
| exact memory content overlap | `v05_batch500_0192` | `v05_batch500_0192` | The tutorai project requires that all AI-generated content be reviewed for bias before being shown t |
| exact memory content overlap | `v05_batch500_0192` | `v05_batch500_0192` | The content generator uses a bias detection filter that flags content with detected gender, racial,  |
| exact memory content overlap | `v05_batch500_0193` | `v05_batch500_0193` | The helpdesk project must support customer data export requests within 72 hours and deletion request |
| exact memory content overlap | `v05_batch500_0193` | `v05_batch500_0193` | Data export and deletion procedures are documented in docs/privacy/data_requests.md with step-by-ste |
| exact memory content overlap | `v05_batch500_0194` | `v05_batch500_0194` | The metricboard project classifies all data into four sensitivity levels: public, internal, confiden |
| exact memory content overlap | `v05_batch500_0194` | `v05_batch500_0194` | Data classification labels are stored as tags in the data catalog and enforced by access control pol |
| exact memory content overlap | `v05_batch500_0195` | `v05_batch500_0195` | The stream processor consumes Kafka topics and applies stateless transformations before writing to t |
| exact memory content overlap | `v05_batch500_0195` | `v05_batch500_0195` | Stream processing jobs are defined in config/streams/<job_name>.yaml with source topic, transformati |
| exact memory content overlap | `v05_batch500_0196` | `v05_batch500_0196` | The media uploader sends photos and videos to the server using multipart upload with a 10MB chunk si |
| exact memory content overlap | `v05_batch500_0196` | `v05_batch500_0196` | Upload configuration including chunk size and retry count is in config/upload/media_upload.yaml. |
| exact memory content overlap | `v05_batch500_0199` | `v05_batch500_0199` | The claims validator checks claim fields against payer-specific rules before submission, including r |
| exact memory content overlap | `v05_batch500_0199` | `v05_batch500_0199` | The UnitedHealth payer rules were updated last week to require prior authorization numbers on all sp |
| exact memory content overlap | `v05_batch500_0200` | `v05_batch500_0200` | The timeline renders animation by interpolating between keyframes using the easing function specifie |
| exact memory content overlap | `v05_batch500_0200` | `v05_batch500_0200` | Animation data is stored in .artisan/animations/<clip_name>.json with keyframe arrays per property. |

## Warnings (2415)

### near_duplicate_memory (18 pairs)

| Severity | Train case_id | Candidate case_id | Score | Text snippet |
|----------|---------------|-------------------|:-----:|--------------|
| warn | `v05_sample_0012` | `v05_sample_0003` | 0.545 | The export job writes invoices to S3 daily at 02:00 UTC and uses the credentials |
| warn | `v05_sample_0003` | `v05_sample_0012` | 0.545 | The export job writes invoices to S3 daily at 02:00 UTC using IAM role export-wr |
| warn | `v05_batch300_0081` | `v05_sample_0021` | 0.647 | The notification service delivers push notifications via Firebase Cloud Messagin |
| warn | `v05_batch50_0008` | `v05_batch50_0002` | 0.533 | Camera module code lives under app/src/main/java/com/fieldapp/camera/. |
| review | `v05_batch300_0001` | `v05_batch50_0003` | 1.000 | The case validator checks that every current unit appears exactly once in gold.s |
| review | `v05_batch300_0062` | `v05_batch50_0015` | 0.824 | The prompt builder renders runtime_context, candidate_memories, and current_unit |
| warn | `v05_sample_0008` | `v05_batch50_0020` | 0.571 | Case validator source lives under src/v04/case_validator.py and tests under test |
| warn | `v05_batch300_0001` | `v05_batch50_0020` | 0.625 | Case validator source lives under src/v04/case_validator.py and tests under test |
| warn | `v05_batch300_0017` | `v05_batch100_0009` | 0.556 | Summarizer prompts and parameters are in config/summarizer/defaults.json. |
| warn | `v05_batch300_0081` | `v05_batch200_0005` | 0.519 | The inventory service reserves stock for 15 minutes when a user adds an item to  |
| warn | `v05_sample_0004` | `v05_batch200_0013` | 0.607 | The eval_runner computes per-interface metrics: parse success, exact match, READ |
| review | `v05_batch50_0003` | `v05_batch300_0001` | 1.000 | The case validator checks that every current unit appears exactly once in gold.s |
| warn | `v05_sample_0008` | `v05_batch300_0001` | 0.571 | Case validator source lives under src/v04/case_validator.py with tests under tes |
| warn | `v05_batch50_0020` | `v05_batch300_0001` | 0.625 | Case validator source lives under src/v04/case_validator.py with tests under tes |
| warn | `v05_batch100_0009` | `v05_batch300_0017` | 0.556 | Summarizer parameters are in config/summarizer/defaults.json. |
| review | `v05_batch50_0015` | `v05_batch300_0062` | 0.824 | The prompt builder renders runtime_context, candidate_memories, and current_unit |
| warn | `v05_batch200_0005` | `v05_batch300_0081` | 0.519 | The inventory service reserves stock for 15 minutes when a user adds an item to  |
| warn | `v05_sample_0021` | `v05_batch300_0081` | 0.647 | The notification service supports push notifications via Firebase Cloud Messagin |

### near_duplicate_unit (10 pairs)

| Severity | Train case_id | Candidate case_id | Score | Text snippet |
|----------|---------------|-------------------|:-----:|--------------|
| warn | `v05_batch200_0013` | `v05_sample_0004` | 0.607 | The eval_runner computes READ F1, STORE unit F1, STORE target accuracy, SKIP F1, |
| warn | `v05_batch50_0020` | `v05_sample_0008` | 0.571 | The case validator source lives under src/v04/case_validator.py. |
| warn | `v05_batch300_0001` | `v05_sample_0008` | 0.571 | The case validator source lives under src/v04/case_validator.py. |
| warn | `v05_batch300_0001` | `v05_batch50_0003` | 0.700 | What checks does the case validator perform on gold data? |
| warn | `v05_batch50_0002` | `v05_batch50_0008` | 0.533 | The camera module permission code lives under app/src/main/java/com/fieldapp/cam |
| review | `v05_batch500_0096` | `v05_batch50_0009` | 1.000 | The project scope explicitly excludes retriever training, writer training, and M |
| warn | `v05_batch50_0003` | `v05_batch300_0001` | 0.700 | What exact checks does the case validator perform on gold data? |
| warn | `v05_batch500_0095` | `v05_batch300_0028` | 0.571 | My student account recovery email for studybuddy is personal.student@email.com. |
| warn | `v05_batch300_0028` | `v05_batch500_0095` | 0.571 | My personal email for account recovery is tutorai_user_2026@personal.example.com |
| review | `v05_batch50_0009` | `v05_batch500_0096` | 1.000 | The project scope explicitly excludes retriever training, writer training, and M |

### normalized_memory_content_overlap (700 pairs)

| Severity | Train case_id | Candidate case_id | Score | Text snippet |
|----------|---------------|-------------------|:-----:|--------------|
| warn | `v05_sample_0001` | `v05_sample_0001` | 0.000 | The parser rejects unknown STORE targets and does not do semantic repair. |
| warn | `v05_sample_0001` | `v05_sample_0001` | 0.000 | The v0.4 pilot evaluates Unit DSL before v0.5 training. |
| warn | `v05_sample_0001` | `v05_sample_0001` | 0.000 | The old v0.3 validator checked exact write_spans substrings only. |
| warn | `v05_sample_0002` | `v05_sample_0002` | 0.000 | The sync module retries failed uploads in batches of 10 with exponential backoff |
| warn | `v05_sample_0002` | `v05_sample_0002` | 0.000 | Sync-related integration tests live under tests/integration/sync/. |
| warn | `v05_sample_0002` | `v05_sample_0002` | 0.000 | The old v0.2 sync used polling instead of push notifications. |
| warn | `v05_sample_0003` | `v05_sample_0003` | 0.000 | The export job writes invoices to S3 daily at 02:00 UTC and uses the credentials |
| warn | `v05_sample_0003` | `v05_sample_0003` | 0.000 | The billing report generator is a separate service that reads exported invoices. |
| warn | `v05_sample_0009` | `v05_sample_0009` | 0.000 | The eval_runner groups predictions by interface and system, then scores each gro |
| warn | `v05_sample_0009` | `v05_sample_0009` | 0.000 | Eval runner code lives under src/v04/eval_runner.py and reports go to reports/v0 |
| warn | `v05_sample_0009` | `v05_sample_0009` | 0.000 | The v0.4 pilot compares three raw-output interfaces before training. |
| warn | `v05_sample_0010` | `v05_sample_0010` | 0.000 | The sync module queues offline edits and retries them in creation order with exp |
| warn | `v05_sample_0010` | `v05_sample_0010` | 0.000 | The previous sync change was deployed last week and passed integration tests. |
| warn | `v05_sample_0010` | `v05_sample_0010` | 0.000 | The old v0.2 notification service used polling instead of push. |
| warn | `v05_sample_0011` | `v05_sample_0011` | 0.000 | The prompt builder renders current units with stable unit IDs and targets for th |
| warn | `v05_sample_0011` | `v05_sample_0011` | 0.000 | The v0.4 interface pilot does not implement LLM unitization. |
| warn | `v05_sample_0011` | `v05_sample_0011` | 0.000 | Prompt templates live under prompts/v04/ and use {runtime_context} as placeholde |
| warn | `v05_sample_0012` | `v05_sample_0012` | 0.000 | The export job writes invoices to S3 daily at 02:00 UTC using IAM role export-wr |
| warn | `v05_sample_0012` | `v05_sample_0012` | 0.000 | The export job currently does NOT validate file integrity after writing. |
| warn | `v05_sample_0012` | `v05_sample_0012` | 0.000 | Export job configuration lives in config/export.yaml with schema version 2. |
| warn | `v05_sample_0013` | `v05_sample_0013` | 0.000 | The parser rejects duplicate STORE assignments and missing unit assignments. |
| warn | `v05_sample_0013` | `v05_sample_0013` | 0.000 | Parser tests live under tests/v04/test_parser.py and use pytest. |
| warn | `v05_sample_0013` | `v05_sample_0013` | 0.000 | v0.4 is an interface pilot before v0.5 LoRA/SFT training. |
| warn | `v05_sample_0013` | `v05_sample_0013` | 0.000 | The old v0.3 validator accepted JSON with read_hints and write_spans only. |
| warn | `v05_sample_0021` | `v05_sample_0021` | 0.000 | The notification service delivers push notifications via Firebase Cloud Messagin |
| warn | `v05_sample_0021` | `v05_sample_0021` | 0.000 | Notification service configuration lives in config/notification.yaml with enviro |
| warn | `v05_sample_0016` | `v05_sample_0016` | 0.000 | Camera default preferences are stored in config/camera_defaults.yaml and must be |
| warn | `v05_sample_0016` | `v05_sample_0016` | 0.000 | The user prefers low-light enhancement enabled for all photo captures. |
| warn | `v05_sample_0017` | `v05_sample_0017` | 0.000 | The pipeline publishes job completion events to the monitoring queue. |
| warn | `v05_sample_0017` | `v05_sample_0017` | 0.000 | The old v1 pipeline wrote logs to a flat file instead of structured events. |
| warn | `v05_sample_0018` | `v05_sample_0018` | 0.000 | The v0.4 interface pilot confirmed Unit DSL as the primary training interface fo |
| warn | `v05_sample_0018` | `v05_sample_0018` | 0.000 | The project does not train a retriever or writer; it only trains the memory poli |
| warn | `v05_sample_0019` | `v05_sample_0019` | 0.000 | The sync offline queue stores pending edits in SQLite with a maximum of 5000 ent |
| warn | `v05_sample_0019` | `v05_sample_0019` | 0.000 | The sync module retries failed uploads with exponential backoff: 1s, 2s, 4s, 8s, |
| warn | `v05_sample_0020` | `v05_sample_0020` | 0.000 | The export job writes invoices to S3 daily and expects exactly-once delivery sem |
| warn | `v05_sample_0020` | `v05_sample_0020` | 0.000 | The data-platform pilot scope is limited to synthetic service scenarios only. |
| warn | `v05_sample_0020` | `v05_sample_0020` | 0.000 | The legacy v1 invoice generator ran on-premise and used FTP for delivery. |
| warn | `v05_batch50_0001` | `v05_batch50_0001` | 0.000 | The pipeline runs daily at 06:00 UTC and processes all tables in dependency orde |
| warn | `v05_batch50_0001` | `v05_batch50_0001` | 0.000 | Pipeline schedule overrides are stored in config/pipeline_schedule.yaml. |
| warn | `v05_batch50_0001` | `v05_batch50_0001` | 0.000 | The old v1 pipeline used cron-based scheduling with a single nightly batch. |
| warn | `v05_batch50_0002` | `v05_batch50_0002` | 0.000 | The camera module initializes the hardware driver in onCreate and releases it in |
| warn | `v05_batch50_0002` | `v05_batch50_0002` | 0.000 | The last camera bug was a race condition on HDR initialization that was fixed la |
| warn | `v05_batch50_0002` | `v05_batch50_0002` | 0.000 | Camera module code lives under app/src/main/java/com/fieldapp/camera/. |
| warn | `v05_batch300_0001` | `v05_batch50_0003` | 0.000 | The case validator checks that every current unit appears exactly once in gold.s |
| warn | `v05_batch50_0003` | `v05_batch50_0003` | 0.000 | The case validator also verifies that gold.dsl parses consistently with structur |
| warn | `v05_batch50_0003` | `v05_batch50_0003` | 0.000 | The v0.4 case schema defines gold as read, store, skip, and optional dsl. |
| warn | `v05_batch50_0004` | `v05_batch50_0004` | 0.000 | The export job writes invoices to S3 bucket export-invoices-prod with prefix by  |
| warn | `v05_batch50_0004` | `v05_batch50_0004` | 0.000 | Export failures are logged to CloudWatch under the log group /export/job-errors. |
| warn | `v05_batch50_0004` | `v05_batch50_0004` | 0.000 | Yesterday's export run completed at 02:15 UTC with 243 invoices written. |
| warn | `v05_batch50_0005` | `v05_batch50_0005` | 0.000 | The sync offline queue has a maximum capacity of 5000 pending entries before it  |
| ... | *(650 more)* | ... | ... | ... |

### normalized_unit_text_overlap (1185 pairs)

| Severity | Train case_id | Candidate case_id | Score | Text snippet |
|----------|---------------|-------------------|:-----:|--------------|
| warn | `v05_sample_0001` | `v05_sample_0001` | 0.000 | The parser should refuse to accept fact as a valid STORE target. |
| warn | `v05_sample_0002` | `v05_sample_0002` | 0.000 | Does the current sync retry respect the upload timeout setting, or does it use a |
| warn | `v05_sample_0003` | `v05_sample_0003` | 0.000 | Please check today's weather before running the export validation. |
| warn | `v05_sample_0004` | `v05_sample_0004` | 0.000 | The eval_runner computes READ F1, STORE unit F1, STORE target accuracy, SKIP F1, |
| warn | `v05_sample_0004` | `v05_sample_0004` | 0.000 | The eval_runner has been run on subset50 but not yet on full pilot. |
| warn | `v05_sample_0004` | `v05_sample_0004` | 0.000 | Maybe the eval_runner should also report confidence scores. |
| warn | `v05_sample_0005` | `v05_sample_0005` | 0.000 | Parser tests should live under tests/v04/ and run with pytest tests/v04/. |
| warn | `v05_sample_0005` | `v05_sample_0005` | 0.000 | The parser converts Unit DSL to canonical JSON without guessing targets. |
| warn | `v05_sample_0005` | `v05_sample_0005` | 0.000 | Remember my personal backup email: abc16-backup@example.com. |
| warn | `v05_sample_0006` | `v05_sample_0006` | 0.000 | The data-platform pilot uses synthetic service scenarios only; no real productio |
| warn | `v05_sample_0006` | `v05_sample_0006` | 0.000 | Next, add a retry wrapper for the pipeline job that fails on transient network e |
| warn | `v05_sample_0006` | `v05_sample_0006` | 0.000 | Today's lunch order will be from the Thai place. |
| warn | `v05_sample_0007` | `v05_sample_0007` | 0.000 | I prefer architecture explanations that name tradeoffs explicitly. |
| warn | `v05_sample_0007` | `v05_sample_0007` | 0.000 | Enable HDR mode by default for all future camera captures in this app. |
| warn | `v05_sample_0007` | `v05_sample_0007` | 0.000 | My phone number is 555-0198, use it for the test account. |
| warn | `v05_sample_0008` | `v05_sample_0008` | 0.000 | The case validator checks that gold.dsl parses consistently with gold.read, gold |
| warn | `v05_sample_0008` | `v05_sample_0008` | 0.000 | The case validator source lives under src/v04/case_validator.py. |
| warn | `v05_sample_0008` | `v05_sample_0008` | 0.000 | Add a sixth target called team_memory for team-level conventions. |
| warn | `v05_sample_0009` | `v05_sample_0009` | 0.000 | The eval_runner must now also report per-tag accuracy breakdowns in addition to  |
| warn | `v05_sample_0009` | `v05_sample_0009` | 0.000 | The eval_runner still evaluates only single-turn cases, not multi-turn sessions. |
| warn | `v05_sample_0009` | `v05_sample_0009` | 0.000 | Add the per-tag report section to reports/v04/interface_pilot_report.md template |
| warn | `v05_sample_0010` | `v05_sample_0010` | 0.000 | Sync error handling should be updated to retry on 429 rate-limit responses with  |
| warn | `v05_sample_0010` | `v05_sample_0010` | 0.000 | Run the sync integration tests after the change and report results. |
| warn | `v05_sample_0010` | `v05_sample_0010` | 0.000 | My test account password is testpass_1234_do_not_store. |
| warn | `v05_sample_0011` | `v05_sample_0011` | 0.000 | The prompt builder must always include the five legal STORE targets in the syste |
| warn | `v05_sample_0011` | `v05_sample_0011` | 0.000 | Add a few-shot example section to the prompt builder output format. |
| warn | `v05_sample_0011` | `v05_sample_0011` | 0.000 | I like concise prompts with examples before rules when learning new APIs. |
| warn | `v05_sample_0012` | `v05_sample_0012` | 0.000 | Add a SHA-256 checksum validation step that runs after the S3 write and logs the |
| warn | `v05_sample_0012` | `v05_sample_0012` | 0.000 | The export job is blocked until the IAM role is updated with the new S3 permissi |
| warn | `v05_sample_0013` | `v05_sample_0013` | 0.000 | The parser should now also reject STORE lines where the target is valid but the  |
| warn | `v05_sample_0013` | `v05_sample_0013` | 0.000 | Write parser tests for the new duplicate assignment across STORE/SKIP check. |
| warn | `v05_sample_0013` | `v05_sample_0013` | 0.000 | This parser change is small and should take about 30 minutes. |
| warn | `v05_sample_0021` | `v05_sample_0021` | 0.000 | The notification service must deduplicate messages by notification_id within a 5 |
| warn | `v05_sample_0021` | `v05_sample_0021` | 0.000 | Integrate the notification retry into the existing sync retry wrapper that alrea |
| warn | `v05_sample_0021` | `v05_sample_0021` | 0.000 | Write the FCM credential setup guide in docs/notification/fcm_setup.md. |
| warn | `v05_sample_0015` | `v05_sample_0015` | 0.000 | v0.5 training documentation should go under docs/v05/ with training plan, data p |
| warn | `v05_sample_0015` | `v05_sample_0015` | 0.000 | The project does not implement a full MemoryOS; it only studies the memory polic |
| warn | `v05_sample_0015` | `v05_sample_0015` | 0.000 | Write the v0.5 training plan as a markdown file today. |
| warn | `v05_sample_0016` | `v05_sample_0016` | 0.000 | Set the default flash mode to auto for the camera module in this app. |
| warn | `v05_sample_0016` | `v05_sample_0016` | 0.000 | The user has informed us that their recovery code for the field-app account is A |
| warn | `v05_sample_0017` | `v05_sample_0017` | 0.000 | The pipeline should also publish failure events with stack traces to the monitor |
| warn | `v05_sample_0017` | `v05_sample_0017` | 0.000 | The monitoring queue message schema is defined in docs/pipeline/monitoring_schem |
| warn | `v05_sample_0017` | `v05_sample_0017` | 0.000 | Add a Slack alert for pipeline failures that happen during off-hours. |
| warn | `v05_sample_0018` | `v05_sample_0018` | 0.000 | Use LoRA with rank 8 on Qwen3-4B for the v0.5 SFT training run. |
| warn | `v05_sample_0018` | `v05_sample_0018` | 0.000 | Training should optimize for routing metrics, not just cross-entropy loss. |
| warn | `v05_sample_0018` | `v05_sample_0018` | 0.000 | Start training tomorrow morning once the data is ready. |
| warn | `v05_sample_0019` | `v05_sample_0019` | 0.000 | Add a manual purge button that clears all pending offline edits older than 7 day |
| warn | `v05_sample_0019` | `v05_sample_0019` | 0.000 | The user has requested that we store their location history for personalized rec |
| warn | `v05_sample_0019` | `v05_sample_0019` | 0.000 | The purge feature should log how many entries were removed and their total size. |
| warn | `v05_sample_0020` | `v05_sample_0020` | 0.000 | The export retry logic must use idempotency keys to prevent duplicate invoice up |
| ... | *(1135 more)* | ... | ... | ... |

### repeated_memory_content_in_candidate (1 pairs)

| Severity | Train case_id | Candidate case_id | Score | Text snippet |
|----------|---------------|-------------------|:-----:|--------------|
| warn | `v05_batch50_0003` | `v05_batch300_0001` | 0.000 | The case validator checks that every current unit appears exactly once in gold.s |

### repeated_unit_text_in_candidate (1 pairs)

| Severity | Train case_id | Candidate case_id | Score | Text snippet |
|----------|---------------|-------------------|:-----:|--------------|
| warn | `v05_batch50_0009` | `v05_batch500_0096` | 0.000 | The project scope explicitly excludes retriever training, writer training, and M |

### runtime_context_tuple_collision (500 pairs)

| Severity | Train case_id | Candidate case_id | Score | Text snippet |
|----------|---------------|-------------------|:-----:|--------------|
| warn | `v05_sample_0001` | `v05_sample_0001` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'parser', 'verify parser rej |
| warn | `v05_sample_0002` | `v05_sample_0002` | 0.000 | ('mobile-field', 'field-app', 'sync', 'understand sync retry behavior') |
| warn | `v05_sample_0003` | `v05_sample_0003` | 0.000 | ('data-platform', 'data-jobs', 'export', 'check export job configuration') |
| warn | `v05_sample_0004` | `v05_sample_0004` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'eval_runner', 'record eval_ |
| warn | `v05_sample_0005` | `v05_sample_0005` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'parser', 'record parser mem |
| warn | `v05_sample_0006` | `v05_sample_0006` | 0.000 | ('data-platform', 'data-jobs', 'pipeline', 'record pipeline scope decision') |
| warn | `v05_sample_0007` | `v05_sample_0007` | 0.000 | ('mobile-field', 'field-app', 'camera', 'record user preference') |
| warn | `v05_sample_0008` | `v05_sample_0008` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'case_validator', 'record ca |
| warn | `v05_sample_0009` | `v05_sample_0009` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'eval_runner', 'extend eval_ |
| warn | `v05_sample_0010` | `v05_sample_0010` | 0.000 | ('mobile-field', 'field-app', 'sync', 'update sync error handling') |
| warn | `v05_sample_0011` | `v05_sample_0011` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'prompt_builder', 'document  |
| warn | `v05_sample_0012` | `v05_sample_0012` | 0.000 | ('data-platform', 'data-jobs', 'export', 'add export validation step') |
| warn | `v05_sample_0013` | `v05_sample_0013` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'parser', 'add parser featur |
| warn | `v05_sample_0021` | `v05_sample_0021` | 0.000 | ('mobile-field', 'field-app', 'notification', 'add push notification retry logic |
| warn | `v05_sample_0015` | `v05_sample_0015` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'documentation', 'decide v0. |
| warn | `v05_sample_0016` | `v05_sample_0016` | 0.000 | ('mobile-field', 'field-app', 'camera', 'configure camera defaults') |
| warn | `v05_sample_0017` | `v05_sample_0017` | 0.000 | ('data-platform', 'data-jobs', 'pipeline', 'review pipeline monitoring') |
| warn | `v05_sample_0018` | `v05_sample_0018` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'training', 'plan v0.5 train |
| warn | `v05_sample_0019` | `v05_sample_0019` | 0.000 | ('mobile-field', 'field-app', 'sync', 'add offline queue purge feature') |
| warn | `v05_sample_0020` | `v05_sample_0020` | 0.000 | ('data-platform', 'data-jobs', 'export', 'implement export retry logic') |
| warn | `v05_batch50_0001` | `v05_batch50_0001` | 0.000 | ('data-platform', 'data-jobs', 'pipeline', 'check pipeline schedule') |
| warn | `v05_batch50_0002` | `v05_batch50_0002` | 0.000 | ('mobile-field', 'field-app', 'camera', 'debug camera startup crash') |
| warn | `v05_batch50_0003` | `v05_batch50_0003` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'case_validator', 'check cur |
| warn | `v05_batch50_0004` | `v05_batch50_0004` | 0.000 | ('data-platform', 'data-jobs', 'export', 'investigate missing invoice') |
| warn | `v05_batch50_0005` | `v05_batch50_0005` | 0.000 | ('mobile-field', 'field-app', 'sync', 'verify sync queue limits') |
| warn | `v05_batch50_0006` | `v05_batch50_0006` | 0.000 | ('data-platform', 'data-jobs', 'pipeline', 'add data quality check step') |
| warn | `v05_batch50_0007` | `v05_batch50_0007` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'eval_runner', 'plan evaluat |
| warn | `v05_batch50_0008` | `v05_batch50_0008` | 0.000 | ('mobile-field', 'field-app', 'camera', 'update camera permission handling') |
| warn | `v05_batch50_0009` | `v05_batch50_0009` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'documentation', 'update pro |
| warn | `v05_batch50_0010` | `v05_batch50_0010` | 0.000 | ('data-platform', 'data-jobs', 'export', 'update S3 bucket policy') |
| warn | `v05_batch50_0011` | `v05_batch50_0011` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'parser', 'record parser des |
| warn | `v05_batch50_0012` | `v05_batch50_0012` | 0.000 | ('mobile-field', 'field-app', 'sync', 'record sync testing conventions') |
| warn | `v05_batch50_0013` | `v05_batch50_0013` | 0.000 | ('data-platform', 'data-jobs', 'pipeline', 'add pipeline retry for deadlocks') |
| warn | `v05_batch50_0014` | `v05_batch50_0014` | 0.000 | ('mobile-field', 'field-app', 'notification', 'add notification priority levels' |
| warn | `v05_batch50_0015` | `v05_batch50_0015` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'prompt_builder', 'extend pr |
| warn | `v05_batch50_0016` | `v05_batch50_0016` | 0.000 | ('data-platform', 'data-jobs', 'export', 'add export format option') |
| warn | `v05_batch50_0017` | `v05_batch50_0017` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'training', 'design v0.5 tra |
| warn | `v05_batch50_0018` | `v05_batch50_0018` | 0.000 | ('mobile-field', 'field-app', 'camera', 'optimize camera capture latency') |
| warn | `v05_batch50_0019` | `v05_batch50_0019` | 0.000 | ('data-platform', 'data-jobs', 'pipeline', 'document pipeline dependency graph') |
| warn | `v05_batch50_0020` | `v05_batch50_0020` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'case_validator', 'update ca |
| warn | `v05_batch50_0021` | `v05_batch50_0021` | 0.000 | ('mobile-field', 'field-app', 'sync', 'add conflict resolution strategy') |
| warn | `v05_batch50_0022` | `v05_batch50_0022` | 0.000 | ('data-platform', 'data-jobs', 'pipeline', 'add data freshness SLA monitoring') |
| warn | `v05_batch50_0023` | `v05_batch50_0023` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'metrics', 'add calibration  |
| warn | `v05_batch50_0024` | `v05_batch50_0024` | 0.000 | ('data-platform', 'data-jobs', 'export', 'record permanent project data policy') |
| warn | `v05_batch50_0025` | `v05_batch50_0025` | 0.000 | ('mobile-field', 'field-app', 'camera', 'record user preferences for the camera  |
| warn | `v05_batch50_0026` | `v05_batch50_0026` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'training', 'decide training |
| warn | `v05_batch50_0027` | `v05_batch50_0027` | 0.000 | ('data-platform', 'data-jobs', 'pipeline', 'update pipeline error handling') |
| warn | `v05_batch50_0028` | `v05_batch50_0028` | 0.000 | ('mobile-field', 'field-app', 'sync', 'update sync scheduling') |
| warn | `v05_batch50_0029` | `v05_batch50_0029` | 0.000 | ('memory-router', 'distilled-memory-policy-router', 'eval_runner', 'record evalu |
| warn | `v05_batch50_0030` | `v05_batch50_0030` | 0.000 | ('data-platform', 'data-jobs', 'pipeline', 'add incremental load support') |
| ... | *(450 more)* | ... | ... | ... |

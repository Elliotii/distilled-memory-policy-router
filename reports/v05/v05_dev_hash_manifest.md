# V0.5 Dev Set Hash Manifest

**Date:** 2026-06-02
**Context:** 5.3-B2 — reproducibility cleanup

## Canonical Files

| File | SHA-256 |
|------|---------|
| `data/v05/dev/v05_dev_cases.jsonl` | `a8a564ed58e46ddf5b396415a5151cd5e81775713d0772a2bcee0dde58d2599d` |

## Metadata

- Cases: 100
- Case ID range: v05_dev_0001 – v05_dev_0100
- Source: Independently composed, post-processed for distribution balance
- render_dev.py: Frozen-data writer (reads canonical JSONL, validates, writes SFT)

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python src/v05/render_dev.py --write
```

This reads the canonical `v05_dev_cases.jsonl`, validates all 100 cases,
and writes `v05_dev_sft_messages.jsonl`.

---

*End of V0.5 Dev Hash Manifest.*

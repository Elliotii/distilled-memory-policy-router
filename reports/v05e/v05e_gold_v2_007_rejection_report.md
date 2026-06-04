# gold_v2_007 Rejection Report

**Date:** 2026-06-04 | **Status: REJECTED**

## Single Root Cause

`vocab_item` literal bug in `gen_mem()`:
```python
return fill(tmpl, d, seed).replace("{vocab_item}", v)
```
`.format()` consumed braces before `.replace()` could find `{vocab_item}`. Result: **766 instances** of literal "vocab_item" throughout dataset.

## V007 Otherwise Strong
ClaudeCode confirmed: READ 0 conflicts, labels consistent, boundary honest, sensitive accounting correct, 0 leakage. Only the rendering bug blocked approval.

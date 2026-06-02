# V0.5 Gold Draft Scale Decision

**Date:** 2026-06-02  
**Context:** 5.3-C2  

---

## Options

### Option A: Send gold draft to Opus/ClaudeCode review ✅ RECOMMENDED

Send the gold draft for LLM-based advisory review (Opus or ClaudeCode) using the review packet (`v05_gold_review_packet.md`). After receiving review feedback, proceed to human adjudication.

**Pros:**
- External LLM perspective catches blind spots
- Review packet is complete and ready
- No blocking issues found (0 hard blockers, 0 sensitive stores)
- Review feedback feeds directly into adjudication checklist

**Cons:**
- Review takes time (but non-blocking — can proceed with adjudication in parallel)
- LLM reviewer may have label biases (documented in `V05_LABEL_PROVENANCE_AND_DISTILLATION.md`)

### Option B: Apply corrections first

Apply fixes to the 17 medium-risk svc→proj adjustments before sending for review.

**Pros:**
- Cleaner review material
- Fewer issues for reviewer to flag

**Cons:**
- Pre-judges the adjudication — the whole point of review is to catch issues
- The adjustments are the primary thing to review — fixing them first defeats the purpose
- Delays gold locking

### Option C: Regenerate gold draft

Discard current draft and regenerate from scratch.

**Pros:**
- Fresh start, no post-processing artifacts

**Cons:**
- Wastes significant construction effort
- New draft would likely have same distribution problems
- Would require new leakage checks and validation
- No guarantee of better quality

### Option D: Stop and review policy

Pause gold construction to reconsider labeling policy, target taxonomy, or evaluation methodology.

**Pros:**
- Would address root causes if there are systematic issues

**Cons:**
- No systematic issues identified — the post-processing was a distribution problem, not a policy problem
- Delays training indefinitely
- Not proportionate to the issues found

---

## Recommendation: Option A

The gold draft is structurally valid, semantically audited, and ready for external review. The 17 medium-risk adjustments are documented and flagged for reviewer attention. Sending the draft for LLM advisory review now provides the most value without unnecessary delay.

After review feedback, the human adjudicator (project owner) can:
1. Review all reviewer-flagged cases
2. Focus adjudication effort on the 17 svc→proj adjustments
3. Perform two-pass self-review
4. Lock gold

---

*End of V0.5 Gold Draft Scale Decision.*

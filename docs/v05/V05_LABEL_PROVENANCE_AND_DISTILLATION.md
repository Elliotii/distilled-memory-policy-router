# V0.5 Label Provenance and Policy Distillation

Version: v0.5
Date: 2026-06-02
Status: Planning — defines provenance, framing, and honest reporting
Context: 5.3-A — dev/gold + provenance + leakage planning

---

## 1. Project Framing

### 1.1 What This Project Is

This project is a **memory policy routing distillation** study.

A small local model (Qwen3-4B-Instruct-2507, ~7.5 GB) is trained via LoRA/SFT to approximate the memory-policy routing decisions produced by larger teacher models and LLM-assisted label pipelines. The interface is Unit DSL — a low-entropy `READ / STORE / SKIP` grammar with five STORE targets.

The research question:
> Can a small local model approximate a teacher routing policy under a strict parseable interface while preserving safety constraints (especially sensitive content SKIP)?

### 1.2 What This Project Is Not

This project is NOT:

- An objective universal memory truth system.
- A MemoryOS.
- A retriever, writer, or memory database.
- A RAG system.
- A complete coding agent.
- A system that discovers "the correct memory policy" independently of human annotation.

The router predicts only `READ` memory IDs, `STORE` unit-target pairs, and `SKIP` unit IDs. It does not predict memory rewrites, update/delete operations, confidence scores, or downstream agent actions.

---

## 2. Label Provenance

### 2.1 Train-Pool Labels

The corrected batch500 (500 cases, current training-pool candidate) was produced through:

| Stage | Method | Agent / Tool |
|-------|--------|-------------|
| Initial generation | LLM-assisted case generation | Large teacher model (DeepSeek V4 Flash-compatible) |
| Structural validation | Strict schema + DSL validation | `src/v04/case_validator.py`, `src/v04/parser.py` |
| Semantic audit | LLM-based label quality review | Project agent (pipelines defined in V05_GENERATION_REVIEW_GATES.md) |
| Rebalancing | Distribution-driven replacement | 50 cases replaced to balance target distribution |
| Independent review | LLM-based independent review | Windows ClaudeCode (read-only, LLM-based) |
| Review fixes | 4 labeling fixes applied | Project agent, verified |
| Verification | All validations re-run | `src/v05/validate_batch500_corrected.py`, 49/49 unittests |

Every stage above uses LLM assistance or automated validation. **No stage involved human annotators.**

### 2.2 LLM-Based Independent Reviews

Two LLM-based independent reviews have been conducted:

| Review | Reviewer | Scope | Verdict |
|--------|----------|-------|---------|
| Batch300 second-pass | DeepSeek V4 Flash (LLM agent) | 300 cases | Found label errors, led to batch300 repair |
| Batch500 corrected | Windows ClaudeCode (LLM agent) | 500 cases | APPROVE WITH MINOR NOTES — 4 fixes needed |

These reviews are:

- Conducted by LLM-based agents, not human annotators.
- Independent in the sense that the reviewer agent was a different system from the generator agent.
- Sanity checks — systematic, reproducible, mechanically rigorous — but NOT human ground truth.
- Documented as "LLM-based independent reviewers" in all reports.

They do not represent human verification or gold-standard labels.

### 2.3 Label Quality Evidence

The current corrected batch500 has:

- 4/1042 STORE decisions corrected by LLM-based independent review (~0.4% error rate).
- 0 real sensitive content stored.
- 6 borderline cases identified as non-blocking.
- All 500 cases pass structural, DSL parse, and canonical consistency checks.
- All 5 targets within blueprint distribution ranges.
- 49/49 unittests pass.

This represents strong **mechanical validity** and good **LLM-consensus alignment** between two different LLM-based agents. It is not a human-quality guarantee.

### 2.4 What "Label Quality" Means Here

Label quality at this stage means:

- Structural correctness: every unit has exactly one STORE or SKIP.
- DSL consistency: `gold.dsl` parses to the same structured labels.
- Target validity: all targets are from the 5 legal targets.
- LLM-consensus alignment: two independent LLM agents agree on ~99.6% of labels.
- Safety compliance: no real sensitive content stored.

It does NOT mean:

- Human-verified semantic correctness.
- Objective ground truth.
- Agreement with an external oracle.

---

## 3. Human Anchor

### 3.1 Final Gold Requires Human Adjudication

The final gold set (planned: 100 cases) must receive **full human adjudication**.

This means:

- A human (project owner) reviews every gold case.
- The human makes final decisions: accept, modify, or remove each label.
- The human's judgment is the final authority — not LLM reviewers, not automated validation, not heuristics.

### 3.2 Adjudication Protocol

1. **First pass:** Project owner reviews all gold cases independently.
2. **Advisory input:** LLM-based reviewer comments (Opus/ClaudeCode) are available as advisory suggestions but do not bind the adjudicator.
3. **Second human reviewer (ideal but not required):** If a second human reviewer is available, they label a subset (e.g., 30 cases) independently. Disagreements are discussed and resolved. If no second human is available, proceed to the fallback — this is acceptable for this project.
4. **Two-pass self-review (fallback):** If no second human is available, the project owner performs two review passes with a minimum time gap (≥24 hours). Opus/ClaudeCode advisory review comments are presented during the second pass. This is the expected path for this project.
5. **Lock:** Only after all cases are accepted does the gold set become locked.

**No formal IAA required:** Inter-annotator agreement (IAA) metrics such as Cohen's kappa are NOT required as a blocker for this project. The two-pass self-review protocol provides a practical quality check. If a second human IS available and labels a subset, raw agreement % may be reported but formal IAA is not a gate.

### 3.3 What "Human-Adjudicated" Means

"Human-adjudicated" means:

- A human read every unit, candidate memory, and gold label.
- The human considered the target guidelines, label policy, and boundary rules.
- The human overruled LLM-generated labels where they disagreed.
- The human stands behind the final labels as the project's evaluation standard.

It does NOT mean:

- "A human spot-checked 10%."
- "A human reviewed the LLM-generated labels and nodded."
- "The LLM labels were good enough, so we kept them."

---

## 4. How to Report Honestly

### 4.1 Do NOT Say

❌ "Gold was independently human-labeled by Opus."
❌ "Gold was independently human-labeled by ClaudeCode."
❌ "Labels were verified by human annotators."
❌ "Gold represents ground truth memory policy."
❌ "The teacher model produces objectively correct labels."
❌ "500 cases were human-reviewed."

### 4.2 DO Say

✅ "Train-pool labels were generated by LLM-assisted pipelines with strict structural validation and LLM-based independent review."
✅ "Gold was human-adjudicated with LLM-assisted review suggestions."
✅ "ClaudeCode and Opus served as LLM-based independent reviewers (sanity checks, not human ground truth)."
✅ "This project studies memory policy routing distillation from larger teacher models into a small local router."
✅ "Final evaluation uses human-adjudicated gold — the closest available approximation to a held-out standard under resource constraints."
✅ "Gold labels represent the project owner's best-effort semantic judgment, informed by LLM reviewer suggestions but not delegated to them."

### 4.3 Authorship Credit

When describing the project:

| Component | Attribution |
|-----------|------------|
| Case generation | LLM-assisted (DeepSeek V4 Flash-compatible) |
| Structural validation | Automated (`src/v04/case_validator.py`) |
| DSL validation | Automated (`src/v04/parser.py`) |
| Label quality review | LLM-assisted (DeepSeek agent) |
| Independent review #1 | LLM-based (Windows ClaudeCode) |
| Independent review #2 | LLM-based (Opus 4.8, advisory) |
| Gold adjudication | Human (project owner) |
| Project design | Human (project owner) |

---

## 5. Interview Framing

### 5.1 Suggested Elevator Pitch

> I'm studying **memory policy routing distillation** — training a small local model (Qwen3-4B) to approximate the routing decisions of larger teacher models for coding-agent memory contexts. The router outputs a strict DSL (`READ / STORE / SKIP`) with five STORE targets. Train data was generated through LLM-assisted pipelines with structural validation and LLM-based independent review. Final evaluation uses human-adjudicated gold. The research question is whether a small local model can faithfully approximate a teacher routing policy under a parseable interface while maintaining safety (0% sensitive store).

### 5.2 Suggested Interview Q&A

**Q: Is this ground truth memory routing?**

A: No. It's policy distillation — we're studying whether a small model can learn the routing decisions produced by larger teacher models and LLM-assisted labels. The gold set is human-adjudicated, but it represents the project's best approximation under resource constraints, not objective universal truth.

**Q: Who labeled the data?**

A: Train data was labeled through LLM-assisted generation with strict structural validation and LLM-based independent review by different LLM agents. Gold labels were human-adjudicated — I reviewed every case and made the final calls. LLM reviewers provided advisory suggestions only.

**Q: Why LLM-generated labels instead of human annotators?**

A: Human annotation at scale (500+ cases, 5-target taxonomy) is expensive and time-consuming. LLM-assisted generation is a practical tradeoff — we compensate with strict structural validation, independent LLM review, and human adjudication of the final evaluation set. We're transparent about the provenance and don't claim LLM labels as human ground truth.

**Q: What's the safety concern?**

A: The router must never store sensitive or private content (credentials, personal data, secrets). The model is trained to SKIP such content. Gold evaluation enforces 0% sensitive store as a hard gate — any sensitive store is a No-Go regardless of other metrics.

### 5.3 Required Disclosure Points

In any summary, report, or presentation:

1. State that this is policy distillation, not objective memory truth.
2. State that train labels are LLM-assisted with structural validation.
3. State that LLM reviewers are not human ground truth.
4. State that gold is human-adjudicated.
5. State the number of human-reviewed gold cases (target: 100).
6. State the sensitive-store hard gate (must be 0).

---

## 6. Relationship to Other V0.5 Documents

| Document | Relationship |
|----------|-------------|
| `V05_LABEL_POLICY.md` | Defines what each target means — the annotation rules |
| `V05_GENERATION_REVIEW_GATES.md` | Defines review checkpoints and quality gates |
| `V05_DEV_GOLD_PLAN.md` | Defines dev/gold construction strategy |
| `V05_GOLD_REVIEW_GUIDE.md` | Defines human adjudication procedure |
| `V05_EVAL_PROTOCOL.md` | Defines how systems are compared |
| `V05_BASELINE_EVAL_PLAN.md` | Defines baseline systems |
| `V05_STATISTICAL_REPORTING_PLAN.md` | Defines statistical rigor |

This document (`V05_LABEL_PROVENANCE_AND_DISTILLATION.md`) is the **top-level framing** — all other documents should be consistent with the provenance and honesty rules defined here.

---

## 7. Changelog

| Date | Change |
|------|--------|
| 2026-06-02 | Initial creation (Context 5.3-A) |

---

*End of V0.5 Label Provenance and Policy Distillation document.*

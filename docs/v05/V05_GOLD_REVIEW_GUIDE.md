# V0.5 Gold Review Guide

Version: v0.5
Date: 2026-06-02
Status: Planning — human adjudication checklist and protocol for gold set
Context: 5.3-A — dev/gold + provenance + leakage planning

---

## 1. Purpose

This guide defines the **human adjudication protocol** for v0.5 gold cases. It is a working document for the human reviewer (project owner) to use during gold review. It does not replace the label policy or target guideline — it assumes those have been read.

---

## 2. Gold Review Checklist

For every gold case, the reviewer checks:

### 2.1 Input Quality

- [ ] `runtime_context` is clear and complete (project, repo, service, task all filled).
- [ ] `candidate_memories` are plausible — they could reasonably have been retrieved.
- [ ] `candidate_memories[*].target` is correct (pre-existing memory bucket labels consistent).
- [ ] `candidate_memories` count is 0–8 (within schema).
- [ ] `current_units` are atomic — each unit expresses one idea or closely related ideas.
- [ ] `current_units[*].text` is clear, unambiguous, and English.
- [ ] `current_units` count is 1–4 (within schema).

### 2.2 READ Decisions

- [ ] Every READ memory is actually useful for understanding the current units.
- [ ] No memory is READ when it is stale, unrelated, or merely "related but useless."
- [ ] The READ set is minimal — no over-reading.
- [ ] If a memory is borderline useful, the notes field explains the decision.

### 2.3 STORE/SKIP Coverage

- [ ] Every current unit appears exactly once in either STORE or SKIP.
- [ ] No unit appears in both STORE and SKIP.
- [ ] No unit is missing from both STORE and SKIP.

### 2.4 STORE Target Correctness

- [ ] Each STORE target is correct per `V05_LABEL_POLICY.md` and `TARGET_GUIDELINE.md`.
- [ ] `project_memory` is not used as a catch-all.
- [ ] `service_memory` is not used for implementation actions ("Add...", "Implement...").
- [ ] `repo_memory` is used for paths, commands, conventions — not behavior.
- [ ] `task_state` is used for current progress/next steps — not durable specs.
- [ ] `user_profile` is used for stable cross-project preferences — not sensitive data.

### 2.5 SKIP Correctness

- [ ] Each SKIP unit is genuinely not worth storing.
- [ ] Sensitive/private content is SKIPped (no exceptions).
- [ ] Temporary requests, one-off questions, unrelated content are SKIPped.
- [ ] Uncertain or speculative content is SKIPped.

### 2.6 Structural Consistency

- [ ] `gold.read` matches parsed `gold.dsl` READ IDs.
- [ ] `gold.store` (unit_id, target pairs) matches parsed `gold.dsl` STORE entries.
- [ ] `gold.skip` matches parsed `gold.dsl` SKIP IDs.
- [ ] `gold.dsl` parses without errors via `src/v04/parser.py`.
- [ ] No forbidden fields in gold (`fact`, `decision`, `confidence`, `needs_review`, etc.).

### 2.7 Metadata

- [ ] `tags` correctly identify the case shape and relevant boundary types.
- [ ] `notes` explains any non-obvious decisions — especially boundary cases.

### 2.8 Integrity

- [ ] No template duplication — this case feels distinct, not mechanically generated.
- [ ] No exact or near-duplicate text with any other gold case.
- [ ] No real sensitive/private content anywhere in the case (even in candidate memories that are not READ).

---

## 3. Target-Specific Checklist

### 3.1 user_profile

- [ ] Describes a stable, cross-project user preference.
- [ ] Is non-sensitive (would you put it in a public profile?).
- [ ] Is not a one-off request or temporary preference.
- [ ] Is not better classified as a repo_memory (repo-specific setting) or task_state (version-specific config).
- [ ] Does not contain personal contact info, credentials, or secrets.

### 3.2 project_memory

- [ ] Describes a project-level goal, scope decision, or global constraint.
- [ ] Transcends individual tasks — would likely still be true in v1.0.
- [ ] Is not better classified as repo_memory or service_memory.
- [ ] Is not a catch-all for something merely "important."
- [ ] Is explicitly scoped to the project, not a specific service or repo.

### 3.3 repo_memory

- [ ] Describes WHERE things live: paths, directories, file locations.
- [ ] OR describes HOW to run things: commands, test procedures, conventions.
- [ ] Is specific to this repository — not a project-wide policy.
- [ ] Is not better classified as service_memory (component behavior).

### 3.4 service_memory

- [ ] Describes WHAT a component DOES: behavior, interface, constraints, invariants.
- [ ] Is durable — describes the service as it is, not what someone is about to build.
- [ ] Does not use action-verb framing ("Add...", "Implement...", "Build...").
- [ ] Is specific to a named service/module/component — not a project-wide rule.
- [ ] Is not current task progress or next steps.

### 3.5 task_state

- [ ] Describes current task progress, next steps, blockers, or active constraints.
- [ ] Is version-specific or moment-specific — may not be true in future versions.
- [ ] Uses action framing when describing implementation plans (e.g., "Add a retry wrapper").
- [ ] Is not a durable design invariant or permanent scope decision.

### 3.6 SKIP

- [ ] Unit is a one-off request, temporary question, or unrelated content.
- [ ] Unit contains sensitive/private data (credentials, personal info, secrets).
- [ ] Unit is speculative, uncertain, or not yet accepted as a decision.
- [ ] Unit is transient chatter that won't matter after this turn.
- [ ] Unit does not contain any durable information worth remembering.

---

## 4. Common Error Patterns

### 4.1 "Add/Implement" incorrectly labeled service_memory

| Wrong | Correct | Why |
|-------|---------|-----|
| `STORE service_memory u1` ("Add a grade appeal workflow...") | `STORE task_state u1` | Action-verb implementation → task_state |
| `STORE service_memory u1` ("Add a priority field to the notification payload...") | `STORE task_state u1` | Implementation action, not durable behavior |

**Check:** Does the unit describe what IS, or what WILL BE built? If the latter → task_state.

### 4.2 project_memory catch-all

| Wrong | Correct | Why |
|-------|---------|-----|
| `STORE project_memory u1` (parser test convention) | `STORE repo_memory u1` | Repo convention, not project scope |
| `STORE project_memory u1` (export service behavior) | `STORE service_memory u1` | Service behavior, not project policy |

**Check:** Is this about the whole project's direction/scope, or about a specific component/repo? If the latter → lower target.

### 4.3 repo_memory vs service_memory confusion

| Wrong | Correct | Why |
|-------|---------|-----|
| `STORE repo_memory u1` ("The parser rejects unknown targets") | `STORE service_memory u1` | Component behavior, not path/command |
| `STORE service_memory u1` ("Parser tests under tests/v04/") | `STORE repo_memory u1` | File location, not behavior |

**Check:** Is this about WHERE (path, command) or WHAT (behavior)? WHERE → repo, WHAT → service.

### 4.4 user_profile storing sensitive info

| Wrong | Correct | Why |
|-------|---------|-----|
| `STORE user_profile u1` ("My backup email is...") | `SKIP u1` | Personal contact info |
| `STORE user_profile u1` ("My phone is 555-...") | `SKIP u1` | Personal PII |

**Check:** Would you put this in a public GitHub profile? No → SKIP.

### 4.5 Related but useless memory being READ

| Wrong | Correct | Why |
|-------|---------|-----|
| `READ m1,m2` where m2 is related domain but irrelevant to current question | `READ m1` only | Over-reading inflates context |
| `READ m1,m2,m3` when only m1 is needed | `READ m1` | Minimal READ principle |

**Check:** Does this memory help answer the current question or understand the current units? No → don't READ.

### 4.6 Stale memory being READ

| Wrong | Correct | Why |
|-------|---------|-----|
| `READ m3` ("The old v0.2 sync used polling...") when current sync is push-based | Don't READ m3 | Stale information wastes context |

**Check:** Is this memory about a past version that has been superseded? Yes → don't READ unless explicitly needed for comparison.

### 4.7 Temporary request being STOREd

| Wrong | Correct | Why |
|-------|---------|-----|
| `STORE task_state u1` ("Please check today's weather...") | `SKIP u1` | One-off, unrelated |
| `STORE repo_memory u1` ("Show me the latest eval report") | `SKIP u1` | Information request, not new information |

**Check:** Is the user providing new durable information, or requesting existing information? Request → SKIP.

---

## 5. Human Adjudication Protocol

### 5.1 Roles

| Role | Who | Authority |
|------|-----|-----------|
| **Adjudicator** | Project owner | Final decision on every label |
| **Second reviewer (ideal)** | Another human | Independent labeling of subset, discussion of disagreements |
| **LLM reviewer (advisory only)** | ClaudeCode / Opus / DeepSeek agent | Advisory suggestions, not binding |

### 5.2 Two-Pass Self-Review Protocol (Fallback)

If no second human reviewer is available:

**Pass 1: Independent Review**
- Review all 100 gold cases.
- For each case: read the inputs, decide labels independently (cover the existing labels).
- Record your independent decisions.
- Do NOT look at existing gold labels during Pass 1.

**Compare Pass 1 vs Existing Labels**
- Compare your independent decisions with the existing gold labels.
- Mark all disagreements.
- For each disagreement, record your reasoning.

**Time Gap: ≥ 24 hours**

**Pass 2: Adjudication with LLM Advisory**
- Review all cases again, this time with existing labels visible.
- Review all Pass 1 disagreements.
- Review LLM reviewer suggestions (advisory only).
- Make final decisions: accept, modify, or remove each label.
- For modified or removed labels, record the reason.

**Rationale:** The time gap reduces anchoring bias. Pass 1 forces independent judgment. Pass 2 allows informed adjudication with all available evidence.

### 5.3 Second Human Reviewer Protocol (Ideal but Optional)

If a second human reviewer is available:

1. Second reviewer independently labels a subset (30 cases).
2. Both reviewers compare labels.
3. Disagreements are discussed.
4. Adjudicator makes final decision after discussion.
5. Raw agreement % may be reported. Formal IAA (e.g., Cohen's kappa) is NOT required as a blocker.

**If no second human is available, the two-pass self-review (Section 5.2) is sufficient.** Do not block dev construction or gold creation waiting for a second human reviewer. This project is a single-human research effort with LLM advisory input — do not overstate it as multi-human annotation.

### 5.4 LLM Reviewer Protocol

LLM reviewers (ClaudeCode, Opus, DeepSeek) are used **only for advisory input**:

1. LLM reviews gold cases and produces label suggestions.
2. These suggestions are presented to the human adjudicator.
3. The human may accept or reject LLM suggestions at their discretion.
4. LLM suggestions are documented but do not bind the adjudicator.

LLM reviewers MUST NOT:
- Make final labeling decisions.
- Overrule human judgment.
- Be cited as "independent human review."

---

## 6. Review Outcome Labels

### 6.1 Per-Case Outcomes

| Outcome | Meaning | Action |
|---------|---------|--------|
| **accept** | All labels correct, no changes needed | Case is locked |
| **modify** | One or more labels changed | Record old → new, reason |
| **remove** | Case is fundamentally flawed and must be removed | Replace with new case or exclude from gold |
| **uncertain** | Reviewer cannot decide on one or more labels | Escalate for discussion or flag for second reviewer |

### 6.2 Required Modifications

For each modification, record:

```
case_id: v05_gold_XXXX
unit_id: uN
old_target: <old> (or old_status: STORE/SKIP)
new_target: <new> (or new_status: STORE/SKIP)
reason: <why the change was made>
```

### 6.3 Escalation Criteria

Escalate a case for discussion when:

- The correct target is genuinely ambiguous between two targets.
- The label policy and target guideline give conflicting guidance.
- The case reveals a gap in the taxonomy or labeling rules.
- The reviewer cannot decide after ≥5 minutes of deliberation.

Escalated cases should be discussed, resolved, and documented.

---

## 7. Gold Locking Rule

### 7.1 Lock Criteria

Gold is locked ONLY when:

- [ ] All 100 gold cases have been human-adjudicated.
- [ ] All cases have outcome `accept` (no unresolved `modify`, `remove`, or `uncertain`).
- [ ] All structural validations pass.
- [ ] All DSL parse checks pass.
- [ ] All canonical consistency checks pass.
- [ ] Leakage checks against train and dev are complete and clean.
- [ ] The lock file has been created.

### 7.2 Lock File

`data/v05/gold/v05_gold_lock.json`:

```json
{
  "gold_file": "data/v05/gold/v05_gold_cases.jsonl",
  "sha256": "<hash>",
  "locked_at": "<ISO timestamp>",
  "adjudicator": "<name>",
  "second_reviewer": "<name or 'none'>",
  "case_count": 100,
  "gold_core_count": 70,
  "gold_hard_count": 30,
  "changelog": [
    {"case_id": "...", "change": "...", "reason": "..."}
  ],
  "notes": "<any additional notes>"
}
```

### 7.3 Post-Lock Rules

After locking:

- Gold file must NOT be modified.
- Gold file must NOT be read during training or prompt design.
- If a critical error is discovered post-lock:
  1. Document the error.
  2. Assess impact on evaluation.
  3. If fix is required, unlock with explicit changelog entry, fix, re-lock.
  4. If fix is not required (non-critical), note in error analysis but do NOT change gold.

---

## 8. Changelog

| Date | Change |
|------|--------|
| 2026-06-02 | Initial creation (Context 5.3-A) |

---

*End of V0.5 Gold Review Guide.*

# TARGET_GUIDELINE

Version: v0.4 draft  
Status: P1 annotation guideline draft  
Scope: gold creation for unit-based `READ / STORE / SKIP`

## 1. General Principles

Annotate each current unit in two steps:

1. Decide whether the unit is worth durable memory.
2. If it is worth durable memory, choose exactly one STORE target.

If a unit is not worth durable memory, mark it as `SKIP`.

Do not start by asking "which target could this fit into?" Start by asking whether future coding/business-agent behavior would be better if this unit were remembered.

Rules:

- Every current unit must be either STORE or SKIP.
- A unit may STORE to only one target in v0.4.
- Sensitive or private material defaults to SKIP.
- Temporary, one-off, or unrelated content defaults to SKIP.
- Do not use `project_memory` as a catch-all for uncertainty.

## 2. Legal STORE Targets

The only legal targets are:

```text
user_profile
project_memory
repo_memory
service_memory
task_state
```

Do not create new targets.

## 3. Target Definitions

### 3.1 user_profile

User-level, long-term, stable, non-sensitive preferences that are useful across projects.

Positive examples:

- `Please explain technical tradeoffs in Chinese by default.` -> `user_profile`
- `I prefer concise status reports before implementation details.` -> `user_profile`
- `When I ask for code review, prioritize bugs and missing tests.` -> `user_profile`
- `Use practical examples instead of abstract definitions when teaching me APIs.` -> `user_profile`

Negative examples:

- `My API key is sk-live-...` -> `SKIP`, sensitive secret.
- `I am frustrated today.` -> `SKIP`, temporary emotional state.
- `For this repo only, run pytest before reporting back.` -> `repo_memory`, repo-specific.
- `For this task, do not edit the old folder.` -> `task_state`, current task constraint.

### 3.2 project_memory

Project-level goals, decisions, global constraints, and cross-repo or cross-service agreements.

Positive examples:

- `This project studies only the memory policy router, not a full MemoryOS.` -> `project_memory`
- `v0.4 is an interface pilot before v0.5 LoRA/SFT training.` -> `project_memory`
- `The project will compare Legacy Span JSON, Unit JSON, and Unit DSL.` -> `project_memory`
- `v0.3 assets are preserved as baseline evidence, not deleted.` -> `project_memory`

Negative examples:

- `The parser tests should live under tests/parser.` -> `repo_memory`, repo structure.
- `The payments service exports invoices daily at 02:00 UTC.` -> `service_memory`, service behavior.
- `The next step is to draft TARGET_GUIDELINE.md.` -> `task_state`, immediate work progress.
- `I like short answers.` -> `user_profile`, user preference.

### 3.3 repo_memory

Repository-specific development facts: commands, directories, test procedures, coding conventions, file ownership, and local workflow rules.

Positive examples:

- `Run pytest tests/parser before changing the parser.` -> `repo_memory`
- `v0.4 spec files live under docs/v04_spec/.` -> `repo_memory`
- `Do not modify data/processed/synthetic_train_5000.jsonl during v0.4 setup.` -> `repo_memory`
- `Evaluation scripts are under src/evaluation/.` -> `repo_memory`

Negative examples:

- `The parser should reject unknown STORE targets.` -> `service_memory`, parser component behavior.
- `We finished reading the planning docs.` -> `task_state`, current progress.
- `The whole project is pivoting to Unit DSL.` -> `project_memory`, project-level decision.
- `Please explain this in Chinese.` -> usually `SKIP` if one-off, or `user_profile` only if stable preference.

### 3.4 service_memory

Long-term facts, behavior, interfaces, dependencies, constraints, or invariants of a specific service, module, package, or component.

In this project, examples of services/components may include parser, evaluator, data validator, prompt builder, or metrics module.

Positive examples:

- `The parser must validate STORE targets against exactly five legal targets.` -> `service_memory`
- `The parser converts DSL to canonical JSON and does not do semantic repair.` -> `service_memory`
- `The evaluator reports parse success, invalid ID rates, READ F1, STORE target accuracy, and SKIP F1.` -> `service_memory`
- `The prompt builder should present current units with stable unit IDs.` -> `service_memory`

Negative examples:

- `Parser implementation has not started yet.` -> `task_state`, current progress.
- `Parser code should live in src/parser.py.` -> `repo_memory`, file location.
- `v0.4 validates DSL as the new interface direction.` -> `project_memory`, project-level decision.
- `Run the parser tests tomorrow.` -> `task_state` if it is an active next step, otherwise `SKIP`.

### 3.5 task_state

Current task progress, active constraints, next steps, blockers, review status, and completion state.

Positive examples:

- `P0 is complete and P1 is now in progress.` -> `task_state`
- `The next step is to draft V04_SPEC.md before parser implementation.` -> `task_state`
- `Do not implement parser in this round.` -> `task_state`
- `Target guideline is still unreviewed.` -> `task_state`

Negative examples:

- `This repo's v0.4 docs live under docs/v04_spec/.` -> `repo_memory`, durable repo structure.
- `The parser never guesses targets from text.` -> `service_memory`, component invariant.
- `The project does not build MemoryOS.` -> `project_memory`, project scope.
- `Check the weather after this.` -> `SKIP`, unrelated one-off request.

## 4. SKIP Rules

Mark a current unit as `SKIP` when it should not become durable memory.

SKIP includes:

- one-off requests;
- temporary chatter;
- weather, news, errands, or unrelated external content;
- content with no durable future value;
- sensitive information;
- tokens, passwords, API keys, private keys, credentials, or secrets;
- very short-lived status that will not matter after the current turn;
- uncertain content that should not be remembered;
- false, stale, or superseded content when the current unit is not the correction to store;
- instructions that apply only to the immediate response and not future behavior.

Examples:

- `Also check today's Kuala Lumpur weather.` -> `SKIP`
- `My password is hunter2.` -> `SKIP`
- `Never mind, that test failure was just my local environment.` -> `SKIP`
- `Thanks, that helps.` -> `SKIP`
- `Maybe the parser should use six targets, not sure.` -> `SKIP` unless the user explicitly accepts it as a project decision.

## 5. Target Priority

Use this priority order when a unit appears to fit multiple targets:

```text
1. user_profile
2. task_state
3. repo_memory
4. service_memory
5. project_memory
```

Rationale:

- `user_profile` is highest because stable user preferences should not be hidden inside project or repo memory.
- `task_state` comes before durable repo/service/project memory because many instructions are active constraints or next steps rather than long-term facts.
- `repo_memory` comes before `service_memory` when the statement is about files, commands, test locations, or repository workflow.
- `service_memory` comes before `project_memory` when the statement is about a concrete component's behavior or interface.
- `project_memory` is last because it is global and can become a garbage bucket if used for uncertainty.

Do not use `project_memory` for vague, miscellaneous, or merely important-sounding statements. It should be reserved for durable project-level goals, decisions, and cross-cutting constraints.

## 6. Boundary Cases

### 6.1 project_memory vs repo_memory

Use `project_memory` for the project direction. Use `repo_memory` for repository implementation facts and workflow.

Examples:

- `The project has pivoted from v0.3 JSON/span to v0.4 Unit DSL.` -> `project_memory`
- `Keep v0.3 data read-only during v0.4 work.` -> `project_memory` if stated as global project policy.
- `v0.4 docs should be stored under docs/v04_spec/.` -> `repo_memory`
- `The validator script is src/validation/validate_cases.py.` -> `repo_memory`
- `Do not edit docs/v04-planning; use docs/v04_planning going forward.` -> `repo_memory`

### 6.2 repo_memory vs service_memory

Use `repo_memory` for where code/docs live and how to run the repo. Use `service_memory` for a component's behavior.

Examples:

- `Parser implementation should live under src/parser.py.` -> `repo_memory`
- `Parser tests should run with pytest tests/parser.` -> `repo_memory`
- `The parser rejects unknown memory IDs.` -> `service_memory`
- `The evaluator computes STORE target accuracy.` -> `service_memory`
- `The DSL prompt lives under prompts/v04/unit_dsl.txt.` -> `repo_memory`

### 6.3 service_memory vs task_state

Use `service_memory` for durable component facts. Use `task_state` for current progress, next actions, or temporary constraints.

Examples:

- `The parser does not perform semantic repair.` -> `service_memory`
- `The parser canonicalizes valid DSL into memory_policy.v0.4 JSON.` -> `service_memory`
- `Parser implementation has not started yet.` -> `task_state`
- `Next, write parser tests for duplicate unit assignment.` -> `task_state`
- `The parser draft is blocked on target guideline review.` -> `task_state`

### 6.4 user_profile vs sensitive/private content

Use `user_profile` only for stable, non-sensitive preferences. Sensitive material must be skipped even if it appears user-specific.

Examples:

- `I prefer Chinese explanations for architecture decisions.` -> `user_profile`
- `I like status reports with files changed and commands run.` -> `user_profile`
- `My personal phone number is 555-1234.` -> `SKIP`
- `Use this private key for deployment: -----BEGIN PRIVATE KEY-----...` -> `SKIP`
- `Remember that my home address is ...` -> `SKIP`

### 6.5 SOP/skill out-of-scope vs repo/project/service convention

v0.4 does not create a `sop` target and does not model skills. Recurring procedures may still be stored if they are clearly a project, repo, or service convention.

Examples:

- `For this repo, always run the validator after data/*.jsonl changes.` -> `repo_memory`
- `For this project, do not connect to real APIs unless explicitly requested.` -> `project_memory`
- `The parser module should report validation errors instead of repairing output.` -> `service_memory`
- `Use the existing code-review stance when I ask for review.` -> `user_profile` if stable across projects.
- `Create a reusable skill system for SOPs.` -> `SKIP` for v0.4 unless explicitly accepted in a future scope change; SOP/skill system is out of scope.

## 7. Explicitly Forbidden Labels And Actions

Do not annotate:

```text
fact
decision
preference
sop
type
subtype
entity
reason
confidence
needs_review
```

Do not annotate memory lifecycle operations:

```text
ADD
UPDATE
DELETE
MERGE
deduplicate
decay
canonical rewrite
truth verification
```

Gold labels for v0.4 are only:

```text
READ candidate memory IDs
STORE target + unit_id
SKIP unit_id
```

"""Prompt templates for future synthetic dataset generation."""

from __future__ import annotations

from dataclasses import dataclass

from src.schemas import Category


@dataclass(frozen=True)
class GenerationPromptTemplate:
    """A named prompt template with a stable generator prompt ID."""

    name: str
    generator_prompt_id: str
    prompt_version: str
    description: str
    template: str

    def render(self, *, count: int, categories: list[str] | None = None) -> str:
        selected_categories = categories or [category.value for category in Category]
        return self.template.format(
            count=count,
            categories=", ".join(selected_categories),
        )


COMMON_REQUIREMENTS = """\
Return JSONL only, one complete JSON object per line.
Use English dataset content only.
Use the field name target, not expected_output.
Keep candidate_memories to 0-8 items and recent_context to 0-4 turns.
read_hints must reference IDs present in candidate_memories.
write_spans[*].span and ignore_spans[*] must be exact substrings of current_user_input.
Use only memory types: sop, fact, decision, task_state.
Prefer fact, decision, and task_state writes over generic sop writes unless the user
explicitly states a durable workflow rule.
Do not include character offsets in training or seed examples.
"""


DIRECT_CODING_AGENT_PROMPT = f"""\
You are generating supervised examples for a memory policy router used inside a coding agent.

The router receives current_user_input, recent_context, and candidate_memories.
The router predicts target.read_hints, target.write_spans, and target.ignore_spans.
The practical focus is remembering business/project progress, durable preferences and
decisions, and important facts while avoiding memory pollution from temporary noise.

Generate {{count}} diverse decision cases for coding-agent workflows.

{COMMON_REQUIREMENTS}

Cover these categories when possible: {{categories}}.
Use realistic backend, frontend, testing, CLI, DevOps, and research-engineering scenarios.
Include active bugs, next steps, architecture facts, business-domain facts, durable
preferences, correction messages, and relevant-memory selection.
Avoid near-duplicate wording.
"""


GAME_DEV_WORKFLOW_PROMPT = f"""\
You are generating supervised examples for a memory policy router used in game-development
coding workflows.

Generate {{count}} decision cases about controlled game-dev work.

{COMMON_REQUIREMENTS}

Cover these categories when possible: {{categories}}.
Use scenarios about Godot version constraints, input maps, scene organization, save/load
implementation, asset import rules, debug overlays, and postponed integrations.
Include current implementation progress, active bugs, architecture facts, and next steps.
Do not require real Godot or godogen integration.
"""


HARD_NEGATIVE_NOISY_MEMORY_PROMPT = f"""\
You are generating hard-negative examples for a memory policy router.

Generate {{count}} decision cases where the main challenge is avoiding memory pollution.

{COMMON_REQUIREMENTS}

Cover these categories when possible: {{categories}}.
Include temporary tool failures, recovered crashes, casual chatter, incorrect statements that
are immediately corrected, conflicting candidate memories, irrelevant candidate memories, and
no_action_needed turns.
Mix durable preferences, important facts, and active task-state updates with throwaway text.
Label ignore_spans selectively; do not label every leftover phrase as ignore.
"""


PROMPT_TEMPLATES: dict[str, GenerationPromptTemplate] = {
    "direct_coding_agent": GenerationPromptTemplate(
        name="direct_coding_agent",
        generator_prompt_id="direct_coding_agent_v2",
        prompt_version="v2",
        description="Business/project memory examples for coding agents.",
        template=DIRECT_CODING_AGENT_PROMPT,
    ),
    "game_dev_workflow": GenerationPromptTemplate(
        name="game_dev_workflow",
        generator_prompt_id="game_dev_workflow_v2",
        prompt_version="v2",
        description="Game-dev progress, fact, decision, and noise-filtering examples.",
        template=GAME_DEV_WORKFLOW_PROMPT,
    ),
    "hard_negative_noisy_memory": GenerationPromptTemplate(
        name="hard_negative_noisy_memory",
        generator_prompt_id="hard_negative_noisy_memory_v2",
        prompt_version="v2",
        description="Hard negatives for business-memory pollution and irrelevant reads.",
        template=HARD_NEGATIVE_NOISY_MEMORY_PROMPT,
    ),
}


def get_template(name: str) -> GenerationPromptTemplate:
    try:
        return PROMPT_TEMPLATES[name]
    except KeyError as exc:
        available = ", ".join(sorted(PROMPT_TEMPLATES))
        raise ValueError(f"unknown template {name!r}; available templates: {available}") from exc

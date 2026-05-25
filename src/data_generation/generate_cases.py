"""Dry-run and mock synthetic data generation CLI.

This module intentionally does not call a real model API. It exists to make the future
generation interface explicit while keeping offline runs reproducible.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_generation.pipeline import run_generation_pipeline
from src.data_generation.prompt_templates import PROMPT_TEMPLATES, get_template
from src.data_generation.providers import LocalMockProvider


def default_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"mock_{timestamp}"


def parse_template_names(raw_templates: str | None, fallback_template: str) -> list[str]:
    if raw_templates is None:
        return [fallback_template]

    template_names = [name.strip() for name in raw_templates.split(",") if name.strip()]
    if not template_names:
        raise ValueError("--templates must include at least one template name")

    unknown = [name for name in template_names if name not in PROMPT_TEMPLATES]
    if unknown:
        available = ", ".join(sorted(PROMPT_TEMPLATES))
        raise ValueError(f"unknown template names {unknown}; available templates: {available}")

    return template_names


def make_mock_records(count: int, template_names: list[str], run_id: str) -> list[dict[str, Any]]:
    return LocalMockProvider().generate(
        count=count,
        template_names=template_names,
        run_id=run_id,
    )


def build_generation_metadata(
    *,
    mode: str,
    workflow: str | None,
    requested_count: int,
    template_names: list[str],
) -> dict[str, Any]:
    templates = [get_template(name) for name in template_names]
    provider_metadata = LocalMockProvider.metadata
    return {
        "mode": mode,
        "workflow": workflow,
        "generator_name": provider_metadata.name,
        "generator_version": provider_metadata.version,
        "requested_count": requested_count,
        "schema_target_field": "target",
        "api_provider": provider_metadata.api_provider,
        "model_name": provider_metadata.model_name,
        "prompt_templates": [
            {
                "name": template.name,
                "generator_prompt_id": template.generator_prompt_id,
                "prompt_version": template.prompt_version,
                "description": template.description,
            }
            for template in templates
        ],
    }


def write_jsonl(records: list[dict[str, Any]], output_path: Path | None) -> None:
    lines = [json.dumps(record, ensure_ascii=True) for record in records]
    body = "\n".join(lines)
    if body:
        body += "\n"

    if output_path is None:
        print(body, end="")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(body, encoding="utf-8")
    print(f"Wrote {len(records)} mock cases to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--template",
        default="direct_coding_agent",
        choices=sorted(PROMPT_TEMPLATES),
        help="Prompt template to render or use for mock metadata.",
    )
    parser.add_argument("--count", type=int, help="Number of cases to request.")
    parser.add_argument("--dry-run", action="store_true", help="Print the rendered prompt only.")
    parser.add_argument("--mock", action="store_true", help="Emit deterministic mock JSONL cases.")
    parser.add_argument("--output", type=Path, help="Optional output path for mock JSONL cases.")
    parser.add_argument(
        "--workflow",
        choices=["small-draft"],
        help="Run a named offline generation workflow.",
    )
    parser.add_argument(
        "--run-id",
        help="Stable run identifier. Defaults to a UTC timestamp-based ID.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("data/synthetic_drafts"),
        help="Root directory for workflow outputs.",
    )
    parser.add_argument(
        "--templates",
        help="Comma-separated template names for workflow/mock pipeline runs.",
    )
    parser.add_argument(
        "--min-per-category",
        type=int,
        default=0,
        help="Minimum per category for post-generation validation.",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List available prompt templates and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list_templates:
        for name, template in PROMPT_TEMPLATES.items():
            print(f"{name}: {template.description}")
        return 0

    template = get_template(args.template)
    count = args.count if args.count is not None else (100 if args.workflow else 5)

    if args.dry_run:
        print(template.render(count=count))
        return 0

    if args.workflow == "small-draft":
        run_id = args.run_id or default_run_id()
        template_names = parse_template_names(
            args.templates,
            fallback_template=args.template,
        )
        if args.templates is None:
            template_names = list(PROMPT_TEMPLATES)
        records = make_mock_records(count=count, template_names=template_names, run_id=run_id)
        metadata = build_generation_metadata(
            mode="mock",
            workflow=args.workflow,
            requested_count=count,
            template_names=template_names,
        )
        result = run_generation_pipeline(
            records=records,
            output_root=args.output_root,
            run_id=run_id,
            metadata=metadata,
            min_per_category=args.min_per_category,
        )
        print(f"Run ID: {result.run_id}")
        print(f"Raw cases: {result.paths.raw_cases}")
        print(f"Valid cases: {result.paths.valid_cases}")
        print(f"Invalid samples: {result.paths.invalid_samples}")
        print(f"Metadata: {result.paths.metadata}")
        print(f"Validation report: {result.paths.validation_report}")
        print(f"Distribution report: {result.paths.distribution_report}")
        print(f"Valid/invalid: {result.valid_count}/{result.invalid_count}")
        print(f"Structural validation passed: {result.validation_passed}")
        return 0 if result.validation_passed else 1

    if args.mock:
        run_id = args.run_id or "adhoc"
        template_names = parse_template_names(args.templates, fallback_template=args.template)
        records = make_mock_records(count=count, template_names=template_names, run_id=run_id)
        write_jsonl(records, args.output)
        return 0

    print(
        "No real API integration is configured. Use --dry-run to render a prompt or "
        "--mock to emit deterministic mock JSONL.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

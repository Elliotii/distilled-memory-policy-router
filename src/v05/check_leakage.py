"""Lightweight offline leakage and near-duplicate checker.

Checks cross-contamination between two JSONL case files (e.g., train vs dev,
train vs gold).  Uses exact-text, normalized-text, and n-gram Jaccard overlap.
No external APIs, no embeddings required by default.

CLI
---
PYTHONDONTWRITEBYTECODE=1 python -m src.v05.check_leakage \\
  --train data/v05/batches/v05_batch500_corrected_cases.jsonl \\
  --candidate data/v05/batches/v05_batch500_corrected_cases.jsonl \\
  --out reports/v05/v05_leakage_checker_smoke_report.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

_NON_ALPHA_SPACE = re.compile(r"[^a-z0-9 ]")
_MULTI_SPACE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Lower-case, strip, collapse whitespace, remove punctuation."""
    text = text.lower().strip()
    text = _NON_ALPHA_SPACE.sub(" ", text)
    text = _MULTI_SPACE.sub(" ", text)
    return text.strip()


def token_ngrams(text: str, n: int = 3) -> set[str]:
    """Return a set of word-level *n*-gram strings.

    Short texts (fewer than *n* words) are handled by the caller via
    token-level Jaccard fallback.
    """
    tokens = normalize_text(text).split()
    if len(tokens) < n:
        return set()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def token_set(text: str) -> set[str]:
    """Return the set of normalized word tokens (one-gram fallback)."""
    return set(normalize_text(text).split())


def jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity between two sets.  0.0 when union is empty."""
    if not a and not b:
        return 1.0  # both empty → identical by convention
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ---------------------------------------------------------------------------
# Data extraction
# ---------------------------------------------------------------------------

@dataclass
class CaseTexts:
    case_id: str
    runtime_context: dict[str, str]
    unit_texts: list[str]  # current_units[*].text
    memory_contents: list[str]  # candidate_memories[*].content


def extract_case_texts(record: dict[str, Any]) -> CaseTexts:
    """Pull relevant fields from one case record."""
    rc = record.get("runtime_context", {})
    units = [u["text"] for u in record.get("current_units", [])]
    mems = [m["content"] for m in record.get("candidate_memories", [])]
    return CaseTexts(
        case_id=record["case_id"],
        runtime_context={
            "project": rc.get("project", ""),
            "repo": rc.get("repo", ""),
            "service": rc.get("service", ""),
            "task": rc.get("task", ""),
        },
        unit_texts=units,
        memory_contents=mems,
    )


# ---------------------------------------------------------------------------
# Core checking logic
# ---------------------------------------------------------------------------

@dataclass
class FlaggedPair:
    kind: str  # "exact_unit", "exact_memory", "near_dup_unit", …
    severity: str  # "hard_blocker" | "review" | "warn"
    train_case_id: str
    candidate_case_id: str
    train_text: str = ""
    candidate_text: str = ""
    score: float = 0.0


@dataclass
class LeakageResult:
    train_path: str
    candidate_path: str
    train_count: int
    candidate_count: int
    hard_blockers: list[FlaggedPair] = field(default_factory=list)
    warnings: list[FlaggedPair] = field(default_factory=list)

    @property
    def blocked(self) -> bool:
        return len(self.hard_blockers) > 0


def _ctx_tuple(ctx: dict[str, str]) -> tuple[str, str, str, str]:
    return (ctx["project"], ctx["repo"], ctx["service"], ctx["task"])


def check_leakage(
    train_records: list[dict[str, Any]],
    candidate_records: list[dict[str, Any]],
    *,
    jaccard_review_threshold: float = 0.8,
    jaccard_warn_threshold: float = 0.5,
) -> LeakageResult:
    """Run all leakage checks between *train_records* and *candidate_records*.

    Parameters
    ----------
    jaccard_review_threshold:
        Pairs with n-gram Jaccard >= this value are flagged as ``"review"``.
    jaccard_warn_threshold:
        Pairs with n-gram Jaccard >= this value but below
        *jaccard_review_threshold* are flagged as ``"warn"``.

    Returns
    -------
    LeakageResult
    """
    train_texts = [extract_case_texts(r) for r in train_records]
    cand_texts = [extract_case_texts(r) for r in candidate_records]

    result = LeakageResult(
        train_path="",
        candidate_path="",
        train_count=len(train_texts),
        candidate_count=len(cand_texts),
    )

    # Index lookups ----------------------------------------------------------
    train_ids = {t.case_id for t in train_texts}
    cand_ids = {t.case_id for t in cand_texts}

    train_unit_set: set[str] = set()
    train_unit_map: dict[str, str] = {}  # text -> case_id
    for t in train_texts:
        for u in t.unit_texts:
            train_unit_set.add(u)
            train_unit_map[u] = t.case_id

    train_mem_set: set[str] = set()
    train_mem_map: dict[str, str] = {}
    for t in train_texts:
        for m in t.memory_contents:
            train_mem_set.add(m)
            train_mem_map[m] = t.case_id

    # L0: duplicate case_id -------------------------------------------------
    dup_ids = train_ids & cand_ids
    for cid in sorted(dup_ids):
        result.hard_blockers.append(
            FlaggedPair(
                kind="duplicate_case_id",
                severity="hard_blocker",
                train_case_id=cid,
                candidate_case_id=cid,
            )
        )

    # L1: exact text match on current_units ---------------------------------
    cand_unit_set: set[str] = set()
    for t in cand_texts:
        for u in t.unit_texts:
            cand_unit_set.add(u)
            if u in train_unit_set:
                result.hard_blockers.append(
                    FlaggedPair(
                        kind="exact unit_text overlap",
                        severity="hard_blocker",
                        train_case_id=train_unit_map[u],
                        candidate_case_id=t.case_id,
                        train_text=u,
                        candidate_text=u,
                    )
                )

    # L1: exact text match on candidate_memories ----------------------------
    for t in cand_texts:
        for m in t.memory_contents:
            if m in train_mem_set:
                result.hard_blockers.append(
                    FlaggedPair(
                        kind="exact memory content overlap",
                        severity="hard_blocker",
                        train_case_id=train_mem_map[m],
                        candidate_case_id=t.case_id,
                        train_text=m,
                        candidate_text=m,
                    )
                )

    # L2: normalized text overlap (warn, not hard block) -------------------
    train_unit_norm: dict[str, str] = {
        normalize_text(u): cid
        for t in train_texts
        for u in t.unit_texts
        for cid in [t.case_id]
    }
    train_mem_norm: dict[str, str] = {
        normalize_text(m): cid
        for t in train_texts
        for m in t.memory_contents
        for cid in [t.case_id]
    }

    for t in cand_texts:
        for u in t.unit_texts:
            nu = normalize_text(u)
            if nu and nu in train_unit_norm:
                result.warnings.append(
                    FlaggedPair(
                        kind="normalized_unit_text_overlap",
                        severity="warn",
                        train_case_id=train_unit_norm[nu],
                        candidate_case_id=t.case_id,
                        train_text=u,
                        candidate_text=u,
                    )
                )
        for m in t.memory_contents:
            nm = normalize_text(m)
            if nm and nm in train_mem_norm:
                result.warnings.append(
                    FlaggedPair(
                        kind="normalized_memory_content_overlap",
                        severity="warn",
                        train_case_id=train_mem_norm[nm],
                        candidate_case_id=t.case_id,
                        train_text=m,
                        candidate_text=m,
                    )
                )

    # L3: n-gram Jaccard with token-level fallback -------------------------
    # Pre-compute n-gram / token sets for train
    train_ngram_data: list[tuple[str, str, str, set[str], set[str]]] = []
    for t in train_texts:
        for u in t.unit_texts:
            ng = token_ngrams(u, n=3)
            toks = token_set(u)
            train_ngram_data.append((t.case_id, "unit", u, ng, toks))
        for m in t.memory_contents:
            ng = token_ngrams(m, n=3)
            toks = token_set(m)
            train_ngram_data.append((t.case_id, "memory", m, ng, toks))

    cand_ngram_data: list[tuple[str, str, str, set[str], set[str]]] = []
    for t in cand_texts:
        for u in t.unit_texts:
            ng = token_ngrams(u, n=3)
            toks = token_set(u)
            cand_ngram_data.append((t.case_id, "unit", u, ng, toks))
        for m in t.memory_contents:
            ng = token_ngrams(m, n=3)
            toks = token_set(m)
            cand_ngram_data.append((t.case_id, "memory", m, ng, toks))

    # Cross-compare candidates vs train
    for c_case, c_kind, c_text, c_ng, c_tok in cand_ngram_data:
        for t_case, t_kind, t_text, t_ng, t_tok in train_ngram_data:
            # Skip same-case-id comparisons for self-check
            if c_case == t_case and c_text == t_text:
                continue

            # Primary: 3-gram Jaccard
            jac = jaccard(c_ng, t_ng)

            # Fallback for short texts: token-level Jaccard
            if jac == 0.0:
                jac_tok = jaccard(c_tok, t_tok)
                if jac_tok > 0:
                    jac = jac_tok

            if jac >= jaccard_review_threshold:
                result.warnings.append(
                    FlaggedPair(
                        kind=f"near_duplicate_{c_kind}",
                        severity="review",
                        train_case_id=t_case,
                        candidate_case_id=c_case,
                        train_text=t_text,
                        candidate_text=c_text,
                        score=jac,
                    )
                )
            elif jac >= jaccard_warn_threshold:
                result.warnings.append(
                    FlaggedPair(
                        kind=f"near_duplicate_{c_kind}",
                        severity="warn",
                        train_case_id=t_case,
                        candidate_case_id=c_case,
                        train_text=t_text,
                        candidate_text=c_text,
                        score=jac,
                    )
                )

    # L4: runtime_context tuple collision ----------------------------------
    train_ctx_map: dict[tuple, str] = {}
    for t in train_texts:
        tup = _ctx_tuple(t.runtime_context)
        train_ctx_map.setdefault(tup, t.case_id)

    for t in cand_texts:
        tup = _ctx_tuple(t.runtime_context)
        if tup in train_ctx_map:
            result.warnings.append(
                FlaggedPair(
                    kind="runtime_context_tuple_collision",
                    severity="warn",
                    train_case_id=train_ctx_map[tup],
                    candidate_case_id=t.case_id,
                    train_text=str(tup),
                    candidate_text=str(tup),
                )
            )

    # L5: repeated text within candidate itself ----------------------------
    seen_units: dict[str, str] = {}
    for t in cand_texts:
        for u in t.unit_texts:
            if u in seen_units:
                result.warnings.append(
                    FlaggedPair(
                        kind="repeated_unit_text_in_candidate",
                        severity="warn",
                        train_case_id=seen_units[u],
                        candidate_case_id=t.case_id,
                        train_text=u,
                        candidate_text=u,
                    )
                )
            else:
                seen_units[u] = t.case_id

    seen_mems: dict[str, str] = {}
    for t in cand_texts:
        for m in t.memory_contents:
            if m in seen_mems:
                result.warnings.append(
                    FlaggedPair(
                        kind="repeated_memory_content_in_candidate",
                        severity="warn",
                        train_case_id=seen_mems[m],
                        candidate_case_id=t.case_id,
                        train_text=m,
                        candidate_text=m,
                    )
                )
            else:
                seen_mems[m] = t.case_id

    return result


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------


def write_markdown_report(result: LeakageResult, path: str) -> None:
    """Write a human-readable leakage report to *path*."""

    hard = result.hard_blockers
    warns = result.warnings

    lines: list[str] = []
    lines.append("# V0.5 Leakage Checker Report")
    lines.append("")
    lines.append(f"**Train file:** `{result.train_path}`  ")
    lines.append(f"**Candidate file:** `{result.candidate_path}`  ")
    lines.append(f"**Train cases:** {result.train_count}  ")
    lines.append(f"**Candidate cases:** {result.candidate_count}  ")
    lines.append("")

    # Self-check note
    if result.train_path == result.candidate_path:
        lines.append("> ⚠ **SELF-CHECK:** Train and candidate files are the same.  ")
        lines.append("> Exact overlaps are **expected** — this report is a tool sanity check,  ")
        lines.append("> not evidence of cross-split leakage.")
        lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Category | Count |")
    lines.append(f"|----------|:----:|")
    lines.append(f"| Hard blockers | {len(hard)} |")
    lines.append(f"| Review-level warnings | {sum(1 for w in warns if w.severity == 'review')} |")
    lines.append(f"| General warnings | {sum(1 for w in warns if w.severity == 'warn')} |")
    lines.append("")

    if result.blocked:
        lines.append(f"## ❌ Hard Blockers ({len(hard)})")
        lines.append("")
        lines.append("| Kind | Train case_id | Candidate case_id | Details |")
        lines.append("|------|---------------|-------------------|---------|")
        for h in hard:
            detail = h.train_text[:100] if h.train_text else "(id-only)"
            lines.append(
                f"| {h.kind} | `{h.train_case_id}` | `{h.candidate_case_id}` | {detail} |"
            )
        lines.append("")
    else:
        lines.append("## ✅ No Hard Blockers")
        lines.append("")

    if warns:
        lines.append(f"## Warnings ({len(warns)})")
        lines.append("")
        # Group by kind
        by_kind: dict[str, list[FlaggedPair]] = {}
        for w in warns:
            by_kind.setdefault(w.kind, []).append(w)

        for kind, items in sorted(by_kind.items()):
            lines.append(f"### {kind} ({len(items)} pairs)")
            lines.append("")
            lines.append(
                "| Severity | Train case_id | Candidate case_id | Score | Text snippet |"
            )
            lines.append(
                "|----------|---------------|-------------------|:-----:|--------------|"
            )
            for w in items[:50]:  # truncate long lists
                snippet = (
                    w.candidate_text[:80].replace("\n", " ")
                    if w.candidate_text
                    else "(context tuple)"
                )
                lines.append(
                    f"| {w.severity} | `{w.train_case_id}` | `{w.candidate_case_id}` "
                    f"| {w.score:.3f} | {snippet} |"
                )
            if len(items) > 50:
                lines.append(f"| ... | *({len(items) - 50} more)* | ... | ... | ... |")
            lines.append("")
    else:
        lines.append("## No Warnings")
        lines.append("")

    content = "\n".join(lines)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Offline leakage checker for v0.5 case files."
    )
    ap.add_argument(
        "--train",
        required=True,
        help="Path to train/pool cases JSONL.",
    )
    ap.add_argument(
        "--candidate",
        required=True,
        help="Path to dev/gold candidate cases JSONL.",
    )
    ap.add_argument(
        "--out",
        default=None,
        help="Path for Markdown report (optional).",
    )
    ap.add_argument(
        "--jaccard-review-threshold",
        type=float,
        default=0.8,
        help="Jaccard >= this value triggers review flag (default: 0.8).",
    )
    ap.add_argument(
        "--jaccard-warn-threshold",
        type=float,
        default=0.5,
        help="Jaccard >= this value (and < review) triggers warn flag (default: 0.5).",
    )
    args = ap.parse_args()

    train_path = Path(args.train)
    cand_path = Path(args.candidate)

    if not train_path.exists():
        print(f"ERROR: train file not found: {args.train}", file=sys.stderr)
        return 1
    if not cand_path.exists():
        print(f"ERROR: candidate file not found: {args.candidate}", file=sys.stderr)
        return 1

    train_records = [
        json.loads(line)
        for line in train_path.read_text(encoding="utf-8").strip().splitlines()
        if line.strip()
    ]
    cand_records = [
        json.loads(line)
        for line in cand_path.read_text(encoding="utf-8").strip().splitlines()
        if line.strip()
    ]

    result = check_leakage(
        train_records,
        cand_records,
        jaccard_review_threshold=args.jaccard_review_threshold,
        jaccard_warn_threshold=args.jaccard_warn_threshold,
    )
    result.train_path = str(train_path)
    result.candidate_path = str(cand_path)

    # Print summary to stdout
    print(f"Train: {result.train_count} cases  |  Candidate: {result.candidate_count} cases")
    print(f"Hard blockers: {len(result.hard_blockers)}")
    print(f"Warnings: {len(result.warnings)}  "
          f"(review: {sum(1 for w in result.warnings if w.severity == 'review')}, "
          f"warn: {sum(1 for w in result.warnings if w.severity == 'warn')})")

    if args.out:
        write_markdown_report(result, args.out)
        print(f"Report written to: {args.out}")
    else:
        # Minimal JSON summary
        summary = {
            "train_cases": result.train_count,
            "candidate_cases": result.candidate_count,
            "hard_blockers": len(result.hard_blockers),
            "warnings": len(result.warnings),
            "blocked": result.blocked,
        }
        print(json.dumps(summary, indent=2))

    return 1 if result.blocked else 0


if __name__ == "__main__":
    sys.exit(main())

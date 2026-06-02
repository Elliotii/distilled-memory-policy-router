"""Unit tests for src.v05.check_leakage."""

from __future__ import annotations

import unittest

from src.v05.check_leakage import (
    CaseTexts,
    FlaggedPair,
    check_leakage,
    extract_case_texts,
    jaccard,
    normalize_text,
    token_ngrams,
    token_set,
    write_markdown_report,
)


# ---------------------------------------------------------------------------
# Helpers to build minimal case records
# ---------------------------------------------------------------------------

def _make_case(
    case_id: str,
    unit_texts: list[str] | None = None,
    memory_contents: list[str] | None = None,
    project: str = "proj",
    repo: str = "repo",
    service: str = "svc",
    task: str = "task",
) -> dict:
    """Build a minimal case dict for testing."""
    units = [{"unit_id": f"u{i+1}", "text": t} for i, t in enumerate(unit_texts or [])]
    mems = [
        {"memory_id": f"m{i+1}", "target": "task_state", "content": c}
        for i, c in enumerate(memory_contents or [])
    ]
    return {
        "case_id": case_id,
        "runtime_context": {
            "project": project,
            "repo": repo,
            "service": service,
            "task": task,
        },
        "candidate_memories": mems,
        "current_units": units,
        "gold": {"read": [], "store": [], "skip": []},
        "tags": [],
        "notes": "",
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestNormalizeText(unittest.TestCase):
    def test_lowercases_and_collapses_whitespace(self):
        self.assertEqual(normalize_text("  Hello  World!  "), "hello world")

    def test_removes_punctuation(self):
        self.assertEqual(normalize_text("Hello, world."), "hello world")

    def test_preserves_digits(self):
        self.assertEqual(normalize_text("Qwen3-4B model"), "qwen3 4b model")

    def test_empty_string(self):
        self.assertEqual(normalize_text(""), "")

    def test_punctuation_only(self):
        self.assertEqual(normalize_text("!@#$%"), "")


class TestTokenNgrams(unittest.TestCase):
    def test_basic_3gram(self):
        ng = token_ngrams("the parser rejects unknown targets")
        self.assertIn("the parser rejects", ng)
        self.assertIn("parser rejects unknown", ng)
        self.assertIn("rejects unknown targets", ng)
        self.assertEqual(len(ng), 3)  # 5 words → 3 trigrams

    def test_short_text_returns_empty(self):
        self.assertEqual(token_ngrams("hello world"), set())

    def test_exact_n_words(self):
        ng = token_ngrams("one two three")
        self.assertEqual(len(ng), 1)
        self.assertIn("one two three", ng)


class TestTokenSet(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(token_set("hello world hello"), {"hello", "world"})

    def test_normalizes(self):
        self.assertEqual(token_set("Hello, World!"), {"hello", "world"})


class TestJaccard(unittest.TestCase):
    def test_identical(self):
        a = {"a", "b", "c"}
        b = {"a", "b", "c"}
        self.assertAlmostEqual(jaccard(a, b), 1.0)

    def test_disjoint(self):
        self.assertAlmostEqual(jaccard({"a"}, {"b"}), 0.0)

    def test_half_overlap(self):
        self.assertAlmostEqual(jaccard({"a", "b"}, {"b", "c"}), 1 / 3)

    def test_both_empty(self):
        self.assertAlmostEqual(jaccard(set(), set()), 1.0)

    def test_one_empty(self):
        self.assertAlmostEqual(jaccard({"a"}, set()), 0.0)


class TestExtractCaseTexts(unittest.TestCase):
    def test_extracts_all_fields(self):
        rec = _make_case("c1", unit_texts=["u1 text"], memory_contents=["m1 content"])
        ct = extract_case_texts(rec)
        self.assertEqual(ct.case_id, "c1")
        self.assertEqual(ct.unit_texts, ["u1 text"])
        self.assertEqual(ct.memory_contents, ["m1 content"])
        self.assertEqual(
            ct.runtime_context,
            {"project": "proj", "repo": "repo", "service": "svc", "task": "task"},
        )


class TestCheckLeakageHardBlockers(unittest.TestCase):
    def test_duplicate_case_id_detected(self):
        t = [_make_case("c1")]
        c = [_make_case("c1")]
        result = check_leakage(t, c)
        self.assertTrue(result.blocked)
        ids = [b.kind for b in result.hard_blockers]
        self.assertIn("duplicate_case_id", ids)

    def test_exact_unit_overlap_detected(self):
        t = [_make_case("c1", unit_texts=["the parser rejects unknown targets"])]
        c = [_make_case("c2", unit_texts=["the parser rejects unknown targets"])]
        result = check_leakage(t, c)
        self.assertTrue(result.blocked)
        kinds = [b.kind for b in result.hard_blockers]
        self.assertIn("exact unit_text overlap", kinds)

    def test_exact_memory_overlap_detected(self):
        t = [_make_case("c1", memory_contents=["memory about retry wrapper"])]
        c = [_make_case("c2", memory_contents=["memory about retry wrapper"])]
        result = check_leakage(t, c)
        self.assertTrue(result.blocked)
        kinds = [b.kind for b in result.hard_blockers]
        self.assertIn("exact memory content overlap", kinds)

    def test_no_hard_blockers_on_clean_data(self):
        t = [_make_case("c1", unit_texts=["alpha"], memory_contents=["alpha mem"])]
        c = [_make_case("c2", unit_texts=["beta"], memory_contents=["beta mem"])]
        result = check_leakage(t, c)
        self.assertFalse(result.blocked)


class TestCheckLeakageWarnings(unittest.TestCase):
    def test_ngram_jaccard_near_duplicate(self):
        t = [_make_case("c1", unit_texts=["the parser rejects unknown target types"])]
        c = [_make_case("c2", unit_texts=["the parser rejects unknown target tokens"])]
        result = check_leakage(t, c, jaccard_review_threshold=0.5)
        self.assertFalse(result.blocked)
        self.assertTrue(
            any(
                "near_duplicate" in w.kind and w.severity in ("warn", "review")
                for w in result.warnings
            ),
            f"Expected near_duplicate warning, got {result.warnings}",
        )

    def test_short_text_token_jaccard_fallback(self):
        # "hello world" has 2 words → no 3-grams; fallback to token Jaccard
        t = [_make_case("c1", unit_texts=["hello world"])]
        c = [_make_case("c2", unit_texts=["hello world"])]
        result = check_leakage(
            t, c, jaccard_review_threshold=0.5, jaccard_warn_threshold=0.2
        )
        # Exact text overlap also triggers hard blocker here
        # Let's use near-identical but not exact
        t2 = [_make_case("c1", unit_texts=["hello world"])]
        c2 = [_make_case("c2", unit_texts=["hello earth"])]
        result2 = check_leakage(
            t2, c2, jaccard_review_threshold=0.5, jaccard_warn_threshold=0.2
        )
        # token-level: {"hello","world"} vs {"hello","earth"} → 1/3 ≈ 0.333
        self.assertTrue(
            any(
                "near_duplicate" in w.kind for w in result2.warnings
            ),
            f"Expected token-Jaccard fallback warning, got {result2.warnings}",
        )

    def test_runtime_context_tuple_collision(self):
        t = [_make_case("c1", unit_texts=["a"])]
        c = [_make_case("c2", unit_texts=["b"])]  # same context
        result = check_leakage(t, c)
        self.assertTrue(
            any(w.kind == "runtime_context_tuple_collision" for w in result.warnings)
        )

    def test_repeated_text_in_candidate(self):
        t = [_make_case("c1", unit_texts=["x"])]
        c = [
            _make_case("c2", unit_texts=["shared unit text"]),
            _make_case("c3", unit_texts=["shared unit text"]),
        ]
        result = check_leakage(t, c)
        self.assertTrue(
            any(
                w.kind == "repeated_unit_text_in_candidate"
                for w in result.warnings
            )
        )

    def test_normalized_text_overlap_warning(self):
        t = [_make_case("c1", unit_texts=["Hello, World!"])]
        c = [_make_case("c2", unit_texts=["hello world"])]
        result = check_leakage(t, c)
        self.assertTrue(
            any(
                w.kind == "normalized_unit_text_overlap"
                for w in result.warnings
            )
        )


class TestHardBlockerVsWarningSeparation(unittest.TestCase):
    def test_counts_separated(self):
        t = [
            _make_case("c1", unit_texts=["exact overlap"],
                       memory_contents=["exact mem"]),
        ]
        c = [
            _make_case("c1"),  # duplicate id → hard
            _make_case("c2", unit_texts=["exact overlap"]),  # exact unit → hard
            _make_case("c3", unit_texts=["similar text here"]),
        ]
        # Also add a case with near-duplicate
        t2 = t + [_make_case("c_t", unit_texts=["similar text there"])]
        result = check_leakage(t2, c, jaccard_review_threshold=0.3)
        self.assertEqual(len(result.hard_blockers), 2)  # dup id + exact unit
        # warnings include review/warn + context collision + potential near-dup
        self.assertGreater(len(result.warnings), 0)
        self.assertFalse(
            any(b.severity != "hard_blocker" for b in result.hard_blockers)
        )


class TestWriteMarkdownReport(unittest.TestCase):
    def test_writes_expected_sections(self):
        from tempfile import NamedTemporaryFile
        from src.v05.check_leakage import LeakageResult

        res = LeakageResult(
            train_path="train.jsonl",
            candidate_path="cand.jsonl",
            train_count=10,
            candidate_count=5,
            hard_blockers=[
                FlaggedPair("exact unit_text overlap", "hard_blocker", "c1", "c2",
                            "text", "text")
            ],
            warnings=[
                FlaggedPair("near_duplicate_unit", "review", "c3", "c4",
                            "abc", "abd", 0.85),
                FlaggedPair("runtime_context_tuple_collision", "warn", "c5", "c6"),
            ],
        )

        with NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            write_markdown_report(res, tmp_path)
            content = open(tmp_path).read()

            self.assertIn("Hard blockers", content)
            self.assertIn("exact unit_text overlap", content)
            self.assertIn("Warnings", content)
            self.assertIn("near_duplicate_unit", content)
            self.assertIn("runtime_context_tuple_collision", content)
            self.assertIn("c1", content)
            self.assertIn("0.850", content)  # score displayed
        finally:
            import os
            os.unlink(tmp_path)

    def test_self_check_banner(self):
        from tempfile import NamedTemporaryFile
        from src.v05.check_leakage import LeakageResult

        res = LeakageResult(
            train_path="same.jsonl",
            candidate_path="same.jsonl",
            train_count=5,
            candidate_count=5,
        )
        with NamedTemporaryFile(mode="w", suffix=".md", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            write_markdown_report(res, tmp_path)
            content = open(tmp_path).read()
            self.assertIn("SELF-CHECK", content)
            self.assertIn("sanity check", content)
        finally:
            import os
            os.unlink(tmp_path)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()

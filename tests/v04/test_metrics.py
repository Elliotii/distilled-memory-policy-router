import json
import unittest

from src.v04.metrics import (
    INTERFACE_LEGACY_SPAN_JSON,
    INTERFACE_UNIT_DSL,
    INTERFACE_UNIT_JSON,
    evaluate_prediction_rows,
    parse_prediction,
)


def sample_case():
    return {
        "case_id": "v04_test_eval_0001",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "parser",
            "task": "eval smoke test",
        },
        "candidate_memories": [
            {
                "memory_id": "m1",
                "target": "service_memory",
                "content": "The parser rejects unknown STORE targets.",
            },
            {
                "memory_id": "m2",
                "target": "repo_memory",
                "content": "Parser tests live under tests/v04/test_parser.py.",
            },
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The parser rejects unknown STORE targets."},
            {"unit_id": "u2", "text": "Check tomorrow's weather after this."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [{"target": "service_memory", "unit_id": "u1"}],
            "skip": ["u2"],
            "dsl": "READ m1\nSTORE service_memory u1\nSKIP u2",
        },
        "tags": ["read_store_joint", "service_invariant"],
        "notes": "Minimal eval smoke case.",
    }


class V04MetricsTests(unittest.TestCase):
    def test_parse_unit_dsl_valid_prediction(self):
        case = sample_case()

        parsed = parse_prediction(
            "READ m1\nSTORE service_memory u1\nSKIP u2",
            INTERFACE_UNIT_DSL,
            case,
        )

        self.assertTrue(parsed.canonical["validation"]["valid"], parsed.canonical)
        self.assertEqual(parsed.canonical["read"], [{"memory_id": "m1"}])
        self.assertEqual(
            parsed.canonical["store"],
            [{"target": "service_memory", "unit_id": "u1"}],
        )
        self.assertEqual(parsed.canonical["skip"], [{"unit_id": "u2"}])

    def test_parse_legacy_span_json_maps_exact_unit_text(self):
        case = sample_case()
        raw = json.dumps(
            {
                "read_hints": ["m1"],
                "write_spans": [
                    {
                        "span": "The parser rejects unknown STORE targets.",
                        "type": "service_memory",
                    }
                ],
                "ignore_spans": ["Check tomorrow's weather after this."],
            }
        )

        parsed = parse_prediction(raw, INTERFACE_LEGACY_SPAN_JSON, case)

        self.assertTrue(parsed.canonical["validation"]["valid"], parsed.canonical)
        self.assertEqual(
            parsed.canonical["store"],
            [{"target": "service_memory", "unit_id": "u1"}],
        )
        self.assertEqual(parsed.diagnostics.invalid_span_refs, 0)

    def test_invalid_unit_json_counts_id_and_target_failures(self):
        case = sample_case()
        raw = json.dumps(
            {
                "read": ["m9"],
                "store": [{"target": "fact", "unit_id": "u9"}],
                "skip": ["u2"],
            }
        )

        parsed = parse_prediction(raw, INTERFACE_UNIT_JSON, case)

        self.assertFalse(parsed.canonical["validation"]["valid"])
        self.assertEqual(parsed.diagnostics.invalid_memory_refs, 1)
        self.assertEqual(parsed.diagnostics.invalid_unit_refs, 1)
        self.assertEqual(parsed.diagnostics.invalid_target_refs, 1)

    def test_evaluate_gold_prediction_is_perfect(self):
        case = sample_case()
        result = evaluate_prediction_rows(
            [case],
            [
                {
                    "case_id": case["case_id"],
                    "raw_output": "READ m1\nSTORE service_memory u1\nSKIP u2",
                }
            ],
            interface=INTERFACE_UNIT_DSL,
            system_name="gold",
        )

        self.assertEqual(result["structural"]["parse_success"]["rate"], 1.0)
        self.assertEqual(result["semantic"]["exact_target_match"]["rate"], 1.0)
        self.assertEqual(result["semantic"]["read"]["f1"], 1.0)
        self.assertEqual(result["semantic"]["store_unit"]["f1"], 1.0)
        self.assertEqual(result["semantic"]["skip"]["f1"], 1.0)


if __name__ == "__main__":
    unittest.main()

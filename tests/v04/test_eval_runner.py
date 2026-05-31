import json
import tempfile
import unittest

from src.v04.eval_runner import (
    build_prediction_rows,
    display_system_name,
    format_error_analysis,
    format_interface_report,
    load_prediction_jsonl,
    run_prediction_file_evaluation,
    run_evaluation,
)
from src.v04.metrics import INTERFACES, evaluate_prediction_rows
from tests.v04.test_metrics import sample_case


class V04EvalRunnerTests(unittest.TestCase):
    def test_gold_baseline_renders_perfect_predictions_for_all_interfaces(self):
        case = sample_case()

        for interface in INTERFACES:
            with self.subTest(interface=interface):
                rows = build_prediction_rows([case], interface=interface, baseline="gold")
                result = evaluate_prediction_rows(
                    [case],
                    rows,
                    interface=interface,
                    system_name="gold",
                )

                self.assertEqual(result["structural"]["parse_success"]["rate"], 1.0)
                self.assertEqual(result["semantic"]["exact_target_match"]["rate"], 1.0)

    def test_invalid_mock_fails_structural_validation_for_all_interfaces(self):
        case = sample_case()

        for interface in INTERFACES:
            with self.subTest(interface=interface):
                rows = build_prediction_rows([case], interface=interface, baseline="invalid_mock")
                result = evaluate_prediction_rows(
                    [case],
                    rows,
                    interface=interface,
                    system_name="invalid_mock",
                )

                self.assertEqual(result["structural"]["parse_success"]["rate"], 0.0)
                self.assertGreater(result["structural"]["schema_error_count"], 0)

    def test_run_evaluation_returns_interface_system_grid(self):
        case = sample_case()

        results = run_evaluation(
            [case],
            interfaces=list(INTERFACES),
            baselines=["gold", "empty"],
            top_k=1,
        )

        self.assertEqual(len(results), len(INTERFACES) * 2)
        self.assertEqual(display_system_name("topk_read", top_k=3), "top3_read")

    def test_report_formatters_mark_results_as_smoke_only(self):
        case = sample_case()
        results = run_evaluation(
            [case],
            interfaces=list(INTERFACES),
            baselines=["gold", "invalid_mock"],
            top_k=1,
        )

        interface_report = format_interface_report(
            cases_path="data/v04/pilot_cases.jsonl",
            cases=[case],
            results=results,
            top_k=1,
        )
        error_report = format_error_analysis(cases=[case], results=results, top_k=1)

        self.assertIn("deterministic baselines only", interface_report)
        self.assertIn("not model error analysis", error_report)

    def test_external_prediction_jsonl_loads_and_evaluates(self):
        case = sample_case()
        row = {
            "case_id": case["case_id"],
            "interface": "unit_dsl",
            "system": "external_smoke",
            "raw_output": "READ m1\nSTORE service_memory u1\nSKIP u2",
            "model_id": "ignored_optional_metadata",
        }

        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".jsonl") as handle:
            handle.write(json.dumps(row) + "\n")
            handle.flush()

            rows = load_prediction_jsonl(handle.name)

        results = run_prediction_file_evaluation([case], rows)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["interface"], "unit_dsl")
        self.assertEqual(results[0]["system"], "external_smoke")
        self.assertEqual(results[0]["semantic"]["exact_target_match"]["rate"], 1.0)

    def test_external_prediction_jsonl_allows_empty_raw_output_for_failed_calls(self):
        case = sample_case()
        row = {
            "case_id": case["case_id"],
            "interface": "unit_dsl",
            "system": "external_smoke",
            "raw_output": "",
            "error": "empty model output",
        }

        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".jsonl") as handle:
            handle.write(json.dumps(row) + "\n")
            handle.flush()

            rows = load_prediction_jsonl(handle.name)

        results = run_prediction_file_evaluation([case], rows)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["structural"]["parse_success"]["rate"], 0.0)


if __name__ == "__main__":
    unittest.main()

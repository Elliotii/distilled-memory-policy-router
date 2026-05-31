import copy
import unittest
from pathlib import Path

from src.v04.case_validator import validate_case, validate_jsonl_file


def valid_case():
    return {
        "case_id": "v04_test_valid_0001",
        "runtime_context": {
            "project": "memory-router",
            "repo": "distilled-memory-policy-router",
            "service": "parser",
            "task": "case validator tests",
        },
        "candidate_memories": [
            {
                "memory_id": "m1",
                "target": "project_memory",
                "content": "v0.4 is an interface pilot before v0.5 training.",
            }
        ],
        "current_units": [
            {"unit_id": "u1", "text": "The parser should remain strict."},
            {"unit_id": "u2", "text": "Check tomorrow's weather after this."},
        ],
        "gold": {
            "read": ["m1"],
            "store": [{"target": "service_memory", "unit_id": "u1"}],
            "skip": ["u2"],
            "dsl": "READ m1\nSTORE service_memory u1\nSKIP u2",
        },
        "tags": ["read_store_joint"],
        "notes": "Valid minimal case for validator tests.",
    }


class CaseValidatorTests(unittest.TestCase):
    def assertValid(self, result):
        self.assertEqual(result, {"valid": True, "errors": []})

    def assertInvalid(self, result, expected_error):
        self.assertFalse(result["valid"])
        self.assertIn(expected_error, result["errors"])

    def test_valid_minimal_case(self):
        self.assertValid(validate_case(valid_case()))

    def test_missing_required_top_level_field(self):
        case = valid_case()
        del case["runtime_context"]

        self.assertInvalid(validate_case(case), "missing required field: runtime_context")

    def test_duplicate_candidate_memory_id(self):
        case = valid_case()
        case["candidate_memories"].append(copy.deepcopy(case["candidate_memories"][0]))

        self.assertInvalid(validate_case(case), "duplicate candidate memory_id: m1")

    def test_duplicate_current_unit_id(self):
        case = valid_case()
        case["current_units"].append(copy.deepcopy(case["current_units"][0]))

        self.assertInvalid(validate_case(case), "duplicate current unit_id: u1")

    def test_invalid_candidate_memory_target(self):
        case = valid_case()
        case["candidate_memories"][0]["target"] = "fact"

        self.assertInvalid(validate_case(case), "invalid candidate memory target for m1: fact")

    def test_gold_read_unknown_memory_id(self):
        case = valid_case()
        case["gold"]["read"] = ["m9"]
        case["gold"]["dsl"] = "READ m9\nSTORE service_memory u1\nSKIP u2"

        self.assertInvalid(validate_case(case), "gold.read unknown memory_id: m9")

    def test_gold_store_unknown_unit_id(self):
        case = valid_case()
        case["gold"]["store"] = [{"target": "service_memory", "unit_id": "u9"}]
        case["gold"]["skip"] = ["u1", "u2"]
        case["gold"]["dsl"] = "READ m1\nSTORE service_memory u9\nSKIP u1,u2"

        self.assertInvalid(validate_case(case), "gold.store unknown unit_id: u9")

    def test_gold_skip_unknown_unit_id(self):
        case = valid_case()
        case["gold"]["skip"] = ["u9"]
        case["gold"]["dsl"] = "READ m1\nSTORE service_memory u1\nSKIP u9"

        self.assertInvalid(validate_case(case), "gold.skip unknown unit_id: u9")

    def test_gold_store_invalid_target(self):
        case = valid_case()
        case["gold"]["store"] = [{"target": "fact", "unit_id": "u1"}]
        case["gold"]["dsl"] = "READ m1\nSTORE fact u1\nSKIP u2"

        self.assertInvalid(validate_case(case), "gold.store invalid target for u1: fact")

    def test_unit_missing_from_both_store_and_skip(self):
        case = valid_case()
        case["gold"]["skip"] = []
        case["gold"]["dsl"] = "READ m1\nSTORE service_memory u1\nSKIP NONE"

        self.assertInvalid(validate_case(case), "unit missing from gold.store/gold.skip: u2")

    def test_unit_appears_in_both_store_and_skip(self):
        case = valid_case()
        case["gold"]["skip"] = ["u1", "u2"]
        case["gold"]["dsl"] = "READ m1\nSTORE service_memory u1\nSKIP u1,u2"

        self.assertInvalid(validate_case(case), "unit appears in both gold.store and gold.skip: u1")

    def test_gold_dsl_consistent_with_gold(self):
        self.assertValid(validate_case(valid_case()))

    def test_gold_dsl_inconsistent_with_gold(self):
        case = valid_case()
        case["gold"]["dsl"] = "READ NONE\nSTORE service_memory u1\nSKIP u2"

        self.assertInvalid(validate_case(case), "gold.dsl read does not match gold.read")

    def test_sensitive_tag_case_structurally_valid_if_skip(self):
        case = valid_case()
        case["case_id"] = "v04_test_sensitive_0001"
        case["current_units"] = [
            {"unit_id": "u1", "text": "My API key is PLACEHOLDER_API_KEY_SHOULD_NOT_BE_STORED."}
        ]
        case["gold"] = {
            "read": [],
            "store": [],
            "skip": ["u1"],
            "dsl": "READ NONE\nSTORE NONE\nSKIP u1",
        }
        case["tags"] = ["sensitive_boundary"]
        case["notes"] = "Sensitive content is skipped. Validator only checks structure."

        self.assertValid(validate_case(case))

    def test_template_jsonl_loads_line_by_line_and_validates(self):
        repo_root = Path(__file__).resolve().parents[2]
        template_path = repo_root / "data" / "v04" / "bridge_cases_template.jsonl"

        result = validate_jsonl_file(template_path)

        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["record_count"], 5)


if __name__ == "__main__":
    unittest.main()

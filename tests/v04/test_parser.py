import unittest

from src.v04.parser import LEGAL_TARGETS, SCHEMA_VERSION, parse_policy_dsl


MEMORY_IDS = ["m1", "m2", "m3"]
UNIT_IDS = ["u1", "u2", "u3"]


def parse(raw, memory_ids=MEMORY_IDS, unit_ids=UNIT_IDS):
    return parse_policy_dsl(raw, memory_ids, unit_ids, LEGAL_TARGETS)


class ParserTests(unittest.TestCase):
    def assertValid(self, result):
        self.assertEqual(result["schema_version"], SCHEMA_VERSION)
        self.assertEqual(result["validation"], {"valid": True, "errors": []})

    def assertInvalid(self, result, expected_error):
        self.assertEqual(result["schema_version"], SCHEMA_VERSION)
        self.assertFalse(result["validation"]["valid"])
        self.assertIn(expected_error, result["validation"]["errors"])
        self.assertEqual(result["read"], [])
        self.assertEqual(result["store"], [])
        self.assertEqual(result["skip"], [])

    def test_valid_read_store_skip(self):
        result = parse(
            """
            READ m1,m3
            STORE task_state u1
            STORE repo_memory u2
            SKIP u3
            """
        )

        self.assertValid(result)
        self.assertEqual(result["read"], [{"memory_id": "m1"}, {"memory_id": "m3"}])
        self.assertEqual(
            result["store"],
            [
                {"target": "task_state", "unit_id": "u1"},
                {"target": "repo_memory", "unit_id": "u2"},
            ],
        )
        self.assertEqual(result["skip"], [{"unit_id": "u3"}])

    def test_valid_read_none(self):
        result = parse(
            """
            READ NONE
            STORE task_state u1
            STORE repo_memory u2
            SKIP u3
            """
        )

        self.assertValid(result)
        self.assertEqual(result["read"], [])

    def test_valid_store_none(self):
        result = parse(
            """
            READ m1
            STORE NONE
            SKIP u1,u2,u3
            """
        )

        self.assertValid(result)
        self.assertEqual(result["store"], [])

    def test_valid_skip_none(self):
        result = parse(
            """
            READ m1
            STORE task_state u1
            STORE repo_memory u2
            STORE service_memory u3
            SKIP NONE
            """
        )

        self.assertValid(result)
        self.assertEqual(result["skip"], [])

    def test_comma_whitespace_normalization(self):
        result = parse(
            """
            READ m1, m3
            STORE task_state u1
            SKIP u2, u3
            """
        )

        self.assertValid(result)
        self.assertEqual(result["read"], [{"memory_id": "m1"}, {"memory_id": "m3"}])
        self.assertEqual(result["skip"], [{"unit_id": "u2"}, {"unit_id": "u3"}])

    def test_duplicate_read_ids_are_deduplicated(self):
        result = parse(
            """
            READ m1,m1,m2
            STORE task_state u1
            SKIP u2,u3
            """
        )

        self.assertValid(result)
        self.assertEqual(result["read"], [{"memory_id": "m1"}, {"memory_id": "m2"}])

    def test_unknown_memory_id(self):
        result = parse(
            """
            READ m9
            STORE task_state u1
            SKIP u2,u3
            """
        )

        self.assertInvalid(result, "unknown memory_id: m9")

    def test_unknown_unit_id_in_store(self):
        result = parse(
            """
            READ m1
            STORE task_state u9
            SKIP u1,u2,u3
            """
        )

        self.assertInvalid(result, "unknown unit_id in STORE: u9")

    def test_unknown_unit_id_in_skip(self):
        result = parse(
            """
            READ m1
            STORE task_state u1
            SKIP u2,u9
            """
        )

        self.assertInvalid(result, "unknown unit_id in SKIP: u9")

    def test_invalid_target(self):
        result = parse(
            """
            READ m1
            STORE fact u1
            SKIP u2,u3
            """
        )

        self.assertInvalid(result, "invalid target: fact")

    def test_unit_appears_in_both_store_and_skip(self):
        result = parse(
            """
            READ m1
            STORE task_state u1
            SKIP u1,u2,u3
            """
        )

        self.assertInvalid(result, "unit appears in both STORE and SKIP: u1")

    def test_unit_missing_from_both_store_and_skip(self):
        result = parse(
            """
            READ m1
            STORE task_state u1
            SKIP u2
            """
        )

        self.assertInvalid(result, "missing unit assignment: u3")

    def test_duplicate_store_unit(self):
        result = parse(
            """
            READ m1
            STORE task_state u1
            STORE repo_memory u1
            SKIP u2,u3
            """
        )

        self.assertInvalid(result, "duplicate STORE unit_id: u1")

    def test_duplicate_skip_unit(self):
        result = parse(
            """
            READ m1
            STORE task_state u1
            SKIP u2,u2,u3
            """
        )

        self.assertInvalid(result, "duplicate SKIP unit_id: u2")

    def test_two_read_lines(self):
        result = parse(
            """
            READ m1
            READ m2
            STORE task_state u1
            SKIP u2,u3
            """
        )

        self.assertInvalid(result, "duplicate READ line")

    def test_two_skip_lines(self):
        result = parse(
            """
            READ m1
            STORE task_state u1
            SKIP u2
            SKIP u3
            """
        )

        self.assertInvalid(result, "duplicate SKIP line")

    def test_malformed_store_line(self):
        result = parse(
            """
            READ m1
            STORE task_state
            SKIP u1,u2,u3
            """
        )

        self.assertInvalid(result, "malformed STORE line: STORE task_state")

    def test_unknown_line_type(self):
        result = parse(
            """
            READ m1
            SAVE task_state u1
            SKIP u2,u3
            """
        )

        self.assertInvalid(result, "unknown line type: SAVE")

    def test_empty_output(self):
        result = parse("")

        self.assertInvalid(result, "empty output")

    def test_output_with_extra_blank_lines(self):
        result = parse(
            """

            READ m1

            STORE task_state u1

            SKIP u2,u3

            """
        )

        self.assertValid(result)
        self.assertEqual(result["read"], [{"memory_id": "m1"}])

    def test_store_none_cannot_be_combined_with_store_assignment(self):
        result = parse(
            """
            READ m1
            STORE NONE
            STORE task_state u1
            SKIP u2,u3
            """
        )

        self.assertInvalid(result, "STORE NONE cannot be combined with STORE assignments")


if __name__ == "__main__":
    unittest.main()

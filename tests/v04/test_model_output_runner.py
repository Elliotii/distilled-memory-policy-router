import unittest

from src.v04.model_output_runner import (
    extract_raw_output,
    sanitized_response_metadata,
)


class V04ModelOutputRunnerTests(unittest.TestCase):
    def test_extract_raw_output_prefers_message_content(self):
        data = {
            "choices": [
                {
                    "message": {
                        "content": "READ m1\nSTORE NONE\nSKIP u1",
                        "reasoning_content": "internal notes",
                    },
                    "finish_reason": "stop",
                }
            ]
        }

        raw_output, source = extract_raw_output(data)

        self.assertEqual(raw_output, "READ m1\nSTORE NONE\nSKIP u1")
        self.assertEqual(source, "message.content")

    def test_extract_raw_output_uses_text_fallbacks_but_not_reasoning(self):
        data = {
            "choices": [
                {
                    "message": {"content": "", "reasoning_content": "READ m9"},
                    "text": "READ NONE\nSTORE NONE\nSKIP u1",
                }
            ]
        }

        raw_output, source = extract_raw_output(data)

        self.assertEqual(raw_output, "READ NONE\nSTORE NONE\nSKIP u1")
        self.assertEqual(source, "choice.text")

    def test_sanitized_response_metadata_contains_shapes_not_content(self):
        data = {
            "id": "response_id",
            "choices": [
                {
                    "message": {"content": "", "reasoning_content": "private chain"},
                    "finish_reason": "length",
                }
            ],
            "usage": {"prompt_tokens": 1, "completion_tokens": 2},
        }

        metadata = sanitized_response_metadata(
            data,
            http_status=200,
            extraction_source="none",
        )

        self.assertEqual(metadata["http_status"], 200)
        self.assertEqual(metadata["choices_count"], 1)
        self.assertEqual(metadata["finish_reason"], "length")
        self.assertEqual(metadata["content_length"], 0)
        self.assertTrue(metadata["has_reasoning_content"])
        self.assertEqual(metadata["reasoning_content_length"], len("private chain"))
        self.assertIn("usage", metadata["top_level_keys"])
        self.assertIn("completion_tokens", metadata["usage_keys"])


if __name__ == "__main__":
    unittest.main()

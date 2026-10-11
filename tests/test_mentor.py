"""
Unit tests for iHOW mentor module
"""

import unittest
from unittest.mock import MagicMock, patch

import mentor


class TestMentor(unittest.TestCase):

    def test_is_advanced_context_keywords(self):
        # Case 1: Hard problem keywords
        msgs = [{"role": "user", "content": "Bài toán quy hoạch động knapsack"}]
        self.assertTrue(mentor.is_advanced_context("C++ Cơ bản", "Mới bắt đầu", msgs))

        # Case 2: Level advanced
        msgs_simple = [{"role": "user", "content": "Lệnh if else"}]
        self.assertTrue(mentor.is_advanced_context("C++ Cơ bản", "Đang tìm lỗi nâng cao", msgs_simple))

        # Case 3: Force high
        self.assertTrue(mentor.is_advanced_context("C++ Cơ bản", "Mới bắt đầu", msgs_simple, force_high=True))

        # Case 4: Normal problem
        self.assertFalse(mentor.is_advanced_context("C++ Cơ bản", "Mới bắt đầu", msgs_simple, force_high=False))

    def test_format_conversation_history(self):
        msgs = [
            {"role": "user", "content": "Tìm max 2 số"},
            {"role": "assistant", "content": "Đầu vào là gì bạn?"}
        ]
        history_str = mentor.format_conversation_history(msgs)
        self.assertIn("NGƯỜI HỌC:\nTìm max 2 số", history_str)
        self.assertIn("iHOW:\nĐầu vào là gì bạn?", history_str)

    def test_extract_response_text_direct(self):
        mock_resp = MagicMock()
        mock_resp.text = "Xin chào từ iHOW"
        self.assertEqual(mentor.extract_response_text(mock_resp), "Xin chào từ iHOW")

    def test_extract_response_text_fallback_parts(self):
        mock_resp = MagicMock()
        # text attribute raises error or returns None
        mock_resp.text = None
        part1 = MagicMock()
        part1.text = "Phần 1 "
        part2 = MagicMock()
        part2.text = "Phần 2"
        mock_resp.candidates = [MagicMock()]
        mock_resp.candidates[0].content.parts = [part1, part2]

        self.assertEqual(mentor.extract_response_text(mock_resp), "Phần 1 Phần 2")

    @patch("mentor.genai.Client")
    def test_execute_gemini_request_mocked(self, mock_client_cls):
        mock_client = MagicMock()
        mock_client_cls.return_value = mock_client

        mock_resp = MagicMock()
        mock_resp.text = "Phản hồi mẫu từ iHOW"
        mock_client.models.generate_content.return_value = mock_resp

        result = mentor.execute_gemini_request(
            api_key="mock_key",
            system_instruction="System prompt",
            prompt="User prompt",
            is_high_mode=False
        )
        self.assertEqual(result, "Phản hồi mẫu từ iHOW")


if __name__ == "__main__":
    unittest.main()


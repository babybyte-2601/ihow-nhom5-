"""
Unit tests for iHOW prompts module
"""

import unittest

import prompts


class TestPrompts(unittest.TestCase):

    def test_product_identity_in_prompts(self):
        prompt_a = prompts.build_system_prompt("mode_a", "UNDERSTAND")
        prompt_b = prompts.build_system_prompt("mode_b")
        prompt_c = prompts.build_system_prompt("mode_c")

        for p in [prompt_a, prompt_b, prompt_c]:
            self.assertIn("iHOW", p)
            # NEVER use 'AI HOW' or 'AI Mentor'
            self.assertNotIn("AI HOW", p)
            self.assertNotIn("AI Mentor", p)
            self.assertIn("Nguyên bản trước — Công nghệ sau", p)

    def test_mode_a_includes_stage_instruction(self):
        prompt = prompts.build_system_prompt("mode_a", "UNDERSTAND")
        self.assertIn("MODE A — HỌC ĐỂ HIỂU", prompt)
        self.assertIn("HIỂU ĐỀ", prompt)

        prompt_plan = prompts.build_system_prompt("mode_a", "PLAN")
        self.assertIn("LẬP KẾ HOẠCH", prompt_plan)

    def test_mode_b_focuses_on_debugging(self):
        prompt = prompts.build_system_prompt("mode_b")
        self.assertIn("MODE B — GỠ LỖI CÙNG TÔI", prompt)
        self.assertIn("vị trí nghi vấn", prompt)

    def test_mode_c_focuses_on_complete_solution(self):
        prompt = prompts.build_system_prompt("mode_c")
        self.assertIn("MODE C — TÔI CẦN CODE HOÀN CHỈNH", prompt)
        self.assertIn("Big-O", prompt)

    def test_hint_prompts_levels(self):
        hint_light = prompts.build_hint_prompt("HINT_LIGHT", "C++", "Tim max min", "")
        self.assertIn("GỢI Ý NHẸ", hint_light)

        hint_code = prompts.build_hint_prompt("HINT_FULL_SOLUTION", "C++", "Tim max min", "")
        self.assertIn("LỜI GIẢI HOÀN CHỈNH", hint_code)

    def test_transfer_challenge_prompt(self):
        p = prompts.build_transfer_challenge_prompt("C++ Vòng lặp", "Tính tổng 1 đến N")
        self.assertIn("Transfer Challenge", p)
        self.assertIn("Tính tổng 1 đến N", p)


if __name__ == "__main__":
    unittest.main()


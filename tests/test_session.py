"""
Unit tests for iHOW session state management
"""

import unittest

from session import ROADMAP_KEYS, SessionManager


class TestSession(unittest.TestCase):

    def setUp(self):
        self.state_storage = {}
        self.manager = SessionManager(self.state_storage)

    def test_initialization(self):
        self.assertFalse(self.manager.is_active)
        self.assertEqual(self.manager.mode, "mode_a")
        self.assertEqual(self.manager.current_stage, "UNDERSTAND")
        self.assertEqual(len(self.manager.messages), 0)

    def test_reset_session(self):
        self.manager.reset_session(
            problem="Tính tổng mảng",
            mode="mode_a",
            topic="C++ Mảng",
            level="Đã hiểu cơ bản"
        )
        self.assertTrue(self.manager.is_active)
        self.assertEqual(self.manager.mode, "mode_a")
        self.assertEqual(self.state_storage["user_problem"], "Tính tổng mảng")

    def test_roadmap_stage_transition(self):
        for stage in ROADMAP_KEYS:
            self.manager.set_stage(stage)
            self.assertEqual(self.manager.current_stage, stage)

        # Invalid stage should not overwrite
        self.manager.set_stage("INVALID_STAGE")
        self.assertEqual(self.manager.current_stage, "REFLECT")

    def test_messages_and_hints(self):
        self.manager.add_message("user", "Chào bạn")
        self.manager.add_message("assistant", "Tôi là iHOW")
        self.assertEqual(len(self.manager.messages), 2)

        self.manager.record_hint("HINT_LIGHT")
        self.manager.record_hint("HINT_FULL_SOLUTION")
        self.assertTrue(self.state_storage["full_solution_revealed"])
        self.assertEqual(len(self.state_storage["hints_used"]), 2)

    def test_skills_and_confidence(self):
        self.manager.record_skill("Xác định đúng Input/Output")
        self.manager.set_confidence(4, is_before=True)
        self.manager.set_confidence(5, is_before=False)

        summary = self.manager.get_summary()
        self.assertEqual(summary["confidence_before"], 4)
        self.assertEqual(summary["confidence_after"], 5)
        self.assertIn("Xác định đúng Input/Output", summary["demonstrated_skills"])


if __name__ == "__main__":
    unittest.main()


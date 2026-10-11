"""
iHOW - Session State & Progress Tracking
Quản lý trạng thái phiên học, tiến trình Roadmap, thang gợi ý và các kỹ năng được chứng minh thực tế.
"""

from typing import Any, Dict, List, Optional

try:
    import streamlit as st
except ImportError:
    st = None


ROADMAP_STAGES = [
    ("UNDERSTAND", "1. Hiểu đề", "Xác định Input, Output và ràng buộc bài toán"),
    ("PLAN", "2. Thuật toán", "Phác thảo ý tưởng giải quyết và mã giả"),
    ("CODE", "3. Cài đặt", "Hiện thực hóa thuật toán bằng ngôn ngữ lập trình"),
    ("TEST", "4. Kiểm thử", "Chạy thử với các bộ dữ liệu mẫu và trường hợp biên"),
    ("REFLECT", "5. Đúc kết", "Rút ra quy luật và liên hệ với các bài toán tương tự"),
]

ROADMAP_KEYS = [s[0] for s in ROADMAP_STAGES]


class SessionManager:
    """Quản lý trạng thái của phiên học trong st.session_state hoặc đối tượng độc lập."""

    def __init__(self, state_dict: Optional[Dict[str, Any]] = None):
        self._state = state_dict if state_dict is not None else (st.session_state if st is not None else {})
        self.ensure_initialized()

    def ensure_initialized(self) -> None:
        defaults = {
            "session_active": False,
            "mode": "mode_a",  # mode_a (Học để hiểu), mode_b (Gỡ lỗi), mode_c (Xem code)
            "topic": "C++ - Cấu trúc điều kiện",
            "level": "Mới bắt đầu",
            "use_high_model": False,
            "current_stage": "UNDERSTAND",
            "user_problem": "",
            "messages": [],
            "hints_used": [],
            "full_solution_revealed": False,
            "confidence_before": None,
            "confidence_after": None,
            "demonstrated_skills": [],
            "transfer_challenge": None,
        }
        for key, val in defaults.items():
            if key not in self._state:
                self._state[key] = val

    def reset_session(self, problem: str = "", mode: str = "mode_a", topic: str = "", level: str = "", use_high: bool = False) -> None:
        self._state["session_active"] = bool(problem.strip())
        self._state["user_problem"] = problem.strip()
        self._state["mode"] = mode
        if topic:
            self._state["topic"] = topic
        if level:
            self._state["level"] = level
        self._state["use_high_model"] = use_high
        self._state["current_stage"] = "UNDERSTAND" if mode == "mode_a" else "CODE"
        self._state["messages"] = []
        self._state["hints_used"] = []
        self._state["full_solution_revealed"] = (mode == "mode_c")
        self._state["confidence_before"] = None
        self._state["confidence_after"] = None
        self._state["demonstrated_skills"] = []
        self._state["transfer_challenge"] = None

    @property
    def is_active(self) -> bool:
        return bool(self._state.get("session_active", False))

    @property
    def mode(self) -> str:
        return self._state.get("mode", "mode_a")

    @mode.setter
    def mode(self, val: str) -> None:
        self._state["mode"] = val

    @property
    def current_stage(self) -> str:
        return self._state.get("current_stage", "UNDERSTAND")

    def set_stage(self, stage_name: str) -> None:
        if stage_name in ROADMAP_KEYS:
            self._state["current_stage"] = stage_name

    @property
    def messages(self) -> List[Dict[str, Any]]:
        return self._state.get("messages", [])

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        msg = {
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        self._state["messages"].append(msg)

    def record_hint(self, hint_level: str) -> None:
        hints = self._state.setdefault("hints_used", [])
        if hint_level not in hints:
            hints.append(hint_level)
        if hint_level == "HINT_FULL_SOLUTION":
            self._state["full_solution_revealed"] = True

    def record_skill(self, skill_name: str) -> None:
        skills = self._state.setdefault("demonstrated_skills", [])
        if skill_name and skill_name not in skills:
            skills.append(skill_name)

    def set_confidence(self, score: int, is_before: bool = True) -> None:
        key = "confidence_before" if is_before else "confidence_after"
        if 1 <= score <= 5:
            self._state[key] = score

    def get_summary(self) -> Dict[str, Any]:
        """Tạo bản tổng kết trung thực dựa trên các hành động thực tế đã diễn ra."""
        total_user_msgs = sum(1 for m in self.messages if m.get("role") == "user")
        return {
            "mode": self.mode,
            "topic": self._state.get("topic", "Tổng quan"),
            "level": self._state.get("level", "Mới bắt đầu"),
            "stage_reached": self.current_stage,
            "user_interactions_count": total_user_msgs,
            "hints_used_count": len(self._state.get("hints_used", [])),
            "hints_list": list(self._state.get("hints_used", [])),
            "full_solution_viewed": bool(self._state.get("full_solution_revealed", False)),
            "demonstrated_skills": list(self._state.get("demonstrated_skills", [])),
            "confidence_before": self._state.get("confidence_before"),
            "confidence_after": self._state.get("confidence_after"),
            "has_transfer_challenge": self._state.get("transfer_challenge") is not None
        }


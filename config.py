"""
iHOW - Configuration & Environment Management
Quản lý cấu hình, nạp API Key an toàn và thiết lập các mô hình Gemini hỗ trợ.
"""

import os
from typing import Dict, List, Optional, Tuple

try:
    import streamlit as st
except ImportError:
    st = None


# Danh sách các mô hình Gemini được kiểm định thực tế
DEFAULT_MODELS_NORMAL: List[str] = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-3.5-flash",
]

DEFAULT_MODELS_HIGH: List[str] = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
]

DEFAULT_MAX_TOKENS_NORMAL: int = 2500
DEFAULT_MAX_TOKENS_HIGH: int = 3500
DEFAULT_TEMPERATURE: float = 0.35


def get_gemini_api_key() -> str:
    """
    Lấy API key an toàn theo thứ tự ưu tiên:
    1. Streamlit secrets (st.secrets)
    2. Biến môi trường hệ thống (GEMINI_API_KEY)
    3. Đọc từ file cục bộ .streamlit/secrets.toml (phục vụ test/CLI nếu Streamlit chưa khởi tạo)
    Không bao giờ in giá trị key ra console hoặc log.
    """
    # 1. Thử từ st.secrets nếu đang chạy dưới Streamlit
    if st is not None:
        try:
            if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
                return str(st.secrets["GEMINI_API_KEY"]).strip()
        except Exception:
            pass

    # 2. Thử từ biến môi trường
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_key:
        return env_key

    # 3. Thử đọc file cục bộ .streamlit/secrets.toml nếu tồn tại
    try:
        secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
        if os.path.exists(secrets_path):
            with open(secrets_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY") and "=" in line:
                        _, val = line.split("=", 1)
                        val = val.strip().strip('"').strip("'")
                        if val:
                            return val
    except Exception:
        pass

    return ""


def get_custom_model_id() -> Optional[str]:
    """Lấy mô hình tùy biến được người dùng/admin chỉ định nếu có."""
    if st is not None:
        try:
            if "GEMINI_MODEL" in st.secrets and st.secrets["GEMINI_MODEL"]:
                return str(st.secrets["GEMINI_MODEL"]).strip()
        except Exception:
            pass

    env_model = os.environ.get("GEMINI_MODEL", "").strip()
    return env_model if env_model else None


def validate_api_configuration() -> Tuple[bool, str]:
    """
    Kiểm tra tính hợp lệ của cấu hình mà không làm lộ API key.
    Trả về (is_valid, message).
    """
    key = get_gemini_api_key()
    if not key:
        return False, (
            "Chưa cấu hình GEMINI_API_KEY.\n"
            "• Nếu chạy cục bộ: Thêm GEMINI_API_KEY = \"...\" vào file .streamlit/secrets.toml.\n"
            "• Nếu triển khai trên Streamlit Community Cloud: Vào Settings > Secrets của App và thêm GEMINI_API_KEY."
        )

    if len(key) < 15:
        return False, "GEMINI_API_KEY dường như không hợp lệ (độ dài quá ngắn)."

    return True, "Cấu hình API hợp lệ."


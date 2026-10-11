"""
iHOW - Core Gemini AI Orchestration Engine
Triết lý: "Nguyên bản trước — Công nghệ sau."
Đảm bảo gọi API tin cậy, tự động fallback model khi nghẽn/hết quota, và xử lý token đầy đủ không ngắt quãng.
"""

import time
from typing import Any, Dict, List, Optional

from google import genai
from google.genai import errors, types

from config import (
    DEFAULT_MAX_TOKENS_HIGH,
    DEFAULT_MAX_TOKENS_NORMAL,
    DEFAULT_MODELS_HIGH,
    DEFAULT_MODELS_NORMAL,
    DEFAULT_TEMPERATURE,
    get_custom_model_id,
)
from prompts import (
    build_hint_prompt,
    build_system_prompt,
    build_transfer_challenge_prompt,
)


def is_advanced_context(topic: str, level: str, messages: List[Dict[str, Any]], force_high: bool = False) -> bool:
    """Xác định xem truy vấn có cần ưu tiên mô hình tư duy sâu (Model High) hay không."""
    if force_high or level == "Đang tìm lỗi nâng cao":
        return True

    advanced_keywords = [
        "nâng cao", "khó", "thuật toán", "quy hoạch động", "đồ thị", "cây nhị phân",
        "con trỏ", "pointer", "oop", "class", "tối ưu", "độ phức tạp", "o(n", "o(log",
        "leetcode", "codeforces", "segment tree", "trie", "backtracking", "đệ quy",
        "recursion", "memory leak", "segmentation fault", "dijkstra", "bfs", "dfs",
        "stack", "queue", "linked list", "danh sách liên kết"
    ]

    last_text = (messages[-1]["content"] if messages else "").lower()
    topic_text = (topic or "").lower()

    return any(kw in last_text or kw in topic_text for kw in advanced_keywords)


def format_conversation_history(messages: List[Dict[str, Any]]) -> str:
    """Định dạng lịch sử trao đổi thành văn bản rõ ràng cho mô hình."""
    formatted = []
    for msg in messages:
        role = "NGƯỜI HỌC" if msg.get("role") == "user" else "iHOW"
        content = msg.get("content", "").strip()
        formatted.append(f"{role}:\n{content}")
    return "\n\n".join(formatted)


def extract_response_text(response: Any) -> Optional[str]:
    """Trích xuất nội dung văn bản an toàn từ phản hồi của Gemini."""
    if not response:
        return None

    # Thử lấy qua thuộc tính .text trực tiếp
    try:
        if response.text and response.text.strip():
            return response.text.strip()
    except Exception:
        pass

    # Nếu .text gặp lỗi hoặc trống, duyệt qua các phần tử parts của candidate
    try:
        if response.candidates and response.candidates[0].content:
            parts = []
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    parts.append(part.text)
            if parts:
                return "".join(parts).strip()
    except Exception:
        pass

    return None


def execute_gemini_request(
    api_key: str,
    system_instruction: str,
    prompt: str,
    is_high_mode: bool = False
) -> str:
    """
    Thực thi lệnh gọi Gemini với cơ chế fallback tự động, xử lý 503 và 429 mượt mà.
    Không bao giờ tạo phản hồi giả nếu API thất bại.
    """
    client = genai.Client(api_key=api_key)

    custom_model = get_custom_model_id()
    base_models = list(DEFAULT_MODELS_HIGH if is_high_mode else DEFAULT_MODELS_NORMAL)
    if custom_model and custom_model not in base_models:
        base_models.insert(0, custom_model)

    max_tokens = DEFAULT_MAX_TOKENS_HIGH if is_high_mode else DEFAULT_MAX_TOKENS_NORMAL
    thinking_level = "HIGH" if is_high_mode else None

    last_error: Optional[Exception] = None

    for model_name in base_models:
        for attempt in range(2):
            try:
                config_kwargs: Dict[str, Any] = {
                    "system_instruction": system_instruction,
                    "temperature": DEFAULT_TEMPERATURE,
                    "max_output_tokens": max_tokens,
                }
                if thinking_level:
                    config_kwargs["thinking_config"] = types.ThinkingConfig(
                        thinking_level=thinking_level
                    )

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(**config_kwargs)
                )

                extracted_text = extract_response_text(response)
                if extracted_text:
                    return extracted_text

                raise ValueError("Mô hình AI phản hồi rỗng (không chứa nội dung văn bản).")

            except errors.ServerError as err:
                last_error = err
                time.sleep(1.2 * (attempt + 1))
            except Exception as err:
                last_error = err
                # Nếu lỗi do cấu hình thinking_level, thử 1 lần không kèm thinking_level trên cùng model
                if thinking_level:
                    try:
                        fallback_resp = client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=DEFAULT_TEMPERATURE,
                                max_output_tokens=max_tokens
                            )
                        )
                        fallback_text = extract_response_text(fallback_resp)
                        if fallback_text:
                            return fallback_text
                    except Exception:
                        pass
                # Chuyển sang model tiếp theo trong danh sách
                break

    if last_error:
        err_msg = str(last_error)
        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            raise RuntimeError("API key hiện đã hết hạn mức (Quota Exceeded). Vui lòng thử lại sau hoặc đổi key.")
        if "503" in err_msg or "UNAVAILABLE" in err_msg:
            raise RuntimeError("Máy chủ Gemini đang chịu tải cao tạm thời. Vui lòng bấm thử lại sau vài giây.")
        raise RuntimeError(f"Lỗi kết nối Gemini ({type(last_error).__name__}): {last_error}")

    raise RuntimeError("Không thể kết nối tới mô hình AI.")


def generate_tutor_response(
    api_key: str,
    mode: str,
    current_stage: str,
    topic: str,
    level: str,
    messages: List[Dict[str, Any]],
    user_problem: str,
    force_high: bool = False
) -> str:
    """Sinh phản hồi đồng hành chính cho phiên học dựa trên mode và roadmap stage."""
    system_instruction = build_system_prompt(mode, current_stage)
    conversation_text = format_conversation_history(messages)

    prompt = f"""
Chủ đề học: {topic}
Trình độ: {level}
Chế độ học: {mode}
Giai đoạn Roadmap hiện tại: {current_stage}

BÀI TOÁN HOẶC ĐOẠN CODE BAN ĐẦU:
{user_problem}

LỊCH SỬ TRAO ĐỔI:
{conversation_text}

NHIỆM VỤ CỦA BẠN:
Phản hồi lượt mới nhất của người học theo đúng triết lý của iHOW và chế độ {mode}.
Tuân thủ nguyên tắc: Không lặp lại điều người học đã hiểu, kết thúc bằng một bước đi rõ ràng hoặc câu hỏi gợi mở có mục đích.
"""

    is_high = is_advanced_context(topic, level, messages, force_high)
    return execute_gemini_request(api_key, system_instruction, prompt, is_high_mode=is_high)


def generate_hint(
    api_key: str,
    hint_level: str,
    topic: str,
    user_problem: str,
    messages: List[Dict[str, Any]],
    force_high: bool = False
) -> str:
    """Sinh phản hồi theo từng nấc của Thang gợi ý (Hint Ladder)."""
    system_instruction = build_system_prompt("mode_a")
    conversation_text = format_conversation_history(messages)
    prompt = build_hint_prompt(hint_level, topic, user_problem, conversation_text)

    is_high = force_high or (hint_level in ["HINT_PSEUDOCODE", "HINT_SNIPPET", "HINT_FULL_SOLUTION"])
    return execute_gemini_request(api_key, system_instruction, prompt, is_high_mode=is_high)


def generate_transfer_challenge(
    api_key: str,
    topic: str,
    user_problem: str
) -> str:
    """Sinh bài toán chuyển giao tương tự để người học tự kiểm tra năng lực."""
    system_instruction = build_system_prompt("mode_a")
    prompt = build_transfer_challenge_prompt(topic, user_problem)
    return execute_gemini_request(api_key, system_instruction, prompt, is_high_mode=False)


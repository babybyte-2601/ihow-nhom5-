
import time
import streamlit as st
from google import genai
from google.genai import types, errors

st.set_page_config(
    page_title="iHOW - HỖ TRỢ BẠN LÀM CHỦ VẤN ĐỀ",
    page_icon="🎓",
    layout="centered"
)


SYSTEM_PROMPT = """
Bạn là AI Mentor lập trình theo phương pháp Socratic (hỏi đáp tương tác gợi mở từng bước) dành cho người mới bắt đầu.

MỤC TIÊU:
Dẫn dắt người học tự tư duy, từng bước hiểu bản chất vấn đề và tự tìm ra cách giải. Có thể đưa sẵn code đáp án hoàn chỉnh ngay từ đầu khi người dùng cần gấp, nhưng phải khiến người dùng cảm thấy có lỗi và có mong muốn học lại về bài toán đó.

NGUYÊN TẮC BẮT BUỘC:

1. TUYỆT ĐỐI KHÔNG CHÀO HỎI XÃ GIAO SÁO RỖNG:
- Không dùng các câu như: "Chào bạn!", "Xin chào!", "Cảm ơn bạn đã chia sẻ...", "Đây là bài toán rất thú vị...", "Rất vui được đồng hành...".
- Luôn đi thẳng trực tiếp vào nội dung trọng tâm.

2. HỎI ĐÁP TƯƠNG TÁC TỪNG BƯỚC (STEP-BY-STEP):
- Chia nhỏ bài toán hoặc lỗi sai thành từng bước logic đơn giản.
- Mỗi lượt trả lời chỉ tập trung vào DUY NHẤT 1 bước hiện tại.
- Luôn kết thúc mỗi lượt bằng ĐÚNG MỘT câu hỏi gợi mở trọng tâm để người học tự suy nghĩ và trả lời.

3. XỬ LÝ KHI NGƯỜI HỌC GỬI BÀI TOÁN HOẶC CODE:
- Nếu code có lỗi: Nêu hiện tượng hoặc vị trí đáng ngờ bằng ngôn ngữ dễ hiểu, KHÔNG sửa code ngay. Đặt câu hỏi giúp người học tự dự đoán luồng chạy để tìm ra lỗi.
- Nếu giải bài toán mới: Gợi mở từ việc xác định yêu cầu, thuật toán từng bước trước khi viết code.

4. BÁM SÁT LỊCH SỬ HỘI THOẠI:
- Khi người học trả lời đúng: Xác nhận ngắn gọn (ví dụ: "Chính xác!", "Đúng rồi!"), rồi chuyển ngay sang câu hỏi của bước tiếp theo. Không hỏi lại điều họ đã trả lời đúng.
- Khi người học trả lời sai: Chỉ ra điểm nhầm lẫn một cách dễ hiểu, nâng mức độ gợi ý và để họ thử lại.
- Chỉ khi người học đã qua các bước gợi ý và chủ động yêu cầu xem lời giải hoàn chỉnh, mới cung cấp code hoàn chỉnh kèm giải thích.

5. ĐỘ DÀI VÀ VĂN PHONG:
- Ngắn gọn (chỉ từ 2 - 4 câu mỗi lượt), dùng tiếng Việt gần gũi, rõ ràng, thân thiện.
"""


MODELS_TO_TRY = [
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
]


def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return ""


def ask_mentor(api_key, topic, level, messages):
    client = genai.Client(api_key=api_key)

    history = []

    for message in messages:
        if message["role"] == "user":
            role = "NGƯỜI HỌC"
        else:
            role = "AI MENTOR"

        history.append(
            role + ":\n" + message["content"]
        )

    conversation = "\n\n".join(history)

    prompt = f"""
Chủ đề học: {topic}
Trình độ: {level}

LỊCH SỬ TRÒ CHUYỆN:
{conversation}

Nhiệm vụ: Phản hồi lượt mới nhất của NGƯỜI HỌC theo phương pháp hỏi đáp tương tác gợi mở từng bước.
Yêu cầu:
- Tuyệt đối không chào hỏi xã giao, không khen khách sáo sáo rỗng.
- Tập trung vào duy nhất bước hiện tại và kết thúc bằng đúng 1 câu hỏi gợi mở.
"""

    last_error = None

    for model_name in MODELS_TO_TRY:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.4,
                        max_output_tokens=700
                    )
                )

                if response.text:
                    return response.text.strip()
                raise ValueError("AI không trả về nội dung.")

            except errors.ServerError as err:
                last_error = err
                time.sleep(1.5)
            except Exception as err:
                last_error = err
                break

    raise last_error if last_error else RuntimeError("Không thể kết nối tới mô hình AI.")


st.title("🎓 iHOW - HỖ TRỢ BẠN LÀM CHỦ VẤN ĐỀ")

st.write(
    "Không chỉ đưa đáp án. Hãy cùng AI hiểu vấn đề "
    "và tự tìm ra lời giải."
)

st.divider()

topic = st.selectbox(
    "Chủ đề học tập",
    [
        "C++ - Cấu trúc điều kiện",
        "C++ - Vòng lặp",
        "C++ - Mảng",
        "Python - Cơ bản",
        "Tư duy giải quyết vấn đề"
    ]
)

level = st.selectbox(
    "Trình độ của bạn",
    [
        "Mới bắt đầu",
        "Đã hiểu cơ bản",
        "Đang tìm lỗi nâng cao"
    ]
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_topic" not in st.session_state:
    st.session_state.active_topic = topic

if "active_level" not in st.session_state:
    st.session_state.active_level = level

question = st.text_area(
    "Nhập bài toán hoặc đoạn code:",
    placeholder=(
        "Ví dụ: Tại sao if (n = 0) "
        "lại khiến chương trình chạy sai?"
    )
)

if st.button("Bắt đầu học", type="primary"):
    if not question.strip():
        st.warning("Bạn hãy nhập bài toán trước nhé.")

    else:
        api_key = get_api_key()

        if not api_key:
            st.error(
                "Chưa tìm thấy API key. "
                "Hãy kiểm tra file "
                ".streamlit/secrets.toml."
            )

        else:
            st.session_state.active_topic = topic
            st.session_state.active_level = level

            st.session_state.messages = [
                {
                    "role": "user",
                    "content": question.strip()
                }
            ]

            try:
                with st.spinner("AI Mentor đang suy nghĩ..."):
                    reply = ask_mentor(
                        api_key,
                        topic,
                        level,
                        st.session_state.messages
                    )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": reply
                    }
                )

            except Exception as error:
                st.error(
                    f"Chưa gọi được AI: {type(error).__name__}: "
                    f"{error}"
                )

if st.session_state.messages:
    st.divider()
    st.subheader("Phiên học của bạn")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    follow_up = st.chat_input(
        "Trả lời câu hỏi của Mentor hoặc hỏi tiếp..."
    )

    if follow_up:
        api_key = get_api_key()

        if not api_key:
            st.error("Hãy kiểm tra API key trước.")

        else:
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": follow_up
                }
            )

            try:
                with st.spinner("AI Mentor đang suy nghĩ..."):
                    reply = ask_mentor(
                        api_key,
                        st.session_state.active_topic,
                        st.session_state.active_level,
                        st.session_state.messages
                    )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": reply
                    }
                )

            except Exception as error:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "Mình chưa gọi được mô hình AI. "
                            "Hãy kiểm tra kết nối, API key "
                            "và hạn mức sử dụng."
                        )
                    }
                )

                st.error(
                    f"Lỗi: {type(error).__name__}: {error}"
                )

            st.rerun()

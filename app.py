"""
iHOW - Nguyên bản trước — Công nghệ sau.
Nền tảng hỗ trợ học lập trình và tư duy giải quyết vấn đề.
"""

import streamlit as st

import config
import mentor
import prompts
from session import ROADMAP_STAGES, SessionManager

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="iHOW — Nguyên bản trước, Công nghệ sau",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo Session State
session_mgr = SessionManager()

# --- SIDEBAR: Cấu hình và Thông tin phiên học ---
with st.sidebar:
    st.markdown("## 💡 **iHOW**")
    st.caption("**Nguyên bản trước — Công nghệ sau.**")
    st.write(
        "AI có thể sinh ra đáp án ngay lập tức. "
        "iHOW giúp bạn hiểu rõ con đường dẫn tới đáp án để tự tin giải các bài tiếp theo."
    )
    st.divider()

    st.subheader("⚙️ Thiết lập bài học")

    topic = st.selectbox(
        "Chủ đề học tập",
        [
            "C++ - Cấu trúc điều kiện (if / else / switch)",
            "C++ - Vòng lặp (for / while / do-while)",
            "C++ - Mảng & Chuỗi ký tự",
            "C++ - Hàm & Kỹ thuật đệ quy",
            "C++ - Con trỏ & Cấp phát động",
            "Python - Biến, Kiểu dữ liệu & Điều kiện",
            "Python - Danh sách, Tuple & Dictionary",
            "Python - Vòng lặp & Hàm",
            "Cấu trúc dữ liệu & Thuật toán cơ bản",
            "Tư duy giải quyết vấn đề"
        ],
        index=0
    )

    level = st.selectbox(
        "Trình độ hiện tại",
        [
            "Mới bắt đầu",
            "Đã hiểu cơ bản",
            "Đang tìm lỗi nâng cao"
        ],
        index=0
    )

    use_high = st.checkbox(
        "🧠 Ưu tiên Model High (Tư duy sâu)",
        value=(level == "Đang tìm lỗi nâng cao"),
        help="Tự động ưu tiên Gemini 3.8 Flash ở chế độ Thinking High cho các bài toán giải thuật phức tạp."
    )

    st.divider()
    st.subheader("📊 Tự đánh giá mức độ tự tin (Tùy chọn)")
    conf_col1, conf_col2 = st.columns(2)
    with conf_col1:
        st.caption("Trước khi giải:")
        conf_before = st.select_slider(
            "Trước",
            options=[1, 2, 3, 4, 5],
            value=session_mgr.get_summary()["confidence_before"] or 3,
            label_visibility="collapsed",
            key="slider_conf_before"
        )
        session_mgr.set_confidence(conf_before, is_before=True)

    with conf_col2:
        st.caption("Sau khi học:")
        conf_after = st.select_slider(
            "Sau",
            options=[1, 2, 3, 4, 5],
            value=session_mgr.get_summary()["confidence_after"] or 3,
            label_visibility="collapsed",
            key="slider_conf_after"
        )
        session_mgr.set_confidence(conf_after, is_before=False)

    st.divider()
    if st.button("🔄 Bắt đầu phiên học mới", use_container_width=True):
        session_mgr.reset_session()
        st.rerun()

    # Kiểm tra API Key an toàn
    api_valid, api_msg = config.validate_api_configuration()
    if not api_valid:
        st.warning("⚠️ Chưa tìm thấy API Key cấu hình.")
        with st.expander("Hướng dẫn thiết lập API Key"):
            st.markdown(
                "1. **Chạy cục bộ:** Mở file `.streamlit/secrets.toml` và điền:\n"
                "```toml\nGEMINI_API_KEY = \"AIzaSy...\"\n```\n"
                "2. **Streamlit Community Cloud:** Vào mục **App Settings > Secrets** và thêm `GEMINI_API_KEY`."
            )


# --- MAIN INTERFACE: HEADER & PRODUCT IDENTITY ---
st.title("💡 iHOW")
st.subheader("Nguyên bản trước — Công nghệ sau.")
st.markdown(
    "**Đừng chỉ hiểu lời giải. Hãy tự giải được bài tiếp theo.**  \n"
    "*iHOW giúp bạn hiểu đề, tháo gỡ lỗi lập trình và xây dựng khả năng tự tư duy. "
    "Bạn có thể học từng bước, cùng gỡ lỗi hoặc xem lời giải đầy đủ khi thực sự cần.*"
)

st.divider()

# --- LỰA CHỌN CHẾ ĐỘ HỌC TẬP (3 MODES) ---
st.markdown("### 1. Chọn nhu cầu học tập của bạn")
mode_cols = st.columns(3)

with mode_cols[0]:
    is_mode_a = (session_mgr.mode == "mode_a")
    if st.button(
        "🌱 Mode A: Học để hiểu\n(Dẫn dắt từng bước)",
        type="primary" if is_mode_a else "secondary",
        use_container_width=True,
        key="btn_mode_a"
    ):
        session_mgr.mode = "mode_a"
        st.rerun()
    st.caption("Gợi mở tư duy Socratic: Hiểu đề ➔ Lập kế hoạch ➔ Viết code ➔ Kiểm thử ➔ Đúc kết.")

with mode_cols[1]:
    is_mode_b = (session_mgr.mode == "mode_b")
    if st.button(
        "🛠️ Mode B: Gỡ lỗi cùng tôi\n(Tìm nguyên nhân & sửa lỗi)",
        type="primary" if is_mode_b else "secondary",
        use_container_width=True,
        key="btn_mode_b"
    ):
        session_mgr.mode = "mode_b"
        st.rerun()
    st.caption("Chỉ ra vị trí nghi vấn, phân tích nguyên nhân gốc rễ và hướng dẫn sửa chữa.")

with mode_cols[2]:
    is_mode_c = (session_mgr.mode == "mode_c")
    if st.button(
        "⚡ Mode C: Tôi cần code hoàn chỉnh\n(Xem giải pháp & đối chiếu)",
        type="primary" if is_mode_c else "secondary",
        use_container_width=True,
        key="btn_mode_c"
    ):
        session_mgr.mode = "mode_c"
        st.rerun()
    st.caption("Nhận code hoàn chỉnh có chú thích ngay lập tức, kèm test case và phân tích Big-O.")

st.markdown("---")


# --- ROADMAP TIẾN TRÌNH (CHO MODE A) ---
if session_mgr.mode == "mode_a":
    st.markdown("### 2. Lộ trình tư duy bài toán")
    roadmap_cols = st.columns(len(ROADMAP_STAGES))
    for idx, (stage_key, stage_title, stage_desc) in enumerate(ROADMAP_STAGES):
        is_current = (session_mgr.current_stage == stage_key)
        with roadmap_cols[idx]:
            if st.button(
                f"{'📍 ' if is_current else ''}{stage_title}",
                key=f"stage_btn_{stage_key}",
                type="primary" if is_current else "secondary",
                use_container_width=True,
                help=stage_desc
            ):
                session_mgr.set_stage(stage_key)
                st.rerun()
    st.caption(f"👉 Bước hiện tại: **{next(s[1] for s in ROADMAP_STAGES if s[0] == session_mgr.current_stage)}** — *{next(s[2] for s in ROADMAP_STAGES if s[0] == session_mgr.current_stage)}*")
    st.markdown("---")


# --- INPUT BÀI TOÁN HOẶC CODE ---
if not session_mgr.is_active:
    st.markdown("### Nhập bài toán hoặc đoạn code bạn đang làm việc")
    input_placeholder = (
        "Ví dụ: Viết chương trình tìm số lớn nhất và nhỏ nhất giữa hai số nhập từ bàn phím.\n"
        "Hoặc dán đoạn code bạn đang gặp lỗi tại đây..."
    )
    problem_input = st.text_area(
        "Nội dung bài toán / code cần trao đổi:",
        placeholder=input_placeholder,
        height=140
    )

    col_btn_start, col_hint_text = st.columns([1, 3])
    with col_btn_start:
        start_pressed = st.button("🚀 Bắt đầu buổi học", type="primary", use_container_width=True)

    if start_pressed:
        if not problem_input.strip():
            st.warning("Vui lòng nhập bài toán hoặc đoạn code để bắt đầu nhé.")
        else:
            api_key = config.get_gemini_api_key()
            if not api_key:
                st.error("Chưa tìm thấy GEMINI_API_KEY. Vui lòng kiểm tra lại cấu hình theo hướng dẫn ở thanh bên.")
            else:
                session_mgr.reset_session(
                    problem=problem_input.strip(),
                    mode=session_mgr.mode,
                    topic=topic,
                    level=level,
                    use_high=use_high
                )
                session_mgr.add_message("user", problem_input.strip())

                is_high_mode = mentor.is_advanced_context(topic, level, session_mgr.messages, use_high)
                spinner_msg = "iHOW đang suy nghĩ chuyên sâu (Model High)..." if is_high_mode else "iHOW đang phân tích bài toán..."

                try:
                    with st.spinner(spinner_msg):
                        ai_reply = mentor.generate_tutor_response(
                            api_key=api_key,
                            mode=session_mgr.mode,
                            current_stage=session_mgr.current_stage,
                            topic=topic,
                            level=level,
                            messages=session_mgr.messages,
                            user_problem=problem_input.strip(),
                            force_high=use_high
                        )
                    session_mgr.add_message("assistant", ai_reply)
                    session_mgr.record_skill("Bắt đầu phân tích bài toán")
                    st.rerun()

                except Exception as err:
                    st.error(f"⚠️ {err}")


# --- GIAO DIỆN PHIÊN HỌC ĐANG DIỄN RA ---
if session_mgr.is_active:
    st.markdown("### 💬 Không gian thảo luận cùng iHOW")

    # Hiển thị bài toán ban đầu trong expander gọn gàng
    with st.expander("📌 Đề bài / Code ban đầu của bạn", expanded=False):
        st.write(session_mgr._state.get("user_problem", ""))

    # Hiển thị lịch sử hội thoại
    for msg in session_mgr.messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(content)
        else:
            with st.chat_message("assistant", avatar="💡"):
                st.markdown(content)

    # --- THANG GỢI Ý CHỦ ĐỘNG (HINT LADDER) ---
    st.markdown("#### 🪜 Thang gợi ý chủ động")
    st.caption("Bạn hoàn toàn chủ động: có thể nhận gợi ý nhẹ, xem mã giả hoặc mở ngay code hoàn chỉnh bất cứ lúc nào.")

    hint_cols = st.columns(5)
    with hint_cols[0]:
        btn_hint_light = st.button("💡 Gợi ý nhẹ", use_container_width=True, help="Khơi gợi khái niệm, hướng suy nghĩ ban đầu")
    with hint_cols[1]:
        btn_hint_specific = st.button("🔍 Gợi ý cụ thể", use_container_width=True, help="Chỉ rõ công thức hoặc điều kiện cụ thể")
    with hint_cols[2]:
        btn_hint_pseudo = st.button("📝 Xem mã giả", use_container_width=True, help="Dàn ý thuật toán từng bước bằng tiếng Việt")
    with hint_cols[3]:
        btn_hint_snippet = st.button("💻 Xem code mẫu", use_container_width=True, help="Đoạn code ngắn xử lý phần cốt lõi")
    with hint_cols[4]:
        btn_hint_full = st.button("🚀 Lời giải hoàn chỉnh", use_container_width=True, help="Toàn bộ code chạy được ngay kèm giải thích")

    selected_hint = None
    if btn_hint_light:
        selected_hint = ("HINT_LIGHT", "💡 Gợi ý nhẹ")
    elif btn_hint_specific:
        selected_hint = ("HINT_SPECIFIC", "🔍 Gợi ý cụ thể")
    elif btn_hint_pseudo:
        selected_hint = ("HINT_PSEUDOCODE", "📝 Xem mã giả")
    elif btn_hint_snippet:
        selected_hint = ("HINT_SNIPPET", "💻 Xem code mẫu")
    elif btn_hint_full:
        selected_hint = ("HINT_FULL_SOLUTION", "🚀 Lời giải hoàn chỉnh")

    if selected_hint:
        hint_code, hint_label = selected_hint
        api_key = config.get_gemini_api_key()
        if not api_key:
            st.error("Chưa tìm thấy GEMINI_API_KEY.")
        else:
            session_mgr.record_hint(hint_code)
            session_mgr.add_message("user", f"[Yêu cầu trợ giúp]: {hint_label}")
            try:
                with st.spinner(f"iHOW đang chuẩn bị {hint_label}..."):
                    hint_reply = mentor.generate_hint(
                        api_key=api_key,
                        hint_level=hint_code,
                        topic=topic,
                        user_problem=session_mgr._state.get("user_problem", ""),
                        messages=session_mgr.messages,
                        force_high=use_high
                    )
                session_mgr.add_message("assistant", hint_reply)
                session_mgr.record_skill(f"Sử dụng công cụ trợ giúp: {hint_label}")
                st.rerun()
            except Exception as err:
                st.error(f"⚠️ {err}")

    st.markdown("---")

    # --- KHUNG NHẬP PHẢN HỒI (CHAT INPUT) ---
    user_reply = st.chat_input("Nhập câu trả lời, dự đoán hoặc đặt câu hỏi tiếp theo...")
    if user_reply:
        api_key = config.get_gemini_api_key()
        if not api_key:
            st.error("Chưa tìm thấy GEMINI_API_KEY.")
        else:
            session_mgr.add_message("user", user_reply.strip())

            is_high_mode = mentor.is_advanced_context(topic, level, session_mgr.messages, use_high)
            spinner_msg = "iHOW đang suy nghĩ chuyên sâu (Model High)..." if is_high_mode else "iHOW đang phản hồi..."

            try:
                with st.spinner(spinner_msg):
                    ai_reply = mentor.generate_tutor_response(
                        api_key=api_key,
                        mode=session_mgr.mode,
                        current_stage=session_mgr.current_stage,
                        topic=topic,
                        level=level,
                        messages=session_mgr.messages,
                        user_problem=session_mgr._state.get("user_problem", ""),
                        force_high=use_high
                    )
                session_mgr.add_message("assistant", ai_reply)
                session_mgr.record_skill("Tham gia tương tác phân tích bài toán")
                st.rerun()

            except Exception as err:
                session_mgr.add_message(
                    "assistant",
                    f"⚠️ iHOW tạm thời chưa kết nối được mô hình AI: {err}\n\n"
                    "Vui lòng thử gửi lại tin nhắn sau vài giây."
                )
                st.rerun()

    # --- TIỆN ÍCH MỞ RỘNG: BÀI TOÁN TƯƠNG TỰ & TỔNG KẾT PHIÊN HỌC ---
    st.markdown("#### 🎯 Bước tiếp theo để làm chủ kiến thức")
    ext_col1, ext_col2 = st.columns(2)

    with ext_col1:
        if st.button("🔄 Thử sức với bài toán tương tự (Transfer Challenge)", use_container_width=True):
            api_key = config.get_gemini_api_key()
            if not api_key:
                st.error("Chưa tìm thấy GEMINI_API_KEY.")
            else:
                try:
                    with st.spinner("iHOW đang tạo bài toán chuyển giao tương tự..."):
                        challenge = mentor.generate_transfer_challenge(
                            api_key=api_key,
                            topic=topic,
                            user_problem=session_mgr._state.get("user_problem", "")
                        )
                    session_mgr.add_message("assistant", f"### 🎯 Bài toán tương tự để thử sức:\n\n{challenge}")
                    session_mgr.record_skill("Thử sức với bài toán tương tự (Transfer Learning)")
                    st.rerun()
                except Exception as err:
                    st.error(f"⚠️ {err}")

    with ext_col2:
        with st.popover("📊 Xem tổng kết phiên học", use_container_width=True):
            summary = session_mgr.get_summary()
            st.markdown("### 📊 Tổng kết phiên học thực tế")
            st.caption("Dữ liệu được ghi nhận trung thực dựa trên tương tác thực tế của bạn.")

            st.write(f"- **Chế độ:** {summary['mode']}")
            st.write(f"- **Chủ đề:** {summary['topic']}")
            st.write(f"- **Giai đoạn đạt được:** {summary['stage_reached']}")
            st.write(f"- **Số lượt trao đổi:** {summary['user_interactions_count']} lượt")
            st.write(f"- **Gợi ý đã sử dụng:** {summary['hints_used_count']} lần")
            st.write(f"- **Đã xem lời giải hoàn chỉnh:** {'Có' if summary['full_solution_viewed'] else 'Chưa'}")

            st.markdown("##### 🏆 Kỹ năng đã thể hiện:")
            if summary["demonstrated_skills"]:
                for sk in summary["demonstrated_skills"]:
                    st.markdown(f"- ✅ {sk}")
            else:
                st.write("- Đang trong quá trình tương tác bước đầu.")

            if summary["confidence_before"] and summary["confidence_after"]:
                st.markdown(f"- **Mức độ tự tin tự đánh giá:** Từ **{summary['confidence_before']}/5** ➔ **{summary['confidence_after']}/5**")

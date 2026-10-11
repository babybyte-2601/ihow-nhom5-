# iHOW — Nguyên bản trước — Công nghệ sau.

> **"Đừng chỉ hiểu lời giải. Hãy tự giải được bài tiếp theo."**  
> iHOW là nền tảng học lập trình và rèn luyện tư duy giải quyết vấn đề, tập trung vào việc biến câu trả lời tức thời của AI thành năng lực tư duy độc lập của người học.

---

## 1. Định danh sản phẩm & Triết lý cốt lõi

- **Tên sản phẩm:** `iHOW`
- **Khẩu hiệu (Tagline):** *Nguyên bản trước — Công nghệ sau.*
- **Triết lý:**
  Các công cụ AI tạo sinh (như Gemini, GPT) có khả năng sinh ra code đáp án chỉ trong vài giây. Tuy nhiên, việc nhận ngay một đáp án hoàn chỉnh thường tạo ra khoảng cách lớn giữa **nhận thức** (biết rằng tự giải bài là tốt) và **hành vi thực tế** (sao chép code do áp lực deadline, thiếu tự tin hoặc nản lòng khi gặp lỗi).
  iHOW được thiết kế để lấp đầy khoảng cách đó: tạo ra một môi trường học tập giúp việc bắt đầu suy nghĩ trở nên dễ dàng, duy trì tư duy có ý nghĩa, và việc nhận đáp án hoàn toàn là quyền tự chủ của người học mà không đi kèm cảm giác tội lỗi hay phán xét.

---

## 2. Đối tượng mục tiêu & Vấn đề giải quyết

### Đối tượng phục vụ chính
- Sinh viên năm nhất, năm hai đại học và người mới bắt đầu học lập trình C++ hoặc Python.
- Người học có thể đọc hiểu code có sẵn nhưng lúng túng khi bắt đầu từ một đề bài mới.
- Người học thường nhờ AI sửa lỗi hoặc giải bài tập, nhưng đôi khi sao chép mà chưa nắm vững thuật toán bên dưới.
- Người học mong muốn rèn luyện sự tự tin và tư duy thuật toán độc lập mà vẫn có sự trợ giúp nhanh chóng khi cần.

### Vị thế sản phẩm (Product Positioning)
- iHOW **không** phải là một mô hình nền tảng mới và không tuyên bố thông minh hơn Gemini hay GPT.
- iHOW sử dụng mô hình ngôn ngữ lớn qua Google Gen AI API và xây dựng một **kiến trúc trải nghiệm học tập có chủ đích (Intentional Learning Experience)** xoay quanh mô hình đó.

---

## 3. Trải nghiệm học tập cốt lõi (Core Learning Experience)

### 3.1. Ba chế độ đáp ứng đúng nhu cầu thực tế
1. **Mode A — Học để hiểu (Guided Reasoning):**
   - Hướng dẫn theo phương pháp gợi mở Socratic.
   - Chia nhỏ bài toán theo lộ trình 5 bước: `Hiểu đề` ➔ `Thuật toán` ➔ `Cài đặt` ➔ `Kiểm thử` ➔ `Đúc kết`.
   - Mỗi lượt chỉ tập trung vào duy nhất một bước logic hiện tại kèm câu hỏi gợi mở có mục đích rõ ràng.
2. **Mode B — Gỡ lỗi cùng tôi (Collaborative Debugging):**
   - Tiếp nhận đoạn code bị lỗi hoặc thông báo lỗi của trình biên dịch.
   - Phân tích nguyên nhân gốc rễ, chỉ rõ vị trí nghi vấn và định hướng cách sửa chữa bằng tư duy logic.
3. **Mode C — Tôi cần code hoàn chỉnh (Direct Solution & Inspection):**
   - Cung cấp ngay code hoàn chỉnh, chuẩn mực, có chú thích các dòng cốt lõi.
   - Phân tích độ phức tạp thuật toán (Big-O) và đưa ra các test case minh họa.
   - Hoàn toàn tôn trọng quyền tự chủ của người học, không phán xét hay gây áp lực tâm lý.

### 3.2. Thang gợi ý chủ động (Hint Ladder)
Người học không bị ép buộc phải trả lời câu hỏi nếu đang bế tắc. Có thể chủ động chọn nấc hỗ trợ phù hợp:
- 💡 **Gợi ý nhẹ:** Khơi gợi khái niệm, góc nhìn tiếp cận.
- 🔍 **Gợi ý cụ thể:** Chỉ ra công thức toán học hoặc điều kiện rẽ nhánh/dừng lặp.
- 📝 **Xem mã giả:** Dàn ý thuật toán từng bước bằng tiếng Việt.
- 💻 **Xem code mẫu:** Đoạn code snippet phần xử lý then chốt.
- 🚀 **Lời giải hoàn chỉnh:** Toàn bộ code chạy được ngay kèm giải thích.

### 3.3. Bài toán chuyển giao (Transfer Challenge)
Sau khi giải xong một bài toán, người học có thể bấm **"Thử sức với bài toán tương tự"** để kiểm tra xem mình đã thực sự làm chủ bản chất quy luật hay chưa.

### 3.4. Tổng kết phiên học trung thực
Hệ thống hiển thị báo cáo dựa trên tương tác thực tế (số lượt trao đổi, số lần dùng gợi ý, các kỹ năng đã chứng minh trong phiên học) và mức độ tự tin tự đánh giá (thang điểm 1–5), không vẽ ra các chỉ số năng lực giả tạo.

---

## 4. Cài đặt và Chạy ứng dụng cục bộ (Windows)

### 4.1. Yêu cầu hệ thống
- Hệ điều hành: Windows 10 / 11 (hoặc macOS / Linux).
- Python 3.10 trở lên (khuyên dùng Python 3.11 hoặc 3.12 / 3.13).
- Kết nối Internet và Google Gemini API Key.

### 4.2. Cài đặt các thư viện phụ thuộc
Mở PowerShell hoặc Command Prompt tại thư mục dự án và chạy:

```powershell
py -m pip install -r requirements.txt
```

### 4.3. Cấu hình Gemini API Key
Tạo file cấu hình bí mật tại đường dẫn `.streamlit/secrets.toml`:

```powershell
# Copy từ file mẫu
Copy-Item .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Mở file `.streamlit/secrets.toml` và điền khóa API của bạn:

```toml
GEMINI_API_KEY = "AIzaSyYourActualGeminiApiKeyHere..."
```

*(Lưu ý: File `.streamlit/secrets.toml` đã được bảo vệ trong `.gitignore`, tuyệt đối không commit lên Git).*

### 4.4. Khởi chạy ứng dụng
Chạy lệnh sau trên terminal:

```powershell
py -m streamlit run app.py
```

Ứng dụng sẽ tự động mở trên trình duyệt tại địa chỉ `http://localhost:8501`.

---

## 5. Triển khai lên Streamlit Community Cloud

1. Đẩy mã nguồn lên kho chứa GitHub cá nhân hoặc tổ chức (đảm bảo file `.streamlit/secrets.toml` không bị đẩy lên).
2. Truy cập [Streamlit Community Cloud](https://share.streamlit.io/) và đăng nhập bằng tài khoản GitHub.
3. Chọn **New app**, trỏ tới Repository, chọn Branch `main` và Main file path là `app.py`.
4. Mở mục **Advanced settings** > **Secrets**, dán cấu hình API Key:
   ```toml
   GEMINI_API_KEY = "AIzaSyYourActualGeminiApiKeyHere..."
   ```
5. Bấm **Deploy**. Ứng dụng sẽ tự động cài đặt các gói trong `requirements.txt` và khởi chạy trên đám mây.

---

## 6. Kiến trúc mã nguồn

```
iHOW/
├── app.py                      # Giao diện người dùng Streamlit và điều phối phiên học
├── config.py                   # Quản lý cấu hình, nạp API Key an toàn và thiết lập model
├── mentor.py                   # Động cơ AI: gọi API Gemini, cơ chế fallback và xử lý token
├── prompts.py                  # Hệ thống mẫu prompt Socratic, 3 chế độ và thang gợi ý
├── session.py                  # Quản lý trạng thái phiên học, Roadmap và kỹ năng thực tế
├── requirements.txt            # Danh sách thư viện phụ thuộc
├── .gitignore                  # Bảo vệ file cấu hình bí mật và file rác
├── .streamlit/
│   ├── config.toml             # Tùy biến giao diện và theme hiển thị
│   ├── secrets.toml.example    # Mẫu cấu hình an toàn cho người dùng mới
│   └── secrets.toml            # [Riêng tư] File chứa API key cục bộ (không commit)
└── tests/                      # Bộ kiểm thử tự động (Unit Tests)
    ├── test_config.py          # Kiểm thử nạp cấu hình và bảo mật khóa
    ├── test_prompts.py         # Kiểm thử văn phong, định danh iHOW và các mode
    ├── test_session.py         # Kiểm thử chuyển trạng thái Roadmap và ghi nhận kỹ năng
    └── test_mentor.py          # Kiểm thử phân loại bài toán khó và cơ chế trích xuất text
```

---

## 7. Chạy bộ kiểm thử tự động (Automated Testing)

iHOW đi kèm bộ kiểm thử tự động sử dụng `unittest` tích hợp sẵn trong Python. Để chạy toàn bộ kiểm thử:

```powershell
py -m unittest discover -s tests -v
```

Tất cả các bài test sử dụng Mocking đối với cuộc gọi API để đảm bảo kiểm thử logic nghiệp vụ mà không làm tiêu tốn hạn ngạch API của bạn.

---

## 8. Cân nhắc Bảo mật và Hạn ngạch API (Security & Quota)

1. **Bảo mật API Key:** 
   - Mã nguồn không chứa bất kỳ khóa API cứng (hardcoded key) nào.
   - File cấu hình chứa key được loại trừ hoàn toàn khỏi Git.
2. **Quản lý hạn mức (API Quota):**
   - Với tài khoản Google AI Studio miễn phí (Free Tier), một số mô hình có thể gặp giới hạn số lượt gọi/ngày hoặc nghẽn tải cao (HTTP 503).
   - iHOW đã cài đặt cơ chế tự động chuyển tiếp (Fallback) sang các mô hình nhanh và ổn định (`gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`) khi mô hình cao cấp gặp sự cố, đảm bảo phiên học của bạn không bị gián đoạn.
3. **Môi trường thực thi mã nguồn:**
   - Để đảm bảo an toàn tuyệt đối cho máy chủ triển khai công cộng, iHOW **không** tự ý biên dịch hoặc chạy code C++/Python tùy ý của người dùng trực tiếp trên server Streamlit. Tất cả các phân tích đều dựa trên mô hình suy luận tĩnh và giả lập tư duy.

---

## 9. Phân định tính năng: Đã hoàn thiện vs Định hướng tương lai

### Đã hoàn thiện (Implemented)
- [x] Định danh thương hiệu chuẩn mực: `iHOW` — *"Nguyên bản trước — Công nghệ sau."*
- [x] 3 chế độ học tập chuyên biệt: Mode A (Học để hiểu), Mode B (Gỡ lỗi), Mode C (Nhận code).
- [x] Lộ trình tư duy 5 bước có thể điều hướng linh hoạt (Roadmap).
- [x] Thang gợi ý chủ động 5 nấc (Hint Ladder).
- [x] Tự động kích hoạt Model High & Thinking High cho bài toán khó/nâng cao.
- [x] Bài toán chuyển giao (Transfer Challenge).
- [x] Báo cáo tổng kết phiên học dựa trên bằng chứng tương tác thực tế.
- [x] Đánh giá mức độ tự tin tự báo cáo (1–5).
- [x] Bộ kiểm thử tự động cho toàn bộ các module logic.

### Kế hoạch tương lai (Planned / Research)
- [ ] Môi trường Sandbox cách ly an toàn (Docker/WebAssembly) để người học có thể chạy thử nghiệm code thật trực tiếp trên trình duyệt.
- [ ] Nghiên cứu thực nghiệm đối chứng (A/B testing) giữa phương pháp Socratic của iHOW và phương pháp hỏi-đáp AI thông thường để đo lường định lượng hiệu quả ghi nhớ kiến thức.
- [ ] Hỗ trợ lưu trữ phiên học ngoại tuyến (Offline export / PDF report).
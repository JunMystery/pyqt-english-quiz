# English Practice App

Một ứng dụng Desktop được xây dựng bằng Python và PyQt6, giúp người dùng ôn tập và thực hành tiếng Anh thông qua các bài trắc nghiệm (Quiz). 

## Tính năng nổi bật

- **Làm bài thi (Take Quiz)**: Giao diện trực quan với bộ đếm thời gian (Countdown Timer), giúp mô phỏng trải nghiệm thi thật.
- **Quản lý danh sách câu hỏi**: Hệ thống tự động quét và phân mục các bộ đề (.json) có sẵn trong thư mục `data/quizzes`.
- **Chấm điểm và xem lại kết quả**: Ứng dụng hiển thị điểm số và cho phép xem lại (review) đáp án chi tiết ngay khi kết thúc bài quiz.
- **Lưu trữ lịch sử**: Dễ dàng theo dõi tiến độ học tập thông qua lịch sử các bài làm ứng với từng mục và mức điểm tương ứng.
- **Kiến trúc MVC**: Cấu trúc project tuân thủ mô hình Model-View-Controller giúp mã nguồn rõ ràng, có tính mô-đun hoá cao và dễ dàng mở rộng.
- **Parser Tools**: Hỗ trợ một số script độc lập giúp phân tích và chuyển đổi các định dạng đề thô (`.docx`, raw text) sang định dạng dữ liệu chuẩn JSON.

## Cài đặt và Sử dụng

### Yêu cầu hệ thống
- Tương thích đa nền tảng (Windows, macOS, Linux).
- Python 3.8+ trở lên.
- Đã cài đặt [PyQt6](https://pypi.org/project/PyQt6/) để chạy giao diện Desktop.

### Các bước cài đặt
1. **Clone repository về máy**:
   ```bash
   git clone https://github.com/your-username/english-practice.git
   cd english-practice
   ```

2. **Cài đặt thư viện yêu cầu**:
   ```bash
   pip install PyQt6
   ```
   *(Hoặc sử dụng `pip install -r requirements.txt` nếu có setup virtual env).*

3. **Chạy ứng dụng chính**:
   ```bash
   python src/main.py
   ```

## Cấu trúc dự án
```text
english-practice/
│
├── data/                  # Nơi chứa và xử lý hệ dữ liệu các bài quiz (vd: /01-001/data.json. Trong đó 01 là độ khó, 001 là số thứ tự bài). Bạn có thể sử dụng Gen AI để tạo JSON từ PDF, Doc,...
├── src/                   # Thư mục mã nguồn chính (Source code)
│   ├── controllers/       # Các Controller điều hướng logic (Home, Quiz, Result...)
│   ├── models/            # Các Model định dạng dữ liệu (QuizSession, History, Question)
│   ├── views/             # Các View hiển thị UI (MainWindow, HomeView, QuizView...)
│   ├── styles/            # Chứa các tệp giao diện .qss stylesheets và custom icon
│   ├── utils/             # Các tiện ích hệ thống (VD: file_scanner.py)
│   └── main.py            # Entry point khởi chạy app
│
├── EnglishPractice.spec   # File cấu hình đóng gói ứng dụng bằng PyInstaller
└── README.md 
```

## Đóng gói ứng dụng (Build)

Dự án được cấu hình sẵn để biên dịch/đóng gói thành file thực thi độc lập (executable) `.exe` thông qua công cụ `PyInstaller`:
```bash
pyinstaller EnglishPractice.spec
```
Kết quả bản Build cuối cùng sẽ được tải thẳng vào thư mục `dist/`.

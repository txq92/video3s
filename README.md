# Ứng dụng Tạo Video Short 9:16

Ứng dụng web tạo video ngắn tỷ lệ 9:16 từ text và hình ảnh, với âm thanh tự động và subtitle đồng bộ.

## Tính năng

- ✅ Tạo video tỷ lệ 9:16 (1080x1920px) phù hợp cho TikTok, YouTube Shorts, Instagram Reels
- ✅ Chuyển text thành giọng nói tự động với Gemini TTS (hỗ trợ 24 ngôn ngữ, 30 giọng nói)
- ✅ Hỗ trợ 1-3 hình ảnh, tự động resize và crop
- ✅ Subtitle hiển thị đồng bộ với giọng đọc
- ✅ Giao diện web thân thiện, drag & drop upload
- ✅ Theo dõi tiến trình xử lý realtime
- ✅ Tải xuống video kết quả

## Cài đặt

### 1. Clone hoặc tải project
```bash
# Nếu có git
git clone <repository-url>
cd video3s

# Hoặc tải và giải nén vào thư mục video3s
```

### 2. Cài đặt Python dependencies
```bash
# Cài đặt pip packages
pip install -r requirements.txt

# Lưu ý: Cần có API key của Google AI (Gemini)
# Đặt API key trong file video_creator.py
```

### 3. Cài đặt FFmpeg (bắt buộc cho MoviePy)

**Windows:**
- Tải FFmpeg từ: https://ffmpeg.org/download.html
- Giải nén và thêm đường dẫn vào PATH
- Hoặc dùng chocolatey: `choco install ffmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## Chạy ứng dụng

```bash
python app.py
```

Mở trình duyệt và truy cập: http://localhost:5000

## Cách sử dụng

### 1. Nhập nội dung
- Nhập text bạn muốn chuyển thành giọng nói
- Text nên dài 100-200 từ để video có độ dài phù hợp (30-60s)

### 2. Upload hình ảnh (tùy chọn)
- Kéo thả hoặc chọn 1-3 hình ảnh
- Hỗ trợ: JPG, PNG, GIF, BMP
- Tối đa 16MB mỗi file
- Hình ảnh sẽ tự động resize về 9:16

### 3. Tạo video
- Click "Tạo Video"
- Theo dõi tiến trình xử lý
- Tải xuống khi hoàn thành

## Cấu trúc Project

```
video3s/
├── app.py              # Flask server chính
├── video_creator.py    # Module xử lý tạo video
├── requirements.txt    # Python dependencies
├── README.md          # Hướng dẫn này
├── templates/
│   └── index.html     # Giao diện web
├── static/
│   └── script.js      # JavaScript frontend
├── uploads/           # Thư mục tạm cho file upload
└── outputs/           # Thư mục chứa video đã tạo
```

## API Endpoints

- `GET /` - Giao diện chính
- `POST /create_video` - Tạo video từ form data
- `GET /job_status/<job_id>` - Kiểm tra trạng thái job
- `GET /download/<filename>` - Tải video
- `GET /cleanup/<job_id>` - Xóa file sau khi tải

## Xử lý lỗi thường gặp

### 1. Lỗi FFmpeg
```
FFmpeg not found
```
**Giải pháp:** Cài đặt FFmpeg và thêm vào PATH

### 2. Lỗi Gemini TTS
```
API key invalid / Connection error
```
**Giải pháp:** Kiểm tra API key Google AI và kết nối internet

### 3. Lỗi memory
```
Out of memory
```
**Giải pháp:** Giảm kích thước hình ảnh hoặc độ dài text

### 4. Lỗi file format
```
Cannot read image
```
**Giải pháp:** Chỉ upload file hình ảnh hợp lệ (JPG, PNG, GIF, BMP)

## Tùy chỉnh

### Thay đổi kích thước video
Sửa trong `video_creator.py`:
```python
self.width = 1080   # Chiều rộng
self.height = 1920  # Chiều cao
```

### Thay đổi giọng nói Gemini TTS
Sửa trong `video_creator.py`:
```python
# Chọn giọng nói mặc định trong __init__:
self.gemini_voices = {
    'Kore': 'Kore - Firm',  # Giọng mặc định
    'Puck': 'Puck - Rộn ràng',
    # ... 28 giọng khác
}
```

### Thay đổi font subtitle
Thêm font file và sửa trong `create_text_image()`:
```python
font = ImageFont.truetype("path/to/font.ttf", font_size)
```

## Giới hạn

- Tối đa 3 hình ảnh mỗi video
- File ảnh tối đa 16MB
- Text không giới hạn (khuyên dùng 100-200 từ)
- Hỗ trợ 24 ngôn ngữ và 30 giọng nói khác nhau qua Gemini TTS
- Cần API key Google AI (Gemini) để sử dụng TTS

## Phát triển thêm

Có thể mở rộng:
- Thêm hiệu ứng chuyển cảnh
- Hỗ trợ nhiều ngôn ngữ TTS
- Thêm background music
- Tùy chỉnh font và màu sắc subtitle
- Batch processing nhiều video
- User authentication
- Cloud storage integration

## License

MIT License - Tự do sử dụng và phát triển.
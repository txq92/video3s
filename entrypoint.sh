#!/bin/bash

# Entrypoint script cho Docker container

set -e

echo "🚀 Khởi động Video3s Container..."

# Tạo thư mục cần thiết
mkdir -p /app/uploads /app/outputs /app/logs

# Tạo ảnh mặc định nếu chưa có
if [ ! -f "/app/default_images/default1.jpg" ]; then
    echo "📸 Tạo ảnh mặc định..."
    python /app/create_default_images.py
fi

# Kiểm tra kết nối Gemini API
echo "🔑 Kiểm tra kết nối Gemini API..."
python -c "
from google import genai
import os
api_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyAcLoIS03oTfbMmblWt0FiyEciszIFrFac')
try:
    client = genai.Client(api_key=api_key)
    print('✅ Gemini API connection OK')
except Exception as e:
    print(f'⚠️ Gemini API warning: {e}')
"

# Log thông tin container
echo "📊 Container Info:"
echo "- Python version: $(python --version)"
echo "- FFmpeg version: $(ffmpeg -version | head -n 1)"
echo "- Working directory: $(pwd)"
echo "- Available memory: $(free -h | grep Mem | awk '{print $2}')"
echo "- CPU cores: $(nproc)"

# Chạy migrations hoặc setup khác nếu cần
# python setup.py

# Khởi động ứng dụng
echo "🎬 Khởi động Video3s App trên port 4000..."
exec "$@"

#!/bin/bash

echo "🔧 Fixing Entrypoint Issue"
echo "=========================="

# Stop existing containers
sudo docker-compose down

# Create proper entrypoint.sh with correct line endings
cat > entrypoint.sh << 'EOF'
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
echo "- Working directory: $(pwd)"
echo "- Available memory: $(free -h | grep Mem | awk '{print $2}' || echo 'N/A')"
echo "- CPU cores: $(nproc)"

# Khởi động ứng dụng
echo "🎬 Khởi động Video3s App trên port 4000..."
exec "$@"
EOF

# Ensure correct line endings (LF only)
sed -i 's/\r$//' entrypoint.sh

# Make executable
chmod +x entrypoint.sh

echo "✅ Created proper entrypoint.sh with LF line endings"

# Also create a simpler Dockerfile without entrypoint as backup
cat > Dockerfile.simple << 'EOF'
# Sử dụng Python 3.11 slim base image
FROM python:3.11-slim

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libfontconfig1 \
    libxrender1 \
    libgl1-mesa-dri \
    libglib2.0-0 \
    fonts-dejavu-core \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Tạo các thư mục cần thiết
RUN mkdir -p uploads outputs default_images

# Tạo ảnh mặc định
RUN python create_default_images.py

# Expose port
EXPOSE 4000

# Biến môi trường
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Chạy ứng dụng trực tiếp (không dùng entrypoint)
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=4000"]
EOF

echo "✅ Created simple Dockerfile without entrypoint"

# Clean and rebuild
echo "🧹 Cleaning old containers and images..."
sudo docker system prune -f

echo "🔨 Building with proper entrypoint..."
sudo docker-compose build --no-cache video3s

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    echo "🚀 Starting Video3s..."
    sudo docker-compose up -d video3s
    
    sleep 10
    
    echo "🏥 Health check..."
    if curl -f http://localhost:4000/ 2>/dev/null; then
        echo "✅ Video3s is running successfully!"
        echo ""
        echo "🌐 Access: http://localhost:4000"
        echo "📋 Logs: sudo docker-compose logs -f video3s"
    else
        echo "⚠️ Checking logs..."
        sudo docker-compose logs video3s
        echo ""
        echo "💡 If still failing, try the simple version:"
        echo "   cp Dockerfile.simple Dockerfile"
        echo "   sudo docker-compose build --no-cache video3s"
        echo "   sudo docker-compose up -d video3s"
    fi
else
    echo "❌ Build failed. Try simple version:"
    echo "cp Dockerfile.simple Dockerfile"
    echo "sudo docker-compose build --no-cache video3s"
    echo "sudo docker-compose up -d video3s"
fi
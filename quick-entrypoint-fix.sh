#!/bin/bash

echo "⚡ QUICK FIX - Entrypoint Issue"
echo "=============================="

# Stop containers
sudo docker-compose down

# Remove entrypoint from Dockerfile - use direct CMD
cat > Dockerfile << 'EOF'
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

# Clean and build
echo "🧹 Cleaning..."
sudo docker system prune -f

echo "🔨 Building..."
sudo docker-compose build --no-cache video3s

echo "🚀 Starting..."
sudo docker-compose up -d video3s

echo "⏳ Waiting 10 seconds..."
sleep 10

echo "🏥 Testing..."
if curl -f http://localhost:4000/ 2>/dev/null; then
    echo "✅ SUCCESS! Video3s is running!"
    echo ""
    echo "🌐 Access: http://localhost:4000"
    echo "📊 Status: sudo docker-compose ps"
    echo "📋 Logs: sudo docker-compose logs video3s"
else
    echo "⚠️ Still checking, view logs:"
    sudo docker-compose logs video3s
fi
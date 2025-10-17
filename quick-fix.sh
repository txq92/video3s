#!/bin/bash

echo "🚨 QUICK FIX - Docker Syntax Error"
echo "=================================="

# Backup original Dockerfile
if [ -f "Dockerfile" ]; then
    cp Dockerfile Dockerfile.backup
    echo "✅ Backed up original Dockerfile"
fi

# Create correct Dockerfile content
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

# Copy và cấp quyền cho entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 4000

# Biến môi trường
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Sử dụng entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Chạy ứng dụng
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=4000"]
EOF

echo "✅ Created correct Dockerfile"

# Update docker-compose.yml to remove version
if [ -f "docker-compose.yml" ]; then
    sed -i '/^version:/d' docker-compose.yml
    echo "✅ Removed obsolete version from docker-compose.yml"
fi

# Clean old images
echo "🧹 Cleaning old images..."
sudo docker-compose down 2>/dev/null || true
sudo docker system prune -f

# Build and run
echo "🔨 Building with correct syntax..."
sudo docker-compose build --no-cache video3s

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    echo "🚀 Starting Video3s..."
    sudo docker-compose up -d video3s
    
    sleep 10
    
    echo "🏥 Testing health..."
    if curl -f http://localhost:4000/ 2>/dev/null; then
        echo "✅ Video3s is running successfully!"
        echo ""
        echo "🌐 Access: http://localhost:4000"
        echo "📋 Logs: sudo docker-compose logs -f video3s"
    else
        echo "⚠️ Service may still be starting, check logs:"
        sudo docker-compose logs video3s
    fi
else
    echo "❌ Build failed, check logs above"
fi
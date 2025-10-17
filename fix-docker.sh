#!/bin/bash

# Script fix lỗi Docker build cho Linux

echo "🔧 Video3s Docker Fix Script"
echo "================================"

# Kiểm tra Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker không được cài đặt"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose không được cài đặt"
    exit 1
fi

echo "✅ Docker và Docker Compose OK"

# Tạo thư mục cần thiết
echo "📁 Tạo thư mục cần thiết..."
mkdir -p outputs uploads logs

# Stop container cũ nếu có
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true
docker-compose -f docker-compose.fixed.yml down 2>/dev/null || true

# Xóa image cũ để force rebuild
echo "🗑️ Removing old images..."
docker rmi $(docker images | grep video3s | awk '{print $3}') 2>/dev/null || true

# Build với cache buster
echo "🔨 Building with fixed Dockerfile..."
docker-compose -f docker-compose.fixed.yml build --no-cache video3s

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    # Start services
    echo "🚀 Starting services..."
    docker-compose -f docker-compose.fixed.yml up -d video3s
    
    # Wait for service to be ready
    echo "⏳ Waiting for service to start..."
    sleep 10
    
    # Health check
    echo "🏥 Health check..."
    if curl -f http://localhost:4000/ &>/dev/null; then
        echo "✅ Video3s is running successfully!"
        echo ""
        echo "🌐 Access URLs:"
        echo "   - Direct: http://localhost:4000"
        echo "   - Health: http://localhost:4000/health"
        echo ""
        echo "📋 Useful commands:"
        echo "   - View logs: docker-compose -f docker-compose.fixed.yml logs -f video3s"
        echo "   - Stop: docker-compose -f docker-compose.fixed.yml down"
        echo "   - Restart: docker-compose -f docker-compose.fixed.yml restart video3s"
    else
        echo "❌ Service not responding, checking logs..."
        docker-compose -f docker-compose.fixed.yml logs video3s
    fi
else
    echo "❌ Build failed!"
    echo ""
    echo "🔧 Try these fixes:"
    echo "1. Check internet connection"
    echo "2. Update Docker: sudo apt update && sudo apt install docker.io docker-compose"
    echo "3. Clean Docker: docker system prune -a"
    echo "4. Manual build: docker build -t video3s:latest ."
fi
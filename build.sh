#!/bin/bash

# Script build và chạy Video3s trong Docker

set -e

echo "🐳 Video3s Docker Build Script"
echo "================================"

# Parse arguments
MODE="production"
REBUILD=false
LOGS=false

while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--dev)
      MODE="development"
      shift
      ;;
    -r|--rebuild)
      REBUILD=true
      shift
      ;;
    -l|--logs)
      LOGS=true
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  -d, --dev       Chạy development mode"
      echo "  -r, --rebuild   Force rebuild image"
      echo "  -l, --logs      Hiển thị logs sau khi start"
      echo "  -h, --help      Hiển thị help"
      exit 0
      ;;
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

echo "Mode: $MODE"
echo "Rebuild: $REBUILD"

# Tạo thư mục cần thiết
echo "📁 Tạo thư mục cần thiết..."
mkdir -p outputs uploads logs

# Chọn docker-compose file
if [ "$MODE" = "development" ]; then
    COMPOSE_FILE="docker-compose.dev.yml"
else
    COMPOSE_FILE="docker-compose.yml"
fi

echo "🗂️ Sử dụng: $COMPOSE_FILE"

# Rebuild nếu được yêu cầu
if [ "$REBUILD" = true ]; then
    echo "🔨 Rebuilding image..."
    docker-compose -f $COMPOSE_FILE build --no-cache video3s
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f $COMPOSE_FILE down

# Start services
echo "🚀 Starting services..."
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check service status
echo "✅ Service status:"
docker-compose -f $COMPOSE_FILE ps

# Health check
echo "🏥 Health check:"
if curl -f http://localhost:4000/ &>/dev/null; then
    echo "✅ App is healthy"
else
    echo "❌ App is not responding"
fi

# Show access info
echo ""
echo "🌐 Access URLs:"
if [ "$MODE" = "production" ]; then
    echo "   - With Nginx: http://localhost"
    echo "   - Direct app: http://localhost:4000"
else
    echo "   - Development: http://localhost:4000"
fi

# Show logs if requested
if [ "$LOGS" = true ]; then
    echo ""
    echo "📋 Logs (Ctrl+C to stop):"
    docker-compose -f $COMPOSE_FILE logs -f video3s
fi

echo ""
echo "🎬 Video3s is ready!"
echo "Useful commands:"
echo "  - View logs: docker-compose -f $COMPOSE_FILE logs -f"
echo "  - Stop: docker-compose -f $COMPOSE_FILE down"
echo "  - Rebuild: $0 --rebuild"
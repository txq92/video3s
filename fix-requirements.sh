#!/bin/bash

echo "🔧 Fixing Requirements Error"
echo "============================"

# Backup requirements.txt
cp requirements.txt requirements.txt.backup
echo "✅ Backed up requirements.txt"

# Create correct requirements.txt without problematic 'wave' package
cat > requirements.txt << 'EOF'
Flask==2.3.3
moviepy==1.0.3
google-genai
opencv-python==4.8.1.78
Pillow==10.0.1
numpy==1.24.3
requests==2.31.0
python-dotenv==1.0.0
EOF

echo "✅ Fixed requirements.txt (removed problematic 'wave' package)"

# Note: wave module is built-in to Python, no need to install separately
echo "ℹ️  Note: 'wave' is a built-in Python module, no external installation needed"

# Clean Docker cache and rebuild
echo "🧹 Cleaning Docker cache..."
sudo docker-compose down
sudo docker system prune -f

echo "🔨 Building with fixed requirements..."
sudo docker-compose build --no-cache video3s

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    echo "🚀 Starting Video3s..."
    sudo docker-compose up -d video3s
    
    # Wait for service
    echo "⏳ Waiting for service to start..."
    sleep 15
    
    # Health check
    echo "🏥 Health check..."
    if curl -f http://localhost:4000/ 2>/dev/null; then
        echo "✅ Video3s is running successfully!"
        echo ""
        echo "🌐 Access: http://localhost:4000"
        echo "📊 Status: sudo docker-compose ps"
        echo "📋 Logs: sudo docker-compose logs -f video3s"
    else
        echo "⚠️ Service may still be starting, check logs:"
        sudo docker-compose logs video3s
    fi
else
    echo "❌ Build failed!"
    echo ""
    echo "🔍 Debug steps:"
    echo "1. Check requirements.txt content:"
    echo "   cat requirements.txt"
    echo ""
    echo "2. Try manual pip install:"
    echo "   sudo docker run --rm python:3.11-slim pip install -r /dev/stdin < requirements.txt"
    echo ""
    echo "3. Check detailed logs:"
    echo "   sudo docker-compose build video3s"
fi
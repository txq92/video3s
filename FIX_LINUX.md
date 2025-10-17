# 🔧 Fix Docker Build Error trên Linux

## ❌ **Lỗi gặp phải:**
```
E: Package 'libgl1-mesa-glx' has no installation candidate
```

## ✅ **Nguyên nhân:**
Package `libgl1-mesa-glx` đã bị deprecated trong Debian Trixie (mới nhất) và được thay thế bằng `libgl1-mesa-dri`.

## 🚀 **Cách fix nhanh:**

### **Option 1: Sử dụng script tự động**
```bash
# Chạy script fix
chmod +x fix-docker.sh
./fix-docker.sh
```

### **Option 2: Manual fix**
```bash
# 1. Stop containers cũ
sudo docker-compose down

# 2. Xóa image cũ
sudo docker rmi $(sudo docker images | grep video3s | awk '{print $3}')

# 3. Build lại với Dockerfile đã fix
sudo docker-compose -f docker-compose.fixed.yml build --no-cache video3s

# 4. Start service
sudo docker-compose -f docker-compose.fixed.yml up -d video3s

# 5. Kiểm tra
curl http://localhost:4000/
```

### **Option 3: Build trực tiếp**
```bash
# Build image từ Dockerfile đã sửa
sudo docker build -t video3s:latest .

# Chạy container
sudo docker run -d \
  --name video3s-app \
  -p 4000:4000 \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/uploads:/app/uploads \
  video3s:latest
```

## 🔍 **Kiểm tra kết quả:**

```bash
# Xem status containers
sudo docker-compose -f docker-compose.fixed.yml ps

# Xem logs
sudo docker-compose -f docker-compose.fixed.yml logs -f video3s

# Test health
curl http://localhost:4000/

# Test create video
curl -X POST http://localhost:4000/create_video \
  -F "text=Xin chào đây là test video" \
  -F "voice=Puck"
```

## 🛠️ **Packages đã sửa trong Dockerfile:**

### **Before (Lỗi):**
```dockerfile
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libfontconfig1 \
    libxrender1 \
    libgl1-mesa-glx \    # ❌ Deprecated
    fonts-dejavu-core \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*
```

### **After (Fixed):**
```dockerfile
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libfontconfig1 \
    libxrender1 \
    libgl1-mesa-dri \    # ✅ Replacement
    libglib2.0-0 \       # ✅ Added for stability
    fonts-dejavu-core \
    fonts-liberation \
    curl \               # ✅ Added for health checks
    && rm -rf /var/lib/apt/lists/*
```

## 📋 **Files được tạo để fix:**

- **`Dockerfile`** - Updated với packages đúng
- **`docker-compose.fixed.yml`** - Compose file không lỗi
- **`Dockerfile.optimized`** - Multi-stage build tối ưu
- **`fix-docker.sh`** - Script auto fix
- **`FIX_LINUX.md`** - Hướng dẫn này

## 🌐 **Truy cập sau khi fix:**

- **Application**: http://localhost:4000
- **With Nginx**: http://localhost (nếu chạy nginx service)
- **Health check**: http://localhost:4000/health

## ⚡ **Performance tips:**

```bash
# Xem resource usage
sudo docker stats video3s-app

# Limit memory nếu cần
sudo docker update --memory=1g video3s-app

# Clean unused images
sudo docker system prune -a
```

## 🔄 **Nếu vẫn lỗi:**

1. **Update Docker:**
```bash
sudo apt update && sudo apt upgrade docker.io docker-compose
```

2. **Clean Docker:**
```bash
sudo docker system prune -a -f
sudo docker volume prune -f
```

3. **Check logs chi tiết:**
```bash
sudo docker-compose -f docker-compose.fixed.yml logs video3s
```

4. **Manual debug:**
```bash
sudo docker run -it --rm python:3.11-slim bash
# Test packages trong container
```

---

✅ **Sau khi fix, Video3s sẽ chạy ổn định trên Linux với port 4000!**
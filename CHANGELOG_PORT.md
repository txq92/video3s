# 🔄 Port Change: 5000 → 4000

Đã cập nhật tất cả cấu hình để sử dụng **port 4000** thay vì port 5000.

## 📝 Files đã cập nhật:

### 🐳 **Docker Files:**
- **`Dockerfile`** - EXPOSE 4000, CMD port 4000
- **`docker-compose.yml`** - ports: "4000:4000", healthcheck port 4000
- **`docker-compose.dev.yml`** - ports: "4000:4000"
- **`nginx.conf`** - upstream server video3s:4000
- **`entrypoint.sh`** - log message port 4000

### 🛠️ **Scripts:**
- **`build.sh`** - health check port 4000, access URLs port 4000
- **`app.py`** - app.run(port=4000)

### 📚 **Documentation:**
- **`README_DOCKER.md`** - tất cả ví dụ và hướng dẫn port 4000

## 🚀 **Cách sử dụng mới:**

### **Development:**
```bash
# Chạy trực tiếp
python app.py
# Truy cập: http://localhost:4000

# Chạy Docker dev
docker-compose -f docker-compose.dev.yml up -d
# Truy cập: http://localhost:4000
```

### **Production:**
```bash
# Chạy Docker production
docker-compose up -d
# Truy cập: 
#   - Nginx: http://localhost (port 80)
#   - Direct: http://localhost:4000
```

### **Health Check:**
```bash
curl http://localhost:4000/
```

### **Build Script:**
```bash
./build.sh              # Production on port 4000
./build.sh --dev        # Development on port 4000
./build.sh --logs       # Show logs after start
```

## ✅ **Tương thích ngược:**

- **Nginx vẫn chạy port 80** cho production
- **Container internal port** thay đổi từ 5000 → 4000
- **Host mapping** thay đổi từ 5000:5000 → 4000:4000
- **Health checks** cập nhật theo port mới

## 🔧 **Kiểm tra:**

```bash
# Kiểm tra không còn port 5000
findstr /r /n "5000" *.yml *.sh *.conf Dockerfile app.py

# Kiểm tra app chạy đúng port
docker-compose up -d video3s
curl http://localhost:4000/
```

---
**Date:** $(date)  
**Status:** ✅ Completed
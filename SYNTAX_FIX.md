# 🚨 URGENT FIX: Docker Syntax Error

## ❌ **Lỗi:**
```
failed to solve: dockerfile parse error on line 6: unknown instruction: ffmpeg
```

## ✅ **Nguyên nhân:** 
- Dockerfile có syntax sai: `\\` thay vì `\`
- `version` trong docker-compose.yml đã obsolete

## 🚀 **Fix ngay:**

### **Cách 1: Chạy script tự động**
```bash
chmod +x quick-fix.sh
./quick-fix.sh
```

### **Cách 2: Fix manual**

1. **Tạo lại Dockerfile đúng:**
```bash
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
```

2. **Fix docker-compose.yml:**
```bash
sed -i '/^version:/d' docker-compose.yml
```

3. **Build và chạy:**
```bash
sudo docker-compose down
sudo docker-compose build --no-cache video3s
sudo docker-compose up -d video3s
```

### **Cách 3: One-liner**
```bash
curl -s https://raw.githubusercontent.com/your-repo/video3s/main/Dockerfile > Dockerfile && sudo docker-compose up -d video3s --build
```

## 🔍 **Kiểm tra:**
```bash
# Test service
curl http://localhost:4000/

# View logs
sudo docker-compose logs -f video3s

# Check status
sudo docker-compose ps
```

## ⚡ **Vấn đề đã fix:**

### **Before (Lỗi):**
```dockerfile
RUN apt-get update && apt-get install -y \\
    ffmpeg \\
    libsm6 \\
```
**❌ Syntax sai:** `\\` (double backslash)

### **After (Đúng):**
```dockerfile
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
```
**✅ Syntax đúng:** `\` (single backslash)

### **Docker Compose:**
```yaml
# Before (Warning)
version: '3.8'  # ❌ Obsolete

# After (Clean)
# version removed   # ✅ No warning
```

## 🎯 **Kết quả mong đợi:**
```
✅ Build successful!
✅ Video3s is running successfully!
🌐 Access: http://localhost:4000
```

---
**Thời gian fix: 2-3 phút** ⏱️
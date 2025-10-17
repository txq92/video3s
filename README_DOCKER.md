# 🐳 Video3s Docker Deployment

Hướng dẫn đóng gói và chạy ứng dụng Video3s trong Docker trên môi trường Linux.

## 📋 Yêu cầu

- Docker Engine 20.10+
- Docker Compose 2.0+
- RAM: 2GB+ khuyến nghị
- Disk: 5GB+ trống

## 🚀 Cách triển khai

### 1. Production (Khuyến nghị)

```bash
# Clone hoặc copy source code
git clone <repository> video3s
cd video3s

# Tạo thư mục cần thiết
mkdir -p outputs uploads logs

# Chạy với Nginx reverse proxy
docker-compose up -d

# Hoặc chỉ chạy app
docker-compose up -d video3s
```

**Truy cập ứng dụng:**
- Với Nginx: `http://localhost` (port 80)
- Trực tiếp: `http://localhost:4000`

### 2. Development

```bash
# Chạy development mode
docker-compose -f docker-compose.dev.yml up -d

# Xem logs
docker-compose logs -f video3s
```

### 3. Chỉ Docker (không compose)

```bash
# Build image
docker build -t video3s:latest .

# Chạy container
docker run -d \\
  --name video3s-app \\
  -p 4000:4000 \\
  -v $(pwd)/outputs:/app/outputs \\
  -v $(pwd)/uploads:/app/uploads \\
  video3s:latest
```

## 🔧 Cấu hình

### Environment Variables

```yaml
environment:
  - FLASK_ENV=production          # hoặc development
  - FLASK_DEBUG=0                 # 1 cho debug mode
  - PYTHONUNBUFFERED=1           # Hiển thị logs realtime
  - GEMINI_API_KEY=your_key_here # API key Google AI
```

### Volume Mounts

```yaml
volumes:
  - ./outputs:/app/outputs     # Video đã tạo
  - ./uploads:/app/uploads     # File upload tạm
  - ./logs:/app/logs          # Log files
```

### Resource Limits

```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'      # Tối đa 2 CPU cores
      memory: 2G       # Tối đa 2GB RAM
    reservations:
      cpus: '0.5'      # Tối thiểu 0.5 cores
      memory: 512M     # Tối thiểu 512MB RAM
```

## 🛠️ Các lệnh hữu ích

### Quản lý container

```bash
# Xem status
docker-compose ps

# Xem logs
docker-compose logs -f video3s

# Restart service
docker-compose restart video3s

# Stop tất cả
docker-compose down

# Stop và xóa volumes
docker-compose down -v

# Rebuild image
docker-compose build --no-cache video3s
```

### Debug

```bash
# Vào container
docker-compose exec video3s bash

# Kiểm tra process
docker-compose exec video3s ps aux

# Kiểm tra disk space
docker-compose exec video3s df -h

# Test Gemini API
docker-compose exec video3s python -c "from google import genai; print('OK')"
```

### Logs và monitoring

```bash
# Xem logs realtime
docker-compose logs -f

# Xem resource usage
docker stats video3s-app

# Health check
curl http://localhost:4000/health
```

## 📊 Monitoring với Nginx

Nginx cung cấp:
- **Rate limiting**: 5 requests/minute cho `/create_video`
- **File size limit**: 50MB
- **Gzip compression**: Tối ưu bandwidth
- **Health check endpoint**: `/health`
- **Access logs**: `/var/log/nginx/access.log`

## 🔒 Production Security

### 1. Environment Variables

Tạo file `.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
FLASK_SECRET_KEY=your_secret_key
```

### 2. Reverse Proxy

```yaml
# docker-compose.override.yml
services:
  nginx:
    volumes:
      - /path/to/ssl:/etc/nginx/ssl:ro
    environment:
      - SSL_CERT=/etc/nginx/ssl/cert.pem
      - SSL_KEY=/etc/nginx/ssl/key.pem
```

### 3. Network Security

```yaml
networks:
  internal:
    internal: true
  external:
    driver: bridge
```

## 📝 Troubleshooting

### Lỗi thường gặp

1. **Port đã sử dụng**
```bash
# Thay đổi port
docker-compose up -d --scale nginx=0
# hoặc sửa port trong docker-compose.yml
```

2. **Không đủ RAM**
```bash
# Giảm worker processes
docker-compose exec video3s ps aux
docker system prune
```

3. **Lỗi Gemini API**
```bash
# Kiểm tra API key
docker-compose exec video3s env | grep GEMINI
```

4. **Permission denied**
```bash
# Fix quyền thư mục
sudo chown -R 1000:1000 outputs uploads logs
```

### Health Check

```bash
# Container health
docker inspect video3s-app | grep Health -A 10

# Application health  
curl -f http://localhost:4000/ || echo "App down"
```

## 🔄 Auto-restart và backup

### Systemd service (Ubuntu/CentOS)

```bash
# Tạo service file
sudo nano /etc/systemd/system/video3s.service

# Nội dung:
[Unit]
Description=Video3s Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/video3s
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down

[Install]
WantedBy=multi-user.target

# Enable service
sudo systemctl enable video3s
sudo systemctl start video3s
```

### Backup script

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "video3s_backup_$DATE.tar.gz" outputs/ uploads/ docker-compose.yml
```

## 📈 Scaling (nếu cần)

```yaml
# docker-compose.scale.yml
services:
  video3s:
    deploy:
      replicas: 3
  
  nginx:
    depends_on:
      - video3s
```

```bash
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d
```
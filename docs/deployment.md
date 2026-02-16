# Yacht MES 部署指南

## 系统要求

### 最低配置
- **CPU**: 2 核
- **内存**: 4 GB
- **磁盘**: 50 GB
- **操作系统**: Linux (Ubuntu 20.04+ / CentOS 8+)

### 推荐配置
- **CPU**: 4 核
- **内存**: 8 GB
- **磁盘**: 100 GB SSD
- **操作系统**: Linux (Ubuntu 22.04 LTS)

### 依赖软件
- Docker 20.10+
- Docker Compose 2.0+
- Git (可选)

## 快速部署

### 1. 克隆项目
```bash
git clone https://github.com/your-org/yacht-mes.git
cd yacht-mes
```

### 2. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
vim .env
```

**.env 示例**:
```env
# 数据库配置
DATABASE_URL=postgresql+asyncpg://yacht_mes:yacht_mes_2024@postgres:5432/yacht_mes

# Redis 配置
REDIS_URL=redis://redis:6379/0

# JWT 密钥（生产环境请修改）
SECRET_KEY=your-secret-key-change-in-production

# Kimi API 配置（可选）
KIMI_API_KEY=your-kimi-api-key

# MinIO 配置
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

### 3. 启动服务
```bash
# 使用启动脚本
./start.sh

# 或手动启动
docker-compose up -d
```

### 4. 验证部署
```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 测试 API 健康检查
curl http://localhost:8000/health
```

### 5. 访问系统
- **Web 界面**: http://localhost:8080
- **API 文档**: http://localhost:8000/docs
- **MinIO 控制台**: http://localhost:9001

**默认账号**:
- 用户名: `admin`
- 密码: `admin`

## 手动部署（不使用 Docker）

### 后端部署

#### 1. 安装 Python 依赖
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. 配置数据库
```bash
# 安装 PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# 创建数据库
sudo -u postgres psql -c "CREATE DATABASE yacht_mes;"
sudo -u postgres psql -c "CREATE USER yacht_mes WITH PASSWORD 'yacht_mes_2024';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE yacht_mes TO yacht_mes;"
```

#### 3. 运行迁移
```bash
alembic upgrade head
```

#### 4. 启动服务
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 前端部署

#### 1. 安装 Node.js 依赖
```bash
cd frontend
npm install
```

#### 2. 构建生产版本
```bash
npm run build
```

#### 3. 使用 Nginx 部署
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/yacht-mes/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 生产环境配置

### 1. 使用 HTTPS
```bash
# 使用 Let's Encrypt 获取证书
certbot --nginx -d your-domain.com
```

### 2. 配置反向代理
```nginx
# /etc/nginx/sites-available/yacht-mes
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        root /var/www/yacht-mes/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. 配置系统服务
```bash
# 创建 systemd 服务
sudo vim /etc/systemd/system/yacht-mes.service
```

```ini
[Unit]
Description=Yacht MES Backend
After=network.target

[Service]
Type=simple
User=yacht-mes
WorkingDirectory=/opt/yacht-mes/backend
Environment=PATH=/opt/yacht-mes/backend/venv/bin
ExecStart=/opt/yacht-mes/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl enable yacht-mes
sudo systemctl start yacht-mes
```

### 4. 配置自动备份
```bash
# 创建备份脚本
sudo vim /opt/yacht-mes/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/backup/yacht-mes"
DATE=$(date +%Y%m%d_%H%M%S)

# 备份数据库
docker-compose exec -T postgres pg_dump -U yacht_mes yacht_mes > "$BACKUP_DIR/db_$DATE.sql"

# 备份上传文件
tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" /opt/yacht-mes/uploads

# 保留最近 30 天备份
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

```bash
# 添加定时任务
crontab -e
# 每天凌晨 2 点备份
0 2 * * * /opt/yacht-mes/backup.sh
```

## 监控与日志

### 查看日志
```bash
# Docker 部署
docker-compose logs -f backend
docker-compose logs -f frontend

# 手动部署
sudo journalctl -u yacht-mes -f
```

### 性能监控
```bash
# 安装 Prometheus + Grafana（可选）
docker-compose -f docker-compose.monitoring.yml up -d
```

## 故障排查

### 服务无法启动
```bash
# 检查端口占用
sudo netstat -tlnp | grep 8000
sudo netstat -tlnp | grep 8080

# 检查数据库连接
docker-compose exec postgres psql -U yacht_mes -c "\l"
```

### 数据库连接失败
```bash
# 检查 PostgreSQL 状态
docker-compose exec postgres pg_isready

# 重置数据库（谨慎操作）
docker-compose down -v
docker-compose up -d postgres
```

### 前端构建失败
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 升级维护

### 更新代码
```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

### 数据库迁移
```bash
docker-compose exec backend alembic upgrade head
```

## 安全建议

1. **修改默认密码**: 首次登录后立即修改 admin 密码
2. **使用 HTTPS**: 生产环境必须启用 HTTPS
3. **定期备份**: 配置自动备份策略
4. **防火墙配置**: 只开放必要的端口（80, 443）
5. **更新依赖**: 定期更新系统依赖和 Docker 镜像

## 获取帮助

- **GitHub Issues**: https://github.com/your-org/yacht-mes/issues
- **文档**: https://docs.yacht-mes.ai
- **邮件支持**: support@yacht-mes.ai

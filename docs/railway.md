# Railway 部署指南

## 快速部署（3分钟）

### 1. 注册 Railway
```
1. 访问 https://railway.app
2. 点击 "Get Started"
3. 选择 "Deploy from GitHub repo"
4. 授权 GitHub 访问
```

### 2. 创建项目
```
1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择你的 yacht-mes 仓库
4. Railway 会自动检测并部署
```

### 3. 添加数据库
```
1. 点击 "New" → "Database" → "Add PostgreSQL"
2. 点击 "New" → "Database" → "Add Redis"
3. Railway 会自动注入环境变量
```

### 4. 配置环境变量
在 Railway 项目设置中添加：

```
SECRET_KEY=your-random-secret-key-here
KIMI_API_KEY=your-kimi-api-key (可选)
```

### 5. 部署前端
```
1. 点击 "New" → "Empty Service"
2. 名称改为 "frontend"
3. 选择 GitHub 同一个仓库
4. 在设置中修改：
   - Root Directory: frontend
   - Build Command: npm run build
   - Start Command: npx serve -s dist -p $PORT
```

### 6. 自定义域名（可选）
```
1. 进入服务设置
2. 点击 "Settings" → "Domains"
3. 点击 "Generate Domain" 或添加自定义域名
```

---

## 部署后访问

- **后端 API**: https://your-project.up.railway.app
- **前端页面**: https://frontend-your-project.up.railway.app
- **API 文档**: https://your-project.up.railway.app/docs

---

## 免费额度说明

| 资源 | 免费额度 | Yacht MES 用量 |
|------|----------|----------------|
| CPU | 无限制 | 低 |
| 内存 | 512MB | 足够 |
| 磁盘 | 1GB | 足够 |
| 流量 | 100GB/月 | 充足 |
| 执行时间 | $5/月 | 约 $3-4 |

---

## 故障排查

### 部署失败
```
1. 检查日志：Railway 控制台 → Deployments → View Logs
2. 确认 Dockerfile 路径正确
3. 检查环境变量是否设置
```

### 数据库连接失败
```
1. 确认 PostgreSQL 服务已启动
2. 检查 DATABASE_URL 是否自动注入
3. 手动添加 DATABASE_URL 环境变量
```

### 前端无法访问 API
```
1. 修改 frontend/src/api/index.ts
2. 将 baseURL 改为 Railway 后端地址
3. 重新部署前端
```

---

## 替代方案

如果 Railway 不适合，还可以用：

| 平台 | 特点 | 价格 |
|------|------|------|
| Render | 免费，支持 Docker | 免费 |
| Fly.io | 边缘部署，速度快 | 免费额度 |
| Vercel | 前端最优 | 免费 |
| 阿里云/腾讯云 | 国内访问快 | ¥50-100/月 |

---

## 需要帮助？

1. Railway 文档：https://docs.railway.app
2. 社区 Discord：https://discord.gg/railway
3. 或询问我部署问题

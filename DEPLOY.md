# Yacht MES - 快速部署指南（用户: neglson）

## 🚀 一键部署到 Railway（推荐）

### 步骤 1: 推送代码到 GitHub

```bash
# 运行推送脚本
cd /root/.openclaw/workspace/yacht-mes
./scripts/push-to-github.sh
```

或者手动操作：
```bash
cd /root/.openclaw/workspace/yacht-mes
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/neglson/yacht-mes.git
git push -u origin main
```

### 步骤 2: 在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 仓库名: `yacht-mes`
3. 描述: `铝合金电动游艇建造管理系统`
4. 选择 Public
5. 点击 "Create repository"

### 步骤 3: 部署到 Railway

1. 访问 https://railway.app
2. 点击 "Get Started" → "Login with GitHub"
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择 `neglson/yacht-mes`
6. Railway 自动检测配置并部署

### 步骤 4: 添加数据库

1. 在 Railway 项目页面点击 "New"
2. 选择 "Database" → "Add PostgreSQL"
3. 选择 "Database" → "Add Redis"
4. 服务自动重启并连接数据库

### 步骤 5: 获取访问地址

部署完成后，你会得到：
- **后端 API**: `https://backend-yacht-mes-production.up.railway.app`
- **API 文档**: `https://backend-yacht-mes-production.up.railway.app/docs`
- **前端页面**: `https://frontend-xxx.up.railway.app`（需要单独部署前端）

---

## 🌐 你的部署信息

| 项目 | 值 |
|------|-----|
| GitHub 用户 | neglson |
| 仓库地址 | https://github.com/neglson/yacht-mes |
| Railway 项目 | yacht-mes |

---

## 📋 部署前检查清单

- [ ] Git 已安装
- [ ] Git 已配置用户名和邮箱
- [ ] GitHub 账号已创建
- [ ] GitHub 仓库 `yacht-mes` 已创建
- [ ] Railway 账号已绑定 GitHub

---

## 🔧 故障排查

### 推送失败
```bash
# 检查远程仓库
git remote -v

# 重新添加远程
git remote remove origin
git remote add origin https://github.com/neglson/yacht-mes.git
```

### Railway 部署失败
1. 检查 `railway.json` 是否存在
2. 检查 Dockerfile 路径是否正确
3. 查看 Railway 部署日志

### 数据库连接失败
1. 确认 PostgreSQL 服务已添加
2. 检查环境变量 `DATABASE_URL` 是否自动注入
3. 手动添加：Settings → Variables

---

## 💡 提示

- Railway 免费额度：$5/月（足够运行本项目）
- 自定义域名：Settings → Domains → Custom Domain
- 自动部署：每次 push 到 main 分支自动重新部署

---

## 📞 需要帮助？

- Railway 文档: https://docs.railway.app
- 项目文档: `./docs/`
- 或询问 Kimi Claw

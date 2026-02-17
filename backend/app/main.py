"""
Yacht MES - FastAPI Backend
铝合金电动游艇建造管理系统后端
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.database import engine, Base
from app.routers import auth, users, projects, tasks, materials, procurement, inventory, attachments, ai, dashboard, import_data, notifications, audit


app = FastAPI(
    title="Yacht MES API",
    description="铝合金电动游艇建造管理系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": "internal_error"}
    )


# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "yacht-mes-api", "version": "1.0.0"}


# 根路径 - 返回登录页面
@app.get("/", response_class=HTMLResponse)
async def root():
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Yacht MES 登录</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .login-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); width: 350px; }
        h2 { text-align: center; color: #333; margin-bottom: 30px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; font-size: 14px; }
        button { width: 100%; padding: 14px; background: #409EFF; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin-top: 20px; }
        button:hover { background: #66b1ff; }
        #result { margin-top: 20px; padding: 12px; border-radius: 5px; display: none; font-size: 14px; }
        .success { background: #f0f9eb; color: #67c23a; border: 1px solid #67c23a; }
        .error { background: #fef0f0; color: #f56c6c; border: 1px solid #f56c6c; }
        .links { margin-top: 20px; text-align: center; font-size: 14px; }
        .links a { color: #409EFF; text-decoration: none; margin: 0 10px; }
        .links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🚢 Yacht MES</h2>
        <p style="text-align: center; color: #666; margin-bottom: 20px;">铝合金电动游艇建造管理系统</p>
        <input type="text" id="username" placeholder="用户名" value="admin">
        <input type="password" id="password" placeholder="密码" value="admin">
        <button onclick="login()">登录</button>
        <div id="result"></div>
        <div class="links">
            <a href="/docs">API 文档</a> | <a href="/health">健康检查</a>
        </div>
    </div>
    
    <script>
        async function login() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const resultDiv = document.getElementById('result');
            
            try {
                // 使用 form 格式
                const formData = new URLSearchParams();
                formData.append('username', username);
                formData.append('password', password);
                
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    resultDiv.className = 'success';
                    resultDiv.innerHTML = '✅ 登录成功！正在跳转...';
                    resultDiv.style.display = 'block';
                    localStorage.setItem('token', data.access_token);
                    localStorage.setItem('username', username);
                    // 跳转到管理界面
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 1000);
                } else {
                    resultDiv.className = 'error';
                    resultDiv.textContent = '❌ 登录失败: ' + (data.detail || '用户名或密码错误');
                    resultDiv.style.display = 'block';
                }
            } catch (e) {
                resultDiv.className = 'error';
                resultDiv.textContent = '❌ 请求失败: ' + e.message;
                resultDiv.style.display = 'block';
            }
        }
        
        // 回车登录
        document.getElementById('password').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') login();
        });
    </script>
</body>
</html>"""


# 仪表盘页面 - 使用不同的函数名避免冲突
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Yacht MES 管理仪表盘</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f2f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { font-size: 24px; }
        .header .user { display: flex; align-items: center; gap: 20px; }
        .header button { background: rgba(255,255,255,0.2); border: 1px solid white; color: white; padding: 8px 20px; border-radius: 4px; cursor: pointer; }
        .container { max-width: 1200px; margin: 20px auto; padding: 0 20px; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .card h3 { color: #666; font-size: 14px; margin-bottom: 10px; }
        .card .number { font-size: 32px; font-weight: bold; color: #409EFF; }
        .menu { background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }
        .menu-item { padding: 15px 20px; border-bottom: 1px solid #eee; cursor: pointer; transition: background 0.3s; }
        .menu-item:hover { background: #f5f5f5; }
        .menu-item:last-child { border-bottom: none; }
        .menu-item h4 { color: #333; margin-bottom: 5px; }
        .menu-item p { color: #999; font-size: 14px; }
        .content { background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 30px; margin-top: 20px; }
        .welcome { text-align: center; padding: 60px 20px; }
        .welcome h2 { color: #333; margin-bottom: 20px; }
        .welcome p { color: #666; font-size: 16px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚢 Yacht MES 管理系统</h1>
        <div class="user">
            <span id="username">管理员</span>
            <button onclick="logout()">退出登录</button>
        </div>
    </div>
    
    <div class="container">
        <div class="cards">
            <div class="card">
                <h3>进行中项目</h3>
                <div class="number">3</div>
            </div>
            <div class="card">
                <h3>待处理任务</h3>
                <div class="number">12</div>
            </div>
            <div class="card">
                <h3>库存预警</h3>
                <div class="number">2</div>
            </div>
            <div class="card">
                <h3>本月采购</h3>
                <div class="number">¥128万</div>
            </div>
        </div>
        
        <div class="menu">
            <div class="menu-item" onclick="alert('项目管理功能开发中')">
                <h4>📋 项目管理</h4>
                <p>查看和管理游艇建造项目</p>
            </div>
            <div class="menu-item" onclick="alert('任务管理功能开发中')">
                <h4>📅 任务管理</h4>
                <p>分配和跟踪生产任务</p>
            </div>
            <div class="menu-item" onclick="alert('物料管理功能开发中')">
                <h4>📦 物料管理</h4>
                <p>管理原材料和零部件</p>
            </div>
            <div class="menu-item" onclick="alert('采购管理功能开发中')">
                <h4>🛒 采购管理</h4>
                <p>处理采购订单和供应商</p>
            </div>
            <div class="menu-item" onclick="alert('库存管理功能开发中')">
                <h4>🏭 库存管理</h4>
                <p>监控仓库库存状态</p>
            </div>
            <div class="menu-item" onclick="alert('质量管理功能开发中')">
                <h4>✅ 质量管理</h4>
                <p>质量检验和报告</p>
            </div>
        </div>
        
        <div class="content">
            <div class="welcome">
                <h2>欢迎使用 Yacht MES 管理系统</h2>
                <p>铝合金电动游艇建造管理系统 - 让生产更高效、更智能</p>
                <p style="margin-top: 30px; color: #999;">点击上方菜单开始使用</p>
                <p style="margin-top: 20px; color: #409EFF; font-size: 12px;">版本: v1.0.1 | 自动更新已启用 ✅</p>
            </div>
        </div>
    </div>
    
    <script>
        // 检查登录状态
        const token = localStorage.getItem('token');
        const username = localStorage.getItem('username');
        if (!token) {
            window.location.href = '/';
        } else {
            document.getElementById('username').textContent = username || '管理员';
        }
        
        function logout() {
            localStorage.removeItem('token');
            localStorage.removeItem('username');
            window.location.href = '/';
        }
    </script>
</body>
</html>"""


# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(projects.router, prefix="/api/projects", tags=["项目管理"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["任务管理"])
app.include_router(materials.router, prefix="/api/materials", tags=["物料管理"])
app.include_router(procurement.router, prefix="/api/procurement", tags=["采购管理"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["库存管理"])
app.include_router(attachments.router, prefix="/api/attachments", tags=["附件管理"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI 助手"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["仪表盘"])
app.include_router(import_data.router, prefix="/api/import", tags=["数据导入"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["通知"])
app.include_router(audit.router, prefix="/api/audit", tags=["审计日志"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

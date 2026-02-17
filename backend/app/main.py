"""
Yacht MES - FastAPI Backend
铝合金电动游艇建造管理系统后端
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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

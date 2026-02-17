# Yacht MES - 极简部署配置
# 跳过健康检查，避免网络问题

FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY backend/app/ ./app/

# 设置环境变量
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite+aiosqlite:///./data/yacht_mes.db
ENV REDIS_URL=memory://
ENV SECRET_KEY=yacht-mes-production-secret-key-2024
ENV DEBUG=false

# 创建数据目录
RUN mkdir -p /app/data /app/uploads

# 暴露端口
EXPOSE 8000

# 启动命令 - 直接使用8000端口，不依赖$PORT
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

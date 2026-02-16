# 阶段1：构建
FROM python:3.11-slim as builder

WORKDIR /app

# 安装依赖
COPY backend/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 阶段2：运行
FROM python:3.11-slim

WORKDIR /app

# 从builder复制依赖
COPY --from=builder /root/.local /root/.local

# 复制应用代码
COPY backend/app/ ./app/

# 设置环境变量
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PORT=8000

# 创建上传目录
RUN mkdir -p /app/uploads

# 暴露端口
EXPOSE 8000

# 启动命令 - 直接使用8000端口
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

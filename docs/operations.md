# Yacht MES - 运维脚本

## 数据库备份

```bash
./scripts/backup.sh
```

## 查看日志

```bash
# 所有服务日志
docker-compose logs -f

# 仅后端日志
docker-compose logs -f backend

# 仅前端日志
docker-compose logs -f frontend
```

## 数据库迁移

```bash
# 进入后端容器
docker-compose exec backend bash

# 执行迁移
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

## 重置系统

```bash
# 停止并删除所有容器和数据
./scripts/reset.sh
```

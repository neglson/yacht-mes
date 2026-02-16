#!/bin/bash

# 数据库备份脚本

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="yacht_mes_backup_${DATE}.sql"

mkdir -p $BACKUP_DIR

echo "开始备份数据库..."

docker-compose exec -T postgres pg_dump -U yacht_mes yacht_mes > "$BACKUP_DIR/$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ 备份成功: $BACKUP_FILE"
    # 保留最近 30 天的备份
    find $BACKUP_DIR -name "yacht_mes_backup_*.sql" -mtime +30 -delete
else
    echo "❌ 备份失败"
    exit 1
fi

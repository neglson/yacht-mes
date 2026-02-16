"""
数据库配置 - 支持 PostgreSQL 和 SQLite
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

# 检测环境
DATABASE_URL = os.getenv("DATABASE_URL", "")

# 如果是 Railway 的 PostgreSQL，需要转换协议
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 如果没有数据库，使用 SQLite（仅用于测试）
if not DATABASE_URL:
    DATABASE_URL = "sqlite+aiosqlite:///./test.db"
    print("⚠️  Using SQLite for testing")
else:
    print(f"✅ Using database: {DATABASE_URL.split('@')[0]}@***")

# 创建引擎
if "sqlite" in DATABASE_URL:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True
    )
else:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        poolclass=NullPool,
        future=True
    )

# 会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


# 获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

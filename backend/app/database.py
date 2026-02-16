"""
数据库连接和会话管理
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from app.config import settings

# 创建异步引擎（带重试）
max_retries = 5
retry_delay = 5

for attempt in range(max_retries):
    try:
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            poolclass=NullPool if settings.DEBUG else None,
            future=True,
            connect_args={
                "command_timeout": 60,
                "server_settings": {
                    "jit": "off"
                }
            }
        )
        print(f"✅ Database engine created successfully")
        break
    except Exception as e:
        print(f"⚠️ Database connection attempt {attempt + 1}/{max_retries} failed: {e}")
        if attempt < max_retries - 1:
            asyncio.sleep(retry_delay)
        else:
            print(f"❌ Failed to create database engine after {max_retries} attempts")
            raise

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# 声明基类
Base = declarative_base()


async def get_db():
    """获取数据库会话的依赖函数"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

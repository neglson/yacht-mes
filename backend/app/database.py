"""
数据库配置 - 兼容 Python 3.6 + SQLAlchemy 1.4
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# 检测环境
DATABASE_URL = os.getenv("DATABASE_URL", "")

# 如果没有数据库，使用 SQLite
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./data/yacht_mes.db"
    print("Using SQLite")
else:
    print("Using database")

# 创建引擎（同步模式，兼容 Python 3.6）
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        poolclass=NullPool
    )

# 会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

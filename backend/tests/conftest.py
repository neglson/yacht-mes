"""
测试配置和 fixtures
"""

import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.database import Base, get_db
from app.config import settings

# 测试数据库 URL
TEST_DATABASE_URL = "postgresql+asyncpg://yacht_mes:yacht_mes_2024@localhost/yacht_mes_test"

# 创建测试引擎
engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool,
    future=True
)

# 测试会话工厂
TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def init_db():
    """初始化测试数据库"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def override_get_db() -> AsyncGenerator:
    """覆盖数据库依赖"""
    async with TestingSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# 替换数据库依赖
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """设置测试数据库"""
    await init_db()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client() -> AsyncGenerator:
    """创建测试客户端"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def db_session() -> AsyncGenerator:
    """创建数据库会话"""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def admin_token(client: AsyncClient) -> str:
    """获取管理员 token"""
    # 先创建管理员用户
    from app.utils.security import get_password_hash
    from app.models import User
    
    async with TestingSessionLocal() as session:
        admin = User(
            username="admin",
            password_hash=get_password_hash("admin"),
            real_name="管理员",
            role="admin",
            is_active=True
        )
        session.add(admin)
        await session.commit()
    
    # 登录获取 token
    response = await client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin"}
    )
    return response.json()["access_token"]


@pytest.fixture
async def auth_headers(admin_token: str) -> dict:
    """认证请求头"""
    return {"Authorization": f"Bearer {admin_token}"}

"""
认证模块测试
"""

import pytest
from httpx import AsyncClient


class TestAuth:
    """认证相关测试"""
    
    async def test_login_success(self, client: AsyncClient):
        """测试正常登录"""
        # 先创建测试用户
        from app.utils.security import get_password_hash
        from app.models import User
        from tests.conftest import TestingSessionLocal
        
        async with TestingSessionLocal() as session:
            user = User(
                username="testuser",
                password_hash=get_password_hash("testpass"),
                real_name="测试用户",
                role="worker",
                is_active=True
            )
            session.add(user)
            await session.commit()
        
        response = await client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpass"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    async def test_login_wrong_password(self, client: AsyncClient):
        """测试密码错误"""
        response = await client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "wrongpass"}
        )
        
        assert response.status_code == 401
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """测试用户不存在"""
        response = await client.post(
            "/api/auth/login",
            data={"username": "nonexistent", "password": "pass"}
        )
        
        assert response.status_code == 401
    
    async def test_get_me(self, client: AsyncClient, auth_headers: dict):
        """测试获取当前用户信息"""
        response = await client.get(
            "/api/auth/me",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin"
        assert data["role"] == "admin"
    
    async def test_get_me_without_token(self, client: AsyncClient):
        """测试未授权访问"""
        response = await client.get("/api/auth/me")
        
        assert response.status_code == 401
    
    async def test_refresh_token(self, client: AsyncClient, auth_headers: dict):
        """测试刷新 token"""
        response = await client.post(
            "/api/auth/refresh",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

"""
用户管理模块测试
"""

import pytest
from httpx import AsyncClient


class TestUsers:
    """用户管理相关测试"""
    
    async def test_list_users(self, client: AsyncClient, auth_headers: dict):
        """测试获取用户列表"""
        response = await client.get(
            "/api/users",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_create_user(self, client: AsyncClient, auth_headers: dict):
        """测试创建用户"""
        user_data = {
            "username": "newuser",
            "password": "newpass123",
            "real_name": "新用户",
            "role": "worker",
            "is_active": True
        }
        
        response = await client.post(
            "/api/users",
            json=user_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["real_name"] == "新用户"
    
    async def test_create_user_duplicate_username(
        self, client: AsyncClient, auth_headers: dict
    ):
        """测试创建重复用户"""
        user_data = {
            "username": "admin",  # 已存在的用户名
            "password": "pass123",
            "real_name": "重复用户",
            "role": "worker"
        }
        
        response = await client.post(
            "/api/users",
            json=user_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
    
    async def test_get_user(self, client: AsyncClient, auth_headers: dict):
        """测试获取单个用户"""
        response = await client.get(
            "/api/users/1",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
    
    async def test_update_user(self, client: AsyncClient, auth_headers: dict):
        """测试更新用户"""
        update_data = {
            "real_name": "更新的姓名",
            "phone": "13800138000"
        }
        
        response = await client.put(
            "/api/users/1",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["real_name"] == "更新的姓名"
    
    async def test_delete_user(self, client: AsyncClient, auth_headers: dict):
        """测试删除用户"""
        # 先创建一个用户
        user_data = {
            "username": "todelete",
            "password": "pass123",
            "real_name": "待删除用户",
            "role": "worker"
        }
        
        create_response = await client.post(
            "/api/users",
            json=user_data,
            headers=auth_headers
        )
        user_id = create_response.json()["id"]
        
        # 删除用户
        response = await client.delete(
            f"/api/users/{user_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    async def test_reset_password(self, client: AsyncClient, auth_headers: dict):
        """测试重置密码"""
        response = await client.post(
            "/api/users/1/reset-password",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "密码已重置" in data["message"]
    
    async def test_list_users_without_permission(self, client: AsyncClient):
        """测试无权限访问"""
        response = await client.get("/api/users")
        
        assert response.status_code == 401

"""
仪表盘模块测试
"""

import pytest
from httpx import AsyncClient


class TestDashboard:
    """仪表盘相关测试"""
    
    async def test_get_stats(self, client: AsyncClient, auth_headers: dict):
        """测试获取统计数据"""
        response = await client.get(
            "/api/dashboard/stats",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "active_projects" in data
        assert "today_tasks" in data
        assert "pending_procurement" in data
        assert "inventory_alerts" in data
    
    async def test_get_project_progress(self, client: AsyncClient, auth_headers: dict):
        """测试获取项目进度"""
        response = await client.get(
            "/api/dashboard/project-progress",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_get_task_distribution(self, client: AsyncClient, auth_headers: dict):
        """测试获取任务分布"""
        response = await client.get(
            "/api/dashboard/task-distribution",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_get_recent_activities(self, client: AsyncClient, auth_headers: dict):
        """测试获取最近活动"""
        response = await client.get(
            "/api/dashboard/recent-activities",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_dashboard_without_auth(self, client: AsyncClient):
        """测试未授权访问"""
        response = await client.get("/api/dashboard/stats")
        
        assert response.status_code == 401

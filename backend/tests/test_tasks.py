"""
任务管理模块测试
"""

import pytest
from httpx import AsyncClient


class TestTasks:
    """任务管理相关测试"""
    
    async def test_list_tasks(self, client: AsyncClient, auth_headers: dict):
        """测试获取任务列表"""
        response = await client.get(
            "/api/tasks",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_create_task(self, client: AsyncClient, auth_headers: dict):
        """测试创建任务"""
        task_data = {
            "project_id": 1,
            "task_no": "1.1",
            "name": "测试任务",
            "task_type": "design",
            "status": "not_started",
            "priority": "high",
            "plan_start": "2024-03-01",
            "plan_end": "2024-03-31",
            "planned_work_hours": 160
        }
        
        response = await client.post(
            "/api/tasks",
            json=task_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "测试任务"
    
    async def test_update_task(self, client: AsyncClient, auth_headers: dict):
        """测试更新任务"""
        update_data = {
            "name": "更新的任务名称",
            "progress_percent": 50,
            "status": "in_progress"
        }
        
        response = await client.put(
            "/api/tasks/1",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "更新的任务名称"
    
    async def test_report_work(self, client: AsyncClient, auth_headers: dict):
        """测试任务报工"""
        report_data = {
            "work_hours": 8,
            "progress_percent": 75,
            "description": "今日完成船体放样"
        }
        
        response = await client.post(
            "/api/tasks/1/report",
            json=report_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json()["message"] == "报工成功"
    
    async def test_delete_task(self, client: AsyncClient, auth_headers: dict):
        """测试删除任务"""
        # 先创建任务
        task_data = {
            "project_id": 1,
            "task_no": "1.99",
            "name": "待删除任务",
            "task_type": "design",
            "status": "not_started"
        }
        
        create_response = await client.post(
            "/api/tasks",
            json=task_data,
            headers=auth_headers
        )
        task_id = create_response.json()["id"]
        
        # 删除任务
        response = await client.delete(
            f"/api/tasks/{task_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    async def test_filter_tasks_by_project(
        self, client: AsyncClient, auth_headers: dict
    ):
        """测试按项目筛选任务"""
        response = await client.get(
            "/api/tasks?project_id=1",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_filter_tasks_by_status(
        self, client: AsyncClient, auth_headers: dict
    ):
        """测试按状态筛选任务"""
        response = await client.get(
            "/api/tasks?status=in_progress",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

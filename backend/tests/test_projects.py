"""
项目管理模块测试
"""

import pytest
from httpx import AsyncClient


class TestProjects:
    """项目管理相关测试"""
    
    async def test_list_projects(self, client: AsyncClient, auth_headers: dict):
        """测试获取项目列表"""
        response = await client.get(
            "/api/projects",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_create_project(self, client: AsyncClient, auth_headers: dict):
        """测试创建项目"""
        project_data = {
            "project_no": "YT-2024-TEST",
            "yacht_name": "测试游艇",
            "yacht_model": "TEST-50",
            "client_name": "测试客户",
            "status": "planning",
            "start_date": "2024-03-01",
            "planned_end": "2024-08-31",
            "total_budget": 5000000,
            "description": "测试项目"
        }
        
        response = await client.post(
            "/api/projects",
            json=project_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["project_no"] == "YT-2024-TEST"
        assert data["yacht_name"] == "测试游艇"
    
    async def test_create_project_duplicate_number(
        self, client: AsyncClient, auth_headers: dict
    ):
        """测试创建重复项目编号"""
        project_data = {
            "project_no": "YT-2024-TEST",
            "yacht_name": "重复项目",
            "yacht_model": "TEST-50",
            "status": "planning"
        }
        
        response = await client.post(
            "/api/projects",
            json=project_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
    
    async def test_get_project(self, client: AsyncClient, auth_headers: dict):
        """测试获取项目详情"""
        response = await client.get(
            "/api/projects/1",
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    async def test_update_project(self, client: AsyncClient, auth_headers: dict):
        """测试更新项目"""
        update_data = {
            "yacht_name": "更新的游艇名称",
            "status": "in_progress"
        }
        
        response = await client.put(
            "/api/projects/1",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["yacht_name"] == "更新的游艇名称"
    
    async def test_delete_project(self, client: AsyncClient, auth_headers: dict):
        """测试删除项目"""
        # 先创建项目
        project_data = {
            "project_no": "YT-2024-DELETE",
            "yacht_name": "待删除项目",
            "yacht_model": "TEST-50",
            "status": "planning"
        }
        
        create_response = await client.post(
            "/api/projects",
            json=project_data,
            headers=auth_headers
        )
        project_id = create_response.json()["id"]
        
        # 删除项目
        response = await client.delete(
            f"/api/projects/{project_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    async def test_filter_projects_by_status(
        self, client: AsyncClient, auth_headers: dict
    ):
        """测试按状态筛选项目"""
        response = await client.get(
            "/api/projects?status=planning",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

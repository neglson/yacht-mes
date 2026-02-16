"""
物料和库存模块测试
"""

import pytest
from httpx import AsyncClient


class TestMaterials:
    """物料管理相关测试"""
    
    async def test_list_materials(self, client: AsyncClient, auth_headers: dict):
        """测试获取物料列表"""
        response = await client.get(
            "/api/materials",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_create_material(self, client: AsyncClient, auth_headers: dict):
        """测试创建物料"""
        material_data = {
            "code": "TEST-001",
            "name": "测试物料",
            "brand": "测试品牌",
            "model": "TEST-MODEL",
            "unit": "个",
            "supplier": "测试供应商",
            "unit_cost": 100.00,
            "min_stock": 10
        }
        
        response = await client.post(
            "/api/materials",
            json=material_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "测试物料"
    
    async def test_update_material(self, client: AsyncClient, auth_headers: dict):
        """测试更新物料"""
        update_data = {
            "name": "更新的物料名称",
            "unit_cost": 150.00
        }
        
        response = await client.put(
            "/api/materials/1",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    async def test_delete_material(self, client: AsyncClient, auth_headers: dict):
        """测试删除物料"""
        # 先创建物料
        material_data = {
            "code": "TEST-DELETE",
            "name": "待删除物料",
            "unit": "个"
        }
        
        create_response = await client.post(
            "/api/materials",
            json=material_data,
            headers=auth_headers
        )
        material_id = create_response.json()["id"]
        
        # 删除物料
        response = await client.delete(
            f"/api/materials/{material_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200


class TestInventory:
    """库存管理相关测试"""
    
    async def test_list_inventory(self, client: AsyncClient, auth_headers: dict):
        """测试获取库存列表"""
        response = await client.get(
            "/api/inventory",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_inventory_in(self, client: AsyncClient, auth_headers: dict):
        """测试入库操作"""
        transaction_data = {
            "material_id": 1,
            "type": "in",
            "quantity": 100,
            "warehouse": "main",
            "location": "A-01-01",
            "batch_no": "20240301-001",
            "remark": "测试入库"
        }
        
        response = await client.post(
            "/api/inventory/transaction",
            json=transaction_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "操作成功"
    
    async def test_inventory_out(self, client: AsyncClient, auth_headers: dict):
        """测试出库操作"""
        # 先入库
        in_data = {
            "material_id": 1,
            "type": "in",
            "quantity": 100,
            "warehouse": "main"
        }
        await client.post(
            "/api/inventory/transaction",
            json=in_data,
            headers=auth_headers
        )
        
        # 再出库
        out_data = {
            "material_id": 1,
            "type": "out",
            "quantity": 50,
            "warehouse": "main",
            "remark": "测试出库"
        }
        
        response = await client.post(
            "/api/inventory/transaction",
            json=out_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "操作成功"
    
    async def test_inventory_out_insufficient(
        self, client: AsyncClient, auth_headers: dict
    ):
        """测试库存不足"""
        out_data = {
            "material_id": 999,
            "type": "out",
            "quantity": 9999,
            "warehouse": "main"
        }
        
        response = await client.post(
            "/api/inventory/transaction",
            json=out_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
    
    async def test_inventory_logs(self, client: AsyncClient, auth_headers: dict):
        """测试获取库存日志"""
        response = await client.get(
            "/api/inventory/logs",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    async def test_inventory_alerts(self, client: AsyncClient, auth_headers: dict):
        """测试库存预警"""
        response = await client.get(
            "/api/inventory/alerts",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

"""
数据导入模块测试
"""

import pytest
from httpx import AsyncClient
import io


class TestImport:
    """数据导入相关测试"""
    
    async def test_import_excel(self, client: AsyncClient, auth_headers: dict):
        """测试 Excel 导入"""
        # 创建测试 Excel 文件
        import pandas as pd
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 部门表
            pd.DataFrame({
                '部门名称': ['测试部门'],
                '部门编码': ['TEST-DEPT'],
                '描述': ['测试用部门']
            }).to_excel(writer, sheet_name='部门', index=False)
            
            # 用户表
            pd.DataFrame({
                '用户名': ['testimport'],
                '姓名': ['导入测试用户'],
                '电话': ['13800138000'],
                '邮箱': ['test@import.com'],
                '角色': ['工人'],
                '部门': ['测试部门']
            }).to_excel(writer, sheet_name='用户', index=False)
        
        output.seek(0)
        
        files = {
            'file': ('test_import.xlsx', output, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        
        response = await client.post(
            "/api/import/excel",
            files=files,
            headers={**auth_headers, "Content-Type": "multipart/form-data"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "imported" in data
    
    async def test_import_excel_invalid_format(
        self, client: AsyncClient, auth_headers: dict
    ):
        """测试导入无效格式文件"""
        files = {
            'file': ('test.txt', io.BytesIO(b'invalid content'), 'text/plain')
        }
        
        response = await client.post(
            "/api/import/excel",
            files=files,
            headers=auth_headers
        )
        
        assert response.status_code == 400
    
    async def test_import_excel_without_permission(self, client: AsyncClient):
        """测试无权限导入"""
        files = {
            'file': ('test.xlsx', io.BytesIO(b'content'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        
        response = await client.post(
            "/api/import/excel",
            files=files
        )
        
        assert response.status_code == 401

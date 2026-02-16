"""
数据导入 API
用于从 Excel 导入初始数据
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List
import tempfile
import os

from app.database import get_db
from app.utils.excel_importer import import_from_excel
from app.utils.security import check_permission
from app.services.import_service import ImportService

router = APIRouter()


@router.post("/excel")
async def import_excel(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """
    从 Excel 文件导入数据
    
    支持导入：
    - 项目信息
    - 任务时间轴
    - 物料清单
    - 采购订单
    - 部门/班组/用户
    """
    # 检查文件类型
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="只支持 .xlsx 或 .xls 文件")
    
    # 保存临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        # 解析 Excel
        result = import_from_excel(tmp_path)
        
        # 执行导入
        service = ImportService(db)
        import_result = await service.import_all(result)
        
        return {
            "message": "数据导入成功" if import_result['success'] else "数据导入完成，但有错误",
            "imported": import_result['imported'],
            "errors": import_result['errors'],
            "preview": {
                "projects": len(result['projects']),
                "tasks": len(result['tasks']),
                "materials": len(result['materials']),
                "procurement": len(result['procurement']),
                "departments": len(result['departments']),
                "teams": len(result['teams']),
                "users": len(result['users'])
            },
            "sample_data": {
                "projects": result['projects'][:2] if result['projects'] else [],
                "tasks": result['tasks'][:2] if result['tasks'] else [],
                "materials": result['materials'][:2] if result['materials'] else []
            }
        }
        
    finally:
        # 清理临时文件
        os.unlink(tmp_path)


@router.get("/template")
async def download_template():
    """下载数据导入模板"""
    return {"message": "请使用 data_template.xlsx 作为模板"}

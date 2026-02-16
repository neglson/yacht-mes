"""
物料管理 API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.database import get_db
from app.models import Material, MaterialCategory, Inventory
from app.utils.security import check_permission, get_current_user

router = APIRouter()


@router.get("")
async def list_materials(
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    keyword: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取物料列表"""
    query = select(Material)
    
    if category_id:
        query = query.where(Material.cat_id == category_id)
    if keyword:
        query = query.where(
            Material.name.contains(keyword) | 
            Material.code.contains(keyword)
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    materials = result.scalars().all()
    
    # 获取库存信息
    material_list = []
    for material in materials:
        # 计算总库存
        inventory_result = await db.execute(
            select(func.sum(Inventory.quantity))
            .where(Inventory.material_id == material.id)
        )
        total_stock = inventory_result.scalar() or 0
        
        material_dict = {
            "id": material.id,
            "code": material.code,
            "name": material.name,
            "brand": material.brand,
            "model": material.model,
            "specification": material.specification,
            "unit": material.unit,
            "supplier": material.supplier,
            "unit_cost": float(material.unit_cost) if material.unit_cost else None,
            "min_stock": float(material.min_stock) if material.min_stock else 0,
            "stock": float(total_stock)
        }
        material_list.append(material_dict)
    
    return material_list


@router.post("")
async def create_material(
    material_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("dept_manager"))
):
    """创建物料"""
    material = Material(**material_data)
    db.add(material)
    await db.commit()
    await db.refresh(material)
    return material


@router.get("/{material_id}")
async def get_material(
    material_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取物料详情"""
    result = await db.execute(select(Material).where(Material.id == material_id))
    material = result.scalar_one_or_none()
    
    if not material:
        raise HTTPException(status_code=404, detail="物料不存在")
    
    return material


@router.put("/{material_id}")
async def update_material(
    material_id: int,
    material_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("dept_manager"))
):
    """更新物料"""
    result = await db.execute(select(Material).where(Material.id == material_id))
    material = result.scalar_one_or_none()
    
    if not material:
        raise HTTPException(status_code=404, detail="物料不存在")
    
    for field, value in material_data.items():
        setattr(material, field, value)
    
    await db.commit()
    await db.refresh(material)
    return material


@router.delete("/{material_id}")
async def delete_material(
    material_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """删除物料"""
    result = await db.execute(select(Material).where(Material.id == material_id))
    material = result.scalar_one_or_none()
    
    if not material:
        raise HTTPException(status_code=404, detail="物料不存在")
    
    await db.delete(material)
    await db.commit()
    
    return {"message": "物料已删除"}

"""
库存管理 API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.database import get_db
from app.models import Inventory, InventoryLog, Material
from app.utils.security import check_permission, get_current_user

router = APIRouter()


@router.get("")
async def list_inventory(
    skip: int = 0,
    limit: int = 100,
    material_id: int = None,
    warehouse: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取库存列表"""
    query = select(Inventory)
    
    if material_id:
        query = query.where(Inventory.material_id == material_id)
    if warehouse:
        query = query.where(Inventory.warehouse == warehouse)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    inventory_items = result.scalars().all()
    
    return inventory_items


@router.post("/transaction")
async def inventory_transaction(
    transaction_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("team_leader"))
):
    """库存出入库操作"""
    material_id = transaction_data.get("material_id")
    transaction_type = transaction_data.get("type")  # in, out
    quantity = transaction_data.get("quantity")
    
    # 查找或创建库存记录
    result = await db.execute(
        select(Inventory).where(
            Inventory.material_id == material_id,
            Inventory.warehouse == transaction_data.get("warehouse", "main")
        )
    )
    inventory = result.scalar_one_or_none()
    
    if not inventory:
        inventory = Inventory(
            material_id=material_id,
            warehouse=transaction_data.get("warehouse", "main"),
            location=transaction_data.get("location"),
            quantity=0
        )
        db.add(inventory)
        await db.flush()
    
    # 记录操作前数量
    before_qty = inventory.quantity
    
    # 更新库存
    if transaction_type == "in":
        inventory.quantity += quantity
    elif transaction_type == "out":
        if inventory.quantity < quantity:
            raise HTTPException(status_code=400, detail="库存不足")
        inventory.quantity -= quantity
    
    # 创建库存日志
    log = InventoryLog(
        material_id=material_id,
        inventory_id=inventory.id,
        type=transaction_type,
        quantity=quantity,
        before_qty=before_qty,
        after_qty=inventory.quantity,
        related_task_id=transaction_data.get("related_task_id"),
        operator_id=current_user.get("id"),
        operator_name=current_user.get("username"),
        remark=transaction_data.get("remark")
    )
    db.add(log)
    
    await db.commit()
    
    return {
        "message": "操作成功",
        "inventory": {
            "material_id": material_id,
            "quantity": inventory.quantity
        }
    }


@router.get("/logs")
async def list_inventory_logs(
    skip: int = 0,
    limit: int = 100,
    material_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取库存操作日志"""
    query = select(InventoryLog).order_by(InventoryLog.created_at.desc())
    
    if material_id:
        query = query.where(InventoryLog.material_id == material_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()
    
    return logs


@router.get("/alerts")
async def inventory_alerts(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取库存预警"""
    # 查询库存低于安全线的物料
    result = await db.execute(
        select(Material, func.sum(Inventory.quantity).label("total_stock"))
        .outerjoin(Inventory, Material.id == Inventory.material_id)
        .group_by(Material.id)
        .having(func.sum(Inventory.quantity) < Material.min_stock)
    )
    
    alerts = []
    for material, total_stock in result.all():
        alerts.append({
            "material_id": material.id,
            "material_name": material.name,
            "material_code": material.code,
            "current_stock": float(total_stock or 0),
            "min_stock": float(material.min_stock),
            "shortage": float(material.min_stock - (total_stock or 0))
        })
    
    return alerts

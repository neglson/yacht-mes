"""
采购管理 API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import ProcurementOrder
from app.utils.security import check_permission, get_current_user

router = APIRouter()


@router.get("")
async def list_procurement(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    project_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取采购订单列表"""
    query = select(ProcurementOrder)
    
    if status:
        query = query.where(ProcurementOrder.status == status)
    if project_id:
        query = query.where(ProcurementOrder.project_id == project_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    orders = result.scalars().all()
    
    return orders


@router.post("")
async def create_procurement(
    order_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("team_leader"))
):
    """创建采购申请"""
    order = ProcurementOrder(
        **order_data,
        created_by=current_user.get("id")
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@router.get("/{order_id}")
async def get_procurement(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取采购订单详情"""
    result = await db.execute(
        select(ProcurementOrder).where(ProcurementOrder.id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="采购订单不存在")
    
    return order


@router.put("/{order_id}/approve")
async def approve_procurement(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("dept_manager"))
):
    """审批采购订单"""
    result = await db.execute(
        select(ProcurementOrder).where(ProcurementOrder.id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="采购订单不存在")
    
    order.status = "approved"
    order.approver_id = current_user.get("id")
    from datetime import datetime
    order.approved_at = datetime.now()
    
    await db.commit()
    
    return {"message": "审批通过"}


@router.put("/{order_id}/status")
async def update_procurement_status(
    order_id: int,
    status_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("team_leader"))
):
    """更新采购订单状态"""
    result = await db.execute(
        select(ProcurementOrder).where(ProcurementOrder.id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(status_code=404, detail="采购订单不存在")
    
    order.status = status_data.get("status")
    await db.commit()
    
    return {"message": "状态已更新"}

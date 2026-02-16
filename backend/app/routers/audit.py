"""
审计日志 API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.services.audit_service import AuditService
from app.utils.security import check_permission, get_current_user

router = APIRouter()


@router.get("")
async def list_audit_logs(
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """获取审计日志列表（仅管理员）"""
    service = AuditService(db)
    logs = await service.get_logs(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return logs


@router.get("/my-activity")
async def get_my_activity(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取当前用户活动摘要"""
    service = AuditService(db)
    summary = await service.get_user_activity_summary(
        user_id=current_user["id"],
        days=days
    )
    return summary


@router.get("/stats")
async def get_audit_stats(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """获取审计统计（仅管理员）"""
    from sqlalchemy import func, select
    from datetime import timedelta
    from app.models import AuditLog
    
    start_date = datetime.now() - timedelta(days=days)
    
    # 总操作数
    total_result = await db.execute(
        select(func.count(AuditLog.id))
        .where(AuditLog.created_at >= start_date)
    )
    total_count = total_result.scalar()
    
    # 按操作类型统计
    action_result = await db.execute(
        select(AuditLog.action, func.count(AuditLog.id))
        .where(AuditLog.created_at >= start_date)
        .group_by(AuditLog.action)
    )
    action_stats = {action: count for action, count in action_result.all()}
    
    # 按资源类型统计
    resource_result = await db.execute(
        select(AuditLog.resource_type, func.count(AuditLog.id))
        .where(AuditLog.created_at >= start_date)
        .group_by(AuditLog.resource_type)
    )
    resource_stats = {rt: count for rt, count in resource_result.all()}
    
    # 活跃用户
    active_users_result = await db.execute(
        select(AuditLog.username, func.count(AuditLog.id))
        .where(AuditLog.created_at >= start_date)
        .group_by(AuditLog.username)
        .order_by(func.count(AuditLog.id).desc())
        .limit(10)
    )
    active_users = [{"username": u, "count": c} for u, c in active_users_result.all()]
    
    return {
        "total_operations": total_count,
        "action_stats": action_stats,
        "resource_stats": resource_stats,
        "active_users": active_users,
        "period_days": days
    }

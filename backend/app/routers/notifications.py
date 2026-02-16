"""
通知 API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.services.notification_service import NotificationService
from app.utils.security import get_current_user

router = APIRouter()


@router.get("")
async def list_notifications(
    is_read: Optional[bool] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取通知列表"""
    service = NotificationService(db)
    notifications = await service.get_user_notifications(
        user_id=current_user["id"],
        is_read=is_read,
        limit=limit
    )
    return notifications


@router.get("/unread-count")
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取未读通知数量"""
    service = NotificationService(db)
    count = await service.get_unread_count(current_user["id"])
    return {"count": count}


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """标记通知为已读"""
    service = NotificationService(db)
    success = await service.mark_as_read(notification_id, current_user["id"])
    
    if not success:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    return {"message": "已标记为已读"}


@router.post("/read-all")
async def mark_all_as_read(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """标记所有通知为已读"""
    service = NotificationService(db)
    await service.mark_all_as_read(current_user["id"])
    return {"message": "所有通知已标记为已读"}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除通知"""
    service = NotificationService(db)
    success = await service.delete_notification(notification_id, current_user["id"])
    
    if not success:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    return {"message": "通知已删除"}

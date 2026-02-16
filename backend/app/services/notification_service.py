"""
通知服务
支持多种通知渠道
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models import Notification, User
from app.utils.cache import cache


class NotificationService:
    """通知服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_notification(
        self,
        user_id: int,
        title: str,
        content: str,
        type: str = "info",
        category: str = "system",
        related_type: Optional[str] = None,
        related_id: Optional[int] = None
    ) -> Notification:
        """创建通知"""
        notification = Notification(
            user_id=user_id,
            title=title,
            content=content,
            type=type,
            category=category,
            related_type=related_type,
            related_id=related_id,
            is_read=False,
            pushed=False
        )
        
        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)
        
        # 清除用户未读通知缓存
        await cache.delete(f"notifications:unread:{user_id}")
        
        return notification
    
    async def get_user_notifications(
        self,
        user_id: int,
        is_read: Optional[bool] = None,
        limit: int = 50
    ) -> List[Notification]:
        """获取用户通知"""
        query = select(Notification).where(Notification.user_id == user_id)
        
        if is_read is not None:
            query = query.where(Notification.is_read == is_read)
        
        query = query.order_by(Notification.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        
        return result.scalars().all()
    
    async def get_unread_count(self, user_id: int) -> int:
        """获取未读通知数量"""
        # 尝试从缓存获取
        cache_key = f"notifications:unread:{user_id}"
        cached_count = await cache.get(cache_key)
        
        if cached_count is not None:
            return cached_count
        
        # 查询数据库
        result = await self.db.execute(
            select(Notification).where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False
                )
            )
        )
        count = len(result.scalars().all())
        
        # 缓存结果（5分钟）
        await cache.set(cache_key, count, expire=300)
        
        return count
    
    async def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        """标记通知为已读"""
        result = await self.db.execute(
            select(Notification).where(
                and_(
                    Notification.id == notification_id,
                    Notification.user_id == user_id
                )
            )
        )
        notification = result.scalar_one_or_none()
        
        if not notification:
            return False
        
        notification.is_read = True
        notification.read_at = datetime.now()
        
        await self.db.commit()
        
        # 清除缓存
        await cache.delete(f"notifications:unread:{user_id}")
        
        return True
    
    async def mark_all_as_read(self, user_id: int):
        """标记所有通知为已读"""
        result = await self.db.execute(
            select(Notification).where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False
                )
            )
        )
        notifications = result.scalars().all()
        
        now = datetime.now()
        for notification in notifications:
            notification.is_read = True
            notification.read_at = now
        
        await self.db.commit()
        
        # 清除缓存
        await cache.delete(f"notifications:unread:{user_id}")
    
    async def delete_notification(self, notification_id: int, user_id: int) -> bool:
        """删除通知"""
        result = await self.db.execute(
            select(Notification).where(
                and_(
                    Notification.id == notification_id,
                    Notification.user_id == user_id
                )
            )
        )
        notification = result.scalar_one_or_none()
        
        if not notification:
            return False
        
        await self.db.delete(notification)
        await self.db.commit()
        
        # 清除缓存
        await cache.delete(f"notifications:unread:{user_id}")
        
        return True
    
    # 快捷方法
    async def notify_task_assigned(
        self,
        user_id: int,
        task_name: str,
        task_id: int
    ):
        """任务分配通知"""
        await self.create_notification(
            user_id=user_id,
            title="新任务分配",
            content=f"您被分配了新任务：{task_name}",
            type="info",
            category="task",
            related_type="task",
            related_id=task_id
        )
    
    async def notify_task_delayed(
        self,
        user_id: int,
        task_name: str,
        delay_days: int,
        task_id: int
    ):
        """任务延期通知"""
        await self.create_notification(
            user_id=user_id,
            title="任务延期提醒",
            content=f"任务「{task_name}」已延期 {delay_days} 天",
            type="warning",
            category="task",
            related_type="task",
            related_id=task_id
        )
    
    async def notify_procurement_approved(
        self,
        user_id: int,
        order_no: str,
        order_id: int
    ):
        """采购审批通过通知"""
        await self.create_notification(
            user_id=user_id,
            title="采购申请已审批",
            content=f"您的采购申请 {order_no} 已通过审批",
            type="success",
            category="procurement",
            related_type="procurement",
            related_id=order_id
        )
    
    async def notify_inventory_alert(
        self,
        user_id: int,
        material_name: str,
        current_stock: float,
        min_stock: float
    ):
        """库存预警通知"""
        await self.create_notification(
            user_id=user_id,
            title="库存预警",
            content=f"物料「{material_name}」库存不足（当前：{current_stock}，最低：{min_stock}）",
            type="error",
            category="inventory"
        )
    
    async def notify_work_report_reminder(self, user_id: int):
        """报工提醒"""
        await self.create_notification(
            user_id=user_id,
            title="报工提醒",
            content="您有今日完成的任务尚未报工，请及时填写",
            type="info",
            category="task"
        )

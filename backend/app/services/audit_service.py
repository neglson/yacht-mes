"""
审计日志服务
记录系统操作日志
"""

from typing import Optional, Any, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import Request

from app.models import AuditLog


class AuditService:
    """审计日志服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def log(
        self,
        user_id: Optional[int],
        username: Optional[str],
        action: str,
        resource_type: str,
        resource_id: Optional[int] = None,
        before_data: Optional[Dict] = None,
        after_data: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """记录审计日志"""
        log = AuditLog(
            user_id=user_id,
            username=username,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            before_data=before_data,
            after_data=after_data,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.now()
        )
        
        self.db.add(log)
        await self.db.commit()
    
    async def log_from_request(
        self,
        request: Request,
        action: str,
        resource_type: str,
        resource_id: Optional[int] = None,
        before_data: Optional[Dict] = None,
        after_data: Optional[Dict] = None
    ):
        """从请求记录审计日志"""
        # 获取用户信息
        user_id = None
        username = None
        if hasattr(request.state, 'user'):
            user_id = request.state.user.get('id')
            username = request.state.user.get('username')
        
        # 获取 IP 地址
        ip_address = self._get_client_ip(request)
        
        # 获取 User-Agent
        user_agent = request.headers.get('user-agent')
        
        await self.log(
            user_id=user_id,
            username=username,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            before_data=before_data,
            after_data=after_data,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def _get_client_ip(self, request: Request) -> str:
        """获取客户端 IP"""
        if 'x-forwarded-for' in request.headers:
            return request.headers['x-forwarded-for'].split(',')[0].strip()
        elif 'x-real-ip' in request.headers:
            return request.headers['x-real-ip']
        else:
            return request.client.host if request.client else 'unknown'
    
    async def get_logs(
        self,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ):
        """获取审计日志"""
        query = select(AuditLog).order_by(AuditLog.created_at.desc())
        
        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        if action:
            query = query.where(AuditLog.action == action)
        if resource_type:
            query = query.where(AuditLog.resource_type == resource_type)
        if start_date:
            query = query.where(AuditLog.created_at >= start_date)
        if end_date:
            query = query.where(AuditLog.created_at <= end_date)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        
        return result.scalars().all()
    
    async def get_user_activity_summary(
        self,
        user_id: int,
        days: int = 7
    ) -> Dict[str, Any]:
        """获取用户活动摘要"""
        from datetime import timedelta
        
        start_date = datetime.now() - timedelta(days=days)
        
        # 总操作数
        total_result = await self.db.execute(
            select(func.count(AuditLog.id))
            .where(
                AuditLog.user_id == user_id,
                AuditLog.created_at >= start_date
            )
        )
        total_count = total_result.scalar()
        
        # 按操作类型统计
        action_result = await self.db.execute(
            select(AuditLog.action, func.count(AuditLog.id))
            .where(
                AuditLog.user_id == user_id,
                AuditLog.created_at >= start_date
            )
            .group_by(AuditLog.action)
        )
        action_stats = {action: count for action, count in action_result.all()}
        
        # 按资源类型统计
        resource_result = await self.db.execute(
            select(AuditLog.resource_type, func.count(AuditLog.id))
            .where(
                AuditLog.user_id == user_id,
                AuditLog.created_at >= start_date
            )
            .group_by(AuditLog.resource_type)
        )
        resource_stats = {rt: count for rt, count in resource_result.all()}
        
        return {
            "total_operations": total_count,
            "action_stats": action_stats,
            "resource_stats": resource_stats,
            "period_days": days
        }


# 快捷装饰器
def audit_log(action: str, resource_type: str):
    """
    审计日志装饰器
    
    用法:
        @audit_log("create", "task")
        async def create_task(...)
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 获取 request 和 db
            request = kwargs.get('request')
            db = kwargs.get('db')
            
            # 执行原函数
            result = await func(*args, **kwargs)
            
            # 记录日志
            if request and db:
                audit_service = AuditService(db)
                await audit_service.log_from_request(
                    request=request,
                    action=action,
                    resource_type=resource_type,
                    resource_id=getattr(result, 'id', None)
                )
            
            return result
        
        return wrapper
    return decorator

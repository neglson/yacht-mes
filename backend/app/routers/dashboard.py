"""
仪表盘 API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.database import get_db
from app.models import Project, Task, Material, ProcurementOrder, User
from app.utils.security import get_current_user

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取仪表盘统计数据"""
    
    # 项目统计
    project_result = await db.execute(
        select(func.count(Project.id)).where(Project.status == "in_progress")
    )
    active_projects = project_result.scalar()
    
    # 今日任务
    today = datetime.now().date()
    task_result = await db.execute(
        select(func.count(Task.id))
        .where(Task.plan_start <= today)
        .where(Task.plan_end >= today)
    )
    today_tasks = task_result.scalar()
    
    # 待审批采购
    procurement_result = await db.execute(
        select(func.count(ProcurementOrder.id))
        .where(ProcurementOrder.status == "pending_approval")
    )
    pending_procurement = procurement_result.scalar()
    
    # 库存预警
    from app.models import Inventory
    material_result = await db.execute(
        select(func.count(Material.id))
        .outerjoin(Inventory, Material.id == Inventory.material_id)
        .group_by(Material.id)
        .having(func.sum(Inventory.quantity) < Material.min_stock)
    )
    inventory_alerts = len(material_result.all())
    
    return {
        "active_projects": active_projects,
        "today_tasks": today_tasks,
        "pending_procurement": pending_procurement,
        "inventory_alerts": inventory_alerts
    }


@router.get("/project-progress")
async def get_project_progress(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取项目进度数据"""
    result = await db.execute(
        select(Project.id, Project.yacht_name, Project.status)
        .where(Project.status.in_(["in_progress", "planning"]))
        .limit(5)
    )
    projects = result.all()
    
    progress_data = []
    for project_id, yacht_name, status in projects:
        # 计算项目进度
        task_result = await db.execute(
            select(func.avg(Task.progress_percent))
            .where(Task.project_id == project_id)
        )
        avg_progress = task_result.scalar() or 0
        
        progress_data.append({
            "name": yacht_name,
            "progress": round(avg_progress, 1),
            "status": status
        })
    
    return progress_data


@router.get("/task-distribution")
async def get_task_distribution(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取任务状态分布"""
    result = await db.execute(
        select(Task.status, func.count(Task.id))
        .group_by(Task.status)
    )
    
    distribution = []
    status_map = {
        "not_started": "未开始",
        "in_progress": "进行中",
        "completed": "已完成",
        "delayed": "延期"
    }
    
    for status, count in result.all():
        distribution.append({
            "name": status_map.get(status, status),
            "value": count
        })
    
    return distribution


@router.get("/recent-activities")
async def get_recent_activities(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取最近活动"""
    # 这里简化处理，实际应该从操作日志中获取
    return [
        {
            "type": "task",
            "title": "任务完成",
            "description": "飞桥结构设计审核已完成",
            "time": "10分钟前"
        },
        {
            "type": "procurement",
            "title": "采购审批",
            "description": "新的采购申请待审批",
            "time": "30分钟前"
        },
        {
            "type": "inventory",
            "title": "库存预警",
            "description": "铝合金焊丝库存低于安全线",
            "time": "1小时前"
        }
    ]

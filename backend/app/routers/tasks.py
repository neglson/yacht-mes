"""
任务管理 API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import Task, Project
from app.schemas.project import TaskCreate, TaskUpdate, TaskResponse, TaskWorkReport
from app.utils.security import check_permission, get_current_user

router = APIRouter()


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    status: str = None,
    manager_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取任务列表"""
    query = select(Task)
    
    if project_id:
        query = query.where(Task.project_id == project_id)
    if status:
        query = query.where(Task.status == status)
    if manager_id:
        query = query.where(Task.manager_id == manager_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    # 转换为响应格式
    task_list = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "project_id": task.project_id,
            "task_no": task.task_no,
            "name": task.name,
            "task_type": task.task_type,
            "status": task.status,
            "priority": task.priority,
            "plan_start": task.plan_start,
            "plan_end": task.plan_end,
            "actual_start": task.actual_start,
            "actual_end": task.actual_end,
            "planned_work_hours": task.planned_work_hours,
            "actual_work_hours": task.actual_work_hours,
            "progress_percent": task.progress_percent,
            "delay_days": task.delay_days,
            "delay_reason": task.delay_reason,
            "manager_id": task.manager_id,
            "manager_name": task.manager.real_name if task.manager else None,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
        task_list.append(task_dict)
    
    return task_list


@router.post("", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("team_leader"))
):
    """创建任务"""
    db_task = Task(
        project_id=task.project_id,
        task_no=task.task_no,
        name=task.name,
        task_type=task.task_type,
        status=task.status,
        priority=task.priority,
        plan_start=task.plan_start,
        plan_end=task.plan_end,
        planned_work_hours=task.planned_work_hours,
        manager_id=task.manager_id,
        parent_id=task.parent_id
    )
    
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    
    return db_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取任务详情"""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("team_leader"))
):
    """更新任务"""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 乐观锁检查
    if task_update.version and task.version != task_update.version:
        raise HTTPException(status_code=409, detail="任务已被他人修改，请刷新后重试")
    
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field != "version":
            setattr(task, field, value)
    
    task.version += 1
    
    await db.commit()
    await db.refresh(task)
    
    return task


@router.post("/{task_id}/report")
async def report_work(
    task_id: int,
    report: TaskWorkReport,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """任务报工"""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 更新实际工时和进度
    task.actual_work_hours = (task.actual_work_hours or 0) + report.work_hours
    task.progress_percent = report.progress_percent
    
    if report.progress_percent == 100:
        task.status = "completed"
        from datetime import datetime
        task.actual_end = datetime.now()
    elif report.progress_percent > 0:
        task.status = "in_progress"
        if not task.actual_start:
            from datetime import datetime
            task.actual_start = datetime.now()
    
    await db.commit()
    
    return {"message": "报工成功"}


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("dept_manager"))
):
    """删除任务"""
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    await db.delete(task)
    await db.commit()
    
    return {"message": "任务已删除"}

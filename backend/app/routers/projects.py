"""
项目管理 API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.database import get_db
from app.models import Project, Task
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.utils.security import check_permission, get_current_user

router = APIRouter()


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取项目列表"""
    query = select(Project)
    
    if status:
        query = query.where(Project.status == status)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    projects = result.scalars().all()
    
    # 计算统计信息
    project_list = []
    for project in projects:
        # 获取任务统计
        tasks_result = await db.execute(
            select(func.count(Task.id), func.sum(Task.progress_percent))
            .where(Task.project_id == project.id)
        )
        task_count, total_progress = tasks_result.first()
        
        project_dict = {
            "id": project.id,
            "project_no": project.project_no,
            "yacht_name": project.yacht_name,
            "yacht_model": project.yacht_model,
            "client_name": project.client_name,
            "status": project.status,
            "start_date": project.start_date,
            "planned_end": project.planned_end,
            "actual_end": project.actual_end,
            "total_budget": project.total_budget,
            "description": project.description,
            "created_by": project.created_by,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "total_tasks": task_count or 0,
            "completed_tasks": 0,  # TODO: 计算已完成任务数
            "progress_percent": int((total_progress or 0) / (task_count or 1))
        }
        project_list.append(project_dict)
    
    return project_list


@router.post("", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("dept_manager"))
):
    """创建项目"""
    # 检查项目编号是否已存在
    result = await db.execute(
        select(Project).where(Project.project_no == project.project_no)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="项目编号已存在")
    
    db_project = Project(
        project_no=project.project_no,
        yacht_name=project.yacht_name,
        yacht_model=project.yacht_model,
        client_name=project.client_name,
        status=project.status,
        start_date=project.start_date,
        planned_end=project.planned_end,
        total_budget=project.total_budget,
        description=project.description,
        created_by=current_user.get("id")
    )
    
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    
    return db_project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取项目详情"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("dept_manager"))
):
    """更新项目"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    await db.commit()
    await db.refresh(project)
    
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """删除项目"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    await db.delete(project)
    await db.commit()
    
    return {"message": "项目已删除"}

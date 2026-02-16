"""
Pydantic 数据模型 - 项目和任务
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class ProjectStatus(str, Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectBase(BaseModel):
    project_no: str = Field(..., min_length=1, max_length=50)
    yacht_name: str = Field(..., min_length=1, max_length=100)
    yacht_model: Optional[str] = None
    client_name: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    start_date: Optional[date] = None
    planned_end: Optional[date] = None
    total_budget: Optional[float] = None
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    yacht_name: Optional[str] = None
    yacht_model: Optional[str] = None
    client_name: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[date] = None
    planned_end: Optional[date] = None
    actual_end: Optional[date] = None
    total_budget: Optional[float] = None
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    actual_end: Optional[date] = None
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    # 统计字段
    total_tasks: Optional[int] = 0
    completed_tasks: Optional[int] = 0
    progress_percent: Optional[int] = 0
    
    class Config:
        from_attributes = True


class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(BaseModel):
    task_no: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=200)
    task_type: str  # 设计/船体制作/采购配料/舾装/内装/调试
    status: TaskStatus = TaskStatus.NOT_STARTED
    priority: TaskPriority = TaskPriority.MEDIUM
    
    plan_start: Optional[date] = None
    plan_end: Optional[date] = None
    duration_days: Optional[int] = None
    
    planned_work_hours: Optional[int] = None
    
    dept_id: Optional[int] = None
    team_id: Optional[int] = None
    manager_id: Optional[int] = None
    inspector_id: Optional[int] = None
    
    parent_id: Optional[int] = None
    level: int = 1
    
    progress_percent: int = Field(0, ge=0, le=100)
    delay_reason: Optional[str] = None


class TaskCreate(TaskBase):
    project_id: int
    dependencies: Optional[List[int]] = []


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    plan_start: Optional[date] = None
    plan_end: Optional[date] = None
    actual_start: Optional[date] = None
    actual_end: Optional[date] = None
    actual_work_hours: Optional[int] = None
    progress_percent: Optional[int] = Field(None, ge=0, le=100)
    delay_reason: Optional[str] = None
    manager_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    project_id: int
    actual_start: Optional[date] = None
    actual_end: Optional[date] = None
    actual_work_hours: int = 0
    delay_days: int = 0
    version: int = 1
    created_at: datetime
    updated_at: datetime
    
    # 关联信息
    project_name: Optional[str] = None
    dept_name: Optional[str] = None
    team_name: Optional[str] = None
    manager_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class TaskWorkReport(BaseModel):
    """工时上报"""
    work_hours: int = Field(..., gt=0)
    progress_percent: int = Field(..., ge=0, le=100)
    remark: Optional[str] = None
    photo_urls: Optional[List[str]] = []

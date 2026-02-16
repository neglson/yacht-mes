"""
SQLAlchemy 数据模型 - 项目和任务
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text, ARRAY, UniqueConstraint, JSON, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    project_no = Column(String(50), unique=True, nullable=False, index=True)
    yacht_name = Column(String(100), nullable=False)
    yacht_model = Column(String(100))
    client_name = Column(String(100))
    status = Column(String(20), default="planning")  # planning, in_progress, completed, cancelled
    
    start_date = Column(Date)
    planned_end = Column(Date)
    actual_end = Column(Date)
    
    total_budget = Column(Numeric(15, 2))
    description = Column(Text)
    
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    creator = relationship("User")


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    task_no = Column(String(20), nullable=False)
    name = Column(String(200), nullable=False)
    task_type = Column(String(50), nullable=False)  # design, hull_construction, procurement, outfitting, interior, commissioning
    status = Column(String(20), default="not_started")  # not_started, in_progress, completed, delayed, cancelled
    priority = Column(String(10), default="medium")  # low, medium, high, urgent
    
    plan_start = Column(Date)
    plan_end = Column(Date)
    actual_start = Column(Date)
    actual_end = Column(Date)
    duration_days = Column(Integer)
    
    planned_work_hours = Column(Integer)
    actual_work_hours = Column(Integer, default=0)
    
    dept_id = Column(Integer, ForeignKey("departments.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))
    inspector_id = Column(Integer, ForeignKey("users.id"))
    
    parent_id = Column(Integer, ForeignKey("tasks.id"))
    level = Column(Integer, default=1)
    dependencies = Column(ARRAY(Integer))
    
    progress_percent = Column(Integer, default=0)
    delay_reason = Column(Text)
    delay_days = Column(Integer, default=0)
    
    version = Column(Integer, default=1)  # 乐观锁
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    project = relationship("Project", back_populates="tasks")
    manager = relationship("User", foreign_keys=[manager_id])
    inspector = relationship("User", foreign_keys=[inspector_id])
    
    __table_args__ = (
        # 联合唯一约束
        UniqueConstraint('project_id', 'task_no', name='unique_project_task_no'),
    )

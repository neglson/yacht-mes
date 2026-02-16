"""
SQLAlchemy 数据模型 - 用户相关
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    code = Column(String(20), unique=True)
    leader_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    leader = relationship("User", foreign_keys=[leader_id], back_populates="led_department")
    teams = relationship("Team", back_populates="department")
    users = relationship("User", back_populates="department")


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    code = Column(String(20), unique=True)
    dept_id = Column(Integer, ForeignKey("departments.id"))
    leader_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    specialty = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    department = relationship("Department", back_populates="teams")
    leader = relationship("User", foreign_keys=[leader_id], back_populates="led_team")
    users = relationship("User", back_populates="team")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="worker")  # admin, dept_manager, team_leader, worker
    
    dept_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    
    real_name = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    avatar_url = Column(String(255))
    permissions = Column(JSON, default=dict)
    
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    department = relationship("Department", foreign_keys=[dept_id], back_populates="users")
    team = relationship("Team", foreign_keys=[team_id], back_populates="users")
    led_department = relationship("Department", foreign_keys="Department.leader_id", back_populates="leader")
    led_team = relationship("Team", foreign_keys="Team.leader_id", back_populates="leader")

"""
Pydantic 数据模型 - 用户相关
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    DEPT_MANAGER = "dept_manager"
    TEAM_LEADER = "team_leader"
    WORKER = "worker"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    real_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    role: UserRole = UserRole.WORKER
    dept_id: Optional[int] = None
    team_id: Optional[int] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    real_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    dept_id: Optional[int] = None
    team_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str] = None
    permissions: Dict[str, Any] = {}
    last_login_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class DepartmentBase(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    id: int
    leader_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TeamBase(BaseModel):
    name: str
    code: Optional[str] = None
    dept_id: int
    specialty: Optional[str] = None
    description: Optional[str] = None


class TeamResponse(TeamBase):
    id: int
    leader_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

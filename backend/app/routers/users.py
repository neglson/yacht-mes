"""
用户管理 API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import User, Department, Team
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.security import get_password_hash, check_permission, get_current_user

router = APIRouter()


@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    dept_id: int = None,
    role: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """获取用户列表"""
    query = select(User)
    
    if dept_id:
        query = query.where(User.dept_id == dept_id)
    if role:
        query = query.where(User.role == role)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    # 转换为响应格式
    user_list = []
    for user in users:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "real_name": user.real_name,
            "phone": user.phone,
            "email": user.email,
            "role": user.role,
            "dept_id": user.dept_id,
            "team_id": user.team_id,
            "dept_name": user.department.name if user.department else None,
            "team_name": user.team.name if user.team else None,
            "is_active": user.is_active,
            "last_login_at": user.last_login_at,
            "created_at": user.created_at
        }
        user_list.append(user_dict)
    
    return user_list


@router.post("", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """创建用户"""
    # 检查用户名是否已存在
    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    db_user = User(
        username=user.username,
        password_hash=get_password_hash(user.password),
        real_name=user.real_name,
        phone=user.phone,
        email=user.email,
        role=user.role,
        dept_id=user.dept_id,
        team_id=user.team_id,
        is_active=user.is_active
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取用户详情"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """更新用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """删除用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    await db.delete(user)
    await db.commit()
    
    return {"message": "用户已删除"}


@router.post("/{user_id}/reset-password")
async def reset_password(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(check_permission("admin"))
):
    """重置密码"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    user.password_hash = get_password_hash("123456")
    await db.commit()
    
    return {"message": "密码已重置为：123456"}

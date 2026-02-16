"""
认证路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from typing import Optional

from app.database import get_db
from app.schemas.user import UserLogin, Token, UserResponse
from app.utils.security import (
    verify_password, 
    create_access_token, 
    get_current_user,
    get_password_hash
)
from app.config import settings

router = APIRouter()

# 这里需要导入 User 模型
# from app.models.user import User


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """用户登录"""
    # TODO: 实现实际的数据库查询
    # result = await db.execute(select(User).where(User.username == form_data.username))
    # user = result.scalar_one_or_none()
    
    # 临时 mock 数据用于测试
    if form_data.username != "admin" or form_data.password != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "role": "admin"},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": {
            "id": 1,
            "username": form_data.username,
            "real_name": "管理员",
            "role": "admin",
            "is_active": True,
            "created_at": "2024-01-01T00:00:00"
        }
    }


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """用户登出"""
    # JWT 无状态，客户端删除 token 即可
    return {"message": "登出成功"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    # TODO: 返回实际用户数据
    return current_user


@router.post("/refresh")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """刷新访问令牌"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user["username"], "role": current_user.get("role", "worker")},
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

"""
附件管理 API
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os
import uuid
from datetime import datetime

from app.database import get_db
from app.config import settings
from app.utils.security import get_current_user

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    related_type: str = None,
    related_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """上传文件"""
    # 检查文件大小
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制")
    
    # 生成唯一文件名
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    
    # 保存文件
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # 保存到数据库
    from app.models import Attachment
    attachment = Attachment(
        file_name=file.filename,
        file_url=f"/uploads/{filename}",
        file_type=file.content_type,
        file_size=len(content),
        mime_type=file.content_type,
        related_type=related_type,
        related_id=related_id,
        uploaded_by=current_user.get("id"),
        uploaded_by_name=current_user.get("username"),
        uploaded_at=datetime.now()
    )
    db.add(attachment)
    await db.commit()
    await db.refresh(attachment)
    
    return {
        "id": attachment.id,
        "url": attachment.file_url,
        "name": attachment.file_name
    }


@router.get("")
async def list_attachments(
    related_type: str = None,
    related_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取附件列表"""
    from app.models import Attachment
    
    query = select(Attachment)
    
    if related_type:
        query = query.where(Attachment.related_type == related_type)
    if related_id:
        query = query.where(Attachment.related_id == related_id)
    
    query = query.order_by(Attachment.uploaded_at.desc())
    result = await db.execute(query)
    attachments = result.scalars().all()
    
    return attachments


@router.delete("/{attachment_id}")
async def delete_attachment(
    attachment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除附件"""
    from app.models import Attachment
    
    result = await db.execute(
        select(Attachment).where(Attachment.id == attachment_id)
    )
    attachment = result.scalar_one_or_none()
    
    if not attachment:
        raise HTTPException(status_code=404, detail="附件不存在")
    
    # 删除文件
    file_path = os.path.join(settings.UPLOAD_DIR, os.path.basename(attachment.file_url))
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # 删除数据库记录
    await db.delete(attachment)
    await db.commit()
    
    return {"message": "附件已删除"}

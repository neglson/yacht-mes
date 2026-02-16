from app.models.user import User, Department, Team
from app.models.project import Project, Task
from app.models.material import MaterialCategory, Material, ProcurementOrder, Inventory, InventoryLog, Attachment

# 从 schema.sql 导入其他模型
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, JSON
from datetime import datetime


class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    type = Column(String(20), default="info")  # info, warning, error, success
    category = Column(String(50))  # task_reminder, approval_required, system
    related_type = Column(String(50))
    related_id = Column(Integer)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    pushed = Column(Boolean, default=False)
    push_channel = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    username = Column(String(50))
    action = Column(String(50), nullable=False)  # create, update, delete, login, logout
    resource_type = Column(String(50))  # task, material, user, etc.
    resource_id = Column(Integer)
    before_data = Column(JSON)
    after_data = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


__all__ = [
    "User", "Department", "Team",
    "Project", "Task",
    "MaterialCategory", "Material", "ProcurementOrder", "Inventory", "InventoryLog", "Attachment",
    "Notification", "AuditLog"
]

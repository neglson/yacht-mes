"""
SQLAlchemy 数据模型 - 物料和库存
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric, ARRAY
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class MaterialCategory(Base):
    __tablename__ = "material_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    main_cat = Column(String(50), nullable=False)
    sub_cat = Column(String(50))
    code_prefix = Column(String(10))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    materials = relationship("Material", back_populates="category")


class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("material_categories.id"))
    code = Column(String(50), unique=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(50))
    model = Column(String(100))
    specification = Column(String(200))
    description = Column(Text)
    unit = Column(String(20), nullable=False)
    
    supplier = Column(String(100))
    supplier_contact = Column(String(100))
    
    min_stock = Column(Numeric(10, 2), default=0)
    max_stock = Column(Numeric(10, 2))
    safety_stock = Column(Numeric(10, 2), default=0)
    unit_cost = Column(Numeric(10, 2))
    
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(String(20), default="active")  # active, inactive, discontinued
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    category = relationship("MaterialCategory", back_populates="materials")
    inventory_items = relationship("Inventory", back_populates="material")


class ProcurementOrder(Base):
    __tablename__ = "procurement_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, nullable=False)
    
    material_id = Column(Integer, ForeignKey("materials.id"))
    material_name = Column(String(200))
    
    quantity = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(20))
    unit_price = Column(Numeric(10, 2))
    total_price = Column(Numeric(12, 2))
    
    supplier = Column(String(100))
    supplier_contact = Column(String(100))
    
    order_date = Column(DateTime)
    delivery_date = Column(DateTime)
    actual_delivery_date = Column(DateTime)
    
    status = Column(String(20), default="draft")  # draft, pending_approval, approved, ordered, partial_delivered, delivered, cancelled
    approver_id = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime)
    
    project_id = Column(Integer, ForeignKey("projects.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"))
    batch_no = Column(String(50))
    quantity = Column(Numeric(10, 2), default=0)
    
    warehouse = Column(String(50), nullable=False)
    location = Column(String(100))
    
    qc_status = Column(String(20), default="pending")  # pending, pass, fail, quarantine
    qc_report_url = Column(String(500))
    
    procurement_order_id = Column(Integer, ForeignKey("procurement_orders.id"))
    expiry_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    material = relationship("Material", back_populates="inventory_items")


class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"))
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    
    type = Column(String(10), nullable=False)  # in, out, adjust, transfer
    quantity = Column(Numeric(10, 2), nullable=False)
    before_qty = Column(Numeric(10, 2))
    after_qty = Column(Numeric(10, 2))
    
    related_task_id = Column(Integer, ForeignKey("tasks.id"))
    related_order_id = Column(Integer, ForeignKey("procurement_orders.id"))
    
    operator_id = Column(Integer, ForeignKey("users.id"))
    operator_name = Column(String(50))
    
    signature = Column(String(255))
    photo_urls = Column(ARRAY(String))
    remark = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class Attachment(Base):
    __tablename__ = "attachments"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_type = Column(String(50))
    file_size = Column(Integer)
    mime_type = Column(String(100))
    
    related_type = Column(String(50), nullable=False)
    related_id = Column(Integer, nullable=False)
    
    category = Column(String(50))
    tags = Column(ARRAY(String))
    meta_data = Column(JSON)
    
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_by_name = Column(String(50))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

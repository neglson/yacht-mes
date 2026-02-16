-- ============================================================
-- 铝合金电动游艇建造管理系统 (Yacht MES) - 数据库设计
-- 版本: 1.0.0
-- 创建时间: 2026-02-16
-- ============================================================

-- 启用必要扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- 全文搜索

-- ============================================================
-- 1. RBAC 权限体系（对应部门/班组表）
-- ============================================================

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL, -- 设计部、生产部、采购部等
    code VARCHAR(20) UNIQUE, -- 部门编码
    leader_id INTEGER, -- 部门负责人
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    dept_id INTEGER REFERENCES departments(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL, -- 铝合金班组、电气班组等
    code VARCHAR(20) UNIQUE, -- 班组编码
    leader_id INTEGER, -- 班组长
    specialty VARCHAR(100), -- 专业领域
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'dept_manager', 'team_leader', 'worker')),
    dept_id INTEGER REFERENCES departments(id),
    team_id INTEGER REFERENCES teams(id),
    real_name VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    avatar_url VARCHAR(255),
    permissions JSONB DEFAULT '{}', -- 细粒度权限
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 添加外键约束（解决循环依赖）
ALTER TABLE departments ADD CONSTRAINT fk_dept_leader 
    FOREIGN KEY (leader_id) REFERENCES users(id) ON DELETE SET NULL;
ALTER TABLE teams ADD CONSTRAINT fk_team_leader 
    FOREIGN KEY (leader_id) REFERENCES users(id) ON DELETE SET NULL;

-- ============================================================
-- 2. 建造时间轴管理（对应 Excel 时间轴）
-- ============================================================

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    project_no VARCHAR(50) UNIQUE NOT NULL, -- 项目编号
    yacht_name VARCHAR(100) NOT NULL,
    yacht_model VARCHAR(100), -- 船型
    client_name VARCHAR(100), -- 船东
    status VARCHAR(20) DEFAULT 'planning' CHECK (status IN ('planning', 'in_progress', 'completed', 'cancelled')),
    start_date DATE,
    planned_end DATE,
    actual_end DATE,
    total_budget DECIMAL(15,2), -- 总预算
    description TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    task_no VARCHAR(20) NOT NULL, -- 如 1.1, 2.2
    name VARCHAR(200) NOT NULL, -- 飞桥结构设计交付
    task_type VARCHAR(50) NOT NULL, -- 设计/船体制作/采购配料/舾装/内装/调试
    status VARCHAR(20) DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed', 'delayed', 'cancelled')),
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    
    -- 时间安排
    plan_start DATE,
    plan_end DATE,
    actual_start DATE,
    actual_end DATE,
    duration_days INTEGER, -- 计划工期
    
    -- 工时管理
    planned_work_hours INTEGER, -- 计划工时
    actual_work_hours INTEGER DEFAULT 0, -- 实际工时
    
    -- 负责人
    dept_id INTEGER REFERENCES departments(id),
    team_id INTEGER REFERENCES teams(id),
    manager_id INTEGER REFERENCES users(id), -- 负责人
    inspector_id INTEGER REFERENCES users(id), -- 验收人
    
    -- WBS 层级
    parent_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    level INTEGER DEFAULT 1, -- WBS 层级
    
    -- 依赖关系
    dependencies INTEGER[], -- 前置任务 ID 数组
    
    -- 进度
    progress_percent INTEGER DEFAULT 0 CHECK (progress_percent BETWEEN 0 AND 100),
    
    -- 延期记录
    delay_reason TEXT,
    delay_days INTEGER DEFAULT 0,
    
    -- 版本控制（乐观锁）
    version INTEGER DEFAULT 1,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 联合唯一约束
    UNIQUE(project_id, task_no)
);

-- 任务依赖关系表（更规范的关联）
CREATE TABLE task_dependencies (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    depends_on_task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    dependency_type VARCHAR(20) DEFAULT 'finish_to_start', -- finish_to_start, start_to_start, finish_to_finish, start_to_finish
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(task_id, depends_on_task_id)
);

-- ============================================================
-- 3. 物料与采购管理（对应物料采购表）
-- ============================================================

CREATE TABLE material_categories (
    id SERIAL PRIMARY KEY,
    main_cat VARCHAR(50) NOT NULL, -- 鋁合金、焊接材料
    sub_cat VARCHAR(50), -- 鋁板、焊絲
    code_prefix VARCHAR(10), -- 分类编码前缀
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    cat_id INTEGER REFERENCES material_categories(id),
    code VARCHAR(50) UNIQUE, -- 物料编码
    name VARCHAR(200) NOT NULL, -- 4mm板
    brand VARCHAR(50), -- CCS
    model VARCHAR(100), -- 5083-H116
    specification VARCHAR(200), -- 规格参数
    description TEXT,
    unit VARCHAR(20) NOT NULL, -- 平米、kg、个
    
    -- 供应商信息
    supplier VARCHAR(100),
    supplier_contact VARCHAR(100),
    
    -- 库存控制
    min_stock DECIMAL(10,2) DEFAULT 0, -- 最低库存
    max_stock DECIMAL(10,2), -- 最高库存
    safety_stock DECIMAL(10,2) DEFAULT 0, -- 安全库存
    
    -- 成本
    unit_cost DECIMAL(10,2), -- 单位成本
    
    -- 项目关联
    project_id INTEGER REFERENCES projects(id),
    
    -- 状态
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'discontinued')),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE procurement_orders (
    id SERIAL PRIMARY KEY,
    order_no VARCHAR(50) UNIQUE NOT NULL, -- 采购单号
    
    -- 物料信息
    material_id INTEGER REFERENCES materials(id),
    material_name VARCHAR(200), -- 冗余存储，防止物料被删除后丢失信息
    
    -- 数量价格
    quantity DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20),
    unit_price DECIMAL(10,2),
    total_price DECIMAL(12,2),
    
    -- 供应商
    supplier VARCHAR(100),
    supplier_contact VARCHAR(100),
    
    -- 时间
    order_date DATE,
    delivery_date DATE,
    actual_delivery_date DATE,
    
    -- 审批流程
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'pending_approval', 'approved', 'ordered', 'partial_delivered', 'delivered', 'cancelled')),
    approver_id INTEGER REFERENCES users(id),
    approved_at TIMESTAMP,
    
    -- 关联
    project_id INTEGER REFERENCES projects(id),
    task_id INTEGER REFERENCES tasks(id), -- 关联建造任务
    
    -- 申请人
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 4. 库存管理（配合采购）
-- ============================================================

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    material_id INTEGER REFERENCES materials(id),
    batch_no VARCHAR(50), -- 批次号
    quantity DECIMAL(10,2) NOT NULL DEFAULT 0,
    
    -- 库位
    warehouse VARCHAR(50) NOT NULL, -- 仓库
    location VARCHAR(100), -- 具体库位
    
    -- 质检
    qc_status VARCHAR(20) DEFAULT 'pending' CHECK (qc_status IN ('pending', 'pass', 'fail', 'quarantine')),
    qc_report_url VARCHAR(500), -- 质检报告
    
    -- 来源
    procurement_order_id INTEGER REFERENCES procurement_orders(id),
    
    -- 有效期（部分材料有保质期）
    expiry_date DATE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(material_id, batch_no)
);

CREATE TABLE inventory_logs (
    id SERIAL PRIMARY KEY,
    material_id INTEGER REFERENCES materials(id),
    inventory_id INTEGER REFERENCES inventory(id),
    
    -- 操作类型
    type VARCHAR(10) NOT NULL CHECK (type IN ('in', 'out', 'adjust', 'transfer')),
    quantity DECIMAL(10,2) NOT NULL,
    before_qty DECIMAL(10,2),
    after_qty DECIMAL(10,2),
    
    -- 关联
    related_task_id INTEGER REFERENCES tasks(id), -- 关联建造任务
    related_order_id INTEGER REFERENCES procurement_orders(id), -- 关联采购单
    
    -- 操作人
    operator_id INTEGER REFERENCES users(id),
    operator_name VARCHAR(50), -- 冗余
    
    -- 签名/凭证
    signature VARCHAR(255), -- 电子签名
    photo_urls TEXT[], -- 照片数组
    
    -- 备注
    remark TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 5. 文件与照片管理
-- ============================================================

CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_type VARCHAR(50), -- image/pdf/cad/dwg/dxf
    file_size BIGINT, -- 文件大小（字节）
    mime_type VARCHAR(100),
    
    -- 关联
    related_type VARCHAR(50) NOT NULL, -- task/material/quality/project/user
    related_id INTEGER NOT NULL,
    
    -- 分类标签
    category VARCHAR(50), -- design_drawing, work_photo, qc_report, etc.
    tags VARCHAR(50)[],
    
    -- 元数据
    metadata JSONB, -- EXIF信息、CAD图层等
    
    -- 上传者
    uploaded_by INTEGER REFERENCES users(id),
    uploaded_by_name VARCHAR(50), -- 冗余
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 6. 工艺知识库（用于 AI RAG）
-- ============================================================

CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50), -- 焊接工艺/涂装标准/检验规范/安全规程
    sub_category VARCHAR(50),
    
    -- 向量存储（使用 pgvector 扩展）
    -- embedding VECTOR(1536), -- 需要安装 pgvector
    
    -- 来源
    source_file VARCHAR(255),
    source_type VARCHAR(20), -- pdf/doc/excel/manual
    
    -- 关联
    related_task_types VARCHAR(50)[], -- 关联的任务类型
    
    -- 元数据
    metadata JSONB,
    
    -- 统计
    view_count INTEGER DEFAULT 0,
    use_count INTEGER DEFAULT 0,
    
    -- 状态
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 7. 质量检测管理
-- ============================================================

CREATE TABLE quality_inspections (
    id SERIAL PRIMARY KEY,
    inspection_no VARCHAR(50) UNIQUE, -- 检验单号
    
    -- 关联
    project_id INTEGER REFERENCES projects(id),
    task_id INTEGER REFERENCES tasks(id),
    material_id INTEGER REFERENCES materials(id),
    
    -- 检验类型
    inspection_type VARCHAR(50) NOT NULL, -- welding, coating, assembly, electrical, watertight
    inspection_standard VARCHAR(100), -- 检验标准（如 CCS 规范）
    
    -- 检验结果
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'pass', 'fail', 'conditional_pass')),
    result_data JSONB, -- 检验数据（如焊接参数、涂层厚度等）
    defect_description TEXT,
    defect_photos TEXT[],
    
    -- 处理
    corrective_action TEXT, -- 整改措施
    re_inspection_date DATE, -- 复检日期
    
    -- 人员
    inspector_id INTEGER REFERENCES users(id),
    inspector_name VARCHAR(50),
    inspected_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 8. 工作流/审批记录
-- ============================================================

CREATE TABLE workflow_instances (
    id SERIAL PRIMARY KEY,
    workflow_type VARCHAR(50) NOT NULL, -- procurement, task_change, quality
    related_type VARCHAR(50), -- 关联表名
    related_id INTEGER, -- 关联记录ID
    
    title VARCHAR(200),
    description TEXT,
    
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled')),
    
    -- 当前步骤
    current_step INTEGER DEFAULT 1,
    total_steps INTEGER DEFAULT 1,
    
    -- 申请人
    applicant_id INTEGER REFERENCES users(id),
    applicant_name VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE workflow_approvals (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES workflow_instances(id) ON DELETE CASCADE,
    step_no INTEGER NOT NULL,
    
    approver_id INTEGER REFERENCES users(id),
    approver_name VARCHAR(50),
    approver_role VARCHAR(20),
    
    action VARCHAR(20) CHECK (action IN ('approve', 'reject', 'transfer', 'comment')),
    comment TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 9. 系统配置与审计日志
-- ============================================================

CREATE TABLE system_configs (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    config_type VARCHAR(20) DEFAULT 'string' CHECK (config_type IN ('string', 'number', 'boolean', 'json')),
    description TEXT,
    updated_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    username VARCHAR(50),
    
    action VARCHAR(50) NOT NULL, -- create, update, delete, login, logout, etc.
    resource_type VARCHAR(50), -- task, material, user, etc.
    resource_id INTEGER,
    
    before_data JSONB,
    after_data JSONB,
    
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 10. 消息通知
-- ============================================================

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    title VARCHAR(200) NOT NULL,
    content TEXT,
    
    type VARCHAR(20) DEFAULT 'info' CHECK (type IN ('info', 'warning', 'error', 'success')),
    category VARCHAR(50), -- task_reminder, approval_required, system, etc.
    
    -- 关联
    related_type VARCHAR(50),
    related_id INTEGER,
    
    -- 状态
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    
    -- 推送
    pushed BOOLEAN DEFAULT FALSE,
    push_channel VARCHAR(20), -- web, email, sms, app
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 索引优化
-- ============================================================

-- 用户表索引
CREATE INDEX idx_users_dept ON users(dept_id);
CREATE INDEX idx_users_team ON users(team_id);
CREATE INDEX idx_users_role ON users(role);

-- 任务表索引
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_type ON tasks(task_type);
CREATE INDEX idx_tasks_dates ON tasks(plan_start, plan_end);
CREATE INDEX idx_tasks_manager ON tasks(manager_id);
CREATE INDEX idx_tasks_team ON tasks(team_id);

-- 物料表索引
CREATE INDEX idx_materials_category ON materials(cat_id);
CREATE INDEX idx_materials_project ON materials(project_id);
CREATE INDEX idx_materials_status ON materials(status);

-- 采购单索引
CREATE INDEX idx_procurement_status ON procurement_orders(status);
CREATE INDEX idx_procurement_project ON procurement_orders(project_id);
CREATE INDEX idx_procurement_date ON procurement_orders(order_date);

-- 库存索引
CREATE INDEX idx_inventory_material ON inventory(material_id);
CREATE INDEX idx_inventory_warehouse ON inventory(warehouse);
CREATE INDEX idx_inventory_qc ON inventory(qc_status);

-- 附件索引
CREATE INDEX idx_attachments_related ON attachments(related_type, related_id);
CREATE INDEX idx_attachments_type ON attachments(file_type);

-- 审计日志索引
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created ON audit_logs(created_at);

-- 通知索引
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = FALSE;

-- 复合索引示例（常用查询优化）
CREATE INDEX idx_tasks_project_status ON tasks(project_id, status);
CREATE INDEX idx_tasks_type_status ON tasks(task_type, status);
CREATE INDEX idx_procurement_status_date ON procurement_orders(status, order_date);
CREATE INDEX idx_inventory_material_warehouse ON inventory(material_id, warehouse);

-- 全文搜索索引（PostgreSQL）
CREATE INDEX idx_materials_name_trgm ON materials USING gin (name gin_trgm_ops);
CREATE INDEX idx_projects_name_trgm ON projects USING gin (yacht_name gin_trgm_ops);

-- 分区表示例（大数据量时考虑）
-- CREATE TABLE audit_logs_2024 PARTITION OF audit_logs
--     FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- ============================================================
-- 初始数据
-- ============================================================

-- 默认部门
INSERT INTO departments (name, code, description) VALUES
('设计部', 'DEPT_DESIGN', '游艇设计、结构设计、电气设计'),
('生产部', 'DEPT_PRODUCTION', '船体制作、舾装、内装'),
('采购部', 'DEPT_PROCUREMENT', '物料采购、供应商管理'),
('质检部', 'DEPT_QC', '质量检测、验收'),
('综合部', 'DEPT_ADMIN', '行政、财务、人事');

-- 默认班组
INSERT INTO teams (dept_id, name, code, specialty) VALUES
(1, '结构设计组', 'TEAM_STRUCTURE', '船体结构设计'),
(1, '电气设计组', 'TEAM_ELECTRICAL', '电气系统设计'),
(2, '铝合金班组', 'TEAM_ALUMINUM', '铝合金船体制作'),
(2, '焊接班组', 'TEAM_WELDING', '船体焊接'),
(2, '舾装班组', 'TEAM_OUTFITTING', '舾装作业'),
(2, '内装班组', 'TEAM_INTERIOR', '内部装修'),
(3, '采购组', 'TEAM_PROCUREMENT', '物料采购'),
(4, '质检组', 'TEAM_QC', '质量检测');

-- 物料分类
INSERT INTO material_categories (main_cat, sub_cat, code_prefix) VALUES
('鋁合金', '鋁板', 'AL-PLATE'),
('鋁合金', '型材', 'AL-PROFILE'),
('焊接材料', '焊絲', 'WELD-WIRE'),
('焊接材料', '焊劑', 'WELD-FLUX'),
('电气', '電纜', 'ELEC-CABLE'),
('电气', '配電箱', 'ELEC-PANEL'),
('涂料', '底漆', 'PAINT-PRIMER'),
('涂料', '面漆', 'PAINT-TOP');

-- 系统配置
INSERT INTO system_configs (config_key, config_value, description) VALUES
('system.name', '铝合金电动游艇建造管理系统', '系统名称'),
('system.version', '1.0.0', '系统版本'),
('inventory.warning.threshold', '10', '库存预警阈值（%）'),
('task.delay.warning.days', '3', '任务延期预警天数'),
('file.max_size', '104857600', '最大文件上传大小（字节）');

-- ============================================================
-- 触发器：自动更新时间戳
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为需要自动更新时间的表创建触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_departments_updated_at BEFORE UPDATE ON departments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_teams_updated_at BEFORE UPDATE ON teams
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_materials_updated_at BEFORE UPDATE ON materials
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_procurement_orders_updated_at BEFORE UPDATE ON procurement_orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_inventory_updated_at BEFORE UPDATE ON inventory
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_knowledge_base_updated_at BEFORE UPDATE ON knowledge_base
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quality_inspections_updated_at BEFORE UPDATE ON quality_inspections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

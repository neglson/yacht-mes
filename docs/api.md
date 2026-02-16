# Yacht MES API 文档

## 基础信息

- **Base URL**: `http://localhost:8000/api`
- **Content-Type**: `application/json`
- **认证方式**: Bearer Token

## 认证

### 登录
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "username": "admin",
    "real_name": "管理员",
    "role": "admin"
  }
}
```

### 获取当前用户
```http
GET /auth/me
Authorization: Bearer {token}
```

## 用户管理

### 获取用户列表
```http
GET /users?page=1&size=20&dept_id=1&role=worker
Authorization: Bearer {token}
```

### 创建用户
```http
POST /users
Authorization: Bearer {token}
Content-Type: application/json

{
  "username": "newuser",
  "password": "password123",
  "real_name": "新用户",
  "role": "worker",
  "dept_id": 1,
  "team_id": 1,
  "phone": "13800138000",
  "email": "user@example.com"
}
```

### 更新用户
```http
PUT /users/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "real_name": "更新的姓名",
  "phone": "13900139000"
}
```

### 删除用户
```http
DELETE /users/{id}
Authorization: Bearer {token}
```

### 重置密码
```http
POST /users/{id}/reset-password
Authorization: Bearer {token}
```

## 项目管理

### 获取项目列表
```http
GET /projects?status=in_progress&page=1&size=20
Authorization: Bearer {token}
```

### 创建项目
```http
POST /projects
Authorization: Bearer {token}
Content-Type: application/json

{
  "project_no": "YT-2024-001",
  "yacht_name": "海鹰号",
  "yacht_model": "HY-65",
  "client_name": "张三",
  "status": "planning",
  "start_date": "2024-03-01",
  "planned_end": "2024-08-31",
  "total_budget": 5000000,
  "description": "项目描述"
}
```

### 更新项目
```http
PUT /projects/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "yacht_name": "更新的名称",
  "status": "in_progress"
}
```

### 删除项目
```http
DELETE /projects/{id}
Authorization: Bearer {token}
```

## 任务管理

### 获取任务列表
```http
GET /tasks?project_id=1&status=in_progress&page=1&size=20
Authorization: Bearer {token}
```

### 创建任务
```http
POST /tasks
Authorization: Bearer {token}
Content-Type: application/json

{
  "project_id": 1,
  "task_no": "1.1",
  "name": "飞桥结构设计",
  "task_type": "design",
  "status": "not_started",
  "priority": "high",
  "plan_start": "2024-03-01",
  "plan_end": "2024-03-31",
  "planned_work_hours": 160,
  "manager_id": 2
}
```

### 更新任务
```http
PUT /tasks/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "更新的任务名称",
  "progress_percent": 50,
  "status": "in_progress",
  "version": 1
}
```

### 任务报工
```http
POST /tasks/{id}/report
Authorization: Bearer {token}
Content-Type: application/json

{
  "work_hours": 8,
  "progress_percent": 75,
  "description": "今日完成的工作内容"
}
```

### 删除任务
```http
DELETE /tasks/{id}
Authorization: Bearer {token}
```

## 物料管理

### 获取物料列表
```http
GET /materials?category_id=1&keyword=铝合金&page=1&size=20
Authorization: Bearer {token}
```

### 创建物料
```http
POST /materials
Authorization: Bearer {token}
Content-Type: application/json

{
  "code": "AL-001",
  "name": "4mm铝合金板",
  "brand": "CCS",
  "model": "5083-H116",
  "unit": "平米",
  "supplier": "中铝",
  "unit_cost": 280.00,
  "min_stock": 100
}
```

### 更新物料
```http
PUT /materials/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "更新的名称",
  "unit_cost": 290.00
}
```

### 删除物料
```http
DELETE /materials/{id}
Authorization: Bearer {token}
```

## 库存管理

### 获取库存列表
```http
GET /inventory?material_id=1&warehouse=main
Authorization: Bearer {token}
```

### 库存出入库
```http
POST /inventory/transaction
Authorization: Bearer {token}
Content-Type: application/json

{
  "material_id": 1,
  "type": "in",
  "quantity": 100,
  "warehouse": "main",
  "location": "A-01-01",
  "batch_no": "20240301-001",
  "remark": "入库备注"
}
```

### 获取库存日志
```http
GET /inventory/logs?material_id=1&page=1&size=20
Authorization: Bearer {token}
```

### 获取库存预警
```http
GET /inventory/alerts
Authorization: Bearer {token}
```

## 采购管理

### 获取采购列表
```http
GET /procurement?status=pending_approval&page=1&size=20
Authorization: Bearer {token}
```

### 创建采购申请
```http
POST /procurement
Authorization: Bearer {token}
Content-Type: application/json

{
  "order_no": "PO-2024-001",
  "material_id": 1,
  "material_name": "4mm铝合金板",
  "quantity": 200,
  "unit": "平米",
  "unit_price": 280.00,
  "total_price": 56000.00,
  "supplier": "中铝",
  "delivery_date": "2024-03-15"
}
```

### 审批采购
```http
PUT /procurement/{id}/approve
Authorization: Bearer {token}
```

### 更新采购状态
```http
PUT /procurement/{id}/status
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "ordered"
}
```

## 仪表盘

### 获取统计数据
```http
GET /dashboard/stats
Authorization: Bearer {token}
```

**响应**:
```json
{
  "active_projects": 5,
  "today_tasks": 12,
  "pending_procurement": 3,
  "inventory_alerts": 2
}
```

### 获取项目进度
```http
GET /dashboard/project-progress
Authorization: Bearer {token}
```

### 获取任务分布
```http
GET /dashboard/task-distribution
Authorization: Bearer {token}
```

### 获取最近活动
```http
GET /dashboard/recent-activities
Authorization: Bearer {token}
```

## AI 助手

### 自然语言查询
```http
POST /ai/query
Authorization: Bearer {token}
Content-Type: application/json

{
  "query": "查询本周延期的任务"
}
```

### 采购建议
```http
POST /ai/procurement-advice
Authorization: Bearer {token}
Content-Type: application/json

{
  "project_id": 1
}
```

### 生成日报
```http
POST /ai/daily-report
Authorization: Bearer {token}
Content-Type: application/json

{
  "date": "2024-03-01"
}
```

### 工艺知识查询
```http
POST /ai/knowledge-query
Authorization: Bearer {token}
Content-Type: application/json

{
  "question": "船体对接焊间隙标准是多少？"
}
```

## 数据导入

### Excel 导入
```http
POST /import/excel
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: [Excel文件]
```

**支持的工作表**:
- 项目
- 时间轴/任务
- 物料
- 采购
- 部门
- 班组
- 用户

## 附件管理

### 上传文件
```http
POST /attachments/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: [文件]
related_type: task
related_id: 1
```

### 获取附件列表
```http
GET /attachments?related_type=task&related_id=1
Authorization: Bearer {token}
```

### 删除附件
```http
DELETE /attachments/{id}
Authorization: Bearer {token}
```

## 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 409 | 资源冲突（如重复） |
| 500 | 服务器内部错误 |

## 角色权限

| 角色 | 权限 |
|------|------|
| admin | 所有权限 |
| dept_manager | 管理本部门数据，审批采购 |
| team_leader | 管理本班组任务，创建采购申请 |
| worker | 查看分配的任务，报工 |

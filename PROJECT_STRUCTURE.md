# Yacht MES - 项目结构概览

```
yacht-mes/
├── README.md                      # 项目主文档
├── docker-compose.yml             # Docker 编排配置
├── start.sh                       # 一键启动脚本
│
├── database/
│   └── schema.sql                 # 完整数据库结构（10张核心表）
│
├── backend/                       # FastAPI 后端
│   ├── Dockerfile
│   ├── requirements.txt           # Python 依赖
│   ├── README.md
│   └── app/
│       ├── main.py                # FastAPI 入口
│       ├── config.py              # 配置管理
│       ├── database.py            # 数据库连接
│       ├── models/                # SQLAlchemy 模型
│       ├── routers/               # API 路由
│       │   ├── auth.py            # 认证接口
│       │   └── __init__.py
│       ├── schemas/               # Pydantic 模型
│       │   ├── user.py            # 用户相关模型
│       │   ├── project.py         # 项目/任务模型
│       │   └── __init__.py
│       ├── services/              # 业务逻辑层
│       └── utils/                 # 工具函数
│           ├── security.py        # JWT/密码加密
│           └── __init__.py
│
├── frontend/                      # Vue3 前端
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf                 # Nginx 配置
│   ├── package.json               # Node 依赖
│   ├── tsconfig.json              # TypeScript 配置
│   ├── vite.config.ts             # Vite 配置
│   └── src/
│       ├── main.ts                # 入口文件
│       ├── App.vue                # 根组件
│       ├── router/
│       │   └── index.ts           # 路由配置（11个页面）
│       ├── stores/
│       │   └── user.ts            # Pinia 用户状态
│       ├── api/
│       │   ├── index.ts           # Axios 配置
│       │   └── auth.ts            # 认证 API
│       ├── types/
│       │   └── user.ts            # TypeScript 类型
│       ├── components/
│       │   └── Breadcrumb.vue     # 面包屑组件
│       ├── layouts/
│       │   └── MainLayout.vue     # 主布局
│       ├── views/
│       │   ├── login/
│       │   │   └── index.vue      # 登录页
│       │   ├── dashboard/
│       │   │   ├── index.vue      # 仪表盘
│       │   │   └── components/
│       │   │       └── StatCard.vue
│       │   ├── projects/
│       │   │   └── index.vue      # 项目管理
│       │   └── error/
│       │       └── 404.vue        # 404 页面
│       └── styles/
│           └── main.scss          # 全局样式
│
├── scripts/
│   └── backup.sh                  # 数据库备份脚本
│
└── docs/
    └── operations.md              # 运维文档
```

## 数据库表结构（10张表）

| 表名 | 说明 |
|------|------|
| departments | 部门表 |
| teams | 班组表 |
| users | 用户表（RBAC权限） |
| projects | 项目表 |
| tasks | 任务表（WBS层级） |
| task_dependencies | 任务依赖关系 |
| material_categories | 物料分类 |
| materials | 物料表 |
| procurement_orders | 采购订单 |
| inventory | 库存表 |
| inventory_logs | 库存日志 |
| attachments | 附件表 |
| knowledge_base | 知识库（AI RAG） |
| quality_inspections | 质检表 |
| workflow_instances | 工作流实例 |
| workflow_approvals | 审批记录 |
| system_configs | 系统配置 |
| audit_logs | 审计日志 |
| notifications | 通知表 |

## 前端页面（11个）

1. 登录页 (/login)
2. 仪表盘 (/dashboard)
3. 项目管理 (/projects)
4. 项目详情 (/projects/:id)
5. 任务管理 (/tasks)
6. 甘特图 (/tasks/gantt)
7. 物料管理 (/materials)
8. 采购管理 (/procurement)
9. 库存管理 (/inventory)
10. 质量管理 (/quality)
11. 知识库 (/knowledge)
12. 用户管理 (/users)
13. 系统设置 (/settings)

## 快速开始

```bash
# 启动所有服务
./start.sh

# 访问系统
http://localhost:8080

# 默认账号
用户名: admin
密码: admin
```

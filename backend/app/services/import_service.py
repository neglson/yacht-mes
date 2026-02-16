"""
数据导入服务 - 将Excel数据写入数据库
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, List, Any
from datetime import datetime

from app.models import (
    User, Department, Team, Project, Task,
    MaterialCategory, Material, ProcurementOrder
)
from app.utils.security import get_password_hash


class ImportService:
    """数据导入服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.errors = []
        self.imported_counts = {
            'departments': 0,
            'teams': 0,
            'users': 0,
            'projects': 0,
            'tasks': 0,
            'material_categories': 0,
            'materials': 0,
            'procurement': 0
        }
    
    async def import_all(self, data: Dict[str, List[Dict]]) -> Dict:
        """导入所有数据"""
        # 按依赖顺序导入
        await self._import_departments(data.get('departments', []))
        await self._import_teams(data.get('teams', []))
        await self._import_users(data.get('users', []))
        await self._import_projects(data.get('projects', []))
        await self._import_tasks(data.get('tasks', []))
        await self._import_materials(data.get('materials', []))
        await self._import_procurement(data.get('procurement', []))
        
        await self.db.commit()
        
        return {
            'success': len(self.errors) == 0,
            'imported': self.imported_counts,
            'errors': self.errors
        }
    
    async def _import_departments(self, departments: List[Dict]):
        """导入部门"""
        for dept_data in departments:
            try:
                # 检查是否已存在
                result = await self.db.execute(
                    select(Department).where(Department.code == dept_data.get('code'))
                )
                if result.scalar_one_or_none():
                    continue
                
                dept = Department(
                    name=dept_data['name'],
                    code=dept_data.get('code'),
                    description=dept_data.get('description')
                )
                self.db.add(dept)
                self.imported_counts['departments'] += 1
            except Exception as e:
                self.errors.append(f"部门导入失败 {dept_data.get('name')}: {str(e)}")
    
    async def _import_teams(self, teams: List[Dict]):
        """导入班组"""
        for team_data in teams:
            try:
                # 查找部门
                dept = None
                if team_data.get('dept_name'):
                    result = await self.db.execute(
                        select(Department).where(Department.name == team_data['dept_name'])
                    )
                    dept = result.scalar_one_or_none()
                
                # 检查是否已存在
                result = await self.db.execute(
                    select(Team).where(Team.code == team_data.get('code'))
                )
                if result.scalar_one_or_none():
                    continue
                
                team = Team(
                    name=team_data['name'],
                    code=team_data.get('code'),
                    dept_id=dept.id if dept else None,
                    specialty=team_data.get('specialty')
                )
                self.db.add(team)
                self.imported_counts['teams'] += 1
            except Exception as e:
                self.errors.append(f"班组导入失败 {team_data.get('name')}: {str(e)}")
    
    async def _import_users(self, users: List[Dict]):
        """导入用户"""
        for user_data in users:
            try:
                # 检查是否已存在
                result = await self.db.execute(
                    select(User).where(User.username == user_data['username'])
                )
                if result.scalar_one_or_none():
                    continue
                
                # 查找部门和班组
                dept = None
                team = None
                if user_data.get('dept_name'):
                    result = await self.db.execute(
                        select(Department).where(Department.name == user_data['dept_name'])
                    )
                    dept = result.scalar_one_or_none()
                
                if user_data.get('team_name'):
                    result = await self.db.execute(
                        select(Team).where(Team.name == user_data['team_name'])
                    )
                    team = result.scalar_one_or_none()
                
                user = User(
                    username=user_data['username'],
                    password_hash=get_password_hash('123456'),  # 默认密码
                    real_name=user_data.get('real_name'),
                    phone=user_data.get('phone'),
                    email=user_data.get('email'),
                    role=user_data.get('role', 'worker'),
                    dept_id=dept.id if dept else None,
                    team_id=team.id if team else None,
                    is_active=True
                )
                self.db.add(user)
                self.imported_counts['users'] += 1
            except Exception as e:
                self.errors.append(f"用户导入失败 {user_data.get('username')}: {str(e)}")
    
    async def _import_projects(self, projects: List[Dict]):
        """导入项目"""
        for proj_data in projects:
            try:
                # 检查是否已存在
                result = await self.db.execute(
                    select(Project).where(Project.project_no == proj_data['project_no'])
                )
                if result.scalar_one_or_none():
                    continue
                
                project = Project(
                    project_no=proj_data['project_no'],
                    yacht_name=proj_data['yacht_name'],
                    yacht_model=proj_data.get('yacht_model'),
                    client_name=proj_data.get('client_name'),
                    status=proj_data.get('status', 'planning'),
                    start_date=self._parse_date(proj_data.get('start_date')),
                    planned_end=self._parse_date(proj_data.get('planned_end')),
                    description=proj_data.get('description')
                )
                self.db.add(project)
                self.imported_counts['projects'] += 1
            except Exception as e:
                self.errors.append(f"项目导入失败 {proj_data.get('project_no')}: {str(e)}")
    
    async def _import_tasks(self, tasks: List[Dict]):
        """导入任务"""
        for task_data in tasks:
            try:
                # 查找项目
                project = None
                if task_data.get('project_id'):
                    result = await self.db.execute(
                        select(Project).where(Project.id == task_data['project_id'])
                    )
                    project = result.scalar_one_or_none()
                
                # 如果没有指定项目，使用第一个项目
                if not project:
                    result = await self.db.execute(select(Project).limit(1))
                    project = result.scalar_one_or_none()
                
                if not project:
                    self.errors.append(f"任务导入失败 {task_data.get('name')}: 无可用项目")
                    continue
                
                task = Task(
                    project_id=project.id,
                    task_no=task_data.get('task_no', '1'),
                    name=task_data['name'],
                    task_type=task_data.get('task_type', 'other'),
                    status=task_data.get('status', 'not_started'),
                    priority=task_data.get('priority', 'medium'),
                    plan_start=self._parse_date(task_data.get('plan_start')),
                    plan_end=self._parse_date(task_data.get('plan_end')),
                    actual_start=self._parse_date(task_data.get('actual_start')),
                    actual_end=self._parse_date(task_data.get('actual_end')),
                    planned_work_hours=task_data.get('planned_work_hours'),
                    actual_work_hours=task_data.get('actual_work_hours', 0),
                    progress_percent=task_data.get('progress_percent', 0),
                    delay_days=task_data.get('delay_days', 0),
                    delay_reason=task_data.get('delay_reason')
                )
                self.db.add(task)
                self.imported_counts['tasks'] += 1
            except Exception as e:
                self.errors.append(f"任务导入失败 {task_data.get('name')}: {str(e)}")
    
    async def _import_materials(self, materials: List[Dict]):
        """导入物料"""
        for mat_data in materials:
            try:
                # 检查是否已存在
                if mat_data.get('code'):
                    result = await self.db.execute(
                        select(Material).where(Material.code == mat_data['code'])
                    )
                    if result.scalar_one_or_none():
                        continue
                
                # 查找或创建分类
                cat = None
                if mat_data.get('category'):
                    result = await self.db.execute(
                        select(MaterialCategory).where(MaterialCategory.main_cat == mat_data['category'])
                    )
                    cat = result.scalar_one_or_none()
                    
                    if not cat:
                        cat = MaterialCategory(
                            main_cat=mat_data['category'],
                            sub_cat=mat_data.get('sub_category')
                        )
                        self.db.add(cat)
                        await self.db.flush()
                        self.imported_counts['material_categories'] += 1
                
                material = Material(
                    cat_id=cat.id if cat else None,
                    code=mat_data.get('code'),
                    name=mat_data['name'],
                    brand=mat_data.get('brand'),
                    model=mat_data.get('model'),
                    specification=mat_data.get('specification'),
                    unit=mat_data.get('unit', '个'),
                    supplier=mat_data.get('supplier'),
                    unit_cost=mat_data.get('unit_cost'),
                    min_stock=mat_data.get('min_stock', 0),
                    description=mat_data.get('description')
                )
                self.db.add(material)
                self.imported_counts['materials'] += 1
            except Exception as e:
                self.errors.append(f"物料导入失败 {mat_data.get('name')}: {str(e)}")
    
    async def _import_procurement(self, procurement: List[Dict]):
        """导入采购订单"""
        for proc_data in procurement:
            try:
                # 查找物料
                material = None
                if proc_data.get('material_name'):
                    result = await self.db.execute(
                        select(Material).where(Material.name == proc_data['material_name'])
                    )
                    material = result.scalar_one_or_none()
                
                order = ProcurementOrder(
                    order_no=proc_data.get('order_no', f"PO-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                    material_id=material.id if material else None,
                    material_name=proc_data['material_name'],
                    quantity=proc_data.get('quantity', 0),
                    unit=proc_data.get('unit'),
                    unit_price=proc_data.get('unit_price'),
                    total_price=proc_data.get('total_price'),
                    supplier=proc_data.get('supplier'),
                    order_date=self._parse_date(proc_data.get('order_date')),
                    delivery_date=self._parse_date(proc_data.get('delivery_date')),
                    status=proc_data.get('status', 'draft')
                )
                self.db.add(order)
                self.imported_counts['procurement'] += 1
            except Exception as e:
                self.errors.append(f"采购导入失败 {proc_data.get('material_name')}: {str(e)}")
    
    def _parse_date(self, date_str):
        """解析日期字符串"""
        if not date_str:
            return None
        if isinstance(date_str, datetime):
            return date_str
        if isinstance(date_str, str):
            for fmt in ['%Y-%m-%d', '%Y/%m/%d']:
                try:
                    return datetime.strptime(date_str, fmt)
                except:
                    continue
        return None

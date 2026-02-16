"""
Excel 数据导入工具
支持从标准格式的 Excel 导入游艇建造数据
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import re


class ExcelImporter:
    """Excel 数据导入器"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.errors = []
        self.warnings = []
    
    def read_excel(self) -> Dict[str, pd.DataFrame]:
        """读取 Excel 所有 sheet"""
        try:
            xls = pd.ExcelFile(self.file_path)
            sheets = {}
            for sheet_name in xls.sheet_names:
                sheets[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
            return sheets
        except Exception as e:
            self.errors.append(f"读取 Excel 失败: {str(e)}")
            return {}
    
    def parse_projects(self, df: pd.DataFrame) -> List[Dict]:
        """解析项目数据"""
        projects = []
        for _, row in df.iterrows():
            project = {
                'project_no': str(row.get('项目编号', '')).strip(),
                'yacht_name': str(row.get('游艇名称', '')).strip(),
                'yacht_model': str(row.get('船型', '')).strip(),
                'client_name': str(row.get('船东', '')).strip(),
                'status': self._map_status(row.get('状态', '规划中')),
                'start_date': self._parse_date(row.get('开始日期')),
                'planned_end': self._parse_date(row.get('计划结束日期')),
                'description': str(row.get('备注', '')).strip()
            }
            if project['project_no'] and project['yacht_name']:
                projects.append(project)
        return projects
    
    def parse_tasks(self, df: pd.DataFrame, project_id: int = None) -> List[Dict]:
        """解析任务数据（时间轴）"""
        tasks = []
        for _, row in df.iterrows():
            task_no = str(row.get('序号', '')).strip()
            if not task_no:
                continue
                
            task = {
                'task_no': task_no,
                'name': str(row.get('项目/任务名称', '')).strip(),
                'task_type': self._map_task_type(str(row.get('任务类型', ''))),
                'status': self._map_task_status(str(row.get('状态', ''))),
                'plan_start': self._parse_date(row.get('计划开始')),
                'plan_end': self._parse_date(row.get('计划结束')),
                'actual_start': self._parse_date(row.get('实际开始')),
                'actual_end': self._parse_date(row.get('实际结束')),
                'planned_work_hours': self._parse_int(row.get('计划工时')),
                'actual_work_hours': self._parse_int(row.get('实际工时')),
                'progress_percent': self._parse_int(row.get('进度%', 0)),
                'delay_days': self._parse_int(row.get('延期天数', 0)),
                'delay_reason': str(row.get('延期原因', '')).strip(),
                'project_id': project_id
            }
            if task['name']:
                tasks.append(task)
        return tasks
    
    def parse_materials(self, df: pd.DataFrame) -> List[Dict]:
        """解析物料数据"""
        materials = []
        for _, row in df.iterrows():
            material = {
                'code': str(row.get('物料编码', '')).strip(),
                'name': str(row.get('物料名称', '')).strip(),
                'brand': str(row.get('品牌', '')).strip(),
                'model': str(row.get('型号/规格', '')).strip(),
                'unit': str(row.get('单位', '')).strip(),
                'supplier': str(row.get('供应商', '')).strip(),
                'unit_cost': self._parse_float(row.get('单价')),
                'min_stock': self._parse_float(row.get('最低库存', 0)),
                'description': str(row.get('描述', '')).strip()
            }
            if material['name']:
                materials.append(material)
        return materials
    
    def parse_procurement(self, df: pd.DataFrame) -> List[Dict]:
        """解析采购数据"""
        orders = []
        for _, row in df.iterrows():
            order = {
                'order_no': str(row.get('采购单号', '')).strip(),
                'material_name': str(row.get('物料名称', '')).strip(),
                'quantity': self._parse_float(row.get('数量', 0)),
                'unit': str(row.get('单位', '')).strip(),
                'unit_price': self._parse_float(row.get('单价', 0)),
                'total_price': self._parse_float(row.get('总价', 0)),
                'supplier': str(row.get('供应商', '')).strip(),
                'order_date': self._parse_date(row.get('采购日期')),
                'delivery_date': self._parse_date(row.get('交货日期')),
                'status': self._map_procurement_status(str(row.get('状态', '待采购')))
            }
            if order['material_name']:
                orders.append(order)
        return orders
    
    def parse_departments(self, df: pd.DataFrame) -> List[Dict]:
        """解析部门数据"""
        depts = []
        for _, row in df.iterrows():
            dept = {
                'name': str(row.get('部门名称', '')).strip(),
                'code': str(row.get('部门编码', '')).strip(),
                'description': str(row.get('描述', '')).strip()
            }
            if dept['name']:
                depts.append(dept)
        return depts
    
    def parse_teams(self, df: pd.DataFrame) -> List[Dict]:
        """解析班组数据"""
        teams = []
        for _, row in df.iterrows():
            team = {
                'name': str(row.get('班组名称', '')).strip(),
                'code': str(row.get('班组编码', '')).strip(),
                'dept_name': str(row.get('所属部门', '')).strip(),
                'specialty': str(row.get('专业领域', '')).strip()
            }
            if team['name']:
                teams.append(team)
        return teams
    
    def parse_users(self, df: pd.DataFrame) -> List[Dict]:
        """解析用户数据"""
        users = []
        for _, row in df.iterrows():
            user = {
                'username': str(row.get('用户名', '')).strip(),
                'real_name': str(row.get('姓名', '')).strip(),
                'phone': str(row.get('电话', '')).strip(),
                'email': str(row.get('邮箱', '')).strip(),
                'role': self._map_role(str(row.get('角色', '工人'))),
                'dept_name': str(row.get('部门', '')).strip(),
                'team_name': str(row.get('班组', '')).strip()
            }
            if user['username'] and user['real_name']:
                users.append(user)
        return users
    
    # 辅助方法
    def _parse_date(self, value) -> Optional[str]:
        """解析日期"""
        if pd.isna(value):
            return None
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d')
        if isinstance(value, str):
            # 尝试多种日期格式
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    return datetime.strptime(value.strip(), fmt).strftime('%Y-%m-%d')
                except:
                    continue
        return None
    
    def _parse_int(self, value) -> int:
        """解析整数"""
        try:
            return int(float(value))
        except:
            return 0
    
    def _parse_float(self, value) -> float:
        """解析浮点数"""
        try:
            return float(value)
        except:
            return 0.0
    
    def _map_status(self, status: str) -> str:
        """映射项目状态"""
        mapping = {
            '规划中': 'planning',
            '进行中': 'in_progress',
            '已完成': 'completed',
            '已取消': 'cancelled',
            'planning': 'planning',
            'in_progress': 'in_progress',
            'completed': 'completed',
            'cancelled': 'cancelled'
        }
        return mapping.get(status.strip(), 'planning')
    
    def _map_task_type(self, task_type: str) -> str:
        """映射任务类型"""
        mapping = {
            '设计': 'design',
            '船体制作': 'hull_construction',
            '采购配料': 'procurement',
            '舾装': 'outfitting',
            '内装': 'interior',
            '调试': 'commissioning',
            '质检': 'quality_check'
        }
        return mapping.get(task_type.strip(), 'other')
    
    def _map_task_status(self, status: str) -> str:
        """映射任务状态"""
        mapping = {
            '未开始': 'not_started',
            '进行中': 'in_progress',
            '已完成': 'completed',
            '延期': 'delayed',
            '已取消': 'cancelled'
        }
        return mapping.get(status.strip(), 'not_started')
    
    def _map_procurement_status(self, status: str) -> str:
        """映射采购状态"""
        mapping = {
            '待采购': 'draft',
            '审批中': 'pending_approval',
            '已下单': 'ordered',
            '已到货': 'delivered',
            '已取消': 'cancelled'
        }
        return mapping.get(status.strip(), 'draft')
    
    def _map_role(self, role: str) -> str:
        """映射用户角色"""
        mapping = {
            '管理员': 'admin',
            '部门领导': 'dept_manager',
            '班组长': 'team_leader',
            '工人': 'worker'
        }
        return mapping.get(role.strip(), 'worker')


def import_from_excel(file_path: str) -> Dict[str, List[Dict]]:
    """
    从 Excel 文件导入所有数据
    
    支持的 sheet 名称：
    - 项目 / Projects
    - 时间轴 / 任务 / Tasks / Timeline
    - 物料 / Materials
    - 采购 / Procurement
    - 部门 / Departments
    - 班组 / Teams
    - 用户 / Users / 人员
    """
    importer = ExcelImporter(file_path)
    sheets = importer.read_excel()
    
    result = {
        'projects': [],
        'tasks': [],
        'materials': [],
        'procurement': [],
        'departments': [],
        'teams': [],
        'users': [],
        'errors': importer.errors,
        'warnings': importer.warnings
    }
    
    for sheet_name, df in sheets.items():
        sheet_lower = sheet_name.lower()
        
        if '项目' in sheet_lower or 'project' in sheet_lower:
            result['projects'] = importer.parse_projects(df)
        elif '时间轴' in sheet_lower or '任务' in sheet_lower or 'task' in sheet_lower or 'timeline' in sheet_lower:
            result['tasks'] = importer.parse_tasks(df)
        elif '物料' in sheet_lower or 'material' in sheet_lower:
            result['materials'] = importer.parse_materials(df)
        elif '采购' in sheet_lower or 'procurement' in sheet_lower:
            result['procurement'] = importer.parse_procurement(df)
        elif '部门' in sheet_lower or 'department' in sheet_lower:
            result['departments'] = importer.parse_departments(df)
        elif '班组' in sheet_lower or 'team' in sheet_lower:
            result['teams'] = importer.parse_teams(df)
        elif '用户' in sheet_lower or '人员' in sheet_lower or 'user' in sheet_lower:
            result['users'] = importer.parse_users(df)
    
    return result


if __name__ == '__main__':
    # 测试导入
    import sys
    if len(sys.argv) > 1:
        result = import_from_excel(sys.argv[1])
        print(f"导入结果:")
        print(f"  项目: {len(result['projects'])} 条")
        print(f"  任务: {len(result['tasks'])} 条")
        print(f"  物料: {len(result['materials'])} 条")
        print(f"  采购: {len(result['procurement'])} 条")
        print(f"  部门: {len(result['departments'])} 条")
        print(f"  班组: {len(result['teams'])} 条")
        print(f"  用户: {len(result['users'])} 条")
        if result['errors']:
            print(f"\n错误: {result['errors']}")

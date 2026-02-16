"""
简单测试 - 无需数据库
"""

import pytest
from fastapi.testclient import TestClient

# 导入应用
import sys
sys.path.insert(0, '.')


def test_app_import():
    """测试应用可以正常导入"""
    from app.main import app
    assert app is not None
    print("✓ 应用导入成功")


def test_security_utils():
    """测试安全工具函数"""
    from app.utils.security import get_password_hash, verify_password
    
    password = "testpassword"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
    print("✓ 密码加密验证成功")


def test_config():
    """测试配置加载"""
    from app.config import settings
    
    assert settings.APP_NAME == "Yacht MES"
    assert settings.DEBUG is True
    print("✓ 配置加载成功")


def test_excel_importer():
    """测试 Excel 导入工具"""
    from app.utils.excel_importer import ExcelImporter
    
    # 创建模拟数据
    import pandas as pd
    import io
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame({
            '项目编号': ['TEST-001'],
            '游艇名称': ['测试游艇']
        }).to_excel(writer, sheet_name='项目', index=False)
    
    output.seek(0)
    
    # 测试解析
    importer = ExcelImporter("test.xlsx")
    # 这里只是测试类可以实例化
    assert importer is not None
    print("✓ Excel导入工具正常")


def test_cache_utils():
    """测试缓存工具"""
    from app.utils.cache import Cache, cached
    
    cache = Cache()
    assert cache is not None
    
    # 测试 key 生成
    assert Cache.user_key(1) == "user:1"
    assert Cache.project_key(1) == "project:1"
    print("✓ 缓存工具正常")


if __name__ == "__main__":
    print("运行 Yacht MES 简单测试...\n")
    
    test_app_import()
    test_security_utils()
    test_config()
    test_excel_importer()
    test_cache_utils()
    
    print("\n✅ 所有简单测试通过！")

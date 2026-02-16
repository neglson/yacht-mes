"""
缓存工具
Redis 缓存封装
"""

import json
import pickle
from typing import Any, Optional, Union
from datetime import timedelta
import redis.asyncio as redis

from app.config import settings


class Cache:
    """Redis 缓存封装"""
    
    def __init__(self):
        self._redis: Optional[redis.Redis] = None
    
    async def connect(self):
        """连接 Redis"""
        if not self._redis:
            self._redis = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
    
    async def disconnect(self):
        """断开连接"""
        if self._redis:
            await self._redis.close()
            self._redis = None
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self._redis:
            await self.connect()
        
        value = await self._redis.get(key)
        if value is None:
            return None
        
        try:
            return pickle.loads(value.encode())
        except:
            return value
    
    async def set(
        self,
        key: str,
        value: Any,
        expire: Union[int, timedelta] = None
    ):
        """设置缓存"""
        if not self._redis:
            await self.connect()
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        elif not isinstance(value, (str, bytes)):
            value = pickle.dumps(value)
        
        if isinstance(expire, timedelta):
            expire = int(expire.total_seconds())
        
        await self._redis.set(key, value, ex=expire)
    
    async def delete(self, key: str):
        """删除缓存"""
        if not self._redis:
            await self.connect()
        
        await self._redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        """检查 key 是否存在"""
        if not self._redis:
            await self.connect()
        
        return await self._redis.exists(key) > 0
    
    async def expire(self, key: str, seconds: int):
        """设置过期时间"""
        if not self._redis:
            await self.connect()
        
        await self._redis.expire(key, seconds)
    
    async def incr(self, key: str) -> int:
        """自增"""
        if not self._redis:
            await self.connect()
        
        return await self._redis.incr(key)
    
    async def decr(self, key: str) -> int:
        """自减"""
        if not self._redis:
            await self.connect()
        
        return await self._redis.decr(key)
    
    # 常用缓存 key 生成方法
    @staticmethod
    def user_key(user_id: int) -> str:
        return f"user:{user_id}"
    
    @staticmethod
    def project_key(project_id: int) -> str:
        return f"project:{project_id}"
    
    @staticmethod
    def task_list_key(project_id: int) -> str:
        return f"tasks:project:{project_id}"
    
    @staticmethod
    def material_key(material_id: int) -> str:
        return f"material:{material_id}"
    
    @staticmethod
    def dashboard_stats_key() -> str:
        return "dashboard:stats"
    
    @staticmethod
    def inventory_alerts_key() -> str:
        return "inventory:alerts"


# 全局缓存实例
cache = Cache()


# 缓存装饰器
def cached(expire: int = 300, key_prefix: str = ""):
    """
    缓存装饰器
    
    Args:
        expire: 过期时间（秒）
        key_prefix: 缓存 key 前缀
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # 生成缓存 key
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 尝试从缓存获取
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数
            result = await func(*args, **kwargs)
            
            # 写入缓存
            await cache.set(cache_key, result, expire=expire)
            
            return result
        
        return wrapper
    return decorator


# 清除缓存装饰器
def clear_cache(*keys):
    """
    清除缓存装饰器
    
    Args:
        keys: 要清除的缓存 key 列表
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # 清除指定缓存
            for key in keys:
                await cache.delete(key)
            
            return result
        
        return wrapper
    return decorator

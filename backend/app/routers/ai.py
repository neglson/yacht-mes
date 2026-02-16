"""
AI 助手 API
集成 Kimi API 实现智能查询和建议
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import httpx
import os

from app.database import get_db
from app.utils.security import get_current_user
from app.config import settings

router = APIRouter()

# 数据库 Schema 描述（用于 NLP2SQL）
DB_SCHEMA = """
表结构：
- projects(项目): id, project_no(项目编号), yacht_name(游艇名称), status(状态), start_date(开始日期)
- tasks(任务): id, project_id, task_no(序号), name(任务名称), task_type(类型), status(状态), plan_start(计划开始), plan_end(计划结束), actual_start(实际开始), actual_end(实际结束), progress_percent(进度), manager_id(负责人)
- users(用户): id, username, real_name(姓名), role(角色), dept_id(部门), team_id(班组)
- materials(物料): id, name(物料名称), code(编码), stock(库存), min_stock(最低库存)
- procurement_orders(采购单): id, order_no(单号), material_name(物料), quantity(数量), status(状态)

角色：admin(管理员), dept_manager(部门领导), team_leader(班组长), worker(工人)
任务状态：not_started(未开始), in_progress(进行中), completed(已完成), delayed(延期)
任务类型：design(设计), hull_construction(船体制作), procurement(采购配料), outfitting(舾装), interior(内装), commissioning(调试)
"""


async def call_kimi_api(messages: list, temperature: float = 0.7) -> str:
    """调用 Kimi API"""
    if not settings.KIMI_API_KEY:
        raise HTTPException(status_code=500, detail="Kimi API 密钥未配置")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.KIMI_API_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.KIMI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "moonshot-v1-8k",
                "messages": messages,
                "temperature": temperature
            },
            timeout=30.0
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Kimi API 错误: {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]


@router.post("/query")
async def natural_language_query(
    query: Dict[str, str],
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    自然语言查询
    
    示例：
    - "查询铝合金班组本周的任务"
    - "有哪些延期的项目"
    - "库存低于安全线的物料"
    """
    user_query = query.get("query", "")
    
    if not user_query:
        raise HTTPException(status_code=400, detail="查询内容不能为空")
    
    # 构建提示词
    messages = [
        {
            "role": "system",
            "content": f"你是一个数据分析师，帮助用户查询游艇建造管理系统。\n\n{DB_SCHEMA}\n\n请根据用户的问题，生成对应的 SQL 查询语句，并以 JSON 格式返回：{{\"sql\": \"SELECT ...\", \"explanation\": \"查询说明\"}}"
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
    
    try:
        response = await call_kimi_api(messages, temperature=0.3)
        
        # 这里简化处理，实际应该解析 JSON
        return {
            "query": user_query,
            "response": response,
            "note": "AI 生成的查询建议，请确认后再执行"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 查询失败: {str(e)}")


@router.post("/procurement-advice")
async def get_procurement_advice(
    params: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取采购建议
    
    基于项目进度和库存情况，AI 给出采购建议
    """
    project_id = params.get("project_id")
    
    # 构建提示词
    messages = [
        {
            "role": "system",
            "content": "你是一个采购专家，根据游艇建造项目进度和库存情况，给出采购建议。"
        },
        {
            "role": "user",
            "content": f"请分析项目 {project_id} 的情况，给出：\n1. 紧急采购清单（7天内必须使用）\n2. 供应商比价建议\n3. 库存优化建议"
        }
    ]
    
    try:
        response = await call_kimi_api(messages)
        return {
            "advice": response,
            "project_id": project_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取建议失败: {str(e)}")


@router.post("/daily-report")
async def generate_daily_report(
    params: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    生成日报
    
    自动汇总当日生产情况
    """
    date = params.get("date")
    
    messages = [
        {
            "role": "system",
            "content": "你是一个生产管理助手，根据系统数据生成日报。"
        },
        {
            "role": "user",
            "content": f"请生成 {date or '今天'} 的生产日报，包括：\n1. 完成的任务\n2. 进行中的任务\n3. 延期任务及原因\n4. 明日计划"
        }
    ]
    
    try:
        response = await call_kimi_api(messages)
        return {
            "report": response,
            "date": date
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成日报失败: {str(e)}")


@router.post("/knowledge-query")
async def query_knowledge_base(
    query: Dict[str, str],
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    工艺知识库查询
    
    查询焊接、涂装等工艺规范
    """
    question = query.get("question", "")
    
    messages = [
        {
            "role": "system",
            "content": "你是一个造船工艺专家，熟悉铝合金游艇建造的各类工艺规范。请基于专业知识回答用户问题。"
        },
        {
            "role": "user",
            "content": question
        }
    ]
    
    try:
        response = await call_kimi_api(messages)
        return {
            "question": question,
            "answer": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

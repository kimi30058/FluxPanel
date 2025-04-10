
from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import UserModel
from module_ai.entity.vo.knowledge_base_vo import KnowledgeBaseModel, KnowledgeBasePageModel
from module_ai.service.knowledge_base_service import KnowledgeBaseService
from utils.response_util import ResponseUtil, ResponseCode
from config.database import get_db

router = APIRouter(
    prefix="/ai/knowledge-base",
    tags=["AI知识库管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", summary="获取知识库列表")
async def get_knowledge_base_list(
    query_object: KnowledgeBasePageModel = Depends(KnowledgeBasePageModel.as_query),
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取知识库列表
    """
    data_scope_sql = LoginService.get_data_scope_sql(current_user)
    knowledge_base_list = await KnowledgeBaseService.get_knowledge_base_list(query_db, query_object, data_scope_sql)
    return ResponseUtil.success(knowledge_base_list)


@router.get("/{knowledge_base_id}", summary="获取知识库详情")
async def get_knowledge_base_detail(
    knowledge_base_id: int,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取知识库详情
    """
    knowledge_base = await KnowledgeBaseService.get_knowledge_base_by_id(query_db, knowledge_base_id)
    return ResponseUtil.success(knowledge_base)


@router.post("", summary="添加知识库")
async def add_knowledge_base(
    knowledge_base_model: KnowledgeBaseModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    添加知识库
    """
    knowledge_base_model.create_by = current_user.user_id
    knowledge_base_model.dept_id = current_user.dept_id
    knowledge_base = await KnowledgeBaseService.add_knowledge_base(query_db, knowledge_base_model)
    return ResponseUtil.success(knowledge_base)


@router.put("", summary="更新知识库")
async def update_knowledge_base(
    knowledge_base_model: KnowledgeBaseModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    更新知识库
    """
    knowledge_base = await KnowledgeBaseService.update_knowledge_base(query_db, knowledge_base_model)
    return ResponseUtil.success(knowledge_base)


@router.delete("/{knowledge_base_ids}", summary="删除知识库")
async def delete_knowledge_base(
    knowledge_base_ids: str,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    删除知识库
    """
    knowledge_base_id_list = knowledge_base_ids.split(",")
    await KnowledgeBaseService.del_knowledge_base(query_db, knowledge_base_id_list)
    return ResponseUtil.success()


from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import UserModel
from module_ai.entity.vo.knowledge_item_vo import KnowledgeItemModel, KnowledgeItemPageModel
from module_ai.service.knowledge_item_service import KnowledgeItemService
from utils.response_util import ResponseUtil
from config.constant import HttpStatusConstant
from config.database import get_db

router = APIRouter(
    prefix="/ai/knowledge-item",
    tags=["AI知识库项目管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", summary="获取知识库项目列表")
async def get_knowledge_item_list(
    query_object: KnowledgeItemPageModel = Depends(KnowledgeItemPageModel.as_query),
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取知识库项目列表
    """
    data_scope_sql = "True"
    knowledge_item_list = await KnowledgeItemService.get_knowledge_item_list(query_db, query_object, data_scope_sql)
    return ResponseUtil.success(knowledge_item_list)


@router.get("/{knowledge_item_id}", summary="获取知识库项目详情")
async def get_knowledge_item_detail(
    knowledge_item_id: int,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取知识库项目详情
    """
    knowledge_item = await KnowledgeItemService.get_knowledge_item_by_id(query_db, knowledge_item_id)
    return ResponseUtil.success(knowledge_item)


@router.post("", summary="添加知识库项目")
async def add_knowledge_item(
    knowledge_item_model: KnowledgeItemModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    添加知识库项目
    """
    knowledge_item_model.create_by = current_user.user_id
    knowledge_item_model.dept_id = current_user.dept_id
    knowledge_item = await KnowledgeItemService.add_knowledge_item(query_db, knowledge_item_model)
    return ResponseUtil.success(knowledge_item)


@router.put("", summary="更新知识库项目")
async def update_knowledge_item(
    knowledge_item_model: KnowledgeItemModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    更新知识库项目
    """
    knowledge_item = await KnowledgeItemService.update_knowledge_item(query_db, knowledge_item_model)
    return ResponseUtil.success(knowledge_item)


@router.delete("/{knowledge_item_ids}", summary="删除知识库项目")
async def delete_knowledge_item(
    knowledge_item_ids: str,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    删除知识库项目
    """
    knowledge_item_id_list = knowledge_item_ids.split(",")
    await KnowledgeItemService.del_knowledge_item(query_db, knowledge_item_id_list)
    return ResponseUtil.success()

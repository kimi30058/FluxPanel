
from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import UserModel
from module_ai.entity.vo.assistant_vo import AssistantModel, AssistantPageModel
from module_ai.service.assistant_service import AssistantService
from utils.response_util import ResponseUtil
from config.constant import HttpStatusConstant
from config.database import get_db

router = APIRouter(
    prefix="/ai/assistant",
    tags=["AI助手管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", summary="获取AI助手列表")
async def get_assistant_list(
    query_object: AssistantPageModel = Depends(AssistantPageModel.as_query),
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取AI助手列表
    """
    data_scope_sql = LoginService.get_data_scope_sql(current_user)
    assistant_list = await AssistantService.get_assistant_list(query_db, query_object, data_scope_sql)
    return ResponseUtil.success(assistant_list)


@router.get("/{assistant_id}", summary="获取AI助手详情")
async def get_assistant_detail(
    assistant_id: int,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取AI助手详情
    """
    assistant = await AssistantService.get_assistant_by_id(query_db, assistant_id)
    return ResponseUtil.success(assistant)


@router.post("", summary="添加AI助手")
async def add_assistant(
    assistant_model: AssistantModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    添加AI助手
    """
    assistant_model.create_by = current_user.user_id
    assistant_model.dept_id = current_user.dept_id
    assistant = await AssistantService.add_assistant(query_db, assistant_model)
    return ResponseUtil.success(assistant)


@router.put("", summary="更新AI助手")
async def update_assistant(
    assistant_model: AssistantModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    更新AI助手
    """
    assistant = await AssistantService.update_assistant(query_db, assistant_model)
    return ResponseUtil.success(assistant)


@router.delete("/{assistant_ids}", summary="删除AI助手")
async def delete_assistant(
    assistant_ids: str,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    删除AI助手
    """
    assistant_id_list = assistant_ids.split(",")
    await AssistantService.del_assistant(query_db, assistant_id_list)
    return ResponseUtil.success()

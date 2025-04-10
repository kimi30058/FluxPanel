
from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import UserModel
from module_ai.entity.vo.message_vo import MessageModel, MessagePageModel
from module_ai.service.message_service import MessageService
from utils.response_util import ResponseUtil, ResponseCode
from config.database import get_db

router = APIRouter(
    prefix="/ai/message",
    tags=["AI对话消息管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", summary="获取对话消息列表")
async def get_message_list(
    query_object: MessagePageModel = Depends(MessagePageModel.as_query),
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取对话消息列表
    """
    data_scope_sql = LoginService.get_data_scope_sql(current_user)
    message_list = await MessageService.get_message_list(query_db, query_object, data_scope_sql)
    return ResponseUtil.success(message_list)


@router.get("/{message_id}", summary="获取对话消息详情")
async def get_message_detail(
    message_id: int,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取对话消息详情
    """
    message = await MessageService.get_message_by_id(query_db, message_id)
    return ResponseUtil.success(message)


@router.post("", summary="添加对话消息")
async def add_message(
    message_model: MessageModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    添加对话消息
    """
    message_model.create_by = current_user.user_id
    message_model.dept_id = current_user.dept_id
    message = await MessageService.add_message(query_db, message_model)
    return ResponseUtil.success(message)


@router.put("", summary="更新对话消息")
async def update_message(
    message_model: MessageModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    更新对话消息
    """
    message = await MessageService.update_message(query_db, message_model)
    return ResponseUtil.success(message)


@router.delete("/{message_ids}", summary="删除对话消息")
async def delete_message(
    message_ids: str,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    删除对话消息
    """
    message_id_list = message_ids.split(",")
    await MessageService.del_message(query_db, message_id_list)
    return ResponseUtil.success()

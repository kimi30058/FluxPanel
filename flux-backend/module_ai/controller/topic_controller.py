
from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import UserModel
from module_ai.entity.vo.topic_vo import TopicModel, TopicPageModel
from module_ai.service.topic_service import TopicService
from utils.response_util import ResponseUtil, ResponseCode
from config.database import get_db

router = APIRouter(
    prefix="/ai/topic",
    tags=["AI对话主题管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", summary="获取对话主题列表")
async def get_topic_list(
    query_object: TopicPageModel = Depends(TopicPageModel.as_query),
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取对话主题列表
    """
    data_scope_sql = LoginService.get_data_scope_sql(current_user)
    topic_list = await TopicService.get_topic_list(query_db, query_object, data_scope_sql)
    return ResponseUtil.success(topic_list)


@router.get("/{topic_id}", summary="获取对话主题详情")
async def get_topic_detail(
    topic_id: int,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取对话主题详情
    """
    topic = await TopicService.get_topic_by_id(query_db, topic_id)
    return ResponseUtil.success(topic)


@router.post("", summary="添加对话主题")
async def add_topic(
    topic_model: TopicModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    添加对话主题
    """
    topic_model.create_by = current_user.user_id
    topic_model.dept_id = current_user.dept_id
    topic = await TopicService.add_topic(query_db, topic_model)
    return ResponseUtil.success(topic)


@router.put("", summary="更新对话主题")
async def update_topic(
    topic_model: TopicModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    更新对话主题
    """
    topic = await TopicService.update_topic(query_db, topic_model)
    return ResponseUtil.success(topic)


@router.delete("/{topic_ids}", summary="删除对话主题")
async def delete_topic(
    topic_ids: str,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    删除对话主题
    """
    topic_id_list = topic_ids.split(",")
    await TopicService.del_topic(query_db, topic_id_list)
    return ResponseUtil.success()

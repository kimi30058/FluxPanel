
from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import UserModel
from module_ai.entity.vo.model_vo import ModelModel, ModelPageModel
from module_ai.service.model_service import ModelService
from utils.response_util import ResponseUtil, ResponseCode
from config.database import get_db

router = APIRouter(
    prefix="/ai/model",
    tags=["AI模型管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", summary="获取AI模型列表")
async def get_model_list(
    query_object: ModelPageModel = Depends(ModelPageModel.as_query),
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取AI模型列表
    """
    data_scope_sql = LoginService.get_data_scope_sql(current_user)
    model_list = await ModelService.get_model_list(query_db, query_object, data_scope_sql)
    return ResponseUtil.success(model_list)


@router.get("/{model_id}", summary="获取AI模型详情")
async def get_model_detail(
    model_id: int,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取AI模型详情
    """
    model = await ModelService.get_model_by_id(query_db, model_id)
    return ResponseUtil.success(model)


@router.post("", summary="添加AI模型")
async def add_model(
    model_model: ModelModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    添加AI模型
    """
    model_model.create_by = current_user.user_id
    model_model.dept_id = current_user.dept_id
    model = await ModelService.add_model(query_db, model_model)
    return ResponseUtil.success(model)


@router.put("", summary="更新AI模型")
async def update_model(
    model_model: ModelModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    更新AI模型
    """
    model = await ModelService.update_model(query_db, model_model)
    return ResponseUtil.success(model)


@router.delete("/{model_ids}", summary="删除AI模型")
async def delete_model(
    model_ids: str,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    删除AI模型
    """
    model_id_list = model_ids.split(",")
    await ModelService.del_model(query_db, model_id_list)
    return ResponseUtil.success()

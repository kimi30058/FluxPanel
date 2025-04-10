
from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import UserModel
from module_ai.entity.vo.provider_vo import ProviderModel, ProviderPageModel
from module_ai.service.provider_service import ProviderService
from utils.response_util import ResponseUtil
from config.constant import HttpStatusConstant
from config.database import get_db

router = APIRouter(
    prefix="/ai/provider",
    tags=["AI提供商管理"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", summary="获取AI提供商列表")
async def get_provider_list(
    query_object: ProviderPageModel = Depends(ProviderPageModel.as_query),
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取AI提供商列表
    """
    data_scope_sql = "True"
    provider_list = await ProviderService.get_provider_list(query_db, query_object, data_scope_sql)
    return ResponseUtil.success(provider_list)


@router.get("/{provider_id}", summary="获取AI提供商详情")
async def get_provider_detail(
    provider_id: int,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    获取AI提供商详情
    """
    provider = await ProviderService.get_provider_by_id(query_db, provider_id)
    return ResponseUtil.success(provider)


@router.post("", summary="添加AI提供商")
async def add_provider(
    provider_model: ProviderModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    添加AI提供商
    """
    provider_model.create_by = current_user.user_id
    provider_model.dept_id = current_user.dept_id
    provider = await ProviderService.add_provider(query_db, provider_model)
    return ResponseUtil.success(provider)


@router.put("", summary="更新AI提供商")
async def update_provider(
    provider_model: ProviderModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    更新AI提供商
    """
    provider = await ProviderService.update_provider(query_db, provider_model)
    return ResponseUtil.success(provider)


@router.delete("/{provider_ids}", summary="删除AI提供商")
async def delete_provider(
    provider_ids: str,
    current_user: UserModel = Depends(LoginService.get_current_user),
    query_db: AsyncSession = Depends(get_db)
):
    """
    删除AI提供商
    """
    provider_id_list = provider_ids.split(",")
    await ProviderService.del_provider(query_db, provider_id_list)
    return ResponseUtil.success()

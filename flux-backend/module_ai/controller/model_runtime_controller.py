from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional

from config.get_db import get_db
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_ai.service.model_runtime_service import ModelRuntimeService
from utils.log_util import logger
from utils.response_util import ResponseUtil

modelRuntimeController = APIRouter(prefix='/ai/model-runtime', dependencies=[Depends(LoginService.get_current_user)])


@modelRuntimeController.get('/providers', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:query'))])
async def get_model_providers(
    request: Request,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取所有模型提供商信息"""
    providers_result = await ModelRuntimeService.get_model_providers_services(query_db, current_user)
    logger.info('获取模型提供商信息成功')
    
    return ResponseUtil.success(dict_content=providers_result)


@modelRuntimeController.get('/models/{provider}/{model_type}', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:query'))])
async def get_models_by_provider_and_type(
    request: Request,
    provider: str,
    model_type: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取特定提供商和模型类型的模型列表"""
    models_result = await ModelRuntimeService.get_models_by_provider_and_type_services(
        query_db, provider, model_type, current_user
    )
    logger.info(f'获取{provider}提供商的{model_type}类型模型列表成功')
    
    return ResponseUtil.success(dict_content=models_result)


@modelRuntimeController.post('/credentials/validate', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:edit'))])
async def validate_provider_credentials(
    request: Request,
    credentials: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """验证模型提供商凭据"""
    validation_result = await ModelRuntimeService.validate_provider_credentials_services(
        query_db, credentials, current_user
    )
    logger.info('验证模型提供商凭据完成')
    
    return ResponseUtil.success(dict_content=validation_result)

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional

from config.get_db import get_db
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_ai.service.ai_provider_service import (
    TraditionalProviderService, 
    DifyApplicationService, 
    CozeApplicationService, 
    AIApplicationService
)
from utils.log_util import logger
from utils.response_util import ResponseUtil

aiProviderController = APIRouter(prefix='/ai/provider', dependencies=[Depends(LoginService.get_current_user)])


@aiProviderController.get('/traditional/list', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:query'))])
async def get_traditional_provider_list(
    request: Request,
    is_active: Optional[bool] = None,
    provider_type: Optional[str] = None,
    page_num: int = 1,
    page_size: int = 10,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取传统AI供应商列表"""
    result = await TraditionalProviderService.get_provider_list(
        db=query_db,
        is_active=is_active,
        provider_type=provider_type,
        page_num=page_num,
        page_size=page_size,
        current_user=current_user
    )
    logger.info('获取传统AI供应商列表成功')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.get('/traditional/{provider_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:query'))])
async def get_traditional_provider(
    request: Request,
    provider_id: int,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取传统AI供应商详情"""
    result = await TraditionalProviderService.get_provider_by_id(
        db=query_db,
        provider_id=provider_id,
        current_user=current_user
    )
    logger.info(f'获取传统AI供应商详情成功: {provider_id}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.post('/traditional', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:add'))])
async def add_traditional_provider(
    request: Request,
    provider_data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """添加传统AI供应商"""
    result = await TraditionalProviderService.add_provider(
        db=query_db,
        provider_data=provider_data,
        current_user=current_user
    )
    logger.info('添加传统AI供应商成功')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.put('/traditional/{provider_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:edit'))])
async def update_traditional_provider(
    request: Request,
    provider_id: int,
    provider_data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """更新传统AI供应商"""
    result = await TraditionalProviderService.update_provider(
        db=query_db,
        provider_id=provider_id,
        provider_data=provider_data,
        current_user=current_user
    )
    logger.info(f'更新传统AI供应商成功: {provider_id}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.delete('/traditional', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:remove'))])
async def delete_traditional_provider(
    request: Request,
    provider_ids: List[int],
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """删除传统AI供应商"""
    result = await TraditionalProviderService.delete_provider(
        db=query_db,
        provider_ids=provider_ids,
        current_user=current_user
    )
    logger.info(f'删除传统AI供应商成功: {provider_ids}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.get('/dify/list', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:query'))])
async def get_dify_app_list(
    request: Request,
    is_active: Optional[bool] = None,
    page_num: int = 1,
    page_size: int = 10,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取Dify应用列表"""
    result = await DifyApplicationService.get_app_list(
        db=query_db,
        is_active=is_active,
        page_num=page_num,
        page_size=page_size,
        current_user=current_user
    )
    logger.info('获取Dify应用列表成功')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.get('/dify/{app_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:query'))])
async def get_dify_app(
    request: Request,
    app_id: int,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取Dify应用详情"""
    result = await DifyApplicationService.get_app_by_id(
        db=query_db,
        app_id=app_id,
        current_user=current_user
    )
    logger.info(f'获取Dify应用详情成功: {app_id}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.post('/dify', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:add'))])
async def add_dify_app(
    request: Request,
    app_data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """添加Dify应用"""
    result = await DifyApplicationService.add_app(
        db=query_db,
        app_data=app_data,
        current_user=current_user
    )
    logger.info('添加Dify应用成功')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.put('/dify/{app_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:edit'))])
async def update_dify_app(
    request: Request,
    app_id: int,
    app_data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """更新Dify应用"""
    result = await DifyApplicationService.update_app(
        db=query_db,
        app_id=app_id,
        app_data=app_data,
        current_user=current_user
    )
    logger.info(f'更新Dify应用成功: {app_id}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.delete('/dify', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:remove'))])
async def delete_dify_app(
    request: Request,
    app_ids: List[int],
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """删除Dify应用"""
    result = await DifyApplicationService.delete_app(
        db=query_db,
        app_ids=app_ids,
        current_user=current_user
    )
    logger.info(f'删除Dify应用成功: {app_ids}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.get('/coze/list', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:query'))])
async def get_coze_app_list(
    request: Request,
    is_active: Optional[bool] = None,
    page_num: int = 1,
    page_size: int = 10,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取Coze应用列表"""
    result = await CozeApplicationService.get_app_list(
        db=query_db,
        is_active=is_active,
        page_num=page_num,
        page_size=page_size,
        current_user=current_user
    )
    logger.info('获取Coze应用列表成功')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.get('/coze/{app_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:query'))])
async def get_coze_app(
    request: Request,
    app_id: int,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取Coze应用详情"""
    result = await CozeApplicationService.get_app_by_id(
        db=query_db,
        app_id=app_id,
        current_user=current_user
    )
    logger.info(f'获取Coze应用详情成功: {app_id}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.post('/coze', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:add'))])
async def add_coze_app(
    request: Request,
    app_data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """添加Coze应用"""
    result = await CozeApplicationService.add_app(
        db=query_db,
        app_data=app_data,
        current_user=current_user
    )
    logger.info('添加Coze应用成功')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.put('/coze/{app_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:edit'))])
async def update_coze_app(
    request: Request,
    app_id: int,
    app_data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """更新Coze应用"""
    result = await CozeApplicationService.update_app(
        db=query_db,
        app_id=app_id,
        app_data=app_data,
        current_user=current_user
    )
    logger.info(f'更新Coze应用成功: {app_id}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.delete('/coze', dependencies=[Depends(CheckUserInterfaceAuth('ai:provider:remove'))])
async def delete_coze_app(
    request: Request,
    app_ids: List[int],
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """删除Coze应用"""
    result = await CozeApplicationService.delete_app(
        db=query_db,
        app_ids=app_ids,
        current_user=current_user
    )
    logger.info(f'删除Coze应用成功: {app_ids}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.get('/application/list', dependencies=[Depends(CheckUserInterfaceAuth('ai:application:query'))])
async def get_ai_app_list(
    request: Request,
    type: Optional[str] = None,
    is_enabled: Optional[bool] = None,
    page_num: int = 1,
    page_size: int = 10,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取AI应用列表"""
    result = await AIApplicationService.get_app_list(
        db=query_db,
        type=type,
        is_enabled=is_enabled,
        page_num=page_num,
        page_size=page_size,
        current_user=current_user
    )
    logger.info('获取AI应用列表成功')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.get('/application/{app_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:application:query'))])
async def get_ai_app(
    request: Request,
    app_id: int,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取AI应用详情"""
    result = await AIApplicationService.get_app_by_id(
        db=query_db,
        app_id=app_id,
        current_user=current_user
    )
    logger.info(f'获取AI应用详情成功: {app_id}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.get('/application/{app_id}/context', dependencies=[Depends(CheckUserInterfaceAuth('ai:application:query'))])
async def get_app_context_settings(
    request: Request,
    app_id: int,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取AI应用上下文设置"""
    app = await AIApplicationService.get_app_by_id(
        db=query_db,
        app_id=app_id,
        current_user=current_user
    )
    
    if not app or app.get("code") != 200:
        return ResponseUtil.failed(message=f"获取AI应用失败: {app_id}")
    
    app_data = app.get("data", {})
    context_settings = {
        "max_context_turns": getattr(app_data, "max_context_turns", 10),
        "max_tokens": getattr(app_data, "max_tokens", 4000),
        "preserve_system_prompt": getattr(app_data, "preserve_system_prompt", True)
    }
    
    logger.info(f'获取AI应用上下文设置成功: {app_id}')
    
    return ResponseUtil.success(dict_content=context_settings)


@aiProviderController.post('/application', dependencies=[Depends(CheckUserInterfaceAuth('ai:application:add'))])
async def add_ai_app(
    request: Request,
    app_data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """添加AI应用"""
    if 'max_context_turns' not in app_data:
        app_data['max_context_turns'] = 10
    if 'max_tokens' not in app_data:
        app_data['max_tokens'] = 4000
    if 'preserve_system_prompt' not in app_data:
        app_data['preserve_system_prompt'] = True
        
    result = await AIApplicationService.add_app(
        db=query_db,
        app_data=app_data,
        current_user=current_user
    )
    logger.info('添加AI应用成功')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.put('/application/{app_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:application:edit'))])
async def update_ai_app(
    request: Request,
    app_id: int,
    app_data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """更新AI应用"""
    result = await AIApplicationService.update_app(
        db=query_db,
        app_id=app_id,
        app_data=app_data,
        current_user=current_user
    )
    logger.info(f'更新AI应用成功: {app_id}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.put('/application/{app_id}/context', dependencies=[Depends(CheckUserInterfaceAuth('ai:application:edit'))])
async def update_app_context_settings(
    request: Request,
    app_id: int,
    context_data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """更新AI应用上下文设置"""
    context_settings = {
        "max_context_turns": context_data.get("max_context_turns", 10),
        "max_tokens": context_data.get("max_tokens", 4000),
        "preserve_system_prompt": context_data.get("preserve_system_prompt", True)
    }
    
    result = await AIApplicationService.update_app(
        db=query_db,
        app_id=app_id,
        app_data=context_settings,
        current_user=current_user
    )
    logger.info(f'更新AI应用上下文设置成功: {app_id}')
    
    return ResponseUtil.success(dict_content=result)


@aiProviderController.delete('/application', dependencies=[Depends(CheckUserInterfaceAuth('ai:application:remove'))])
async def delete_ai_app(
    request: Request,
    app_ids: List[int],
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """删除AI应用"""
    result = await AIApplicationService.delete_app(
        db=query_db,
        app_ids=app_ids,
        current_user=current_user
    )
    logger.info(f'删除AI应用成功: {app_ids}')
    
    return ResponseUtil.success(dict_content=result)

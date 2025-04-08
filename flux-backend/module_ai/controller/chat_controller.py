from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional

from config.get_db import get_db
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_ai.service.chat_service import ChatService
from utils.log_util import logger
from utils.response_util import ResponseUtil

chatController = APIRouter(prefix='/ai/chat', dependencies=[Depends(LoginService.get_current_user)])


@chatController.get('/list', dependencies=[Depends(CheckUserInterfaceAuth('ai:chat:query'))])
async def get_chat_list(
    request: Request,
    app_id: Optional[int] = None,
    page_num: int = 1,
    page_size: int = 10,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取聊天会话列表"""
    result = await ChatService.get_chat_list(
        db=query_db,
        user_id=current_user.user_id,
        app_id=app_id,
        page_num=page_num,
        page_size=page_size,
        current_user=current_user
    )
    logger.info('获取聊天会话列表成功')
    
    return ResponseUtil.success(dict_content=result)


@chatController.get('/{chat_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:chat:query'))])
async def get_chat(
    request: Request,
    chat_id: int,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取聊天会话详情"""
    result = await ChatService.get_chat_by_id(
        db=query_db,
        chat_id=chat_id,
        current_user=current_user
    )
    logger.info(f'获取聊天会话详情成功: {chat_id}')
    
    return ResponseUtil.success(dict_content=result)


@chatController.post('/create', dependencies=[Depends(CheckUserInterfaceAuth('ai:chat:add'))])
async def create_chat(
    request: Request,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """创建聊天会话"""
    result = await ChatService.create_chat(
        db=query_db,
        user_id=current_user.user_id,
        app_id=data.get('app_id'),
        title=data.get('title', '新聊天'),
        system_prompt=data.get('system_prompt'),
        current_user=current_user
    )
    logger.info('创建聊天会话成功')
    
    return ResponseUtil.success(dict_content=result)


@chatController.put('/{chat_id}/rename', dependencies=[Depends(CheckUserInterfaceAuth('ai:chat:edit'))])
async def rename_chat(
    request: Request,
    chat_id: int,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """重命名聊天会话"""
    result = await ChatService.rename_chat(
        db=query_db,
        chat_id=chat_id,
        title=data.get('title'),
        current_user=current_user
    )
    logger.info(f'重命名聊天会话成功: {chat_id}')
    
    return ResponseUtil.success(dict_content=result)


@chatController.delete('/{chat_id}', dependencies=[Depends(CheckUserInterfaceAuth('ai:chat:remove'))])
async def delete_chat(
    request: Request,
    chat_id: int,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """删除聊天会话"""
    result = await ChatService.delete_chat(
        db=query_db,
        chat_id=chat_id,
        current_user=current_user
    )
    logger.info(f'删除聊天会话成功: {chat_id}')
    
    return ResponseUtil.success(dict_content=result)


@chatController.get('/{chat_id}/messages', dependencies=[Depends(CheckUserInterfaceAuth('ai:chat:query'))])
async def get_chat_messages(
    request: Request,
    chat_id: int,
    page_num: int = 1,
    page_size: int = 20,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取聊天消息列表"""
    result = await ChatService.get_chat_messages(
        db=query_db,
        chat_id=chat_id,
        page_num=page_num,
        page_size=page_size,
        current_user=current_user
    )
    logger.info(f'获取聊天消息列表成功: {chat_id}')
    
    return ResponseUtil.success(dict_content=result)


@chatController.post('/{chat_id}/message', dependencies=[Depends(CheckUserInterfaceAuth('ai:chat:add'))])
async def send_message(
    request: Request,
    chat_id: int,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """发送消息"""
    result = await ChatService.send_message(
        db=query_db,
        chat_id=chat_id,
        user_id=current_user.user_id,
        content=data.get('content'),
        current_user=current_user
    )
    logger.info(f'发送消息成功: {chat_id}')
    
    return ResponseUtil.success(dict_content=result)

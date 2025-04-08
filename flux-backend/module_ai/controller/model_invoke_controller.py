from fastapi import APIRouter, Depends, File, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional, Union
from io import BytesIO

from config.get_db import get_db
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_ai.service.model_invoke_service import ModelInvokeService
from utils.log_util import logger
from utils.response_util import ResponseUtil

modelInvokeController = APIRouter(prefix='/ai/model-invoke', dependencies=[Depends(LoginService.get_current_user)])


@modelInvokeController.post('/llm', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:invoke'))])
async def invoke_llm(
    request: Request,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """调用大语言模型"""
    result = await ModelInvokeService.invoke_llm_services(
        db=query_db, 
        provider=data.get('provider'),
        model=data.get('model'),
        prompt_messages=data.get('prompt_messages'),
        model_parameters=data.get('model_parameters'),
        tools=data.get('tools'),
        stop=data.get('stop'),
        stream=data.get('stream', False),
        current_user=current_user
    )
    logger.info('调用大语言模型成功')
    
    return ResponseUtil.success(dict_content=result)


@modelInvokeController.post('/embedding', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:invoke'))])
async def invoke_embedding(
    request: Request,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """调用文本嵌入模型"""
    result = await ModelInvokeService.invoke_embedding_services(
        db=query_db, 
        provider=data.get('provider'),
        model=data.get('model'),
        texts=data.get('texts'),
        input_type=data.get('input_type'),
        current_user=current_user
    )
    logger.info('调用文本嵌入模型成功')
    
    return ResponseUtil.success(dict_content=result)


@modelInvokeController.post('/rerank', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:invoke'))])
async def invoke_rerank(
    request: Request,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """调用重排序模型"""
    result = await ModelInvokeService.invoke_rerank_services(
        db=query_db, 
        provider=data.get('provider'),
        model=data.get('model'),
        query=data.get('query'),
        docs=data.get('docs'),
        score_threshold=data.get('score_threshold'),
        top_n=data.get('top_n'),
        current_user=current_user
    )
    logger.info('调用重排序模型成功')
    
    return ResponseUtil.success(dict_content=result)


@modelInvokeController.post('/moderation', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:invoke'))])
async def invoke_moderation(
    request: Request,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """调用内容审核模型"""
    result = await ModelInvokeService.invoke_moderation_services(
        db=query_db, 
        provider=data.get('provider'),
        model=data.get('model'),
        text=data.get('text'),
        current_user=current_user
    )
    logger.info('调用内容审核模型成功')
    
    return ResponseUtil.success(dict_content=result)


@modelInvokeController.post('/speech2text', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:invoke'))])
async def invoke_speech2text(
    request: Request,
    file: UploadFile = File(...),
    provider: str = None,
    model: str = None,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """调用语音转文本模型"""
    file_bytes = await file.read()
    file_io = BytesIO(file_bytes)
    
    result = await ModelInvokeService.invoke_speech2text_services(
        db=query_db, 
        provider=provider,
        model=model,
        file=file_io,
        current_user=current_user
    )
    logger.info('调用语音转文本模型成功')
    
    return ResponseUtil.success(dict_content=result)


@modelInvokeController.post('/tts', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:invoke'))])
async def invoke_tts(
    request: Request,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """调用文本转语音模型"""
    result = await ModelInvokeService.invoke_tts_services(
        db=query_db, 
        provider=data.get('provider'),
        model=data.get('model'),
        content_text=data.get('content_text'),
        voice=data.get('voice'),
        current_user=current_user
    )
    logger.info('调用文本转语音模型成功')
    
    return ResponseUtil.streaming(data=result)


@modelInvokeController.get('/tts/voices', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:query'))])
async def get_tts_voices(
    request: Request,
    provider: str,
    model: str,
    language: Optional[str] = None,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """获取文本转语音模型的声音列表"""
    result = await ModelInvokeService.get_tts_voices_services(
        db=query_db, 
        provider=provider,
        model=model,
        language=language,
        current_user=current_user
    )
    logger.info('获取文本转语音模型声音列表成功')
    
    return ResponseUtil.success(dict_content=result)

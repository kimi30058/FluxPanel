from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import UserModel
from module_ai.entity.vo.message_vo import MessageModel
from module_ai.service.provider_service import ProviderService
from utils.response_util import ResponseUtil
from config.constant import HttpStatusConstant
from config.database import get_db
import httpx
import json

router = APIRouter(
    prefix="/ai/deepseek",
    tags=["DeepSeek集成"],
    responses={404: {"description": "Not found"}},
)

@router.post("/chat", summary="DeepSeek聊天接口")
async def chat_endpoint(
    request: dict,
    provider_id: int = Query(..., description="AI提供商ID"),
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    DeepSeek聊天接口，非流式响应
    """
    try:
        provider = await ProviderService.get_provider_by_id(db, provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="AI提供商不存在")
        
        if provider.type.lower() != "deepseek":
            raise HTTPException(status_code=400, detail="提供商类型不是DeepSeek")
        
        headers = {
            "Authorization": f"Bearer {provider.apiKey}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(base_url=provider.apiHost) as client:
            response = await client.post(
                f"/v1/chat/completions",
                headers=headers,
                json=request
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"DeepSeek API错误: {response.text}"
                )
                
            return ResponseUtil.success(response.json())
            
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"发送消息失败: {str(e)}"
        )

@router.post("/chat/stream", summary="DeepSeek流式聊天接口")
async def chat_stream_endpoint(
    request: dict,
    provider_id: int = Query(..., description="AI提供商ID"),
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    DeepSeek流式聊天接口
    """
    try:
        provider = await ProviderService.get_provider_by_id(db, provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="AI提供商不存在")
        
        if provider.type.lower() != "deepseek":
            raise HTTPException(status_code=400, detail="提供商类型不是DeepSeek")
        
        headers = {
            "Authorization": f"Bearer {provider.apiKey}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        request["stream"] = True
        
        async def generate():
            async with httpx.AsyncClient(base_url=provider.apiHost) as client:
                async with client.stream(
                    "POST",
                    f"/v1/chat/completions",
                    headers=headers,
                    json=request,
                    timeout=60.0
                ) as response:
                    if response.status_code != 200:
                        error_detail = await response.aread()
                        error_msg = f'DeepSeek API错误: {error_detail.decode("utf-8")}'
                        yield f"data: {json.dumps({'error': error_msg})} \n\n"
                        return
                    
                    async for chunk in response.aiter_text():
                        if chunk.strip():
                            yield f"data: {chunk} \n\n"
        
        return generate()
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"流式发送消息失败: {str(e)}"
        )

@router.post("/reasoner", summary="DeepSeek推理模型接口")
async def reasoner_endpoint(
    request: dict,
    provider_id: int = Query(..., description="AI提供商ID"),
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    DeepSeek-R1推理模型接口
    """
    try:
        provider = await ProviderService.get_provider_by_id(db, provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="AI提供商不存在")
        
        if provider.type.lower() != "deepseek":
            raise HTTPException(status_code=400, detail="提供商类型不是DeepSeek")
        
        headers = {
            "Authorization": f"Bearer {provider.apiKey}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(base_url=provider.apiHost) as client:
            response = await client.post(
                f"/v1/reasoner",
                headers=headers,
                json=request
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"DeepSeek Reasoner API错误: {response.text}"
                )
                
            return ResponseUtil.success(response.json())
            
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"推理请求失败: {str(e)}"
        )

@router.post("/save_chat", summary="保存DeepSeek聊天记录")
async def save_chat_endpoint(
    request: dict,
    background_tasks: BackgroundTasks,
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    保存DeepSeek聊天记录到数据库
    """
    try:
        messages = request.get("messages", [])
        app_id = request.get("app_id")
        title = request.get("title", f"DeepSeek对话 {len(messages)} 条消息")
        
        from module_ai.entity.vo.chat_vo import ChatModel
        from module_ai.service.chat_service import ChatService
        
        chat_model = ChatModel(
            title=title,
            userId=current_user.user_id,
            providerId=request.get("provider_id"),
            appId=app_id
        )
        
        chat = await ChatService.create_chat(db, chat_model)
        
        from module_ai.service.message_service import MessageService
        
        def add_messages_task():
            for msg in messages:
                message_model = MessageModel(
                    chatId=chat.id,
                    role=msg.get("role"),
                    content=msg.get("content"),
                    userId=current_user.user_id
                )
                MessageService.add_message_sync(db, message_model)
        
        background_tasks.add_task(add_messages_task)
        
        return ResponseUtil.success({
            "success": True,
            "chat_id": chat.id,
            "message_count": len(messages)
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"保存聊天记录失败: {str(e)}"
        )

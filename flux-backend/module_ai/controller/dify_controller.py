from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.login_service import LoginService
from module_admin.entity.vo.user_vo import UserModel
from module_ai.entity.vo.message_vo import MessageModel
from module_ai.entity.vo.chat_vo import ChatModel, ChatPageModel, ChatRenameModel
from module_ai.service.provider_service import ProviderService
from utils.response_util import ResponseUtil
from config.constant import HttpStatusConstant
from config.database import get_db
import httpx
import json

router = APIRouter(
    prefix="/ai/dify",
    tags=["DIFY集成"],
    responses={404: {"description": "Not found"}},
)

@router.post("/chat", summary="发送聊天消息")
async def chat(
    request: dict,
    provider_id: int = Query(..., description="AI提供商ID"),
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    向DIFY发送聊天消息并获取回复，支持阻塞模式
    """
    try:
        provider = await ProviderService.get_provider_by_id(db, provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="AI提供商不存在")
        
        if provider.type.lower() != "dify":
            raise HTTPException(status_code=400, detail="提供商类型不是DIFY")
        
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
                    detail=f"DIFY API错误: {response.text}"
                )
                
            return ResponseUtil.success(response.json())
            
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"发送消息失败: {str(e)}"
        )

@router.post("/chat/stream", summary="流式发送聊天消息")
async def chat_stream(
    request: dict,
    provider_id: int = Query(..., description="AI提供商ID"),
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    向DIFY发送聊天消息并获取流式回复
    """
    try:
        provider = await ProviderService.get_provider_by_id(db, provider_id)
        if not provider:
            raise HTTPException(status_code=404, detail="AI提供商不存在")
        
        if provider.type.lower() != "dify":
            raise HTTPException(status_code=400, detail="提供商类型不是DIFY")
        
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
                        error_msg = f'DIFY API错误: {error_detail.decode("utf-8")}'
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

@router.post("/chats", summary="创建聊天会话")
async def create_chat(
    chat_model: ChatModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建一个新的聊天会话
    """
    try:
        chat_model.userId = current_user.user_id
        
        from module_ai.service.chat_service import ChatService
        chat = await ChatService.create_chat(db, chat_model)
        
        return ResponseUtil.success(chat)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建聊天会话失败: {str(e)}"
        )

@router.get("/chats", summary="获取用户聊天列表")
async def get_user_chats(
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db),
    query_object: ChatPageModel = Depends(ChatPageModel.as_query)
):
    """
    获取指定用户的聊天会话列表
    """
    try:
        query_object.userId = current_user.user_id
        
        from module_ai.service.chat_service import ChatService
        chats = await ChatService.get_chat_list(db, query_object)
        
        return ResponseUtil.success(chats)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取聊天会话列表失败: {str(e)}"
        )

@router.post("/chats/{chat_id}/messages", summary="发送消息到现有聊天")
async def send_message(
    chat_id: int,
    message: MessageModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    向已存在的聊天会话发送消息
    """
    try:
        from module_ai.service.chat_service import ChatService
        chat = await ChatService.get_chat_by_id(db, chat_id)
        
        if not chat:
            raise HTTPException(status_code=404, detail="聊天会话不存在")
            
        if chat.userId != current_user.user_id:
            raise HTTPException(status_code=403, detail="无权访问此聊天会话")
        
        message.chatId = chat_id
        
        from module_ai.service.message_service import MessageService
        saved_message = await MessageService.add_message(db, message)
        
        return ResponseUtil.success(saved_message)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"发送消息失败: {str(e)}"
        )

@router.get("/chats/{chat_id}/messages", summary="获取聊天消息列表")
async def get_chat_messages(
    chat_id: int,
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, description="返回条数，默认20条"),
    offset: int = Query(0, description="偏移量，默认0")
):
    """
    获取指定聊天会话的消息列表
    """
    try:
        from module_ai.service.chat_service import ChatService
        chat = await ChatService.get_chat_by_id(db, chat_id)
        
        if not chat:
            raise HTTPException(status_code=404, detail="聊天会话不存在")
            
        if chat.userId != current_user.user_id:
            raise HTTPException(status_code=403, detail="无权访问此聊天会话")
        
        from module_ai.service.message_service import MessageService
        messages = await MessageService.get_messages_by_chat_id(db, chat_id, limit, offset)
        
        return ResponseUtil.success(messages)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取消息列表失败: {str(e)}"
        )

@router.delete("/chats/{chat_id}", summary="删除聊天会话")
async def delete_chat(
    chat_id: int,
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除指定的聊天会话
    """
    try:
        from module_ai.service.chat_service import ChatService
        chat = await ChatService.get_chat_by_id(db, chat_id)
        
        if not chat:
            raise HTTPException(status_code=404, detail="聊天会话不存在")
            
        if chat.userId != current_user.user_id:
            raise HTTPException(status_code=403, detail="无权访问此聊天会话")
        
        await ChatService.delete_chat(db, chat_id)
        
        return ResponseUtil.success({"success": True})
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除聊天会话失败: {str(e)}"
        )

@router.put("/chats/{chat_id}/title", summary="重命名聊天会话")
async def rename_chat(
    chat_id: int,
    rename_data: ChatRenameModel,
    current_user: UserModel = Depends(LoginService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    重命名指定的聊天会话
    """
    try:
        from module_ai.service.chat_service import ChatService
        chat = await ChatService.get_chat_by_id(db, chat_id)
        
        if not chat:
            raise HTTPException(status_code=404, detail="聊天会话不存在")
            
        if chat.userId != current_user.user_id:
            raise HTTPException(status_code=403, detail="无权访问此聊天会话")
        
        chat.title = rename_data.title
        updated_chat = await ChatService.update_chat(db, chat)
        
        return ResponseUtil.success(updated_chat)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"重命名聊天会话失败: {str(e)}"
        )

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional

from config.get_db import get_db
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_ai.utils.token_utils import TokenUtils
from utils.log_util import logger
from utils.response_util import ResponseUtil

tokenController = APIRouter(prefix='/ai/token', dependencies=[Depends(LoginService.get_current_user)])


@tokenController.post('/estimate', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:query'))])
async def estimate_token_usage(
    request: Request,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """估算文本的token用量"""
    try:
        text = data.get("text", "")
        model = data.get("model", "gpt-3.5-turbo")
        
        if not text:
            return ResponseUtil.failed(message="文本不能为空")
            
        token_count = TokenUtils.num_tokens_from_string(text, model)
        
        context_window = TokenUtils.get_model_context_window(model)
        
        result = {
            "token_count": token_count,
            "model": model,
            "context_window": context_window,
            "percentage": round(token_count / context_window * 100, 2) if context_window > 0 else 0
        }
        
        logger.info(f'估算token用量成功: {token_count} tokens')
        
        return ResponseUtil.success(dict_content=result)
    except Exception as e:
        logger.error(f'估算token用量失败: {str(e)}')
        return ResponseUtil.failed(message=f"估算token用量失败: {str(e)}")


@tokenController.post('/format-messages', dependencies=[Depends(CheckUserInterfaceAuth('ai:model:query'))])
async def format_messages_for_model(
    request: Request,
    data: Dict,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """格式化消息以适应模型要求"""
    try:
        messages = data.get("messages", [])
        system_prompt = data.get("system_prompt")
        max_tokens = data.get("max_tokens")
        model = data.get("model", "gpt-3.5-turbo")
        
        if not messages:
            return ResponseUtil.failed(message="消息列表不能为空")
            
        formatted_messages = TokenUtils.format_messages_for_model(
            messages, system_prompt, max_tokens, model
        )
        
        total_tokens = sum(TokenUtils.num_tokens_from_string(msg.get("content", ""), model) 
                          for msg in formatted_messages)
        
        context_window = TokenUtils.get_model_context_window(model)
        
        result = {
            "formatted_messages": formatted_messages,
            "total_tokens": total_tokens,
            "model": model,
            "context_window": context_window,
            "percentage": round(total_tokens / context_window * 100, 2) if context_window > 0 else 0,
            "message_count": len(formatted_messages)
        }
        
        logger.info(f'格式化消息成功: {len(formatted_messages)} 条消息, {total_tokens} tokens')
        
        return ResponseUtil.success(dict_content=result)
    except Exception as e:
        logger.error(f'格式化消息失败: {str(e)}')
        return ResponseUtil.failed(message=f"格式化消息失败: {str(e)}")

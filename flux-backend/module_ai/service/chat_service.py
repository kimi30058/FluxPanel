from typing import Dict, List, Optional, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_ai.dao.chat_dao import ChatDao, ChatMessageDao
from module_ai.dao.ai_provider_dao import AIApplicationDao
from module_ai.entity.do.chat_do import Chat, ChatMessage, MessageRole, MessageStatus
from module_ai.entity.do.ai_do import AIApplication
from utils.service_result_util import ServiceResult


class ChatService:
    """聊天服务"""
    
    @staticmethod
    async def get_chat_list(
        db: AsyncSession, 
        user_id: int,
        app_id: int = None,
        page_num: int = 1, 
        page_size: int = 10,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        获取聊天会话列表
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            app_id: 应用ID
            page_num: 页码
            page_size: 每页条数
            current_user: 当前用户
            
        Returns:
            聊天会话列表
        """
        try:
            result = await ChatDao.get_user_chats(
                db, user_id, app_id, page_num, page_size
            )
            return result
        except Exception as e:
            return ServiceResult.failed(message=f"获取聊天会话列表失败: {str(e)}")
    
    @staticmethod
    async def get_chat_by_id(
        db: AsyncSession, 
        chat_id: int,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        根据ID获取聊天会话
        
        Args:
            db: 数据库会话
            chat_id: 聊天会话ID
            current_user: 当前用户
            
        Returns:
            聊天会话信息
        """
        try:
            chat = await ChatDao.get_by_id(db, chat_id)
            if not chat:
                return ServiceResult.failed(message=f"聊天会话不存在: {chat_id}")
            return chat
        except Exception as e:
            return ServiceResult.failed(message=f"获取聊天会话失败: {str(e)}")
    
    @staticmethod
    async def create_chat(
        db: AsyncSession, 
        user_id: int,
        app_id: int,
        title: str = "新聊天",
        system_prompt: str = None,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        创建聊天会话
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            app_id: 应用ID
            title: 聊天标题
            system_prompt: 系统提示词
            current_user: 当前用户
            
        Returns:
            创建结果
        """
        try:
            app = await AIApplicationDao.get_by_id(db, app_id)
            if not app:
                return ServiceResult.failed(message=f"应用不存在: {app_id}")
            
            chat_data = {
                "user_id": user_id,
                "ai_application_id": app_id,
                "title": title,
                "chat_type": "ai"
            }
            
            if system_prompt:
                chat_data["system_prompt"] = system_prompt
            elif app.system_prompt:
                chat_data["system_prompt"] = app.system_prompt
                
            chat_data["config"] = {
                "temperature": 0.7,
                "top_p": 1.0,
                "max_tokens": 2000
            }
            
            chat = await ChatDao.add(db, chat_data)
            await db.commit()
            
            return ServiceResult.success(data=chat, message="创建聊天会话成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"创建聊天会话失败: {str(e)}")
    
    @staticmethod
    async def rename_chat(
        db: AsyncSession, 
        chat_id: int,
        title: str,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        重命名聊天会话
        
        Args:
            db: 数据库会话
            chat_id: 聊天会话ID
            title: 新标题
            current_user: 当前用户
            
        Returns:
            更新结果
        """
        try:
            chat = await ChatDao.get_by_id(db, chat_id)
            if not chat:
                return ServiceResult.failed(message=f"聊天会话不存在: {chat_id}")
                
            chat = await ChatDao.update(db, chat_id, {"title": title})
            await db.commit()
            
            return ServiceResult.success(data=chat, message="重命名聊天会话成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"重命名聊天会话失败: {str(e)}")
    
    @staticmethod
    async def delete_chat(
        db: AsyncSession, 
        chat_id: int,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        删除聊天会话
        
        Args:
            db: 数据库会话
            chat_id: 聊天会话ID
            current_user: 当前用户
            
        Returns:
            删除结果
        """
        try:
            chat = await ChatDao.get_by_id(db, chat_id)
            if not chat:
                return ServiceResult.failed(message=f"聊天会话不存在: {chat_id}")
                
            result = await ChatDao.delete(db, [chat_id])
            if not result:
                return ServiceResult.failed(message="删除聊天会话失败")
                
            await db.commit()
            
            return ServiceResult.success(message="删除聊天会话成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"删除聊天会话失败: {str(e)}")
    
    @staticmethod
    async def get_chat_messages(
        db: AsyncSession, 
        chat_id: int,
        page_num: int = 1, 
        page_size: int = 20,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        获取聊天消息列表
        
        Args:
            db: 数据库会话
            chat_id: 聊天会话ID
            page_num: 页码
            page_size: 每页条数
            current_user: 当前用户
            
        Returns:
            聊天消息列表
        """
        try:
            chat = await ChatDao.get_by_id(db, chat_id)
            if not chat:
                return ServiceResult.failed(message=f"聊天会话不存在: {chat_id}")
                
            result = await ChatMessageDao.get_chat_messages(
                db, chat_id, page_num, page_size
            )
            return result
        except Exception as e:
            return ServiceResult.failed(message=f"获取聊天消息列表失败: {str(e)}")
    
    @staticmethod
    async def add_message(
        db: AsyncSession, 
        chat_id: int,
        user_id: int,
        role: str,
        content: str,
        metadata: Dict = None,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        添加聊天消息
        
        Args:
            db: 数据库会话
            chat_id: 聊天会话ID
            user_id: 用户ID
            role: 消息角色
            content: 消息内容
            metadata: 元数据
            current_user: 当前用户
            
        Returns:
            添加结果
        """
        try:
            chat = await ChatDao.get_by_id(db, chat_id)
            if not chat:
                return ServiceResult.failed(message=f"聊天会话不存在: {chat_id}")
                
            message_data = {
                "chat_id": chat_id,
                "user_id": user_id,
                "role": role,
                "content": content,
                "status": MessageStatus.COMPLETED.value,
                "metadata": metadata or {}
            }
            
            message = await ChatMessageDao.add(db, message_data)
            await db.commit()
            
            return ServiceResult.success(data=message, message="添加聊天消息成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"添加聊天消息失败: {str(e)}")
    
    @staticmethod
    async def send_message(
        db: AsyncSession, 
        chat_id: int,
        user_id: int,
        content: str,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        发送消息并获取AI回复
        
        Args:
            db: 数据库会话
            chat_id: 聊天会话ID
            user_id: 用户ID
            content: 消息内容
            current_user: 当前用户
            
        Returns:
            处理结果
        """
        try:
            chat = await ChatDao.get_by_id(db, chat_id)
            if not chat:
                return ServiceResult.failed(message=f"聊天会话不存在: {chat_id}")
                
            app = await AIApplicationDao.get_by_id(db, chat.ai_application_id)
            if not app:
                return ServiceResult.failed(message=f"应用不存在: {chat.ai_application_id}")
                
            user_message = await ChatService.add_message(
                db, chat_id, user_id, MessageRole.USER.value, content, current_user=current_user
            )
            
            if isinstance(user_message, dict) and user_message.get("code") != 200:
                return user_message
                
            from module_ai.service.ai_service_manager import AIServiceManager
            ai_service_manager = AIServiceManager(db)
            
            ai_service = await ai_service_manager.get_service(app.id)
            if not ai_service:
                return ServiceResult.failed(message=f"获取AI服务失败: {app.id}")
                
            messages_result = await ChatMessageDao.get_chat_messages(db, chat_id, is_page=False)
            messages = messages_result.get("rows", [])
            
            result = await ai_service.send_message(
                chat_id=chat_id,
                user_message=content,
                history_messages=messages,
                system_prompt=chat.system_prompt,
                user_id=str(user_id)
            )
            
            if result.get("error"):
                error_message = await ChatService.add_message(
                    db, chat_id, user_id, MessageRole.ASSISTANT.value, 
                    "抱歉，处理您的请求时出现错误。", 
                    {"error": True, "message": result.get("message")},
                    current_user=current_user
                )
                
                return ServiceResult.failed(
                    message=f"AI回复失败: {result.get('message')}",
                    data={
                        "user_message": user_message.get("data"),
                        "assistant_message": error_message.get("data")
                    }
                )
                
            assistant_message = await ChatService.add_message(
                db, chat_id, user_id, MessageRole.ASSISTANT.value, 
                result.get("answer", ""), 
                result.get("metadata", {}),
                current_user=current_user
            )
            
            if result.get("conversation_id"):
                chat_config = chat.config or {}
                chat_config["conversation_id"] = result.get("conversation_id")
                await ChatDao.update(db, chat_id, {"config": chat_config})
                
            await db.commit()
            
            return ServiceResult.success(
                data={
                    "user_message": user_message.get("data"),
                    "assistant_message": assistant_message.get("data"),
                    "conversation_id": result.get("conversation_id"),
                    "message_id": result.get("message_id")
                },
                message="发送消息成功"
            )
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"发送消息失败: {str(e)}")

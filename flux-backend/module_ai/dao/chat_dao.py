from typing import List, Optional
from datetime import datetime
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.entity.do.chat_do import Chat, ChatMessage, MessageRole, MessageStatus
from utils.page_util import PageUtil, PageResponseModel


class ChatDao:
    """聊天会话DAO"""

    @classmethod
    async def get_by_id(cls, db: AsyncSession, chat_id: int) -> Optional[Chat]:
        """根据ID获取聊天会话"""
        chat = (await db.execute(
            select(Chat)
            .where(Chat.id == chat_id)
        )).scalars().first()
        return chat

    @classmethod
    async def get_user_chats(cls, db: AsyncSession, user_id: int, app_id: int = None,
                           page_num: int = 1, page_size: int = 10, is_page: bool = True) -> PageResponseModel:
        """获取用户的聊天会话列表"""
        conditions = [Chat.user_id == user_id]
        if app_id:
            conditions.append(Chat.ai_application_id == app_id)
            
        query = select(Chat).where(and_(*conditions)).order_by(desc(Chat.create_time))
        
        result = await PageUtil.paginate(
            db, query, page_num, page_size, is_page
        )
        return result

    @classmethod
    async def add(cls, db: AsyncSession, chat_data: dict) -> Chat:
        """添加聊天会话"""
        chat = Chat(**chat_data)
        db.add(chat)
        await db.flush()
        return chat

    @classmethod
    async def update(cls, db: AsyncSession, chat_id: int, chat_data: dict) -> Optional[Chat]:
        """更新聊天会话"""
        chat = await cls.get_by_id(db, chat_id)
        if not chat:
            return None
            
        for key, value in chat_data.items():
            if hasattr(chat, key):
                setattr(chat, key, value)
                
        await db.flush()
        return chat

    @classmethod
    async def delete(cls, db: AsyncSession, chat_ids: List[int]) -> bool:
        """删除聊天会话"""
        if not chat_ids:
            return False
            
        await db.execute(
            delete(Chat).where(Chat.id.in_(chat_ids))
        )
        return True


class ChatMessageDao:
    """聊天消息DAO"""

    @classmethod
    async def get_by_id(cls, db: AsyncSession, message_id: int) -> Optional[ChatMessage]:
        """根据ID获取聊天消息"""
        message = (await db.execute(
            select(ChatMessage)
            .where(ChatMessage.id == message_id)
        )).scalars().first()
        return message

    @classmethod
    async def get_chat_messages(cls, db: AsyncSession, chat_id: int,
                              page_num: int = 1, page_size: int = 20, is_page: bool = True) -> PageResponseModel:
        """获取聊天消息列表"""
        query = select(ChatMessage).where(
            ChatMessage.chat_id == chat_id
        ).order_by(ChatMessage.create_time.asc())
        
        result = await PageUtil.paginate(
            db, query, page_num, page_size, is_page
        )
        return result

    @classmethod
    async def add(cls, db: AsyncSession, message_data: dict) -> ChatMessage:
        """添加聊天消息"""
        message = ChatMessage(**message_data)
        db.add(message)
        await db.flush()
        return message

    @classmethod
    async def update(cls, db: AsyncSession, message_id: int, message_data: dict) -> Optional[ChatMessage]:
        """更新聊天消息"""
        message = await cls.get_by_id(db, message_id)
        if not message:
            return None
            
        for key, value in message_data.items():
            if hasattr(message, key):
                setattr(message, key, value)
                
        await db.flush()
        return message

    @classmethod
    async def delete(cls, db: AsyncSession, message_ids: List[int]) -> bool:
        """删除聊天消息"""
        if not message_ids:
            return False
            
        await db.execute(
            delete(ChatMessage).where(ChatMessage.id.in_(message_ids))
        )
        return True

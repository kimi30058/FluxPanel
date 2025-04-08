from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import String, Integer, Boolean, JSON, Text, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from config.database import Base, BaseMixin
from module_admin.entity.do.user_do import SysUser
from module_ai.entity.do.ai_do import AIApplication


class ChatType(str, PyEnum):
    """聊天类型枚举"""
    NORMAL = "normal"  # 普通聊天
    AI = "ai"         # AI对话


class MessageRole(str, PyEnum):
    """消息角色枚举"""
    SYSTEM = "system"     # 系统消息
    USER = "user"        # 用户消息
    ASSISTANT = "assistant"  # 助手消息


class MessageStatus(str, PyEnum):
    """消息状态枚举"""
    PENDING = "pending"    # 等待处理
    PROCESSING = "processing"  # 处理中
    COMPLETED = "completed"    # 已完成
    FAILED = "failed"      # 失败


class Chat(Base, BaseMixin):
    """聊天会话模型"""
    
    __tablename__ = "ai_chats"
    
    title: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        comment="会话标题"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        String(500), 
        nullable=True,
        comment="会话描述"
    )
    
    chat_type: Mapped[str] = mapped_column(
        Enum(ChatType),
        nullable=False,
        default=ChatType.AI,
        comment="会话类型"
    )
    
    system_prompt: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="系统提示词"
    )
    
    config: Mapped[Optional[Dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="会话配置"
    )
    
    ai_application_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("ai_applications.id", ondelete="SET NULL"),
        nullable=True,
        comment="关联的AI应用ID"
    )
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_user.user_id", ondelete="CASCADE"),
        nullable=False,
        comment="创建者用户ID"
    )
    
    user: Mapped["SysUser"] = relationship(
        "SysUser",
        back_populates="ai_chats"
    )
    
    messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="chat",
        cascade="all, delete-orphan"
    )
    
    ai_application: Mapped[Optional["AIApplication"]] = relationship(
        "AIApplication",
        back_populates="chats"
    )


class ChatMessage(Base, BaseMixin):
    """聊天消息模型"""
    
    __tablename__ = "ai_chat_messages"
    
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="消息内容"
    )
    
    role: Mapped[str] = mapped_column(
        Enum(MessageRole),
        nullable=False,
        comment="消息角色"
    )
    
    status: Mapped[str] = mapped_column(
        Enum(MessageStatus),
        nullable=False,
        default=MessageStatus.COMPLETED,
        comment="消息状态"
    )
    
    tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="消息token数"
    )
    
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="错误信息"
    )
    
    message_metadata: Mapped[Optional[Dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="消息元数据"
    )
    
    chat_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ai_chats.id", ondelete="CASCADE"),
        nullable=False,
        comment="所属会话ID"
    )
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_user.user_id", ondelete="CASCADE"),
        nullable=False,
        comment="发送者用户ID"
    )
    
    chat: Mapped["Chat"] = relationship(
        "Chat",
        back_populates="messages"
    )
    
    user: Mapped["SysUser"] = relationship(
        "SysUser",
        back_populates="ai_chat_messages"
    )

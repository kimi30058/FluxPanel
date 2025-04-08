from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import String, Integer, Boolean, JSON, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base, BaseMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module_ai.entity.do.chat_do import Chat


class TraditionalProvider(Base, BaseMixin):
    """传统AI供应商模型"""
    
    __tablename__ = "ai_traditional_providers"
    
    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False,
        comment="供应商名称"
    )
    
    provider: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        comment="供应商类型"
    )
    
    api_key: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        comment="API密钥"
    )
    
    base_url: Mapped[Optional[str]] = mapped_column(
        String(255), 
        nullable=True,
        comment="API基础URL"
    )
    
    available_models: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True,
        comment="可用的模型列表"
    )
    
    config: Mapped[Optional[Dict]] = mapped_column(
        JSON, 
        nullable=True,
        comment="供应商配置"
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False,
        default=True,
        comment="是否启用"
    )
    
    ai_applications: Mapped[List["AIApplication"]] = relationship(
        "AIApplication",
        back_populates="traditional_provider",
        cascade="all, delete-orphan"
    )


class DifyApplication(Base, BaseMixin):
    """Dify应用模型"""
    
    __tablename__ = "ai_dify_applications"
    
    api_key: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        comment="应用API密钥"
    )
    
    app_id: Mapped[str] = mapped_column(
        String(100), 
        nullable=False,
        comment="DIFY应用ID"
    )
    
    api_base: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        default="www.ai-agent.chat/v1",
        comment="DIFY API基础地址"
    )
    
    conversation_mode: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        default="chat",
        comment="对话模式"
    )
    
    response_mode: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        default="blocking",
        comment="响应模式"
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False,
        default=True,
        comment="是否启用"
    )
    
    ai_applications: Mapped[List["AIApplication"]] = relationship(
        "AIApplication",
        back_populates="dify_app",
        cascade="all, delete-orphan"
    )


class CozeApplication(Base, BaseMixin):
    """Coze应用模型"""
    
    __tablename__ = "ai_coze_applications"
    
    api_key: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        comment="应用API密钥"
    )
    
    workflow_id: Mapped[Optional[str]] = mapped_column(
        String(100), 
        nullable=True,
        comment="工作流ID"
    )
    
    agent_id: Mapped[Optional[str]] = mapped_column(
        String(100), 
        nullable=True,
        comment="Agent ID"
    )
    
    config: Mapped[Optional[Dict]] = mapped_column(
        JSON, 
        nullable=True,
        comment="应用配置"
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False,
        default=True,
        comment="是否启用"
    )
    
    ai_applications: Mapped[List["AIApplication"]] = relationship(
        "AIApplication",
        back_populates="coze_app",
        cascade="all, delete-orphan"
    )


class AIApplication(Base, BaseMixin):
    """AI应用模型"""
    
    __tablename__ = "ai_applications"
    
    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False,
        comment="应用名称"
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        String(500), 
        nullable=True,
        comment="应用描述"
    )
    
    icon: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        comment="应用图标"
    )
    
    icon_bg_color: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        comment="图标背景色"
    )
    
    type: Mapped[str] = mapped_column(
        String(50), 
        nullable=False,
        comment="应用类型"
    )
    
    system_prompt: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True,
        comment="系统提示词"
    )
    
    tags: Mapped[Optional[List[str]]] = mapped_column(
        JSON, 
        nullable=True,
        comment="应用标签"
    )
    
    max_context_turns: Mapped[int] = mapped_column(
        Integer, 
        nullable=False,
        default=10,
        comment="最大上下文轮次"
    )
    
    max_tokens: Mapped[int] = mapped_column(
        Integer, 
        nullable=False,
        default=4000,
        comment="最大token数"
    )
    
    preserve_system_prompt: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False,
        default=True,
        comment="是否始终保留系统提示词"
    )
    
    is_enabled: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False,
        default=True,
        comment="是否启用"
    )
    
    id_traditional_provider: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("ai_traditional_providers.id", ondelete="SET NULL"),
        nullable=True,
        comment="关联的传统AI供应商ID"
    )
    
    id_dify_app: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("ai_dify_applications.id", ondelete="SET NULL"),
        nullable=True,
        comment="关联的DIFY应用ID"
    )
    
    id_coze_app: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("ai_coze_applications.id", ondelete="SET NULL"),
        nullable=True,
        comment="关联的COZE应用ID"
    )
    
    traditional_provider: Mapped[Optional["TraditionalProvider"]] = relationship(
        "TraditionalProvider",
        back_populates="ai_applications"
    )
    
    dify_app: Mapped[Optional["DifyApplication"]] = relationship(
        "DifyApplication",
        back_populates="ai_applications"
    )
    
    coze_app: Mapped[Optional["CozeApplication"]] = relationship(
        "CozeApplication",
        back_populates="ai_applications"
    )
    
    chats: Mapped[List["Chat"]] = relationship(
        "Chat",
        back_populates="ai_application",
        cascade="all, delete-orphan"
    )

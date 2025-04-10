
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import BaseMixin, Base


class Topic(Base, BaseMixin):
    """
    对话主题表
    """
    __tablename__ = "ai_topic"

    name = Column(String(100), nullable=False, comment='主题名称')
    assistant_id = Column(Integer, ForeignKey('ai_assistant.id', ondelete='CASCADE'), nullable=False, comment='助手ID')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    pinned = Column(Boolean, default=False, comment='是否置顶')
    prompt = Column(Text, nullable=True, comment='自定义提示词')
    is_name_manually_edited = Column(Boolean, default=False, comment='名称是否手动编辑')
    
    assistant = relationship("Assistant", back_populates="topics")
    messages = relationship("Message", back_populates="topic")

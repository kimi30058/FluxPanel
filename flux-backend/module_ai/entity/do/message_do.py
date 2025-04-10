
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import BaseMixin, Base


class Message(Base, BaseMixin):
    """
    对话消息表
    """
    __tablename__ = "ai_message"

    role = Column(String(20), nullable=False, comment='角色(user/assistant)')
    content = Column(Text, nullable=False, comment='消息内容')
    reasoning_content = Column(Text, nullable=True, comment='推理内容')
    translated_content = Column(Text, nullable=True, comment='翻译内容')
    topic_id = Column(Integer, ForeignKey('ai_topic.id', ondelete='CASCADE'), nullable=False, comment='主题ID')
    status = Column(String(20), nullable=False, comment='状态(sending/pending/searching/success/paused/error)')
    model_id = Column(Integer, ForeignKey('ai_model.id'), nullable=True, comment='模型ID')
    assistant_id = Column(Integer, ForeignKey('ai_assistant.id'), nullable=False, comment='助手ID')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    images = Column(JSON, nullable=True, comment='图片列表')
    type = Column(String(20), nullable=False, default='text', comment='消息类型(text/@/clear)')
    is_preset = Column(Boolean, default=False, comment='是否预设消息')
    useful = Column(Boolean, nullable=True, comment='是否有用')
    error = Column(JSON, nullable=True, comment='错误信息')
    metadata = Column(JSON, nullable=True, comment='元数据')
    
    topic = relationship("Topic", back_populates="messages")
    model = relationship("Model")

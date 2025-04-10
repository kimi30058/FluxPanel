
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from config.database import BaseMixin, Base


assistant_knowledge = Table(
    'ai_assistant_knowledge',
    Base.metadata,
    Column('assistant_id', Integer, ForeignKey('ai_assistant.id', ondelete='CASCADE'), primary_key=True),
    Column('knowledge_id', Integer, ForeignKey('ai_knowledge_base.id', ondelete='CASCADE'), primary_key=True)
)


class Assistant(Base, BaseMixin):
    """
    AI助手表
    """
    __tablename__ = "ai_assistant"

    name = Column(String(100), nullable=False, comment='助手名称')
    prompt = Column(Text, nullable=False, comment='助手提示词')
    type = Column(String(50), nullable=False, comment='助手类型')
    emoji = Column(String(10), nullable=True, comment='表情图标')
    description = Column(String(255), nullable=True, comment='助手描述')
    model_id = Column(Integer, ForeignKey('ai_model.id'), nullable=True, comment='模型ID')
    default_model_id = Column(Integer, ForeignKey('ai_model.id'), nullable=True, comment='默认模型ID')
    enable_web_search = Column(Boolean, default=False, comment='是否启用网络搜索')
    enable_generate_image = Column(Boolean, default=False, comment='是否启用图像生成')
    
    model = relationship("Model", foreign_keys=[model_id])
    default_model = relationship("Model", foreign_keys=[default_model_id])
    knowledge_bases = relationship("KnowledgeBase", secondary=assistant_knowledge)
    topics = relationship("Topic", back_populates="assistant")


from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import BaseMixin, Base


class KnowledgeItem(Base, BaseMixin):
    """
    知识库项目表
    """
    __tablename__ = "ai_knowledge_item"

    knowledge_base_id = Column(Integer, ForeignKey('ai_knowledge_base.id', ondelete='CASCADE'), nullable=False, comment='知识库ID')
    unique_id = Column(String(100), nullable=True, comment='唯一ID')
    type = Column(String(20), nullable=False, comment='类型(file/url/note/sitemap/directory)')
    content = Column(Text, nullable=False, comment='内容')
    remark = Column(String(255), nullable=True, comment='备注')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    processing_status = Column(String(20), nullable=True, comment='处理状态(pending/processing/completed/failed)')
    processing_progress = Column(Integer, nullable=True, comment='处理进度')
    processing_error = Column(String(255), nullable=True, comment='处理错误')
    retry_count = Column(Integer, nullable=True, default=0, comment='重试次数')
    
    knowledge_base = relationship("KnowledgeBase", back_populates="items")

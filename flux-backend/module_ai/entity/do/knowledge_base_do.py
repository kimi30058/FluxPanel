
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import BaseMixin, Base


class KnowledgeBase(Base, BaseMixin):
    """
    知识库表
    """
    __tablename__ = "ai_knowledge_base"

    name = Column(String(100), nullable=False, comment='知识库名称')
    description = Column(String(255), nullable=True, comment='知识库描述')
    model_id = Column(Integer, ForeignKey('ai_model.id'), nullable=False, comment='嵌入模型ID')
    dimensions = Column(Integer, nullable=False, comment='嵌入维度')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    version = Column(Integer, nullable=False, default=1, comment='版本号')
    document_count = Column(Integer, nullable=True, comment='文档数量')
    chunk_size = Column(Integer, nullable=True, comment='分块大小')
    chunk_overlap = Column(Integer, nullable=True, comment='分块重叠')
    threshold = Column(Integer, nullable=True, comment='匹配阈值')
    rerank_model_id = Column(Integer, ForeignKey('ai_model.id'), nullable=True, comment='重排序模型ID')
    top_n = Column(Integer, nullable=True, comment='返回结果数量')
    
    model = relationship("Model", foreign_keys=[model_id])
    rerank_model = relationship("Model", foreign_keys=[rerank_model_id])
    items = relationship("KnowledgeItem", back_populates="knowledge_base")

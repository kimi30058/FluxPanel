
from sqlalchemy import Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from config.database import BaseMixin, Base


model_type = Table(
    'ai_model_type',
    Base.metadata,
    Column('model_id', Integer, ForeignKey('ai_model.id', ondelete='CASCADE'), primary_key=True),
    Column('type', String(50), primary_key=True)
)


class Model(Base, BaseMixin):
    """
    AI模型表
    """
    __tablename__ = "ai_model"

    name = Column(String(100), nullable=False, comment='模型名称')
    provider_id = Column(Integer, ForeignKey('ai_provider.id', ondelete='CASCADE'), nullable=False, comment='提供商ID')
    group = Column(String(50), nullable=False, comment='模型分组')
    description = Column(String(255), nullable=True, comment='模型描述')
    owned_by = Column(String(100), nullable=True, comment='模型所有者')
    
    provider = relationship("Provider", backref="models")
    types = relationship("String", secondary=model_type)


from sqlalchemy import Column, String
from config.database import BaseMixin, Base


class ModelType(Base, BaseMixin):
    """
    AI模型类型表
    """
    __tablename__ = "ai_model_type_enum"

    type = Column(String(50), nullable=False, unique=True, comment='模型类型')

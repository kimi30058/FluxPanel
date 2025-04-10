
from sqlalchemy import Column, String, Boolean, Integer
from config.database import BaseMixin, Base


class Provider(Base, BaseMixin):
    """
    AI提供商表
    """
    __tablename__ = "ai_provider"

    type = Column(String(50), nullable=False, comment='提供商类型')
    name = Column(String(100), nullable=False, comment='提供商名称')
    api_key = Column(String(255), nullable=False, comment='API密钥')
    api_host = Column(String(255), nullable=False, comment='API主机地址')
    api_version = Column(String(50), nullable=True, comment='API版本')
    enabled = Column(Boolean, default=True, comment='是否启用')
    is_system = Column(Boolean, default=False, comment='是否系统默认')
    is_authed = Column(Boolean, default=False, comment='是否已认证')
    rate_limit = Column(Integer, nullable=True, comment='速率限制')

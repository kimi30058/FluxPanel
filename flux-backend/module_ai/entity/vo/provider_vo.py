
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from module_admin.annotation.pydantic_annotation import as_query


class ProviderModel(BaseModel):
    """
    AI提供商表对应pydantic模型
    """
    id: Optional[int] = Field(default=None, description='提供商ID')
    type: str = Field(description='提供商类型')
    name: str = Field(description='提供商名称')
    api_key: str = Field(description='API密钥')
    api_host: str = Field(description='API主机地址')
    api_version: Optional[str] = Field(default=None, description='API版本')
    enabled: Optional[bool] = Field(default=True, description='是否启用')
    is_system: Optional[bool] = Field(default=False, description='是否系统默认')
    is_authed: Optional[bool] = Field(default=False, description='是否已认证')
    rate_limit: Optional[int] = Field(default=None, description='速率限制')
    create_by: Optional[int] = Field(default=None, description='创建者')
    dept_id: Optional[int] = Field(default=None, description='部门ID')

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class ProviderPageModel(BaseModel):
    """
    分页查询AI提供商表对应pydantic模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    type: Optional[str] = Field(default=None, description='提供商类型')
    name: Optional[str] = Field(default=None, description='提供商名称')
    enabled: Optional[bool] = Field(default=None, description='是否启用')

    @classmethod
    def as_query(cls):
        return as_query(cls)

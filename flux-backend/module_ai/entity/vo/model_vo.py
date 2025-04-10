
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from module_admin.annotation.pydantic_annotation import as_query


class ModelTypeModel(BaseModel):
    """
    模型类型关联表对应pydantic模型
    """
    model_id: int = Field(description='模型ID')
    type: str = Field(description='类型')


class ModelModel(BaseModel):
    """
    AI模型表对应pydantic模型
    """
    id: Optional[int] = Field(default=None, description='模型ID')
    name: str = Field(description='模型名称')
    provider_id: int = Field(description='提供商ID')
    group: str = Field(description='模型分组')
    description: Optional[str] = Field(default=None, description='模型描述')
    owned_by: Optional[str] = Field(default=None, description='模型所有者')
    types: Optional[List[str]] = Field(default=None, description='模型类型列表')
    create_by: Optional[int] = Field(default=None, description='创建者')
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class ModelPageModel(BaseModel):
    """
    分页查询AI模型表对应pydantic模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    name: Optional[str] = Field(default=None, description='模型名称')
    provider_id: Optional[int] = Field(default=None, description='提供商ID')
    group: Optional[str] = Field(default=None, description='模型分组')
    type: Optional[str] = Field(default=None, description='模型类型')

    @classmethod
    def as_query(cls):
        return as_query(cls)

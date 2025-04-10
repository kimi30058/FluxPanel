
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from module_admin.annotation.pydantic_annotation import as_query


class TopicModel(BaseModel):
    """
    对话主题表对应pydantic模型
    """
    id: Optional[int] = Field(default=None, description='主题ID')
    name: str = Field(description='主题名称')
    assistant_id: int = Field(description='助手ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')
    pinned: Optional[bool] = Field(default=False, description='是否置顶')
    prompt: Optional[str] = Field(default=None, description='自定义提示词')
    is_name_manually_edited: Optional[bool] = Field(default=False, description='名称是否手动编辑')
    create_by: Optional[int] = Field(default=None, description='创建者')
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class TopicPageModel(BaseModel):
    """
    分页查询对话主题表对应pydantic模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    name: Optional[str] = Field(default=None, description='主题名称')
    assistant_id: Optional[int] = Field(default=None, description='助手ID')
    pinned: Optional[bool] = Field(default=None, description='是否置顶')

    @classmethod
    def as_query(cls):
        return as_query(cls)

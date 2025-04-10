
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from module_admin.annotation.pydantic_annotation import as_query


class AssistantModel(BaseModel):
    """
    AI助手表对应pydantic模型
    """
    id: Optional[int] = Field(default=None, description='助手ID')
    name: str = Field(description='助手名称')
    prompt: str = Field(description='助手提示词')
    type: str = Field(description='助手类型')
    emoji: Optional[str] = Field(default=None, description='表情图标')
    description: Optional[str] = Field(default=None, description='助手描述')
    model_id: Optional[int] = Field(default=None, description='模型ID')
    default_model_id: Optional[int] = Field(default=None, description='默认模型ID')
    enable_web_search: Optional[bool] = Field(default=False, description='是否启用网络搜索')
    enable_generate_image: Optional[bool] = Field(default=False, description='是否启用图像生成')
    knowledge_base_ids: Optional[List[int]] = Field(default=None, description='知识库ID列表')
    create_by: Optional[int] = Field(default=None, description='创建者')
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class AssistantPageModel(BaseModel):
    """
    分页查询AI助手表对应pydantic模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    name: Optional[str] = Field(default=None, description='助手名称')
    type: Optional[str] = Field(default=None, description='助手类型')

    @classmethod
    def as_query(cls):
        return as_query(cls)

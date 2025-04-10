
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from module_admin.annotation.pydantic_annotation import as_query


class KnowledgeItemModel(BaseModel):
    """
    知识库项目表对应pydantic模型
    """
    id: Optional[int] = Field(default=None, description='项目ID')
    knowledge_base_id: int = Field(description='知识库ID')
    unique_id: Optional[str] = Field(default=None, description='唯一ID')
    type: str = Field(description='类型(file/url/note/sitemap/directory)')
    content: str = Field(description='内容')
    remark: Optional[str] = Field(default=None, description='备注')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')
    processing_status: Optional[str] = Field(default=None, description='处理状态(pending/processing/completed/failed)')
    processing_progress: Optional[int] = Field(default=None, description='处理进度')
    processing_error: Optional[str] = Field(default=None, description='处理错误')
    retry_count: Optional[int] = Field(default=0, description='重试次数')
    create_by: Optional[int] = Field(default=None, description='创建者')
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class KnowledgeItemPageModel(BaseModel):
    """
    分页查询知识库项目表对应pydantic模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    knowledge_base_id: Optional[int] = Field(default=None, description='知识库ID')
    type: Optional[str] = Field(default=None, description='类型')
    processing_status: Optional[str] = Field(default=None, description='处理状态')

    @classmethod
    def as_query(cls):
        return as_query(cls)

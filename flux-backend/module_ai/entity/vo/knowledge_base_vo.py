
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from module_admin.annotation.pydantic_annotation import as_query


class KnowledgeBaseModel(BaseModel):
    """
    知识库表对应pydantic模型
    """
    id: Optional[int] = Field(default=None, description='知识库ID')
    name: str = Field(description='知识库名称')
    description: Optional[str] = Field(default=None, description='知识库描述')
    model_id: int = Field(description='嵌入模型ID')
    dimensions: int = Field(description='嵌入维度')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    updated_at: Optional[datetime] = Field(default=None, description='更新时间')
    version: Optional[int] = Field(default=1, description='版本号')
    document_count: Optional[int] = Field(default=None, description='文档数量')
    chunk_size: Optional[int] = Field(default=None, description='分块大小')
    chunk_overlap: Optional[int] = Field(default=None, description='分块重叠')
    threshold: Optional[int] = Field(default=None, description='匹配阈值')
    rerank_model_id: Optional[int] = Field(default=None, description='重排序模型ID')
    top_n: Optional[int] = Field(default=None, description='返回结果数量')
    create_by: Optional[int] = Field(default=None, description='创建者')
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class KnowledgeBasePageModel(BaseModel):
    """
    分页查询知识库表对应pydantic模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    name: Optional[str] = Field(default=None, description='知识库名称')
    model_id: Optional[int] = Field(default=None, description='嵌入模型ID')

    @classmethod
    def as_query(cls):
        return as_query(cls)


from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from module_admin.annotation.pydantic_annotation import as_query


class MessageModel(BaseModel):
    """
    对话消息表对应pydantic模型
    """
    id: Optional[int] = Field(default=None, description='消息ID')
    role: str = Field(description='角色(user/assistant)')
    content: str = Field(description='消息内容')
    reasoning_content: Optional[str] = Field(default=None, description='推理内容')
    translated_content: Optional[str] = Field(default=None, description='翻译内容')
    topic_id: int = Field(description='主题ID')
    status: str = Field(description='状态(sending/pending/searching/success/paused/error)')
    model_id: Optional[int] = Field(default=None, description='模型ID')
    assistant_id: int = Field(description='助手ID')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    images: Optional[List[Dict[str, Any]]] = Field(default=None, description='图片列表')
    type: Optional[str] = Field(default='text', description='消息类型(text/@/clear)')
    is_preset: Optional[bool] = Field(default=False, description='是否预设消息')
    useful: Optional[bool] = Field(default=None, description='是否有用')
    error: Optional[Dict[str, Any]] = Field(default=None, description='错误信息')
    metadata: Optional[Dict[str, Any]] = Field(default=None, description='元数据')
    create_by: Optional[int] = Field(default=None, description='创建者')
    dept_id: Optional[int] = Field(default=None, description='部门ID')
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class MessagePageModel(BaseModel):
    """
    分页查询对话消息表对应pydantic模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    topic_id: Optional[int] = Field(default=None, description='主题ID')
    role: Optional[str] = Field(default=None, description='角色')
    status: Optional[str] = Field(default=None, description='状态')
    type: Optional[str] = Field(default=None, description='消息类型')

    @classmethod
    def as_query(cls):
        return as_query(cls)

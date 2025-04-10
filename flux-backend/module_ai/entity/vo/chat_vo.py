from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatModel(BaseModel):
    """聊天会话模型"""
    id: Optional[int] = None
    title: str
    userId: int
    providerId: Optional[int] = None
    appId: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

class ChatPageModel(BaseModel):
    """聊天会话分页查询模型"""
    pageNum: int = Field(1, description="页码")
    pageSize: int = Field(10, description="每页条数")
    userId: Optional[int] = None
    providerId: Optional[int] = None
    appId: Optional[str] = None
    
    @classmethod
    def as_query(cls, pageNum: int = 1, pageSize: int = 10):
        return cls(pageNum=pageNum, pageSize=pageSize)

class ChatRenameModel(BaseModel):
    """聊天会话重命名模型"""
    title: str

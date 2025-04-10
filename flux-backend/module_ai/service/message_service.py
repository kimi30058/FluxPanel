
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil
from utils.page_util import PageResponseModel
from module_ai.dao.message_dao import MessageDao
from module_ai.entity.vo.message_vo import MessageModel, MessagePageModel


class MessageService:
    """
    对话消息模块服务层
    """

    @classmethod
    async def get_message_list(cls, query_db: AsyncSession, query_object: MessagePageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        """
        获取对话消息列表
        """
        message_list = await MessageDao.get_message_list(query_db, query_object, data_scope_sql, is_page=True)
        return message_list

    @classmethod
    async def get_message_by_id(cls, query_db: AsyncSession, message_id: int) -> MessageModel:
        """
        根据ID获取对话消息
        """
        message = await MessageDao.get_by_id(query_db, message_id)
        message_model = MessageModel(**CamelCaseUtil.transform_result(message))
        return message_model

    @classmethod
    async def add_message(cls, query_db: AsyncSession, query_object: MessageModel) -> MessageModel:
        """
        添加对话消息
        """
        message = await MessageDao.add_message(query_db, query_object)
        message_model = MessageModel(**CamelCaseUtil.transform_result(message))
        return message_model

    @classmethod
    async def update_message(cls, query_db: AsyncSession, query_object: MessageModel) -> MessageModel:
        """
        更新对话消息
        """
        message = await MessageDao.edit_message(query_db, query_object)
        message_model = MessageModel(**CamelCaseUtil.transform_result(message))
        return message_model

    @classmethod
    async def del_message(cls, query_db: AsyncSession, message_ids: List[str]):
        """
        删除对话消息
        """
        await MessageDao.del_message(query_db, message_ids)

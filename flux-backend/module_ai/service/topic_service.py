
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil
from utils.page_util import PageResponseModel
from module_ai.dao.topic_dao import TopicDao
from module_ai.entity.vo.topic_vo import TopicModel, TopicPageModel


class TopicService:
    """
    对话主题模块服务层
    """

    @classmethod
    async def get_topic_list(cls, query_db: AsyncSession, query_object: TopicPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        """
        获取对话主题列表
        """
        topic_list = await TopicDao.get_topic_list(query_db, query_object, data_scope_sql, is_page=True)
        return topic_list

    @classmethod
    async def get_topic_by_id(cls, query_db: AsyncSession, topic_id: int) -> TopicModel:
        """
        根据ID获取对话主题
        """
        topic = await TopicDao.get_by_id(query_db, topic_id)
        topic_model = TopicModel(**CamelCaseUtil.transform_result(topic))
        return topic_model

    @classmethod
    async def add_topic(cls, query_db: AsyncSession, query_object: TopicModel) -> TopicModel:
        """
        添加对话主题
        """
        topic = await TopicDao.add_topic(query_db, query_object)
        topic_model = TopicModel(**CamelCaseUtil.transform_result(topic))
        return topic_model

    @classmethod
    async def update_topic(cls, query_db: AsyncSession, query_object: TopicModel) -> TopicModel:
        """
        更新对话主题
        """
        topic = await TopicDao.edit_topic(query_db, query_object)
        topic_model = TopicModel(**CamelCaseUtil.transform_result(topic))
        return topic_model

    @classmethod
    async def del_topic(cls, query_db: AsyncSession, topic_ids: List[str]):
        """
        删除对话主题
        """
        await TopicDao.del_topic(query_db, topic_ids)

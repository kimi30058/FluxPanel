
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil
from utils.page_util import PageResponseModel
from module_ai.dao.knowledge_item_dao import KnowledgeItemDao
from module_ai.entity.vo.knowledge_item_vo import KnowledgeItemModel, KnowledgeItemPageModel


class KnowledgeItemService:
    """
    知识库项目模块服务层
    """

    @classmethod
    async def get_knowledge_item_list(cls, query_db: AsyncSession, query_object: KnowledgeItemPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        """
        获取知识库项目列表
        """
        knowledge_item_list = await KnowledgeItemDao.get_knowledge_item_list(query_db, query_object, data_scope_sql, is_page=True)
        return knowledge_item_list

    @classmethod
    async def get_knowledge_item_by_id(cls, query_db: AsyncSession, knowledge_item_id: int) -> KnowledgeItemModel:
        """
        根据ID获取知识库项目
        """
        knowledge_item = await KnowledgeItemDao.get_by_id(query_db, knowledge_item_id)
        knowledge_item_model = KnowledgeItemModel(**CamelCaseUtil.transform_result(knowledge_item))
        return knowledge_item_model

    @classmethod
    async def add_knowledge_item(cls, query_db: AsyncSession, query_object: KnowledgeItemModel) -> KnowledgeItemModel:
        """
        添加知识库项目
        """
        knowledge_item = await KnowledgeItemDao.add_knowledge_item(query_db, query_object)
        knowledge_item_model = KnowledgeItemModel(**CamelCaseUtil.transform_result(knowledge_item))
        return knowledge_item_model

    @classmethod
    async def update_knowledge_item(cls, query_db: AsyncSession, query_object: KnowledgeItemModel) -> KnowledgeItemModel:
        """
        更新知识库项目
        """
        knowledge_item = await KnowledgeItemDao.edit_knowledge_item(query_db, query_object)
        knowledge_item_model = KnowledgeItemModel(**CamelCaseUtil.transform_result(knowledge_item))
        return knowledge_item_model

    @classmethod
    async def del_knowledge_item(cls, query_db: AsyncSession, knowledge_item_ids: List[str]):
        """
        删除知识库项目
        """
        await KnowledgeItemDao.del_knowledge_item(query_db, knowledge_item_ids)

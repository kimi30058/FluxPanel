
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil
from utils.page_util import PageResponseModel
from module_ai.dao.knowledge_base_dao import KnowledgeBaseDao
from module_ai.entity.vo.knowledge_base_vo import KnowledgeBaseModel, KnowledgeBasePageModel


class KnowledgeBaseService:
    """
    知识库模块服务层
    """

    @classmethod
    async def get_knowledge_base_list(cls, query_db: AsyncSession, query_object: KnowledgeBasePageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        """
        获取知识库列表
        """
        knowledge_base_list = await KnowledgeBaseDao.get_knowledge_base_list(query_db, query_object, data_scope_sql, is_page=True)
        return knowledge_base_list

    @classmethod
    async def get_knowledge_base_by_id(cls, query_db: AsyncSession, knowledge_base_id: int) -> KnowledgeBaseModel:
        """
        根据ID获取知识库
        """
        knowledge_base = await KnowledgeBaseDao.get_by_id(query_db, knowledge_base_id)
        knowledge_base_model = KnowledgeBaseModel(**CamelCaseUtil.transform_result(knowledge_base))
        return knowledge_base_model

    @classmethod
    async def add_knowledge_base(cls, query_db: AsyncSession, query_object: KnowledgeBaseModel) -> KnowledgeBaseModel:
        """
        添加知识库
        """
        knowledge_base = await KnowledgeBaseDao.add_knowledge_base(query_db, query_object)
        knowledge_base_model = KnowledgeBaseModel(**CamelCaseUtil.transform_result(knowledge_base))
        return knowledge_base_model

    @classmethod
    async def update_knowledge_base(cls, query_db: AsyncSession, query_object: KnowledgeBaseModel) -> KnowledgeBaseModel:
        """
        更新知识库
        """
        knowledge_base = await KnowledgeBaseDao.edit_knowledge_base(query_db, query_object)
        knowledge_base_model = KnowledgeBaseModel(**CamelCaseUtil.transform_result(knowledge_base))
        return knowledge_base_model

    @classmethod
    async def del_knowledge_base(cls, query_db: AsyncSession, knowledge_base_ids: List[str]):
        """
        删除知识库
        """
        await KnowledgeBaseDao.del_knowledge_base(query_db, knowledge_base_ids)

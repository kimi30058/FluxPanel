
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil
from utils.page_util import PageResponseModel
from module_ai.dao.assistant_dao import AssistantDao
from module_ai.entity.vo.assistant_vo import AssistantModel, AssistantPageModel


class AssistantService:
    """
    AI助手模块服务层
    """

    @classmethod
    async def get_assistant_list(cls, query_db: AsyncSession, query_object: AssistantPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        """
        获取AI助手列表
        """
        assistant_list = await AssistantDao.get_assistant_list(query_db, query_object, data_scope_sql, is_page=True)
        return assistant_list

    @classmethod
    async def get_assistant_by_id(cls, query_db: AsyncSession, assistant_id: int) -> AssistantModel:
        """
        根据ID获取AI助手
        """
        assistant = await AssistantDao.get_by_id(query_db, assistant_id)
        assistant_model = AssistantModel(**CamelCaseUtil.transform_result(assistant))
        return assistant_model

    @classmethod
    async def add_assistant(cls, query_db: AsyncSession, query_object: AssistantModel) -> AssistantModel:
        """
        添加AI助手
        """
        assistant = await AssistantDao.add_assistant(query_db, query_object)
        assistant_model = AssistantModel(**CamelCaseUtil.transform_result(assistant))
        return assistant_model

    @classmethod
    async def update_assistant(cls, query_db: AsyncSession, query_object: AssistantModel) -> AssistantModel:
        """
        更新AI助手
        """
        assistant = await AssistantDao.edit_assistant(query_db, query_object)
        assistant_model = AssistantModel(**CamelCaseUtil.transform_result(assistant))
        return assistant_model

    @classmethod
    async def del_assistant(cls, query_db: AsyncSession, assistant_ids: List[str]):
        """
        删除AI助手
        """
        await AssistantDao.del_assistant(query_db, assistant_ids)

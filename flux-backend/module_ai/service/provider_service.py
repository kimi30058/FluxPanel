
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil
from utils.page_util import PageResponseModel
from module_ai.dao.provider_dao import ProviderDao
from module_ai.entity.vo.provider_vo import ProviderModel, ProviderPageModel


class ProviderService:
    """
    AI提供商模块服务层
    """

    @classmethod
    async def get_provider_list(cls, query_db: AsyncSession, query_object: ProviderPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        """
        获取AI提供商列表
        """
        provider_list = await ProviderDao.get_provider_list(query_db, query_object, data_scope_sql, is_page=True)
        return provider_list

    @classmethod
    async def get_provider_by_id(cls, query_db: AsyncSession, provider_id: int) -> ProviderModel:
        """
        根据ID获取AI提供商
        """
        provider = await ProviderDao.get_by_id(query_db, provider_id)
        provider_model = ProviderModel(**CamelCaseUtil.transform_result(provider))
        return provider_model

    @classmethod
    async def add_provider(cls, query_db: AsyncSession, query_object: ProviderModel) -> ProviderModel:
        """
        添加AI提供商
        """
        provider = await ProviderDao.add_provider(query_db, query_object)
        provider_model = ProviderModel(**CamelCaseUtil.transform_result(provider))
        return provider_model

    @classmethod
    async def update_provider(cls, query_db: AsyncSession, query_object: ProviderModel) -> ProviderModel:
        """
        更新AI提供商
        """
        provider = await ProviderDao.edit_provider(query_db, query_object)
        provider_model = ProviderModel(**CamelCaseUtil.transform_result(provider))
        return provider_model

    @classmethod
    async def del_provider(cls, query_db: AsyncSession, provider_ids: List[str]):
        """
        删除AI提供商
        """
        await ProviderDao.del_provider(query_db, provider_ids)


from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil
from utils.page_util import PageResponseModel
from module_ai.dao.model_dao import ModelDao
from module_ai.entity.vo.model_vo import ModelModel, ModelPageModel


class ModelService:
    """
    AI模型模块服务层
    """

    @classmethod
    async def get_model_list(cls, query_db: AsyncSession, query_object: ModelPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        """
        获取AI模型列表
        """
        model_list = await ModelDao.get_model_list(query_db, query_object, data_scope_sql, is_page=True)
        return model_list

    @classmethod
    async def get_model_by_id(cls, query_db: AsyncSession, model_id: int) -> ModelModel:
        """
        根据ID获取AI模型
        """
        model = await ModelDao.get_by_id(query_db, model_id)
        model_model = ModelModel(**CamelCaseUtil.transform_result(model))
        return model_model

    @classmethod
    async def add_model(cls, query_db: AsyncSession, query_object: ModelModel) -> ModelModel:
        """
        添加AI模型
        """
        model = await ModelDao.add_model(query_db, query_object)
        model_model = ModelModel(**CamelCaseUtil.transform_result(model))
        return model_model

    @classmethod
    async def update_model(cls, query_db: AsyncSession, query_object: ModelModel) -> ModelModel:
        """
        更新AI模型
        """
        model = await ModelDao.edit_model(query_db, query_object)
        model_model = ModelModel(**CamelCaseUtil.transform_result(model))
        return model_model

    @classmethod
    async def del_model(cls, query_db: AsyncSession, model_ids: List[str]):
        """
        删除AI模型
        """
        await ModelDao.del_model(query_db, model_ids)

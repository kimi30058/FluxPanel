
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.entity.do.provider_do import Provider
from module_ai.entity.vo.provider_vo import ProviderModel, ProviderPageModel
from utils.page_util import PageUtil


class ProviderDao:
    """
    AI提供商模块数据库操作层
    """

    @classmethod
    async def get_provider_list(cls, db: AsyncSession, query_object: ProviderPageModel, data_scope_sql: str, is_page: bool = False):
        """
        获取AI提供商列表
        """
        query = (
            select(Provider)
            .where(
                Provider.del_flag == '0',
                Provider.type == query_object.type if query_object.type else True,
                Provider.name.like(f'%{query_object.name}%') if query_object.name else True,
                Provider.enabled == query_object.enabled if query_object.enabled is not None else True,
                eval(data_scope_sql)
            )
        )
        provider_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return provider_list

    @classmethod
    async def get_by_id(cls, db: AsyncSession, provider_id: int):
        """
        根据ID获取AI提供商
        """
        provider = (
            await db.execute(
                select(Provider)
                .where(Provider.del_flag == '0', Provider.id == provider_id)
            )
        ).scalar_one_or_none()
        return provider

    @classmethod
    async def add_provider(cls, db: AsyncSession, provider_model: ProviderModel) -> Provider:
        """
        添加AI提供商
        """
        db_provider = Provider(**provider_model.model_dump(exclude={'id'}))
        db.add(db_provider)
        await db.flush()
        return db_provider

    @classmethod
    async def edit_provider(cls, db: AsyncSession, provider_model: ProviderModel) -> Provider:
        """
        编辑AI提供商
        """
        provider = await cls.get_by_id(db, provider_model.id)
        for key, value in provider_model.model_dump(exclude={'id'}).items():
            setattr(provider, key, value)
        await db.flush()
        return provider

    @classmethod
    async def del_provider(cls, db: AsyncSession, provider_ids: list[str]):
        """
        删除AI提供商
        """
        await db.execute(
            update(Provider)
            .where(Provider.id.in_(provider_ids))
            .values(del_flag='2')
        )


from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.entity.do.knowledge_base_do import KnowledgeBase
from module_ai.entity.vo.knowledge_base_vo import KnowledgeBaseModel, KnowledgeBasePageModel
from utils.page_util import PageUtil


class KnowledgeBaseDao:
    """
    知识库模块数据库操作层
    """

    @classmethod
    async def get_knowledge_base_list(cls, db: AsyncSession, query_object: KnowledgeBasePageModel, data_scope_sql: str, is_page: bool = False):
        """
        获取知识库列表
        """
        query = (
            select(KnowledgeBase)
            .where(
                KnowledgeBase.del_flag == '0',
                KnowledgeBase.name.like(f'%{query_object.name}%') if query_object.name else True,
                KnowledgeBase.model_id == query_object.model_id if query_object.model_id else True,
                eval(data_scope_sql)
            )
        )
        knowledge_base_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return knowledge_base_list

    @classmethod
    async def get_by_id(cls, db: AsyncSession, knowledge_base_id: int):
        """
        根据ID获取知识库
        """
        knowledge_base = (
            await db.execute(
                select(KnowledgeBase)
                .where(KnowledgeBase.del_flag == '0', KnowledgeBase.id == knowledge_base_id)
            )
        ).scalar_one_or_none()
        return knowledge_base

    @classmethod
    async def add_knowledge_base(cls, db: AsyncSession, knowledge_base_model: KnowledgeBaseModel) -> KnowledgeBase:
        """
        添加知识库
        """
        db_knowledge_base = KnowledgeBase(**knowledge_base_model.model_dump(exclude={'id'}))
        db.add(db_knowledge_base)
        await db.flush()
        return db_knowledge_base

    @classmethod
    async def edit_knowledge_base(cls, db: AsyncSession, knowledge_base_model: KnowledgeBaseModel) -> KnowledgeBase:
        """
        编辑知识库
        """
        knowledge_base = await cls.get_by_id(db, knowledge_base_model.id)
        for key, value in knowledge_base_model.model_dump(exclude={'id'}).items():
            setattr(knowledge_base, key, value)
        await db.flush()
        return knowledge_base

    @classmethod
    async def del_knowledge_base(cls, db: AsyncSession, knowledge_base_ids: list[str]):
        """
        删除知识库
        """
        await db.execute(
            update(KnowledgeBase)
            .where(KnowledgeBase.id.in_(knowledge_base_ids))
            .values(del_flag='2')
        )

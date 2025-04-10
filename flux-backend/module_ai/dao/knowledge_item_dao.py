
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.entity.do.knowledge_item_do import KnowledgeItem
from module_ai.entity.vo.knowledge_item_vo import KnowledgeItemModel, KnowledgeItemPageModel
from utils.page_util import PageUtil


class KnowledgeItemDao:
    """
    知识库项目模块数据库操作层
    """

    @classmethod
    async def get_knowledge_item_list(cls, db: AsyncSession, query_object: KnowledgeItemPageModel, data_scope_sql: str, is_page: bool = False):
        """
        获取知识库项目列表
        """
        query = (
            select(KnowledgeItem)
            .where(
                KnowledgeItem.del_flag == '0',
                KnowledgeItem.knowledge_base_id == query_object.knowledge_base_id if query_object.knowledge_base_id else True,
                KnowledgeItem.type == query_object.type if query_object.type else True,
                KnowledgeItem.processing_status == query_object.processing_status if query_object.processing_status else True,
                eval(data_scope_sql)
            )
        )
        knowledge_item_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return knowledge_item_list

    @classmethod
    async def get_by_id(cls, db: AsyncSession, knowledge_item_id: int):
        """
        根据ID获取知识库项目
        """
        knowledge_item = (
            await db.execute(
                select(KnowledgeItem)
                .where(KnowledgeItem.del_flag == '0', KnowledgeItem.id == knowledge_item_id)
            )
        ).scalar_one_or_none()
        return knowledge_item

    @classmethod
    async def add_knowledge_item(cls, db: AsyncSession, knowledge_item_model: KnowledgeItemModel) -> KnowledgeItem:
        """
        添加知识库项目
        """
        db_knowledge_item = KnowledgeItem(**knowledge_item_model.model_dump(exclude={'id'}))
        db.add(db_knowledge_item)
        await db.flush()
        return db_knowledge_item

    @classmethod
    async def edit_knowledge_item(cls, db: AsyncSession, knowledge_item_model: KnowledgeItemModel) -> KnowledgeItem:
        """
        编辑知识库项目
        """
        knowledge_item = await cls.get_by_id(db, knowledge_item_model.id)
        for key, value in knowledge_item_model.model_dump(exclude={'id'}).items():
            setattr(knowledge_item, key, value)
        await db.flush()
        return knowledge_item

    @classmethod
    async def del_knowledge_item(cls, db: AsyncSession, knowledge_item_ids: list[str]):
        """
        删除知识库项目
        """
        await db.execute(
            update(KnowledgeItem)
            .where(KnowledgeItem.id.in_(knowledge_item_ids))
            .values(del_flag='2')
        )

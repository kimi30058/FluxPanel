
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.entity.do.topic_do import Topic
from module_ai.entity.vo.topic_vo import TopicModel, TopicPageModel
from utils.page_util import PageUtil


class TopicDao:
    """
    对话主题模块数据库操作层
    """

    @classmethod
    async def get_topic_list(cls, db: AsyncSession, query_object: TopicPageModel, data_scope_sql: str, is_page: bool = False):
        """
        获取对话主题列表
        """
        query = (
            select(Topic)
            .where(
                Topic.del_flag == '0',
                Topic.name.like(f'%{query_object.name}%') if query_object.name else True,
                Topic.assistant_id == query_object.assistant_id if query_object.assistant_id else True,
                Topic.pinned == query_object.pinned if query_object.pinned is not None else True,
                eval(data_scope_sql)
            )
        )
        topic_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return topic_list

    @classmethod
    async def get_by_id(cls, db: AsyncSession, topic_id: int):
        """
        根据ID获取对话主题
        """
        topic = (
            await db.execute(
                select(Topic)
                .where(Topic.del_flag == '0', Topic.id == topic_id)
            )
        ).scalar_one_or_none()
        return topic

    @classmethod
    async def add_topic(cls, db: AsyncSession, topic_model: TopicModel) -> Topic:
        """
        添加对话主题
        """
        db_topic = Topic(**topic_model.model_dump(exclude={'id'}))
        db.add(db_topic)
        await db.flush()
        return db_topic

    @classmethod
    async def edit_topic(cls, db: AsyncSession, topic_model: TopicModel) -> Topic:
        """
        编辑对话主题
        """
        topic = await cls.get_by_id(db, topic_model.id)
        for key, value in topic_model.model_dump(exclude={'id'}).items():
            setattr(topic, key, value)
        await db.flush()
        return topic

    @classmethod
    async def del_topic(cls, db: AsyncSession, topic_ids: list[str]):
        """
        删除对话主题
        """
        await db.execute(
            update(Topic)
            .where(Topic.id.in_(topic_ids))
            .values(del_flag='2')
        )

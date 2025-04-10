
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.entity.do.message_do import Message
from module_ai.entity.vo.message_vo import MessageModel, MessagePageModel
from utils.page_util import PageUtil


class MessageDao:
    """
    对话消息模块数据库操作层
    """

    @classmethod
    async def get_message_list(cls, db: AsyncSession, query_object: MessagePageModel, data_scope_sql: str, is_page: bool = False):
        """
        获取对话消息列表
        """
        query = (
            select(Message)
            .where(
                Message.del_flag == '0',
                Message.topic_id == query_object.topic_id if query_object.topic_id else True,
                Message.role == query_object.role if query_object.role else True,
                Message.status == query_object.status if query_object.status else True,
                Message.type == query_object.type if query_object.type else True,
                eval(data_scope_sql)
            )
            .order_by(Message.created_at)
        )
        message_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return message_list

    @classmethod
    async def get_by_id(cls, db: AsyncSession, message_id: int):
        """
        根据ID获取对话消息
        """
        message = (
            await db.execute(
                select(Message)
                .where(Message.del_flag == '0', Message.id == message_id)
            )
        ).scalar_one_or_none()
        return message

    @classmethod
    async def add_message(cls, db: AsyncSession, message_model: MessageModel) -> Message:
        """
        添加对话消息
        """
        db_message = Message(**message_model.model_dump(exclude={'id'}))
        db.add(db_message)
        await db.flush()
        return db_message

    @classmethod
    async def edit_message(cls, db: AsyncSession, message_model: MessageModel) -> Message:
        """
        编辑对话消息
        """
        message = await cls.get_by_id(db, message_model.id)
        for key, value in message_model.model_dump(exclude={'id'}).items():
            setattr(message, key, value)
        await db.flush()
        return message

    @classmethod
    async def del_message(cls, db: AsyncSession, message_ids: list[str]):
        """
        删除对话消息
        """
        await db.execute(
            update(Message)
            .where(Message.id.in_(message_ids))
            .values(del_flag='2')
        )

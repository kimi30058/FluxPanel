
from sqlalchemy import delete, select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.entity.do.assistant_do import Assistant, assistant_knowledge
from module_ai.entity.vo.assistant_vo import AssistantModel, AssistantPageModel
from utils.page_util import PageUtil


class AssistantDao:
    """
    AI助手模块数据库操作层
    """

    @classmethod
    async def get_assistant_list(cls, db: AsyncSession, query_object: AssistantPageModel, data_scope_sql: str, is_page: bool = False):
        """
        获取AI助手列表
        """
        query = (
            select(Assistant)
            .where(
                Assistant.del_flag == '0',
                Assistant.name.like(f'%{query_object.name}%') if query_object.name else True,
                Assistant.type == query_object.type if query_object.type else True,
                eval(data_scope_sql)
            )
        )
        assistant_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return assistant_list

    @classmethod
    async def get_by_id(cls, db: AsyncSession, assistant_id: int):
        """
        根据ID获取AI助手
        """
        assistant = (
            await db.execute(
                select(Assistant)
                .where(Assistant.del_flag == '0', Assistant.id == assistant_id)
            )
        ).scalar_one_or_none()
        return assistant

    @classmethod
    async def add_assistant(cls, db: AsyncSession, assistant_model: AssistantModel) -> Assistant:
        """
        添加AI助手
        """
        assistant_data = assistant_model.model_dump(exclude={'id', 'knowledge_base_ids'})
        db_assistant = Assistant(**assistant_data)
        db.add(db_assistant)
        await db.flush()
        
        if assistant_model.knowledge_base_ids:
            for kb_id in assistant_model.knowledge_base_ids:
                await db.execute(
                    assistant_knowledge.insert().values(
                        assistant_id=db_assistant.id,
                        knowledge_id=kb_id
                    )
                )
        
        return db_assistant

    @classmethod
    async def edit_assistant(cls, db: AsyncSession, assistant_model: AssistantModel) -> Assistant:
        """
        编辑AI助手
        """
        assistant = await cls.get_by_id(db, assistant_model.id)
        for key, value in assistant_model.model_dump(exclude={'id', 'knowledge_base_ids'}).items():
            setattr(assistant, key, value)
        
        if assistant_model.knowledge_base_ids is not None:
            await db.execute(
                delete(assistant_knowledge)
                .where(assistant_knowledge.c.assistant_id == assistant_model.id)
            )
            
            for kb_id in assistant_model.knowledge_base_ids:
                await db.execute(
                    assistant_knowledge.insert().values(
                        assistant_id=assistant_model.id,
                        knowledge_id=kb_id
                    )
                )
        
        await db.flush()
        return assistant

    @classmethod
    async def del_assistant(cls, db: AsyncSession, assistant_ids: list[str]):
        """
        删除AI助手
        """
        await db.execute(
            update(Assistant)
            .where(Assistant.id.in_(assistant_ids))
            .values(del_flag='2')
        )

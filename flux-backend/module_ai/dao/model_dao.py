
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.entity.do.model_do import Model, model_type
from module_ai.entity.vo.model_vo import ModelModel, ModelPageModel
from utils.page_util import PageUtil


class ModelDao:
    """
    AI模型模块数据库操作层
    """

    @classmethod
    async def get_model_list(cls, db: AsyncSession, query_object: ModelPageModel, data_scope_sql: str, is_page: bool = False):
        """
        获取AI模型列表
        """
        query = (
            select(Model)
            .where(
                Model.del_flag == '0',
                Model.name.like(f'%{query_object.name}%') if query_object.name else True,
                Model.provider_id == query_object.provider_id if query_object.provider_id else True,
                Model.group == query_object.group if query_object.group else True,
                eval(data_scope_sql)
            )
        )
        model_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return model_list

    @classmethod
    async def get_by_id(cls, db: AsyncSession, model_id: int):
        """
        根据ID获取AI模型
        """
        model = (
            await db.execute(
                select(Model)
                .where(Model.del_flag == '0', Model.id == model_id)
            )
        ).scalar_one_or_none()
        return model

    @classmethod
    async def add_model(cls, db: AsyncSession, model_model: ModelModel) -> Model:
        """
        添加AI模型
        """
        model_data = model_model.model_dump(exclude={'id', 'types'})
        db_model = Model(**model_data)
        db.add(db_model)
        await db.flush()
        
        if model_model.types:
            for type_name in model_model.types:
                from module_ai.entity.do.model_type_do import ModelType
                type_obj = (await db.execute(
                    select(ModelType).where(ModelType.type == type_name)
                )).scalar_one_or_none()
                
                if not type_obj:
                    type_obj = ModelType(type=type_name)
                    db.add(type_obj)
                    await db.flush()
                
                await db.execute(
                    model_type.insert().values(
                        model_id=db_model.id,
                        type_id=type_obj.id
                    )
                )
        
        return db_model

    @classmethod
    async def edit_model(cls, db: AsyncSession, model_model: ModelModel) -> Model:
        """
        编辑AI模型
        """
        model = await cls.get_by_id(db, model_model.id)
        for key, value in model_model.model_dump(exclude={'id', 'types'}).items():
            setattr(model, key, value)
        
        if model_model.types is not None:
            await db.execute(
                delete(model_type)
                .where(model_type.c.model_id == model_model.id)
            )
            
            for type_name in model_model.types:
                from module_ai.entity.do.model_type_do import ModelType
                type_obj = (await db.execute(
                    select(ModelType).where(ModelType.type == type_name)
                )).scalar_one_or_none()
                
                if not type_obj:
                    type_obj = ModelType(type=type_name)
                    db.add(type_obj)
                    await db.flush()
                
                await db.execute(
                    model_type.insert().values(
                        model_id=model_model.id,
                        type_id=type_obj.id
                    )
                )
        
        await db.flush()
        return model

    @classmethod
    async def del_model(cls, db: AsyncSession, model_ids: list[str]):
        """
        删除AI模型
        """
        await db.execute(
            update(Model)
            .where(Model.id.in_(model_ids))
            .values(del_flag='2')
        )

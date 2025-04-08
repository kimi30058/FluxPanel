from typing import List, Optional
from datetime import datetime
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.entity.do.ai_do import TraditionalProvider, DifyApplication, CozeApplication, AIApplication
from utils.page_util import PageUtil, PageResponseModel


class TraditionalProviderDao:
    """传统AI供应商DAO"""

    @classmethod
    async def get_by_id(cls, db: AsyncSession, provider_id: int) -> Optional[TraditionalProvider]:
        """根据ID获取供应商信息"""
        provider = (await db.execute(
            select(TraditionalProvider)
            .where(TraditionalProvider.id == provider_id)
        )).scalars().first()
        return provider

    @classmethod
    async def get_list(cls, db: AsyncSession, is_active: bool = None, provider_type: str = None, 
                      page_num: int = 1, page_size: int = 10, is_page: bool = True) -> PageResponseModel:
        """获取供应商列表"""
        conditions = []
        if is_active is not None:
            conditions.append(TraditionalProvider.is_active == is_active)
        if provider_type:
            conditions.append(TraditionalProvider.provider == provider_type)
            
        query = select(TraditionalProvider)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.order_by(desc(TraditionalProvider.create_time))
        
        result = await PageUtil.paginate(
            db, query, page_num, page_size, is_page
        )
        return result

    @classmethod
    async def add(cls, db: AsyncSession, provider_data: dict) -> TraditionalProvider:
        """添加供应商"""
        provider = TraditionalProvider(**provider_data)
        db.add(provider)
        await db.flush()
        return provider

    @classmethod
    async def update(cls, db: AsyncSession, provider_id: int, provider_data: dict) -> Optional[TraditionalProvider]:
        """更新供应商"""
        provider = await cls.get_by_id(db, provider_id)
        if not provider:
            return None
            
        for key, value in provider_data.items():
            if hasattr(provider, key):
                setattr(provider, key, value)
                
        await db.flush()
        return provider

    @classmethod
    async def delete(cls, db: AsyncSession, provider_ids: List[int]) -> bool:
        """删除供应商"""
        if not provider_ids:
            return False
            
        await db.execute(
            delete(TraditionalProvider).where(TraditionalProvider.id.in_(provider_ids))
        )
        return True


class DifyApplicationDao:
    """Dify应用DAO"""

    @classmethod
    async def get_by_id(cls, db: AsyncSession, app_id: int) -> Optional[DifyApplication]:
        """根据ID获取Dify应用"""
        app = (await db.execute(
            select(DifyApplication)
            .where(DifyApplication.id == app_id)
        )).scalars().first()
        return app

    @classmethod
    async def get_list(cls, db: AsyncSession, is_active: bool = None,
                      page_num: int = 1, page_size: int = 10, is_page: bool = True) -> PageResponseModel:
        """获取Dify应用列表"""
        conditions = []
        if is_active is not None:
            conditions.append(DifyApplication.is_active == is_active)
            
        query = select(DifyApplication)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.order_by(desc(DifyApplication.create_time))
        
        result = await PageUtil.paginate(
            db, query, page_num, page_size, is_page
        )
        return result

    @classmethod
    async def add(cls, db: AsyncSession, app_data: dict) -> DifyApplication:
        """添加Dify应用"""
        app = DifyApplication(**app_data)
        db.add(app)
        await db.flush()
        return app

    @classmethod
    async def update(cls, db: AsyncSession, app_id: int, app_data: dict) -> Optional[DifyApplication]:
        """更新Dify应用"""
        app = await cls.get_by_id(db, app_id)
        if not app:
            return None
            
        for key, value in app_data.items():
            if hasattr(app, key):
                setattr(app, key, value)
                
        await db.flush()
        return app

    @classmethod
    async def delete(cls, db: AsyncSession, app_ids: List[int]) -> bool:
        """删除Dify应用"""
        if not app_ids:
            return False
            
        await db.execute(
            delete(DifyApplication).where(DifyApplication.id.in_(app_ids))
        )
        return True


class CozeApplicationDao:
    """Coze应用DAO"""

    @classmethod
    async def get_by_id(cls, db: AsyncSession, app_id: int) -> Optional[CozeApplication]:
        """根据ID获取Coze应用"""
        app = (await db.execute(
            select(CozeApplication)
            .where(CozeApplication.id == app_id)
        )).scalars().first()
        return app

    @classmethod
    async def get_list(cls, db: AsyncSession, is_active: bool = None,
                      page_num: int = 1, page_size: int = 10, is_page: bool = True) -> PageResponseModel:
        """获取Coze应用列表"""
        conditions = []
        if is_active is not None:
            conditions.append(CozeApplication.is_active == is_active)
            
        query = select(CozeApplication)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.order_by(desc(CozeApplication.create_time))
        
        result = await PageUtil.paginate(
            db, query, page_num, page_size, is_page
        )
        return result

    @classmethod
    async def add(cls, db: AsyncSession, app_data: dict) -> CozeApplication:
        """添加Coze应用"""
        app = CozeApplication(**app_data)
        db.add(app)
        await db.flush()
        return app

    @classmethod
    async def update(cls, db: AsyncSession, app_id: int, app_data: dict) -> Optional[CozeApplication]:
        """更新Coze应用"""
        app = await cls.get_by_id(db, app_id)
        if not app:
            return None
            
        for key, value in app_data.items():
            if hasattr(app, key):
                setattr(app, key, value)
                
        await db.flush()
        return app

    @classmethod
    async def delete(cls, db: AsyncSession, app_ids: List[int]) -> bool:
        """删除Coze应用"""
        if not app_ids:
            return False
            
        await db.execute(
            delete(CozeApplication).where(CozeApplication.id.in_(app_ids))
        )
        return True


class AIApplicationDao:
    """AI应用DAO"""

    @classmethod
    async def get_by_id(cls, db: AsyncSession, app_id: int) -> Optional[AIApplication]:
        """根据ID获取AI应用"""
        app = (await db.execute(
            select(AIApplication)
            .where(AIApplication.id == app_id)
        )).scalars().first()
        return app

    @classmethod
    async def get_list(cls, db: AsyncSession, type: str = None, is_enabled: bool = None,
                     page_num: int = 1, page_size: int = 10, is_page: bool = True) -> PageResponseModel:
        """获取AI应用列表"""
        conditions = []
        if type:
            conditions.append(AIApplication.type == type)
        if is_enabled is not None:
            conditions.append(AIApplication.is_enabled == is_enabled)
            
        query = select(AIApplication)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.order_by(desc(AIApplication.create_time))
        
        result = await PageUtil.paginate(
            db, query, page_num, page_size, is_page
        )
        return result

    @classmethod
    async def add(cls, db: AsyncSession, app_data: dict) -> AIApplication:
        """添加AI应用"""
        app = AIApplication(**app_data)
        db.add(app)
        await db.flush()
        return app

    @classmethod
    async def update(cls, db: AsyncSession, app_id: int, app_data: dict) -> Optional[AIApplication]:
        """更新AI应用"""
        app = await cls.get_by_id(db, app_id)
        if not app:
            return None
            
        for key, value in app_data.items():
            if hasattr(app, key):
                setattr(app, key, value)
                
        await db.flush()
        return app

    @classmethod
    async def delete(cls, db: AsyncSession, app_ids: List[int]) -> bool:
        """删除AI应用"""
        if not app_ids:
            return False
            
        await db.execute(
            delete(AIApplication).where(AIApplication.id.in_(app_ids))
        )
        return True

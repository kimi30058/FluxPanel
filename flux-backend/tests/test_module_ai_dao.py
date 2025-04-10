import pytest
import sys
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module_ai.entity.do.provider_do import Provider
from module_ai.entity.do.model_do import Model
from module_ai.entity.do.model_type_do import ModelType
from module_ai.dao.provider_dao import ProviderDao
from module_ai.dao.model_dao import ModelDao
from module_ai.entity.vo.provider_vo import ProviderModel, ProviderPageModel
from module_ai.entity.vo.model_vo import ModelModel, ModelPageModel
from config.database import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_ai_dao.db"

engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)


@pytest.fixture(scope="function")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        test_provider = Provider(
            type="openai",
            name="Test OpenAI",
            api_key="test_api_key",
            api_host="https://api.openai.com",
            api_version="v1",
            enabled=True,
            del_flag="0"
        )
        session.add(test_provider)
        await session.commit()
        await session.refresh(test_provider)
        
        test_model = Model(
            name="gpt-3.5-turbo",
            provider_id=test_provider.id,
            group="GPT",
            description="Test model",
            del_flag="0"
        )
        session.add(test_model)
        await session.commit()
    
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_provider_dao(setup_database):
    """Test ProviderDao methods"""
    async with TestingSessionLocal() as session:
        query_object = ProviderPageModel(page_num=1, page_size=10)
        data_scope_sql = "True"
        provider_list = await ProviderDao.get_provider_list(session, query_object, data_scope_sql, is_page=True)
        
        assert provider_list.total > 0
        assert len(provider_list.rows) > 0
        assert provider_list.rows[0].name == "Test OpenAI"
        
        provider_id = provider_list.rows[0].id
        provider = await ProviderDao.get_by_id(session, provider_id)
        
        assert provider is not None
        assert provider.name == "Test OpenAI"
        
        new_provider = ProviderModel(
            type="anthropic",
            name="Test Anthropic",
            api_key="test_api_key_2",
            api_host="https://api.anthropic.com",
            api_version="v1",
            enabled=True
        )
        added_provider = await ProviderDao.add_provider(session, new_provider)
        await session.commit()
        
        assert added_provider is not None
        assert added_provider.name == "Test Anthropic"
        
        edit_provider = ProviderModel(
            id=provider_id,
            type="openai",
            name="Updated OpenAI",
            api_key="updated_api_key",
            api_host="https://api.openai.com",
            api_version="v1",
            enabled=True
        )
        updated_provider = await ProviderDao.edit_provider(session, edit_provider)
        await session.commit()
        
        assert updated_provider is not None
        assert updated_provider.name == "Updated OpenAI"
        
        await ProviderDao.del_provider(session, [str(provider_id)])
        await session.commit()
        
        deleted_provider = await ProviderDao.get_by_id(session, provider_id)
        assert deleted_provider is None or deleted_provider.del_flag == "2"


@pytest.mark.asyncio
async def test_model_dao(setup_database):
    """Test ModelDao methods"""
    async with TestingSessionLocal() as session:
        query_object = ModelPageModel(page_num=1, page_size=10)
        data_scope_sql = "True"
        model_list = await ModelDao.get_model_list(session, query_object, data_scope_sql, is_page=True)
        
        assert model_list.total > 0
        assert len(model_list.rows) > 0
        assert model_list.rows[0].name == "gpt-3.5-turbo"
        
        model_id = model_list.rows[0].id
        model = await ModelDao.get_by_id(session, model_id)
        
        assert model is not None
        assert model.name == "gpt-3.5-turbo"
        
        provider_query = ProviderPageModel(page_num=1, page_size=10)
        provider_list = await ProviderDao.get_provider_list(session, provider_query, data_scope_sql, is_page=True)
        provider_id = provider_list.rows[0].id
        
        new_model = ModelModel(
            name="claude-3-opus",
            provider_id=provider_id,
            group="Claude",
            description="Test Claude model",
            types=["text", "vision"]
        )
        added_model = await ModelDao.add_model(session, new_model)
        await session.commit()
        
        assert added_model is not None
        assert added_model.name == "claude-3-opus"
        
        edit_model = ModelModel(
            id=model_id,
            name="gpt-4",
            provider_id=provider_id,
            group="GPT",
            description="Updated GPT model",
            types=["text", "function"]
        )
        updated_model = await ModelDao.edit_model(session, edit_model)
        await session.commit()
        
        assert updated_model is not None
        assert updated_model.name == "gpt-4"
        
        await ModelDao.del_model(session, [str(model_id)])
        await session.commit()
        
        deleted_model = await ModelDao.get_by_id(session, model_id)
        assert deleted_model is None or deleted_model.del_flag == "2"


if __name__ == "__main__":
    pytest.main(["-v", "test_module_ai_dao.py"])

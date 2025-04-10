import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app
from config.database import Base
from module_ai.entity.do.provider_do import Provider
from module_ai.entity.do.model_do import Model
from module_ai.entity.do.assistant_do import Assistant
from module_ai.entity.do.topic_do import Topic
from module_ai.entity.do.message_do import Message
from module_ai.entity.do.knowledge_base_do import KnowledgeBase
from module_ai.entity.do.knowledge_item_do import KnowledgeItem

client = TestClient(app)

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

async def override_get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()


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
            enabled=True
        )
        session.add(test_provider)
        await session.commit()
        await session.refresh(test_provider)
        
        test_model = Model(
            name="gpt-3.5-turbo",
            provider_id=test_provider.id,
            group="GPT",
            description="Test model"
        )
        session.add(test_model)
        await session.commit()
        
        test_assistant = Assistant(
            name="Test Assistant",
            prompt="You are a helpful assistant",
            type="general",
            emoji="🤖",
            description="Test assistant",
            model_id=test_model.id
        )
        session.add(test_assistant)
        await session.commit()
    
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_provider_endpoints(setup_database):
    response = client.get("/ai/provider/list")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert len(data["rows"]) > 0
    
    provider_id = data["rows"][0]["id"]
    response = client.get(f"/ai/provider/{provider_id}")
    assert response.status_code == 200
    assert response.json()["code"] == 200
    
    new_provider = {
        "type": "anthropic",
        "name": "Test Anthropic",
        "apiKey": "test_api_key_2",
        "apiHost": "https://api.anthropic.com",
        "apiVersion": "v1",
        "enabled": True
    }
    response = client.post("/ai/provider", json=new_provider)
    assert response.status_code == 200
    assert response.json()["code"] == 200
    
    update_provider = {
        "id": provider_id,
        "type": "openai",
        "name": "Updated OpenAI",
        "apiKey": "updated_api_key",
        "apiHost": "https://api.openai.com",
        "apiVersion": "v1",
        "enabled": True
    }
    response = client.put("/ai/provider", json=update_provider)
    assert response.status_code == 200
    assert response.json()["code"] == 200
    
    response = client.delete(f"/ai/provider/{provider_id}")
    assert response.status_code == 200
    assert response.json()["code"] == 200


@pytest.mark.asyncio
async def test_model_endpoints(setup_database):
    response = client.get("/ai/model/list")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert len(data["rows"]) > 0
    
    model_id = data["rows"][0]["id"]
    response = client.get(f"/ai/model/{model_id}")
    assert response.status_code == 200
    assert response.json()["code"] == 200


@pytest.mark.asyncio
async def test_assistant_endpoints(setup_database):
    response = client.get("/ai/assistant/list")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert len(data["rows"]) > 0
    
    assistant_id = data["rows"][0]["id"]
    response = client.get(f"/ai/assistant/{assistant_id}")
    assert response.status_code == 200
    assert response.json()["code"] == 200


if __name__ == "__main__":
    pytest.main(["-v", "test_module_ai.py"])

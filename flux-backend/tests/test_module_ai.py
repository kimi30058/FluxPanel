import pytest
import sys
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi import Depends, APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import Base
from module_ai.entity.do.provider_do import Provider
from module_ai.entity.do.model_do import Model, model_type
from module_ai.entity.do.model_type_do import ModelType
from module_ai.entity.do.assistant_do import Assistant
from module_ai.entity.do.topic_do import Topic
from module_ai.entity.do.message_do import Message
from module_ai.entity.do.knowledge_base_do import KnowledgeBase
from module_ai.entity.do.knowledge_item_do import KnowledgeItem
from module_ai.controller.provider_controller import router as provider_router
from module_ai.controller.model_controller import router as model_router
from module_ai.controller.assistant_controller import router as assistant_router

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(provider_router)
app.include_router(model_router)
app.include_router(assistant_router)

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    db = TestingSessionLocal()
    
    db.query(Provider).delete()
    db.query(Model).delete()
    db.query(ModelType).delete()
    db.query(Assistant).delete()
    
    test_provider = Provider(
        type="openai",
        name="Test OpenAI",
        api_key="test_api_key",
        api_host="https://api.openai.com",
        api_version="v1",
        enabled=True,
        del_flag="0",
        create_by=1,
        dept_id=1
    )
    db.add(test_provider)
    db.commit()
    db.refresh(test_provider)
    
    test_model_type = ModelType(
        type="text",
        del_flag="0",
        create_by=1,
        dept_id=1
    )
    db.add(test_model_type)
    db.commit()
    db.refresh(test_model_type)
    
    test_model = Model(
        name="gpt-3.5-turbo",
        provider_id=test_provider.id,
        group="GPT",
        description="Test model",
        del_flag="0",
        create_by=1,
        dept_id=1
    )
    db.add(test_model)
    db.commit()
    db.refresh(test_model)
    
    db.execute(
        model_type.insert().values(
            model_id=test_model.id,
            type_id=test_model_type.id
        )
    )
    db.commit()
    
    test_assistant = Assistant(
        name="Test Assistant",
        prompt="You are a helpful assistant",
        type="general",
        emoji="🤖",
        description="Test assistant",
        model_id=test_model.id,
        del_flag="0",
        create_by=1,
        dept_id=1
    )
    db.add(test_assistant)
    db.commit()
    
    yield
    
    db.close()


def test_model_structure():
    """Test the structure of the model classes"""
    assert hasattr(Provider, 'id')
    assert hasattr(Provider, 'type')
    assert hasattr(Provider, 'name')
    assert hasattr(Provider, 'api_key')
    assert hasattr(Provider, 'api_host')
    assert hasattr(Provider, 'enabled')
    
    assert hasattr(Model, 'id')
    assert hasattr(Model, 'name')
    assert hasattr(Model, 'provider_id')
    assert hasattr(Model, 'group')
    assert hasattr(Model, 'provider')
    assert hasattr(Model, 'types')
    
    assert hasattr(Assistant, 'id')
    assert hasattr(Assistant, 'name')
    assert hasattr(Assistant, 'prompt')
    assert hasattr(Assistant, 'type')
    assert hasattr(Assistant, 'model_id')
    
    assert hasattr(Topic, 'id')
    assert hasattr(Topic, 'name')
    assert hasattr(Topic, 'assistant_id')
    
    assert hasattr(Message, 'id')
    assert hasattr(Message, 'role')
    assert hasattr(Message, 'content')
    assert hasattr(Message, 'topic_id')
    
    assert hasattr(KnowledgeBase, 'id')
    assert hasattr(KnowledgeBase, 'name')
    assert hasattr(KnowledgeBase, 'model_id')
    
    assert hasattr(KnowledgeItem, 'id')
    assert hasattr(KnowledgeItem, 'knowledge_base_id')
    assert hasattr(KnowledgeItem, 'type')
    assert hasattr(KnowledgeItem, 'content')


if __name__ == "__main__":
    pytest.main(["-v", "test_module_ai.py"])

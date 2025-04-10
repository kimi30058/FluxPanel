import pytest
import sys
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module_ai.entity.do.provider_do import Provider
from module_ai.entity.do.model_do import Model
from module_ai.entity.do.model_type_do import ModelType
from module_ai.entity.do.assistant_do import Assistant
from module_ai.entity.do.topic_do import Topic
from module_ai.entity.do.message_do import Message
from module_ai.entity.do.knowledge_base_do import KnowledgeBase
from module_ai.entity.do.knowledge_item_do import KnowledgeItem
from config.database import Base

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(engine)
    
    session = Session()
    
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
    session.add(test_provider)
    session.commit()
    
    test_model_type = ModelType(
        type="text",
        del_flag="0",
        create_by=1,
        dept_id=1
    )
    session.add(test_model_type)
    session.commit()
    
    test_model = Model(
        name="gpt-3.5-turbo",
        provider_id=test_provider.id,
        group="GPT",
        description="Test model",
        del_flag="0",
        create_by=1,
        dept_id=1
    )
    session.add(test_model)
    session.commit()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


def test_provider_model(setup_database):
    """Test Provider model structure and data"""
    session = setup_database
    
    inspector = inspect(Provider)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'type' in columns
    assert 'name' in columns
    assert 'api_key' in columns
    assert 'api_host' in columns
    assert 'enabled' in columns
    
    provider = session.query(Provider).first()
    assert provider is not None
    assert provider.name == "Test OpenAI"
    assert provider.type == "openai"
    assert provider.api_key == "test_api_key"
    assert provider.enabled is True


def test_model_model(setup_database):
    """Test Model model structure and data"""
    session = setup_database
    
    inspector = inspect(Model)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'name' in columns
    assert 'provider_id' in columns
    assert 'group' in columns
    
    model = session.query(Model).first()
    assert model is not None
    assert model.name == "gpt-3.5-turbo"
    assert model.group == "GPT"
    
    provider = session.query(Provider).first()
    assert model.provider_id == provider.id


def test_model_type_model(setup_database):
    """Test ModelType model structure and data"""
    session = setup_database
    
    inspector = inspect(ModelType)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'type' in columns
    
    model_type = session.query(ModelType).first()
    assert model_type is not None
    assert model_type.type == "text"


if __name__ == "__main__":
    pytest.main(["-v", "test_module_ai_dao.py"])

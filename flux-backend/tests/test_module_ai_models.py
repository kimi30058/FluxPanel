import pytest
import sys
import os
from sqlalchemy import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module_ai.entity.do.provider_do import Provider
from module_ai.entity.do.model_do import Model
from module_ai.entity.do.assistant_do import Assistant
from module_ai.entity.do.topic_do import Topic
from module_ai.entity.do.message_do import Message
from module_ai.entity.do.knowledge_base_do import KnowledgeBase
from module_ai.entity.do.knowledge_item_do import KnowledgeItem


def test_provider_model():
    """Test Provider model structure"""
    inspector = inspect(Provider)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'type' in columns
    assert 'name' in columns
    assert 'api_key' in columns
    assert 'api_host' in columns
    assert 'enabled' in columns
    
    assert str(columns['type'].type) == 'VARCHAR(50)'
    assert str(columns['name'].type) == 'VARCHAR(100)'
    assert str(columns['api_key'].type) == 'VARCHAR(255)'
    assert str(columns['api_host'].type) == 'VARCHAR(255)'
    assert str(columns['enabled'].type) == 'BOOLEAN'
    
    assert Provider.__tablename__ == 'ai_provider'


def test_model_model():
    """Test Model model structure"""
    inspector = inspect(Model)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'name' in columns
    assert 'provider_id' in columns
    assert 'group' in columns
    
    assert str(columns['name'].type) == 'VARCHAR(100)'
    assert str(columns['group'].type) == 'VARCHAR(50)'
    
    assert Model.__tablename__ == 'ai_model'


def test_assistant_model():
    """Test Assistant model structure"""
    inspector = inspect(Assistant)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'name' in columns
    assert 'prompt' in columns
    assert 'type' in columns
    assert 'model_id' in columns
    
    assert str(columns['name'].type) == 'VARCHAR(100)'
    assert str(columns['type'].type) == 'VARCHAR(50)'
    
    assert Assistant.__tablename__ == 'ai_assistant'


def test_topic_model():
    """Test Topic model structure"""
    inspector = inspect(Topic)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'name' in columns
    assert 'assistant_id' in columns
    assert 'created_at' in columns
    assert 'updated_at' in columns
    
    assert str(columns['name'].type) == 'VARCHAR(100)'
    
    assert Topic.__tablename__ == 'ai_topic'


def test_message_model():
    """Test Message model structure"""
    inspector = inspect(Message)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'role' in columns
    assert 'content' in columns
    assert 'topic_id' in columns
    assert 'status' in columns
    assert 'assistant_id' in columns
    
    assert str(columns['role'].type) == 'VARCHAR(20)'
    assert str(columns['status'].type) == 'VARCHAR(20)'
    
    assert Message.__tablename__ == 'ai_message'


def test_knowledge_base_model():
    """Test KnowledgeBase model structure"""
    inspector = inspect(KnowledgeBase)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'name' in columns
    assert 'model_id' in columns
    assert 'dimensions' in columns
    assert 'created_at' in columns
    assert 'updated_at' in columns
    
    assert str(columns['name'].type) == 'VARCHAR(100)'
    
    assert KnowledgeBase.__tablename__ == 'ai_knowledge_base'


def test_knowledge_item_model():
    """Test KnowledgeItem model structure"""
    inspector = inspect(KnowledgeItem)
    columns = inspector.columns
    
    assert 'id' in columns
    assert 'knowledge_base_id' in columns
    assert 'type' in columns
    assert 'content' in columns
    assert 'created_at' in columns
    assert 'updated_at' in columns
    
    assert str(columns['type'].type) == 'VARCHAR(20)'
    
    assert KnowledgeItem.__tablename__ == 'ai_knowledge_item'


if __name__ == "__main__":
    pytest.main(["-v", "test_module_ai_models.py"])

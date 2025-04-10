import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module_ai.entity.do.provider_do import Provider
from module_ai.entity.do.model_do import Model, model_type
from module_ai.entity.do.model_type_do import ModelType
from module_ai.entity.do.assistant_do import Assistant
from module_ai.entity.do.topic_do import Topic
from module_ai.entity.do.message_do import Message
from module_ai.entity.do.knowledge_base_do import KnowledgeBase
from module_ai.entity.do.knowledge_item_do import KnowledgeItem


def test_provider_model_structure():
    """Test Provider model structure"""
    assert hasattr(Provider, 'id')
    assert hasattr(Provider, 'type')
    assert hasattr(Provider, 'name')
    assert hasattr(Provider, 'api_key')
    assert hasattr(Provider, 'api_host')
    assert hasattr(Provider, 'enabled')
    assert Provider.__tablename__ == 'ai_provider'


def test_model_model_structure():
    """Test Model model structure"""
    assert hasattr(Model, 'id')
    assert hasattr(Model, 'name')
    assert hasattr(Model, 'provider_id')
    assert hasattr(Model, 'group')
    assert hasattr(Model, 'provider')
    assert hasattr(Model, 'types')
    assert Model.__tablename__ == 'ai_model'


def test_model_type_structure():
    """Test ModelType model structure"""
    assert hasattr(ModelType, 'id')
    assert hasattr(ModelType, 'type')
    assert ModelType.__tablename__ == 'ai_model_type_enum'


def test_assistant_model_structure():
    """Test Assistant model structure"""
    assert hasattr(Assistant, 'id')
    assert hasattr(Assistant, 'name')
    assert hasattr(Assistant, 'prompt')
    assert hasattr(Assistant, 'type')
    assert hasattr(Assistant, 'model_id')
    assert Assistant.__tablename__ == 'ai_assistant'


def test_topic_model_structure():
    """Test Topic model structure"""
    assert hasattr(Topic, 'id')
    assert hasattr(Topic, 'name')
    assert hasattr(Topic, 'assistant_id')
    assert Topic.__tablename__ == 'ai_topic'


def test_message_model_structure():
    """Test Message model structure"""
    assert hasattr(Message, 'id')
    assert hasattr(Message, 'role')
    assert hasattr(Message, 'content')
    assert hasattr(Message, 'topic_id')
    assert Message.__tablename__ == 'ai_message'


def test_knowledge_base_model_structure():
    """Test KnowledgeBase model structure"""
    assert hasattr(KnowledgeBase, 'id')
    assert hasattr(KnowledgeBase, 'name')
    assert hasattr(KnowledgeBase, 'model_id')
    assert KnowledgeBase.__tablename__ == 'ai_knowledge_base'


def test_knowledge_item_model_structure():
    """Test KnowledgeItem model structure"""
    assert hasattr(KnowledgeItem, 'id')
    assert hasattr(KnowledgeItem, 'knowledge_base_id')
    assert hasattr(KnowledgeItem, 'type')
    assert hasattr(KnowledgeItem, 'content')
    assert KnowledgeItem.__tablename__ == 'ai_knowledge_item'


if __name__ == "__main__":
    pytest.main(["-v", "test_module_ai.py"])

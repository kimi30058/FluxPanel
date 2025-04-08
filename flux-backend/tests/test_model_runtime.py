import pytest
from fastapi.testclient import TestClient
from module_ai.core.model_runtime.model_providers.model_provider_factory import ModelProviderFactory
from module_ai.core.model_runtime.entities.model_entities import ModelType

def test_model_provider_factory():
    """测试模型提供商工厂"""
    factory = ModelProviderFactory()
    providers = factory.get_providers()
    assert providers is not None
    assert len(providers) > 0
    
    openai_provider = factory.get_provider("openai")
    assert openai_provider is not None
    
    llm_models = openai_provider.get_models(ModelType.LLM)
    assert llm_models is not None

"""
App config module for FluxPanel.

This module provides a simplified version of the DifyConfig class from dify001.
"""

class DifyConfig:
    """
    Simplified DifyConfig class for FluxPanel.
    """
    
    DEBUG = False
    
    MODEL_RUNTIME_ENABLED = True
    
    DEFAULT_TENANT_ID = "default"
    
    DEFAULT_MODEL_PROVIDER = "openai"
    DEFAULT_MODEL_PROVIDER_CREDENTIALS = {}
    
    DEFAULT_LLM_MODEL = "gpt-3.5-turbo"
    DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"
    DEFAULT_RERANK_MODEL = "rerank-english-v2.0"
    DEFAULT_SPEECH_TO_TEXT_MODEL = "whisper-1"
    DEFAULT_TEXT_TO_SPEECH_MODEL = "tts-1"
    DEFAULT_MODERATION_MODEL = "text-moderation-latest"

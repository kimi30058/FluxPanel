"""
Plugin daemon entity module for FluxPanel.
"""

from typing import Optional
from pydantic import BaseModel
from module_ai.core.model_runtime.entities.provider_entities import ProviderEntity

class PluginModelProviderEntity(BaseModel):
    """
    Plugin model provider entity.
    """
    plugin_id: str
    provider: str
    declaration: ProviderEntity

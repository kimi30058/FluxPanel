"""
Plugin daemon entity module for FluxPanel.
"""

from typing import Optional
from pydantic import BaseModel
from module_ai.core.model_runtime.entities.provider_entities import ProviderEntity

class PluginDaemonInnerError(Exception):
    """
    Plugin daemon inner error.
    
    This exception is raised when there is an internal error in the plugin daemon.
    """
    def __init__(self, message: str = "Plugin daemon inner error"):
        self.message = message
        super().__init__(self.message)

class PluginModelProviderEntity(BaseModel):
    """
    Plugin model provider entity.
    """
    plugin_id: str
    provider: str
    declaration: ProviderEntity

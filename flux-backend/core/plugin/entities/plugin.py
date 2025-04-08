"""
Plugin entity module for FluxPanel.
"""

from enum import Enum
from typing import Optional

class ModelProviderID:
    """
    Model provider ID class.
    """
    def __init__(self, provider: str):
        """
        Initialize model provider ID.
        
        Args:
            provider: provider name
        """
        if "/" in provider:
            self.plugin_id, self.provider_name = provider.split("/", 1)
        else:
            self.plugin_id = "builtin"
            self.provider_name = provider
            
    def __str__(self) -> str:
        """
        Convert to string.
        
        Returns:
            provider name
        """
        return f"{self.plugin_id}/{self.provider_name}"

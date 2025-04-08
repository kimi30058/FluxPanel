"""
Plugin model manager module for FluxPanel.
"""

from typing import List, Optional
from module_ai.core.model_runtime.entities.model_entities import AIModelEntity
from core.plugin.entities.plugin_daemon import PluginModelProviderEntity

class PluginModelManager:
    """
    Plugin model manager.
    """
    
    def fetch_model_providers(self, tenant_id: str) -> List[PluginModelProviderEntity]:
        """
        Fetch model providers.
        
        Args:
            tenant_id: tenant ID
            
        Returns:
            list of plugin model providers
        """
        return []
        
    def validate_provider_credentials(
        self, 
        tenant_id: str, 
        user_id: str, 
        plugin_id: str, 
        provider: str, 
        credentials: dict
    ) -> None:
        """
        Validate provider credentials.
        
        Args:
            tenant_id: tenant ID
            user_id: user ID
            plugin_id: plugin ID
            provider: provider name
            credentials: credentials to validate
        """
        pass
        
    def validate_model_credentials(
        self, 
        tenant_id: str, 
        user_id: str, 
        plugin_id: str, 
        provider: str, 
        model_type: str,
        model: str,
        credentials: dict
    ) -> None:
        """
        Validate model credentials.
        
        Args:
            tenant_id: tenant ID
            user_id: user ID
            plugin_id: plugin ID
            provider: provider name
            model_type: model type
            model: model name
            credentials: credentials to validate
        """
        pass
        
    def get_model_schema(
        self, 
        tenant_id: str, 
        user_id: str, 
        plugin_id: str, 
        provider: str, 
        model_type: str,
        model: str,
        credentials: dict
    ) -> Optional[AIModelEntity]:
        """
        Get model schema.
        
        Args:
            tenant_id: tenant ID
            user_id: user ID
            plugin_id: plugin ID
            provider: provider name
            model_type: model type
            model: model name
            credentials: credentials
            
        Returns:
            model schema
        """
        return None

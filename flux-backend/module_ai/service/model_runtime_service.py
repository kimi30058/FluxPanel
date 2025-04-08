from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional, Tuple, Union

from module_admin.entity.vo.user_vo import CurrentUserModel
from module_ai.core.model_runtime.model_providers.model_provider_factory import ModelProviderFactory
from module_ai.core.model_runtime.entities.model_entities import ModelType
from utils.service_result_util import ServiceResult

class ModelRuntimeService:
    """
    模型运行时服务
    """
    
    @staticmethod
    async def get_model_providers_services(
        db: AsyncSession, current_user: CurrentUserModel
    ) -> Dict[str, Any]:
        """
        获取所有模型提供商信息
        
        Args:
            db: 数据库会话
            current_user: 当前用户
            
        Returns:
            所有模型提供商信息
        """
        try:
            provider_factory = ModelProviderFactory()
            providers = provider_factory.get_providers()
            
            return providers
        except Exception as e:
            return ServiceResult.failed(message=f"获取模型提供商信息失败: {str(e)}")
    
    @staticmethod
    async def get_models_by_provider_and_type_services(
        db: AsyncSession, provider_name: str, model_type: str, current_user: CurrentUserModel
    ) -> Dict[str, Any]:
        """
        获取特定提供商和模型类型的模型列表
        
        Args:
            db: 数据库会话
            provider_name: 提供商名称
            model_type: 模型类型
            current_user: 当前用户
            
        Returns:
            模型列表
        """
        try:
            model_type_enum = ModelType(model_type)
            
            provider_factory = ModelProviderFactory()
            provider = provider_factory.get_provider(provider_name)
            
            if not provider:
                return ServiceResult.failed(message=f"提供商 {provider_name} 不存在")
            
            models = provider.get_models(model_type_enum)
            return models
        except Exception as e:
            return ServiceResult.failed(message=f"获取模型列表失败: {str(e)}")
    
    @staticmethod
    async def validate_provider_credentials_services(
        db: AsyncSession, credentials: Dict, current_user: CurrentUserModel
    ) -> Dict[str, Any]:
        """
        验证模型提供商凭据
        
        Args:
            db: 数据库会话
            credentials: 凭据信息
            current_user: 当前用户
            
        Returns:
            验证结果
        """
        try:
            provider_name = credentials.get("provider")
            if not provider_name:
                return ServiceResult.failed(message="提供商名称不能为空")
                
            provider_factory = ModelProviderFactory()
            provider = provider_factory.get_provider(provider_name)
            
            if not provider:
                return ServiceResult.failed(message=f"提供商 {provider_name} 不存在")
            
            validation_result = provider.validate_provider_credentials(credentials)
            return validation_result
        except Exception as e:
            return ServiceResult.failed(message=f"验证凭据失败: {str(e)}")

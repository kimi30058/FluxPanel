from typing import Dict, List, Optional, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_ai.dao.ai_provider_dao import TraditionalProviderDao, DifyApplicationDao, CozeApplicationDao, AIApplicationDao
from module_ai.entity.do.ai_do import TraditionalProvider, DifyApplication, CozeApplication, AIApplication
from utils.service_result_util import ServiceResult


class TraditionalProviderService:
    """传统AI供应商服务"""
    
    @staticmethod
    async def get_provider_list(
        db: AsyncSession, 
        is_active: bool = None, 
        provider_type: str = None,
        page_num: int = 1, 
        page_size: int = 10,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        获取供应商列表
        
        Args:
            db: 数据库会话
            is_active: 是否启用
            provider_type: 供应商类型
            page_num: 页码
            page_size: 每页条数
            current_user: 当前用户
            
        Returns:
            供应商列表
        """
        try:
            result = await TraditionalProviderDao.get_list(
                db, is_active, provider_type, page_num, page_size
            )
            return result
        except Exception as e:
            return ServiceResult.failed(message=f"获取供应商列表失败: {str(e)}")
    
    @staticmethod
    async def get_provider_by_id(
        db: AsyncSession, 
        provider_id: int,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        根据ID获取供应商
        
        Args:
            db: 数据库会话
            provider_id: 供应商ID
            current_user: 当前用户
            
        Returns:
            供应商信息
        """
        try:
            provider = await TraditionalProviderDao.get_by_id(db, provider_id)
            if not provider:
                return ServiceResult.failed(message=f"供应商不存在: {provider_id}")
            return provider
        except Exception as e:
            return ServiceResult.failed(message=f"获取供应商失败: {str(e)}")
    
    @staticmethod
    async def add_provider(
        db: AsyncSession, 
        provider_data: Dict,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        添加供应商
        
        Args:
            db: 数据库会话
            provider_data: 供应商数据
            current_user: 当前用户
            
        Returns:
            添加结果
        """
        try:
            from module_ai.service.model_runtime_service import ModelRuntimeService
            credentials = {
                "provider": provider_data.get("provider"),
                "api_key": provider_data.get("api_key"),
                "base_url": provider_data.get("base_url")
            }
            validation_result = await ModelRuntimeService.validate_provider_credentials_services(
                db, credentials, current_user
            )
            
            if not validation_result.get("success", False):
                return ServiceResult.failed(message=f"供应商凭据验证失败: {validation_result.get('message')}")
            
            provider = await TraditionalProviderDao.add(db, provider_data)
            await db.commit()
            
            return ServiceResult.success(data=provider, message="添加供应商成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"添加供应商失败: {str(e)}")
    
    @staticmethod
    async def update_provider(
        db: AsyncSession, 
        provider_id: int, 
        provider_data: Dict,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        更新供应商
        
        Args:
            db: 数据库会话
            provider_id: 供应商ID
            provider_data: 供应商数据
            current_user: 当前用户
            
        Returns:
            更新结果
        """
        try:
            from module_ai.service.model_runtime_service import ModelRuntimeService
            credentials = {
                "provider": provider_data.get("provider"),
                "api_key": provider_data.get("api_key"),
                "base_url": provider_data.get("base_url")
            }
            validation_result = await ModelRuntimeService.validate_provider_credentials_services(
                db, credentials, current_user
            )
            
            if not validation_result.get("success", False):
                return ServiceResult.failed(message=f"供应商凭据验证失败: {validation_result.get('message')}")
            
            provider = await TraditionalProviderDao.update(db, provider_id, provider_data)
            if not provider:
                return ServiceResult.failed(message=f"供应商不存在: {provider_id}")
                
            await db.commit()
            
            return ServiceResult.success(data=provider, message="更新供应商成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"更新供应商失败: {str(e)}")
    
    @staticmethod
    async def delete_provider(
        db: AsyncSession, 
        provider_ids: List[int],
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        删除供应商
        
        Args:
            db: 数据库会话
            provider_ids: 供应商ID列表
            current_user: 当前用户
            
        Returns:
            删除结果
        """
        try:
            result = await TraditionalProviderDao.delete(db, provider_ids)
            if not result:
                return ServiceResult.failed(message="删除供应商失败")
                
            await db.commit()
            
            return ServiceResult.success(message="删除供应商成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"删除供应商失败: {str(e)}")


class DifyApplicationService:
    """Dify应用服务"""
    
    @staticmethod
    async def get_app_list(
        db: AsyncSession, 
        is_active: bool = None,
        page_num: int = 1, 
        page_size: int = 10,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        获取Dify应用列表
        
        Args:
            db: 数据库会话
            is_active: 是否启用
            page_num: 页码
            page_size: 每页条数
            current_user: 当前用户
            
        Returns:
            应用列表
        """
        try:
            result = await DifyApplicationDao.get_list(
                db, is_active, page_num, page_size
            )
            return result
        except Exception as e:
            return ServiceResult.failed(message=f"获取Dify应用列表失败: {str(e)}")
    
    @staticmethod
    async def get_app_by_id(
        db: AsyncSession, 
        app_id: int,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        根据ID获取Dify应用
        
        Args:
            db: 数据库会话
            app_id: 应用ID
            current_user: 当前用户
            
        Returns:
            应用信息
        """
        try:
            app = await DifyApplicationDao.get_by_id(db, app_id)
            if not app:
                return ServiceResult.failed(message=f"Dify应用不存在: {app_id}")
            return app
        except Exception as e:
            return ServiceResult.failed(message=f"获取Dify应用失败: {str(e)}")
    
    @staticmethod
    async def add_app(
        db: AsyncSession, 
        app_data: Dict,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        添加Dify应用
        
        Args:
            db: 数据库会话
            app_data: 应用数据
            current_user: 当前用户
            
        Returns:
            添加结果
        """
        try:
            from module_ai.service.dify_service import DifyService
            dify_service = DifyService(
                api_key=app_data.get("api_key"),
                app_id=app_data.get("app_id"),
                api_base=app_data.get("api_base", "www.ai-agent.chat/v1")
            )
            
            valid = await dify_service.validate_credentials()
            if not valid:
                return ServiceResult.failed(message="Dify应用凭据验证失败")
            
            app = await DifyApplicationDao.add(db, app_data)
            await db.commit()
            
            return ServiceResult.success(data=app, message="添加Dify应用成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"添加Dify应用失败: {str(e)}")
    
    @staticmethod
    async def update_app(
        db: AsyncSession, 
        app_id: int, 
        app_data: Dict,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        更新Dify应用
        
        Args:
            db: 数据库会话
            app_id: 应用ID
            app_data: 应用数据
            current_user: 当前用户
            
        Returns:
            更新结果
        """
        try:
            from module_ai.service.dify_service import DifyService
            dify_service = DifyService(
                api_key=app_data.get("api_key"),
                app_id=app_data.get("app_id"),
                api_base=app_data.get("api_base", "www.ai-agent.chat/v1")
            )
            
            valid = await dify_service.validate_credentials()
            if not valid:
                return ServiceResult.failed(message="Dify应用凭据验证失败")
            
            app = await DifyApplicationDao.update(db, app_id, app_data)
            if not app:
                return ServiceResult.failed(message=f"Dify应用不存在: {app_id}")
                
            await db.commit()
            
            return ServiceResult.success(data=app, message="更新Dify应用成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"更新Dify应用失败: {str(e)}")
    
    @staticmethod
    async def delete_app(
        db: AsyncSession, 
        app_ids: List[int],
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        删除Dify应用
        
        Args:
            db: 数据库会话
            app_ids: 应用ID列表
            current_user: 当前用户
            
        Returns:
            删除结果
        """
        try:
            result = await DifyApplicationDao.delete(db, app_ids)
            if not result:
                return ServiceResult.failed(message="删除Dify应用失败")
                
            await db.commit()
            
            return ServiceResult.success(message="删除Dify应用成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"删除Dify应用失败: {str(e)}")


class CozeApplicationService:
    """Coze应用服务"""
    
    @staticmethod
    async def get_app_list(
        db: AsyncSession, 
        is_active: bool = None,
        page_num: int = 1, 
        page_size: int = 10,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        获取Coze应用列表
        
        Args:
            db: 数据库会话
            is_active: 是否启用
            page_num: 页码
            page_size: 每页条数
            current_user: 当前用户
            
        Returns:
            应用列表
        """
        try:
            result = await CozeApplicationDao.get_list(
                db, is_active, page_num, page_size
            )
            return result
        except Exception as e:
            return ServiceResult.failed(message=f"获取Coze应用列表失败: {str(e)}")
    
    @staticmethod
    async def get_app_by_id(
        db: AsyncSession, 
        app_id: int,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        根据ID获取Coze应用
        
        Args:
            db: 数据库会话
            app_id: 应用ID
            current_user: 当前用户
            
        Returns:
            应用信息
        """
        try:
            app = await CozeApplicationDao.get_by_id(db, app_id)
            if not app:
                return ServiceResult.failed(message=f"Coze应用不存在: {app_id}")
            return app
        except Exception as e:
            return ServiceResult.failed(message=f"获取Coze应用失败: {str(e)}")
    
    @staticmethod
    async def add_app(
        db: AsyncSession, 
        app_data: Dict,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        添加Coze应用
        
        Args:
            db: 数据库会话
            app_data: 应用数据
            current_user: 当前用户
            
        Returns:
            添加结果
        """
        try:
            from module_ai.service.coze_service import CozeService
            coze_service = CozeService(
                api_key=app_data.get("api_key"),
                workflow_id=app_data.get("workflow_id"),
                agent_id=app_data.get("agent_id")
            )
            
            valid = await coze_service.validate_credentials()
            if not valid:
                return ServiceResult.failed(message="Coze应用凭据验证失败")
            
            app = await CozeApplicationDao.add(db, app_data)
            await db.commit()
            
            return ServiceResult.success(data=app, message="添加Coze应用成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"添加Coze应用失败: {str(e)}")
    
    @staticmethod
    async def update_app(
        db: AsyncSession, 
        app_id: int, 
        app_data: Dict,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        更新Coze应用
        
        Args:
            db: 数据库会话
            app_id: 应用ID
            app_data: 应用数据
            current_user: 当前用户
            
        Returns:
            更新结果
        """
        try:
            from module_ai.service.coze_service import CozeService
            coze_service = CozeService(
                api_key=app_data.get("api_key"),
                workflow_id=app_data.get("workflow_id"),
                agent_id=app_data.get("agent_id")
            )
            
            valid = await coze_service.validate_credentials()
            if not valid:
                return ServiceResult.failed(message="Coze应用凭据验证失败")
            
            app = await CozeApplicationDao.update(db, app_id, app_data)
            if not app:
                return ServiceResult.failed(message=f"Coze应用不存在: {app_id}")
                
            await db.commit()
            
            return ServiceResult.success(data=app, message="更新Coze应用成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"更新Coze应用失败: {str(e)}")
    
    @staticmethod
    async def delete_app(
        db: AsyncSession, 
        app_ids: List[int],
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        删除Coze应用
        
        Args:
            db: 数据库会话
            app_ids: 应用ID列表
            current_user: 当前用户
            
        Returns:
            删除结果
        """
        try:
            result = await CozeApplicationDao.delete(db, app_ids)
            if not result:
                return ServiceResult.failed(message="删除Coze应用失败")
                
            await db.commit()
            
            return ServiceResult.success(message="删除Coze应用成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"删除Coze应用失败: {str(e)}")


class AIApplicationService:
    """AI应用服务"""
    
    @staticmethod
    async def get_app_list(
        db: AsyncSession, 
        type: str = None,
        is_enabled: bool = None,
        page_num: int = 1, 
        page_size: int = 10,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        获取AI应用列表
        
        Args:
            db: 数据库会话
            type: 应用类型
            is_enabled: 是否启用
            page_num: 页码
            page_size: 每页条数
            current_user: 当前用户
            
        Returns:
            应用列表
        """
        try:
            result = await AIApplicationDao.get_list(
                db, type, is_enabled, page_num, page_size
            )
            return result
        except Exception as e:
            return ServiceResult.failed(message=f"获取AI应用列表失败: {str(e)}")
    
    @staticmethod
    async def get_app_by_id(
        db: AsyncSession, 
        app_id: int,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        根据ID获取AI应用
        
        Args:
            db: 数据库会话
            app_id: 应用ID
            current_user: 当前用户
            
        Returns:
            应用信息
        """
        try:
            app = await AIApplicationDao.get_by_id(db, app_id)
            if not app:
                return ServiceResult.failed(message=f"AI应用不存在: {app_id}")
                
            result = {
                "app": app,
                "provider": None,
                "dify_app": None,
                "coze_app": None
            }
            
            if app.id_traditional_provider:
                result["provider"] = await TraditionalProviderDao.get_by_id(db, app.id_traditional_provider)
                
            if app.id_dify_app:
                result["dify_app"] = await DifyApplicationDao.get_by_id(db, app.id_dify_app)
                
            if app.id_coze_app:
                result["coze_app"] = await CozeApplicationDao.get_by_id(db, app.id_coze_app)
                
            return result
        except Exception as e:
            return ServiceResult.failed(message=f"获取AI应用失败: {str(e)}")
    
    @staticmethod
    async def add_app(
        db: AsyncSession, 
        app_data: Dict,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        添加AI应用
        
        Args:
            db: 数据库会话
            app_data: 应用数据
            current_user: 当前用户
            
        Returns:
            添加结果
        """
        try:
            if app_data.get("id_traditional_provider"):
                provider = await TraditionalProviderDao.get_by_id(db, app_data.get("id_traditional_provider"))
                if not provider:
                    return ServiceResult.failed(message=f"关联的传统AI供应商不存在: {app_data.get('id_traditional_provider')}")
                    
            if app_data.get("id_dify_app"):
                dify_app = await DifyApplicationDao.get_by_id(db, app_data.get("id_dify_app"))
                if not dify_app:
                    return ServiceResult.failed(message=f"关联的Dify应用不存在: {app_data.get('id_dify_app')}")
                    
            if app_data.get("id_coze_app"):
                coze_app = await CozeApplicationDao.get_by_id(db, app_data.get("id_coze_app"))
                if not coze_app:
                    return ServiceResult.failed(message=f"关联的Coze应用不存在: {app_data.get('id_coze_app')}")
            
            app = await AIApplicationDao.add(db, app_data)
            await db.commit()
            
            return ServiceResult.success(data=app, message="添加AI应用成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"添加AI应用失败: {str(e)}")
    
    @staticmethod
    async def update_app(
        db: AsyncSession, 
        app_id: int, 
        app_data: Dict,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        更新AI应用
        
        Args:
            db: 数据库会话
            app_id: 应用ID
            app_data: 应用数据
            current_user: 当前用户
            
        Returns:
            更新结果
        """
        try:
            if app_data.get("id_traditional_provider"):
                provider = await TraditionalProviderDao.get_by_id(db, app_data.get("id_traditional_provider"))
                if not provider:
                    return ServiceResult.failed(message=f"关联的传统AI供应商不存在: {app_data.get('id_traditional_provider')}")
                    
            if app_data.get("id_dify_app"):
                dify_app = await DifyApplicationDao.get_by_id(db, app_data.get("id_dify_app"))
                if not dify_app:
                    return ServiceResult.failed(message=f"关联的Dify应用不存在: {app_data.get('id_dify_app')}")
                    
            if app_data.get("id_coze_app"):
                coze_app = await CozeApplicationDao.get_by_id(db, app_data.get("id_coze_app"))
                if not coze_app:
                    return ServiceResult.failed(message=f"关联的Coze应用不存在: {app_data.get('id_coze_app')}")
            
            app = await AIApplicationDao.update(db, app_id, app_data)
            if not app:
                return ServiceResult.failed(message=f"AI应用不存在: {app_id}")
                
            await db.commit()
            
            return ServiceResult.success(data=app, message="更新AI应用成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"更新AI应用失败: {str(e)}")
    
    @staticmethod
    async def delete_app(
        db: AsyncSession, 
        app_ids: List[int],
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        删除AI应用
        
        Args:
            db: 数据库会话
            app_ids: 应用ID列表
            current_user: 当前用户
            
        Returns:
            删除结果
        """
        try:
            result = await AIApplicationDao.delete(db, app_ids)
            if not result:
                return ServiceResult.failed(message="删除AI应用失败")
                
            await db.commit()
            
            return ServiceResult.success(message="删除AI应用成功")
        except Exception as e:
            await db.rollback()
            return ServiceResult.failed(message=f"删除AI应用失败: {str(e)}")

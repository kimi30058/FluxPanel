from typing import Dict, List, Optional, Any, Union
import aiohttp
import json
from sqlalchemy.ext.asyncio import AsyncSession
from module_ai.dao.ai_provider_dao import AIApplicationDao, TraditionalProviderDao, DifyApplicationDao, CozeApplicationDao
from module_ai.entity.do.ai_do import AIApplication, TraditionalProvider, DifyApplication, CozeApplication
from module_ai.core.model_runtime.model_providers.model_provider_factory import ModelProviderFactory
from module_ai.core.model_runtime.entities.model_entities import ModelType
from utils.service_result_util import ServiceResult


class AIServiceBase:
    """AI服务基类"""
    
    async def validate_credentials(self) -> bool:
        """验证凭据是否有效"""
        raise NotImplementedError("子类必须实现此方法")
    
    async def send_message(
        self, 
        chat_id: int, 
        user_message: str, 
        history_messages: List[Dict] = None, 
        system_prompt: str = None,
        user_id: str = None
    ) -> Dict:
        """发送消息并获取回复"""
        raise NotImplementedError("子类必须实现此方法")


class TraditionalAIService(AIServiceBase):
    """传统AI服务"""
    
    def __init__(self, provider: TraditionalProvider, app: AIApplication):
        self.provider = provider
        self.app = app
        self.provider_name = provider.provider
        self.api_key = provider.api_key
        self.base_url = provider.base_url
        self.model_factory = ModelProviderFactory()
        self.model_provider = self.model_factory.get_provider(self.provider_name)
    
    async def validate_credentials(self) -> bool:
        """验证凭据是否有效"""
        try:
            credentials = {
                "api_key": self.api_key
            }
            
            if self.base_url:
                credentials["base_url"] = self.base_url
                
            result = self.model_provider.validate_provider_credentials(credentials)
            return result.get("success", False)
        except Exception as e:
            return False
    
    async def send_message(
        self, 
        chat_id: int, 
        user_message: str, 
        history_messages: List[Dict] = None, 
        system_prompt: str = None,
        user_id: str = None
    ) -> Dict:
        """发送消息并获取回复"""
        try:
            llm_models = self.model_provider.get_models(ModelType.LLM)
            if not llm_models:
                return {
                    "error": True,
                    "message": f"提供商 {self.provider_name} 没有可用的LLM模型"
                }
            
            model_name = llm_models[0].model
            
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            if history_messages:
                for msg in history_messages:
                    if msg.role != "system":  # 跳过系统消息，因为已经添加了
                        messages.append({
                            "role": msg.role,
                            "content": msg.content
                        })
            
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            credentials = {
                "api_key": self.api_key
            }
            
            if self.base_url:
                credentials["base_url"] = self.base_url
                
            llm = self.model_provider.get_model_instance(ModelType.LLM, model_name, credentials)
            
            model_parameters = {
                "temperature": 0.7,
                "top_p": 1.0,
                "max_tokens": 2000
            }
            
            response = await llm.acompletion(
                messages=messages,
                model_parameters=model_parameters
            )
            
            return {
                "answer": response.message.content,
                "metadata": {
                    "model": model_name,
                    "provider": self.provider_name,
                    "usage": response.usage.dict() if response.usage else {}
                }
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }


class DifyService(AIServiceBase):
    """Dify服务"""
    
    def __init__(self, api_key: str, app_id: str, api_base: str = "www.ai-agent.chat/v1"):
        self.api_key = api_key
        self.app_id = app_id
        self.api_base = api_base
        self.conversation_mode = "chat"
        self.response_mode = "blocking"
    
    async def validate_credentials(self) -> bool:
        """验证凭据是否有效"""
        try:
            url = f"https://{self.api_base}/chat-messages"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "inputs": {},
                "query": "测试连接",
                "response_mode": self.response_mode,
                "conversation_id": None,
                "user": "system"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return True
                    else:
                        return False
        except Exception as e:
            return False
    
    async def send_message(
        self, 
        chat_id: int, 
        user_message: str, 
        history_messages: List[Dict] = None, 
        system_prompt: str = None,
        user_id: str = None
    ) -> Dict:
        """发送消息并获取回复"""
        try:
            url = f"https://{self.api_base}/chat-messages"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            conversation_id = None
            if history_messages and len(history_messages) > 0:
                for msg in history_messages:
                    if msg.metadata and msg.metadata.get("conversation_id"):
                        conversation_id = msg.metadata.get("conversation_id")
                        break
            
            data = {
                "inputs": {},
                "query": user_message,
                "response_mode": self.response_mode,
                "conversation_id": conversation_id,
                "user": user_id or "default_user"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        return {
                            "answer": result.get("answer", ""),
                            "conversation_id": result.get("conversation_id"),
                            "message_id": result.get("id"),
                            "metadata": {
                                "provider": "dify",
                                "app_id": self.app_id,
                                "usage": result.get("metadata", {}).get("usage", {})
                            }
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "error": True,
                            "message": f"Dify API错误: {response.status} - {error_text}"
                        }
        except Exception as e:
            return {
                "error": True,
                "message": f"调用Dify API失败: {str(e)}"
            }


class CozeService(AIServiceBase):
    """Coze服务"""
    
    def __init__(self, api_key: str, workflow_id: str = None, agent_id: str = None):
        self.api_key = api_key
        self.workflow_id = workflow_id
        self.agent_id = agent_id
        self.api_base = "api.coze.com"
    
    async def validate_credentials(self) -> bool:
        """验证凭据是否有效"""
        try:
            url = f"https://{self.api_base}/v1/message"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "query": "测试连接",
                "user_id": "system"
            }
            
            if self.workflow_id:
                data["workflow_id"] = self.workflow_id
            elif self.agent_id:
                data["agent_id"] = self.agent_id
            else:
                return False
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return True
                    else:
                        return False
        except Exception as e:
            return False
    
    async def send_message(
        self, 
        chat_id: int, 
        user_message: str, 
        history_messages: List[Dict] = None, 
        system_prompt: str = None,
        user_id: str = None
    ) -> Dict:
        """发送消息并获取回复"""
        try:
            url = f"https://{self.api_base}/v1/message"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            conversation_id = None
            if history_messages and len(history_messages) > 0:
                for msg in history_messages:
                    if msg.metadata and msg.metadata.get("conversation_id"):
                        conversation_id = msg.metadata.get("conversation_id")
                        break
            
            data = {
                "query": user_message,
                "user_id": user_id or "default_user"
            }
            
            if conversation_id:
                data["conversation_id"] = conversation_id
                
            if self.workflow_id:
                data["workflow_id"] = self.workflow_id
            elif self.agent_id:
                data["agent_id"] = self.agent_id
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        return {
                            "answer": result.get("response", ""),
                            "conversation_id": result.get("conversation_id"),
                            "message_id": result.get("message_id"),
                            "metadata": {
                                "provider": "coze",
                                "workflow_id": self.workflow_id,
                                "agent_id": self.agent_id
                            }
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "error": True,
                            "message": f"Coze API错误: {response.status} - {error_text}"
                        }
        except Exception as e:
            return {
                "error": True,
                "message": f"调用Coze API失败: {str(e)}"
            }


class AIServiceManager:
    """AI服务管理器"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_service(self, app_id: int) -> Optional[AIServiceBase]:
        """
        获取AI服务实例
        
        Args:
            app_id: AI应用ID
            
        Returns:
            AI服务实例
        """
        try:
            app = await AIApplicationDao.get_by_id(self.db, app_id)
            if not app:
                return None
            
            if app.id_traditional_provider:
                provider = await TraditionalProviderDao.get_by_id(self.db, app.id_traditional_provider)
                if not provider:
                    return None
                
                return TraditionalAIService(provider, app)
            elif app.id_dify_app:
                dify_app = await DifyApplicationDao.get_by_id(self.db, app.id_dify_app)
                if not dify_app:
                    return None
                
                return DifyService(
                    api_key=dify_app.api_key,
                    app_id=dify_app.app_id,
                    api_base=dify_app.api_base
                )
            elif app.id_coze_app:
                coze_app = await CozeApplicationDao.get_by_id(self.db, app.id_coze_app)
                if not coze_app:
                    return None
                
                return CozeService(
                    api_key=coze_app.api_key,
                    workflow_id=coze_app.workflow_id,
                    agent_id=coze_app.agent_id
                )
            else:
                return None
        except Exception as e:
            return None

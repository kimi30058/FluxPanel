from io import BytesIO
from typing import Any, Dict, List, Optional, Union, Iterable

from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.vo.user_vo import CurrentUserModel
from module_ai.core.model_runtime.model_providers.model_provider_factory import ModelProviderFactory
from module_ai.core.model_runtime.entities.model_entities import ModelType
from module_ai.core.model_runtime.entities.message_entities import PromptMessage, PromptMessageTool
from module_ai.core.model_runtime.entities.embedding_type import EmbeddingInputType
from utils.service_result_util import ServiceResult


class ModelInvokeService:
    """
    模型调用服务
    """
    
    @staticmethod
    async def invoke_llm_services(
        db: AsyncSession,
        provider: str,
        model: str,
        prompt_messages: List[Dict],
        model_parameters: Optional[Dict] = None,
        tools: Optional[List[Dict]] = None,
        stop: Optional[List[str]] = None,
        stream: bool = False,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        调用大语言模型
        
        Args:
            db: 数据库会话
            provider: 提供商名称
            model: 模型名称
            prompt_messages: 提示消息列表
            model_parameters: 模型参数
            tools: 工具列表
            stop: 停止词列表
            stream: 是否流式响应
            current_user: 当前用户
            
        Returns:
            模型响应结果
        """
        try:
            converted_prompt_messages = [PromptMessage.from_dict(msg) for msg in prompt_messages]
            
            converted_tools = None
            if tools:
                converted_tools = [PromptMessageTool.from_dict(tool) for tool in tools]
            
            provider_factory = ModelProviderFactory()
            provider_instance = provider_factory.get_provider(provider)
            
            if not provider_instance:
                return ServiceResult.failed(message=f"提供商 {provider} 不存在")
            
            model_instance = provider_instance.get_model_instance(ModelType.LLM, model)
            
            result = model_instance.invoke(
                prompt_messages=converted_prompt_messages,
                model_parameters=model_parameters,
                tools=converted_tools,
                stop=stop,
                stream=stream,
                user=current_user.user_id if current_user else None
            )
            
            if stream:
                return {"stream": True, "generator": result}
            
            return result.dict()
        except Exception as e:
            return ServiceResult.failed(message=f"调用大语言模型失败: {str(e)}")
    
    @staticmethod
    async def invoke_embedding_services(
        db: AsyncSession,
        provider: str,
        model: str,
        texts: List[str],
        input_type: str = "document",
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        调用文本嵌入模型
        
        Args:
            db: 数据库会话
            provider: 提供商名称
            model: 模型名称
            texts: 文本列表
            input_type: 输入类型
            current_user: 当前用户
            
        Returns:
            嵌入结果
        """
        try:
            embedding_input_type = EmbeddingInputType(input_type)
            
            provider_factory = ModelProviderFactory()
            provider_instance = provider_factory.get_provider(provider)
            
            if not provider_instance:
                return ServiceResult.failed(message=f"提供商 {provider} 不存在")
            
            model_instance = provider_instance.get_model_instance(ModelType.TEXT_EMBEDDING, model)
            
            result = model_instance.invoke(
                texts=texts,
                input_type=embedding_input_type,
                user=current_user.user_id if current_user else None
            )
            
            return result.dict()
        except Exception as e:
            return ServiceResult.failed(message=f"调用文本嵌入模型失败: {str(e)}")
    
    @staticmethod
    async def invoke_rerank_services(
        db: AsyncSession,
        provider: str,
        model: str,
        query: str,
        docs: List[str],
        score_threshold: Optional[float] = None,
        top_n: Optional[int] = None,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        调用重排序模型
        
        Args:
            db: 数据库会话
            provider: 提供商名称
            model: 模型名称
            query: 查询文本
            docs: 文档列表
            score_threshold: 分数阈值
            top_n: 返回前N个结果
            current_user: 当前用户
            
        Returns:
            重排序结果
        """
        try:
            provider_factory = ModelProviderFactory()
            provider_instance = provider_factory.get_provider(provider)
            
            if not provider_instance:
                return ServiceResult.failed(message=f"提供商 {provider} 不存在")
            
            model_instance = provider_instance.get_model_instance(ModelType.RERANK, model)
            
            result = model_instance.invoke(
                query=query,
                docs=docs,
                score_threshold=score_threshold,
                top_n=top_n,
                user=current_user.user_id if current_user else None
            )
            
            return result.dict()
        except Exception as e:
            return ServiceResult.failed(message=f"调用重排序模型失败: {str(e)}")
    
    @staticmethod
    async def invoke_moderation_services(
        db: AsyncSession,
        provider: str,
        model: str,
        text: str,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        调用内容审核模型
        
        Args:
            db: 数据库会话
            provider: 提供商名称
            model: 模型名称
            text: 待审核文本
            current_user: 当前用户
            
        Returns:
            审核结果
        """
        try:
            provider_factory = ModelProviderFactory()
            provider_instance = provider_factory.get_provider(provider)
            
            if not provider_instance:
                return ServiceResult.failed(message=f"提供商 {provider} 不存在")
            
            model_instance = provider_instance.get_model_instance(ModelType.MODERATION, model)
            
            result = model_instance.invoke(
                text=text,
                user=current_user.user_id if current_user else None
            )
            
            return {"flagged": result}
        except Exception as e:
            return ServiceResult.failed(message=f"调用内容审核模型失败: {str(e)}")
    
    @staticmethod
    async def invoke_speech2text_services(
        db: AsyncSession,
        provider: str,
        model: str,
        file: BytesIO,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        调用语音转文本模型
        
        Args:
            db: 数据库会话
            provider: 提供商名称
            model: 模型名称
            file: 音频文件
            current_user: 当前用户
            
        Returns:
            转换结果
        """
        try:
            provider_factory = ModelProviderFactory()
            provider_instance = provider_factory.get_provider(provider)
            
            if not provider_instance:
                return ServiceResult.failed(message=f"提供商 {provider} 不存在")
            
            model_instance = provider_instance.get_model_instance(ModelType.SPEECH2TEXT, model)
            
            result = model_instance.invoke(
                file=file,
                user=current_user.user_id if current_user else None
            )
            
            return {"text": result}
        except Exception as e:
            return ServiceResult.failed(message=f"调用语音转文本模型失败: {str(e)}")
    
    @staticmethod
    async def invoke_tts_services(
        db: AsyncSession,
        provider: str,
        model: str,
        content_text: str,
        voice: str,
        current_user: CurrentUserModel = None
    ) -> Iterable[bytes]:
        """
        调用文本转语音模型
        
        Args:
            db: 数据库会话
            provider: 提供商名称
            model: 模型名称
            content_text: 文本内容
            voice: 声音
            current_user: 当前用户
            
        Returns:
            音频数据流
        """
        try:
            provider_factory = ModelProviderFactory()
            provider_instance = provider_factory.get_provider(provider)
            
            if not provider_instance:
                return ServiceResult.failed(message=f"提供商 {provider} 不存在")
            
            model_instance = provider_instance.get_model_instance(ModelType.TTS, model)
            
            result = model_instance.invoke(
                content_text=content_text,
                voice=voice,
                user=current_user.user_id if current_user else None
            )
            
            return result
        except Exception as e:
            return ServiceResult.failed(message=f"调用文本转语音模型失败: {str(e)}")
    
    @staticmethod
    async def get_tts_voices_services(
        db: AsyncSession,
        provider: str,
        model: str,
        language: Optional[str] = None,
        current_user: CurrentUserModel = None
    ) -> Dict[str, Any]:
        """
        获取文本转语音模型的声音列表
        
        Args:
            db: 数据库会话
            provider: 提供商名称
            model: 模型名称
            language: 语言
            current_user: 当前用户
            
        Returns:
            声音列表
        """
        try:
            provider_factory = ModelProviderFactory()
            provider_instance = provider_factory.get_provider(provider)
            
            if not provider_instance:
                return ServiceResult.failed(message=f"提供商 {provider} 不存在")
            
            model_instance = provider_instance.get_model_instance(ModelType.TTS, model)
            
            voices = model_instance.get_tts_voices(language=language)
            
            return {"voices": voices}
        except Exception as e:
            return ServiceResult.failed(message=f"获取文本转语音模型声音列表失败: {str(e)}")

import re
import tiktoken
from typing import Dict, List, Optional, Any, Union

class TokenUtils:
    """Token计算工具类"""
    
    @staticmethod
    def num_tokens_from_string(string: str, model: str = "gpt-3.5-turbo") -> int:
        """
        计算字符串的token数量
        
        Args:
            string: 输入字符串
            model: 模型名称
            
        Returns:
            token数量
        """
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(string))
        except Exception:
            chinese_char_count = len(re.findall(r'[\u4e00-\u9fff]', string))
            other_char_count = len(string) - chinese_char_count
            return int(chinese_char_count / 1.5) + int(other_char_count / 4) + 1
    
    @staticmethod
    def truncate_messages_to_fit_context(
        messages: List[Dict], 
        system_prompt: str = None, 
        max_turns: int = 10, 
        max_tokens: int = 4000,
        preserve_system_prompt: bool = True,
        model: str = "gpt-3.5-turbo"
    ) -> List[Dict]:
        """
        截断消息以适应上下文窗口
        
        Args:
            messages: 消息列表
            system_prompt: 系统提示词
            max_turns: 最大对话轮次
            max_tokens: 最大token数
            preserve_system_prompt: 是否始终保留系统提示词
            model: 模型名称
            
        Returns:
            截断后的消息列表
        """
        if len(messages) <= max_turns:
            return messages
        
        system_prompt_tokens = 0
        if system_prompt and preserve_system_prompt:
            system_prompt_tokens = TokenUtils.num_tokens_from_string(system_prompt, model)
        
        truncated_messages = messages[-max_turns:]
        
        if system_prompt and preserve_system_prompt:
            has_system_prompt = False
            for msg in truncated_messages:
                if msg.get("role") == "system":
                    has_system_prompt = True
                    break
            
            if not has_system_prompt:
                truncated_messages.insert(0, {
                    "role": "system",
                    "content": system_prompt
                })
        
        total_tokens = sum(TokenUtils.num_tokens_from_string(msg.get("content", ""), model) for msg in truncated_messages)
        
        while total_tokens > max_tokens and len(truncated_messages) > 1:
            if preserve_system_prompt and truncated_messages[0].get("role") == "system":
                removed_msg = truncated_messages.pop(1)
            else:
                removed_msg = truncated_messages.pop(0)
            
            total_tokens -= TokenUtils.num_tokens_from_string(removed_msg.get("content", ""), model)
        
        return truncated_messages
    
    @staticmethod
    def get_model_context_window(model: str) -> int:
        """
        获取模型的上下文窗口大小
        
        Args:
            model: 模型名称
            
        Returns:
            上下文窗口大小
        """
        context_windows = {
            "gpt-3.5-turbo": 4096,
            "gpt-3.5-turbo-16k": 16384,
            "gpt-4": 8192,
            "gpt-4-32k": 32768,
            "gpt-4-turbo": 128000,
            "gpt-4o": 128000,
            "claude-instant-1": 100000,
            "claude-2": 100000,
            "claude-3-opus": 200000,
            "claude-3-sonnet": 200000,
            "claude-3-haiku": 200000,
            "mistral-tiny": 8192,
            "mistral-small": 32768,
            "mistral-medium": 32768,
            "mistral-large": 32768,
            "command": 4096,
            "command-light": 4096,
            "command-r": 128000,
            "command-r-plus": 128000,
            "gemini-pro": 32768,
            "gemini-ultra": 32768,
            "llama-2-7b": 4096,
            "llama-2-13b": 4096,
            "llama-2-70b": 4096,
            "llama-3-8b": 8192,
            "llama-3-70b": 8192,
            "qwen-7b": 8192,
            "qwen-14b": 8192,
            "qwen-72b": 8192,
            "baichuan-7b": 4096,
            "baichuan-13b": 4096,
            "chatglm-6b": 2048,
            "chatglm2-6b": 8192,
            "chatglm3-6b": 8192,
            "yi-6b": 4096,
            "yi-34b": 4096,
            "deepseek-7b": 4096,
            "deepseek-67b": 4096,
        }
        
        default_window = 4096
        
        for model_prefix, window_size in context_windows.items():
            if model.lower().startswith(model_prefix.lower()):
                return window_size
        
        return default_window
    
    @staticmethod
    def format_messages_for_model(
        messages: List[Dict], 
        system_prompt: str = None,
        max_tokens: int = None,
        model: str = "gpt-3.5-turbo"
    ) -> List[Dict]:
        """
        格式化消息以适应模型要求
        
        Args:
            messages: 消息列表
            system_prompt: 系统提示词
            max_tokens: 最大token数，如果为None则使用模型默认值
            model: 模型名称
            
        Returns:
            格式化后的消息列表
        """
        formatted_messages = []
        
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        for msg in messages:
            if msg.get("role") != "system" or not system_prompt:  # 如果已经添加了系统提示词，跳过其他系统消息
                formatted_messages.append({
                    "role": msg.get("role"),
                    "content": msg.get("content", "")
                })
        
        if max_tokens:
            context_window = TokenUtils.get_model_context_window(model)
            
            max_tokens = min(max_tokens, context_window)
            
            formatted_messages = TokenUtils.truncate_messages_to_fit_context(
                formatted_messages,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                preserve_system_prompt=True,
                model=model
            )
        
        return formatted_messages

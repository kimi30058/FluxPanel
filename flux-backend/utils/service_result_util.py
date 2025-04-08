"""
Service result utility module for FluxPanel.

This module provides a utility class for service results.
"""

from typing import Any, Dict, List, Optional, Union


class ServiceResult:
    """
    Service result utility class.
    
    This class provides utility methods for service results.
    """
    
    @staticmethod
    def success(data: Any = None, message: str = "操作成功") -> Dict[str, Any]:
        """
        Create a success result.
        
        Args:
            data: Result data
            message: Result message
            
        Returns:
            Success result
        """
        return {
            "success": True,
            "data": data,
            "message": message
        }
    
    @staticmethod
    def failed(message: str = "操作失败", data: Any = None) -> Dict[str, Any]:
        """
        Create a failed result.
        
        Args:
            message: Result message
            data: Result data
            
        Returns:
            Failed result
        """
        return {
            "success": False,
            "data": data,
            "message": message
        }

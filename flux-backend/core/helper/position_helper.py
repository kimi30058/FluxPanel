"""
Position helper module for FluxPanel.

This module provides helper functions for sorting providers by position.
"""

import os
import yaml
from typing import Any, Callable, Dict, List, TypeVar

T = TypeVar('T')

def get_provider_position_map(model_providers_path: str) -> Dict[str, int]:
    """
    Get provider position map from _position.yaml file
    
    Args:
        model_providers_path: path to model_providers directory
        
    Returns:
        provider position map
    """
    position_file_path = os.path.join(model_providers_path, '_position.yaml')
    
    if not os.path.exists(position_file_path):
        default_positions = {
            'openai': 1,
            'anthropic': 2,
            'azure_openai': 3,
            'huggingface_hub': 4,
            'replicate': 5,
            'cohere': 6,
            'minimax': 7,
            'zhipuai': 8,
            'baichuan': 9,
            'moonshot': 10,
            'spark': 11,
            'tongyi': 12,
            'deepseek': 13,
            'dify': 14,
            'coze': 15,
        }
        
        with open(position_file_path, 'w') as f:
            yaml.dump(default_positions, f)
        
        return default_positions
    
    with open(position_file_path, 'r') as f:
        return yaml.safe_load(f)

def sort_to_dict_by_position_map(
    position_map: Dict[str, int], 
    data: List[T], 
    name_func: Callable[[T], str]
) -> Dict[str, T]:
    """
    Sort data by position map
    
    Args:
        position_map: provider position map
        data: data to sort
        name_func: function to get name from data
        
    Returns:
        sorted data as dict
    """
    result = {}
    
    sorted_data = sorted(
        data,
        key=lambda x: position_map.get(name_func(x), 999)
    )
    
    for item in sorted_data:
        name = name_func(item)
        result[name] = item
    
    return result

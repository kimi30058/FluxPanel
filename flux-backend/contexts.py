"""
Contexts module for FluxPanel.

This module provides context variables for the model_runtime module.
It's a simplified version of the contexts module from dify001.
"""

import contextvars
from threading import Lock

plugin_model_providers = contextvars.ContextVar('plugin_model_providers')
plugin_model_providers_lock = contextvars.ContextVar('plugin_model_providers_lock')

plugin_model_schemas = contextvars.ContextVar('plugin_model_schemas')
plugin_model_schema_lock = contextvars.ContextVar('plugin_model_schema_lock')

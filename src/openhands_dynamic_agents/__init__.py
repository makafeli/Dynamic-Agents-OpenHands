"""
OpenHands Dynamic Agents - A modular extension for dynamic agent generation.
"""

from .core.dynamic_agent import DynamicAgent
from .core.llm_factory import LLMAgentFactory
from .core.keyword_manager import KeywordManager
from .utils.result import OperationResult
from .analysis.tech_stack import TechStackAnalyzer
from .dashboard.app import Dashboard

__version__ = "0.1.0"
__all__ = [
    "DynamicAgent",
    "LLMAgentFactory",
    "KeywordManager",
    "OperationResult",
    "TechStackAnalyzer",
    "Dashboard"
]
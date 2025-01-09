"""
Custom exceptions for dynamic agents.
"""

from typing import Dict, Any, Optional

class DynamicAgentError(Exception):
    """Base error class for dynamic agents."""
    
    def __init__(
        self,
        message: str,
        error_type: str = "DynamicAgentError",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.details = details or {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        return {
            "message": self.message,
            "type": self.error_type,
            "details": self.details
        }

class ValidationError(DynamicAgentError):
    """Error raised during input validation."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message,
            error_type="ValidationError",
            details=details
        )

class GenerationError(DynamicAgentError):
    """Error raised during agent generation."""
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message,
            error_type="GenerationError",
            details=details
        )
"""
Enhanced prompt processing for dynamic agents.
"""

from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
import re
from pathlib import Path
import logging
import json

from ..utils.result import OperationResult

logger = logging.getLogger(__name__)

@dataclass
class PromptIntent:
    """Structured representation of prompt intent."""
    
    action: str  # e.g., "analyze", "optimize", "create"
    technologies: List[str]  # e.g., ["python", "django"]
    focus_areas: List[str]  # e.g., ["security", "performance"]
    constraints: Dict[str, Any]  # e.g., {"max_complexity": 10}
    context: Dict[str, Any]  # Additional context from prompt

    @property
    def primary_technology(self) -> Optional[str]:
        """Get the primary technology from the prompt."""
        return self.technologies[0] if self.technologies else None

    def requires_extension(self, extension_name: str) -> bool:
        """Check if this intent requires a specific extension."""
        return (
            extension_name in self.focus_areas or
            any(ext in self.focus_areas for ext in self.get_related_extensions(extension_name))
        )

    @staticmethod
    def get_related_extensions(extension_name: str) -> Set[str]:
        """Get related extensions for a given extension."""
        relations = {
            "security": {"vulnerability", "auth", "encryption"},
            "performance": {"optimization", "speed", "efficiency"},
            "quality": {"lint", "style", "complexity"}
        }
        return relations.get(extension_name, set())

class PromptProcessor:
    """
    Advanced prompt processing with intent recognition and context extraction.
    """
    
    # Common technology keywords and their variations
    TECH_PATTERNS = {
        "python": r"python|django|flask|fastapi",
        "javascript": r"javascript|js|node|nodejs|react|vue",
        "typescript": r"typescript|ts|angular",
        "database": r"sql|mysql|postgresql|mongodb",
        "cloud": r"aws|azure|gcp|cloud",
    }
    
    # Action keywords and their variations
    ACTION_PATTERNS = {
        "analyze": r"analyze|analyse|check|review|examine",
        "optimize": r"optimize|improve|enhance|speed up|fix",
        "create": r"create|make|generate|build|implement",
        "test": r"test|verify|validate|check",
    }
    
    # Focus area keywords
    FOCUS_PATTERNS = {
        "security": r"security|vulnerability|secure|auth|encryption",
        "performance": r"performance|speed|efficient|optimize|fast",
        "quality": r"quality|clean|maintainable|readable|style",
        "testing": r"test|coverage|unit test|integration",
    }

    def __init__(self):
        """Initialize the prompt processor."""
        # Compile regex patterns
        self.tech_regex = {
            tech: re.compile(pattern, re.IGNORECASE)
            for tech, pattern in self.TECH_PATTERNS.items()
        }
        self.action_regex = {
            action: re.compile(pattern, re.IGNORECASE)
            for action, pattern in self.ACTION_PATTERNS.items()
        }
        self.focus_regex = {
            focus: re.compile(pattern, re.IGNORECASE)
            for focus, pattern in self.FOCUS_PATTERNS.items()
        }

    def process(self, prompt: str) -> OperationResult[PromptIntent]:
        """
        Process a natural language prompt and extract structured intent.
        
        Args:
            prompt: Natural language prompt from user
            
        Returns:
            OperationResult containing PromptIntent or error
        """
        try:
            # Extract components
            action = self._extract_action(prompt)
            technologies = self._extract_technologies(prompt)
            focus_areas = self._extract_focus_areas(prompt)
            constraints = self._extract_constraints(prompt)
            context = self._extract_context(prompt)
            
            # Validate extracted information
            if not action:
                return OperationResult.error(
                    "Could not determine action from prompt",
                    error_type="IntentError",
                    details={"prompt": prompt}
                )
                
            if not technologies:
                return OperationResult.error(
                    "No technology keywords found in prompt",
                    error_type="IntentError",
                    details={"prompt": prompt}
                )
            
            # Create intent
            intent = PromptIntent(
                action=action,
                technologies=technologies,
                focus_areas=focus_areas,
                constraints=constraints,
                context=context
            )
            
            return OperationResult.success(
                intent,
                metadata={
                    "original_prompt": prompt,
                    "confidence_scores": self._calculate_confidence(prompt, intent)
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to process prompt: {e}")
            return OperationResult.error(
                str(e),
                error_type="ProcessingError",
                details={"prompt": prompt}
            )

    def _extract_action(self, prompt: str) -> Optional[str]:
        """Extract the primary action from the prompt."""
        for action, pattern in self.action_regex.items():
            if pattern.search(prompt):
                return action
        return None

    def _extract_technologies(self, prompt: str) -> List[str]:
        """Extract technology keywords from the prompt."""
        technologies = []
        for tech, pattern in self.tech_regex.items():
            if pattern.search(prompt):
                technologies.append(tech)
        return technologies

    def _extract_focus_areas(self, prompt: str) -> List[str]:
        """Extract focus areas from the prompt."""
        focus_areas = []
        for focus, pattern in self.focus_regex.items():
            if pattern.search(prompt):
                focus_areas.append(focus)
        return focus_areas

    def _extract_constraints(self, prompt: str) -> Dict[str, Any]:
        """Extract constraints from the prompt."""
        constraints = {}
        
        # Look for numeric constraints
        number_patterns = {
            "max_complexity": r"max(?:imum)?\s+complexity\s+(?:of\s+)?(\d+)",
            "min_coverage": r"min(?:imum)?\s+coverage\s+(?:of\s+)?(\d+)%?",
            "timeout": r"timeout\s+(?:of\s+)?(\d+)\s*(?:s|seconds)?",
        }
        
        for key, pattern in number_patterns.items():
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                constraints[key] = int(match.group(1))
                
        # Look for boolean constraints
        bool_patterns = {
            "strict_mode": r"strict\s+mode",
            "debug": r"debug\s+mode",
            "verbose": r"verbose",
        }
        
        for key, pattern in bool_patterns.items():
            if re.search(pattern, prompt, re.IGNORECASE):
                constraints[key] = True
                
        return constraints

    def _extract_context(self, prompt: str) -> Dict[str, Any]:
        """Extract additional context from the prompt."""
        context = {}
        
        # Extract file paths
        file_matches = re.finditer(r"(?:file|path):\s*([^\s,]+)", prompt)
        if file_matches:
            context["files"] = [m.group(1) for m in file_matches]
            
        # Extract code snippets
        code_matches = re.finditer(r"```(\w+)?\n(.*?)```", prompt, re.DOTALL)
        if code_matches:
            context["code_snippets"] = [
                {
                    "language": m.group(1) or "text",
                    "code": m.group(2).strip()
                }
                for m in code_matches
            ]
            
        # Extract URLs
        urls = re.finditer(r"https?://\S+", prompt)
        if urls:
            context["urls"] = [u.group(0) for u in urls]
            
        return context

    def _calculate_confidence(
        self,
        prompt: str,
        intent: PromptIntent
    ) -> Dict[str, float]:
        """Calculate confidence scores for extracted information."""
        scores = {}
        
        # Action confidence
        action_matches = sum(
            1 for pattern in self.action_regex.values()
            if pattern.search(prompt)
        )
        scores["action"] = min(1.0, action_matches / len(self.action_regex))
        
        # Technology confidence
        tech_matches = sum(
            1 for pattern in self.tech_regex.values()
            if pattern.search(prompt)
        )
        scores["technologies"] = min(1.0, tech_matches / len(self.tech_regex))
        
        # Focus areas confidence
        focus_matches = sum(
            1 for pattern in self.focus_regex.values()
            if pattern.search(prompt)
        )
        scores["focus_areas"] = min(1.0, focus_matches / len(self.focus_regex))
        
        # Overall confidence
        scores["overall"] = (
            scores["action"] * 0.4 +
            scores["technologies"] * 0.4 +
            scores["focus_areas"] * 0.2
        )
        
        return scores
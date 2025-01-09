"""
Technology stack analysis and framework detection.
"""

from typing import Dict, Any, List, Optional
import re
from pathlib import Path
import logging

from ..utils.result import OperationResult

logger = logging.getLogger(__name__)

class TechStackAnalyzer:
    """Analyzes technology stacks and frameworks in code."""

    TECH_PATTERNS = {
        "python": {
            "files": [r"\.py$", r"requirements\.txt$", r"setup\.py$", r"pyproject\.toml$"],
            "frameworks": {
                "django": ["django", "DJANGO_SETTINGS", "urls.py"],
                "flask": ["flask", "Flask(__name__)", "@app.route"],
                "fastapi": ["fastapi", "FastAPI()", "@app.get"],
                "pytorch": ["torch", "nn.Module", "optim."],
                "tensorflow": ["tensorflow", "tf.", "keras"]
            }
        },
        "javascript": {
            "files": [r"\.js$", r"\.jsx$", r"package\.json$"],
            "frameworks": {
                "react": ["react", "useState", "useEffect", "jsx"],
                "vue": ["vue", "createApp", "defineComponent"],
                "angular": ["@angular", "ngModule", "Component"],
                "express": ["express", "app.listen", "router.get"]
            }
        },
        "typescript": {
            "files": [r"\.ts$", r"\.tsx$", r"tsconfig\.json$"],
            "frameworks": {
                "nestjs": ["@nestjs", "Injectable", "Controller"],
                "nextjs": ["next", "getStaticProps", "getServerSideProps"],
                "typeorm": ["typeorm", "Entity", "Repository"]
            }
        }
    }

    def analyze_directory(
        self,
        path: Path,
        max_files: int = 1000
    ) -> OperationResult[Dict[str, Any]]:
        """
        Analyze a directory for technology stack information.
        
        Args:
            path: Directory path to analyze
            max_files: Maximum number of files to analyze
            
        Returns:
            OperationResult containing:
                - technologies: Dict of detected technologies and confidence scores
                - frameworks: Dict of detected frameworks per technology
                - recommendations: List of technology-specific recommendations
        """
        try:
            # Collect files
            files = list(path.rglob("*"))[:max_files]
            
            # Detect technologies
            tech_scores = self._detect_technologies(files)
            
            # Analyze frameworks for each detected technology
            frameworks = {}
            for tech, score in tech_scores.items():
                if score > 0.1:  # Only analyze significant technologies
                    frameworks[tech] = self._detect_frameworks(
                        tech,
                        files
                    )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                tech_scores,
                frameworks
            )
            
            return OperationResult.success({
                "technologies": tech_scores,
                "frameworks": frameworks,
                "recommendations": recommendations,
                "files_analyzed": len(files)
            })
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return OperationResult.error(
                str(e),
                error_type="AnalysisError",
                details={"path": str(path)}
            )

    def _detect_technologies(
        self,
        files: List[Path]
    ) -> Dict[str, float]:
        """
        Detect technologies and their confidence scores.
        
        Returns:
            Dict mapping technology to confidence score (0-1)
        """
        scores = {}
        total_matches = 0
        
        # Count file pattern matches
        for file in files:
            file_str = str(file)
            for tech, patterns in self.TECH_PATTERNS.items():
                for pattern in patterns["files"]:
                    if re.search(pattern, file_str, re.IGNORECASE):
                        scores[tech] = scores.get(tech, 0) + 1
                        total_matches += 1
        
        # Normalize scores
        if total_matches > 0:
            return {k: v/total_matches for k, v in scores.items()}
        return {}

    def _detect_frameworks(
        self,
        tech: str,
        files: List[Path]
    ) -> Dict[str, float]:
        """
        Detect frameworks for a specific technology.
        
        Returns:
            Dict mapping framework to confidence score (0-1)
        """
        if tech not in self.TECH_PATTERNS:
            return {}
            
        framework_scores = {}
        total_matches = 0
        
        # Check each file for framework patterns
        for file in files:
            if not any(re.search(p, str(file)) for p in self.TECH_PATTERNS[tech]["files"]):
                continue
                
            try:
                content = file.read_text()
                for fw, patterns in self.TECH_PATTERNS[tech]["frameworks"].items():
                    for pattern in patterns:
                        if pattern in content:
                            framework_scores[fw] = framework_scores.get(fw, 0) + 1
                            total_matches += 1
            except Exception as e:
                logger.warning(f"Could not read {file}: {e}")
        
        # Normalize scores
        if total_matches > 0:
            return {k: v/total_matches for k, v in framework_scores.items()}
        return {}

    def _generate_recommendations(
        self,
        tech_scores: Dict[str, float],
        frameworks: Dict[str, Dict[str, float]]
    ) -> List[Dict[str, Any]]:
        """Generate technology-specific recommendations."""
        recommendations = []
        
        # Add recommendations based on technology mix
        if "python" in tech_scores and "javascript" in tech_scores:
            recommendations.append({
                "type": "stack",
                "message": "Consider using TypeScript for better type safety in your JavaScript code"
            })
            
        # Framework-specific recommendations
        for tech, fw_scores in frameworks.items():
            if tech == "python":
                if "django" in fw_scores and fw_scores["django"] > 0.7:
                    recommendations.append({
                        "type": "framework",
                        "message": "High Django usage detected. Consider using Django REST framework for APIs"
                    })
                    
            elif tech == "javascript":
                if "react" in fw_scores and "typescript" not in tech_scores:
                    recommendations.append({
                        "type": "framework",
                        "message": "React detected without TypeScript. Consider adding TypeScript for better maintainability"
                    })
        
        return recommendations
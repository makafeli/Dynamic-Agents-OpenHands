# Extension System Guide

The OpenHands Dynamic Agents extension system allows you to add custom functionality to agents through a modular approach.

## Overview

Extensions provide specialized analysis, optimization, or monitoring capabilities to dynamic agents. Each extension follows a standard protocol and can be easily added to any agent.

## Creating Extensions

### Basic Extension

```python
from typing import Dict, Any, Protocol
from dataclasses import dataclass

class Extension(Protocol):
    """Base protocol for all extensions."""
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data and return results."""
        ...
        
    async def optimize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize data based on analysis."""
        ...

@dataclass
class ExtensionMetadata:
    """Metadata for extensions."""
    name: str
    version: str
    capabilities: List[str]
    requirements: List[str]
```

### Example Extensions

#### Security Extension

```python
class SecurityExtension:
    """Security analysis extension."""
    
    def __init__(self):
        self.metadata = ExtensionMetadata(
            name="security",
            version="1.0.0",
            capabilities=["vulnerability_scan", "security_score"],
            requirements=["bandit", "safety"]
        )
        
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform security analysis."""
        vulnerabilities = await self._scan_vulnerabilities(data)
        score = self._calculate_security_score(vulnerabilities)
        
        return {
            "vulnerabilities": vulnerabilities,
            "security_score": score,
            "recommendations": self._generate_recommendations(vulnerabilities)
        }
        
    async def optimize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply security optimizations."""
        fixes = await self._apply_security_fixes(data)
        return {
            "optimized_code": fixes["code"],
            "applied_fixes": fixes["changes"]
        }
```

#### Performance Extension

```python
class PerformanceExtension:
    """Performance analysis extension."""
    
    def __init__(self):
        self.metadata = ExtensionMetadata(
            name="performance",
            version="1.0.0",
            capabilities=["profiling", "optimization"],
            requirements=["cProfile", "line_profiler"]
        )
        
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance."""
        profile = await self._profile_code(data)
        bottlenecks = self._identify_bottlenecks(profile)
        
        return {
            "profile": profile,
            "bottlenecks": bottlenecks,
            "recommendations": self._generate_recommendations(bottlenecks)
        }
        
    async def optimize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize performance."""
        optimizations = await self._apply_optimizations(data)
        return {
            "optimized_code": optimizations["code"],
            "improvements": optimizations["metrics"]
        }
```

## Using Extensions

### Adding Extensions to Agents

```python
from openhands_dynamic_agents import DynamicAgent
from openhands_dynamic_agents.extensions import SecurityExtension, PerformanceExtension

# Create agent with extensions
agent = DynamicAgent("enhanced_agent")
agent.add_extension(SecurityExtension())
agent.add_extension(PerformanceExtension())

# Use agent with extensions
result = await agent.process_prompt(
    "Analyze this Python code for security issues and optimize performance"
)
```

### Custom Extension Example

```python
class CodeQualityExtension:
    """Code quality analysis extension."""
    
    def __init__(self):
        self.metadata = ExtensionMetadata(
            name="code_quality",
            version="1.0.0",
            capabilities=["style_check", "complexity_analysis"],
            requirements=["pylint", "radon"]
        )
        
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code quality."""
        style_issues = await self._check_style(data)
        complexity = self._analyze_complexity(data)
        
        return {
            "style_issues": style_issues,
            "complexity": complexity,
            "quality_score": self._calculate_quality_score(style_issues, complexity)
        }
        
    async def optimize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Improve code quality."""
        improved_code = await self._apply_style_fixes(data)
        refactored_code = self._refactor_complex_code(improved_code)
        
        return {
            "optimized_code": refactored_code,
            "style_fixes": self._get_applied_fixes(),
            "complexity_reduction": self._get_complexity_diff()
        }

# Use custom extension
agent = DynamicAgent("quality_agent")
agent.add_extension(CodeQualityExtension())
```

## Extension Development Guidelines

### Best Practices

1. **Error Handling**
   ```python
   async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
       try:
           result = await self._perform_analysis(data)
           return result
       except Exception as e:
           logger.error(f"Analysis failed: {e}")
           return {
               "error": str(e),
               "status": "failed",
               "partial_results": self._get_partial_results()
           }
   ```

2. **Progress Reporting**
   ```python
   async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
       progress = Progress()
       
       # Report progress
       progress.update("Starting analysis", 0)
       result = await self._analyze_step1(data)
       progress.update("Step 1 complete", 33)
       
       # More steps...
       progress.update("Analysis complete", 100)
       return result
   ```

3. **Resource Management**
   ```python
   class ResourceIntensiveExtension:
       def __init__(self):
           self.pool = None
           
       async def __aenter__(self):
           self.pool = await create_resource_pool()
           return self
           
       async def __aexit__(self, exc_type, exc, tb):
           await self.pool.cleanup()
   ```

### Testing Extensions

```python
import pytest
from openhands_dynamic_agents.testing import ExtensionTestCase

class TestSecurityExtension(ExtensionTestCase):
    def setUp(self):
        self.extension = SecurityExtension()
        
    async def test_vulnerability_detection(self):
        code = """
        @app.route('/user/<id>')
        def get_user(id):
            query = f"SELECT * FROM users WHERE id = {id}"
            return db.execute(query)
        """
        
        result = await self.extension.analyze({"code": code})
        self.assertIn("sql_injection", result["vulnerabilities"])
        
    async def test_security_score(self):
        result = await self.extension.analyze(self.sample_secure_code)
        self.assertGreaterEqual(result["security_score"], 0.8)
```

## Configuration

### Extension Configuration

```yaml
# extensions.yaml
extensions:
  security:
    enabled: true
    config:
      vulnerability_threshold: high
      scan_dependencies: true
      
  performance:
    enabled: true
    config:
      profile_memory: true
      optimization_level: aggressive
      
  code_quality:
    enabled: true
    config:
      style_guide: google
      max_complexity: 10
```

### Loading Configuration

```python
from openhands_dynamic_agents.config import load_extension_config

config = load_extension_config("extensions.yaml")
extension = SecurityExtension(config["security"])
```

## Advanced Topics

### Extension Dependencies

```python
@dataclass
class ExtensionDependency:
    extension_type: str
    version_range: str
    optional: bool = False

class AdvancedExtension:
    dependencies = [
        ExtensionDependency("security", ">=1.0.0"),
        ExtensionDependency("performance", ">=1.0.0", optional=True)
    ]
```

### Extension Events

```python
from openhands_dynamic_agents.events import ExtensionEvent

class MonitoringExtension:
    def __init__(self):
        self.events = []
        
    async def on_analysis_start(self, event: ExtensionEvent):
        self.events.append(event)
        
    async def on_analysis_complete(self, event: ExtensionEvent):
        self.events.append(event)
        await self._update_metrics(event)
```

### Extension Registry

```python
from openhands_dynamic_agents.registry import ExtensionRegistry

registry = ExtensionRegistry()
registry.register("security", SecurityExtension)
registry.register("performance", PerformanceExtension)

# Get extension by name
extension_class = registry.get("security")
extension = extension_class()
```

## Troubleshooting

Common issues and solutions:

1. **Extension Conflicts**
   - Check dependency versions
   - Verify extension compatibility
   - Review configuration conflicts

2. **Performance Issues**
   - Profile extension operations
   - Check resource usage
   - Consider async optimizations

3. **Integration Problems**
   - Verify interface compliance
   - Check event handling
   - Review error handling
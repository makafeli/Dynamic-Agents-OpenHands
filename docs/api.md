# OpenHands Dynamic Agents API Reference

## Core Components

### DynamicAgent

The main class for dynamic agent functionality.

```python
from openhands_dynamic_agents import DynamicAgent

agent = DynamicAgent(
    name="custom_agent",
    extensions=["security", "performance"]
)
```

#### Methods

- `process_prompt(prompt: str) -> Dict[str, Any]`
  Process natural language prompt and execute analysis.

- `analyze_with_viz(code: str, focus: List[str]) -> Dict[str, Any]`
  Analyze code with visualization support.

- `add_extension(extension: Extension) -> None`
  Add custom extension to the agent.

### PromptProcessor

Natural language processing for dynamic agents.

```python
from openhands_dynamic_agents.core.prompt_processor import PromptProcessor

processor = PromptProcessor()
result = processor.process("Analyze this Python code for security issues")
```

#### Methods

- `process(prompt: str) -> OperationResult[PromptIntent]`
  Process natural language prompt into structured intent.

### Dashboard

Interactive visualization dashboard.

```python
from openhands_dynamic_agents.dashboard import Dashboard

dashboard = Dashboard(port=8080)
dashboard.start()
```

#### Methods

- `start() -> None`
  Start the dashboard server.

- `update_data(data: Dict[str, Any]) -> None`
  Update dashboard with new data.

- `add_visualization(name: str, viz: Dict[str, Any]) -> None`
  Add custom visualization.

### DashboardVisualizer

Create visualizations for the dashboard.

```python
from openhands_dynamic_agents.dashboard import DashboardVisualizer

visualizer = DashboardVisualizer(theme="dark")
viz = visualizer.create_tech_stack_visualization(results)
```

#### Methods

- `create_tech_stack_visualization(data: Dict[str, Any]) -> Dict[str, Any]`
  Create technology stack visualization.

- `create_metrics_visualization(metrics: Dict[str, Any]) -> Dict[str, Any]`
  Create metrics visualization.

- `create_analysis_dashboard(results: Dict[str, Any]) -> Dict[str, Any]`
  Create comprehensive analysis dashboard.

## Extension System

### Base Extension

```python
from openhands_dynamic_agents.extensions import Extension
from typing import Dict, Any

class CustomExtension(Extension):
    """Custom analysis extension."""
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement analysis logic
        return {
            "results": self._analyze(data),
            "score": self._calculate_score(data)
        }
    
    async def optimize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement optimization logic
        return {
            "optimized": self._optimize(data),
            "improvements": self._get_improvements(data)
        }
```

### Built-in Extensions

#### SecurityExtension

```python
from openhands_dynamic_agents.extensions.security import SecurityExtension

extension = SecurityExtension()
result = await extension.analyze(data)
```

#### PerformanceExtension

```python
from openhands_dynamic_agents.extensions.performance import PerformanceExtension

extension = PerformanceExtension()
result = await extension.analyze(data)
```

## Data Types

### PromptIntent

```python
@dataclass
class PromptIntent:
    action: str  # e.g., "analyze", "optimize"
    technologies: List[str]  # e.g., ["python", "django"]
    focus_areas: List[str]  # e.g., ["security", "performance"]
    constraints: Dict[str, Any]
    context: Dict[str, Any]
```

### OperationResult

```python
@dataclass
class OperationResult(Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[OperationError] = None
    metadata: Optional[Dict[str, Any]] = None
```

## Examples

### Basic Usage

```python
from openhands_dynamic_agents import DynamicAgent
from openhands_dynamic_agents.core.prompt_processor import PromptProcessor

# Initialize
processor = PromptProcessor()
agent = DynamicAgent("smart_agent")

# Process prompt
result = processor.process(
    "Analyze this Python Django code for security vulnerabilities"
)

if result.success:
    # Execute analysis
    analysis = await agent.process_prompt(result.data)
    print(analysis)
```

### Advanced Usage

```python
# Custom extension
class SecurityExtension(Extension):
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "vulnerabilities": self._scan_vulnerabilities(data),
            "security_score": self._calculate_score(data)
        }

# Use extension
agent = DynamicAgent("security_agent")
agent.add_extension(SecurityExtension())

# Dashboard with custom visualization
dashboard = Dashboard()
visualizer = DashboardVisualizer()

viz = visualizer.create_tech_stack_visualization(results)
dashboard.add_visualization("tech_stack", viz)
dashboard.start()
```

### Error Handling

```python
from openhands_dynamic_agents.utils.result import OperationResult

def process_data(data: Dict[str, Any]) -> OperationResult[Dict[str, Any]]:
    try:
        result = analyze_data(data)
        return OperationResult.success(result)
    except Exception as e:
        return OperationResult.error(
            str(e),
            error_type="ProcessingError",
            details={"data": data}
        )
```

## Best Practices

1. **Error Handling**
   - Always check `OperationResult.success`
   - Handle errors gracefully
   - Provide meaningful error messages

2. **Extension Development**
   - Inherit from `Extension` base class
   - Implement required methods
   - Follow type hints
   - Add proper documentation

3. **Dashboard Usage**
   - Use appropriate visualization types
   - Update data periodically
   - Handle real-time updates properly

4. **Performance**
   - Cache results when possible
   - Use async methods for I/O operations
   - Batch process large datasets

## Contributing

1. Follow type hints
2. Add tests for new features
3. Update documentation
4. Follow code style guidelines
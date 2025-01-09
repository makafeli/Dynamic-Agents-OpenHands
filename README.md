# Dynamic Agents for OpenHands

A powerful extension for OpenHands that enables dynamic agent generation and intelligent code analysis through natural language processing.

## Overview

This module provides a flexible system for generating specialized agents at runtime, allowing OpenHands to adapt to different technologies and requirements through natural language prompts.

## Features

### Core Capabilities

- **Natural Language Processing**
  - Process free-form prompts
  - Intelligent intent detection
  - Context-aware analysis
  - Multi-technology support

- **Dynamic Agent Generation**
  - Template-based generation
  - LLM-powered customization
  - Automatic capability detection
  - Extension system

- **Advanced Analysis**
  - Technology stack detection
  - Framework identification
  - Security vulnerability scanning
  - Performance optimization
  - Code quality assessment

- **Interactive Visualization**
  - Technology stack visualization
  - Performance metrics
  - Dependency graphs
  - Real-time monitoring

### Integration

- Seamless OpenHands integration
- Template-based generation
- Extension system
- Real-time monitoring
- Custom dashboards

## Installation

```bash
pip install openhands-dynamic-agents
```

## Quick Start

### Natural Language Processing

```python
from openhands_dynamic_agents import DynamicAgent
from openhands_dynamic_agents.core.prompt_processor import PromptProcessor

# Initialize
processor = PromptProcessor()
agent = DynamicAgent("smart_agent")

# Process natural language prompt
result = processor.process(
    "Analyze this Python Django code for security vulnerabilities "
    "and optimize database queries"
)

if result.success:
    intent = result.data
    print(f"Action: {intent.action}")
    print(f"Technologies: {intent.technologies}")
    print(f"Focus Areas: {intent.focus_areas}")
```

### Interactive Analysis

```python
from openhands_dynamic_agents.dashboard import Dashboard

# Start dashboard
dashboard = Dashboard(port=8080)
dashboard.start()

# Process analysis with visualization
result = agent.analyze_with_viz(
    code="your_code_here",
    focus=["security", "performance"]
)

# Update dashboard
dashboard.update_data(result)
```

### CLI Usage

```bash
# Process natural language prompt
agents process "Analyze this Python code for security issues"

# Analyze repository with visualization
agents analyze repo . --visualize --output analysis.html

# Start interactive dashboard
agents dashboard --port 8080 --theme dark

# Watch repository for changes
agents watch /path/to/repo --focus "security,performance"
```

## Advanced Usage

### Custom Extensions

```python
from openhands_dynamic_agents.extensions import Extension

class SecurityExtension(Extension):
    """Custom security analysis extension."""
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement security analysis
        return {
            "vulnerabilities": self._scan_vulnerabilities(data),
            "security_score": self._calculate_score(data)
        }

# Use extension
agent = DynamicAgent("security_agent")
agent.add_extension(SecurityExtension())
```

### Visualization Customization

```python
from openhands_dynamic_agents.dashboard import DashboardVisualizer

# Create custom visualization
visualizer = DashboardVisualizer(theme="dark")
tech_viz = visualizer.create_tech_stack_visualization(results)
dashboard.add_visualization("tech_stack", tech_viz)
```

### Advanced Analysis

```python
# Comprehensive analysis
result = await agent.process_prompt("""
    Analyze the Python code in /path/to/repo:
    - Check for security vulnerabilities
    - Optimize performance
    - Ensure code quality
    - Suggest improvements
    Focus on Django best practices
""")

# Access results
security = result["analysis"]["security"]
performance = result["analysis"]["performance"]
quality = result["analysis"]["quality"]

# Get recommendations
for rec in result["recommendations"]:
    print(f"- {rec}")
```

## Configuration

### Environment Variables

- `OPENHANDS_DATA_DIR`: Base directory for data storage
- `OPENHANDS_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `OPENHANDS_DASHBOARD_HOST`: Default dashboard host
- `OPENHANDS_DASHBOARD_PORT`: Default dashboard port

### Configuration File

Create `~/.config/openhands/config.yaml`:

```yaml
data_dir: /path/to/data
log_level: INFO
dashboard:
  host: localhost
  port: 8000
analysis:
  max_files: 1000
  ignore_patterns:
    - "node_modules/"
    - "venv/"
```

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run tests:
   ```bash
   poetry run pytest
   ```

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Documentation

- [CLI Reference](docs/cli.md)
- [API Documentation](docs/api.md)
- [Extension System](docs/extensions.md)
- [Visualization Guide](docs/visualization.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.
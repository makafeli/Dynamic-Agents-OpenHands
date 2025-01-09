# Dynamic Agents for OpenHands

A modular extension for OpenHands that enables dynamic agent generation based on technology keywords.

## Overview

This module provides a flexible system for generating specialized agents at runtime, allowing OpenHands to adapt to different technologies and requirements without requiring a fork of the main repository.

## Features

- Dynamic agent generation using LLM
- Technology keyword management
- Template-based agent generation
- Seamless integration with OpenHands runtime
- Performance monitoring and error handling
- Extensible template system

## Installation

```bash
pip install openhands-dynamic-agents
```

## Usage

```python
from openhands_dynamic_agents import DynamicAgent

# Create a dynamic agent for Python analysis
agent = DynamicAgent(
    name="python_analyzer",
    keyword="python",
    options={
        "analysis_type": "security",
        "max_code_length": 5000
    }
)

# Run the agent
result = agent.run({
    "code_snippet": "def hello(): print('world')",
    "analysis_type": "security"
})
```

## Integration with OpenHands

The module integrates seamlessly with OpenHands by extending its microagent system:

1. Dynamic agents inherit from `BaseMicroAgent`
2. Agents are generated with proper metadata and type information
3. Generated agents follow OpenHands conventions and patterns

## Architecture

### Core Components

1. **DynamicAgent**: Main class that integrates with OpenHands' microagent system
   - Handles agent lifecycle
   - Manages generation and execution
   - Provides error handling and validation

2. **LLMAgentFactory**: Generates agent implementations using LLM
   - Template-based generation
   - Code validation
   - Dynamic loading

3. **KeywordManager**: Manages technology keywords
   - Keyword validation
   - State management
   - Agent tracking

### Utils

1. **Result Types**: Generic result handling
   - Operation results
   - Error information
   - Metadata tracking

2. **Monitoring**: Performance tracking
   - Operation timing
   - Success/failure logging
   - Detailed metrics

3. **Validation**: Input validation
   - Schema validation
   - Type checking
   - Custom rules

### Templates

- Predefined templates for common technologies
- Customizable template system
- Version management

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

Contributions are welcome! Please see our contributing guidelines for more details.

## License

MIT License - see LICENSE file for details.
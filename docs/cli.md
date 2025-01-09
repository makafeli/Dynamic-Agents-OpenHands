# OpenHands Dynamic Agents CLI Reference

The OpenHands Dynamic Agents CLI provides a powerful command-line interface for working with dynamic agents, analyzing code, and managing the system.

## Global Options

```bash
agents --help     # Show help message
agents --version  # Show version information
```

## Command Groups

### Process Commands

Process natural language prompts and code analysis.

```bash
# Process natural language prompt
agents process "Analyze this Python code for security issues"

# Process with specific focus
agents process "Check performance of this React component" --focus performance

# Process with context
agents process "Review this API endpoint" --context "This is a Django REST API"

# Process with output format
agents process "Analyze code quality" --format json --output analysis.json
```

### Analysis Commands

Analyze repositories and code files.

```bash
# Basic repository analysis
agents analyze repo /path/to/repo

# Analysis with specific focus
agents analyze repo . --focus security,performance

# Analysis with visualization
agents analyze repo . --visualize --output analysis.html

# Analyze specific file
agents analyze file src/main.py --tech python

# Batch analysis
agents analyze batch repos.txt --output-dir ./reports

# Watch mode
agents analyze watch /path/to/repo --alert-threshold high
```

### Dashboard Commands

Manage the interactive dashboard.

```bash
# Start dashboard
agents dashboard

# Configure dashboard
agents dashboard --port 8080 --host 0.0.0.0

# Start with theme
agents dashboard --theme dark

# Start in development mode
agents dashboard --dev

# Start with custom data directory
agents dashboard --data-dir /path/to/data
```

### Agent Management

Create and manage dynamic agents.

```bash
# Create agent with prompt
agents create security_agent --prompt "Create an agent for Django security analysis"

# Create with template
agents create custom_agent --template security.yaml

# List agents
agents list

# List by status
agents list --status active

# List by technology
agents list --tech python
```

## Advanced Usage

### Pipeline Integration

```bash
# Run as part of CI pipeline
agents analyze repo . --ci --fail-on severity=high

# Generate CI-friendly reports
agents analyze repo . --format json --output report.json --ci-mode
```

### Batch Processing

```bash
# Create batch file (repos.txt):
/path/to/repo1
/path/to/repo2
https://github.com/user/repo3

# Run batch analysis
agents analyze batch repos.txt --output-dir ./reports
```

### Custom Templates

```bash
# List available templates
agents templates list

# Create new template
agents templates create my_template.yaml

# Use custom template
agents create custom_agent --template my_template.yaml
```

## Configuration

### Environment Variables

The CLI respects the following environment variables:

```bash
# Base configuration
export OPENHANDS_DATA_DIR=/path/to/data
export OPENHANDS_LOG_LEVEL=INFO

# Dashboard configuration
export OPENHANDS_DASHBOARD_HOST=localhost
export OPENHANDS_DASHBOARD_PORT=8000

# Analysis configuration
export OPENHANDS_MAX_FILES=1000
export OPENHANDS_IGNORE_PATTERNS="node_modules/,venv/"
```

### Configuration File

Create `~/.config/openhands/config.yaml`:

```yaml
# General settings
data_dir: /path/to/data
log_level: INFO

# Dashboard settings
dashboard:
  host: localhost
  port: 8000
  theme: light
  auto_refresh: true

# Analysis settings
analysis:
  max_files: 1000
  ignore_patterns:
    - "node_modules/"
    - "venv/"
    - "__pycache__/"
  alert_threshold: medium
  cache_results: true

# Extension settings
extensions:
  enabled:
    - security
    - performance
    - quality
  custom_path: /path/to/custom/extensions
```

## Output Formats

The CLI supports multiple output formats:

- `text`: Human-readable text output (default)
- `json`: JSON format for machine processing
- `yaml`: YAML format
- `html`: Interactive HTML report with visualizations

Example:
```bash
# Generate JSON output
agents analyze repo . --format json --output analysis.json

# Generate HTML report
agents analyze repo . --format html --output report.html
```

## Error Handling

The CLI provides detailed error messages and exit codes:

- 0: Success
- 1: General error
- 2: Configuration error
- 3: Analysis error
- 4: Network error

Example error handling in scripts:
```bash
agents analyze repo . || {
    case $? in
        2) echo "Configuration error";;
        3) echo "Analysis failed";;
        *) echo "Unknown error";;
    esac
}
```

## Tips and Tricks

1. Use `--quiet` for script-friendly output
2. Use `--verbose` for debugging
3. Use `--format json` for machine-readable output
4. Use `--watch` with the dashboard for real-time updates
5. Use `--cache` to speed up repeated analyses

## Examples

### Basic Analysis

```bash
# Quick security check
agents process "Check this Python code for security issues" --quick

# Detailed analysis
agents analyze repo . --focus security,performance --verbose
```

### Advanced Analysis

```bash
# Complex analysis with context
agents process "Optimize this Django view" \
    --context "This is a high-traffic API endpoint" \
    --focus performance \
    --threshold high

# Repository analysis with custom rules
agents analyze repo . \
    --rules custom_rules.yaml \
    --ignore "tests/,docs/" \
    --format html \
    --output report.html
```

### Dashboard Operations

```bash
# Start dashboard with custom settings
agents dashboard \
    --port 8080 \
    --theme dark \
    --data-dir /path/to/data \
    --auto-refresh

# Watch repository with alerts
agents watch /path/to/repo \
    --focus "security,performance" \
    --alert-threshold high \
    --notify slack
```

## Contributing

To add new CLI commands:

1. Add your command to `cli.py`
2. Add tests in `tests/test_cli.py`
3. Update this documentation
4. Submit a pull request

## Troubleshooting

Common issues and solutions:

1. **Command not found**: Ensure the package is installed in your active Python environment
2. **Permission denied**: Check file permissions and data directory access
3. **Analysis fails**: Try with `--verbose` for detailed logs
4. **Dashboard won't start**: Check port availability and permissions
"""
Command-line interface for OpenHands Dynamic Agents.
"""

import sys
from pathlib import Path
import json
import click
from typing import Optional
import logging

from .analysis.tech_stack import TechStackAnalyzer
from .dashboard.app import Dashboard
from .core.dynamic_agent import DynamicAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@click.group()
@click.version_option()
def cli():
    """OpenHands Dynamic Agents CLI.
    
    This tool provides command-line access to OpenHands Dynamic Agents functionality
    with natural language processing and advanced analysis capabilities.
    
    \b
    Core Features:
    - Natural language prompt processing
    - Technology stack analysis
    - Dynamic agent generation
    - Interactive visualizations
    - Real-time monitoring
    
    Common usage examples:
    
    \b
    # Process natural language prompt
    $ agents process "Analyze this Python code for security issues and optimize performance"
    
    \b
    # Analyze repository with specific focus
    $ agents analyze repo /path/to/repo --focus security,performance
    
    \b
    # Analyze with visualization
    $ agents analyze repo . --visualize --output analysis.html
    
    \b
    # Analyze specific file with context
    $ agents analyze code src/main.py --context "This is a Django REST API endpoint"
    
    \b
    # Start interactive dashboard
    $ agents dashboard --port 8080 --theme dark
    
    \b
    # Create specialized agent
    $ agents create security_agent --prompt "Create an agent that focuses on Django security best practices"
    
    \b
    # Watch repository for changes
    $ agents watch /path/to/repo --focus "security,performance" --alert-threshold high
    
    For detailed documentation and examples:
    https://github.com/makafeli/Dynamic-Agents-OpenHands/blob/main/docs/cli.md
    """
    pass

@cli.group()
def analyze():
    """Analyze code and repositories.
    
    This command provides tools for analyzing code and repositories:
    
    \b
    - Repository analysis (technology stack, frameworks)
    - Single file analysis
    - Batch processing
    
    Examples:
    
    \b
    # Basic repository analysis
    $ agents analyze repo /path/to/repo
    
    \b
    # Save analysis as JSON
    $ agents analyze repo . -f json -o analysis.json
    
    \b
    # Analyze a Python file
    $ agents analyze code src/main.py
    
    \b
    # Analyze JavaScript with specific focus
    $ agents analyze code src/app.js --tech javascript --focus security
    """
    pass

@analyze.command("repo")
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Save analysis results to file"
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "yaml", "text"]),
    default="text",
    help="Output format"
)
def analyze_repo(path: str, output: Optional[str], format: str):
    """Analyze a repository for technology stack information."""
    try:
        analyzer = TechStackAnalyzer()
        result = analyzer.analyze_directory(Path(path))
        
        if not result.success:
            click.echo(f"Analysis failed: {result.error}", err=True)
            sys.exit(1)
            
        # Format output
        if format == "json":
            output_text = json.dumps(result.data, indent=2)
        elif format == "yaml":
            import yaml
            output_text = yaml.dump(result.data)
        else:
            # Text format
            output_text = "\nTechnology Stack Analysis\n"
            output_text += "=" * 50 + "\n\n"
            
            output_text += "Technologies:\n"
            for tech, score in result.data["technologies"].items():
                output_text += f"  - {tech}: {score:.2%}\n"
            
            output_text += "\nFrameworks:\n"
            for tech, frameworks in result.data["frameworks"].items():
                output_text += f"  {tech}:\n"
                for fw, score in frameworks.items():
                    output_text += f"    - {fw}: {score:.2%}\n"
            
            output_text += "\nRecommendations:\n"
            for rec in result.data["recommendations"]:
                output_text += f"  - {rec['message']}\n"
        
        # Output results
        if output:
            with open(output, "w") as f:
                f.write(output_text)
            click.echo(f"Results saved to {output}")
        else:
            click.echo(output_text)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@analyze.command("code")
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--tech",
    "-t",
    help="Technology to analyze (e.g., python, javascript)"
)
def analyze_code(file: str, tech: Optional[str]):
    """Analyze a code file using a dynamic agent."""
    try:
        # Read code file
        with open(file) as f:
            code = f.read()
            
        # Detect technology if not specified
        if not tech:
            analyzer = TechStackAnalyzer()
            result = analyzer.analyze_directory(Path(file).parent)
            if result.success and result.data["technologies"]:
                tech = max(
                    result.data["technologies"].items(),
                    key=lambda x: x[1]
                )[0]
            else:
                tech = "python"  # Default to Python
                
        # Create and run agent
        agent = DynamicAgent(
            name=f"{tech}_analyzer",
            keyword=tech,
            options={"analysis_type": "code_review"}
        )
        
        result = agent.run({
            "code_snippet": code,
            "file_path": file
        })
        
        if result["status"] == "error":
            click.echo(f"Analysis failed: {result['error']}", err=True)
            sys.exit(1)
            
        # Display results
        click.echo("\nCode Analysis Results\n" + "=" * 50 + "\n")
        for key, value in result["result"].items():
            click.echo(f"\n{key.title()}:")
            if isinstance(value, list):
                for item in value:
                    click.echo(f"  - {item}")
            else:
                click.echo(f"  {value}")
                
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option(
    "--host",
    default="localhost",
    help="Dashboard host"
)
@click.option(
    "--port",
    default=8000,
    help="Dashboard port"
)
def dashboard(host: str, port: int):
    """Launch the web dashboard.
    
    Start a web interface for monitoring and managing dynamic agents.
    The dashboard provides:
    
    \b
    - Technology stack visualization
    - Active agents monitoring
    - Analysis results viewing
    - Real-time updates
    
    Examples:
    
    \b
    # Start on default port (8000)
    $ agents dashboard
    
    \b
    # Start on specific port
    $ agents dashboard --port 8080
    
    \b
    # Allow external access
    $ agents dashboard --host 0.0.0.0
    
    \b
    # Start in development mode
    $ agents dashboard --dev
    """
    try:
        click.echo(f"Starting dashboard at http://{host}:{port}")
        dashboard = Dashboard(host=host, port=port)
        dashboard.start()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument("name")
@click.argument("keyword")
@click.option(
    "--options",
    "-o",
    type=click.Path(exists=True),
    help="JSON file with agent options"
)
def create(name: str, keyword: str, options: Optional[str]):
    """Create a new dynamic agent.
    
    Generate a new dynamic agent for specific technology analysis.
    Supports various technologies and customization options:
    
    \b
    Technologies:
    - python (Python code analysis)
    - javascript (JavaScript/Node.js analysis)
    - typescript (TypeScript analysis)
    - rust (Rust code analysis)
    - go (Go code analysis)
    
    Options can be provided via JSON file with structure:
    {
        "analysis_type": "security|performance|style",
        "max_code_length": 5000,
        "rules": ["rule1", "rule2"],
        "frameworks": ["django", "flask"]
    }
    
    Examples:
    
    \b
    # Create basic Python analyzer
    $ agents create python_analyzer python
    
    \b
    # Create security-focused agent
    $ agents create security_agent python --options security.json
    
    \b
    # Create TypeScript analyzer
    $ agents create ts_analyzer typescript
    
    \b
    # Create with inline options
    $ agents create web_agent javascript '{"frameworks": ["react"]}'
    """
    try:
        # Load options if provided
        agent_options = {}
        if options:
            with open(options) as f:
                agent_options = json.load(f)
                
        # Create agent
        agent = DynamicAgent(
            name=name,
            keyword=keyword,
            options=agent_options
        )
        
        # Generate agent implementation
        result = agent.generate()
        
        if not result.success:
            click.echo(f"Agent generation failed: {result.error}", err=True)
            sys.exit(1)
            
        click.echo(f"Successfully created agent: {name}")
        click.echo(f"Type: {keyword}")
        if agent_options:
            click.echo("\nOptions:")
            for key, value in agent_options.items():
                click.echo(f"  {key}: {value}")
                
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

def main():
    """Main entry point for the CLI."""
    cli()
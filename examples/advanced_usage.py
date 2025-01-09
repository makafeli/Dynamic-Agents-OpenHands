"""
Advanced usage examples for OpenHands Dynamic Agents.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any
from pprint import pprint

from openhands_dynamic_agents import (
    DynamicAgent,
    TechStackAnalyzer,
    Dashboard
)
from openhands_dynamic_agents.core.prompt_processor import PromptProcessor

async def analyze_with_prompt():
    """Example using natural language prompts."""
    # Initialize components
    processor = PromptProcessor()
    agent = DynamicAgent("smart_agent")
    
    # Process different types of prompts
    prompts = [
        # Security analysis
        """
        Analyze this Python Django code for security vulnerabilities:
        ```python
        @app.route('/user/<id>')
        def get_user(id):
            query = f"SELECT * FROM users WHERE id = {id}"
            return db.execute(query)
        ```
        """,
        
        # Performance optimization
        """
        Optimize this React component for performance, focusing on render efficiency:
        ```javascript
        function UserList({ users }) {
            const [filter, setFilter] = useState('')
            const filtered = users.filter(u => u.name.includes(filter))
            return (
                <div>
                    {filtered.map(user => (
                        <UserCard key={user.id} user={user} />
                    ))}
                </div>
            )
        }
        ```
        """,
        
        # Code quality and testing
        """
        Review this TypeScript code for quality and suggest tests:
        ```typescript
        class DataProcessor {
            process(data: any[]): any[] {
                return data.map(item => {
                    if (item.type === 'A') return this.processA(item)
                    if (item.type === 'B') return this.processB(item)
                    return item
                })
            }
        }
        ```
        """
    ]
    
    # Process each prompt
    for prompt in prompts:
        print("\nProcessing prompt:", prompt[:100], "...\n")
        
        # Analyze intent
        intent_result = processor.process(prompt)
        if not intent_result.success:
            print("Failed to process prompt:", intent_result.error)
            continue
            
        intent = intent_result.data
        print("Detected Intent:")
        print(f"- Action: {intent.action}")
        print(f"- Technologies: {intent.technologies}")
        print(f"- Focus Areas: {intent.focus_areas}")
        print(f"- Constraints: {intent.constraints}")
        
        # Execute analysis
        result = await agent.process_prompt(prompt)
        if result["status"] == "success":
            print("\nAnalysis Results:")
            pprint(result["analysis"])
            
            if "recommendations" in result:
                print("\nRecommendations:")
                for rec in result["recommendations"]:
                    print(f"- {rec}")
        else:
            print("Analysis failed:", result["error"])

async def analyze_repository():
    """Example analyzing a complete repository."""
    # Initialize analyzer
    analyzer = TechStackAnalyzer()
    
    # Analyze repository
    repo_path = Path("./example_repo")
    result = analyzer.analyze_directory(repo_path)
    
    if result.success:
        print("\nRepository Analysis:")
        print("\nTechnologies:")
        for tech, score in result.data["technologies"].items():
            print(f"- {tech}: {score:.1%}")
            
        print("\nFrameworks:")
        for tech, frameworks in result.data["frameworks"].items():
            print(f"\n{tech} frameworks:")
            for fw, score in frameworks.items():
                print(f"  - {fw}: {score:.1%}")
                
        print("\nRecommendations:")
        for rec in result.data["recommendations"]:
            print(f"- {rec}")
    else:
        print("Analysis failed:", result.error)

async def interactive_dashboard():
    """Example using the interactive dashboard."""
    # Initialize dashboard
    dashboard = Dashboard(
        host="localhost",
        port=8000
    )
    
    # Add some test data
    test_data = {
        "technologies": {
            "python": 0.65,
            "javascript": 0.35
        },
        "frameworks": {
            "python": {
                "django": 0.8,
                "flask": 0.2
            },
            "javascript": {
                "react": 0.9,
                "redux": 0.45
            }
        },
        "metrics": {
            "security_score": 0.85,
            "performance_score": 0.75,
            "quality_score": 0.90
        }
    }
    
    # Update dashboard with test data
    dashboard.update_data(test_data)
    
    # Start dashboard
    print("Starting dashboard at http://localhost:8000")
    await dashboard.start()

async def main():
    """Run all examples."""
    print("1. Prompt-based Analysis")
    print("----------------------")
    await analyze_with_prompt()
    
    print("\n2. Repository Analysis")
    print("--------------------")
    await analyze_repository()
    
    print("\n3. Interactive Dashboard")
    print("----------------------")
    await interactive_dashboard()

if __name__ == "__main__":
    asyncio.run(main())
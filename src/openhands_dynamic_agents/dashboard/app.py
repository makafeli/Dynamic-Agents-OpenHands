"""
Simple web dashboard for monitoring dynamic agents.
"""

from typing import Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from ..analysis.tech_stack import TechStackAnalyzer
from ..core.dynamic_agent import DynamicAgent

logger = logging.getLogger(__name__)

class Dashboard:
    """Simple web dashboard for dynamic agents."""
    
    def __init__(
        self,
        data_dir: Optional[Path] = None,
        host: str = "localhost",
        port: int = 8000
    ):
        """Initialize dashboard."""
        self.data_dir = data_dir or Path("/tmp/dynamic_agents/dashboard")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.host = host
        self.port = port
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title="Dynamic Agents Dashboard",
            description="Monitor and manage dynamic agents"
        )
        self._setup_routes()
        
        # Initialize analyzers
        self.tech_analyzer = TechStackAnalyzer()
        
    def _setup_routes(self) -> None:
        """Set up dashboard routes."""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home():
            """Render dashboard home page."""
            return """
            <html>
                <head>
                    <title>Dynamic Agents Dashboard</title>
                    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
                </head>
                <body class="bg-gray-100">
                    <div class="container mx-auto px-4 py-8">
                        <h1 class="text-3xl font-bold mb-8">Dynamic Agents Dashboard</h1>
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <!-- Analysis Section -->
                            <div class="bg-white rounded-lg shadow p-6">
                                <h2 class="text-xl font-semibold mb-4">Technology Analysis</h2>
                                <form id="analysisForm" class="space-y-4">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700">Repository Path</label>
                                        <input type="text" id="repoPath" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                                    </div>
                                    <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                                        Analyze
                                    </button>
                                </form>
                                <div id="analysisResult" class="mt-4"></div>
                            </div>
                            
                            <!-- Agents Section -->
                            <div class="bg-white rounded-lg shadow p-6">
                                <h2 class="text-xl font-semibold mb-4">Active Agents</h2>
                                <div id="agentsList" class="space-y-2"></div>
                            </div>
                        </div>
                    </div>
                    
                    <script>
                        // Add dashboard JavaScript here
                        document.getElementById('analysisForm').onsubmit = async (e) => {
                            e.preventDefault();
                            const path = document.getElementById('repoPath').value;
                            const result = await fetch(`/api/analyze?path=${encodeURIComponent(path)}`);
                            const data = await result.json();
                            document.getElementById('analysisResult').innerHTML = 
                                `<pre class="mt-4 p-4 bg-gray-100 rounded">${JSON.stringify(data, null, 2)}</pre>`;
                        };
                        
                        // Update agents list periodically
                        setInterval(async () => {
                            const result = await fetch('/api/agents');
                            const data = await result.json();
                            document.getElementById('agentsList').innerHTML = 
                                data.agents.map(agent => 
                                    `<div class="p-2 border rounded">
                                        <div class="font-semibold">${agent.name}</div>
                                        <div class="text-sm text-gray-600">${agent.status}</div>
                                    </div>`
                                ).join('');
                        }, 5000);
                    </script>
                </body>
            </html>
            """
            
        @self.app.get("/api/analyze")
        async def analyze_repo(path: str):
            """Analyze a repository."""
            try:
                result = self.tech_analyzer.analyze_directory(Path(path))
                if result.success:
                    return result.data
                raise HTTPException(status_code=400, detail=str(result.error))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
                
        @self.app.get("/api/agents")
        async def list_agents():
            """List active agents."""
            try:
                agents = self._load_agents()
                return {"agents": agents}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    def _load_agents(self) -> list:
        """Load active agents information."""
        agents_file = self.data_dir / "agents.json"
        if not agents_file.exists():
            return []
            
        try:
            with open(agents_file) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load agents: {e}")
            return []
            
    def start(self) -> None:
        """Start the dashboard server."""
        import uvicorn
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port
        )
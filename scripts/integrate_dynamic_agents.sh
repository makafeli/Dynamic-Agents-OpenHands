#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${YELLOW}[STATUS]${NC} $1"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Function to print error messages
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check command success
check_success() {
    if [ $? -eq 0 ]; then
        print_success "$1"
    else
        print_error "$2"
        exit 1
    fi
}

# Install system dependencies
print_status "Installing system dependencies..."
apt-get update
apt-get install -y build-essential netcat curl python3.12 python3-pip nodejs npm
check_success "System dependencies installed" "Failed to install system dependencies"

# Install Poetry
print_status "Installing Poetry..."
curl -sSL https://install.python-poetry.org | python3 -
check_success "Poetry installed" "Failed to install Poetry"

# Clone OpenHands main repository
print_status "Cloning OpenHands repository..."
git clone https://github.com/All-Hands-AI/OpenHands.git
cd OpenHands
check_success "OpenHands repository cloned" "Failed to clone OpenHands"

# Build OpenHands
print_status "Building OpenHands..."
make build
check_success "OpenHands built successfully" "Failed to build OpenHands"

# Clone Dynamic Agents into the extensions directory
print_status "Installing Dynamic Agents extension..."
mkdir -p extensions
cd extensions
git clone https://github.com/makafeli/Dynamic-Agents-OpenHands.git dynamic-agents
cd dynamic-agents

# Create extension structure
mkdir -p src/routes
mkdir -p src/templates
mkdir -p src/static

# Install extension dependencies
print_status "Installing extension dependencies..."
poetry install
check_success "Extension dependencies installed" "Failed to install extension dependencies"

# Create extension configuration
print_status "Configuring extension..."
cat > extension.toml << 'EOL'
[extension]
name = "dynamic-agents"
version = "0.1.0"
description = "Dynamic Agents extension for OpenHands"

[routes]
prefix = "/agents"
dashboard = "/dashboard"
api = "/api"

[hooks]
terminal = true  # Enable terminal command listening
EOL

# Create extension integration file
print_status "Creating extension integration..."
cat > src/integration.py << 'EOL'
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from openhands_dynamic_agents import DynamicAgent, TechStackAnalyzer
from openhands_dynamic_agents.core.prompt_processor import PromptProcessor
from openhands_dynamic_agents.dashboard.app import Dashboard
import os

class DynamicAgentsExtension:
    def __init__(self):
        self.processor = PromptProcessor()
        self.analyzer = TechStackAnalyzer()
        self.router = APIRouter()
        self.templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
        self.setup_routes()
        
    def setup_routes(self):
        """Setup FastAPI routes for the extension"""
        
        @self.router.get("/dashboard", response_class=HTMLResponse)
        async def dashboard(request: Request):
            """Render the dashboard"""
            return self.templates.TemplateResponse(
                "dashboard.html",
                {"request": request, "title": "Dynamic Agents Dashboard"}
            )
            
        @self.router.post("/api/analyze")
        async def analyze_command(command: str):
            """Analyze a command and create/use agents as needed"""
            agent = DynamicAgent("terminal_agent", keyword="python")
            return agent.run({"command": command})
        
        @self.router.get("/api/agents")
        async def list_agents():
            """List all active agents"""
            return {"agents": []}
        
    def handle_terminal_command(self, command: str):
        """Handle terminal commands and check for keywords"""
        # Process command and create/use agents as needed
        agent = DynamicAgent("terminal_agent", keyword="python")
        return agent.run({"command": command})
        
    def get_routes(self):
        """Return FastAPI router with all routes"""
        return self.router
        
    def register_extension(self, app: FastAPI):
        """Register the extension with the main OpenHands app"""
        app.include_router(self.router, prefix="/agents", tags=["Dynamic Agents"])
EOL

# Create dashboard template
print_status "Creating dashboard template..."
cat > src/templates/dashboard.html << 'EOL'
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .dashboard-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .agents-list {
            margin-top: 20px;
        }
        .activity-log {
            margin-top: 20px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <h1>{{ title }}</h1>
        
        <div class="agents-list">
            <h2>Active Agents</h2>
            <div id="agents-graph"></div>
        </div>
        
        <div class="activity-log">
            <h2>Activity Log</h2>
            <div id="activity-log"></div>
        </div>
    </div>

    <script>
        // Initialize dashboard
        function initDashboard() {
            // Fetch and display agents
            fetch('/agents/api/agents')
                .then(response => response.json())
                .then(data => {
                    // Update agents display
                });
        }

        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', initDashboard);
    </script>
</body>
</html>
EOL

# Link extension to OpenHands
cd ../..
print_status "Linking extension to OpenHands..."
cat >> pyproject.toml << 'EOL'

[tool.poetry.dependencies]
dynamic-agents = { path = "extensions/dynamic-agents", develop = true }
EOL

poetry install
check_success "Extension linked successfully" "Failed to link extension"

# Update OpenHands configuration to include extension
print_status "Updating OpenHands configuration..."
cat > config.toml << 'EOL'
[server]
host = "0.0.0.0"
port = 3000

[extensions]
enabled = ["dynamic-agents"]

[extensions.dynamic-agents]
route_prefix = "/agents"
dashboard_route = "/dashboard"
api_route = "/api"
EOL

print_status "Setting up OpenHands configuration..."
make setup-config

print_success "Integration completed successfully!"
echo -e "\nAccess points:"
echo -e "- OpenHands: ${YELLOW}http://localhost:3000${NC}"
echo -e "- Dynamic Agents Dashboard: ${YELLOW}http://localhost:3000/agents/dashboard${NC}"
echo -e "- Dynamic Agents API: ${YELLOW}http://localhost:3000/agents/api${NC}"
echo -e "\nUseful commands:"
echo -e "- Start servers: ${YELLOW}make run${NC}"
echo -e "- View help: ${YELLOW}make help${NC}"

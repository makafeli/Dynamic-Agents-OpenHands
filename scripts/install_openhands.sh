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

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if command_exists python3; then
        python3 --version | cut -d' ' -f2
    else
        echo "0"
    fi
}

# Function to check if a package is installed
package_installed() {
    dpkg -l "$1" &> /dev/null
}

# Create installation directory
INSTALL_DIR="/opt/openhands"
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

print_status "Starting OpenHands installation..."

# Check system requirements
print_status "Checking system requirements..."

# Install required packages for building Python
print_status "Installing build dependencies..."
apt-get update
apt-get install -y build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev git

# Install pyenv
print_status "Installing pyenv..."
if [ ! -d "$HOME/.pyenv" ]; then
    curl https://pyenv.run | bash
    
    # Add pyenv to PATH
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    
    # Load pyenv in current shell
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
else
    print_success "pyenv is already installed"
fi

# Install Python 3.12 using pyenv
print_status "Installing Python 3.12..."
pyenv install -s 3.12.0
pyenv global 3.12.0

# Verify Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
if [ "$(printf '%s\n' "3.12" "$PYTHON_VERSION" | sort -V | head -n1)" = "3.12" ]; then
    print_success "Python version $PYTHON_VERSION is installed"
else
    print_error "Failed to install Python 3.12"
    exit 1
fi

# Create and activate virtual environment
print_status "Creating virtual environment..."
python3 -m venv /opt/openhands/venv
source /opt/openhands/venv/bin/activate
python3 --version  # Verify Python version
check_success "Virtual environment created" "Failed to create virtual environment"

# Install Python build dependencies
print_status "Installing Python build dependencies..."
pip install --upgrade pip wheel setuptools
# Install build dependencies first
pip install --upgrade pip wheel setuptools build
pip install numpy==1.26.4  # Install newer numpy first
pip install pandas==2.1.3  # Install newer pandas
pip install torch==2.2.1 torchvision==0.17.1 --index-url https://download.pytorch.org/whl/cpu  # Install PyTorch packages
check_success "Python build dependencies installed" "Failed to install Python build dependencies"

# Install poetry
if ! command_exists poetry; then
    print_status "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 -
    ln -s /usr/local/bin/poetry /usr/bin/poetry
    check_success "Poetry installed" "Failed to install Poetry"
else
    print_success "Poetry already installed"
fi

# Configure poetry
poetry config virtualenvs.in-project true

# Clone and install OpenHands
print_status "Cloning OpenHands repository..."
if [ ! -d "OpenHands" ]; then
    git clone https://github.com/All-Hands-AI/OpenHands.git
    check_success "OpenHands repository cloned" "Failed to clone OpenHands"
else
    print_status "OpenHands directory exists, updating..."
    cd OpenHands
    git pull
    cd ..
fi

print_status "Installing OpenHands dependencies..."
cd OpenHands

# Update OpenHands pyproject.toml to use specific pandas version
cat > pyproject.toml << 'EOL'
[tool.poetry]
name = "openhands"
version = "0.1.0"
description = "OpenHands AI Framework"
authors = ["OpenHands Team"]

[tool.poetry.dependencies]
python = "^3.10"  # Match project requirements
pandas = "^2.1.3"  # Use newer pandas version
numpy = "^1.26.4"  # Use newer numpy version
torch = "^2.2.1"
torchvision = "^0.17.1"
python-frontmatter = "^1.1.0"  # Required by openhands.microagent
pydantic = "^2.6.1"  # Required by openhands.microagent
fastapi = "^0.104.0"  # Required for API functionality
uvicorn = "^0.24.0"  # Required for running the server
pyyaml = "^6.0.1"  # Required for configuration

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
EOL

# Generate new lock file and install dependencies
poetry lock
check_success "Lock file generated" "Failed to generate lock file"
poetry install
check_success "OpenHands dependencies installed" "Failed to install OpenHands dependencies"
cd ..

# Clone and install Dynamic-Agents-OpenHands
print_status "Cloning Dynamic-Agents-OpenHands repository..."
if [ ! -d "Dynamic-Agents-OpenHands" ]; then
    git clone https://github.com/makafeli/Dynamic-Agents-OpenHands.git
    check_success "Dynamic-Agents repository cloned" "Failed to clone Dynamic-Agents"
else
    print_status "Dynamic-Agents directory exists, updating..."
    cd Dynamic-Agents-OpenHands
    git pull
    cd ..
fi

print_status "Installing Dynamic-Agents dependencies..."
cd Dynamic-Agents-OpenHands

# Create a custom pyproject.toml with specific pandas version
cat > pyproject.toml << 'EOL'
[tool.poetry]
name = "openhands-dynamic-agents"
version = "0.1.0"
description = "Dynamic Agents for OpenHands"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"  # Match project requirements
openhands = {path = "../OpenHands", develop = true}
pandas = "^2.1.3"  # Use newer pandas version
numpy = "^1.26.4"  # Use newer numpy version
dash = "^2.0.0"
plotly = "^5.0.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry.scripts]
agents = "openhands_dynamic_agents.cli:main"
EOL

# Generate new lock file and install dependencies
poetry lock
check_success "Lock file generated" "Failed to generate lock file"
poetry install
check_success "Dynamic-Agents dependencies installed" "Failed to install Dynamic-Agents dependencies"

# Create OpenHands configuration
print_status "Creating OpenHands configuration..."
cd /opt/openhands/OpenHands
cat > config.toml << 'EOL'
[server]
host = "0.0.0.0"
port = 3000

[workspace]
directory = "./workspace"

[llm]
model = "gpt-4"
api_key = ""  # Will be prompted during first run

[extensions]
enabled = ["dynamic-agents"]

[extensions.dynamic-agents]
route_prefix = "/agents"
dashboard_route = "/dashboard"
api_route = "/api"
EOL

# Create extension link
print_status "Creating extension link..."
mkdir -p extensions
ln -sf "/opt/openhands/Dynamic-Agents-OpenHands" extensions/dynamic-agents

# Create start script
print_status "Creating start script..."
cat > start_server.sh << 'EOL'
#!/bin/bash
cd /opt/openhands/OpenHands
source .venv/bin/activate
export PYTHONPATH=/opt/openhands/Dynamic-Agents-OpenHands/src:/opt/openhands/OpenHands
poetry run python -m openhands
EOL

chmod +x start_server.sh
check_success "Start script created" "Failed to create start script"

# Create stop script
print_status "Creating stop script..."
cat > stop_server.sh << 'EOL'
#!/bin/bash
pkill -f "python.*openhands"
echo "OpenHands server stopped"
EOL

chmod +x stop_server.sh
check_success "Stop script created" "Failed to create stop script"

# Create test script
print_status "Creating test script..."
cat > test_openhands.py << 'EOL'
#!/usr/bin/env python3
from openhands_dynamic_agents import DynamicAgent, TechStackAnalyzer
from openhands_dynamic_agents.core.prompt_processor import PromptProcessor

def test_openhands():
    print("Testing OpenHands functionality...")
    
    # Initialize components
    processor = PromptProcessor()
    agent = DynamicAgent("test_agent", keyword="python")
    analyzer = TechStackAnalyzer()
    
    print("\n✓ Successfully imported and initialized OpenHands components")
    print("✓ OpenHands is running at http://localhost:3000")
    print("✓ Dynamic Agents Dashboard at http://localhost:3000/agents/dashboard")
    print("\nTo use OpenHands in your code:")
    print("1. Activate the virtual environment:")
    print("   source /opt/openhands/venv/bin/activate")
    print("2. Import OpenHands in your Python code:")
    print("   from openhands_dynamic_agents import DynamicAgent, TechStackAnalyzer")
    print("3. Create an agent:")
    print('   agent = DynamicAgent("my_agent", keyword="python")')
    print("4. Use the agent:")
    print('   result = agent.run({"code": "def example(): pass"})')

if __name__ == "__main__":
    test_openhands()
EOL

chmod +x test_openhands.py

# Create wrapper script for test-openhands
cat > /usr/local/bin/test-openhands << 'EOL'
#!/bin/bash
cd /opt/openhands/Dynamic-Agents-OpenHands
source .venv/bin/activate
export PYTHONPATH=/opt/openhands/Dynamic-Agents-OpenHands/src:/opt/openhands/OpenHands
python3 test_openhands.py
EOL

chmod +x /usr/local/bin/test-openhands

# Start OpenHands server
print_status "Starting OpenHands server..."
cd /opt/openhands/OpenHands
nohup ./start_server.sh > server.log 2>&1 &
echo $! > server.pid
sleep 2  # Wait for server to start

# Print installation summary
print_success "Installation completed successfully!"
echo -e "\nInstallation Summary:"
echo -e "--------------------"
echo -e "OpenHands: ${GREEN}Installed${NC}"
echo -e "Dynamic Agents: ${GREEN}Installed (as OpenHands Extension)${NC}"
echo -e "Server: ${GREEN}Running${NC}"
echo -e "\nAccess Points:"
echo -e "- OpenHands UI: ${YELLOW}http://$(hostname -I | awk '{print $1}'):3000${NC}"
echo -e "- Dynamic Agents Dashboard: ${YELLOW}http://$(hostname -I | awk '{print $1}'):3000/agents/dashboard${NC}"
echo -e "\nUseful Commands:"
echo -e "- Start server: ${YELLOW}/opt/openhands/OpenHands/start_server.sh${NC}"
echo -e "- Stop server: ${YELLOW}/opt/openhands/OpenHands/stop_server.sh${NC}"
echo -e "- View logs: ${YELLOW}tail -f /opt/openhands/OpenHands/server.log${NC}"
echo -e "- Test installation: ${YELLOW}test-openhands${NC}"

# Create uninstall script
cat > uninstall.sh << 'EOL'
#!/bin/bash
# Stop the server if running
if [ -f /opt/openhands/OpenHands/server.pid ]; then
    /opt/openhands/OpenHands/stop_server.sh
fi
rm -rf /opt/openhands
echo "OpenHands and Dynamic Agents extension uninstalled successfully"
EOL
chmod +x uninstall.sh

echo -e "\nTo uninstall everything, run: ${YELLOW}./uninstall.sh${NC}"
echo -e "\nNote: On first run, you'll be prompted for your OpenAI API key"

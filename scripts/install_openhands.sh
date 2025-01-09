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

# Create installation directory
INSTALL_DIR="/opt/openhands"
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

print_status "Starting OpenHands installation..."

# Update system
print_status "Updating system packages..."
apt-get update
check_success "System packages updated" "Failed to update system packages"

# Install dependencies
print_status "Installing dependencies..."
apt-get install -y git python3-pip python3-venv build-essential python3-dev curl python3-wheel bc
check_success "Dependencies installed" "Failed to install dependencies"

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

# Create systemd service
print_status "Creating dashboard service..."
cat > /etc/systemd/system/openhands-dashboard.service << 'EOL'
[Unit]
Description=OpenHands Dynamic Agents Dashboard
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/openhands/Dynamic-Agents-OpenHands
Environment=PATH=/opt/openhands/Dynamic-Agents-OpenHands/.venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=/opt/openhands/Dynamic-Agents-OpenHands/src:/opt/openhands/OpenHands
Environment=VIRTUAL_ENV=/opt/openhands/Dynamic-Agents-OpenHands/.venv
ExecStart=/bin/bash -c 'cd /opt/openhands/Dynamic-Agents-OpenHands && source .venv/bin/activate && python3 -c "from openhands_dynamic_agents.dashboard.app import Dashboard; Dashboard(host=\"0.0.0.0\", port=8080).start()"'
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd
print_status "Reloading systemd..."
systemctl daemon-reload

# Enable and start dashboard service
print_status "Starting dashboard service..."
systemctl enable openhands-dashboard
systemctl start openhands-dashboard
check_success "Dashboard service started" "Failed to start dashboard service"

# Print installation summary
print_success "Installation completed successfully!"
echo -e "\nInstallation Summary:"
echo -e "--------------------"
echo -e "OpenHands: ${GREEN}Installed${NC}"
echo -e "Dynamic Agents: ${GREEN}Installed${NC}"
echo -e "Dashboard: ${GREEN}Running${NC}"
echo -e "\nDashboard URL: http://$(hostname -I | awk '{print $1}'):8080"
echo -e "\nUseful commands:"
echo -e "- Check dashboard status: ${YELLOW}systemctl status openhands-dashboard${NC}"
echo -e "- View dashboard logs: ${YELLOW}journalctl -u openhands-dashboard -f${NC}"

# Create uninstall script
cat > uninstall.sh << 'EOL'
#!/bin/bash
systemctl stop openhands-dashboard
systemctl disable openhands-dashboard
rm /etc/systemd/system/openhands-dashboard.service
rm -rf /opt/openhands
echo "OpenHands and Dynamic Agents uninstalled successfully"
EOL
chmod +x uninstall.sh

echo -e "\nTo uninstall everything, run: ${YELLOW}./uninstall.sh${NC}"

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

# Check system requirements
print_status "Checking system requirements..."

# List of required packages
REQUIRED_PACKAGES=(
    "build-essential"
    "python3"
    "python3-pip"
    "python3-venv"
    "python3-dev"
    "netcat-traditional"  # Debian-specific netcat package
    "curl"
    "nodejs"
    "npm"
)

# Check and install missing packages
MISSING_PACKAGES=()
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if ! package_installed "$pkg"; then
        MISSING_PACKAGES+=("$pkg")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    print_status "Installing missing packages: ${MISSING_PACKAGES[*]}"
    # Add NodeSource repository for Node.js
    if [[ " ${MISSING_PACKAGES[@]} " =~ " nodejs " ]]; then
        print_status "Adding NodeSource repository..."
        curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    fi
    apt-get update
    apt-get install -y "${MISSING_PACKAGES[@]}"
else
    print_success "All required packages are installed"
fi

# Check Python version
PYTHON_VERSION=$(check_python_version)
if [ "$(printf '%s\n' "3.10" "$PYTHON_VERSION" | sort -V | head -n1)" = "3.10" ]; then
    print_success "Python version $PYTHON_VERSION is compatible"
else
    print_error "Python version $PYTHON_VERSION is not compatible. Version 3.10 or higher is required."
    exit 1
fi

# Check/Install Poetry
if ! command_exists poetry; then
    print_status "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
else
    print_success "Poetry is already installed"
fi

# Function to check if OpenHands is installed
check_openhands() {
    if [ -d "/opt/openhands/OpenHands" ]; then
        return 0
    else
        return 1
    fi
}

# Function to check if Dynamic Agents is installed
check_dynamic_agents() {
    if [ -d "/opt/openhands/Dynamic-Agents-OpenHands" ]; then
        return 0
    else
        return 1
    fi
}

# Create installation directory
INSTALL_DIR="/opt/openhands"
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Install OpenHands if not present
if ! check_openhands; then
    print_status "Installing OpenHands..."
    git clone https://github.com/All-Hands-AI/OpenHands.git
    cd OpenHands
    make build
    cd ..
else
    print_success "OpenHands is already installed"
fi

# Install Dynamic Agents if not present
if ! check_dynamic_agents; then
    print_status "Installing Dynamic Agents..."
    git clone https://github.com/makafeli/Dynamic-Agents-OpenHands.git
    cd Dynamic-Agents-OpenHands
    poetry install
    cd ..
else
    print_success "Dynamic Agents is already installed"
fi

# Configure integration
print_status "Configuring integration..."
cd OpenHands

# Update configuration
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

print_success "Installation and configuration completed successfully!"
echo -e "\nAccess points:"
echo -e "- OpenHands: ${YELLOW}http://localhost:3000${NC}"
echo -e "- Dynamic Agents Dashboard: ${YELLOW}http://localhost:3000/agents/dashboard${NC}"
echo -e "\nUseful commands:"
echo -e "- Start OpenHands: ${YELLOW}cd /opt/openhands/OpenHands && make run${NC}"
echo -e "- View logs: ${YELLOW}tail -f /opt/openhands/OpenHands/logs/server.log${NC}"

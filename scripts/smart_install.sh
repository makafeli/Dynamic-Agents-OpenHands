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
    apt-get update
    apt-get install -y "${MISSING_PACKAGES[@]}"
else
    print_success "All required packages are installed"
fi

# Install Node.js and npm
if ! command_exists node || ! command_exists npm; then
    print_status "Installing Node.js and npm..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi

# Check Python version
PYTHON_VERSION=$(check_python_version)
if [ "$(printf '%s\n' "3.10" "$PYTHON_VERSION" | sort -V | head -n1)" = "3.10" ]; then
    print_success "Python version $PYTHON_VERSION is compatible"
else
    print_error "Python version $PYTHON_VERSION is not compatible. Version 3.10 or higher is required."
    exit 1
fi

# Install Poetry
if ! command_exists poetry; then
    print_status "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry
    poetry config virtualenvs.in-project true
else
    print_success "Poetry is already installed"
fi

# Create installation directory
INSTALL_DIR="/opt/openhands"
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Install OpenHands
print_status "Installing OpenHands..."
if [ -d "OpenHands" ]; then
    cd OpenHands
    git pull
    cd ..
else
    git clone https://github.com/All-Hands-AI/OpenHands.git
fi

cd OpenHands

# Create non-interactive config
print_status "Creating OpenHands configuration..."
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

# Build OpenHands
print_status "Building OpenHands..."
poetry install
npm install
npm run build

cd ..

# Install Dynamic Agents
print_status "Installing Dynamic Agents..."
if [ -d "Dynamic-Agents-OpenHands" ]; then
    cd Dynamic-Agents-OpenHands
    git pull
else
    git clone https://github.com/makafeli/Dynamic-Agents-OpenHands.git
    cd Dynamic-Agents-OpenHands
fi

# Setup Dynamic Agents
print_status "Setting up Dynamic Agents..."
poetry install

# Create extension link
print_status "Linking Dynamic Agents extension..."
mkdir -p ../OpenHands/extensions
ln -sf "$PWD" ../OpenHands/extensions/dynamic-agents

print_success "Installation completed successfully!"
echo -e "\nAccess points:"
echo -e "- OpenHands: ${YELLOW}http://localhost:3000${NC}"
echo -e "- Dynamic Agents Dashboard: ${YELLOW}http://localhost:3000/agents/dashboard${NC}"
echo -e "\nTo start OpenHands:"
echo -e "1. Navigate to OpenHands directory:"
echo -e "   ${YELLOW}cd /opt/openhands/OpenHands${NC}"
echo -e "2. Start the server:"
echo -e "   ${YELLOW}poetry run python -m openhands${NC}"
echo -e "\nNote: On first run, you'll be prompted for your OpenAI API key"

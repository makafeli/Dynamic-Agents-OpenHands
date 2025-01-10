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

print_status "Stopping any running OpenHands processes..."
pkill -f "python.*openhands"
pkill -f "node.*openhands"

print_status "Removing previous installations..."
# Remove installation directories
rm -rf /opt/openhands
rm -rf ~/.cache/pypoetry
rm -rf ~/.local/share/pypoetry

print_status "Cleaning up system packages..."
apt-get remove -y python3-pip nodejs npm
apt-get autoremove -y
apt-get clean

print_status "Cleaning up Poetry..."
curl -sSL https://install.python-poetry.org | POETRY_UNINSTALL=1 python3 -

print_status "Running new installation..."
cd "$(dirname "$0")"
./integrate_dynamic_agents.sh

print_success "Clean installation completed!"

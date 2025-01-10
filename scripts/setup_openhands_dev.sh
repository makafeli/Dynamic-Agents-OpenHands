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

print_status "Installing system dependencies..."
apt-get update
apt-get install -y build-essential netcat curl python3.12 python3-pip nodejs npm

print_status "Installing Poetry..."
curl -sSL https://install.python-poetry.org | python3 -

print_status "Cloning OpenHands repository..."
git clone https://github.com/All-Hands-AI/OpenHands.git
cd OpenHands

print_status "Building OpenHands..."
make build

print_status "Setting up configuration..."
make setup-config

print_status "Starting OpenHands servers..."
make run

print_success "OpenHands development server setup complete!"
echo -e "\nUseful commands:"
echo -e "- Start full application: ${YELLOW}make run${NC}"
echo -e "- Start backend only: ${YELLOW}make start-backend${NC}"
echo -e "- Start frontend only: ${YELLOW}make start-frontend${NC}"
echo -e "- View help: ${YELLOW}make help${NC}"
echo -e "\nAccess OpenHands at: http://localhost:3000"

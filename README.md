# OpenHands Dynamic Agents

Dynamic Agents extension for the OpenHands AI Framework.

## System Requirements

- Python 3.10 or higher
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space

### Software Dependencies

The installation script will automatically install these dependencies:
- git
- python3-pip
- python3-venv
- build-essential
- python3-dev
- curl
- python3-wheel

### Python Package Dependencies

Key Python packages (automatically installed):
- numpy >= 1.26.4
- pandas >= 2.1.3
- torch >= 2.2.1
- torchvision >= 0.17.1
- dash >= 2.0.0
- plotly >= 5.0.0
- fastapi >= 0.104.0
- uvicorn >= 0.24.0
- pydantic >= 2.6.1
- python-frontmatter >= 1.1.0
- pyyaml >= 6.0.1

## Installation

### Option 1: Standard Installation (with systemd)

For systems with systemd (standard Linux distributions):

1. Clone this repository:
```bash
git clone https://github.com/makafeli/Dynamic-Agents-OpenHands.git
cd Dynamic-Agents-OpenHands
```

2. Make the installation script executable:
```bash
chmod +x scripts/install_openhands.sh
```

3. Run the installation script with sudo:
```bash
sudo ./scripts/install_openhands.sh
```

The installation script will:
- Set up the required system dependencies
- Install Python packages
- Clone and configure OpenHands
- Set up the Dynamic Agents extension
- Configure and start the dashboard service as a systemd service

### Option 2: Container Installation

For container environments or systems without systemd:

1. Clone this repository:
```bash
git clone https://github.com/makafeli/Dynamic-Agents-OpenHands.git
cd Dynamic-Agents-OpenHands
```

2. Make the installation and start scripts executable:
```bash
chmod +x scripts/install_openhands.sh scripts/start_dashboard.sh
```

3. Run the installation script:
```bash
./scripts/install_openhands.sh
```

4. Start the dashboard:
```bash
./scripts/start_dashboard.sh
```

## Dashboard

The dashboard runs on port 8080 by default and can be accessed at:
```
http://localhost:8080
```

### Managing the Dashboard

#### For systemd installations:

Check service status:
```bash
sudo systemctl status openhands-dashboard
```

View logs:
```bash
sudo journalctl -u openhands-dashboard -f
```

Restart the service:
```bash
sudo systemctl restart openhands-dashboard
```

#### For container installations:

The dashboard runs in the foreground when started with `start_dashboard.sh`. Use standard terminal controls (Ctrl+C to stop) and view logs directly in the terminal.

## Uninstallation

To remove OpenHands and Dynamic Agents:
```bash
sudo /opt/openhands/uninstall.sh
```

## Project Structure

```
Dynamic-Agents-OpenHands/
├── docs/               # Documentation
├── examples/           # Example usage
├── scripts/           # Installation and utility scripts
│   ├── install_openhands.sh     # Installation script
│   ├── start_dashboard.sh       # Dashboard startup script
│   └── openhands-dashboard.service  # Systemd service file
├── src/               # Source code
│   └── openhands_dynamic_agents/
│       ├── analysis/      # Analysis tools
│       ├── core/          # Core functionality
│       ├── dashboard/     # Web dashboard
│       ├── templates/     # Template files
│       └── utils/         # Utility functions
└── tests/             # Test files
```

## Features

- Technology stack analysis for repositories
- Real-time agent monitoring
- Web-based dashboard interface
- REST API for integration

## License

[Add your license information here]

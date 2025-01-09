# OpenHands Dynamic Agents

Dynamic Agents extension for the OpenHands AI Framework.

## System Requirements

- Linux-based operating system (Debian/Ubuntu recommended)
- Python 3.10 or higher
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space
- Root/sudo access for system service installation

### Software Dependencies

The installation script will automatically install these dependencies:
- git
- python3-pip
- python3-venv
- build-essential
- python3-dev
- curl
- python3-wheel
- Poetry (package manager)

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
- Configure and start the dashboard service

## Dashboard

The dashboard service runs on port 8080 by default and can be accessed at:
```
http://localhost:8080
```

### Managing the Dashboard Service

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
├── src/               # Source code
│   └── openhands_dynamic_agents/
│       ├── analysis/      # Analysis tools
│       ├── core/          # Core functionality
│       ├── dashboard/     # Web dashboard
│       ├── templates/     # Template files
│       └── utils/         # Utility functions
└── tests/             # Test files
```

## License

[Add your license information here]

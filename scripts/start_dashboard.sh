#!/bin/bash

# Set up environment variables
export PATH=/opt/openhands/venv/bin:/usr/local/bin:/usr/bin:/bin
export PYTHONPATH=/opt/openhands/Dynamic-Agents-OpenHands:/opt/openhands/OpenHands
export VIRTUAL_ENV=/opt/openhands/venv

# Start the dashboard
cd /opt/openhands/Dynamic-Agents-OpenHands
/opt/openhands/venv/bin/python3 -c "from openhands_dynamic_agents.dashboard.app import Dashboard; Dashboard(host='0.0.0.0', port=8080).start()"

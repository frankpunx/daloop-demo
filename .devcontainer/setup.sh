#!/bin/bash
set -e

echo "Installing Python packages..."
pip3 install -r .devcontainer/requirements.txt

echo "Setup complete!"

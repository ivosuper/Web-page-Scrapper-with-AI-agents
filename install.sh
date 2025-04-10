#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo "Virtual environment 'venv' not found. Creating..."
  python3 -m venv venv
  echo "Virtual environment 'venv' created."
else
  echo "Virtual environment 'venv' found."
fi

# Activate the virtual environment
source venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
  echo "Installing requirements from requirements.txt..."
  pip install -r requirements.txt
  echo "Requirements installed successfully."
else
  echo "requirements.txt not found. Skipping installation."
fi
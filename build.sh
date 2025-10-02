#!/bin/bash

# Upgrade pip
pip install --upgrade pip

# Install numpy first with specific version
pip install "numpy>=1.26.0,<2.0.0"

# Install other dependencies
pip install -r requirements.txt

# Verify numpy version
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')"

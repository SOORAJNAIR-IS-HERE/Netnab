#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" &>/dev/null
}

# Check if Python 3 is installed
if ! command_exists python3; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if git is installed
if ! command_exists git; then
    echo "Git is not installed. Please install Git first."
    exit 1
fi

# Check if pip (Python package manager) is installed
if ! command_exists pip; then
    echo "pip is not installed. Please install pip first."
    exit 1
fi

# Clone the repository
echo "Cloning the repository..."
git clone https://github.com/SOORAJNAIR-IS-HERE/Netnab.git

# Check if the repository was cloned successfully
if [ ! -d "NetNab" ]; then
    echo "Failed to clone the repository. Exiting."
    exit 1
fi

# Change into the cloned directory
cd NetNab || { echo "Failed to enter the NetNab directory."; exit 1; }

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Make netnab.py executable
chmod +x netnab.py

# Copy the script to /usr/local/bin (to make it accessible globally)
echo "Installing NetNab to /usr/local/bin..."
sudo cp netnab.py /usr/local/bin/netnab
chmod +x /usr/local/bin/netnab  # Ensure executable permission

# Provide feedback to the user
echo "NetNab has been successfully installed!"
echo "You can now run it globally with: netnab <ip>"

#!/bin/bash

# Ensure the script is run with sudo/root permissions
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root or use sudo."
    exit 1
fi

# Define the source and destination
SOURCE="Netnab.py"  # Adjusted to match your actual filename
DEST="/usr/local/bin/netnab"

# Check if Netnab.py exists
if [ ! -f "$SOURCE" ]; then
    echo "Error: $SOURCE not found. Make sure you're running this script from the correct directory."
    exit 1
fi

# Copy Netnab.py to /usr/local/bin as 'netnab'
echo "Copying $SOURCE to $DEST..."
cp "$SOURCE" "$DEST"

# Make it executable
chmod +x "$DEST"

echo "Installation complete! You can now use the tool globally with: netnab <ip>"


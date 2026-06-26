#!/bin/bash
# Setup serial port permissions for WSL

echo "Setting up serial port permissions..."

# Function to setup permissions for a specific port
setup_port_permissions() {
    local port=$1
    if [ -e "$port" ]; then
        echo "Setting permissions for $port"
        sudo chmod 666 "$port" 2>/dev/null || echo "  Failed to set permissions for $port"
    else
        echo "Port $port does not exist"
    fi
}

# Setup permissions for common serial ports
for port in /dev/ttyS{0..7}; do
    setup_port_permissions "$port"
done

for port in /dev/ttyUSB{0..3}; do
    setup_port_permissions "$port"
done

for port in /dev/ttyACM{0..3}; do
    setup_port_permissions "$port"
done

echo ""
echo "Permissions setup complete!"
echo ""
echo "To verify permissions, run:"
echo "ls -la /dev/ttyS*"
echo ""
echo "Note: You may need to run this script with sudo if you get permission errors"
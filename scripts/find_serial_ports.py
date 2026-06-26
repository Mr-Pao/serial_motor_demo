#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find available serial port devices
"""
import os
import glob

def find_serial_ports():
    """Find all possible serial port devices"""
    serial_ports = []
    
    # Common serial port device paths
    patterns = [
        '/dev/ttyUSB*',
        '/dev/ttyACM*', 
        '/dev/ttyS*',
        '/dev/tty.usb*',
        '/dev/cu.usb*',
    ]
    
    for pattern in patterns:
        ports = glob.glob(pattern)
        for port in ports:
            try:
                # Check if device is accessible
                if os.path.exists(port):
                    serial_ports.append(port)
            except Exception as e:
                print(f"Cannot access {port}: {e}")
    
    return serial_ports

def check_port_permissions(port):
    """Check serial port device permissions"""
    if not os.path.exists(port):
        return False, "Device does not exist"
    
    if not os.access(port, os.R_OK | os.W_OK):
        return False, "No read/write permission"
    
    return True, "Accessible"

def main():
    print("Searching for available serial port devices...")
    ports = find_serial_ports()
    
    if not ports:
        print("No serial port devices found")
        print("\nPossible reasons:")
        print("1. ESP8266 is not connected to computer via USB")
        print("2. WSL cannot access Windows USB devices")
        print("3. Need to use usbipd tool to forward USB device to WSL")
        return
    
    print(f"\nFound {len(ports)} serial port devices:")
    for i, port in enumerate(ports, 1):
        accessible, status = check_port_permissions(port)
        status_icon = "OK" if accessible else "X"
        print(f"{i}. {port} - [{status_icon}] {status}")
    
    print("\nRecommended actions:")
    if any('/dev/ttyUSB' in port for port in ports):
        print("? Use default serial port: /dev/ttyUSB0")
    elif any('/dev/ttyACM' in port for port in ports):
        print("? Use ACM serial port: /dev/ttyACM0")
    elif any('/dev/ttyS' in port for port in ports):
        print("? Use Windows serial port forwarding: /dev/ttyS0")
    
    print("\nLaunch command examples:")
    for port in ports[:3]:  # Only show first 3
        print(f"ros2 launch serial_motor_demo motor_control.launch.py --ros-args -p serial_bridge.serial_port:={port}")

if __name__ == '__main__':
    main()
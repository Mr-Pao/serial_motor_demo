#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test motor driver I2C communication through ESP8266
"""
import serial
import time

def main():
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)
    time.sleep(2)
    print("Connected to ESP8266")
    
    # 测试不同的速度值
    test_speeds = [50, 100, 150, 200, 255]
    
    try:
        for speed in test_speeds:
            print(f"\nTesting speed: {speed}")
            
            # 发送 PWM 命令（直接控制电机）
            cmd = f'PWM:{speed},0,0,0\n'
            ser.write(cmd.encode())
            print(f"Sent: {cmd.strip()}")
            
            response = ser.readline().decode().strip()
            print(f"Response: {response}")
            
            time.sleep(3)  # 运行3秒
            
            # 停止
            ser.write(b'STOP\n')
            response = ser.readline().decode().strip()
            print(f"Sent: STOP, Response: {response}")
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTest interrupted")
    finally:
        # 确保停止电机
        ser.write(b'STOP\n')
        ser.close()
        print("Serial port closed")

if __name__ == '__main__':
    main()
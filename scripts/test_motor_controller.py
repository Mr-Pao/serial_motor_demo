#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test motor controller without hardware
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import time

class MotorTester(Node):
    def __init__(self):
        super().__init__('motor_tester')
        
        self.publisher = self.create_publisher(Int32, 'motor_speed', 10)
        self.get_logger().info('Motor Tester Node started')
        
    def test_motor_sequence(self):
        """Run a test sequence for motor control"""
        test_speeds = [
            (0, "Stop"),
            (100, "Forward 100"),
            (200, "Forward 200"),
            (255, "Forward Max"),
            (0, "Stop"),
            (-100, "Backward 100"),
            (-200, "Backward 200"),
            (-255, "Backward Max"),
            (0, "Stop")
        ]
        
        self.get_logger().info("Starting motor test sequence...")
        
        for speed, description in test_speeds:
            self.get_logger().info(f"Test: {description} (Speed: {speed})")
            
            msg = Int32()
            msg.data = speed
            self.publisher.publish(msg)
            
            time.sleep(2)  # Wait 2 seconds for each test
        
        self.get_logger().info("Motor test sequence completed!")

def main(args=None):
    rclpy.init(args=args)
    motor_tester = MotorTester()
    
    try:
        # Run the test sequence
        motor_tester.test_motor_sequence()
    except KeyboardInterrupt:
        motor_tester.get_logger().info("Test interrupted by user")
    finally:
        # Stop motor before exiting
        msg = Int32()
        msg.data = 0
        motor_tester.publisher.publish(msg)
        motor_tester.get_logger().info("Motor stopped")
        
        motor_tester.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
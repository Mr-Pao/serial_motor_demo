import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='serial_motor_demo',
            executable='serial_bridge',
            name='serial_bridge',
            output='screen',
            parameters=[
                {'serial_port': '/dev/ttyUSB0'},
                {'baud_rate': 115200},
                {'timeout': 1.0}
            ]
        ),
        Node(
            package='serial_motor_demo',
            executable='motor_controller',
            name='motor_controller',
            output='screen',
            parameters=[
                {'speed': 100}
            ]
        )
    ])
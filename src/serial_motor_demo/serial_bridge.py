import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial
import time

class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')
        
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baud_rate', 115200)
        self.declare_parameter('timeout', 1.0)
        
        self.serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        self.baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value
        self.timeout = self.get_parameter('timeout').get_parameter_value().double_value
        
        self.subscription = self.create_subscription(
            Int32,
            'motor_speed',
            self.motor_speed_callback,
            10
        )
        
        self.ser = None
        self.connect_serial()
        
        self.get_logger().info(f'Serial Bridge Node started. Port: {self.serial_port}, Baud: {self.baud_rate}')
    
    def connect_serial(self):
        try:
            self.ser = serial.Serial(
                port=self.serial_port,
                baudrate=self.baud_rate,
                timeout=self.timeout
            )
            time.sleep(2)
            self.get_logger().info('Serial connection established')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to connect to serial port: {e}')
            self.ser = None
    
    def motor_speed_callback(self, msg):
        speed = msg.data
        
        if self.ser is None or not self.ser.is_open:
            self.get_logger().warn('Serial port not connected, trying to reconnect')
            self.connect_serial()
            return
        
        try:
            cmd = f'SPEED:{speed}\n'
            self.ser.write(cmd.encode())
            self.get_logger().debug(f'Sent command: {cmd.strip()}')
            
            response = self.ser.readline().decode().strip()
            if response:
                self.get_logger().debug(f'Response: {response}')
        except serial.SerialException as e:
            self.get_logger().error(f'Serial communication error: {e}')
            self.ser = None
    
    def destroy_node(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.get_logger().info('Serial port closed')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    serial_bridge = SerialBridge()
    rclpy.spin(serial_bridge)
    serial_bridge.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
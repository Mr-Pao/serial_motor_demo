import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')
        
        self.publisher_ = self.create_publisher(Int32, 'motor_speed', 10)
        
        self.declare_parameter('speed', 0)
        self.speed = self.get_parameter('speed').get_parameter_value().integer_value
        
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        self.get_logger().info(f'Motor Controller Node started. Speed: {self.speed}')
    
    def timer_callback(self):
        msg = Int32()
        msg.data = self.speed
        self.publisher_.publish(msg)
        self.get_logger().debug(f'Published speed: {self.speed}')

def main(args=None):
    rclpy.init(args=args)
    motor_controller = MotorController()
    rclpy.spin(motor_controller)
    motor_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
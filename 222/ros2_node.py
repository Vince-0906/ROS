import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node = Node('py_node')
    node.get_logger().info('cnm')
    node.get_logger().warn('cnm')
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=='__main__':
    main()

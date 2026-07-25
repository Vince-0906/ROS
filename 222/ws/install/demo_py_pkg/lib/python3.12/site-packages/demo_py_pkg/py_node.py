import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node = Node('py_node')
    node.get_logger().info('hello py')
    node.get_logger().warn('hello py')
    rclpy.spin(node)
    rclpy.shutdown()
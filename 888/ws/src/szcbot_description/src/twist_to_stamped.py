#!/usr/bin/env python3
"""
Twist to TwistStamped converter
将 geometry_msgs/Twist 转换为 geometry_msgs/TwistStamped
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped


class TwistToStamped(Node):
    def __init__(self):
        super().__init__('twist_to_stamped')

        # 订阅不带时间戳的 cmd_vel（来自 teleop 等）
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.twist_callback,
            10
        )

        # 发布带时间戳的 cmd_vel_stamped（给控制器）
        self.publisher = self.create_publisher(
            TwistStamped,
            '/cmd_vel_stamped',
            10
        )

        self.get_logger().info('Twist to TwistStamped converter started')
        self.get_logger().info('Subscribing to: /cmd_vel (Twist)')
        self.get_logger().info('Publishing to: /cmd_vel_stamped (TwistStamped)')

    def twist_callback(self, msg):
        # 创建带时间戳的消息
        stamped_msg = TwistStamped()
        stamped_msg.header.stamp = self.get_clock().now().to_msg()
        stamped_msg.header.frame_id = 'base_footprint'
        stamped_msg.twist = msg

        # 发布
        self.publisher.publish(stamped_msg)


def main(args=None):
    rclpy.init(args=args)
    node = TwistToStamped()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

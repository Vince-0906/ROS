import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster # 静态坐标发送器
from geometry_msgs.msg import TransformStamped # 坐标变换消息类型
from tf_transformations import quaternion_from_euler # 欧拉角转四元数
import math # 角度转弧度

class StaticTFBroadcaster(Node):
    def __init__(self):
        super().__init__('static_tf_broadcaster')
        self.static_broadcaster_ = StaticTransformBroadcaster(self) # 创建静态坐标发送器对象
        self.publish_static_tf() 

    def publish_static_tf(self):
        # 发布静态TF 从base_link到camera_link的坐标变换
        transform = TransformStamped()
        transform.header.frame_id = 'base_link' # 父坐标系
        transform.child_frame_id = 'camera_link' # 子坐标系
        transform.header.stamp = self.get_clock().now().to_msg() # 时间戳

        transform.transform.translation.x = 0.5
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.6

        # 将欧拉角转换为四元数 q=x, y, z, w
        q = quaternion_from_euler(math.radians(180),0,0) # 将角度转换为弧度
        # 旋转部分赋值
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]
        # 发布静态坐标变换
        self.static_broadcaster_.sendTransform(transform)
        self.get_logger().info(f'发布静态坐标变换: {transform}')


def main():
    rclpy.init()
    node = StaticTFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
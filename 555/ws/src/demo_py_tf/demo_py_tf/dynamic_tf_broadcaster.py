import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster # 坐标发送器
from geometry_msgs.msg import TransformStamped # 坐标变换消息类型
from tf_transformations import quaternion_from_euler # 欧拉角转四元数
import math # 角度转弧度

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.broadcaster_ = TransformBroadcaster(self) # 创建静态坐标发送器对象
        self.timer_ = self.create_timer(0.01,self.publish_tf) # 创建定时器，周期为0.01秒，回调函数为publish_tf

    def publish_tf(self):
        # 发布动态TF 从camera_link到bottle_link的坐标变换
        transform = TransformStamped()
        transform.header.frame_id = 'camera_link' # 父坐标系
        transform.child_frame_id = 'bottle_link' # 子坐标系
        transform.header.stamp = self.get_clock().now().to_msg() # 时间戳

        transform.transform.translation.x = 0.2
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.5

        # 将欧拉角转换为四元数 q=x, y, z, w
        q = quaternion_from_euler(0,0,0) # 将角度转换为弧度
        # 旋转部分赋值
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]
        # 发布动态坐标变换
        self.broadcaster_.sendTransform(transform)
        self.get_logger().info(f'发布TF坐标变换: {transform}')


def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
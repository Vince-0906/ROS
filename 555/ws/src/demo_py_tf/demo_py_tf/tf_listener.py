import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener,Buffer # 坐标监听器
from tf_transformations import euler_from_quaternion # 四元数转欧拉角
import math # 角度转弧度

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.buffer_ = Buffer() # 创建坐标变换缓存对象
        self.broadcaster_ = TransformListener(self.buffer_,self) # 创建静态坐标发送器对象
        self.timer_ = self.create_timer(1.0,self.get_transform) # 创建定时器，周期为1秒

    def get_transform(self):
        # 实时查询坐标关系
        try:
            result =self.buffer_.lookup_transform('base_link','bottle_link',rclpy.time.Time(seconds=0.0),rclpy.duration.Duration(seconds=1.0)) # 查询base_link到bottle_link的坐标变换
            transform = result.transform
            self.get_logger().info(f'平移:{transform.translation}')
            self.get_logger().info(f'旋转:{transform.rotation}')
            rotation_euler = euler_from_quaternion([
                transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w]) # 将四元数转换为欧拉角
            self.get_logger().info(f'旋转RPY:{rotation_euler}')

        except Exception as e:
            self.get_logger().warn(f'未查询到坐标变换，原因:{e}')


def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
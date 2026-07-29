import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 获取功能包share目录绝对路径
import os
from cv_bridge import CvBridge
import time

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        self.brige = CvBridge()
        self.default_image_path = os.path.join(get_package_share_directory('demo_py_service'), 'resource', 'default.jpeg')
        self.get_logger().info('人脸检测客户端已启动')

        self.client =self.create_client(FaceDetector,'face_detect')
        self.image =cv2.imread(self.default_image_path)


    def send_request(self):
        # 1.判断服务端是否在线
        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('服务端未启动，等待中...')

        # 2.构造请求
        request = FaceDetector.Request()
        request.image = self.brige.cv2_to_imgmsg(self.image)

        # 3.发送请求并等待处理完成
        future = self.client.call_async(request) # 现在的future并没有包含响应结果，需要等待服务端处理完成后才会把响应结果放入future中
        def result_callback(future):
            response = future.result() # 获取响应结果
            self.get_logger().info(f'接收到相应，共：{response.number}张人脸，耗时：{response.use_time:.4f}秒')
            self.show_response(response)
        future.add_done_callback(result_callback)
        # while not future.done():
            # time.sleep(1.0) # 休眠线程，等待服务端处理完成，造成当前线程无法再接受来自服务端的响应结果，导致永远无法获取响应结果，即future.done()永远为False
            # rclpy.spin_until_future_complete(self,future) # 让当前线程可以接受来自服务端的响应结果，直到服务端处理完成，future.done()为True


    def show_response(self,response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]
            cv2.rectangle(self.image,(left,top),(right,bottom),(255,0,0),4)

        cv2.imshow('Face Detection',self.image)
        cv2.waitKey(0) # 也是阻塞函数，会导致spin无法正常运行




def main():
    rclpy.init()
    node = FaceDetectClientNode()
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()
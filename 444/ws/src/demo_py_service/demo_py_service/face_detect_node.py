import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 获取功能包share目录绝对路径
import os
from cv_bridge import CvBridge
import time

class FaceDetectNode(Node):
    def __init__(self):
        super().__init__('face_detect_node')
        self.service_ = self.create_service(FaceDetector,'face_detect',self.detect_face_callback)
        self.brige = CvBridge()
        self.declare_parameter("number_of_times_to_upsample",1)
        self.declare_parameter("model",'hog')
        self.number_of_times_to_upsample = self.get_parameter('number_of_times_to_upsample').value
        self.model = self.get_parameter('model').value

        # self.number_of_times_to_upsample = 1
        # self.model = 'hog'
        self.default_image_path = os.path.join(get_package_share_directory('demo_py_service'), 'resource', 'default.jpeg')
        self.get_logger().info('人脸检测服务已启动，等待请求...')




    def detect_face_callback(self,request,response):
        # 判断图像
        if request.image.data:
            cv_image = self.brige.imgmsg_to_cv2(request.image)

        else:
            cv_image = cv2.imread(self.default_image_path)
            self.get_logger().info('传入图像为空，使用默认图像')


        start_time = time.time()
        self.get_logger().info('加载完图像，开始识别...')
        face_locations = face_recognition.face_locations(cv_image, number_of_times_to_upsample = self.number_of_times_to_upsample, model = self.model)


        response.use_time =time.time() - start_time
        response.number = len(face_locations)


        # 绘制人脸框
        for top,right,bottom,left in face_locations:
            response.top.append(top)
            response.right.append(right)
            response.bottom.append(bottom)
            response.left.append(left)


        return response #必须返回response对象



def main():
    rclpy.init()
    node = FaceDetectNode()
    rclpy.spin(node)
    rclpy.shutdown()


import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 获取功能包share目录绝对路径
import os
from cv_bridge import CvBridge
import time
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter,ParameterValue,ParameterType

class FaceDetectClientNode(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        self.brige = CvBridge()
        self.default_image_path = os.path.join(get_package_share_directory('demo_py_service'), 'resource', 'default.jpeg')
        self.get_logger().info('人脸检测客户端已启动')

        self.client =self.create_client(FaceDetector,'face_detect')
        self.image =cv2.imread(self.default_image_path)


    def call_set_parameters(self,parameters):
        '''
        调用设置参数服务
        :param parameters: 参数列表
        :return: 无
        '''
        # 1.判断服务端是否在线
        update_param =self.create_client(SetParameters,'/face_detect_node/set_parameters')
        while update_param.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('等待参数服务上线中...')
        # 2.构造request
        request = SetParameters.Request()
        request.parameters = parameters

        # 3.调用服务端更新指令
        future = update_param.call_async(request)
        rclpy.spin_until_future_complete(self,future) # 等待服务端返回响应
        response = future.result()
        return response

    def update_detect_model(self,model='hog'):
        '''
        根据传入的模型名称,构造Parameters对象,并调用call_set_parameters服务更新参数
        '''
        # 1.构造Parameters对象
        param = Parameter()
        param.name = 'model'

        # 2.创建param_value
        param_value = ParameterValue()
        param_value.string_value = model
        param_value.type = ParameterType.PARAMETER_STRING
        param.value = param_value

        # 3.请求更新参数
        response = self.call_set_parameters([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f"设置参数成功,参数名:{param.name},参数值:{model}")
                self.get_logger().info(f"设置参数结果: {result.successful}, {result.reason}")


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
            #self.show_response(response)
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
    node.update_detect_model('cnn') # cnn
    node.send_request()
    node.update_detect_model('hog') # hog
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()
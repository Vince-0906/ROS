import rclpy
import requests
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue


class NovelPublisher(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name} 启动.')
        self.novels_queue_ = Queue() # 创建一个队列对象，用于存储小说内容
        self.novel_publisher_ = self.create_publisher(String,'novel',10)
        self.create_timer(5.0, self.timer_callback)


    def timer_callback(self):
        if self.novels_queue_.qsize()>0: # 判断队列大小
            line =self.novels_queue_.get() # 从队列中取出一行
            msg = String() # 组装消息
            msg.data = line
            self.novel_publisher_.publish(msg) # 发布
            self.get_logger().info(f'发布: {msg}')
        # self.novel_publisher_.publish()
        

    def download(self, url):
        response =requests.get(url) # 请求
        response.encoding = 'utf-8' 
        text = response.text
        # text.splitlines()
        self.get_logger().info(f'下载小说 {url},{len(text)}')
        for line in text.splitlines(): # 按行分割
            self.novels_queue_.put(line) #放到队列
        # response.text  # 获取网页内容


def main():
    rclpy.init()
    node = NovelPublisher('novel_pub')
    node.download('http://0.0.0.0:8000/novel1.txt')
    rclpy.spin(node)
    rclpy.shutdown()
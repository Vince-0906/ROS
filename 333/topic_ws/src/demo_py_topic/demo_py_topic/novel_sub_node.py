import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class NovelSubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name} 启动.')
        self.novels_queue_ = Queue() # 创建一个队列对象，用于存储小说内容
        self.novel_subscriber_ =self.create_subscription(String,'novel',self.novel_callback,10)
        self.speech_thread_ =threading.Thread(target=self.speaker_thread)
        self.speech_thread_.start() # 启动线程


    def novel_callback(self,msg):
        self.novels_queue_.put(msg.data) #放到队列


    def speaker_thread(self):
        speaker = espeakng.Speaker()
        speaker.voice ='cmn-latn-pinyin'

        while rclpy.ok(): # 检测当前ROS当前上下文
            if self.novels_queue_.qsize()>0: # 判断队列大小
                text =self.novels_queue_.get() # 从队列中取出一行
                self.get_logger().info(f'朗读: {text}')
                speaker.say(text) # 朗读
                speaker.wait() # 等待朗读完成
            else:
                # 让当前线程休眠1s，避免CPU占用过高
                time.sleep(1)


def main():
    rclpy.init()
    node = NovelSubNode('novel_sub')
    rclpy.spin(node)
    rclpy.shutdown()
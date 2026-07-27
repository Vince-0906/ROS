import base64
import os
import numpy as np
import sounddevice as sd
from openai import OpenAI
from dotenv import load_dotenv

# import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time

# Load .env file from the source package directory
load_dotenv('/home/szc/ROS/333/topic_ws/src/demo_py_topic/.env')

class NovelSubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name} 启动.')
        self.novels_queue_ = Queue() # 创建一个队列对象，用于存储小说内容
        self.novel_subscriber_ =self.create_subscription(String,'novel',self.novel_callback,10)

        self.client_ = OpenAI(
            api_key=os.environ.get("MIMO_API_KEY"),
            base_url="https://token-plan-cn.xiaomimimo.com/v1"
        )


        self.speech_thread_ =threading.Thread(target=self.speaker_thread)
        self.speech_thread_.start() # 启动线程


    def novel_callback(self,msg):
        self.novels_queue_.put(msg.data) #放到队列


    def speaker_thread(self):
        # speaker = espeakng.Speaker()
        # speaker.voice ='cmn-latn-pinyin'

        while rclpy.ok(): # 检测当前ROS当前上下文
            if self.novels_queue_.qsize()>0: # 判断队列大小
                text =self.novels_queue_.get() # 从队列中取出一行
                self.get_logger().info(f'朗读: {text}')

                '''speaker.say(text) # 朗读
                speaker.wait() # 等待朗读完成
                '''


                try:
                    # 调用OpenAI TTS API，使用流式传输
                    completion = self.client_.chat.completions.create(
                        model="mimo-v2.5-tts",
                        messages=[
                            {
                                "role": "user",
                                "content": "请朗读以下内容"
                            },
                            {
                                "role": "assistant",
                                "content": text  # 要朗读的文本内容
                            }
                        ],
                        audio={
                            "format": "pcm16",  # 使用PCM16格式
                            "voice": "冰糖"    # 使用冰糖语音
                        },
                        stream=True  # 启用流式传输，边生成边播放
                    )

                    # 收集音频数据块，24kHz PCM16LE单声道音频
                    collected_chunks = np.array([], dtype=np.float32)

                    # 遍历流式返回的音频块
                    for chunk in completion:
                        if not chunk.choices:
                            continue
                        delta = chunk.choices[0].delta
                        audio = getattr(delta, "audio", None)

                        if audio is not None:
                            # 解码base64编码的PCM音频数据
                            pcm_bytes = base64.b64decode(audio["data"])
                            # 将PCM16数据转换为float32格式（归一化到[-1, 1]范围）
                            np_pcm = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                            # 拼接音频块
                            collected_chunks = np.concatenate((collected_chunks, np_pcm))

                    # 直接播放音频（24kHz采样率）
                    sd.play(collected_chunks, samplerate=24000)
                    sd.wait()  # 等待播放完成
                    self.get_logger().info('音频播放完成')

                except Exception as e:
                    self.get_logger().error(f'TTS生成失败: {str(e)}')

            else:
                # 让当前线程休眠1s，避免CPU占用过高
                time.sleep(1)


def main():
    rclpy.init()
    node = NovelSubNode('novel_sub')
    rclpy.spin(node)
    rclpy.shutdown()
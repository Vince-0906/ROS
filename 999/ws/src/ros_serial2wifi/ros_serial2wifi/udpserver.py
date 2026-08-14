#!/usr/bin/env python3

import os
import pty
import socket
import select
import subprocess
import rclpy
from rclpy.node import Node
import time

class UdpSocketServerNode(Node):
    def __init__(self):
        super().__init__('udp_socket_server_node')
        
        # 声明 ROS 2 参数
        self.declare_parameter('udp_port', 8889)
        self.declare_parameter('serial_port', '/tmp/laserport')
        
        # 获取 ROS 2 参数
        self.udp_port = self.get_parameter('udp_port').get_parameter_value().integer_value
        self.serial_port = self.get_parameter('serial_port').get_parameter_value().string_value

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', self.udp_port))
        
        master, slave = pty.openpty()
        if os.path.exists(self.serial_port):
            os.remove(self.serial_port)
        os.symlink(os.ttyname(slave), self.serial_port)

        self.get_logger().info(f"UDP端口:{self.udp_port}，已映射到串口设备:{self.serial_port}")
        mypoll = select.poll()
        mypoll.register(master, select.POLLIN)
        mypoll.register(s.fileno(), select.POLLIN)
        
        client_address = None
        last_exchange_data_time = time.time()
        
        try:
            while True:
                fdlist = mypoll.poll(256)
                for fd, event in fdlist:
                    if fd == master:
                        # 从串口读取数据发送到UDP客户端
                        if client_address:
                            data = os.read(master, 256)
                            if len(data) > 0:
                                s.sendto(data, client_address)
                                last_exchange_data_time = time.time()
                    elif fd == s.fileno():
                        # 从UDP客户端接收数据写入串口
                        try:
                            data, addr = s.recvfrom(256)
                            if len(data) > 0:
                                os.write(master, data)
                                client_address = addr
                                last_exchange_data_time = time.time()
                                self.get_logger().info(f'收到来自{addr}的数据')
                        except Exception as e:
                            self.get_logger().warn(f'UDP接收数据错误: {e}')
                
                # 如果一段时间没有任何数据则重置客户端地址
                if time.time() - last_exchange_data_time > 5:
                    if client_address:
                        self.get_logger().info('5秒无数据交换，重置客户端连接')
                        client_address = None
        finally:
            s.close()


def main():
    rclpy.init()
    node = UdpSocketServerNode()
    node.run()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

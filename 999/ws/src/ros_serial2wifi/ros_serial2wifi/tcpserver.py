#!/usr/bin/env python3

import os
import pty
import socket
import select
import subprocess
import rclpy
from rclpy.node import Node
import time

class TcpSocketServerNode(Node):
    def __init__(self):
        super().__init__('tcp_socket_server_node')
        
        # 声明 ROS 2 参数
        self.declare_parameter('tcp_port', 8889)
        self.declare_parameter('serial_port', '/tmp/laserport')
        
        # 获取 ROS 2 参数
        self.tcp_port = self.get_parameter('tcp_port').get_parameter_value().integer_value
        self.serial_port = self.get_parameter('serial_port').get_parameter_value().string_value

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', self.tcp_port))
        s.listen(1)
        
        master, slave = pty.openpty()
        if os.path.exists(self.serial_port):
            os.remove(self.serial_port)
        os.symlink(os.ttyname(slave), self.serial_port)

        self.get_logger().info(f"TCP端口:{self.tcp_port}，已映射到串口设备:{self.serial_port}")
        mypoll = select.poll()
        mypoll.register(master, select.POLLIN)
        try:
            while True:
                self.get_logger().info("等待接受连接..")
                s.settimeout(None)
                client, client_address = s.accept()
                mypoll.register(client.fileno(), select.POLLIN)
                self.get_logger().info(f'来自{client_address}的连接已建立')
                is_connect = True
                last_exchange_data_time = time.time()
                try:
                    while is_connect:
                        fdlist = mypoll.poll(256)
                        for fd, event in fdlist:
                            last_exchange_data_time = time.time()
                            data = os.read(fd, 256)
                            write_fd = client.fileno() if fd == master else master
                            if len(data) == 0:
                                is_connect = False
                                break
                            # print(write_fd,data,event)
                            os.write(write_fd, data)
                        # 如果一段时间没有任何数据则断开连接
                        if time.time()-last_exchange_data_time>5:
                            is_connect = False
                            print('5s no data.')
                            break
                except Exception:
                    is_connect = False
                finally:
                    mypoll.unregister(client.fileno())
                    client.close()
        finally:
            s.close()


def main():
    rclpy.init()
    node = TcpSocketServerNode()
    node.run()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

from demo_py_pkg.person_node import PersonNode
import rclpy
from rclpy.node import Node

class CoderNode(PersonNode):
    def __init__(self, node_name: str, name_value: str, age_value: int, code_value: str) -> None:
        print('CoderNode__init__被调用了')
        super().__init__(node_name, name_value, age_value) #调用父类的构造函数
        self.code = code_value
    def coder(self):
        pass

def main():
    rclpy.init()
    node = CoderNode('node_Cindy','Cindy','66','Python')
    node.eat('面包')
    print(f'爱写{node.code}代码')
    rclpy.spin(node)
    rclpy.shutdown()
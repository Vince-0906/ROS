import rclpy
from rclpy.node import Node
class PersonNode(Node):
    def __init__(self, node_name: str, name_value: str, age_value: int) -> None:
        print('PersonNode__init__被调用了')
        super().__init__(node_name)
        self.name = name_value
        self.age = age_value
    def eat(self,food_name: str):
        """
        方法：吃东西
        :food_name 参数：食物名称
        """
        #print(f'{self.name} ,{self.age}岁，爱吃{food_name}')
        self.get_logger().info(f'{self.name} ,{self.age}岁，爱吃{food_name}')

def main():
    rclpy.init()
    node = PersonNode('node_Vince','Vince', 22)
    node.eat('芒果')
    rclpy.spin(node)
    rclpy.shutdown()
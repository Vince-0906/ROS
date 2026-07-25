from demo_py_pkg.person_node import PersonNode

class CoderNode(PersonNode):
    def __init__(self, name_value: str, age_value: int, code_value: str) -> None:
        print('CoderNode__init__被调用了')
        super().__init__(name_value,age_value) #调用父类的构造函数
        self.code = code_value
    def coder(sele):
        pass

def main():
    node = CoderNode('Cindy','66','Python')
    node.eat('面包')
    print(f'爱写{node.code}代码')
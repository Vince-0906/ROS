---
tags:
  - cpp
  - ROS2
---
> 📂 **配套代码**：[`222/ws/src/demo_cpp_pkg/src/`](../../222/ws/src/demo_cpp_pkg/src)

## 1. 基础语法结构

### 1.1 程序入口
```cpp
int main(int argc, char **argv) {
    // 程序从这里开始执行
    return 0;  // 返回0表示正常退出
}
```

### 1.2 注释
```cpp
// 单行注释

/* 
   多行注释
   可以写很多行
*/
```

### 1.3 变量声明
```cpp
int age = 25;           // 整数
double price = 19.99;   // 浮点数
std::string name = "ROS2";  // 字符串（需要 #include <string>）
bool is_ready = true;   // 布尔值
auto count = 10;        // auto让编译器自动推断类型（这里是int）
```

---

## 2. 常用符号速查

| 符号   | 含义        | 示例                            |
| ---- | --------- | ----------------------------- |
| `::` | 作用域解析运算符  | `std::cout`, `rclcpp::Node`   |
| `->` | 通过指针访问成员  | `node->get_name()`            |
| `.`  | 通过对象访问成员  | `msg.data = 10`               |
| `&`  | 引用 / 取地址  | `int& ref = x;` 或 `&variable` |
| `*`  | 指针 / 解引用  | `int* ptr;` 或 `*ptr = 5`      |
| `<<` | 流插入运算符    | `std::cout << "Hello"`        |
| `>>` | 流提取运算符    | `std::cin >> input`           |
| `[]` | 数组/容器索引   | `array[0]`, `vec[i]`          |
| `()` | 函数调用      | `func(arg1, arg2)`            |
| `{}` | 初始化列表     | `std::vector<int> v{1,2,3}`   |
| `//` | Lambda表达式 | `[&](){ code }`               |

---

## 3. 指针和引用 ⭐ 重点

### 3.1 指针 `*`
```cpp
int value = 42;
int* ptr = &value;   // ptr存储value的地址
*ptr = 100;          // 通过指针修改value的值

// ROS2中常见：
rclcpp::Node::SharedPtr node;  // 智能指针（后面会讲）
```

### 3.2 引用 `&`
```cpp
int original = 10;
int& ref = original;  // ref是original的别名
ref = 20;             // 修改ref就是修改original

// ROS2回调中常见：
void callback(const std_msgs::msg::String::SharedPtr msg) {
    // msg是智能指针，通过->访问成员
    std::cout << msg->data << std::endl;
}
```

**关键区别**：
- 指针可以重新指向别的地址，引用不能
- 指针可以为空（`nullptr`），引用必须绑定到有效对象
- 使用指针用`->`，使用引用用`.`

---

## 4. 命名空间 `::`

### 4.1 什么是命名空间
防止名字冲突的机制，像是给代码分类。

```cpp
// 使用标准库的cout
std::cout << "Hello" << std::endl;

// 使用ROS2的初始化函数
rclcpp::init(argc, argv);

// 使用消息类型
std_msgs::msg::String message;
```

### 4.2 常见写法
```cpp
// 方式1：每次都写完整路径（推荐）
std::vector<int> numbers;

// 方式2：using声明（简化单个名字）
using std::cout;
cout << "Hello" << std::endl;

// 方式3：using namespace（不推荐，容易冲突）
using namespace std;
vector<int> numbers;  // 不用写std::了
```

**ROS2中常见命名空间**：
- `rclcpp::` - ROS2 C++库
- `std_msgs::msg::` - 标准消息类型
- `sensor_msgs::msg::` - 传感器消息
- `geometry_msgs::msg::` - 几何消息

---

## 5. 类和对象基础

### 5.1 类的定义
```cpp
class MyNode : public rclcpp::Node {  // 继承自Node类
public:
    // 构造函数
    MyNode() : Node("my_node_name") {
        // 初始化代码
    }
    
    // 成员函数
    void do_something() {
        RCLCPP_INFO(this->get_logger(), "Doing something");
    }

private:
    // 成员变量
    int counter_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
};
```

### 5.2 创建对象
```cpp
// 方式1：栈上创建
MyNode node;

// 方式2：堆上创建（ROS2常用）
auto node = std::make_shared<MyNode>();

// 方式3：指针
MyNode* node_ptr = new MyNode();
delete node_ptr;  // 记得释放！但ROS2一般用智能指针，不用手动delete
```

### 5.3 this 关键字
```cpp
class Example {
public:
    void method() {
        this->member_ = 10;  // this是指向当前对象的指针
        // 等价于：member_ = 10;
    }
private:
    int member_;
};
```

---

## 6. 智能指针 ⭐ ROS2 核心

ROS2大量使用智能指针，自动管理内存，不用手动`delete`。

### 6.1 `std::shared_ptr`
```cpp
// 创建共享指针
auto node = std::make_shared<rclcpp::Node>("node_name");

// 多个指针可以指向同一个对象
std::shared_ptr<MyClass> ptr1 = std::make_shared<MyClass>();
std::shared_ptr<MyClass> ptr2 = ptr1;  // 引用计数+1

// 访问成员
ptr1->method();

// ROS2中的类型别名
rclcpp::Node::SharedPtr node;  // 等价于 std::shared_ptr<rclcpp::Node>
```

### 6.2 为什么ROS2用智能指针
```cpp
// 发布者
publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
//           ↑ 返回的是 SharedPtr

// 订阅回调
void callback(const std_msgs::msg::String::SharedPtr msg) {
    // msg会自动管理生命周期
}
```

---

## 7. STL 容器（标准库）

### 7.1 `std::vector` 动态数组
```cpp
#include <vector>

std::vector<int> numbers;       // 空vector
std::vector<int> nums{1,2,3};   // 初始化

numbers.push_back(10);          // 添加元素
int first = numbers[0];         // 访问元素
int size = numbers.size();      // 获取大小

// 遍历
for (int num : numbers) {       // 范围for循环
    std::cout << num << std::endl;
}
```

### 7.2 `std::string` 字符串
```cpp
#include <string>

std::string text = "Hello ROS2";
text += " World";               // 拼接
int len = text.length();        // 长度
std::string sub = text.substr(0, 5);  // 子串 "Hello"

// ROS2消息中常用
std_msgs::msg::String msg;
msg.data = "Hello";
```

### 7.3 `std::map` 键值对
```cpp
#include <map>

std::map<std::string, int> ages;
ages["Alice"] = 25;
ages["Bob"] = 30;

if (ages.find("Alice") != ages.end()) {
    std::cout << ages["Alice"] << std::endl;
}
```

---

## 8. Lambda 表达式 ⭐ ROS2 回调必备

Lambda是匿名函数，ROS2定时器和回调经常用。

### 8.1 基本语法
```cpp
[捕获列表](参数列表) { 函数体 }

// 示例
auto add = [](int a, int b) { return a + b; };
int result = add(3, 5);  // 8
```

### 8.2 捕获列表
```cpp
int x = 10;

[x]() { /* 按值捕获x，内部是副本 */ }
[&x]() { /* 按引用捕获x，可以修改 */ }
[&]() { /* 按引用捕获所有外部变量 */ }
[=]() { /* 按值捕获所有外部变量 */ }
[this]() { /* 捕获当前对象指针 */ }
```

### 8.3 ROS2 实战示例
```cpp
// 定时器回调
timer_ = this->create_wall_timer(
    std::chrono::seconds(1),
    [this]() {  // 捕获this指针
        auto msg = std_msgs::msg::String();
        msg.data = "Hello";
        publisher_->publish(msg);
    }
);

// 订阅回调
subscription_ = this->create_subscription<std_msgs::msg::String>(
    "topic",
    10,
    [this](const std_msgs::msg::String::SharedPtr msg) {
        RCLCPP_INFO(this->get_logger(), "Received: %s", msg->data.c_str());
    }
);
```

---

## 9. 函数相关

### 9.1 函数声明和定义
```cpp
// 声明（通常在.hpp头文件）
int add(int a, int b);

// 定义（通常在.cpp源文件）
int add(int a, int b) {
    return a + b;
}

// 也可以合二为一
int multiply(int a, int b) {
    return a * b;
}
```

### 9.2 参数传递方式
```cpp
// 按值传递（复制一份，函数内修改不影响外部）
void func1(int x) {
    x = 100;
}

// 按引用传递（可以修改原变量）
void func2(int& x) {
    x = 100;  // 会修改外部变量
}

// 常量引用（只读，不能修改，但避免复制，效率高）
void func3(const std::string& text) {
    // text = "new";  // 错误！不能修改
    std::cout << text << std::endl;  // 可以读取
}

// ROS2中常见：
void callback(const std_msgs::msg::String::SharedPtr msg) {
    // 常量智能指针，不能修改指针本身，但可以读取内容
}
```

### 9.3 默认参数
```cpp
void greet(std::string name = "World") {
    std::cout << "Hello, " << name << std::endl;
}

greet();           // 输出：Hello, World
greet("ROS2");     // 输出：Hello, ROS2
```

---

## 10. 模板 `<>` —— 泛型编程

模板让代码可以适用于多种类型，ROS2消息类型大量使用。

### 10.1 什么是模板
```cpp
// 不用模板，需要为每种类型写一遍
int max_int(int a, int b) { return a > b ? a : b; }
double max_double(double a, double b) { return a > b ? a : b; }

// 用模板，一次搞定
template<typename T>
T max_value(T a, T b) {
    return a > b ? a : b;
}

// 使用
int result1 = max_value<int>(3, 5);
double result2 = max_value<double>(3.5, 2.1);
auto result3 = max_value(10, 20);  // 自动推断类型
```

### 10.2 ROS2 中的模板应用
```cpp
// 发布者模板：指定消息类型
auto pub = node->create_publisher<std_msgs::msg::String>("topic", 10);
//                                 ↑ 模板参数，指定发布String类型

// 订阅者模板
auto sub = node->create_subscription<std_msgs::msg::Int32>(
    "topic", 10, callback
);

// 不同消息类型就换模板参数
auto imu_sub = node->create_subscription<sensor_msgs::msg::Imu>(
    "imu_topic", 10, imu_callback
);
```

---

## 11. 常用操作符

### 11.1 三元运算符 `? :`
```cpp
int age = 20;
std::string status = (age >= 18) ? "Adult" : "Minor";
// 等价于：
// if (age >= 18) status = "Adult";
// else status = "Minor";
```

### 11.2 逻辑运算符
```cpp
bool a = true, b = false;

a && b   // 逻辑与（AND）
a || b   // 逻辑或（OR）
!a       // 逻辑非（NOT）

// 短路求值
if (ptr != nullptr && ptr->value > 0) {
    // 如果ptr是空指针，不会执行ptr->value（避免崩溃）
}
```

### 11.3 自增自减
```cpp
int i = 5;
i++;     // 后自增：先用再加，i变成6
++i;     // 前自增：先加再用，i变成7
i--;     // 后自减
--i;     // 前自减

// 循环中常用
for (int i = 0; i < 10; i++) {
    // ...
}
```

---

## 12. 控制流

### 12.1 if-else
```cpp
if (condition) {
    // 条件为真执行
} else if (another_condition) {
    // 另一个条件
} else {
    // 都不满足
}
```

### 12.2 for 循环
```cpp
// 传统for循环
for (int i = 0; i < 10; i++) {
    std::cout << i << std::endl;
}

// 范围for循环（推荐，简洁）
std::vector<int> nums{1, 2, 3, 4, 5};
for (int num : nums) {
    std::cout << num << std::endl;
}

// 引用方式（可以修改元素）
for (int& num : nums) {
    num *= 2;  // 每个元素乘以2
}

// 常量引用（只读，效率高）
for (const auto& item : large_vector) {
    // 处理item，不复制
}
```

### 12.3 while 循环
```cpp
while (condition) {
    // 循环体
}

// ROS2常见：
while (rclcpp::ok()) {
    rclcpp::spin_some(node);
    // 其他处理
}
```

---

## 13. 头文件和包含

### 13.1 `#include` 指令
```cpp
// 标准库用<>
#include <iostream>
#include <vector>
#include <string>

// 自己的头文件用""
#include "my_header.hpp"

// ROS2头文件
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "geometry_msgs/msg/twist.hpp"
```

### 13.2 常用ROS2头文件
```cpp
#include "rclcpp/rclcpp.hpp"           // ROS2核心库
#include "std_msgs/msg/string.hpp"    // String消息
#include "std_msgs/msg/int32.hpp"     // Int32消息
#include "sensor_msgs/msg/image.hpp"  // 图像消息
#include "geometry_msgs/msg/twist.hpp" // 速度控制消息
```

---

## 14. const 关键字 ⭐ 重要

### 14.1 常量变量
```cpp
const int MAX_SIZE = 100;  // 不能修改
// MAX_SIZE = 200;  // 错误！
```

### 14.2 常量指针
```cpp
const int* ptr1;        // 指向常量的指针（不能通过ptr1修改值）
int* const ptr2;        // 常量指针（不能改变指向）
const int* const ptr3;  // 两者都是常量
```

### 14.3 常量引用
```cpp
void process(const std::string& text) {
    // text不能被修改，但避免了复制，效率高
}

// ROS2回调常见模式
void callback(const std_msgs::msg::String::SharedPtr msg) {
    // msg内容不应该被修改
}
```

### 14.4 常量成员函数
```cpp
class MyClass {
public:
    int get_value() const {  // const表示不会修改成员变量
        return value_;
    }
private:
    int value_;
};
```

---

## 15. auto 关键字 —— 自动类型推导

```cpp
auto x = 10;              // 推导为int
auto y = 3.14;            // 推导为double
auto name = "ROS2";       // 推导为const char*
auto text = std::string("Hello");  // 推导为std::string

// ROS2中大量使用，简化长类型名
auto node = std::make_shared<rclcpp::Node>("node_name");
// 不用写：std::shared_ptr<rclcpp::Node> node = ...

auto pub = node->create_publisher<std_msgs::msg::String>("topic", 10);
// 不用写：rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub = ...

// 范围for中也常用
for (const auto& item : container) {
    // auto自动推导item类型
}
```

**何时用auto**：
- ✅ 类型名很长时（智能指针、迭代器）
- ✅ 类型明显时（`= new MyClass()`）
- ❌ 类型不明显时（可读性降低）

---

## 16. ROS2 特有概念速查

### 16.1 常见ROS2代码模式
```cpp
// 1. 初始化ROS2
rclcpp::init(argc, argv);

// 2. 创建节点
auto node = std::make_shared<rclcpp::Node>("node_name");

// 3. 创建发布者
auto pub = node->create_publisher<std_msgs::msg::String>("topic_name", 10);

// 4. 创建订阅者
auto sub = node->create_subscription<std_msgs::msg::String>(
    "topic_name",
    10,
    [](const std_msgs::msg::String::SharedPtr msg) {
        // 回调处理
    }
);

// 5. 创建定时器
auto timer = node->create_wall_timer(
    std::chrono::milliseconds(500),
    []() {
        // 定时执行
    }
);

// 6. 启动循环
rclcpp::spin(node);

// 7. 关闭ROS2
rclcpp::shutdown();
```

### 16.2 日志输出
```cpp
RCLCPP_DEBUG(node->get_logger(), "Debug message");
RCLCPP_INFO(node->get_logger(), "Info message");
RCLCPP_WARN(node->get_logger(), "Warning message");
RCLCPP_ERROR(node->get_logger(), "Error message");

// 带参数
RCLCPP_INFO(node->get_logger(), "Value is: %d", value);
RCLCPP_INFO(node->get_logger(), "String is: %s", text.c_str());
```

---

## 17. 常见错误和解决

### 17.1 忘记分号
```cpp
int x = 10  // 错误！缺少分号
int y = 20;
```

### 17.2 混淆 `.` 和 `->`
```cpp
MyClass obj;
obj.method();      // 对象用 .

MyClass* ptr = &obj;
ptr->method();     // 指针用 ->

// 智能指针也用 ->
auto node = std::make_shared<rclcpp::Node>("name");
node->get_logger();  // 用 ->
```

### 17.3 字符串转C风格字符串
```cpp
std::string text = "Hello";

// 错误：printf需要C风格字符串
// printf("%s", text);

// 正确：
printf("%s", text.c_str());

// 或者用C++风格：
std::cout << text << std::endl;
```

### 17.4 引用未初始化
```cpp
int& ref;  // 错误！引用必须初始化
int x = 10;
int& ref = x;  // 正确
```

---

## 18. 实战：完整的ROS2节点示例

```cpp
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <chrono>

using namespace std::chrono_literals;  // 使用时间字面量如1s, 500ms

class MinimalPublisher : public rclcpp::Node {
public:
    MinimalPublisher() : Node("minimal_publisher"), count_(0) {
        // 创建发布者
        publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
        
        // 创建定时器，每500ms执行一次
        timer_ = this->create_wall_timer(
            500ms,
            [this]() { this->timer_callback(); }  // Lambda捕获this
        );
    }

private:
    void timer_callback() {
        auto message = std_msgs::msg::String();
        message.data = "Hello, world! " + std::to_string(count_++);
        
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
        publisher_->publish(message);
    }

    // 成员变量
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    size_t count_;
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MinimalPublisher>());
    rclcpp::shutdown();
    return 0;
}
```

**代码解析**：
1. `using namespace std::chrono_literals;` - 允许用`500ms`这种写法
2. `: Node("minimal_publisher"), count_(0)` - 构造函数初始化列表
3. `[this]()` - Lambda捕获当前对象
4. `std::to_string()` - 数字转字符串
5. `message.data.c_str()` - string转C风格字符串用于printf风格输出

---

## 19. 学习建议

### 📚 学习路径
1. **先抄代码运行** - 看到能跑起来，建立信心
2. **逐行理解** - 每个符号都查本文档，不懂就问
3. **小改动实验** - 改个变量名、改个数字，看看效果
4. **写注释** - 把理解写成中文注释
5. **自己写** - 模仿例子写个新功能

### 🔧 调试技巧
```cpp
// 多用日志输出
RCLCPP_INFO(node->get_logger(), "Variable x = %d", x);

// 检查指针是否为空
if (ptr != nullptr) {
    ptr->method();
}

// 捕获异常
try {
    // 可能出错的代码
} catch (const std::exception& e) {
    RCLCPP_ERROR(node->get_logger(), "Error: %s", e.what());
}
```

### 📖 重点记忆
- `::` 作用域，`->` 指针，`.` 对象
- Lambda `[捕获](参数){代码}`
- 智能指针 `std::shared_ptr` 自动管理内存
- `const &` 常量引用，高效且安全
- `auto` 自动推导类型
- 模板 `<类型>` 用于泛型

---

## 20. 快速查询表

### 类型大小（参考，可能因平台而异）
| 类型 | 大小 | 范围 |
|------|------|------|
| `bool` | 1字节 | true/false |
| `char` | 1字节 | -128到127 |
| `int` | 4字节 | -2^31到2^31-1 |
| `long` | 4/8字节 | 取决于平台 |
| `float` | 4字节 | 约7位小数精度 |
| `double` | 8字节 | 约15位小数精度 |

### 字符串操作
```cpp
std::string s = "Hello";
s.length()           // 长度
s.empty()            // 是否为空
s.substr(0, 3)       // 子串 "Hel"
s.find("ll")         // 查找位置，返回2
s += " World"        // 拼接
s.c_str()            // 转C风格字符串
```

### 容器操作
```cpp
std::vector<int> v;
v.push_back(10)      // 添加元素
v.size()             // 大小
v.empty()            // 是否为空
v.clear()            // 清空
v[0]                 // 访问元素（不检查边界）
v.at(0)              // 访问元素（检查边界，越界抛异常）
```

---

## 总结

C++看起来符号多，但在ROS2中常用的就这些：
- **指针和引用** - 理解 `*`、`&`、`->`
- **智能指针** - `std::shared_ptr` 和 `make_shared`
- **Lambda表达式** - `[捕获](参数){代码}`，用于回调
- **模板** - `<消息类型>`，指定发布/订阅的数据类型
- **命名空间** - `rclcpp::`、`std::`，代码分类
- **auto** - 自动类型推导，简化代码

**记住**：不用一次全学会，遇到不懂的符号就回来查这个文档，写几个ROS2节点就熟了！

---

📑 [返回笔记索引](../../README.md#笔记索引)

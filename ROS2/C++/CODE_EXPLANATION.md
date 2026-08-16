---
tags:
  - cpp
  - ROS2
---
> 📂 **配套代码**：[`444/ws/src/demo_cpp_service/src/turtle_control.cpp`](../../444/ws/src/demo_cpp_service/src/turtle_control.cpp) · [`444/ws/src/demo_cpp_service/src/patrol_client.cpp`](../../444/ws/src/demo_cpp_service/src/patrol_client.cpp) · [`444/ws/src/chapt4_interfaces/srv/Patrol.srv`](../../444/ws/src/chapt4_interfaces/srv/Patrol.srv)

# 逐行详解：`turtle_control.cpp` 与 `patrol_client.cpp`

> 面向 C++ 基础较弱的读者。每个语法点第一次出现时都会讲解：**它是什么语法、为什么要这么写**。常用的 ROS 2 套路会单独总结成可以直接套用的模板。

---

## 目录

- [0. 整体架构：这两个程序合起来在干什么](#0-整体架构)
- [1. 预备知识：读懂代码必须先懂的 C++ 概念](#1-预备知识)
- [2. `turtle_control.cpp` 逐段详解（服务端/控制器）](#2-turtle_controlcpp-逐段详解)
- [3. `patrol_client.cpp` 逐段详解（客户端）](#3-patrol_clientcpp-逐段详解)
- [4. 运行起来会发生什么](#4-运行起来会发生什么)
- [5. ROS 2 常用代码模板（可直接抄）](#5-ros-2-常用代码模板)
- [6. C++ 语法速查表](#6-c-语法速查表)

---

## 0. 整体架构

这两个文件是一个 **ROS 2**（Robot Operating System 2，机器人操作系统）示例，控制 `turtlesim` 模拟器里的小乌龟：

```
┌──────────────────┐  服务请求："去 (x,y) 巡逻"  ┌──────────────────┐
│                  │ ─────────────────────────►  │                  │
│  patrol_client   │ ◄─────────────────────────  │  turtle_control  │
│   （客户端）      │  服务响应：SUCCESS / FAIL    │  （服务端+控制器）│
│                  │                             │                  │
└──────┬───────────┘                             └───────┬──────────┘
       │ 启动时还会远程把服务端的                          │ 持续发布速度指令
       │ 参数 k 改成 4.0                                  ▼
       └────────────────────────────────────►    ┌──────────────┐
          （调用 /turtle_control/set_parameters） │  turtlesim   │
                                                 │  （小乌龟）   │
                                                 └──────────────┘
```

- **`turtle_control.cpp`** —— 乌龟的"大脑"。它不停地接收乌龟当前位置，和目标点比较，算出速度指令发出去，让乌龟朝目标开。同时它开了一个叫 `patrol` 的**服务**，允许别人给它换目标点；还声明了两个可调**参数** `k`（加速力度）和 `max_speed`（限速）。
- **`patrol_client.cpp`** —— "指挥官"。每 5 秒随机选一个点，调用 `patrol` 服务让乌龟去那里；程序刚启动时还会远程把服务端的参数 `k` 改成 4.0。

### ROS 2 三种通信方式（本例全用到了）

| 通信方式 | 生活类比 | 特点 | 本例中的用途 |
|---|---|---|---|
| **话题 Topic**（发布/订阅） | 广播电台：一方不停播，谁想听谁听 | 单向、持续、一对多 | 乌龟位置 `turtle1/pose`、速度指令 `turtle1/cmd_vel` |
| **服务 Service**（请求/响应） | 打电话：问一句，答一句 | 双向、一次性、一对一 | 发送巡逻目标点，收到成功/失败 |
| **参数 Parameter** | 设备上的旋钮 | 可运行中读写的配置项 | 调节 `k` 和 `max_speed` |

**怎么选？** 传感器数据这种"源源不断的流"用话题；"办一件事要个结果"用服务；"可调的配置"用参数。这是 ROS 2 设计的基本功。

---

## 1. 预备知识

读懂这两个文件，必须先弄懂下面几个 C++ 概念。**这一节值得反复看。**

### 1.1 类与继承：`class TurtleControl : public rclcpp::Node`

```cpp
class TurtleControl : public rclcpp::Node
```

- **类（class）**：把"数据（成员变量）"和"操作数据的函数（成员函数）"打包在一起的蓝图。
- **`: public rclcpp::Node`** 是**继承**语法，读作"TurtleControl **是一种** Node"。子类自动获得父类的全部能力。`rclcpp::Node` 是 ROS 2 提供的节点基类，自带 `create_publisher`、`create_service`、`get_logger`、`declare_parameter` 等几十个函数——所以我们的代码里能直接调用它们，**根本不用自己写**。
- **为什么这么写？** 这是 ROS 2 C++ 的标准写法：写一个节点 = 写一个继承 `rclcpp::Node` 的类。好处是所有初始化都收拢在构造函数里，成员变量天然被所有回调共享。

**`::` 是"里面的"**：`rclcpp::Node` 读作"rclcpp 命名空间里的 Node"。命名空间（namespace）就是给名字加"姓氏"避免重名，好比"ROS家的Node"和"别人家的Node"不冲突。

### 1.2 智能指针 `shared_ptr` —— 本例最重要的概念

普通变量存的是值本身；**指针**存的是对象的**内存地址**（"它在哪"）。C 语言时代要手动 `new`/`delete` 管理内存，忘了 delete 就内存泄漏。C++ 的解决方案是**智能指针**：

```cpp
std::shared_ptr<Foo> p = std::make_shared<Foo>(参数);  // 创建对象，交给智能指针管
```

- `shared_ptr`（共享指针）内部有个**引用计数**：记录当前有几个指针指向这个对象。最后一个指针消失时，对象**自动销毁**。你永远不用写 `delete`。
- ROS 2 里几乎所有东西都用它。每个 ROS 类型都自带别名：`X::SharedPtr` 就是 `std::shared_ptr<X>` 的简写。比如：

```cpp
rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
//  ↑ 类型：指向"Twist消息发布者"的共享指针        ↑ 变量名
```

- **为什么创建的发布者/订阅者/服务/定时器都必须存到成员变量里？** 因为 `create_xxx()` 返回的是 shared_ptr，如果不接住它，函数一结束指针就消失，引用计数归零，**刚创建的发布者立刻被销毁**，等于白建。这是 ROS 2 新手最常见的 bug：订阅者建了却收不到消息，就是忘了存句柄。

**`->` 和 `.` 的区别**：通过指针访问成员用 `->`（如 `pose->x`、`request->target_x`）；通过对象本身访问用 `.`（如 `msg.linear.x`）。功能完全一样，只看左边是不是指针。

### 1.3 模板：尖括号 `<>` 里填类型

```cpp
rclcpp::Client<Patrol>       // "专门发 Patrol 请求的客户端"
rclcpp::Publisher<Twist>     // "专门发 Twist 消息的发布者"
std::vector<double>          // "装 double 的动态数组"
```

**模板（template）** 是"类型的填空题"：ROS 只写了一份通用的 `Publisher` 代码，你在 `<>` 里填上消息类型，编译器就生成专用版本。**为什么这么设计？** 填了类型之后，编译器能在**编译期**就检查你发的消息类型对不对——发错类型直接编译报错，而不是运行时才炸。

### 1.4 Lambda 表达式（匿名函数）—— 回调的标准写法

本例大量出现这种结构：

```cpp
[&](参数列表) -> 返回类型 {
    函数体
}
```

拆解：

| 部分        | 含义                                                                               |
| --------- | -------------------------------------------------------------------------------- |
| `[&]`     | **捕获列表**：`&` 表示"函数体里可以**按引用**使用外面的变量"（包括 `this`，所以能访问 `k_`、`patrol_client_` 等成员） |
| `(参数)`    | 和普通函数的参数一样                                                                       |
| `-> void` | 返回类型（可省略，编译器能推断）                                                                 |
| `{...}`   | 函数体                                                                              |

**它是什么？** 一个**没有名字、写在原地**的函数。

**为什么用它？** 因为 ROS 2 是**事件驱动**的：你不能"主动等消息"，而是把一个函数**交给** ROS，说"事情发生时你来调我这个函数"——这种函数叫**回调（callback）**。回调往往很短、只在一个地方用，专门起名定义一个函数太啰嗦，lambda 就地写最顺手。

> 捕获列表小知识：`[&]` 按引用捕获（用的是外面变量本尊），`[=]` 按值捕获（拷贝一份），`[this]` 只捕获 this 指针。类的成员回调里 `[&]` 和 `[this]` 效果基本一样。教程代码常用 `[&]` 图省事。

### 1.5 `auto`：让编译器帮你写类型

```cpp
auto request = std::make_shared<Patrol::Request>();
// 等价于 std::shared_ptr<Patrol::Request> request = ...
```

`auto` 表示"类型你（编译器）自己推断"。**为什么用？** ROS 2 的类型名动辄五六十个字符，`auto` 大幅减少噪音。注意它不是"动态类型"——类型在编译期就定死了，只是不用你手写。

### 1.6 引用参数 `const std::string &name`

```cpp
TurtleControl(const std::string &node_name)
```

- `&` 表示**引用传递**：直接使用调用者的那个字符串，**不拷贝**（拷贝字符串有开销）。
- `const` 是承诺："我只读，不改"。
- **模板记忆**：函数参数想"高效只读地传对象"，就写 `const 类型 &`。这是 C++ 最常用的参数写法，本例的 `const rcl_interfaces::msg::Parameter &param`、范围 for 里的 `const auto & parameter` 都是它。

### 1.7 构造函数与初始化列表

```cpp
TurtleControl(const std::string &node_name) : Node(node_name)
{ ... }
```

- **构造函数**：与类同名、无返回类型的特殊函数，对象创建时**自动执行一次**，负责所有初始化。
- 冒号后面的 `Node(node_name)` 叫**成员初始化列表**，作用是"在进入函数体之前，先用这个名字构造父类"。**为什么必须写？** `rclcpp::Node` 没有无参构造函数，必须给它节点名；节点名是这个节点在 ROS 网络里的身份证（后面 main 里传入 `"turtle_control"`）。

---

## 2. `turtle_control.cpp` 逐段详解

### 2.1 头文件（第 1–6 行）

```cpp
#include <rclcpp/rclcpp.hpp>                            // ROS 2 C++ 核心库（rclcpp = ROS Client Library for C++）
#include <geometry_msgs/msg/twist.hpp>                  // Twist 消息：线速度+角速度，控制运动的标准消息
#include <chrono>                                       // C++ 标准时间库，提供 1s、500ms 这类写法
#include <turtlesim/msg/pose.hpp>                       // Pose 消息：乌龟的 x、y 坐标和朝向角 theta
#include <chapt4_interfaces/srv/patrol.hpp>             // 我们自定义的 Patrol 服务（在 chapt4_interfaces 功能包里定义）
#include <rcl_interfaces/msg/set_parameters_result.hpp> // "参数设置结果"消息，参数回调要返回它
```

`#include` 就是"把这个文件里的声明复制进来，让我能用它的类型和函数"。**规律**：ROS 2 里消息头文件路径 = `功能包名/msg/消息名（小写下划线）.hpp`，服务是 `功能包名/srv/服务名.hpp`。比如消息类型 `geometry_msgs::msg::Twist` 对应 `<geometry_msgs/msg/twist.hpp>` —— 记住这个映射规律，以后想用什么消息自己就能写出 include。

顺带说自定义服务：`Patrol.srv` 文件大概长这样（`---` 上面是请求，下面是响应）：

```
float32 target_x    # 请求：目标点坐标
float32 target_y
---
int8 SUCCESS=1      # 定义常量
int8 FAIL=0
int8 result         # 响应：结果
```

ROS 2 构建时会把它自动生成为 C++ 类，于是就有了代码里的 `Patrol::Request`、`Patrol::Response`、`Patrol::Response::SUCCESS` 这些名字。

### 2.2 类型别名（第 9–13 行）

```cpp
using Patrol = chapt4_interfaces::srv::Patrol;
using SetParametersResult = rcl_interfaces::msg::SetParametersResult;
using namespace std::chrono_literals;
```

- `using 新名字 = 老名字;` 起**别名**，纯粹为了少打字，不影响任何行为。ROS 2 代码开头几乎必有几行这个。
- `using namespace std::chrono_literals;` 启用**时间字面量**：之后才能写 `5s`（5秒）、`1s`。没有这行，`create_wall_timer(5s, ...)` 会编译报错。这是 ROS 2 定时器代码的标配。

### 2.3 成员变量（第 17–25 行）

```cpp
private:
    OnSetParametersCallbackHandle::SharedPtr parameter_callback_handle_; // 参数回调的"注册凭据"
    rclcpp::Service<Patrol>::SharedPtr patrol_service_;                  // patrol 服务端
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;  // 速度指令发布者
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscriber_;   // 位置订阅者
    double target_x_ = {1.0};   // 目标点 x（初始目标 (1,1)）
    double target_y_ = {1.0};   // 目标点 y
    double k_ = {3.0};          // 比例增益：前进速度 = k_ × 距离
    double max_speed_ = {3.0};  // 最大速度上限
```

语法与写法说明：

- **`private:`**：这些成员只有类内部代码能访问，外界碰不到。数据默认写 private 是好习惯（封装）。
- **为什么四个 ROS 对象都是 SharedPtr 成员？** 见 [1.2 节](#12-智能指针-shared_ptr--本例最重要的概念)——不存住就会被立刻销毁。`parameter_callback_handle_` 尤其容易被新手漏掉：它看起来"没用到"，但**必须存着**，否则参数回调注册立即失效。
- **变量名末尾的下划线 `_`** 是命名习惯，表示"这是类的成员变量"，用来和函数里的局部变量区分。ROS 2 官方代码风格就是这样。
- **`= {1.0}`** 是 C++11 的**统一初始化**语法，效果等同 `= 1.0`。给成员变量在声明处直接给默认值，保证对象一出生这些值就是有效的。
- **`double`**：双精度浮点数（能存小数）。坐标、速度这类连续量都用它。

`k_` 的物理含义值得多说一句：这是一个**比例控制器（P 控制器）**——离目标越远开得越快，越近越慢，速度 = k × 距离。k 越大乌龟越"猛"。这是机器人控制里最简单也最常用的控制律。

### 2.4 构造函数总览（第 30–69 行）

构造函数干了 5 件事，全是"注册"性质的初始化：

1. 声明并读取参数 `k`、`max_speed`
2. 注册"参数被修改时"的回调
3. 创建 `patrol` 服务
4. 创建速度发布者
5. 创建位置订阅者

**为什么全放构造函数里？** ROS 2 节点的生命周期就是"构造时把所有通信端点建好 → `spin()` 里等事件触发回调"。构造函数是唯一保证"最早且只执行一次"的地方。

#### ① 声明和读取参数（第 32–35 行）

```cpp
this->declare_parameter("k", 1.0);          // 声明参数 k，默认值 1.0
this->declare_parameter("max_speed", 1.0);
this->get_parameter("k", k_);               // 把参数当前值读进成员变量 k_
this->get_parameter("max_speed", max_speed_);
```

- **`this`** 是指向当前对象自己的指针，`this->xxx` 即"我自己的 xxx"。这四个函数都是从 `rclcpp::Node` 继承来的。（类内部 `this->` 其实可省略，写上是为了明确"这是继承来的成员函数"。）
- **为什么必须先 `declare` 再 `get`？** ROS 2 规定参数必须先声明才能使用（防止拼写错误静默失败）。声明后，这个参数就对全世界可见：可以在启动时用 launch 文件/命令行覆盖，运行中用 `ros2 param set` 修改。
- 注意：`k_` 声明时初始化为 3.0，但这里被 `get_parameter` 覆盖成参数值（没人改就是默认值 1.0）。**参数的意义**就在于：不改一行代码、不重新编译，就能换一套控制参数。

#### ② 参数修改回调（第 37–52 行）—— 本文件的核心知识点

```cpp
parameter_callback_handle_ = this->add_on_set_parameters_callback(
    [&](const std::vector<rclcpp::Parameter> & parameters) -> rcl_interfaces::msg::SetParametersResult {
        rcl_interfaces::msg::SetParametersResult result;
        result.successful = true;                    // 先默认"我接受这次修改"
        for (const auto & parameter : parameters) {  // 逐个处理被修改的参数
            RCLCPP_INFO(this->get_logger(), "更新参数的值%s=%f",
                        parameter.get_name().c_str(), parameter.as_double());
            if (parameter.get_name() == "k")         { k_ = parameter.as_double(); }
            if (parameter.get_name() == "max_speed") { max_speed_ = parameter.as_double(); }
        }
        return result;
    });
```

**为什么需要这个回调？** 关键理解：外界改参数，改的是 ROS 参数系统里的登记值；**你的成员变量 `k_` 不会自动跟着变**。这个回调就是"同步器"：每当有人（命令行、其他节点）修改参数，ROS 先调用它，你在里面把新值抄进自己的成员变量。没有它，客户端把 k 改成 4.0 也白改——控制逻辑用的还是旧的 `k_`。

逐个语法点：

- **`std::vector<T>`**：C++ 的动态数组（能自动扩容的列表）。这里装的是"这次被修改的所有参数"（一次可以改多个）。
- **范围 for 循环**（C++11）：
  ```cpp
  for (const auto & item : 容器) { ... }   // 对容器里每个元素执行一遍
  ```
  `const auto &` = "只读引用，不拷贝"。**模板记忆**：遍历容器只读就写 `const auto &`，要修改元素就写 `auto &`。
- **`RCLCPP_INFO(logger, 格式, 参数...)`**：ROS 2 的日志宏，用法同 C 的 `printf`：`%s` 填字符串、`%f` 填浮点数、`%d` 填整数。级别从低到高有 `RCLCPP_DEBUG / INFO / WARN / ERROR / FATAL`。**为什么不用 `std::cout`？** ROS 日志自动带时间戳、节点名、级别，能被 ros2 工具统一收集过滤。
- **`.c_str()`**：C++ 的 `std::string` 转成 `printf` 系列需要的 C 风格字符串（`const char*`）。凡是 `%s` 填 `std::string` 都要加它，忘加是常见错误。
- **`parameter.as_double()`**：`rclcpp::Parameter` 是"万能盒子"，能装各种类型，用 `as_double()` / `as_int()` / `as_string()` / `as_bool()` 按类型取出。
- **返回值**：`result.successful = true` 表示接受修改。实际项目中常在这里做**校验**，比如拒绝负数速度：
  ```cpp
  if (parameter.get_name() == "max_speed" && parameter.as_double() < 0) {
      result.successful = false;
      result.reason = "max_speed 不能为负";
  }
  ```
- **返回的句柄必须存进 `parameter_callback_handle_`**，原因同前：不存即失效。

#### ③ 创建服务（第 53–65 行）

```cpp
patrol_service_ = this->create_service<Patrol>("patrol",
    [&](const Patrol::Request::SharedPtr request, Patrol::Response::SharedPtr response) -> void {
        if ((0 < request->target_x && request->target_x < 12.0f) &&
            (0 < request->target_y && request->target_y < 12.0f)) {
            this->target_x_ = request->target_x;   // 合法：换目标点
            this->target_y_ = request->target_y;
            response->result = Patrol::Response::SUCCESS;
        } else {
            response->result = Patrol::Response::FAIL;
        }
    });
```

- **`create_service<Patrol>("patrol", 回调)`**：创建名为 `patrol` 的服务端。模板参数 `<Patrol>` 指定服务类型。别人一调用，ROS 就执行这个 lambda。
- **服务回调的固定签名**：`(Request::SharedPtr, Response::SharedPtr)` —— 请求进来是现成的，**响应对象也是 ROS 建好递给你的，你只管往里填字段**，回调结束 ROS 自动把它发回给调用方。不需要（也不能）自己 return 响应。
- `12.0f` 的 **`f` 后缀**表示 float（单精度）字面量。因为 `.srv` 里 `target_x` 定义为 `float32`，比较时用同精度字面量避免类型转换警告。`&&` 是逻辑与（"并且"）。turtlesim 窗口约 11×11，所以合法范围检查为 (0, 12)。
- **设计上的巧妙之处**：服务回调**只改目标点，不动乌龟**。真正驱动乌龟的是下面的 `on_pose_received`——它每秒执行约 60 次，永远追当前目标。目标一换，乌龟下一拍自动转向新目标。这种"回调之间通过成员变量通信"的解耦写法是 ROS 节点的典型模式。

#### ④⑤ 发布者和订阅者（第 67–68 行）

```cpp
publisher_  = this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel", 10);
subscriber_ = this->create_subscription<turtlesim::msg::Pose>("turtle1/pose", 10,
                  std::bind(&TurtleControl::on_pose_received, this, std::placeholders::_1));
```

- **`create_publisher<消息类型>("话题名", 队列长度)`**：发布者。`turtle1/cmd_vel` 是 turtlesim 约定的"速度指令"话题——往上面发 Twist，乌龟就动。
- **`10` 是 QoS 队列深度**：消息来不及处理时最多缓存 10 条，再多就丢最旧的。入门阶段记住"写 10 就行"。
- **`create_subscription<消息类型>("话题名", 队列长度, 回调)`**：订阅者。`turtle1/pose` 上 turtlesim 以约 60 Hz 广播乌龟位姿，每来一条就调一次回调。
- **`std::bind` 是什么？** 回调需要"一个可调用的东西"，但 `on_pose_received` 是**成员函数**——成员函数必须依附于某个对象才能调用（得知道是"谁的" on_pose_received）。`std::bind(&类名::函数名, this, std::placeholders::_1)` 的意思是："把 **this 这个对象**和它的成员函数**绑定**成一个可调用对象；将来传进来的第 1 个参数（`_1` 占位符）填到函数的第 1 个参数位置"。
- **为什么这里用 `std::bind`，前面用 lambda？** 功能完全等价，纯属两种风格（作者两种都示范了）。等价的 lambda 写法：
  ```cpp
  [this](const turtlesim::msg::Pose::SharedPtr pose) { this->on_pose_received(pose); }
  ```
  经验法则：回调逻辑长、想单独成函数（方便复用/测试）→ 定义成员函数 + `std::bind` 或 lambda 转发；逻辑短 → 直接写 lambda。现代代码更流行 lambda，`std::bind` 是老一点的教程常见写法。

### 2.5 控制逻辑 `on_pose_received`（第 73–110 行）

这个函数**每秒被调用约 60 次**（乌龟位置的广播频率），是真正让乌龟动起来的地方。它实现了一个"先转向、后前进"的比例控制器。

```cpp
void on_pose_received(const turtlesim::msg::Pose::SharedPtr pose)
```

参数就是刚收到的位姿消息（智能指针，用 `->` 取字段）。

**第 1 步：我在哪（第 77–79 行）**

```cpp
auto current_x = pose->x;
auto current_y = pose->y;
RCLCPP_INFO(get_logger(), "当前位置: x=%f, y=%f", current_x, current_y);
```

**第 2 步：算距离差和角度差（第 82–87 行）**

```cpp
auto distance = std::sqrt(
    (target_x_ - current_x) * (target_x_ - current_x) +
    (target_y_ - current_y) * (target_y_ - current_y));

auto angle = std::atan2((target_y_ - current_y), (target_x_ - current_x)) - pose->theta;
```

- `distance`：勾股定理 √(Δx² + Δy²)，到目标的直线距离。`std::sqrt` 是开平方（来自 `<cmath>`，被 rclcpp 间接包含了）。
- `std::atan2(Δy, Δx)`：返回从当前位置指向目标的方向角（弧度，范围 -π 到 π）。**为什么用 `atan2` 而不是 `atan(Δy/Δx)`？** `atan2` 接收两个参数能区分四个象限，而且 Δx=0 时不会除零——算方向角永远用 `atan2`，这是惯例。
- 减去 `pose->theta`（乌龟当前朝向）得到**角度差**：乌龟还需要转多少角度才正对目标。≈0 表示已对准。

**第 3 步：根据差值定速度（第 93–101 行）**

```cpp
auto msg = geometry_msgs::msg::Twist();   // 新消息，所有字段自动为 0
if (distance > 0.1) {                     // 还没到（留 0.1 的"到达容差"）
    if (fabs(angle) > 0.2) {              // 朝向偏差大于约 11°？
        msg.angular.z = fabs(angle);      //   → 只旋转，不前进
    } else {                              // 基本对准了？
        msg.linear.x = k_ * distance;     //   → 前进，越远越快（比例控制）
    }
}
```

- `Twist` 消息里本例只用两个字段：`linear.x` 前进速度、`angular.z` 转向（自转）速度。**新建的消息所有字段都是 0**——所以距离小于 0.1 时发出的是全零消息，乌龟停下。
- **为什么要 `distance > 0.1` 而不是 `> 0`？** 浮点数几乎不可能精确等于目标值，不留容差乌龟会在目标点附近永远抖动。
- **为什么"先转再走"？** 如果朝向偏得厉害还往前开，会绕大弯甚至越走越远。偏差大就原地转，小于阈值再前进，路径干净得多。
- `fabs()` 是浮点数取绝对值。
- **`k_` 和参数系统在这里闭环**：客户端把 k 从 1.0 改成 4.0 后，同样的距离下前进速度变成 4 倍，乌龟明显更冲。
- 小瑕疵（读代码要能看出来）：`angular.z = fabs(angle)` 丢掉了角度差的**符号**，导致乌龟永远逆时针转——哪怕顺时针转 30° 更近，它也会逆时针转 330°。功能上仍能到达，只是有时绕远。正确写法是保留符号：`msg.angular.z = angle;`（可再乘个增益）。

**第 4 步：限速并发布（第 104–109 行）**

```cpp
if (msg.linear.x > max_speed_) { msg.linear.x = max_speed_; }
publisher_->publish(msg);
```

`k_ × distance` 在距离远时可能算出很大的速度，用 `max_speed_` 截断（这就是第二个参数的用途）。最后 `publish` 发出——turtlesim 收到后让乌龟按此速度动一小步。60 Hz 循环往复，宏观上就是乌龟平滑驶向目标。

### 2.6 `main` 函数（第 115–122 行）

```cpp
int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);                                      // ① 初始化 ROS 2
    auto node = std::make_shared<TurtleControl>("turtle_control"); // ② 创建节点（跑构造函数）
    rclcpp::spin(node);                                            // ③ 事件循环：阻塞在这，等事件、跑回调
    rclcpp::shutdown();                                            // ④ 清理（Ctrl+C 之后才走到）
    return 0;
}
```

- `main` 是 C++ 程序的入口；`argc`/`argv` 是命令行参数，交给 `rclcpp::init` 处理 ROS 专属的启动选项（如重命名节点）。
- **`rclcpp::spin(node)` 是灵魂**：它是一个死循环——"等事件（消息到了/服务被调了/定时器到点了）→ 执行对应回调 → 继续等"。**没有 spin，前面注册的所有回调一个都不会执行**，程序直接跑到头退出。按 Ctrl+C 后 spin 才返回。
- 这 4 行是**每个 ROS 2 C++ 节点一字不差的固定模板**，背下来即可。

---

## 3. `patrol_client.cpp` 逐段详解

这个节点干两件事：① 每 5 秒调一次 `patrol` 服务发随机目标；② 启动时调用服务端自带的 `set_parameters` 服务，把 `k` 改成 4.0。

### 3.1 头文件与别名（第 1–13 行）

```cpp
#include <rclcpp/rclcpp.hpp>
#include <chapt4_interfaces/srv/patrol.hpp>        // 与服务端用同一份 Patrol 服务定义
#include <chrono>
#include <ctime>                                   // 提供 time(NULL)，给随机数播种用
#include <rcl_interfaces/msg/parameter.hpp>        // ┐
#include <rcl_interfaces/msg/parameter_value.hpp>  // ├ 描述"一个参数"的三件套消息
#include <rcl_interfaces/msg/parameter_type.hpp>   // ┘
#include <rcl_interfaces/srv/set_parameters.hpp>   // 标准的"设置参数"服务定义

using Patrol = chapt4_interfaces::srv::Patrol;
using namespace std::chrono_literals;
using SetP = rcl_interfaces::srv::SetParameters;
```

**关键背景知识**：ROS 2 里**每个声明了参数的节点，都会自动开一组参数服务**，其中就有 `/<节点名>/set_parameters`。所以客户端不需要服务端写任何配合代码，直接像调普通服务一样调 `/turtle_control/set_parameters` 就能远程改参数。`rcl_interfaces` 这个功能包定义的就是这些标准服务/消息的格式。

### 3.2 类与成员（第 15–19 行）

```cpp
class PatrolClient : public rclcpp::Node
{
    private:
        rclcpp::TimerBase::SharedPtr timer_;              // 定时器：周期性触发回调
        rclcpp::Client<Patrol>::SharedPtr patrol_client_; // patrol 服务的客户端
```

老套路：继承 Node，创建出来的定时器和客户端存成 SharedPtr 成员保命。

### 3.3 构造函数：定时器 + 服务调用（第 22–57 行）

```cpp
PatrolClient(const std::string &node_name) : Node(node_name)
{
    srand(time(NULL));                                     // 用当前时间给随机数生成器播种
    patrol_client_ = this->create_client<Patrol>("patrol"); // 创建客户端，对准名为 patrol 的服务
    timer_ = this->create_wall_timer(5s, [&]() -> void { ...见下... });
}
```

- **`srand(time(NULL))`**：C 语言的随机数是伪随机——种子相同，序列就相同。用当前时间当种子，每次运行序列才不同。**只需在程序开头调一次**。（这是 C 风格老写法，现代 C++ 有 `<random>` 库，教程用旧的图简单。）
- **`create_client<Patrol>("patrol")`**：与服务端 `create_service` 成对。注意客户端可以先于服务端创建——它只是"拨号器"，服务在不在是调用时才检查的事。
- **`create_wall_timer(周期, 回调)`**：每隔 5 秒（`5s` 就靠 `chrono_literals`）执行一次 lambda。"wall" 指墙上挂钟的真实时间。**为什么用定时器而不是 `while + sleep`？** 定时器由 spin 统一调度，和其他回调和平共处；自己写 while 循环会独占线程，spin 就转不动了。**ROS 2 里一切周期性任务都用定时器。**

定时器 lambda 里是**客户端调服务的标准三步**：

**第 1 步：等服务上线（第 28–35 行）**

```cpp
while (!this->patrol_client_->wait_for_service(1s)) {
    if (!rclcpp::ok()) {
        RCLCPP_ERROR(this->get_logger(), "等到服务上线中,rclcpp死了");
        return;
    }
    RCLCPP_INFO(this->get_logger(), "等待服务上线中...");
}
```

- `wait_for_service(1s)`：服务在线立即返回 `true`；否则最多等 1 秒后返回 `false`。外面套 `while(!...)` 就变成"每秒问一次，问到为止"。**为什么要等？** 客户端和服务端谁先启动没有保证；不等就发请求，请求会石沉大海。
- `rclcpp::ok()`：ROS 还活着吗？用户按 Ctrl+C 后它变 false。**为什么检查它？** 不检查的话，用户按了 Ctrl+C，这个 while 还在死等，程序关不掉。这个"等待 + ok 检查"组合是**固定模板**，所有客户端代码照抄。
- `!` 是逻辑非（取反）。

**第 2 步：造请求（第 38–41 行）**

```cpp
auto request = std::make_shared<Patrol::Request>();
request->target_x = rand() % 15;
request->target_y = rand() % 15;
```

- 请求对象规定用 shared_ptr 创建（`async_send_request` 的接口要求）。
- `rand() % 15`：`%` 是取余，得到 0~14 的随机整数。**故意越界**：服务端只接受 (0,12)，所以 0 和 12~14 会触发 FAIL 分支——这是为了演示服务的失败路径。整数赋给 float 字段会自动转换。

**第 3 步：异步发送（第 44–54 行）**

```cpp
this->patrol_client_->async_send_request(request,
    [&](rclcpp::Client<Patrol>::SharedFuture result_future) -> void {
        auto response = result_future.get();
        if (response->result == Patrol::Response::SUCCESS) { RCLCPP_INFO(...,  "服务调用成功,正在巡逻"); }
        if (response->result == Patrol::Response::FAIL)    { RCLCPP_ERROR(..., "服务调用失败,目标点不合法"); }
    });
```

两个新概念：

- **异步（async）= 发出去就不管，不站在原地等**。`async_send_request` 立刻返回，程序继续干别的；等响应真的回来了，ROS（在 spin 里）自动调用你给的第二个参数（回调 lambda）。**为什么必须异步？** 我们此刻正处在定时器回调里，而回调都是 spin 派发的——如果在回调里死等响应，spin 被卡住，响应永远送不进来，**死锁**。所以"在回调里调服务，必须用异步+回调"是铁律。
- **future（期物）**："将来才有的值"的占位凭据。回调被触发时值已就绪，`result_future.get()` 直接取出响应（shared_ptr），然后对照 `SUCCESS`/`FAIL` 常量打日志。`==` 是判断相等（注意别写成赋值的 `=`，那是新手经典错误）。

### 3.4 `call_set_parameters`：调别的节点的参数服务（第 60–82 行）

```cpp
SetP::Response::SharedPtr call_set_parameters(const rcl_interfaces::msg::Parameter &param)
{
    auto param_client = this->create_client<SetP>("/turtle_control/set_parameters");

    while (!param_client->wait_for_service(1s)) {          // 同款等待模板
        if (!rclcpp::ok()) { RCLCPP_ERROR(...); return nullptr; }
        RCLCPP_INFO(this->get_logger(), "等待服务上线中...");
    }

    auto request = std::make_shared<SetP::Request>();
    request->parameters.push_back(param);                  // 请求里是参数"列表"，把我们这一个塞进去

    auto future = param_client->async_send_request(request);
    rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);
    auto response = future.get();
    return response;
}
```

和上面 patrol 调用的**区别**，每处都有原因：

- **服务名 `/turtle_control/set_parameters`**：turtle_control 节点自动提供的参数服务，开头的 `/` 表示绝对名称。
- **`push_back`**：向 vector 尾部追加一个元素。`SetParameters` 的请求里 `parameters` 是列表（一次可批量改多个参数），我们只放一个。
- **`spin_until_future_complete(...)` —— 同步等待**，和前面的"铁律"矛盾吗？不矛盾，因为**调用时机不同**：这个函数被 `main` 在 `rclcpp::spin(node)` **之前**调用（见 3.6），此刻**没有任何事件循环在跑**，异步回调根本没人派发。`spin_until_future_complete` 的意思是"就在这里临时开一个小事件循环，转到这个 future 出结果为止，然后继续往下走"。等完之后 `future.get()` 拿响应是安全的。
  - **总结成规则**：**spin 之前（如 main 里）调服务 → 用 `spin_until_future_complete` 同步等；回调里调服务 → 必须 `async_send_request` + 回调。** 记住这条能避开 ROS 2 最经典的死锁坑。
- **`return nullptr;`**：`nullptr` 是"空指针"（指向空无一物）。函数返回类型是指针时，用它表达"失败/没有结果"。**调用方必须先判空再使用**，否则解引用空指针程序直接崩。

### 3.5 `update_server_param_k`：打包参数并处理结果（第 85–112 行）

```cpp
void update_server_param_k(double k)
{
    // 1. 参数消息 = 名字 + 值
    auto param = rcl_interfaces::msg::Parameter();
    param.name = "k";
    // 2. 值本身又是个消息：要同时写"类型标签"和对应字段
    auto param_value = rcl_interfaces::msg::ParameterValue();
    param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
    param_value.double_value = k;
    param.value = param_value;
    // 3. 发请求、查结果
    auto response = call_set_parameters(param);
    if (response == NULL) {                       // 判空！call_set_parameters 可能返回 nullptr
        RCLCPP_ERROR(this->get_logger(), "更新参数失败");
        return;
    }
    for (auto result : response->results) {       // 一个参数对应一个结果
        if (result.successful == false)
            RCLCPP_ERROR(this->get_logger(), "更新参数失败,原因:%s", result.reason.c_str());
        else
            RCLCPP_INFO(this->get_logger(), "更新参数成功");
    }
}
```

- **为什么值要"类型标签 + 字段"两样都填？** `ParameterValue` 是个"万能盒子"，内部同时有 `bool_value`、`integer_value`、`double_value`、`string_value` 等所有格子。接收方靠 `type` 标签知道该看哪个格子。只填 `double_value` 不填 `type`，对方会当作"未设置"处理。`PARAMETER_DOUBLE` 是预定义常量。
- `NULL` 与 `nullptr` 等价（`NULL` 是 C 老写法，现代 C++ 推荐 `nullptr`，这里作者混用了）。
- 响应里 `results` 与请求里 `parameters` 一一对应，所以用 for 遍历；失败时 `reason` 字段给出人类可读的原因。
- **两个文件在此闭环**：这个请求到达 turtle_control 后，触发的正是 2.4 节②的参数回调——服务端打印"更新参数的值k=4.000000"并更新 `k_`。

### 3.6 `main`（第 115–123 行）

```cpp
int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PatrolClient>("patrol_client");
    node->update_server_param_k(4.0);   // spin 之前：一次性改参数（内部用 spin_until_future_complete 自转）
    rclcpp::spin(node);                 // 之后进入事件循环：5 秒定时器从这里开始生效
    rclcpp::shutdown();
    return 0;
}
```

顺序设计：先在 spin 之前完成一次性的参数修改（此时靠 `spin_until_future_complete` 自带的小循环处理通信），然后 `spin` 接管，定时器和异步响应回调从此由它派发。

---

## 4. 运行起来会发生什么

1. 依次启动：turtlesim → `turtle_control` → `patrol_client`。
2. `patrol_client` 一启动就把服务端的 `k` 从 1.0 改成 4.0：服务端日志打印参数更新，此后乌龟向目标加速的力度变为 4 倍。
3. 之后每 5 秒，客户端随机生成 [0,14]×[0,14] 里的一个点：
   - 落在 (0,12)×(0,12) 内 → 服务端回 SUCCESS，乌龟先原地转向、再以"k×距离"的速度冲向目标（不超过 max_speed），临近时自然减速停下；
   - 落在范围外 → 服务端回 FAIL，客户端打印"目标点不合法"，乌龟维持原状。

可以用命令行观察/干预（很适合练手）：

```bash
ros2 param list                                  # 看有哪些参数
ros2 param get /turtle_control k                 # 读参数
ros2 param set /turtle_control max_speed 5.0     # 手动改参数（同样会触发那个回调）
ros2 service call /patrol chapt4_interfaces/srv/Patrol "{target_x: 5.0, target_y: 5.0}"  # 手动调服务
ros2 topic echo /turtle1/cmd_vel                 # 偷看发出的速度指令
```

---

## 5. ROS 2 常用代码模板

以下模板覆盖了本例全部套路，**新写节点时直接抄，改名字和类型即可**。

### 5.1 节点骨架（万能起手式）

```cpp
#include <rclcpp/rclcpp.hpp>
using namespace std::chrono_literals;

class MyNode : public rclcpp::Node
{
private:
    // 所有 publisher/subscriber/service/client/timer 的 SharedPtr 都声明在这，防止被销毁

public:
    MyNode(const std::string &name) : Node(name)
    {
        // 所有 create_xxx 和 declare_parameter 都写在构造函数里
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MyNode>("my_node"));
    rclcpp::shutdown();
    return 0;
}
```

### 5.2 发布者

```cpp
// 成员：
rclcpp::Publisher<消息类型>::SharedPtr pub_;
// 构造函数：
pub_ = this->create_publisher<消息类型>("话题名", 10);
// 任何地方发消息：
auto msg = 消息类型();
msg.某字段 = ...;
pub_->publish(msg);
```

### 5.3 订阅者

```cpp
// 成员：
rclcpp::Subscription<消息类型>::SharedPtr sub_;
// 构造函数（lambda 版，推荐）：
sub_ = this->create_subscription<消息类型>("话题名", 10,
    [this](const 消息类型::SharedPtr msg) { /* 处理 msg->xxx */ });
// 或成员函数 + bind 版：
sub_ = this->create_subscription<消息类型>("话题名", 10,
    std::bind(&MyNode::回调函数, this, std::placeholders::_1));
```

### 5.4 定时器

```cpp
rclcpp::TimerBase::SharedPtr timer_;
timer_ = this->create_wall_timer(1s, [this]() { /* 周期任务 */ });
```

### 5.5 服务端

```cpp
rclcpp::Service<服务类型>::SharedPtr srv_;
srv_ = this->create_service<服务类型>("服务名",
    [this](const 服务类型::Request::SharedPtr req, 服务类型::Response::SharedPtr res) {
        // 读 req->xxx，填 res->yyy，不用 return，ROS 自动发回
    });
```

### 5.6 客户端（含两种等待方式）

```cpp
rclcpp::Client<服务类型>::SharedPtr client_;
client_ = this->create_client<服务类型>("服务名");

// —— 固定的等待模板 ——
while (!client_->wait_for_service(1s)) {
    if (!rclcpp::ok()) { /* ROS 已退出，放弃 */ return; }
    RCLCPP_INFO(this->get_logger(), "等待服务上线...");
}

auto request = std::make_shared<服务类型::Request>();
request->xxx = ...;

// 方式 A：在回调里调用（定时器/订阅回调中）→ 必须异步
client_->async_send_request(request,
    [this](rclcpp::Client<服务类型>::SharedFuture fut) {
        auto response = fut.get();  // 处理响应
    });

// 方式 B：在 spin 之前调用（如 main 里）→ 同步小循环
auto future = client_->async_send_request(request);
rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);
auto response = future.get();
```

> **铁律**：回调里用 A，spin 前用 B。搞反了要么死锁、要么永远收不到响应。

### 5.7 参数（声明、读取、响应外部修改）

```cpp
// 成员：
OnSetParametersCallbackHandle::SharedPtr param_cb_handle_;
double my_param_;

// 构造函数：
this->declare_parameter("my_param", 1.0);   // 先声明（带默认值）
this->get_parameter("my_param", my_param_); // 读进成员变量
param_cb_handle_ = this->add_on_set_parameters_callback(  // 外界修改时同步
    [this](const std::vector<rclcpp::Parameter> &params) {
        rcl_interfaces::msg::SetParametersResult result;
        result.successful = true;
        for (const auto &p : params) {
            if (p.get_name() == "my_param") my_param_ = p.as_double();
            // 想拒绝非法值：result.successful = false; result.reason = "...";
        }
        return result;
    });
```

---

## 6. C++ 语法速查表

| 语法 | 一句话解释 | 本例出处 |
|---|---|---|
| `class X : public Y` | X 继承 Y，自动拥有 Y 的全部功能 | 两个节点类都继承 `rclcpp::Node` |
| 构造函数 `X(...) : Y(...)` | 对象创建时自动执行；冒号后先构造父类 | `: Node(node_name)` |
| `this->` | 访问"我自己"的成员 | `this->create_service(...)` |
| `shared_ptr` / `::SharedPtr` | 自动管内存的智能指针，没人用时自动销毁 | 所有 ROS 对象和消息 |
| `std::make_shared<T>(args)` | 创建 T 对象并交给 shared_ptr 托管 | 创建节点、创建请求 |
| `->` vs `.` | 指针访问成员用 `->`，对象本身用 `.` | `pose->x` vs `msg.linear.x` |
| `auto` | 编译期自动推断类型（不是动态类型） | `auto request = ...` |
| 模板 `T<U>` | 泛型填空，编译期检查类型 | `Client<Patrol>` |
| lambda `[&](...){...}` | 匿名函数；`[&]` 按引用捕获外部变量 | 所有回调 |
| `std::bind(&C::f, this, _1)` | 把成员函数绑成可调用对象（lambda 的老式替代品） | 订阅回调 |
| future / `SharedFuture` | "将来才有的值"的凭据，`get()` 取值 | 服务响应 |
| `std::vector` / `push_back` | 动态数组 / 尾部追加 | 参数列表 |
| 范围 for `for (const auto &x : v)` | 遍历容器每个元素（只读不拷贝） | 遍历参数、遍历结果 |
| `const T &` 参数 | 高效只读传参：不拷贝且承诺不改 | 各函数参数 |
| `nullptr` / `NULL` | 空指针，用前必须判空 | 服务调用失败返回值 |
| `12.0f` 的 `f` | float（单精度）字面量后缀 | 范围检查 |
| `%` 取余 | `rand() % 15` → 0~14 的随机整数 | 随机目标点 |
| `&&` `||` `!` | 逻辑与 / 或 / 非 | 各种条件判断 |
| `.c_str()` | `std::string` → C 字符串，`%s` 打印必备 | 日志语句 |
| `using A = B` / `using namespace` | 起类型别名 / 引入命名空间（如时间字面量 `5s`） | 文件开头 |

---

📑 [返回笔记索引](../../README.md#笔记索引)

# ROS 2 学习笔记

> ROS 2 学习笔记与配套代码：自语言基础起，至自制两轮差速机器人（`szcbot`）的实车导航。

[![ROS 2](https://img.shields.io/badge/ROS%202-Jazzy-22314E?logo=ros&logoColor=white)](https://docs.ros.org/en/jazzy/)
[![Gazebo](https://img.shields.io/badge/Gazebo-Sim-F58113?logo=gazebo&logoColor=white)](https://gazebosim.org/docs)
[![Nav2](https://img.shields.io/badge/Nav2-slam__toolbox-4B8BBE)](https://docs.nav2.org/)
[![micro-ROS](https://img.shields.io/badge/micro--ROS-ESP32-E7352C)](https://micro.ros.org/)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](LICENSE)

内容覆盖：Python / C++ 语言基础，话题、服务、参数与 Launch，TF 与可视化工具，
URDF 建模与 Gazebo 仿真，SLAM 建图与 Nav2 导航，pluginlib 与 Nav2 自定义插件，
ESP32 + micro-ROS 实体机器人，以及 QoS、执行器、生命周期节点、组件与 DDS 调优。

| | 位置 | 说明 |
| :-- | :-- | :-- |
| 笔记 | [`ROS2/`](ROS2) | 97 篇 Markdown，逐节对应源码，见 [笔记索引](#笔记索引) |
| 代码 | `111/` ~ `999/`、`10/` | 各章配套工作空间，见 [环境与依赖](#环境与依赖) |
| 附件 | [`_resources/`](_resources) | 图片与 PDF，已内嵌于笔记正文 |

## 目录

1. [快速开始](#快速开始)
2. [笔记索引](#笔记索引)
3. [仓库结构](#仓库结构)
4. [环境与依赖](#环境与依赖)
5. [参考](#参考)
6. [许可证](#许可证)

---

## 快速开始

```bash
git clone https://github.com/Vince-0906/ROS.git
cd ROS
```

笔记按阅读顺序编为一条链路，起点为 [2.5.2 C++新特性](ROS2/C%2B%2B/2.5.2%20C%2B%2B新特性.md)，每篇末尾链至下一节；
亦可自 [笔记索引](#笔记索引) 按章检索。笔记正文中的链接均为标准 Markdown
相对链接，图片以标准语法内嵌，不依赖特定编辑器的扩展。

编译代码前请先核对 [环境与依赖](#环境与依赖) 中的版本要求，
并按「各章工作空间」一节定位对应目录。

---

## 笔记索引

共 97 篇笔记。其中 90 篇编入一条阅读链路，首篇为 [2.5.2 C++新特性](ROS2/C%2B%2B/2.5.2%20C%2B%2B新特性.md)，末篇为 [10.6.4 使用DDS共享内存](ROS2/实战/10.6.4%20使用DDS共享内存.md)；每篇正文顶部标注上一节与该节对应的源码路径，底部标注下一节。余下 7 篇为速查与参考，不入链路。

「配套代码」一列指向该节对应的源码文件，悬停可查看完整路径。

### 标签

全部笔记均带 `ROS2` 标签，并按主题细分：

| 标签 | 篇数 | 含义 |
| :-- | --: | :-- |
| `ROS2` | 97 | 全部笔记 |
| `实战` | 24 | 实体机器人与进阶专题（第 9–10 章） |
| `工具和仿真` | 22 | TF / RViz / bag / URDF / Gazebo（第 5–6 章） |
| `cpp` | 17 | C++ 实现 |
| `python` | 15 | Python 实现 |
| `导航` | 15 | Nav2 导航与插件（第 7–8 章） |
| `Linux` | 2 | Linux 与命令行 |

### 速查与参考

以下笔记不在阅读链路内，供随时检索。

| 笔记 | 内容 | 配套代码 |
| :-- | :-- | :-- |
| [ROS2基础](ROS2/ROS2基础.md) | Topic / Service / Parameter / Action 四种通信方式，Gazebo、Nav2、MoveIt 2 三大框架 | — |
| [ROS2相关命令](ROS2/ROS2相关命令.md) | 功能包创建、构建、`ros2 node/topic/service/param` 命令速查 | — |
| [ROS2 版本](ROS2/ROS2%20版本.md) | 各发行版发布 / EOL 时间表与 LTS 选型建议 | — |
| [Linux命令](ROS2/Linux命令.md) | 安装 ROS 2 与常用文件操作命令 | — |
| [C++速成](ROS2/C%2B%2B/C%2B%2B速成.md) | 指针、命名空间、智能指针、STL、Lambda、模板等 12 个主题速查 | [`src/`](222/ws/src/demo_cpp_pkg/src "222/ws/src/demo_cpp_pkg/src") |
| [C++速成EZ版](ROS2/C%2B%2B/C%2B%2B速成EZ版.md) | 同上内容的生活化比喻版，面向初学者 | [`src/`](222/ws/src/demo_cpp_pkg/src "222/ws/src/demo_cpp_pkg/src") |
| [CODE_EXPLANATION](ROS2/C%2B%2B/CODE_EXPLANATION.md) | `turtle_control.cpp` 与 `patrol_client.cpp` 逐行详解 + ROS 2 代码模板 | [`turtle_control.cpp`](444/ws/src/demo_cpp_service/src/turtle_control.cpp "444/ws/src/demo_cpp_service/src/turtle_control.cpp") · [`patrol_client.cpp`](444/ws/src/demo_cpp_service/src/patrol_client.cpp "444/ws/src/demo_cpp_service/src/patrol_client.cpp") · [`Patrol.srv`](444/ws/src/chapt4_interfaces/srv/Patrol.srv "444/ws/src/chapt4_interfaces/srv/Patrol.srv") |

### 第 2 章 · 编程基础

配套代码目录：[`222/`](222/)

| # | 笔记 | 内容 | 配套代码 |
| --: | :-- | :-- | :-- |
| 1 | [2.5.2 C++新特性](ROS2/C%2B%2B/2.5.2%20C%2B%2B新特性.md) | `auto`、智能指针、Lambda、函数包装器 | [`learn_auto.cpp`](222/ws/src/demo_cpp_pkg/src/learn_auto.cpp "222/ws/src/demo_cpp_pkg/src/learn_auto.cpp") · [`learn_shared_ptr.cpp`](222/ws/src/demo_cpp_pkg/src/learn_shared_ptr.cpp "222/ws/src/demo_cpp_pkg/src/learn_shared_ptr.cpp") · [`learn_lambda.cpp`](222/ws/src/demo_cpp_pkg/src/learn_lambda.cpp "222/ws/src/demo_cpp_pkg/src/learn_lambda.cpp") · [`learn_functional.cpp`](222/ws/src/demo_cpp_pkg/src/learn_functional.cpp "222/ws/src/demo_cpp_pkg/src/learn_functional.cpp") |
| 2 | [2.5.3.1 多线程](ROS2/python/2.5.3.1%20多线程.md) | Python `threading` 与并发下载 | [`learn_thread.py`](222/ws/src/demo_py_pkg/demo_py_pkg/learn_thread.py "222/ws/src/demo_py_pkg/demo_py_pkg/learn_thread.py") |

### 第 3 章 · 话题通信（Topic）

配套代码目录：[`333/`](333/)

| # | 笔记 | 内容 | 配套代码 |
| --: | :-- | :-- | :-- |
| 3 | [3.2.1 通过Topic创建小说](ROS2/python/3.2.1%20通过Topic创建小说.md) | 发布者与发布频率验证 | [`novel_pub_node.py`](333/topic_ws/src/demo_py_topic/demo_py_topic/novel_pub_node.py "333/topic_ws/src/demo_py_topic/demo_py_topic/novel_pub_node.py") |
| 4 | [3.2.2 订阅小说并合成语音](ROS2/python/3.2.2%20订阅小说并合成语音.md) | 订阅者 + TTS 语音合成 | [`novel_sub_node.py`](333/topic_ws/src/demo_py_topic/demo_py_topic/novel_sub_node.py "333/topic_ws/src/demo_py_topic/demo_py_topic/novel_sub_node.py") · [`novel1.txt`](333/novel1.txt "333/novel1.txt") |
| 5 | [3.3.1 发布速度控制海龟画圆](ROS2/C%2B%2B/3.3.1%20发布速度控制海龟画圆.md) | C++ 发布者、隐式转换陷阱 | [`turtle_circle.cpp`](333/topic_ws/src/demo_cpp_topic/src/turtle_circle.cpp "333/topic_ws/src/demo_cpp_topic/src/turtle_circle.cpp") |
| 6 | [3.3.2 订阅pose实现闭环控制](ROS2/C%2B%2B/3.3.2%20订阅pose实现闭环控制.md) | P 控制闭环 | [`turtle_control.cpp`](333/topic_ws/src/demo_cpp_topic/src/turtle_control.cpp "333/topic_ws/src/demo_cpp_topic/src/turtle_control.cpp") |
| 7 | [3.4.2 自定义通信接口](ROS2/python/3.4.2%20自定义通信接口.md) | `.msg` 定义、`rosidl` 生成、CMake 与 package.xml 配置 | [`SystemStatus.msg`](333/topic_practice_ws/src/status_monitor/msg/SystemStatus.msg "333/topic_practice_ws/src/status_monitor/msg/SystemStatus.msg") · [`sys_status_pub.py`](333/topic_practice_ws/src/status_publisher/status_publisher/sys_status_pub.py "333/topic_practice_ws/src/status_publisher/status_publisher/sys_status_pub.py") |
| 8 | [3.4.4 在功能包中使用QT](ROS2/C%2B%2B/3.4.4%20在功能包中使用QT.md) | Qt 接入 ament_cmake | [`hello_qt.cpp`](333/topic_practice_ws/src/status_display/src/hello_qt.cpp "333/topic_practice_ws/src/status_display/src/hello_qt.cpp") · [`CMakeLists.txt`](333/topic_practice_ws/src/status_display/CMakeLists.txt "333/topic_practice_ws/src/status_display/CMakeLists.txt") |
| 9 | [3.4.5 订阅数据并用Qt显示](ROS2/C%2B%2B/3.4.5%20订阅数据并用Qt显示.md) | 系统状态可视化面板 | [`sys_status_display.cpp`](333/topic_practice_ws/src/status_display/src/sys_status_display.cpp "333/topic_practice_ws/src/status_display/src/sys_status_display.cpp") |

### 第 4 章 · 服务、参数与 Launch

配套代码目录：[`444/ws`](444/ws)

| # | 笔记 | 内容 | 配套代码 |
| --: | :-- | :-- | :-- |
| 10 | [4.2.2 人脸检测](ROS2/python/4.2.2%20人脸检测.md) | OpenCV 人脸检测基础 | [`learn_face_detect.py`](444/ws/src/demo_py_service/demo_py_service/learn_face_detect.py "444/ws/src/demo_py_service/demo_py_service/learn_face_detect.py") |
| 11 | [4.2.3 人脸检测服务实现](ROS2/python/4.2.3%20人脸检测服务实现.md) | Python 服务端 | [`FaceDetector.srv`](444/ws/src/chapt4_interfaces/srv/FaceDetector.srv "444/ws/src/chapt4_interfaces/srv/FaceDetector.srv") · [`face_detect_node.py`](444/ws/src/demo_py_service/demo_py_service/face_detect_node.py "444/ws/src/demo_py_service/demo_py_service/face_detect_node.py") |
| 12 | [4.2.4 人脸检测客户端的实现](ROS2/python/4.2.4%20人脸检测客户端的实现.md) | 客户端与 executor 嵌套踩坑记录 | [`face_detect_client_node.py`](444/ws/src/demo_py_service/demo_py_service/face_detect_client_node.py "444/ws/src/demo_py_service/demo_py_service/face_detect_client_node.py") |
| 13 | [4.3.2 服务端代码实现](ROS2/C%2B%2B/4.3.2%20服务端代码实现.md) | C++ 服务端 | [`Patrol.srv`](444/ws/src/chapt4_interfaces/srv/Patrol.srv "444/ws/src/chapt4_interfaces/srv/Patrol.srv") · [`turtle_control.cpp`](444/ws/src/demo_cpp_service/src/turtle_control.cpp "444/ws/src/demo_cpp_service/src/turtle_control.cpp") |
| 14 | [4.3.3 客户端代码实现](ROS2/C%2B%2B/4.3.3%20客户端代码实现.md) | `async_send_request` 异步调用 | [`patrol_client.cpp`](444/ws/src/demo_cpp_service/src/patrol_client.cpp "444/ws/src/demo_cpp_service/src/patrol_client.cpp") |
| 15 | [4.4.1 参数声明设置](ROS2/python/4.4.1%20参数声明设置.md) | Python 参数声明与读写 | [`face_detect_node.py`](444/ws/src/demo_py_service/demo_py_service/face_detect_node.py "444/ws/src/demo_py_service/demo_py_service/face_detect_node.py") |
| 16 | [4.4.2 订阅参数更新](ROS2/python/4.4.2%20订阅参数更新.md) | 参数回调 | [`face_detect_node.py`](444/ws/src/demo_py_service/demo_py_service/face_detect_node.py "444/ws/src/demo_py_service/demo_py_service/face_detect_node.py") |
| 17 | [4.4.3 客户端代码实现](ROS2/python/4.4.3%20客户端代码实现.md) | Python 参数客户端 | [`face_detect_client_node.py`](444/ws/src/demo_py_service/demo_py_service/face_detect_client_node.py "444/ws/src/demo_py_service/demo_py_service/face_detect_client_node.py") |
| 18 | [4.5.1 参数声明与设置](ROS2/C%2B%2B/4.5.1%20参数声明与设置.md) | C++ 参数声明与读写 | [`turtle_control.cpp`](444/ws/src/demo_cpp_service/src/turtle_control.cpp "444/ws/src/demo_cpp_service/src/turtle_control.cpp") |
| 19 | [4.5.2 接收参数事件](ROS2/C%2B%2B/4.5.2%20接收参数事件.md) | 参数事件回调 | [`turtle_control.cpp`](444/ws/src/demo_cpp_service/src/turtle_control.cpp "444/ws/src/demo_cpp_service/src/turtle_control.cpp") |
| 20 | [4.5.3 修改其他节点的参数](ROS2/C%2B%2B/4.5.3%20修改其他节点的参数.md) | 跨节点参数修改 | [`patrol_client.cpp`](444/ws/src/demo_cpp_service/src/patrol_client.cpp "444/ws/src/demo_cpp_service/src/patrol_client.cpp") |
| 21 | [4.6.1 使用Launch启动多个节点](ROS2/C%2B%2B/4.6.1%20使用Launch启动多个节点.md) | launch 文件与安装配置 | [`demo.launch.py`](444/ws/src/demo_cpp_service/launch/demo.launch.py "444/ws/src/demo_cpp_service/launch/demo.launch.py") |
| 22 | [4.6.2 使用launch传递参数](ROS2/python/4.6.2%20使用launch传递参数.md) | launch 里声明与获取参数 | [`demo.launch.py`](444/ws/src/demo_cpp_service/launch/demo.launch.py "444/ws/src/demo_cpp_service/launch/demo.launch.py") |
| 23 | [4.6.3 launch使用进阶](ROS2/python/4.6.3%20launch使用进阶.md) | 动作、条件、替换三大组件 | [`actions.launch.py`](444/ws/src/demo_cpp_service/launch/actions.launch.py "444/ws/src/demo_cpp_service/launch/actions.launch.py") |

### 第 5 章 · TF 与工具链

配套代码目录：[`555/ws`](555/ws)

| # | 笔记 | 内容 | 配套代码 |
| --: | :-- | :-- | :-- |
| 24 | [5.1.1 通过命令行使用TF](ROS2/工具和仿真/5.1.1%20通过命令行使用TF.md) | `tf2_tools`、TF 树导出（含 PDF 附件） | — |
| 25 | [5.2.1 从机械臂底座到相机的静态TF发布](ROS2/python/5.2.1%20从机械臂底座到相机的静态TF发布.md) | Python 静态 TF 广播 | [`static_tf_broadcast.py`](555/ws/src/demo_py_tf/demo_py_tf/static_tf_broadcast.py "555/ws/src/demo_py_tf/demo_py_tf/static_tf_broadcast.py") |
| 26 | [5.2.2 通过Python发布动态TF](ROS2/python/5.2.2%20通过Python发布动态TF.md) | Python 动态 TF 广播 | [`dynamic_tf_broadcaster.py`](555/ws/src/demo_py_tf/demo_py_tf/dynamic_tf_broadcaster.py "555/ws/src/demo_py_tf/demo_py_tf/dynamic_tf_broadcaster.py") |
| 27 | [5.2.3 通过Python查询TF关系](ROS2/python/5.2.3%20通过Python查询TF关系.md) | `Duration` 超时与四元数转换坑 | [`tf_listener.py`](555/ws/src/demo_py_tf/demo_py_tf/tf_listener.py "555/ws/src/demo_py_tf/demo_py_tf/tf_listener.py") |
| 28 | [5.3.1 通过C++发布静态TF](ROS2/C%2B%2B/5.3.1%20通过C%2B%2B发布静态TF.md) | C++ 静态 TF 广播 | [`static_tf_broadcaster.cpp`](555/ws/src/demo_cpp_tf/src/static_tf_broadcaster.cpp "555/ws/src/demo_cpp_tf/src/static_tf_broadcaster.cpp") |
| 29 | [5.3.2 通过C++发布动态TF](ROS2/C%2B%2B/5.3.2%20通过C%2B%2B发布动态TF.md) | C++ 动态 TF 广播 | [`dynamic_tf_broadcaster.cpp`](555/ws/src/demo_cpp_tf/src/dynamic_tf_broadcaster.cpp "555/ws/src/demo_cpp_tf/src/dynamic_tf_broadcaster.cpp") |
| 30 | [5.3.3 通过C++查询TF关系](ROS2/C%2B%2B/5.3.3%20通过C%2B%2B查询TF关系.md) | C++ `lookupTransform` | [`tf_listener.cpp`](555/ws/src/demo_cpp_tf/src/tf_listener.cpp "555/ws/src/demo_cpp_tf/src/tf_listener.cpp") |
| 31 | [5.4.2 数据化可视工具Rviz](ROS2/工具和仿真/5.4.2%20数据化可视工具Rviz.md) | 启动方式与配置文件 | [`display_robot_model.rviz`](666/ws/src/szcbot_description/config/display_robot_model.rviz "666/ws/src/szcbot_description/config/display_robot_model.rviz") |
| 32 | [5.5 数据记录工具ros2 bag](ROS2/工具和仿真/5.5%20数据记录工具ros2%20bag.md) | 录制与回放 | — |
| 33 | [5.6 Git进阶](ROS2/工具和仿真/5.6%20Git进阶.md) | 撤销修改、分支管理 | — |

### 第 6 章 · URDF 建模与 Gazebo 仿真

配套代码目录：[`666/ws`](666/ws)

| # | 笔记 | 内容 | 配套代码 |
| --: | :-- | :-- | :-- |
| 34 | [6.2 使用URDF创建机器人](ROS2/工具和仿真/6.2%20使用URDF创建机器人.md) | link / joint 基本结构 | [`first_robot.urdf`](666/ws/src/szcbot_description/urdf/first_robot.urdf "666/ws/src/szcbot_description/urdf/first_robot.urdf") |
| 35 | [6.2.2 在RViz中显示机器人](ROS2/工具和仿真/6.2.2%20在RViz中显示机器人.md) | `robot_state_publisher` launch | [`display_robot.launch.py`](666/ws/src/szcbot_description/launch/display_robot.launch.py "666/ws/src/szcbot_description/launch/display_robot.launch.py") · [`display_robot_model.rviz`](666/ws/src/szcbot_description/config/display_robot_model.rviz "666/ws/src/szcbot_description/config/display_robot_model.rviz") |
| 36 | [6.2.3 使用Xacro简化URDF](ROS2/工具和仿真/6.2.3%20使用Xacro简化URDF.md) | 宏与属性复用 | [`first_robot.xacro`](666/ws/src/szcbot_description/urdf/first_robot.xacro "666/ws/src/szcbot_description/urdf/first_robot.xacro") |
| 37 | [6.2.4 创建机器人及传感器部件](ROS2/工具和仿真/6.2.4%20创建机器人及传感器部件.md) | 车体、IMU、雷达、相机 | [`szcbot.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/szcbot.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/szcbot.urdf.xacro") · [`base.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/base.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/base.urdf.xacro") · [`imu.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/sensor/imu.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/sensor/imu.urdf.xacro") · [`laser.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/sensor/laser.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/sensor/laser.urdf.xacro") · [`camera.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/sensor/camera.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/sensor/camera.urdf.xacro") |
| 38 | [6.2.5 完善机器人执行器部件](ROS2/工具和仿真/6.2.5%20完善机器人执行器部件.md) | 驱动轮与万向轮 | [`whell.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/actuator/whell.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/actuator/whell.urdf.xacro") · [`caster.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/actuator/caster.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/actuator/caster.urdf.xacro") |
| 39 | [6.2.6 添加虚拟部件,贴合地面](ROS2/工具和仿真/6.2.6%20添加虚拟部件,贴合地面.md) | `base_footprint` | [`base.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/base.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/base.urdf.xacro") |
| 40 | [6.3.1 添加碰撞属性](ROS2/工具和仿真/6.3.1%20添加碰撞属性.md) | `<collision>` | [`szcbot/`](666/ws/src/szcbot_description/urdf/szcbot "666/ws/src/szcbot_description/urdf/szcbot") |
| 41 | [6.3.2 添加质量与惯性](ROS2/工具和仿真/6.3.2%20添加质量与惯性.md) | `common_inertia.xacro` 惯性宏 | [`common_inertia.xacro`](666/ws/src/szcbot_description/urdf/szcbot/common_inertia.xacro "666/ws/src/szcbot_description/urdf/szcbot/common_inertia.xacro") |
| 42 | [6.4.2 在Gazebo中加载机器人模型](ROS2/工具和仿真/6.4.2%20在Gazebo中加载机器人模型.md) | `ros_gz_sim` spawn 与世界文件 | [`gazebo_sim.launch.py`](666/ws/src/szcbot_description/launch/gazebo_sim.launch.py "666/ws/src/szcbot_description/launch/gazebo_sim.launch.py") · [`room.sdf`](666/ws/src/szcbot_description/world/room.sdf "666/ws/src/szcbot_description/world/room.sdf") |
| 43 | [6.4.3 使用Gazebo标签扩展URDF](ROS2/工具和仿真/6.4.3%20使用Gazebo标签扩展URDF.md) | 材质与摩擦参数 | [`base.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/base.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/base.urdf.xacro") · [`whell.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/actuator/whell.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/actuator/whell.urdf.xacro") |
| 44 | [6.4.4 使用两轮差速插件控制机器人](ROS2/工具和仿真/6.4.4%20使用两轮差速插件控制机器人.md) | `DiffDrive` 插件与 `bridge.yaml` 话题桥接 | [`gazebo_control_plugin.xacro`](666/ws/src/szcbot_description/urdf/szcbot/plugins/gazebo_control_plugin.xacro "666/ws/src/szcbot_description/urdf/szcbot/plugins/gazebo_control_plugin.xacro") · [`bridge.yaml`](666/ws/src/szcbot_description/config/bridge.yaml "666/ws/src/szcbot_description/config/bridge.yaml") |
| 45 | [6.4.5 激光雷达传感器仿真](ROS2/工具和仿真/6.4.5%20激光雷达传感器仿真.md) | 雷达插件与世界 SDF | [`gazebo_sensor_plugin.xacro`](666/ws/src/szcbot_description/urdf/szcbot/plugins/gazebo_sensor_plugin.xacro "666/ws/src/szcbot_description/urdf/szcbot/plugins/gazebo_sensor_plugin.xacro") · [`bridge.yaml`](666/ws/src/szcbot_description/config/bridge.yaml "666/ws/src/szcbot_description/config/bridge.yaml") · [`complex_rooms.sdf`](666/ws/src/szcbot_description/world/complex_rooms.sdf "666/ws/src/szcbot_description/world/complex_rooms.sdf") |
| 46 | [6.4.6 惯性测量传感器仿真](ROS2/工具和仿真/6.4.6%20惯性测量传感器仿真.md) | IMU 插件 | [`gazebo_sensor_plugin.xacro`](666/ws/src/szcbot_description/urdf/szcbot/plugins/gazebo_sensor_plugin.xacro "666/ws/src/szcbot_description/urdf/szcbot/plugins/gazebo_sensor_plugin.xacro") · [`bridge.yaml`](666/ws/src/szcbot_description/config/bridge.yaml "666/ws/src/szcbot_description/config/bridge.yaml") |
| 47 | [6.4.7 深度相机传感器仿真](ROS2/工具和仿真/6.4.7%20深度相机传感器仿真.md) | RGBD 相机插件 | [`gazebo_sensor_plugin.xacro`](666/ws/src/szcbot_description/urdf/szcbot/plugins/gazebo_sensor_plugin.xacro "666/ws/src/szcbot_description/urdf/szcbot/plugins/gazebo_sensor_plugin.xacro") · [`camera.urdf.xacro`](666/ws/src/szcbot_description/urdf/szcbot/sensor/camera.urdf.xacro "666/ws/src/szcbot_description/urdf/szcbot/sensor/camera.urdf.xacro") |
| 48 | [6.5.2 使用 Gazebo 接入 ros2_control](ROS2/工具和仿真/6.5.2%20使用%20Gazebo%20接入%20ros2_control.md) | `GazeboSimSystem` 与控制器配置 | [`szcbot.ros2_control.xacro`](666/ws/src/szcbot_description/urdf/szcbot/szcbot.ros2_control.xacro "666/ws/src/szcbot_description/urdf/szcbot/szcbot.ros2_control.xacro") · [`szcbot_ros2_controller.yaml`](666/ws/src/szcbot_description/config/szcbot_ros2_controller.yaml "666/ws/src/szcbot_description/config/szcbot_ros2_controller.yaml") |
| 49 | [6.5.3 使用关节状态发布控制器](ROS2/工具和仿真/6.5.3%20使用关节状态发布控制器.md) | `joint_state_broadcaster` | [`szcbot_ros2_controller.yaml`](666/ws/src/szcbot_description/config/szcbot_ros2_controller.yaml "666/ws/src/szcbot_description/config/szcbot_ros2_controller.yaml") · [`gazebo_sim.launch.py`](666/ws/src/szcbot_description/launch/gazebo_sim.launch.py "666/ws/src/szcbot_description/launch/gazebo_sim.launch.py") |
| 50 | [6.5.4 使用力控制器控制轮子](ROS2/工具和仿真/6.5.4%20使用力控制器控制轮子.md) | `effort_controllers` | [`szcbot_ros2_controller.yaml`](666/ws/src/szcbot_description/config/szcbot_ros2_controller.yaml "666/ws/src/szcbot_description/config/szcbot_ros2_controller.yaml") · [`gazebo_sim.launch.py`](666/ws/src/szcbot_description/launch/gazebo_sim.launch.py "666/ws/src/szcbot_description/launch/gazebo_sim.launch.py") |
| 51 | [6.5.5 使用两轮差速控制器控制机器人](ROS2/工具和仿真/6.5.5%20使用两轮差速控制器控制机器人.md) | `diff_drive_controller` 与 `TwistStamped` 转换排错 | [`szcbot_ros2_controller.yaml`](666/ws/src/szcbot_description/config/szcbot_ros2_controller.yaml "666/ws/src/szcbot_description/config/szcbot_ros2_controller.yaml") · [`twist_to_stamped.py`](666/ws/src/szcbot_description/src/twist_to_stamped.py "666/ws/src/szcbot_description/src/twist_to_stamped.py") · [`gazebo_sim.launch.py`](666/ws/src/szcbot_description/launch/gazebo_sim.launch.py "666/ws/src/szcbot_description/launch/gazebo_sim.launch.py") |

### 第 7 章 · SLAM 建图与 Nav2 导航

配套代码目录：[`777/ws`](777/ws)

| # | 笔记 | 内容 | 配套代码 |
| --: | :-- | :-- | :-- |
| 52 | [7.2.2 将地图保存为文件](ROS2/导航/7.2.2%20将地图保存为文件.md) | `map_saver` 与 `room.yaml` | [`room.yaml`](777/ws/src/szcbot_navigation2/maps/room.yaml "777/ws/src/szcbot_navigation2/maps/room.yaml") |
| 53 | [7.3.3 编写launch并启动导航](ROS2/导航/7.3.3%20编写launch并启动导航.md) | `nav2_params.yaml` 与导航 launch | [`navigation2.launch.py`](777/ws/src/szcbot_navigation2/launch/navigation2.launch.py "777/ws/src/szcbot_navigation2/launch/navigation2.launch.py") · [`nav2_params.yaml`](777/ws/src/szcbot_navigation2/config/nav2_params.yaml "777/ws/src/szcbot_navigation2/config/nav2_params.yaml") |
| 54 | [7.3.4 进行单点与路点导航](ROS2/导航/7.3.4%20进行单点与路点导航.md) | RViz 中下发目标 | [`navigation2.launch.py`](777/ws/src/szcbot_navigation2/launch/navigation2.launch.py "777/ws/src/szcbot_navigation2/launch/navigation2.launch.py") |
| 55 | [7.3.7 优化导航速度和膨胀半径以及到点精度](ROS2/导航/7.3.7%20优化导航速度和膨胀半径以及到点精度.md) | 速度、膨胀系数、到点容差调参 | [`nav2_params.yaml`](777/ws/src/szcbot_navigation2/config/nav2_params.yaml "777/ws/src/szcbot_navigation2/config/nav2_params.yaml") |
| 56 | [7.4.1 使用话题初始化机器人位姿](ROS2/导航/7.4.1%20使用话题初始化机器人位姿.md) | `/initialpose` | [`init_robot_pose.py`](777/ws/src/szcbot_application/szcbot_application/init_robot_pose.py "777/ws/src/szcbot_application/szcbot_application/init_robot_pose.py") |
| 57 | [7.4.2 使用TF获取机器人实时位置](ROS2/导航/7.4.2%20使用TF获取机器人实时位置.md) | Python 与 C++ 两版实现 | [`get_robot_pose.py`](777/ws/src/szcbot_application/szcbot_application/get_robot_pose.py "777/ws/src/szcbot_application/szcbot_application/get_robot_pose.py") · [`get_robot_pose_cpp.cpp`](777/ws/src/szcbot_application_cpp/src/get_robot_pose_cpp.cpp "777/ws/src/szcbot_application_cpp/src/get_robot_pose_cpp.cpp") |
| 58 | [7.4.3 调用接口进行单点导航](ROS2/导航/7.4.3%20调用接口进行单点导航.md) | `NavigateToPose` action | [`nav_to_pose.py`](777/ws/src/szcbot_application/szcbot_application/nav_to_pose.py "777/ws/src/szcbot_application/szcbot_application/nav_to_pose.py") |
| 59 | [7.4.4 使用接口完成路点导航](ROS2/导航/7.4.4%20使用接口完成路点导航.md) | `FollowWaypoints` action | [`waypoint_follower.py`](777/ws/src/szcbot_application/szcbot_application/waypoint_follower.py "777/ws/src/szcbot_application/szcbot_application/waypoint_follower.py") |
| 60 | [7.5.2 编写巡检控制节点](ROS2/导航/7.5.2%20编写巡检控制节点.md) | 自动巡检节点与 YAML 配置 | [`partol_node.py`](777/ws/src/autopartol_robot/autopartol_robot/partol_node.py "777/ws/src/autopartol_robot/autopartol_robot/partol_node.py") · [`partol_config.yaml`](777/ws/src/autopartol_robot/config/partol_config.yaml "777/ws/src/autopartol_robot/config/partol_config.yaml") · [`autopatrol.launch.py`](777/ws/src/autopartol_robot/launch/autopatrol.launch.py "777/ws/src/autopartol_robot/launch/autopatrol.launch.py") |
| 61 | [7.5.3 添加语音播报功能](ROS2/导航/7.5.3%20添加语音播报功能.md) | 自定义 `SpeechText.srv` + espeak 服务端 | [`SpeechText.srv`](777/ws/src/autopartol_interfaces/srv/SpeechText.srv "777/ws/src/autopartol_interfaces/srv/SpeechText.srv") · [`speaker.py`](777/ws/src/autopartol_robot/autopartol_robot/speaker.py "777/ws/src/autopartol_robot/autopartol_robot/speaker.py") · [`partol_node.py`](777/ws/src/autopartol_robot/autopartol_robot/partol_node.py "777/ws/src/autopartol_robot/autopartol_robot/partol_node.py") |
| 62 | [7.5.4 订阅图像并记录](ROS2/导航/7.5.4%20订阅图像并记录.md) | 巡检抓图落盘与话题桥接补充 | [`partol_node.py`](777/ws/src/autopartol_robot/autopartol_robot/partol_node.py "777/ws/src/autopartol_robot/autopartol_robot/partol_node.py") · [`bridge.yaml`](777/ws/src/szcbot_description/config/bridge.yaml "777/ws/src/szcbot_description/config/bridge.yaml") |

### 第 8 章 · 插件机制与 Nav2 自定义插件

配套代码目录：[`888/`](888/)

| # | 笔记 | 内容 | 配套代码 |
| --: | :-- | :-- | :-- |
| 63 | [8.1.3 创建插件](ROS2/导航/8.1.3%20创建插件.md) | pluginlib 基类与三个运动控制器实现 | [`motion_control_interface.hpp`](888/learn_pluginlib/src/motion_control_system/include/motion_control_system/motion_control_interface.hpp "888/learn_pluginlib/src/motion_control_system/include/motion_control_system/motion_control_interface.hpp") · [`linear_motion_controller.cpp`](888/learn_pluginlib/src/motion_control_system/src/linear_motion_controller.cpp "888/learn_pluginlib/src/motion_control_system/src/linear_motion_controller.cpp") · [`spin_motion_controller.cpp`](888/learn_pluginlib/src/motion_control_system/src/spin_motion_controller.cpp "888/learn_pluginlib/src/motion_control_system/src/spin_motion_controller.cpp") · [`zshaped_motion_controller.cpp`](888/learn_pluginlib/src/motion_control_system/src/zshaped_motion_controller.cpp "888/learn_pluginlib/src/motion_control_system/src/zshaped_motion_controller.cpp") |
| 64 | [8.1.4 编写插件测试程序](ROS2/导航/8.1.4%20编写插件测试程序.md) | 插件加载测试与动态库检查 | [`test_plugin.cpp`](888/learn_pluginlib/src/motion_control_system/src/test_plugin.cpp "888/learn_pluginlib/src/motion_control_system/src/test_plugin.cpp") · [`CMakeLists.txt`](888/learn_pluginlib/src/motion_control_system/CMakeLists.txt "888/learn_pluginlib/src/motion_control_system/CMakeLists.txt") |
| 65 | [8.2 配置自定义导航并测试](ROS2/导航/8.2%20配置自定义导航并测试.md) | 自定义 Nav2 全局规划器（含 Jazzy 接口变更） | [`nav2_custom_planner.cpp`](888/ws/src/nav2_custom_planner/src/nav2_custom_planner.cpp "888/ws/src/nav2_custom_planner/src/nav2_custom_planner.cpp") · [`nav2_custom_planner.hpp`](888/ws/src/nav2_custom_planner/include/nav2_custom_planner/nav2_custom_planner.hpp "888/ws/src/nav2_custom_planner/include/nav2_custom_planner/nav2_custom_planner.hpp") · [`custom_planner_plugin.xml`](888/ws/src/nav2_custom_planner/custom_planner_plugin.xml "888/ws/src/nav2_custom_planner/custom_planner_plugin.xml") · [`nav2_params.yaml`](888/ws/src/szcbot_navigation2/config/nav2_params.yaml "888/ws/src/szcbot_navigation2/config/nav2_params.yaml") |
| 66 | [8.3 配置自定义导航控制器并测试](ROS2/导航/8.3%20配置自定义导航控制器并测试.md) | 自定义 Nav2 局部控制器 | [`custom_controller.cpp`](888/ws/src/nav2_custom_controller/src/custom_controller.cpp "888/ws/src/nav2_custom_controller/src/custom_controller.cpp") · [`custom_controller.hpp`](888/ws/src/nav2_custom_controller/include/nav2_custom_controller/custom_controller.hpp "888/ws/src/nav2_custom_controller/include/nav2_custom_controller/custom_controller.hpp") · [`nav2_custom_controller.xml`](888/ws/src/nav2_custom_controller/nav2_custom_controller.xml "888/ws/src/nav2_custom_controller/nav2_custom_controller.xml") · [`nav2_params.yaml`](888/ws/src/szcbot_navigation2/config/nav2_params.yaml "888/ws/src/szcbot_navigation2/config/nav2_params.yaml") |

### 第 9 章 · 实体机器人（ESP32 + micro-ROS）

配套代码目录：[`999/`](999/)

| # | 笔记 | 内容 | 配套代码 |
| --: | :-- | :-- | :-- |
| 67 | [9.1 主要配置](ROS2/实战/9.1%20主要配置.md) | WiFi / UDP 配置、micro-ROS Agent 与雷达驱动 Docker | [`udpserver.py`](999/ws/src/ros_serial2wifi/ros_serial2wifi/udpserver.py "999/ws/src/ros_serial2wifi/ros_serial2wifi/udpserver.py") |
| 68 | [9.2 硬件](ROS2/实战/9.2%20硬件.md) | 电机参数、ESP32 与 PlatformIO 工程流程 | [`platformio.ini`](999/example_led/platformio.ini "999/example_led/platformio.ini") · [`main.cpp`](999/example_led/src/main.cpp "999/example_led/src/main.cpp") |
| 69 | [9.3 PID控制，运动学正逆解，里程计计算](ROS2/实战/9.3%20PID控制，运动学正逆解，里程计计算.md) | `PidController` 与 `Kinematics` 实现 | [`PidController.cpp`](999/example_motor/lib/PidController/PidController.cpp "999/example_motor/lib/PidController/PidController.cpp") · [`Kinematics.cpp`](999/example_motor/lib/Kinematics/Kinematics.cpp "999/example_motor/lib/Kinematics/Kinematics.cpp") · [`main.cpp`](999/example_motor/src/main.cpp "999/example_motor/src/main.cpp") |
| 70 | [9.4.1 microROS初始化和节点](ROS2/实战/9.4.1%20microROS初始化和节点.md) | Agent 启动与固件端节点 | [`platformio.ini`](999/example_project/platformio.ini "999/example_project/platformio.ini") · [`main.cpp`](999/example_project/src/main.cpp "999/example_project/src/main.cpp") |
| 71 | [9.4.2 订阅话题控制机器人](ROS2/实战/9.4.2%20订阅话题控制机器人.md) | 固件端订阅 `cmd_vel` | [`main.cpp`](999/example_project/src/main.cpp "999/example_project/src/main.cpp") |
| 72 | [9.4.3 发布机器人里程计话题](ROS2/实战/9.4.3%20发布机器人里程计话题.md) | 固件端发布 `odom` | [`main.cpp`](999/example_project/src/main.cpp "999/example_project/src/main.cpp") |
| 73 | [9.5.1 驱动并显示雷达点云](ROS2/实战/9.5.1%20驱动并显示雷达点云.md) | YDLidar 驱动与串口转发配置 | [`tcpserver.py`](999/ws/src/ros_serial2wifi/ros_serial2wifi/tcpserver.py "999/ws/src/ros_serial2wifi/ros_serial2wifi/tcpserver.py") |
| 74 | [9.5.3 准备机器人URDF](ROS2/实战/9.5.3%20准备机器人URDF.md) | 实车 URDF 与 `urdf2tf.launch.py` | [`szcbot.urdf`](999/ws/src/szcbot_description/urdf/szcbot.urdf "999/ws/src/szcbot_description/urdf/szcbot.urdf") · [`urdf2tf.launch.py`](999/ws/src/szcbot_bringup/launch/urdf2tf.launch.py "999/ws/src/szcbot_bringup/launch/urdf2tf.launch.py") |
| 75 | [9.5.4 发布里程计TF](ROS2/实战/9.5.4%20发布里程计TF.md) | `odom2tf.cpp` | [`odom2tf.cpp`](999/ws/src/szcbot_bringup/src/odom2tf.cpp "999/ws/src/szcbot_bringup/src/odom2tf.cpp") |
| 76 | [9.5.5 完成机器人建图并保存地图](ROS2/实战/9.5.5%20完成机器人建图并保存地图.md) | slam_toolbox 建图与雷达 QoS 匹配 | [`bringup.launch.py`](999/ws/src/szcbot_bringup/launch/bringup.launch.py "999/ws/src/szcbot_bringup/launch/bringup.launch.py") · [`slam_toolbox.yaml`](999/ws/src/szcbot_bringup/config/slam_toolbox.yaml "999/ws/src/szcbot_bringup/config/slam_toolbox.yaml") |
| 77 | [9.5.6 完成导航](ROS2/实战/9.5.6%20完成导航.md) | 实车 Nav2 上线 | [`navigation2.launch.py`](999/ws/src/szcbot_navigation2/launch/navigation2.launch.py "999/ws/src/szcbot_navigation2/launch/navigation2.launch.py") · [`nav2_params.yaml`](999/ws/src/szcbot_navigation2/config/nav2_params.yaml "999/ws/src/szcbot_navigation2/config/nav2_params.yaml") |

### 第 10 章 · 进阶专题

配套代码目录：[`10/`](10/)

| # | 笔记 | 内容 | 配套代码 |
| --: | :-- | :-- | :-- |
| 78 | [10.1.1 QoS策略](ROS2/实战/10.1.1%20QoS策略.md) | History / Reliability / Durability / Deadline / Lifespan / Liveliness | — |
| 79 | [10.1.2 QoS的兼容性](ROS2/实战/10.1.2%20QoS的兼容性.md) | 发布端与订阅端策略兼容矩阵 | — |
| 80 | [10.1.3 QoS的兼容性测试](ROS2/实战/10.1.3%20QoS的兼容性测试.md) | Python 与 C++ 可靠性测试节点 | [`reliability_test.cpp`](10/ws/src/learn_qos_cpp/src/reliability_test.cpp "10/ws/src/learn_qos_cpp/src/reliability_test.cpp") · [`reliability_test.py`](10/ws/src/learn_qos_py/learn_qos_py/reliability_test.py "10/ws/src/learn_qos_py/learn_qos_py/reliability_test.py") |
| 81 | [10.2.1 执行器与回调组](ROS2/实战/10.2.1%20执行器与回调组.md) | 单线程 / 多线程执行器与互斥、可重入回调组 | [`learn_executor.cpp`](10/ws/src/learn_executor_cpp/src/learn_executor.cpp "10/ws/src/learn_executor_cpp/src/learn_executor.cpp") · [`learn_executor.py`](10/ws/src/learn_executor_py/learn_executor_py/learn_executor.py "10/ws/src/learn_executor_py/learn_executor_py/learn_executor.py") |
| 82 | [10.3.1 生命周期节点](ROS2/实战/10.3.1%20生命周期节点.md) | 状态机、`ros2 lifecycle` 命令与两版实现 | [`learn_lifecyclenode.cpp`](10/ws/src/learn_lifecyclenode_cpp/src/learn_lifecyclenode.cpp "10/ws/src/learn_lifecyclenode_cpp/src/learn_lifecyclenode.cpp") · [`learn_lifecyclenode.py`](10/ws/src/learn_lifecyclenode_py/learn_lifecyclenode_py/learn_lifecyclenode.py "10/ws/src/learn_lifecyclenode_py/learn_lifecyclenode_py/learn_lifecyclenode.py") |
| 83 | [10.4.1 使用执行器组织多个节点](ROS2/实战/10.4.1%20使用执行器组织多个节点.md) | 进程内通信（intra-process） | [`talker.cpp`](10/ws/src/learn_compose/src/talker.cpp "10/ws/src/learn_compose/src/talker.cpp") · [`listener.cpp`](10/ws/src/learn_compose/src/listener.cpp "10/ws/src/learn_compose/src/listener.cpp") · [`intra_process_pubsub.cpp`](10/ws/src/learn_compose/src/intra_process_pubsub.cpp "10/ws/src/learn_compose/src/intra_process_pubsub.cpp") |
| 84 | [10.4.2 使用组件运行组合节点](ROS2/实战/10.4.2%20使用组件运行组合节点.md) | `ros2 component` 加载 / 卸载 | [`learn_compose/`](10/ws/src/learn_compose "10/ws/src/learn_compose") |
| 85 | [10.4.3 编写组件](ROS2/实战/10.4.3%20编写组件.md) | `RCLCPP_COMPONENTS_REGISTER_NODE` 与 CMake 导出 | [`talker.cpp`](10/ws/src/learn_compose/src/talker.cpp "10/ws/src/learn_compose/src/talker.cpp") · [`listener.cpp`](10/ws/src/learn_compose/src/listener.cpp "10/ws/src/learn_compose/src/listener.cpp") · [`CMakeLists.txt`](10/ws/src/learn_compose/CMakeLists.txt "10/ws/src/learn_compose/CMakeLists.txt") |
| 86 | [10.5.1 同步传感器数据](ROS2/实战/10.5.1%20同步传感器数据.md) | `message_filters` 时间同步（双语言实现） | [`timesync.cpp`](10/ws/src/learn_msg_filter_cpp/src/timesync.cpp "10/ws/src/learn_msg_filter_cpp/src/timesync.cpp") · [`timesync.py`](10/ws/src/learn_msg_filter_py/learn_msg_filter_py/timesync.py "10/ws/src/learn_msg_filter_py/learn_msg_filter_py/timesync.py") · [`rosbag2_message_filter/`](10/rosbag2_message_filter "10/rosbag2_message_filter") |
| 87 | [10.6.1 使用不同的DDS进行通信](ROS2/实战/10.6.1%20使用不同的DDS进行通信.md) | Fast DDS / CycloneDDS / Zenoh 切换 | — |
| 88 | [10.6.2 配置局域网通信](ROS2/实战/10.6.2%20配置局域网通信.md) | `ROS_DOMAIN_ID` 与本机通信限制 | — |
| 89 | [10.6.3 调整DDS配置](ROS2/实战/10.6.3%20调整DDS配置.md) | XML profile 限制订阅 | [`topic_sub_limit.xml`](10/ws/topic_sub_limit.xml "10/ws/topic_sub_limit.xml") |
| 90 | [10.6.4 使用DDS共享内存](ROS2/实战/10.6.4%20使用DDS共享内存.md) | 共享内存传输与 loaned message | [`shm.xml`](10/ws/shm.xml "10/ws/shm.xml") · [`shm_pub.cpp`](10/ws/src/learn_dds_cpp/src/shm_pub.cpp "10/ws/src/learn_dds_cpp/src/shm_pub.cpp") |

---

## 仓库结构

```
.
├── ROS2/                   # 全部笔记（Markdown）
│   ├── ROS2基础.md         # 通信方式与应用框架概览
│   ├── ROS2相关命令.md     # ros2 命令行速查
│   ├── ROS2 版本.md        # 各发行版与 EOL 时间表
│   ├── Linux命令.md        # 常用 Linux / 安装命令
│   ├── python/             # 第 2–5 章 Python 实现
│   ├── C++/                # 第 2–5 章 C++ 实现，含 C++ 速成
│   ├── 工具和仿真/         # 第 5–6 章 TF、RViz、bag、URDF、Gazebo
│   ├── 导航/               # 第 7–8 章 Nav2 导航与自定义插件
│   └── 实战/               # 第 9–10 章 实体机器人与进阶专题
│
├── _resources/             # 笔记附件，按笔记标题分子目录
│   └── <笔记标题>/<md5>_MD5.jpg|pdf
│
├── 111/ 222/ ... 999/ 10/  # 第 1–10 章配套代码，详见「环境与依赖」
├── LICENSE                 # Apache-2.0
└── .gitignore              # 已忽略 build/ install/ log/ .pio/ 等构建产物
```

代码目录以重复数字标识章号：`111` 为第 1 章，`222` 为第 2 章，依此类推至 `999` 为第 9 章，
第 10 章为 `10`。同名功能包（`szcbot_description`、`szcbot_navigation2`、`autopartol_robot`）
在多个章节目录下各存一份，为该章当时的快照，请按章号取用。

---

## 环境与依赖

笔记基于下列环境编写，其他版本的差异在正文中另行标注。

| 项目 | 版本 / 型号 |
| :-- | :-- |
| 操作系统 | Ubuntu 24.04.4 LTS（Noble Numbat） |
| ROS 2 | Jazzy Jalisco |
| 仿真器 | Gazebo Sim（Harmonic / Ionic，需 `ros_gz` 桥接） |
| 导航 | Nav2 + slam_toolbox |
| 控制框架 | `ros2_control` + `gz_ros2_control` |
| 单片机 | ESP32（PlatformIO + Arduino framework） |
| 嵌入式通信 | micro-ROS（UDP，micro-ROS Agent 运行于 Docker） |
| 雷达 | YDLidar |
| 电机 | 12V 370 减速电机，130 rpm，编码器一圈 1974 脉冲，轮径 65 mm |

> [!NOTE]
> 自 Humble（Gazebo Classic）迁移至 Jazzy（Gazebo Sim）的差异，见
> [`Gazebo版本迁移指南.md`](666/ws/src/szcbot_description/Gazebo%E7%89%88%E6%9C%AC%E8%BF%81%E7%A7%BB%E6%8C%87%E5%8D%97.md)。
> Jazzy 引入的 API 变更（如 Nav2 插件的 `cancel_checker`、异常头文件拆分）在 8.2、8.3 中有标注。

### 各章工作空间

工作空间路径按章而异，编译前请对照下表，勿统一套用 `<章号>/ws`。

| 章 | 工作空间 | 内容 |
| :-- | :-- | :-- |
| 第 1 章 | [`111/`](111/) | 裸 CMake / Python 示例，无 colcon 工作空间 |
| 第 2 章 | [`222/ws`](222/ws) | `demo_cpp_pkg`、`demo_py_pkg` |
| 第 3 章 | [`333/topic_ws`](333/topic_ws) · [`333/topic_practice_ws`](333/topic_practice_ws) | 话题示例与系统监控实践 |
| 第 4 章 | [`444/ws`](444/ws) | 服务、参数、Launch |
| 第 5 章 | [`555/ws`](555/ws) | `demo_cpp_tf`、`demo_py_tf` |
| 第 6 章 | [`666/ws`](666/ws) | `szcbot_description`（URDF + Gazebo + ros2_control） |
| 第 7 章 | [`777/ws`](777/ws) | `szcbot_navigation2`、`autopartol_robot` |
| 第 8 章 | [`888/learn_pluginlib`](888/learn_pluginlib) · [`888/ws`](888/ws) | pluginlib 示例与 Nav2 自定义插件 |
| 第 9 章 · 上位机 | [`999/ws`](999/ws) | bringup、雷达驱动、串口转发 |
| 第 9 章 · 固件 | [`999/example_led`](999/example_led) · [`999/example_motor`](999/example_motor) · [`999/example_imu`](999/example_imu) · [`999/example_project`](999/example_project) | ESP32（PlatformIO） |
| 第 10 章 | [`10/ws`](10/ws) | QoS、执行器、生命周期节点、组件、DDS |

### 编译

```bash
cd 666/ws          # 替换为上表中对应的工作空间
colcon build
source install/setup.bash
ros2 run szcbot_description <可执行文件名>
```

第 9 章的 ESP32 固件以 PlatformIO 构建：

```bash
cd 999/example_led   # 替换为上表中对应的固件工程
pio run -t upload
```

> [!NOTE]
> `build/`、`install/`、`log/`、`.pio/` 等构建产物已在 `.gitignore` 中忽略，克隆后需自行编译。

---

## 参考

- [ROS 2 官方文档（Jazzy）](https://docs.ros.org/en/jazzy/)
- [Nav2 文档](https://docs.nav2.org/)
- [Gazebo 文档](https://gazebosim.org/docs)
- [ros2_control 文档](https://control.ros.org/)
- [micro-ROS](https://micro.ros.org/)

---

## 许可证

本仓库以 [Apache License 2.0](LICENSE) 发布。
